# ai/example.py
import asyncio
from strategy_generator import StrategyGenerator

async def main():
    # Sample data
    wallet_data = {
        "USDC": 1000,
        "ETH": 0.5,
        "SRC": 100
    }
    
    market_data = {
        "rates": {
            "AAVE": {
                "supply_apy": 3.5,
                "borrow_apy": 4.2
            }
        },
        "tvl": {
            "AAVE": 80320000
        },
        "conditions": "stable"
    }
    
    risk_metrics = {
        "health_factor": 1.8,
        "liquidation_threshold": 0.85,
        "current_ratio": 1.5
    }
    
    generator = StrategyGenerator()
    strategy = await generator.generate_strategy(wallet_data, market_data, risk_metrics)
    print(f"Generated Strategy (Risk Level {strategy.risk_level}):")
    print(f"Explanation: {strategy.explanation}")
    print("\nSteps:")
    for step in strategy.steps:
        print(f"- {step.action} {step.amount} {step.token} on {step.protocol} (APY: {step.expected_apy}%)")
    print(f"\nTotal Expected APY: {strategy.total_expected_apy}%")
    print(f"Risk Factors: {', '.join(strategy.risk_factors)}")

if __name__ == "__main__":
    asyncio.run(main())