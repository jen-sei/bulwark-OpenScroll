# test_ambient_service.py
from ai.services.ambient_service import AmbientService
from decimal import Decimal

def test_ambient_service():
    print("Initializing Ambient service...")
    ambient_service = AmbientService()
    
    print("Connected to Web3:", ambient_service.w3.is_connected() if ambient_service.w3 else False)
    
    print("\nFetching Ambient market data...")
    try:
        market_data = ambient_service.get_market_data()
        print("\nAmbient Market Data:")
        print(f"- DEX: {market_data.get('dex')}")
        print(f"- Swap fee: {market_data.get('swap_fees')}")
        
        # Print pool information
        if 'pools' in market_data:
            print("\nPools:")
            for pair, pool_data in market_data['pools'].items():
                print(f"- {pair}:")
                print(f"  - Price: {pool_data.get('price')}")
                print(f"  - Liquidity: {pool_data.get('total_liquidity')}")
        
    except Exception as e:
        print(f"Error fetching Ambient market data: {e}")
        import traceback
        traceback.print_exc()
    
    # Test swap impact calculation
    print("\nCalculating swap impact...")
    try:
        # Test swapping 1 ETH to USDC
        impact = ambient_service.calculate_swap_impact("ETH", "USDC", Decimal("1.0"))
        print("\nSwap 1 ETH to USDC:")
        print(f"- Input: {impact.get('input_amount')} ETH")
        print(f"- Output: {impact.get('output_amount')} USDC")
        print(f"- Price impact: {impact.get('price_impact') * 100:.2f}%")
        
        # Test swapping 100 USDC to SRC
        impact = ambient_service.calculate_swap_impact("USDC", "SRC", Decimal("100.0"))
        print("\nSwap 100 USDC to SRC:")
        print(f"- Input: {impact.get('input_amount')} USDC")
        print(f"- Output: {impact.get('output_amount')} SRC")
        print(f"- Price impact: {impact.get('price_impact') * 100:.2f}%")
        
    except Exception as e:
        print(f"Error calculating swap impact: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_ambient_service()