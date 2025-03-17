# test_api_real_data.py
import json
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from main import app  # Import directly when running from api directory

client = TestClient(app)

def test_generate_strategies_real_data():
    """Test the strategy generation API endpoint with real wallet data"""
    # Test wallet on Scroll mainnet (replace with a real wallet that has some tokens)
    wallet_address = "0x0a6A5Ba22da4e199bB5d8Cc04a84976C5930d049"
    
    # Make request to API
    response = client.get(f"/api/wallet/{wallet_address}")
    
    # Check response
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Parse response
    wallet_data = response.json()
    
    print(f"Wallet data for {wallet_address}:")
    print(json.dumps(wallet_data, indent=2))
    
    # Now use this data to generate strategies
    request_data = {
        "address": wallet_address,
        "balances": wallet_data.get("wallet_data", {})
    }
    
    # Make request to generate strategies
    response = client.post("/api/generate-strategies", json=request_data)
    
    # Check response
    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
    
    # Parse response
    data = response.json()
    
    # Verify structure
    assert "strategies" in data, "Expected 'strategies' in response"
    assert len(data["strategies"]) == 3, f"Expected 3 strategies, got {len(data['strategies'])}"
    
    # Save result to file
    with open("api_response_real_data.json", "w") as f:
        json.dump(data, f, indent=2)
    
    print("\nAPI test with real data successful! Response saved to api_response_real_data.json")
    
    # Print summary
    for strategy in data["strategies"]:
        print(f"\n===== {strategy['name']} =====")
        print(f"Risk Level: {strategy['risk_level']}")
        print(f"Expected APY: {strategy['total_expected_apy']}%")
        print(f"Steps: {len(strategy['steps'])}")

if __name__ == "__main__":
    print("Testing API with real data...")
    test_generate_strategies_real_data()