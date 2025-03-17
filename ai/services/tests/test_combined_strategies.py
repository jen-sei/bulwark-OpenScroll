# test_combined_strategies.py
from ai.strategy_generator import StrategyGenerator
from ai.services.aave_service import AaveService
from ai.services.ambient_service import AmbientService

def test_combined_strategies():
    print("Initializing services...")
    aave_service = AaveService()
    ambient_service = AmbientService()
    strategy_generator = StrategyGenerator()
    
    # Get market data from both services
    print("Fetching market data from AAVE...")
    aave_market_data = aave_service.get_market_data()
    
    print("Fetching market data from Ambient...")
    ambient_market_data = ambient_service.get_market_data()
    
    # Combine market data
    combined_market_data = {
        "rates": aave_market_data.get("rates", {}),
        "tvl": aave_market_data.get("tvl", {}),
        "conditions": aave_market_data.get("conditions", "stable"),
        "dex": ambient_market_data
    }
    
    # Sample wallet data
    wallet_data = {
        "ETH": 0.5,
        "USDC": 1000,
        "SRC": 100
    }
    
    # Sample risk metrics
    risk_metrics = {
        "health_factor": 1.8,
        "liquidation_threshold": 0.85,
        "current_ratio": 1.5
    }
    
    # Generate all strategies
    print("Generating strategies with combined data...")
    strategies = strategy_generator.generate_all_strategies(
        wallet_data,
        combined_market_data,
        risk_metrics
    )
    
    # Print strategies
    for strategy in strategies:
        print(f"\nStrategy: {strategy.name} (Risk Level: {strategy.risk_level})")
        print(f"Expected APY: {strategy.total_expected_apy}%")
        print(f"Explanation: {strategy.explanation}")
        
        print("\nSteps:")
        for i, step in enumerate(strategy.steps, 1):
            if hasattr(step, 'token_to') and step.token_to:
                print(f"  {i}. {step.protocol} - {step.action} {step.amount} {step.token} to {step.token_to} (Expected APY: {step.expected_apy}%)")
            else:
                print(f"  {i}. {step.protocol} - {step.action} {step.amount} {step.token} (Expected APY: {step.expected_apy}%)")
        
        print("\nRisk Factors:")
        for factor in strategy.risk_factors:
            print(f"  - {factor}")

if __name__ == "__main__":
    test_combined_strategies()