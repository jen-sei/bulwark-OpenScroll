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
        
    def _build_prompt(self, context: str) -> str:
        """Build the prompt for strategy generation"""
        return f"""You are an AI-powered DeFi strategy generator. Based on the following wallet and market data:
        {context}
        
        Generate a DeFi strategy that optimizes returns while managing risk. The strategy should be executable on AAVE.
        
        Requirements:
        - Focus on USDC for lending
        - Consider current market conditions
        - Provide clear step-by-step actions
        - Include risk assessment
        
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
        
    async def generate_strategy(
        self,
        wallet_data: Dict,
        market_data: Dict,
        risk_metrics: Dict
    ) -> Strategy:
        """Generate a single strategy based on the provided data"""
        context = self.prepare_context(wallet_data, market_data, risk_metrics)
        prompt = self._build_prompt(context)
        
        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a DeFi strategy generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={ "type": "json_object" }
        )
        
        strategy_data = json.loads(response.choices[0].message.content)
        return self._parse_strategy(strategy_data)
        
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