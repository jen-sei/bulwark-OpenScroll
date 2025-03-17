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
        
    def _build_prompt(self, context: str, strategy_type: str) -> str:
        """Build the prompt for strategy generation
        
        Args:
            context: JSON string with wallet and market data
            strategy_type: "Anchor" (conservative), "Zenith" (balanced), or "Wildcard" (aggressive)
        """
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
        
        Strategy Guidelines:
        - Anchor: Conservative strategy focused on low-risk activities like USDC supply on AAVE, providing stable liquidity to low-volatility pairs on Ambient DEX, or maintaining well-collateralized positions on Quill.
        - Zenith: Balanced strategy may involve borrowing from AAVE or Quill, then redeploying assets to generate additional yield, while maintaining reasonable health factors and collateral ratios.
        - Wildcard: Aggressive strategy that can use recursive leveraging with multiple protocols, concentrated liquidity positions, or higher leverage positions on Quill with lower interest rates to boost yields.
        
        Available Protocols:
        1. AAVE - For lending and borrowing
        - Actions: "supply", "borrow", "withdraw", "repay"
        - Example: {{ "protocol": "AAVE", "action": "supply", "token": "USDC", "amount": 1000, "expected_apy": 2.2 }}
        
        2. Ambient DEX - For token swaps and liquidity provision
        - Actions: "swap", "add_liquidity", "remove_liquidity"
        - Example swap: {{ "protocol": "Ambient", "action": "swap", "token": "USDC", "token_to": "ETH", "amount": 500, "expected_apy": 0 }}
        - Example liquidity: {{ "protocol": "Ambient", "action": "add_liquidity", "pair": "ETH-USDC", "amount": 1000, "expected_apy": 5.0 }}
        
        3. Quill Finance - For borrowing USDQ stablecoin against collateral
        - Actions: "borrow_usdq", "repay_usdq", "provide_stability"
        - Example borrow: {{ "protocol": "Quill", "action": "borrow_usdq", "token": "ETH", "amount": 0.5, "usdq_amount": 500, "interest_rate": 10, "expected_apy": -10.0 }}
        - Example stability: {{ "protocol": "Quill", "action": "provide_stability", "token": "USDQ", "amount": 500, "expected_apy": 5.0 }}
        
        Requirements:
        - Use all available tokens in the wallet (USDC, ETH, SRC, etc.)
        - Provide clear step-by-step actions
        - Include realistic APY estimates
        - Include comprehensive risk assessment
        - When using Quill, set appropriate interest rates (6% to 350%, with higher rates reducing redemption risk)
        
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
        
        # Convert to JSON-serializable format
        result = {
            "strategies": [
                {
                    "name": strategy.name,
                    "risk_level": strategy.risk_level,
                    "steps": [
                        {
                            "protocol": step.protocol,
                            "action": step.action,
                            "token": step.token,
                            "amount": float(step.amount),
                            "expected_apy": float(step.expected_apy),
                            **({"token_to": step.token_to} if step.token_to else {}),
                            **({"pair": step.pair} if step.pair else {}),
                            **({"interest_rate": step.interest_rate} if step.interest_rate is not None else {}),
                            **({"usdq_amount": float(step.usdq_amount)} if step.usdq_amount is not None else {})
                        }
                        for step in strategy.steps
                    ],
                    "explanation": strategy.explanation,
                    "total_expected_apy": float(strategy.total_expected_apy),
                    "risk_factors": strategy.risk_factors
                }
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