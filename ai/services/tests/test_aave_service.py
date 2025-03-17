# test_aave_service.py
from ai.services.aave_service import AaveService

def test_aave_service():
    print("Initializing AAVE service...")
    aave_service = AaveService()
    
    print("Connected to Web3:", aave_service.w3.is_connected())
    
    print("Fetching market data...")
    try:
        market_data = aave_service.get_market_data()
        print("\nMarket Data:")
        print(f"- Conditions: {market_data['conditions']}")
        print(f"- TVL: {market_data['tvl']}")
        
        # Print some rate information if available
        if 'rates' in market_data and 'AAVE' in market_data['rates']:
            aave_rates = market_data['rates']['AAVE']
            print("\nSupply APY:")
            for token, rate in aave_rates.get('supply_apy', {}).items():
                print(f"- {token}: {rate}%")
                
            print("\nBorrow APY:")
            for token, rate in aave_rates.get('borrow_apy', {}).items():
                print(f"- {token}: {rate}%")
        
    except Exception as e:
        print(f"Error fetching market data: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_aave_service()