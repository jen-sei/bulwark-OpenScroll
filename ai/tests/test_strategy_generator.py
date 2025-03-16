# ai/tests/test_strategy_generator.py
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from strategy_generator import StrategyGenerator

def test_strategy_generation():
    """Test that the strategy generator works end-to-end"""
    # Sample data
    wallet_data = {
        "USDC": 5000,
        "ETH": 2.5,
        "SRC": 250
    }
    
    market_data = {
        "rates": {
            "AAVE": {
                "supply_apy": {
                    "USDC": 3.75,
                    "ETH": 1.82
                },
                "borrow_apy": {
                    "USDC": 4.5,
                    "ETH": 2.1
                }
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
    
    # Create strategy generator
    generator = StrategyGenerator()
    
    print("Generating strategy...")
    try:
        strategy = generator.generate_strategy(wallet_data, market_data, risk_metrics)
        
        print("\n===== Generated Strategy =====")
        print(f"Risk Level: {strategy.risk_level}/5")
        print(f"Explanation: {strategy.explanation}")
        print("\nExecution Steps:")
        for i, step in enumerate(strategy.steps, 1):
            print(f"  {i}. {step.action} {step.amount} {step.token} on {step.protocol} (Expected APY: {step.expected_apy}%)")
        
        print(f"\nTotal Expected APY: {strategy.total_expected_apy}%")
        print(f"Risk Factors: {', '.join(strategy.risk_factors)}")
        print("=============================")
        
        return strategy
    except Exception as e:
        print(f"Error generating strategy: {e}")
        raise

if __name__ == "__main__":
    # Run the test
    test_strategy_generation()