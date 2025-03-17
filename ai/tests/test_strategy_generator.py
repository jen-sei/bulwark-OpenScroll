# test_strategy_generator.py
from ai.strategy_generator import StrategyGenerator
from ai.services.aave_service import AaveService

def test_strategy_generation():
    print("Initializing services...")
    aave_service = AaveService()
    strategy_generator = StrategyGenerator()
    
    # Get real market data
    market_data = aave_service.get_market_data()
    print(f"Fetched market data with {len(market_data['rates']['AAVE']['supply_apy'])} assets")
    
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
    
    # Generate a single strategy for testing
    strategy_type = "Anchor"  # Can be "Anchor", "Zenith", or "Wildcard"
    
    print(f"Generating {strategy_type} strategy...")
    strategy = strategy_generator.generate_strategy(
        wallet_data,
        market_data,
        risk_metrics,
        strategy_type
    )
    
    # Print strategy details
    print(f"\nStrategy: {strategy.name} (Risk Level: {strategy.risk_level})")
    print(f"Expected APY: {strategy.total_expected_apy}%")
    print(f"Explanation: {strategy.explanation}")
    
    print("\nSteps:")
    for i, step in enumerate(strategy.steps, 1):
        print(f"  {i}. {step.protocol} - {step.action} {step.amount} {step.token} (Expected APY: {step.expected_apy}%)")
    
    print("\nRisk Factors:")
    for factor in strategy.risk_factors:
        print(f"  - {factor}")

if __name__ == "__main__":
    test_strategy_generation()