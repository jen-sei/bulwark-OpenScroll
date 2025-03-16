# ai/services/wallet_service.py
from typing import Dict, List, Any, Optional
from web3 import Web3
import os
import json
from decimal import Decimal

class WalletService:
    """Service for analyzing wallet contents and positions"""
    
    # Scroll network constants
    SCROLL_RPC_URL = os.getenv("WEB3_PROVIDER_URI", "https://rpc.scroll.io/")
    
    # Asset addresses and ABI paths - with actual Scroll addresses
    ASSETS = {
        "USDC": {
            "address": "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4",  # Actual USDC address on Scroll
            "decimals": 6
        },
        "ETH": {
            "address": "0x5300000000000000000000000000000000000004",  # WETH underlying on Scroll
            "decimals": 18
        },
        "SRC": {
            "address": "0xd29687c813D741E2F938F4aC377128810E217b1b",  # Actual SCR address on Scroll
            "decimals": 18
        }
    }
    
    # ERC20 ABI - minimal for balance checking
    ERC20_ABI = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function"
        },
        {
            "constant": True,
            "inputs": [],
            "name": "decimals",
            "outputs": [{"name": "", "type": "uint8"}],
            "type": "function"
        }
    ]
    
    def __init__(self):
        # Initialize Web3 connection
        self.w3 = Web3(Web3.HTTPProvider(self.SCROLL_RPC_URL))
        
        # Test connection
        if not self.w3.is_connected():
            print(f"Failed to connect to {self.SCROLL_RPC_URL}")
        else:
            print(f"Connected to {self.SCROLL_RPC_URL}")
    
    def get_token_balance(self, wallet_address: str, token_address: str, decimals: int = 18) -> float:
        """Get token balance for a wallet"""
        try:
            # Special case for ETH (native token)
            if token_address.lower() == self.ASSETS["ETH"]["address"].lower():
                balance_wei = self.w3.eth.get_balance(self.w3.to_checksum_address(wallet_address))
                return float(balance_wei) / (10 ** decimals)
            
            # For ERC20 tokens
            token_contract = self.w3.eth.contract(
                address=self.w3.to_checksum_address(token_address),
                abi=self.ERC20_ABI
            )
            
            # Get balance and convert to float
            balance = token_contract.functions.balanceOf(
                self.w3.to_checksum_address(wallet_address)
            ).call()
            
            # Try to get decimals from contract if not provided
            if decimals is None:
                try:
                    decimals = token_contract.functions.decimals().call()
                except:
                    decimals = 18  # Default to 18 if not specified
            
            # Convert to human-readable format
            return float(balance) / (10 ** decimals)
            
        except Exception as e:
            print(f"Error fetching token balance: {e}")
            return 0.0
    
    def get_wallet_balances(self, wallet_address: str) -> Dict[str, float]:
        """Get all relevant token balances for a wallet"""
        try:
            balances = {}
            
            # Check balance for each tracked asset
            for symbol, asset_data in self.ASSETS.items():
                balance = self.get_token_balance(
                    wallet_address,
                    asset_data["address"],
                    asset_data["decimals"]
                )
                
                if balance > 0:
                    balances[symbol] = balance
            
            return balances
            
        except Exception as e:
            print(f"Error fetching wallet balances: {e}")
            return {}
    
    def analyze_wallet(self, wallet_address: str) -> Dict[str, Any]:
        """Analyze wallet contents and return comprehensive data"""
        try:
            # Get basic token balances
            balances = self.get_wallet_balances(wallet_address)
            
            # Calculate total value in USD (would need price oracle integration)
            # For now, we'll return basic data
            
            return {
                "address": wallet_address,
                "balances": balances,
                "total_value_usd": 0.0,  # Placeholder until price oracle integration
                "assets_count": len(balances)
            }
            
        except Exception as e:
            print(f"Error analyzing wallet: {e}")
            return {
                "address": wallet_address,
                "balances": {},
                "total_value_usd": 0.0,
                "assets_count": 0
            }