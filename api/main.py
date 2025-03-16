# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional
import sys
import os
import json

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.strategy_generator import StrategyGenerator

app = FastAPI(title="Bulwark API", description="AI-powered DeFi strategies for Scroll network")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bulwark-scroll.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize strategy generator
generator = StrategyGenerator()

class WalletRequest(BaseModel):
    address: str
    balances: Dict[str, float]

class GenerateStrategiesResponse(BaseModel):
    strategies: List[Dict]
    wallet: Dict
    market_data: Dict

@app.get("/")
def read_root():
    return {"message": "Welcome to Bulwark API", "version": "1.0"}

@app.post("/api/generate-strategies", response_model=GenerateStrategiesResponse)
def generate_strategies(request: WalletRequest):
    try:
        # Log request
        print(f"Generating strategies for wallet: {request.address}")
        print(f"Balances: {request.balances}")
        
        # For a real implementation, you would fetch market data from external sources
        # For the hackathon, we'll use hardcoded data
        market_data = {
            "rates": {
                "AAVE": {
                    "supply_apy": {
                        "USDC": 3.75,
                        "ETH": 1.82,
                        "SRC": 2.5
                    },
                    "borrow_apy": {
                        "USDC": 4.5,
                        "ETH": 2.1,
                        "SRC": 3.0
                    }
                }
            },
            "tvl": {
                "AAVE": 80320000
            },
            "conditions": "stable"
        }
        
        # In a real implementation, calculate risk metrics based on current positions
        risk_metrics = {
            "health_factor": 1.8,
            "liquidation_threshold": 0.85,
            "current_ratio": 1.5
        }
        
        # Generate strategies
        strategies_json = generator.generate_strategies_json(
            request.balances,
            market_data,
            risk_metrics
        )
        
        return strategies_json
    
    except Exception as e:
        print(f"Error generating strategies: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)