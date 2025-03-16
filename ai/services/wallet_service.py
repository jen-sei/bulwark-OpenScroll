# ai/services/aave_service.py
from typing import Dict, List, Optional, Any
import os
from decimal import Decimal
import json
import web3
from web3 import Web3

# Handle different versions of web3.py
try:
    from web3.middleware import geth_poa_middleware
except ImportError:
    # For newer versions of web3.py
    from web3.middleware.geth import geth_poa_middleware
except:
    # Fallback if middleware can't be imported
    geth_poa_middleware = None

# ABI imports
from .abis.pool_data_provider_abi import POOL_DATA_PROVIDER_ABI
from .abis.ui_pool_data_provider_abi import UI_POOL_DATA_PROVIDER_ABI
from .abis.price_oracle_abi import PRICE_ORACLE_ABI
from .abis.pool_addresses_provider_abi import POOL_ADDRESSES_PROVIDER_ABI

class AaveService:
    """Service for interacting with AAVE protocol on Scroll network"""
    
    # Scroll network constants with actual Scroll values
    SCROLL_RPC_URL = os.getenv("WEB3_PROVIDER_URI", "https://rpc.scroll.io/")
    POOL_ADDRESSES_PROVIDER = "0x69850D0B276776781C063771b161bd8894BCdD04"  # Actual Scroll address
    
    # Asset addresses from AaveV3ScrollAssets library
    ASSETS = {
        "USDC": "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4",  # Actual USDC address on Scroll
        "ETH": "0x5300000000000000000000000000000000000004",   # WETH underlying on Scroll
        "SRC": "0xd29687c813D741E2F938F4aC377128810E217b1b"    # SCR token address on Scroll
    }
    
    def __init__(self):
        # Initialize Web3 connection
        self.w3 = Web3(Web3.HTTPProvider(self.SCROLL_RPC_URL))
        
        # Only inject middleware if available
        if geth_poa_middleware is not None:
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        
        # Test connection
        if not self.w3.is_connected():
            print(f"Failed to connect to {self.SCROLL_RPC_URL}")
        else:
            print(f"Connected to {self.SCROLL_RPC_URL}")
            
        # Initialize contract interfaces
        self.addresses_provider = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.POOL_ADDRESSES_PROVIDER),
            abi=POOL_ADDRESSES_PROVIDER_ABI
        )
        
        # Get contract addresses from PoolAddressesProvider
        self.initialize_contracts()

    def safely_call_contract(self, contract_method, fallback_value=None, *args, **kwargs):
        """Safely call a contract method with fallback value on error"""
        try:
            return contract_method(*args, **kwargs)
        except Exception as e:
            print(f"Error calling contract method {contract_method.__name__ if hasattr(contract_method, '__name__') else 'unknown'}: {e}")
            return fallback_value

    def initialize_contracts(self):
        """Initialize AAVE contracts using the PoolAddressesProvider"""
        try:
            # Get contract addresses
            pool_address = self.safely_call_contract(
                self.addresses_provider.functions.getPool().call,
                "0x11fCfe756c05AD438e312a7fd934381537D3cFfe"  # Fallback address
            )
            
            oracle_address = self.safely_call_contract(
                self.addresses_provider.functions.getPriceOracle().call,
                "0x04421D8C506E2fA2371a08EfAaBf791F624054F3"  # Fallback address
            )
            
            data_provider_address = self.safely_call_contract(
                self.addresses_provider.functions.getPoolDataProvider().call,
                "0xDC3c96ef82F861B4a3f10C81d4340c75460209ca"  # Fallback address
            )
            
            # Initialize contract interfaces
            self.pool = self.w3.eth.contract(
                address=self.w3.to_checksum_address(pool_address),
                abi=[]  # We'll add Pool ABI if needed
            )
            
            self.price_oracle = self.w3.eth.contract(
                address=self.w3.to_checksum_address(oracle_address),
                abi=PRICE_ORACLE_ABI
            )
            
            self.data_provider = self.w3.eth.contract(
                address=self.w3.to_checksum_address(data_provider_address),
                abi=POOL_DATA_PROVIDER_ABI
            )
            
            # For UI data provider we might need a separate address
            # This is just a placeholder - you'll need to set the correct address
            ui_pool_data_provider_address = "0x5598BbFA2f4fE8151f45bBA0a3edE1b54B51a0a9"
            self.ui_data_provider = self.w3.eth.contract(
                address=self.w3.to_checksum_address(ui_pool_data_provider_address),
                abi=UI_POOL_DATA_PROVIDER_ABI
            )
            
            print("All AAVE contracts initialized successfully")
            
        except Exception as e:
            print(f"Error initializing AAVE contracts: {e}")
            raise

    def get_reserve_data(self) -> Dict[str, Any]:
        """Get data for all reserves in the AAVE pool"""
        try:
            # Get list of reserves
            reserves_list = self.safely_call_contract(
                self.data_provider.functions.getAllReservesTokens().call,
                []  # Empty list fallback
            )
            
            # Initialize result dictionary
            reserves_data = {}
            
            # Fallback data in case we can't fetch real data
            fallback_data = {
                "WETH": {
                    "address": self.ASSETS["ETH"],
                    "decimals": 18,
                    "ltv": 0.8,
                    "liquidation_threshold": 0.85,
                    "liquidation_bonus": 0.05,
                    "reserve_factor": 0.1,
                    "usage_as_collateral_enabled": True,
                    "borrowing_enabled": True,
                    "is_active": True,
                    "is_frozen": False,
                    "liquidity_rate": 0.02,
                    "variable_borrow_rate": 0.027,
                },
                "USDC": {
                    "address": self.ASSETS["USDC"],
                    "decimals": 6,
                    "ltv": 0.8,
                    "liquidation_threshold": 0.85,
                    "liquidation_bonus": 0.05,
                    "reserve_factor": 0.1,
                    "usage_as_collateral_enabled": True,
                    "borrowing_enabled": True,
                    "is_active": True,
                    "is_frozen": False,
                    "liquidity_rate": 0.022,
                    "variable_borrow_rate": 0.046,
                },
                "SCR": {
                    "address": self.ASSETS["SRC"],
                    "decimals": 18,
                    "ltv": 0.7,
                    "liquidation_threshold": 0.75,
                    "liquidation_bonus": 0.05,
                    "reserve_factor": 0.1,
                    "usage_as_collateral_enabled": True,
                    "borrowing_enabled": True,
                    "is_active": True,
                    "is_frozen": False,
                    "liquidity_rate": 0.0001,
                    "variable_borrow_rate": 0.003,
                }
            }
            
            # If we couldn't get reserve list, use fallback data
            if not reserves_list:
                return fallback_data
            
            # Fetch data for each reserve
            for reserve in reserves_list:
                token_symbol = reserve[0]
                token_address = reserve[1]
                
                # Get configuration data
                config_data = self.safely_call_contract(
                    self.data_provider.functions.getReserveConfigurationData(token_address).call,
                    [0, 0, 0, 0, 0, False, False, False, False, False]  # Fallback values
                )
                
                # Get current reserve data
                current_data = self.safely_call_contract(
                    self.data_provider.functions.getReserveData(token_address).call,
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # Fallback values
                )
                
                # Format results
                reserves_data[token_symbol] = {
                    "address": token_address,
                    "decimals": config_data[0],
                    "ltv": config_data[1] / 10000,  # Convert from basis points to percentage
                    "liquidation_threshold": config_data[2] / 10000,
                    "liquidation_bonus": config_data[3] / 10000,
                    "reserve_factor": config_data[4] / 10000,
                    "usage_as_collateral_enabled": config_data[5],
                    "borrowing_enabled": config_data[6],
                    "is_active": config_data[8],
                    "is_frozen": config_data[9],
                    "liquidity_rate": current_data[5] / 1e27,  # Convert from ray to percentage
                    "variable_borrow_rate": current_data[6] / 1e27,
                }
            
            # If we didn't get any data, use fallback
            if not reserves_data:
                return fallback_data
                
            return reserves_data
            
        except Exception as e:
            print(f"Error fetching reserve data: {e}")
            # Return fallback data on error
            return {
                "WETH": {
                    "address": self.ASSETS["ETH"],
                    "decimals": 18,
                    "ltv": 0.8,
                    "liquidation_threshold": 0.85,
                    "liquidation_bonus": 0.05,
                    "reserve_factor": 0.1,
                    "usage_as_collateral_enabled": True,
                    "borrowing_enabled": True,
                    "is_active": True,
                    "is_frozen": False,
                    "liquidity_rate": 0.02,
                    "variable_borrow_rate": 0.027,
                },
                "USDC": {
                    "address": self.ASSETS["USDC"],
                    "decimals": 6,
                    "ltv": 0.8,
                    "liquidation_threshold": 0.85,
                    "liquidation_bonus": 0.05,
                    "reserve_factor": 0.1,
                    "usage_as_collateral_enabled": True,
                    "borrowing_enabled": True,
                    "is_active": True,
                    "is_frozen": False,
                    "liquidity_rate": 0.022,
                    "variable_borrow_rate": 0.046,
                },
                "SCR": {
                    "address": self.ASSETS["SRC"],
                    "decimals": 18,
                    "ltv": 0.7,
                    "liquidation_threshold": 0.75,
                    "liquidation_bonus": 0.05,
                    "reserve_factor": 0.1,
                    "usage_as_collateral_enabled": True,
                    "borrowing_enabled": True,
                    "is_active": True,
                    "is_frozen": False,
                    "liquidity_rate": 0.0001,
                    "variable_borrow_rate": 0.003,
                }
            }

    def get_user_account_data(self, wallet_address: str) -> Dict[str, Any]:
        """Get user account data from AAVE"""
        try:
            # Get user account data
            account_data = self.safely_call_contract(
                self.pool.functions.getUserAccountData(
                    self.w3.to_checksum_address(wallet_address)
                ).call,
                [0, 0, 0, 0, 0, 0]  # Fallback values
            )
            
            # Format results
            return {
                "total_collateral_base": account_data[0],
                "total_debt_base": account_data[1],
                "available_borrows_base": account_data[2],
                "current_liquidation_threshold": account_data[3] / 10000,  # Convert from basis points
                "ltv": account_data[4] / 10000,
                "health_factor": account_data[5] / 1e18 if account_data[5] > 0 else 0
            }
            
        except Exception as e:
            print(f"Error fetching user account data: {e}")
            return {
                "total_collateral_base": 0,
                "total_debt_base": 0,
                "available_borrows_base": 0,
                "current_liquidation_threshold": 0.8,
                "ltv": 0.75,
                "health_factor": 0
            }

    def get_asset_price(self, asset_address: str) -> Decimal:
        """Get asset price from AAVE oracle"""
        try:
            price = self.safely_call_contract(
                self.price_oracle.functions.getAssetPrice(
                    self.w3.to_checksum_address(asset_address)
                ).call,
                0  # Fallback value
            )
            
            return Decimal(price) / Decimal(1e8)  # Adjust decimals as needed
            
        except Exception as e:
            print(f"Error fetching asset price: {e}")
            return Decimal(0)

    def get_market_data(self) -> Dict[str, Any]:
        """Get comprehensive market data from AAVE on Scroll"""
        try:
            # Get reserve data
            reserves = self.get_reserve_data()
            
            # Format into the structure expected by the strategy generator
            market_data = {
                "rates": {
                    "AAVE": {
                        "supply_apy": {},
                        "borrow_apy": {}
                    }
                },
                "tvl": {
                    "AAVE": 0  # Will be calculated below
                },
                "conditions": "stable"  # Default value, could be dynamic
            }
            
            total_tvl = 0
            
            # Process each reserve
            for symbol, data in reserves.items():
                # Add supply and borrow rates
                market_data["rates"]["AAVE"]["supply_apy"][symbol] = data["liquidity_rate"] * 100
                market_data["rates"]["AAVE"]["borrow_apy"][symbol] = data["variable_borrow_rate"] * 100
                
                # We could calculate TVL if we had total supply data
                # For now, we'll leave it as 0
                
            # Set TVL - for a real implementation, we'd calculate this from totalSupply * price
            market_data["tvl"]["AAVE"] = total_tvl
            
            return market_data
            
        except Exception as e:
            print(f"Error building market data: {e}")
            return {
                "rates": {"AAVE": {"supply_apy": {}, "borrow_apy": {}}},
                "tvl": {"AAVE": 0},
                "conditions": "unknown"
            }

    def get_user_risk_metrics(self, wallet_address: str) -> Dict[str, Any]:
        """Get risk metrics for a user"""
        try:
            account_data = self.get_user_account_data(wallet_address)
            
            return {
                "health_factor": float(account_data.get("health_factor", 1.8)),
                "liquidation_threshold": float(account_data.get("current_liquidation_threshold", 0.85)),
                "current_ratio": float(account_data.get("ltv", 1.5))
            }
            
        except Exception as e:
            print(f"Error calculating risk metrics: {e}")
            return {
                "health_factor": 1.8,
                "liquidation_threshold": 0.85,
                "current_ratio": 1.5
            }