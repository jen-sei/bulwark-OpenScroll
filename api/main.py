# api/main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import sys
import os
import json
from decimal import Decimal

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.strategy_generator import StrategyGenerator
from ai.services.aave_service import AaveService
from ai.services.ambient_service import AmbientService
from ai.services.wallet_service import WalletService

app = FastAPI(title="Bulwark API", description="AI-powered DeFi strategies for Scroll network")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://bulwark-scroll.vercel.app",
        "http://localhost:3000",     # Standard Next.js port
        "http://127.0.0.1:3000",     # Alternative localhost
        "http://localhost:8000",     # In case they're using this port
        "http://localhost:5173",     # Vite default port
        "http://127.0.0.1:5173"      # Alternative Vite localhost
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)   

# Create service dependencies
def get_strategy_generator():
    return StrategyGenerator()

def get_aave_service():
    return AaveService()

def get_ambient_service():
    return AmbientService()

def get_wallet_service():
    return WalletService()

class WalletRequest(BaseModel):
    address: str
    balances: Optional[Dict[str, float]] = None

class GenerateStrategiesResponse(BaseModel):
    strategies: List[Dict]
    wallet: Dict
    market_data: Dict

@app.get("/")
def read_root():
    return {"message": "Welcome to Bulwark API", "version": "1.0"}

@app.get("/api/market-data")
def get_market_data(aave_service: AaveService = Depends(get_aave_service)):
    """Get current market data from AAVE"""
    try:
        market_data = aave_service.get_market_data()
        return {
            "success": True,
            "data": market_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching market data: {str(e)}")

@app.get("/api/ambient-market-data")
def get_ambient_market_data(ambient_service: AmbientService = Depends(get_ambient_service)):
    """Get current market data from Ambient DEX"""
    try:
        market_data = ambient_service.get_market_data()
        return {
            "success": True,
            "data": market_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Ambient market data: {str(e)}")

@app.get("/api/swap-impact")
def calculate_swap_impact(
    from_token: str,
    to_token: str,
    amount: float,
    ambient_service: AmbientService = Depends(get_ambient_service)
):
    """Calculate the impact of swapping tokens"""
    try:
        impact = ambient_service.calculate_swap_impact(
            from_token, 
            to_token, 
            Decimal(str(amount))
        )
        return {
            "success": True,
            "data": impact
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating swap impact: {str(e)}")

@app.get("/api/wallet/{address}")
def analyze_wallet(address: str, wallet_service: WalletService = Depends(get_wallet_service)):
    """Analyze wallet contents"""
    try:
        wallet_data = wallet_service.analyze_wallet(address)
        return {
            "success": True,
            "data": wallet_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing wallet: {str(e)}")

@app.post("/api/generate-strategies", response_model=GenerateStrategiesResponse)
def generate_strategies(
    request: WalletRequest,
    strategy_generator: StrategyGenerator = Depends(get_strategy_generator),
    aave_service: AaveService = Depends(get_aave_service),
    ambient_service: AmbientService = Depends(get_ambient_service),
    wallet_service: WalletService = Depends(get_wallet_service)
):
    """Generate optimized DeFi strategies based on wallet holdings"""
    try:
        # Log request
        print(f"Generating strategies for wallet: {request.address}")
        
        # Get balances either from request or fetch them if not provided
        wallet_balances = request.balances
        if not wallet_balances:
            print("No balances provided in request, fetching from blockchain...")
            wallet_data = wallet_service.analyze_wallet(request.address)
            wallet_balances = wallet_data.get("balances", {})
        
        print(f"Balances: {wallet_balances}")
        
        # Convert any float balances to the format required by strategy generator
        sanitized_balances = {}
        for token, amount in wallet_balances.items():
            try:
                sanitized_balances[token] = amount
            except Exception as e:
                print(f"Error converting balance for {token}: {e}")
                sanitized_balances[token] = 0
        
        # Fetch real market data from AAVE
        try:
            aave_market_data = aave_service.get_market_data()
            print("Using real market data from AAVE")
        except Exception as e:
            print(f"Error fetching market data from AAVE: {e}, using fallback data")
            # Fallback to hardcoded data if AAVE fetch fails
            aave_market_data = {
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
        
        # Fetch real market data from Ambient
        try:
            ambient_market_data = ambient_service.get_market_data()
            print("Using real market data from Ambient")
        except Exception as e:
            print(f"Error fetching market data from Ambient: {e}, using fallback data")
            ambient_market_data = {
                "dex": "Ambient",
                "pools": {
                    "ETH-USDC": {
                        "price": 2000.0,
                        "total_liquidity": 1000000,
                        "volume_24h": 1000000,
                        "fee": 0.003
                    },
                    "ETH-SRC": {
                        "price": 0.005,
                        "total_liquidity": 1000000,
                        "volume_24h": 1000000,
                        "fee": 0.003
                    },
                    "USDC-SRC": {
                        "price": 0.01,
                        "total_liquidity": 1000000,
                        "volume_24h": 1000000,
                        "fee": 0.003
                    }
                },
                "swap_fees": 0.003
            }
        
        # Combine market data
        combined_market_data = {
            "rates": aave_market_data.get("rates", {}),
            "tvl": aave_market_data.get("tvl", {}),
            "conditions": aave_market_data.get("conditions", "stable"),
            "dex": ambient_market_data
        }
        
        # Get real risk metrics or use fallback
        try:
            risk_metrics = aave_service.get_user_risk_metrics(request.address)
            print("Using real risk metrics from AAVE")
        except Exception as e:
            print(f"Error fetching risk metrics from AAVE: {e}, using fallback data")
            risk_metrics = {
                "health_factor": 1.8,
                "liquidation_threshold": 0.85,
                "current_ratio": 1.5
            }
        
        # Generate strategies
        strategies_json = strategy_generator.generate_strategies_json(
            sanitized_balances,
            combined_market_data,
            risk_metrics
        )
        
        return strategies_json
    
    except Exception as e:
        print(f"Error generating strategies: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
def health_check():
    """API health check endpoint"""
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)