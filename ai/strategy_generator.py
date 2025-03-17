# ai/strategy_generator.py
from typing import Dict, List, Optional
from dataclasses import dataclass
from decimal import Decimal
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

@dataclass
class StrategyStep:
    protocol: str
    action: str
    token: str
    amount: Decimal
    expected_apy: Decimal
    token_to: Optional[str] = None
    pair: Optional[str] = None
    interest_rate: Optional[int] = None
    usdq_amount: Optional[Decimal] = None

@dataclass
class Strategy:
    name: str  # Added name field for Anchor, Zenith, Wildcard
    risk_level: int
    steps: List[StrategyStep]
    explanation: str
    total_expected_apy: Decimal
    risk_factors: List[str]

class StrategyGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Token name mapping (from service to frontend display)
        self.token_mapping = {
            "WETH": "ETH",   # Map WETH to ETH for user-friendly display
            "SCR": "SRC",    # In case the API returns SCR instead of SRC
            # Add other mappings as needed
        }
        
        # Reverse mapping for converting back
        self.reverse_token_mapping = {v: k for k, v in self.token_mapping.items()}
        
    def prepare_context(
        self,
        wallet_data: Dict,
        market_data: Dict,
        risk_metrics: Dict
    ) -> str:
        """Prepare context for LLM prompt with token name mapping"""
        
        # Map AAVE token names to frontend display names
        # For rates in market data
        mapped_rates = {}
        if "rates" in market_data and "AAVE" in market_data["rates"]:
            aave_rates = market_data["rates"]["AAVE"]
            mapped_rates["AAVE"] = {}
            
            for rate_type in ["supply_apy", "borrow_apy"]:
                if rate_type in aave_rates:
                    mapped_rates["AAVE"][rate_type] = {}
                    for token, value in aave_rates[rate_type].items():
                        # Map token names like WETH -> ETH for the prompt
                        display_name = self.token_mapping.get(token, token)
                        mapped_rates["AAVE"][rate_type][display_name] = value
        
        # Include Quill data if available
        if "protocol" in market_data and market_data["protocol"] == "Quill":
            mapped_rates["Quill"] = {
                "collateral_factors": market_data.get("collateral_factors", {}),
                "stability_pool_apy": market_data.get("stability_pool_apy", 5.0),
                "interest_rates": market_data.get("interest_rates", {
                    "min": 6.0,
                    "max": 350.0,
                    "recommended": {
                        "low_risk": 6.0,
                        "medium_risk": 10.0,
                        "high_risk": 15.0
                    }
                })
            }
        
        # Create the final context
        context = {
            "wallet": {
                "balances": wallet_data,
                "current_positions": None,  # To be implemented
                "risk_metrics": risk_metrics
            },
            "market": {
                "apy_rates": mapped_rates or market_data.get("rates"),
                "tvl": market_data.get("tvl"),
                "conditions": market_data.get("conditions"),
                "dex": market_data.get("dex", {}),
                "quill": market_data.get("protocol") == "Quill" and market_data or None
            }
        }
        return json.dumps(context, indent=2)
        
    # Add this method to your ai/strategy_generator.py

    def _build_prompt(self, context: str, strategy_type: str) -> str:
        """Build the prompt for strategy generation
        
        Args:
            context: JSON string with wallet and market data
            strategy_type: "Anchor" (conservative), "Zenith" (balanced), or "Wildcard" (aggressive)
        """
        # Parse the context string to extract wallet balances
        try:
            context_dict = json.loads(context)
            wallet_balances = context_dict.get("wallet", {}).get("balances", {})
            eth_balance = wallet_balances.get("ETH", 0)
            usdc_balance = wallet_balances.get("USDC", 0)
            src_balance = wallet_balances.get("SRC", 0)
        except (json.JSONDecodeError, AttributeError):
            # Fallback if parsing fails
            eth_balance = "unknown"
            usdc_balance = "unknown"
            src_balance = "unknown"
        
        # Strategy descriptions and risk levels based on frontend
        strategy_descriptions = {
            "Anchor": {
                "description": "Conservative strategy focused on steady growth over time. Should prioritize low-risk activities with minimal volatility.",
                "risk_level": 1,
                "target_apy": "around 3.8%"
            },
            "Zenith": {
                "description": "Balanced performance strategy that creates moderate leverage while maintaining reasonable risk levels.",
                "risk_level": 3,
                "target_apy": "around 5.5%"
            },
            "Wildcard": {
                "description": "Aggressive strategy for risk-takers that maximizes yield through leveraging and higher-risk positions.",
                "risk_level": 5,
                "target_apy": "around 8.9%"
            }
        }
        
        # Get the specific strategy details
        strategy_info = strategy_descriptions.get(strategy_type, strategy_descriptions["Anchor"])
        
        return f"""You are an AI-powered DeFi strategy generator for the Scroll network. Based on the following wallet and market data:
        {context}
        
        Generate a {strategy_type} strategy ({strategy_info["description"]})
        This should be a risk level {strategy_info["risk_level"]} strategy with an expected APY of {strategy_info["target_apy"]}.
        
        You can use AAVE for lending/borrowing, Ambient DEX for swapping tokens or providing liquidity, and Quill Finance for borrowing USDQ stablecoin against collateral.
        
        IMPORTANT RULES:
        1. NEVER recommend using more tokens than available in the wallet.
        2. NEVER reuse tokens already allocated in previous steps.
        3. CAREFULLY track available balances through all steps.
        4. Keep proposed amounts PROPORTIONAL to wallet balances.
        5. For small wallets (less than $100 total value), use CONSERVATIVE amounts.
        6. USDQ borrowing amounts should be REASONABLE and no more than 20% of total wallet value.
        
        Strategy Guidelines:
        - Anchor: Conservative strategy focused on low-risk activities like USDC supply on AAVE, providing stable liquidity to low-volatility pairs on Ambient DEX, or maintaining well-collateralized positions on Quill.
        - Zenith: Balanced strategy may involve borrowing from AAVE or Quill, then redeploying assets to generate additional yield, while maintaining reasonable health factors and collateral ratios.
        - Wildcard: Aggressive strategy that can use recursive leveraging with multiple protocols, concentrated liquidity positions, or higher leverage positions on Quill with lower interest rates to boost yields.
        
        Available Protocols:
        1. AAVE - For lending and borrowing
        - Actions: "supply", "borrow", "withdraw", "repay"
        - Example: {{ "protocol": "AAVE", "action": "supply", "token": "USDC", "amount": 5.0, "expected_apy": 2.2 }}
        
        2. Ambient DEX - For token swaps and liquidity provision
        - Actions: "swap", "add_liquidity", "remove_liquidity"
        - Example swap: {{ "protocol": "Ambient", "action": "swap", "token": "USDC", "token_to": "ETH", "amount": 2.5, "expected_apy": 0 }}
        - Example liquidity: {{ "protocol": "Ambient", "action": "add_liquidity", "pair": "ETH-USDC", "amount": 2.5, "expected_apy": 5.0 }}
        
        3. Quill Finance - For borrowing USDQ stablecoin against collateral
        - Actions: "borrow_usdq", "repay_usdq", "provide_stability"
        - Example borrow: {{ "protocol": "Quill", "action": "borrow_usdq", "token": "ETH", "amount": 0.005, "usdq_amount": 5.0, "interest_rate": 10, "expected_apy": -10.0 }}
        - Example stability: {{ "protocol": "Quill", "action": "provide_stability", "token": "USDQ", "amount": 5.0, "expected_apy": 5.0 }}
        
        Requirements:
        - Use available tokens wisely (ETH: {eth_balance}, USDC: {usdc_balance}, SRC: {src_balance})
        - Track used amounts between steps to avoid reusing the same tokens
        - Provide clear step-by-step actions
        - Include realistic APY estimates
        - Include comprehensive risk assessment
        - When using Quill, set appropriate interest rates (6% to 350%, with higher rates reducing redemption risk)
        - IMPORTANT: For small wallet balances, use proportional amounts and avoid suggesting large positions
        
        Return the strategy in the following JSON format:
        {{
            "name": "{strategy_type}",
            "risk_level": {strategy_info["risk_level"]},
            "steps": [
                {{
                    "protocol": "string",
                    "action": "string",
                    "token": "string",
                    "amount": "number",
                    "expected_apy": "number",
                    "token_to": "string",  // Only required for Ambient swaps
                    "interest_rate": "number",  // Only required for Quill borrowing
                    "usdq_amount": "number"  // Only required for Quill borrowing
                }}
            ],
            "explanation": "string",
            "total_expected_apy": "number",
            "risk_factors": ["string"]
        }}
        """
        
    def generate_strategy(
        self,
        wallet_data: Dict,
        market_data: Dict,
        risk_metrics: Dict,
        strategy_type: str
    ) -> Strategy:
        """Generate a strategy based on the provided data
        
        Args:
            wallet_data: Dictionary with token balances
            market_data: Dictionary with protocol rates and TVL
            risk_metrics: Dictionary with risk assessment metrics
            strategy_type: "Anchor" (conservative), "Zenith" (balanced), or "Wildcard" (aggressive)
            
        Returns:
            Strategy object with the generated strategy
        """
        context = self.prepare_context(wallet_data, market_data, risk_metrics)
        prompt = self._build_prompt(context, strategy_type)
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a DeFi strategy generator for the Scroll network."},
                {"role": "user", "content": prompt + "\n\nEnsure your response is valid JSON."}
            ],
            temperature=0.2,
            response_format={ "type": "json_object" }
        )
        
        try:
            # Try to parse response as JSON
            strategy_data = json.loads(response.choices[0].message.content)
            return self._parse_strategy(strategy_data)
        except json.JSONDecodeError as e:
            # If parsing fails, try to extract JSON from the response text
            content = response.choices[0].message.content
            print(f"Warning: Failed to parse response as JSON. Response content: {content[:200]}...")
            # Try fallback parsing (if the model outputs explanatory text before/after JSON)
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                try:
                    strategy_data = json.loads(json_match.group(0))
                    return self._parse_strategy(strategy_data)
                except json.JSONDecodeError:
                    raise ValueError(f"Could not extract valid JSON from response: {e}")
            else:
                raise ValueError(f"Response is not in JSON format: {e}")
        
    def generate_all_strategies(
        self,
        wallet_data: Dict,
        market_data: Dict,
        risk_metrics: Dict
    ) -> List[Strategy]:
        """Generate all three strategies (Anchor, Zenith, Wildcard)
        
        Args:
            wallet_data: Dictionary with token balances
            market_data: Dictionary with protocol rates and TVL
            risk_metrics: Dictionary with risk assessment metrics
            
        Returns:
            List of 3 Strategy objects, one for each strategy type
        """
        strategies = []
        for strategy_type in ["Anchor", "Zenith", "Wildcard"]:
            strategy = self.generate_strategy(
                wallet_data, 
                market_data, 
                risk_metrics, 
                strategy_type
            )
            strategies.append(strategy)
            
        return strategies
        
    def _parse_strategy(self, data: Dict) -> Strategy:
        """Parse the LLM response into a Strategy object"""
        steps = []
        for step in data["steps"]:
            try:
                # More robust conversion for amounts and APY values
                amount_str = str(step["amount"]).replace(',', '')
                apy_str = str(step["expected_apy"]).replace(',', '')
                
                # Handle different step types based on protocol and action
                if step["protocol"] == "Ambient" and step["action"] == "add_liquidity":
                    # For Ambient liquidity steps, use the pair field
                    pair = step.get("pair", "")
                    token = pair.split('-')[0] if pair else "UNKNOWN"
                    steps.append(StrategyStep(
                        protocol=step["protocol"],
                        action=step["action"],
                        token=token,  # Using first token from pair
                        amount=Decimal(amount_str),
                        expected_apy=Decimal(apy_str),
                        pair=pair
                    ))
                elif step["protocol"] == "Ambient" and step["action"] == "swap":
                    # Map the display token names (ETH) back to blockchain names (WETH)
                    token = step["token"]
                    token_to = step.get("token_to", "")
                    blockchain_token = self.reverse_token_mapping.get(token, token)
                    
                    steps.append(StrategyStep(
                        protocol=step["protocol"],
                        action=step["action"],
                        token=blockchain_token,  # Use the blockchain token name
                        amount=Decimal(amount_str),
                        expected_apy=Decimal(apy_str),
                        token_to=token_to
                    ))
                elif step["protocol"] == "Quill":
                    # Handle Quill-specific actions
                    token = step["token"]
                    blockchain_token = self.reverse_token_mapping.get(token, token)
                    
                    # Convert additional Quill-specific fields
                    interest_rate = step.get("interest_rate")
                    usdq_amount = step.get("usdq_amount")
                    
                    if usdq_amount:
                        usdq_amount_str = str(usdq_amount).replace(',', '')
                        usdq_amount_decimal = Decimal(usdq_amount_str)
                    else:
                        usdq_amount_decimal = None
                    
                    steps.append(StrategyStep(
                        protocol=step["protocol"],
                        action=step["action"],
                        token=blockchain_token,
                        amount=Decimal(amount_str),
                        expected_apy=Decimal(apy_str),
                        interest_rate=interest_rate,
                        usdq_amount=usdq_amount_decimal
                    ))
                else:
                    # Regular AAVE steps (supply, borrow, etc.)
                    token = step["token"]
                    blockchain_token = self.reverse_token_mapping.get(token, token)
                    
                    steps.append(StrategyStep(
                        protocol=step["protocol"],
                        action=step["action"],
                        token=blockchain_token,  # Use the blockchain token name
                        amount=Decimal(amount_str),
                        expected_apy=Decimal(apy_str)
                    ))
            except Exception as e:
                print(f"Warning: Error parsing step {step}: {e}")
                # Fallback to default values if conversion fails
                steps.append(StrategyStep(
                    protocol=step.get("protocol", "UNKNOWN"),
                    action=step.get("action", "UNKNOWN"),
                    token=step.get("token", step.get("pair", "UNKNOWN").split('-')[0] if step.get("pair") else "UNKNOWN"),
                    amount=Decimal("0"),
                    expected_apy=Decimal("0")
                ))
        
        # Also make total_expected_apy conversion more robust
        try:
            total_apy_str = str(data["total_expected_apy"]).replace(',', '')
            total_expected_apy = Decimal(total_apy_str)
        except Exception as e:
            print(f"Warning: Error parsing total_expected_apy: {e}")
            total_expected_apy = Decimal("0")
        
        return Strategy(
            name=data["name"],
            risk_level=data["risk_level"],
            steps=steps,
            explanation=data["explanation"],
            total_expected_apy=total_expected_apy,
            risk_factors=data["risk_factors"]
        )
    
    def generate_strategies_json(
        self,
        wallet_data: Dict,
        market_data: Dict,
        risk_metrics: Dict
    ) -> Dict:
        """Generate all strategies and return as JSON-serializable dict
        
        This is useful for API responses
        """
        strategies = self.generate_all_strategies(wallet_data, market_data, risk_metrics)
        
        # Get wallet balances for validation
        wallet_balances = {k: float(v) for k, v in wallet_data.items()}
        
        # Add WETH to wallet balances if ETH exists (to handle token mapping)
        if "ETH" in wallet_balances and "WETH" not in wallet_balances:
            wallet_balances["WETH"] = wallet_balances["ETH"]
        
        # Convert to JSON-serializable format with validation
        result = {
            "strategies": [
                self.validate_strategy({
                    "name": strategy.name,
                    "risk_level": strategy.risk_level,
                    "steps": [
                        {
                            "protocol": step.protocol,
                            "action": step.action,
                            "token": step.token,
                            "amount": float(step.amount),
                            "expected_apy": float(step.expected_apy),
                            **({"token_to": step.token_to} if hasattr(step, "token_to") and step.token_to else {}),
                            **({"pair": step.pair} if hasattr(step, "pair") and step.pair else {}),
                            **({"interest_rate": step.interest_rate} if hasattr(step, "interest_rate") and step.interest_rate is not None else {}),
                            **({"usdq_amount": float(step.usdq_amount)} if hasattr(step, "usdq_amount") and step.usdq_amount is not None else {})
                        }
                        for step in strategy.steps
                    ],
                    "explanation": strategy.explanation,
                    "total_expected_apy": float(strategy.total_expected_apy),
                    "risk_factors": strategy.risk_factors
                }, wallet_balances)
                for strategy in strategies
            ],
            "wallet": {
                "balances": wallet_data
            },
            "market_data": {
                "conditions": market_data.get("conditions", "stable")
            }
        }
        
        return result

    def validate_strategy(self, strategy_data: Dict, wallet_balances: Dict[str, float]) -> Dict:
        """Validate a strategy to ensure it doesn't exceed wallet balances"""
        # Create a copy of wallet balances that we'll update as we process steps
        available_balances = wallet_balances.copy()
        
        # Define token mappings for normalization
        token_mapping = {
            "WETH": "ETH",  # Map WETH to ETH
            "ETH": "ETH",
            "USDC": "USDC",
            "SRC": "SRC",
            "SCR": "SRC"   # Map SCR to SRC if needed
        }
        
        # Make sure "WETH" is in available_balances if "ETH" is
        if "ETH" in available_balances and "WETH" not in available_balances:
            available_balances["WETH"] = available_balances["ETH"]
        
        # Keep track of borrowed assets
        borrowed = {k: 0.0 for k in available_balances.keys()}
        borrowed["USDQ"] = 0.0  # Add USDQ which might not be in initial wallet
        
        # Initialize a list to store the valid steps
        valid_steps = []
        
        # Process each step and update available balances
        for i, step in enumerate(strategy_data.get("steps", [])):
            protocol = step.get("protocol", "")
            action = step.get("action", "")
            token = step.get("token", "")
            amount = float(step.get("amount", 0))
            
            # Normalize token name
            normalized_token = token_mapping.get(token, token)
            
            # Skip steps with invalid or missing fields
            if not all([protocol, action, token, amount > 0]):
                continue
            
            # Handle cross-token operations (borrowing and action consume different tokens)
            if action == "borrow_usdq":
                # Check if we have enough collateral
                if normalized_token not in available_balances or available_balances[normalized_token] < amount:
                    # Not enough balance, skip this step
                    continue
                
                # Update available balance of collateral
                available_balances[normalized_token] -= amount
                
                # Get USDQ amount
                usdq_amount = float(step.get("usdq_amount", 0))
                
                # Ensure USDQ amount is reasonable (max 20% of total wallet value in USD)
                total_wallet_value = sum(
                    available_balances.get(t, 0) * self.get_token_price(t) 
                    for t in available_balances if t != "USDQ"
                )
                max_usdq = max(5.0, total_wallet_value * 0.2)  # At least 5 USDQ
                
                if usdq_amount > max_usdq:
                    # Cap the USDQ amount to 20% of wallet value
                    usdq_amount = max_usdq
                    step["usdq_amount"] = usdq_amount
                
                # Add USDQ to available balances
                if "USDQ" not in available_balances:
                    available_balances["USDQ"] = 0
                
                available_balances["USDQ"] += usdq_amount
                valid_steps.append(step)
                continue
            
            # Handle supply/borrow to AAVE or add liquidity to Ambient
            if action in ["supply", "add_liquidity"]:
                # These actions consume tokens
                if normalized_token not in available_balances:
                    # Not a token we track, skip
                    continue
                
                if available_balances[normalized_token] < amount:
                    # Not enough balance, reduce the amount
                    amount = max(0, available_balances[normalized_token] * 0.95)  # Use 95% of available
                    if amount <= 0:
                        continue
                    step["amount"] = amount
                
                # Update available balance
                available_balances[normalized_token] -= amount
                valid_steps.append(step)
                
            elif action == "borrow":
                # Special handling for WETH/ETH
                if token == "WETH" and "ETH" in available_balances:
                    borrowed["ETH"] += amount
                    available_balances["ETH"] += amount
                    available_balances["WETH"] += amount
                else:
                    # Borrowing adds to available balance
                    if normalized_token not in available_balances:
                        available_balances[normalized_token] = 0
                    
                    borrowed[normalized_token] += amount
                    available_balances[normalized_token] += amount
                
                valid_steps.append(step)
                
            elif action == "provide_stability":
                # For providing USDQ to stability pool
                if token == "USDQ" and ("USDQ" not in available_balances or available_balances["USDQ"] < amount):
                    # Not enough USDQ, reduce the amount
                    amount = available_balances.get("USDQ", 0) * 0.95  # Use 95% of available
                    if amount <= 0:
                        continue
                    step["amount"] = amount
                
                # Update available balance
                if "USDQ" in available_balances:
                    available_balances["USDQ"] -= amount
                
                valid_steps.append(step)
        
        # Replace the original steps with our validated steps
        strategy_data["steps"] = valid_steps
        
        # If all steps were removed, add a basic strategy
        if not valid_steps:
            # Find the token with the highest balance
            best_token = max(wallet_balances.items(), key=lambda x: x[1] * self.get_token_price(x[0]))[0]
            
            # Add a simple AAVE supply step
            strategy_data["steps"] = [{
                "protocol": "AAVE",
                "action": "supply",
                "token": best_token,
                "amount": wallet_balances[best_token] * 0.9,  # Use 90% of available balance
                "expected_apy": 2.0  # Fallback APY
            }]
            
            # Update explanation
            strategy_data["explanation"] = f"A simple strategy supplying {best_token} on AAVE for stable yield."
            
            # Update risk factors
            strategy_data["risk_factors"] = ["Minimal risk with single asset deposit"]
        
        # Recalculate the total expected APY based on valid steps
        total_apy = 0.0
        for step in strategy_data["steps"]:
            step_apy = float(step.get("expected_apy", 0))
            # Use absolute value for borrowing (which has negative APY)
            total_apy += abs(step_apy) if step_apy < 0 else step_apy
        
        # Average the APY based on number of steps (but ensure it's at least 1%)
        avg_apy = max(1.0, total_apy / max(1, len(strategy_data["steps"])))
        strategy_data["total_expected_apy"] = avg_apy
        
        return strategy_data

    def get_token_price(self, token: str) -> float:
        """Get estimated price for a token (simplified version)"""
        # Simplified token prices for validation purposes
        prices = {
            "ETH": 2000.0,
            "WETH": 2000.0,
            "USDC": 1.0,
            "SRC": 10.0,
            "SCR": 10.0,
            "USDQ": 1.0
        }
        return prices.get(token, 1.0)