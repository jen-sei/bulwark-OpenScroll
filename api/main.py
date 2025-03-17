# api/main.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import sys
import os
import json
from decimal import Decimal
import openai  # For the chatbot endpoint
from openai import OpenAI

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ai.strategy_generator import StrategyGenerator
from ai.services.aave_service import AaveService
from ai.services.ambient_service import AmbientService
from ai.services.quill_service import QuillService
from ai.services.wallet_service import WalletService

# Set up OpenAI key
openai.api_key = os.getenv("OPENAI_API_KEY")

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

# Load Bulwark context from file
BULWARK_CONTEXT = ""
try:
    # Adjust path as needed; this example assumes "ai/context/bulwark_context.txt" is one level above this file
    context_file_path = os.path.join(os.path.dirname(__file__), "bulwark_context.txt")
    with open(context_file_path, "r", encoding="utf-8") as f:
        BULWARK_CONTEXT = f.read()
    print("DEBUG: Loaded bulwark context from:", context_file_path)
    print("DEBUG: First 200 chars:", BULWARK_CONTEXT[:200])
except Exception as e:
    print(f"Warning: Could not load Bulwark context file: {e}")

# Create service dependencies
def get_strategy_generator():
    return StrategyGenerator()

def get_aave_service():
    return AaveService()

def get_ambient_service():
    return AmbientService()

def get_quill_service():
    return QuillService()

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

@app.get("/api/quill-market-data")
def get_quill_market_data(quill_service: QuillService = Depends(get_quill_service)):
    """Get current market data from Quill Finance"""
    try:
        market_data = quill_service.get_market_data()
        return {
            "success": True,
            "data": market_data
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Quill market data: {str(e)}")

@app.get("/api/quill-positions/{address}")
def get_quill_positions(address: str, quill_service: QuillService = Depends(get_quill_service)):
    """Get Quill positions for a specific wallet"""
    try:
        positions = quill_service.get_user_positions(address)
        return {
            "success": True,
            "data": positions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching Quill positions: {str(e)}")

@app.get("/api/quill-max-borrowable")
def calculate_max_borrowable(
    collateral_token: str,
    amount: float,
    quill_service: QuillService = Depends(get_quill_service)
):
    """Calculate the maximum USDQ borrowable for a given collateral amount"""
    try:
        max_borrowable = quill_service.get_max_borrowable_amount(
            collateral_token,
            Decimal(str(amount))
        )
        return {
            "success": True,
            "data": {
                "collateral_token": collateral_token,
                "collateral_amount": amount,
                "max_borrowable_usdq": float(max_borrowable)
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating max borrowable amount: {str(e)}")

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
    quill_service: QuillService = Depends(get_quill_service),
    wallet_service: WalletService = Depends(get_wallet_service)
):
    """Generate optimized DeFi strategies based on wallet holdings"""
    try:
        print(f"Generating strategies for wallet: {request.address}")

        # If balances not provided, fetch them from the chain
        wallet_balances = request.balances
        if not wallet_balances:
            print("No balances provided in request, fetching from blockchain...")
            wallet_data = wallet_service.analyze_wallet(request.address)
            wallet_balances = wallet_data.get("balances", {})

        print(f"Balances: {wallet_balances}")

        # Handle ETH/WETH equivalences
        if "ETH" in wallet_balances and "WETH" not in wallet_balances:
            wallet_balances["WETH"] = wallet_balances["ETH"]
        elif "WETH" in wallet_balances and "ETH" not in wallet_balances:
            wallet_balances["ETH"] = wallet_balances["WETH"]

        # Convert balances to float
        sanitized_balances = {}
        for token, amount in wallet_balances.items():
            try:
                sanitized_balances[token] = amount
            except Exception as e:
                print(f"Error converting balance for {token}: {e}")
                sanitized_balances[token] = 0

        # Attempt real market data from AAVE
        try:
            aave_market_data = aave_service.get_market_data()
            print("Using real market data from AAVE")
        except Exception as e:
            print(f"Error fetching market data from AAVE: {e}, using fallback data")
            aave_market_data = {
                "rates": {
                    "AAVE": {
                        "supply_apy": {"USDC": 3.75, "ETH": 1.82, "SRC": 2.5},
                        "borrow_apy": {"USDC": 4.5, "ETH": 2.1, "SRC": 3.0}
                    }
                },
                "tvl": {"AAVE": 80320000},
                "conditions": "stable"
            }

        # Ambient data
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

        # Quill data
        try:
            quill_market_data = quill_service.get_market_data()
            print("Using real market data from Quill")
        except Exception as e:
            print(f"Error fetching market data from Quill: {e}, using fallback data")
            quill_market_data = {
                "protocol": "Quill",
                "collaterals": {
                    "ETH": {"price_usd": 2000.0, "min_collateral_ratio": 1.1},
                    "SRC": {"price_usd": 10.0, "min_collateral_ratio": 1.15}
                },
                "stability_pools": {
                    "ETH": {
                        "total_deposits_usdq": 1000000,
                        "pool_collateral": 500,
                        "estimated_apr": 5.0
                    },
                    "SRC": {
                        "total_deposits_usdq": 500000,
                        "pool_collateral": 50000,
                        "estimated_apr": 7.0
                    }
                },
                "interest_rates": {
                    "min": 6.0,
                    "max": 350.0,
                    "recommended": {
                        "low_risk": 6.0,
                        "medium_risk": 10.0,
                        "high_risk": 15.0
                    }
                }
            }

        # Combine data
        combined_market_data = {
            "rates": aave_market_data.get("rates", {}),
            "tvl": aave_market_data.get("tvl", {}),
            "conditions": aave_market_data.get("conditions", "stable"),
            "dex": ambient_market_data,
            "quill": quill_market_data
        }

        # Risk metrics
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

# ---------------------------
#      NEW CHAT ENDPOINT
# ---------------------------

class ChatRequest(BaseModel):
    user_query: str

@app.post("/api/ask")
def ask_bulwark(request: ChatRequest):
    """
    Q&A Endpoint for Bulwark. Accepts a user_query,
    then uses the content from BULWARK_CONTEXT plus
    OpenAI to generate an answer.
    """
    try:
        user_question = request.user_query
        if not user_question:
            raise ValueError("Query cannot be empty")

        # Build the prompt using system + user
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a helpful assistant with specialized knowledge about the Bulwark DeFi strategy platform on Scroll. "
                    "Use the following context to answer questions accurately:\n\n"
                    f"{BULWARK_CONTEXT}\n\n"
                    "If the user asks something not in the context, do your best to answer. Be concise but informative."
                )
            },
            {
                "role": "user",
                "content": user_question
            }
        ]

        # Create a client with your API key
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,   # <-- pass the system + user messages you constructed
            temperature=0.7
        )

        answer = response.choices[0].message.content
        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
