# ai/tests/test_multi_risk.py
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from strategy_generator import StrategyGenerator

def test_multi_risk_strategies():
    """Test generating strategies for all risk levels"""
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
    
    print("Generating strategies for all risk levels...")
    try:
        strategies = generator.generate_strategies_by_risk(
            wallet_data, market_data, risk_metrics
        )
        
        print(f"\nGenerated {len(strategies)} strategies:")
        
        for strategy in strategies:
            print("\n===== Risk Level", strategy.risk_level, "=====")
            print(f"Explanation: {strategy.explanation[:150]}...")
            
            print("\nKey Steps:")
            for i, step in enumerate(strategy.steps[:3], 1):  # Show first 3 steps
                print(f"  {i}. {step.action} {step.amount} {step.token} on {step.protocol}")
            
            if len(strategy.steps) > 3:
                print(f"  ... and {len(strategy.steps) - 3} more steps")
                
            print(f"\nExpected APY: {strategy.total_expected_apy}%")
            print(f"Risk Factors: {', '.join(strategy.risk_factors[:3])}")
            if len(strategy.risk_factors) > 3:
                print(f"  ... and {len(strategy.risk_factors) - 3} more factors")
        
        return strategies
    except Exception as e:
        print(f"Error generating strategies: {e}")
        raise

if __name__ == "__main__":
    # Run the test
    test_multi_risk_strategies()