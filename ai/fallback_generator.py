# ai/fallback_generator.py
from typing import Dict, List, Optional
from dataclasses import dataclass
from decimal import Decimal
import os
import json
import re
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

class FallbackGenerator:
    """Strategy generator that works with any OpenAI model"""
    
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
        """Build the prompt for strategy generation"""
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
        
        Return ONLY the strategy in the following JSON format with no additional text:
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
        
        Ensure your response is ONLY valid JSON with no markdown formatting or additional text.
        """
        
    def generate_strategy(
        self,
        wallet_data: Dict,
        market_data: Dict,
        risk_metrics: Dict,
        risk_level: Optional[int] = None
    ) -> Strategy:
        """Generate a single strategy based on the provided data"""
        context = self.prepare_context(wallet_data, market_data, risk_metrics)
        prompt = self._build_prompt(context, risk_level)
        
        print("Sending request to OpenAI...")
        try:
            # Try with gpt-3.5-turbo model
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a DeFi strategy generator. Respond only with JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            print("Received response from OpenAI")
            content = response.choices[0].message.content
            
            # Try to extract JSON from the response
            strategy_data = self._extract_json(content)
            return self._parse_strategy(strategy_data)
            
        except Exception as e:
            print(f"Error with OpenAI API: {e}")
            raise
    
    def _extract_json(self, text: str) -> Dict:
        """Extract JSON from text response"""
        # First try direct parsing
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to extract JSON using regex
            json_match = re.search(r'(\{[\s\S]*\})', text)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except json.JSONDecodeError:
                    # If still failing, try to clean the text
                    cleaned_text = re.sub(r'```json|```', '', text).strip()
                    try:
                        return json.loads(cleaned_text)
                    except json.JSONDecodeError:
                        raise ValueError(f"Could not extract valid JSON from response: {text[:200]}...")
            else:
                raise ValueError(f"Response does not contain valid JSON: {text[:200]}...")
        
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
        
    def generate_strategies_by_risk(
        self,
        wallet_data: Dict,
        market_data: Dict,
        risk_metrics: Dict
    ) -> List[Strategy]:
        """Generate strategies for all risk levels (1-5)"""
        strategies = []
        for risk_level in range(1, 6):
            print(f"Generating strategy for risk level {risk_level}...")
            strategy = self.generate_strategy(
                wallet_data, 
                market_data, 
                risk_metrics, 
                risk_level
            )
            strategies.append(strategy)
            
        return strategies