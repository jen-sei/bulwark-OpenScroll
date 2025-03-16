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
    risk_level: int
    steps: List[StrategyStep]
    explanation: str
    total_expected_apy: Decimal
    risk_factors: List[str]

class StrategyGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
    def prepare_context(
        self,
        wallet_data: Dict,
        market_data: Dict,
        risk_metrics: Dict
    ) -> str:
        """Prepare context for LLM prompt"""
        context = {
            "wallet": {
                "balances": wallet_data,
                "current_positions": None,  # To be implemented
                "risk_metrics": risk_metrics
            },
            "market": {
                "apy_rates": market_data.get("rates"),
                "tvl": market_data.get("tvl"),
                "conditions": market_data.get("conditions")
            }
        }
        return json.dumps(context, indent=2)
        
    def _build_prompt(self, context: str, risk_level: Optional[int] = None) -> str:
        """Build the prompt for strategy generation
        
        Args:
            context: JSON string with wallet and market data
            risk_level: Optional specific risk level (1-5) to generate
        """
        risk_instruction = ""
        if risk_level:
            risk_instruction = f"""
            Generate a DeFi strategy with risk level {risk_level} (on a scale of 1-5 where 1 is most conservative and 5 is most aggressive).
            """
        else:
            risk_instruction = """
            Generate a DeFi strategy that optimizes returns while managing risk.
            """
            
        return f"""You are an AI-powered DeFi strategy generator for the Scroll network. Based on the following wallet and market data:
        {context}
        
        {risk_instruction} The strategy should be executable on AAVE.
        
        Risk Level Guidelines:
        - Level 1: Conservative (focus on stable assets like USDC, minimizing risk)
        - Level 2: Moderately Conservative (mostly USDC with small ETH position)
        - Level 3: Balanced (diversified approach with moderate risk)
        - Level 4: Moderately Aggressive (higher ETH allocation, some leverage)
        - Level 5: Aggressive (maximum yield focus, higher leverage)
        
        Requirements:
        - Consider current market conditions and wallet holdings
        - Provide clear step-by-step actions
        - Include realistic APY estimates
        - Include comprehensive risk assessment
        
        Return the strategy in the following JSON format:
        {{
            "risk_level": 1-5,
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
        risk_level: Optional[int] = None
    ) -> Strategy:
        """Generate a single strategy based on the provided data
        
        Args:
            wallet_data: Dictionary with token balances
            market_data: Dictionary with protocol rates and TVL
            risk_metrics: Dictionary with risk assessment metrics
            risk_level: Optional specific risk level (1-5)
            
        Returns:
            Strategy object with the generated strategy
        """
        context = self.prepare_context(wallet_data, market_data, risk_metrics)
        prompt = self._build_prompt(context, risk_level)
        
        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",  # Changed to a model that supports JSON response format
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
        
    def generate_strategies_by_risk(
        self,
        wallet_data: Dict,
        market_data: Dict,
        risk_metrics: Dict
    ) -> List[Strategy]:
        """Generate strategies for all risk levels (1-5)
        
        Args:
            wallet_data: Dictionary with token balances
            market_data: Dictionary with protocol rates and TVL
            risk_metrics: Dictionary with risk assessment metrics
            
        Returns:
            List of 5 Strategy objects, one for each risk level
        """
        strategies = []
        for risk_level in range(1, 6):
            strategy = self.generate_strategy(
                wallet_data, 
                market_data, 
                risk_metrics, 
                risk_level
            )
            strategies.append(strategy)
            
        return strategies
        
    def _parse_strategy(self, data: Dict) -> Strategy:
        """Parse the LLM response into a Strategy object"""
        steps = [
            StrategyStep(
                protocol=step["protocol"],
                action=step["action"],
                token=step["token"],
                amount=Decimal(str(step["amount"])),
                expected_apy=Decimal(str(step["expected_apy"]))
            )
            for step in data["steps"]
        ]
        
        return Strategy(
            risk_level=data["risk_level"],
            steps=steps,
            explanation=data["explanation"],
            total_expected_apy=Decimal(str(data["total_expected_apy"])),
            risk_factors=data["risk_factors"]
        )