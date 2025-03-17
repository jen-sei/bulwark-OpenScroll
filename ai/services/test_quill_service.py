# ai/services/test_quill_service.py
import os
import sys
from decimal import Decimal

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

from ai.services.quill_service import QuillService

def test_quill_service():
    """Test the Quill Finance service integration"""
    # Initialize the Quill service
    print("Initializing Quill service...")
    quill_service = QuillService()
    
    # Check if connected to Web3
    print(f"Connected to Web3: {quill_service.w3 is not None}")
    
    # Fetch market data
    print("Fetching Quill market data...")
    market_data = quill_service.get_market_data()
    
    # Display market data
    print("Quill Market Data:")
    print(f"- Protocol: {market_data.get('protocol', 'Quill')}")
    
    # Display collateral factors
    print("\nCollateral Factors:")
    for token, data in market_data.get('collaterals', {}).items():
        print(f"- {token}:")
        print(f"  - Min Collateral Ratio: {data.get('min_collateral_ratio', 'N/A')}")
        print(f"  - Price (USD): {data.get('price_usd', 'N/A')}")
    
    # Display stability pools
    print("\nStability Pools:")
    for token, data in market_data.get('stability_pools', {}).items():
        print(f"- {token}:")
        print(f"  - Total Deposits (USDQ): {data.get('total_deposits_usdq', 'N/A')}")
        print(f"  - Pool Collateral: {data.get('pool_collateral', 'N/A')}")
        print(f"  - Estimated APR: {data.get('estimated_apr', 'N/A')}%")
    
    # Display interest rates
    interest_rates = market_data.get('interest_rates', {})
    print("\nInterest Rates:")
    print(f"- Min: {interest_rates.get('min', 'N/A')}%")
    print(f"- Max: {interest_rates.get('max', 'N/A')}%")
    
    # Calculate max borrowable amounts with proper error handling
    print("\nMax Borrowable Amounts:")
    test_amounts = {
        "ETH": Decimal("1.0"),
        "SRC": Decimal("1000.0"),
        "wstETH": Decimal("0.5"),
        "weETH": Decimal("0.5")
    }
    
    for token, amount in test_amounts.items():
        try:
            max_borrowable = quill_service.get_max_borrowable_amount(token, amount)
            print(f"- {amount} {token} -> {max_borrowable} USDQ")
        except Exception as e:
            print(f"- Error calculating max borrowable for {amount} {token}: {e}")
    
    # Test user positions (using a test wallet address)
    test_wallet = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"  # Example address
    print(f"\nTesting user positions for wallet {test_wallet}:")
    
    try:
        positions = quill_service.get_user_positions(test_wallet)
        
        # Display user troves
        print("User Troves:")
        if positions['troves']:
            for token, data in positions['troves'].items():
                print(f"- {token}:")
                print(f"  - Debt (USDQ): {data.get('debt_usdq', 'N/A')}")
                print(f"  - Collateral: {data.get('collateral_amount', 'N/A')}")
                print(f"  - Collateral Value (USD): {data.get('collateral_value_usd', 'N/A')}")
                print(f"  - Collateral Ratio: {data.get('collateral_ratio', 'N/A')}")
        else:
            print("No active troves found")
        
        # Display stability pool deposits
        print("\nStability Pool Deposits:")
        if positions['stability_deposits']:
            for token, data in positions['stability_deposits'].items():
                print(f"- {token}:")
                print(f"  - Deposit (USDQ): {data.get('deposit_usdq', 'N/A')}")
                print(f"  - Collateral Gain: {data.get('collateral_gain', 'N/A')}")
                print(f"  - USDQ Gain: {data.get('usdq_gain', 'N/A')}")
        else:
            print("No stability pool deposits found")
    except Exception as e:
        print(f"Error getting user positions: {e}")
    
    # Test getting recommended strategies
    print("\nTesting recommended strategies:")
    test_balances = {
        "ETH": 1.0,
        "USDC": 2000.0,
        "SRC": 500.0
    }
    
    try:
        strategies = quill_service.get_recommended_strategies(test_balances)
        if strategies:
            for i, strategy in enumerate(strategies, 1):
                print(f"\nStrategy {i}: {strategy['name']}")
                print(f"Expected outcome: {strategy['expected_outcome']}")
                print(f"Risk level: {strategy['risk_level']}")
                print("Steps:")
                for j, step in enumerate(strategy['steps'], 1):
                    print(f"  {j}. {step['protocol']} - {step['action']} {step['amount']} {step['token']} (Expected APY: {step['expected_apy']}%)")
        else:
            print("No recommended strategies found")
    except Exception as e:
        print(f"Error getting recommended strategies: {e}")
    
    print("\nQuill service test completed")

if __name__ == "__main__":
    test_quill_service()