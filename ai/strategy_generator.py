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
        
        # Token name mapping (from AAVE service to frontend display)
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
                "conditions": market_data.get("conditions")
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
                "description": "Conservative strategy focused on steady growth over time. Should use USDC primarily for minimal volatility.",
                "risk_level": 1,
                "target_apy": "around 3.8%"
            },
            "Zenith": {
                "description": "Balanced performance strategy that creates moderate leverage while maintaining reasonable health factor.",
                "risk_level": 3,
                "target_apy": "around 5.5%"
            },
            "Wildcard": {
                "description": "Aggressive strategy for risk-takers that maximizes yield through recursive leveraging. Operates near minimum health factor.",
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
        The strategy should be executable on AAVE.
        
        Strategy Guidelines:
        - Anchor: Conservative strategy focusing on USDC supply with minimal risk exposure
        - Zenith: Balanced strategy involving USDC as collateral, borrowing ETH against it, and then supplying that ETH back 
        - Wildcard: Aggressive strategy that maximizes yield through recursive leveraging with multiple cycles of borrowing and supplying
        
        Requirements:
        - Use all available tokens in the wallet (USDC, ETH, SRC)
        - Provide clear step-by-step actions
        - Include realistic APY estimates
        - Include comprehensive risk assessment
        
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
                    "expected_apy": "number"
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
                
                # Map the display token names (ETH) back to blockchain names (WETH)
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
                    protocol=step["protocol"],
                    action=step["action"],
                    token=step["token"],
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
                            "expected_apy": float(step.expected_apy)
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