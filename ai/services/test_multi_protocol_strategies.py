# ai/services/test_multi_protocol_strategies.py
import os
import sys

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from ai.strategy_generator import StrategyGenerator
from ai.services.aave_service import AaveService
from ai.services.ambient_service import AmbientService
from ai.services.quill_service import QuillService

def test_multi_protocol_strategies():
    """Test generating strategies that use all three protocols (AAVE, Ambient, Quill)"""
    print("Initializing services...")
    
    # Initialize services
    aave_service = AaveService()
    ambient_service = AmbientService()
    quill_service = QuillService()
    strategy_generator = StrategyGenerator()
    
    # Get market data from all three services
    print("Fetching market data from AAVE...")
    aave_market_data = aave_service.get_market_data()
    
    print("Fetching market data from Ambient...")
    ambient_market_data = ambient_service.get_market_data()
    
    print("Fetching market data from Quill...")
    quill_market_data = quill_service.get_market_data()
    
    # Combine market data
    combined_market_data = {
        "rates": aave_market_data.get("rates", {}),
        "tvl": aave_market_data.get("tvl", {}),
        "conditions": aave_market_data.get("conditions", "stable"),
        "dex": ambient_market_data,
        "quill": quill_market_data
    }
    
    # Define sample wallet balances
    wallet_balances = {
        "ETH": 2.0,
        "USDC": 2000.0,
        "SRC": 1000.0
    }
    
    # Define risk metrics
    risk_metrics = {
        "health_factor": 1.8,
        "liquidation_threshold": 0.85,
        "current_ratio": 1.5
    }
    
    # Generate strategies
    print("Generating strategies with all three protocols...")
    strategies = strategy_generator.generate_all_strategies(
        wallet_balances,
        combined_market_data,
        risk_metrics
    )
    
    # Print strategies
    for strategy in strategies:
        print(f"\nStrategy: {strategy.name} (Risk Level: {strategy.risk_level})")
        print(f"Expected APY: {strategy.total_expected_apy}%")
        print(f"Explanation: {strategy.explanation}")
        
        print("Steps:")
        for i, step in enumerate(strategy.steps, 1):
            print(f"  {i}. {step.protocol} - {step.action} {step.amount} {step.token} (Expected APY: {step.expected_apy}%)")
            if step.token_to:
                print(f"     → to {step.token_to}")
            if step.pair:
                print(f"     → pair {step.pair}")
            if step.interest_rate:
                print(f"     → interest rate {step.interest_rate}%")
            if step.usdq_amount:
                print(f"     → USDQ amount {step.usdq_amount}")
        
        print("Risk Factors:")
        for factor in strategy.risk_factors:
            print(f"  - {factor}")

if __name__ == "__main__":
    test_multi_protocol_strategies()