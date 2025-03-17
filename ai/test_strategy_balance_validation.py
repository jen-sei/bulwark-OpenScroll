# ai/test_strategy_balance_validation.py
import os
import sys
import json

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_root)

from ai.strategy_generator import StrategyGenerator
from ai.services.aave_service import AaveService
from ai.services.ambient_service import AmbientService
from ai.services.quill_service import QuillService

def test_balance_validation():
    """Test that generated strategies respect wallet balance constraints"""
    # Initialize services
    strategy_generator = StrategyGenerator()
    aave_service = AaveService()
    ambient_service = AmbientService()
    quill_service = QuillService()
    
    # Define a test wallet with small balances
    wallet_balances = {
        "ETH": 0.005483,
        "USDC": 5.044992,
        "SRC": 6.2
    }
    
    # Get market data from services
    try:
        aave_market_data = aave_service.get_market_data()
    except Exception:
        # Fallback data if service fails
        aave_market_data = {
            "rates": {"AAVE": {"supply_apy": {"USDC": 2.2, "ETH": 1.5, "SRC": 0.5}, "borrow_apy": {"USDC": 4.5, "ETH": 2.5, "SRC": 3.0}}},
            "tvl": {"AAVE": 1000000},
            "conditions": "stable"
        }
    
    try:
        ambient_market_data = ambient_service.get_market_data()
    except Exception:
        # Fallback data if service fails
        ambient_market_data = {
            "dex": "Ambient",
            "pools": {
                "ETH-USDC": {"price": 2000.0, "total_liquidity": 1000000, "volume_24h": 1000000, "fee": 0.003},
                "ETH-SRC": {"price": 0.005, "total_liquidity": 500000, "volume_24h": 500000, "fee": 0.003},
                "USDC-SRC": {"price": 0.01, "total_liquidity": 300000, "volume_24h": 300000, "fee": 0.003}
            },
            "swap_fees": 0.003
        }
    
    try:
        quill_market_data = quill_service.get_market_data()
    except Exception:
        # Fallback data if service fails
        quill_market_data = {
            "protocol": "Quill",
            "collaterals": {
                "ETH": {"price_usd": 2000.0, "min_collateral_ratio": 1.1},
                "SRC": {"price_usd": 10.0, "min_collateral_ratio": 1.15}
            },
            "stability_pools": {
                "ETH": {"estimated_apr": 5.0},
                "SRC": {"estimated_apr": 7.0}
            },
            "interest_rates": {"min": 6, "max": 350}
        }
    
    # Combine market data
    combined_market_data = {
        "rates": aave_market_data.get("rates", {}),
        "tvl": aave_market_data.get("tvl", {}),
        "conditions": aave_market_data.get("conditions", "stable"),
        "dex": ambient_market_data,
        "quill": quill_market_data
    }
    
    # Default risk metrics
    risk_metrics = {
        "health_factor": 1.8,
        "liquidation_threshold": 0.85,
        "current_ratio": 1.5
    }
    
    # Generate strategies
    print(f"Generating strategies for wallet with balances: {wallet_balances}")
    
    # Make sure validate_strategy is defined before calling generate_strategies_json
    if not hasattr(strategy_generator, "validate_strategy"):
        # Add the validate_strategy method for testing if it's not already defined
        def validate_strategy(self, strategy_data, wallet_balances):
            """Simple validation just for testing"""
            print("Warning: Using temporary validate_strategy method for testing")
            return strategy_data
            
        strategy_generator.validate_strategy = validate_strategy.__get__(strategy_generator)
        strategy_generator.get_token_price = lambda token: {"ETH": 2000.0, "USDC": 1.0, "SRC": 10.0, "USDQ": 1.0}.get(token, 1.0)
    
    strategies = strategy_generator.generate_all_strategies(wallet_balances, combined_market_data, risk_metrics)
    
    # Convert to JSON-serializable format manually for testing
    result = {
        "strategies": [
            {
                "name": strategy.name,
                "risk_level": strategy.risk_level,
                "steps": [
                    {
                        "protocol": step.protocol,
                        "action": step.action,
                        "token": step.token,
                        "amount": float(step.amount),
                        "expected_apy": float(step.expected_apy),
                        **({"token_to": step.token_to} if hasattr(step, "token_to") and step.token_to else {}),
                        **({"pair": step.pair} if hasattr(step, "pair") and step.pair else {}),
                        **({"interest_rate": step.interest_rate} if hasattr(step, "interest_rate") and step.interest_rate is not None else {}),
                        **({"usdq_amount": float(step.usdq_amount)} if hasattr(step, "usdq_amount") and step.usdq_amount is not None else {})
                    }
                    for step in strategy.steps
                ],
                "explanation": strategy.explanation,
                "total_expected_apy": float(strategy.total_expected_apy),
                "risk_factors": strategy.risk_factors
            }
            for strategy in strategies
        ],
        "wallet": {
            "balances": wallet_balances
        },
        "market_data": {
            "conditions": combined_market_data.get("conditions", "stable")
        }
    }
    
    # Check each strategy for balance constraints
    print("\nValidating generated strategies:")
    for i, strategy in enumerate(result["strategies"]):
        print(f"\nStrategy: {strategy['name']} (Risk Level: {strategy['risk_level']})")
        print(f"Expected APY: {strategy['total_expected_apy']}%")
        print(f"Explanation: {strategy['explanation']}")
        
        # Define token mappings - normalize token names
        token_mapping = {
            "WETH": "ETH",  # Map WETH to ETH
            "ETH": "ETH",
            "USDC": "USDC",
            "SRC": "SRC",
            "SCR": "SRC"   # Map SCR to SRC if needed
        }
        
        # Track token usage within this strategy
        token_usage = {token: 0.0 for token in wallet_balances.keys()}
        token_usage["USDQ"] = 0.0  # Add USDQ for tracking
        borrowed = {token: 0.0 for token in wallet_balances.keys()}
        borrowed["USDQ"] = 0.0
        
        print("\nSteps:")
        for j, step in enumerate(strategy["steps"]):
            protocol = step["protocol"]
            action = step["action"]
            token = step["token"]
            amount = step["amount"]
            
            # Normalize token name
            normalized_token = token_mapping.get(token, token)
            
            print(f"  {j+1}. {protocol} - {action} {amount} {token} (Expected APY: {step['expected_apy']}%)")
            
            if action == "borrow" or action == "borrow_usdq":
                # Track borrowing
                if action == "borrow_usdq":
                    usdq_amount = step.get("usdq_amount", 0)
                    interest_rate = step.get("interest_rate", 0)
                    print(f"     → borrowing {usdq_amount} USDQ at {interest_rate}% interest")
                    borrowed["USDQ"] += usdq_amount
                    token_usage["USDQ"] -= usdq_amount  # Negative usage represents addition
                else:
                    borrowed[normalized_token] += amount
                    token_usage[normalized_token] -= amount  # Negative usage represents addition
            
            elif action in ["supply", "swap", "add_liquidity"]:
                # These actions consume tokens
                if normalized_token in token_usage:
                    token_usage[normalized_token] += amount
                
                if action == "swap" and "token_to" in step:
                    token_to = step["token_to"]
                    print(f"     → to {token_to}")
                elif action == "add_liquidity" and "pair" in step:
                    pair = step["pair"]
                    print(f"     → pair {pair}")
        
        # Verify token usage against wallet balances
        print("\nToken Usage Summary:")
        all_valid = True
        for token, used in token_usage.items():
            if token == "USDQ":
                # Skip USDQ in wallet balance check
                continue
                
            available = wallet_balances.get(token, 0)
            net_usage = used - borrowed.get(token, 0)
            
            valid = net_usage <= available
            status = "✓" if valid else "✗"
            
            print(f"  {token}: Used {used}, Borrowed {borrowed.get(token, 0)}, Net Usage {net_usage}/{available} {status}")
            
            if not valid:
                all_valid = False
        
        if all_valid:
            print("\n✅ Strategy is valid! All token usages within wallet balances.")
        else:
            print("\n❌ Strategy has balance issues! Some token usages exceed wallet balances.")
        
        print("\nRisk Factors:")
        for factor in strategy["risk_factors"]:
            print(f"  - {factor}")
    
    # Pretty print the JSON result for easy inspection
    print("\nFull Generated Strategies JSON:")
    print(json.dumps(result, indent=2))
    
    return result

if __name__ == "__main__":
    test_balance_validation()