# simplified_test.py
import json
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_generate_strategies():
    """Test the strategy generation API endpoint with hardcoded data"""
    # Test data
    wallet_data = {
        "address": "0x0a6A5Ba22da4e199bB5d8Cc04a84976C5930d049",
        "balances": {
            "USDC": 5000,
            "ETH": 2.5,
            "SRC": 250
        }
    }
    
    # Make request to API
    print("Sending request to /api/generate-strategies...")
    response = client.post("/api/generate-strategies", json=wallet_data)
    
    # Check response
    print(f"Status code: {response.status_code}")
    if response.status_code != 200:
        print(f"Error response: {response.text}")
        return
    
    # Parse response 
    data = response.json()
    
    # Save result to file
    with open("api_response.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print("\nAPI test successful! Response saved to api_response.json")
    
    # Print summary
    if "strategies" in data:
        for strategy in data["strategies"]:
            print(f"\n===== {strategy['name']} =====")
            print(f"Risk Level: {strategy['risk_level']}")
            print(f"Expected APY: {strategy['total_expected_apy']}%")
            print(f"Steps: {len(strategy['steps'])}")
    else:
        print("No strategies found in response")

if __name__ == "__main__":
    print("Testing API...")
    test_generate_strategies()