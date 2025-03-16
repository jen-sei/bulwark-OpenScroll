# test_api.py
import json
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_generate_strategies():
    """Test the strategy generation API endpoint"""
    # Test data
    wallet_data = {
        "address": "0x1234567890123456789012345678901234567890",
        "balances": {
            "USDC": 5000,
            "ETH": 2.5,
            "SRC": 250
        }
    }
    
    # Make request to API
    response = client.post("/api/generate-strategies", json=wallet_data)
    
    # Check response
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Parse response 
    data = response.json()
    
    # Verify structure
    assert "strategies" in data, "Expected 'strategies' in response"
    assert len(data["strategies"]) == 3, f"Expected 3 strategies, got {len(data['strategies'])}"
    
    # Save result to file
    with open("api_response.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print("\nAPI test successful! Response saved to api_response.json")
    
    # Print summary
    for strategy in data["strategies"]:
        print(f"\n===== {strategy['name']} =====")
        print(f"Risk Level: {strategy['risk_level']}")
        print(f"Expected APY: {strategy['total_expected_apy']}%")
        print(f"Steps: {len(strategy['steps'])}")

if __name__ == "__main__":
    print("Testing API...")
    test_generate_strategies()