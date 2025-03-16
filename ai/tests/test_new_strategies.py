# ai/tests/test_new_strategies.py
import sys
import os
import json

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from ai.strategy_generator import StrategyGenerator

def test_new_strategies():
    """Test generating the three named strategies"""
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
    
    risk_metrics = {
        "health_factor": 1.8,
        "liquidation_threshold": 0.85,
        "current_ratio": 1.5
    }
    
    # Create strategy generator
    generator = StrategyGenerator()
    
    print("Generating named strategies...")
    try:
        json_result = generator.generate_strategies_json(
            wallet_data, market_data, risk_metrics
        )
        
        # Save to file for easy inspection
        with open('generated_strategies.json', 'w') as f:
            json.dump(json_result, f, indent=2)
            
        print(f"\nGenerated {len(json_result['strategies'])} strategies and saved to generated_strategies.json")
        
        # Print summary of strategies
        for strategy in json_result['strategies']:
            print("\n===== Strategy:", strategy['name'], "=====")
            print(f"Risk Level: {strategy['risk_level']}")
            print(f"Expected APY: {strategy['total_expected_apy']}%")
            print(f"Explanation: {strategy['explanation'][:150]}...")
            
            print("\nKey Steps:")
            for i, step in enumerate(strategy['steps'][:3], 1):
                print(f"  {i}. {step['action']} {step['amount']} {step['token']} on {step['protocol']}")
            
            if len(strategy['steps']) > 3:
                print(f"  ... and {len(strategy['steps']) - 3} more steps")
                
        return json_result
        
    except Exception as e:
        print(f"Error generating strategies: {e}")
        raise

if __name__ == "__main__":
    # Run the test
    test_new_strategies()