# ai/services/quill_service.py
from typing import Dict, List, Optional, Any
import os
from decimal import Decimal
import json
import web3
from web3 import Web3

# Handle different versions of web3.py with comprehensive fallbacks
geth_poa_middleware = None
try:
    # Try the most common import path first
    from web3.middleware import geth_poa_middleware
except ImportError:
    try:
        # Try newer web3.py version import
        from web3.middleware.geth import geth_poa_middleware
    except ImportError:
        try:
            # Another possible location
            from web3.geth import geth_poa_middleware
        except ImportError:
            # Final fallback - we'll handle missing middleware gracefully
            print("Warning: Could not import geth_poa_middleware, continuing without it")
            geth_poa_middleware = None

# Import ABIs
from .abis.quill_borrower_operations_abi import BORROWER_OPERATIONS_ABI
from .abis.quill_trove_manager_abi import TROVE_MANAGER_ABI
from .abis.quill_stability_pool_abi import STABILITY_POOL_ABI
from .abis.quill_usdq_token_abi import USDQ_TOKEN_ABI

class QuillService:
    """Service for interacting with Quill Finance protocol on Scroll network"""
    
    # Scroll network constants with actual values
    SCROLL_RPC_URL = os.getenv("WEB3_PROVIDER_URI", "https://rpc.scroll.io/")
    
    # Quill contract addresses on Scroll
    COLLATERAL_REGISTRY = "0xcc4f29f9d1b03c8e77fc0057a120e2c370d6863d"
    USDQ_TOKEN = "0x6f2a1a886dbf8e36c4fa9f25a517861a930fbf3a"
    
    # Branch-specific contracts (using WETH branch as default)
    WETH_BORROWER_OPERATIONS = "0x05b229f984584589d9af5f768eb4bfccb3f8324f"
    WETH_TROVE_MANAGER = "0x8df7b9f31db3980732a1541c49e50bda62846655"
    WETH_STABILITY_POOL = "0x2c627886421ee62e1c51a4b4248a751089ae57b6"
    
    WSTETH_BORROWER_OPERATIONS = "0xb141f8b767e55099cea16cf969d23d6e0cb2db95"
    WSTETH_TROVE_MANAGER = "0x511973b7e39682f258ce9a5745c7450ce6af3d11"
    WSTETH_STABILITY_POOL = "0x4c05eecd9193e0ac8bc80e3e4248e7808d89eb9b"
    
    WEETH_BORROWER_OPERATIONS = "0x7260e429473f872307f67b2a6267695353b413c9"
    WEETH_TROVE_MANAGER = "0xee7a132c4775d22ff204f017a7f3200df9eb1eaa"
    WEETH_STABILITY_POOL = "0x01149666c61f5a605d2f9296d9da3b49165e04ec"
    
    SCR_BORROWER_OPERATIONS = "0xf02433e0f4d85216915502b800490c7172dc23e8"
    SCR_TROVE_MANAGER = "0x64493522dd375890fd2eb25324e3555279b505b2"
    SCR_STABILITY_POOL = "0xbcb64a2eff9cd8d10f24b5fc74031a157391a496"
    
    # Token addresses on Scroll
    TOKENS = {
        "ETH": "0x5300000000000000000000000000000000000004",  # WETH on Scroll
        "wstETH": "0xf610a9dfb7c89644979b4a0f27063e9e7d7cda32",
        "weETH": "0x01f0a31698c4d065659b9bdc21b3610292a1c506",
        "SRC": "0xd29687c813d741e2f938f4ac377128810e217b1b",
        "USDQ": "0x6f2a1a886dbf8e36c4fa9f25a517861a930fbf3a"
    }
    
    # Token decimals
    DECIMALS = {
        "ETH": 18,
        "wstETH": 18,
        "weETH": 18,
        "SRC": 18,
        "USDQ": 18
    }
    
    # Minimum collateral ratios
    MIN_COLLATERAL_RATIOS = {
        "ETH": 1.1,       # 110%
        "wstETH": 1.1,    # 110%
        "weETH": 1.1,     # 110%
        "SRC": 1.15       # 115% (slightly higher for more volatile asset)
    }
    
    # Default interest rates for different risk levels
    DEFAULT_INTEREST_RATES = {
        "low": 0.06,      # 6% (conservative)
        "medium": 0.1,    # 10% (balanced)
        "high": 0.15      # 15% (aggressive)
    }
    
    def __init__(self):
        # Initialize Web3 connection
        self.w3 = Web3(Web3.HTTPProvider(self.SCROLL_RPC_URL))
        
        # Only inject middleware if available
        if geth_poa_middleware is not None:
            try:
                self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
                print("POA middleware injected successfully")
            except Exception as e:
                print(f"Warning: Failed to inject POA middleware: {e}. Continuing without it.")
        
        # Test connection
        if not self.w3.is_connected():
            print(f"Failed to connect to {self.SCROLL_RPC_URL}")
            self.w3 = None
        else:
            print(f"Connected to {self.SCROLL_RPC_URL}")
            
            # Initialize contract interfaces
            try:
                # USDQ Token contract
                self.usdq_token = self.w3.eth.contract(
                    address=self.w3.to_checksum_address(self.USDQ_TOKEN),
                    abi=USDQ_TOKEN_ABI
                )
                
                # Initialize branch-specific contracts
                self._initialize_branch_contracts()
                
                print("Quill contracts initialized successfully")
            except Exception as e:
                print(f"Error initializing Quill contracts: {e}")
                self.w3 = None

    def _initialize_branch_contracts(self):
        """Initialize branch-specific contract interfaces"""
        # Initialize WETH branch contracts
        self.weth_borrower_operations = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.WETH_BORROWER_OPERATIONS),
            abi=BORROWER_OPERATIONS_ABI
        )
        self.weth_trove_manager = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.WETH_TROVE_MANAGER),
            abi=TROVE_MANAGER_ABI
        )
        self.weth_stability_pool = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.WETH_STABILITY_POOL),
            abi=STABILITY_POOL_ABI
        )
        
        # Initialize wstETH branch contracts
        self.wsteth_borrower_operations = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.WSTETH_BORROWER_OPERATIONS),
            abi=BORROWER_OPERATIONS_ABI
        )
        self.wsteth_trove_manager = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.WSTETH_TROVE_MANAGER),
            abi=TROVE_MANAGER_ABI
        )
        self.wsteth_stability_pool = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.WSTETH_STABILITY_POOL),
            abi=STABILITY_POOL_ABI
        )
        
        # Initialize weETH branch contracts
        self.weeth_borrower_operations = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.WEETH_BORROWER_OPERATIONS),
            abi=BORROWER_OPERATIONS_ABI
        )
        self.weeth_trove_manager = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.WEETH_TROVE_MANAGER),
            abi=TROVE_MANAGER_ABI
        )
        self.weeth_stability_pool = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.WEETH_STABILITY_POOL),
            abi=STABILITY_POOL_ABI
        )
        
        # Initialize SCR branch contracts
        self.scr_borrower_operations = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.SCR_BORROWER_OPERATIONS),
            abi=BORROWER_OPERATIONS_ABI
        )
        self.scr_trove_manager = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.SCR_TROVE_MANAGER),
            abi=TROVE_MANAGER_ABI
        )
        self.scr_stability_pool = self.w3.eth.contract(
            address=self.w3.to_checksum_address(self.SCR_STABILITY_POOL),
            abi=STABILITY_POOL_ABI
        )

    def safely_call_contract(self, contract_method, fallback_value=None, *args, **kwargs):
        """Safely call a contract method with fallback value on error"""
        try:
            return contract_method(*args, **kwargs)
        except Exception as e:
            print(f"Error calling contract method {contract_method.__name__ if hasattr(contract_method, '__name__') else 'unknown'}: {e}")
            return fallback_value

    def _get_branch_contracts(self, collateral_token: str):
        """Get the appropriate branch contracts based on collateral token"""
        token_upper = collateral_token.upper()
        
        if token_upper == "ETH" or token_upper == "WETH":
            return self.weth_borrower_operations, self.weth_trove_manager, self.weth_stability_pool
        elif token_upper == "WSTETH":
            return self.wsteth_borrower_operations, self.wsteth_trove_manager, self.wsteth_stability_pool
        elif token_upper == "WEETH":
            return self.weeth_borrower_operations, self.weeth_trove_manager, self.weeth_stability_pool
        elif token_upper == "SRC":
            return self.scr_borrower_operations, self.scr_trove_manager, self.scr_stability_pool
        else:
            raise ValueError(f"Unsupported collateral token: {collateral_token}")

    def get_trove_info(self, wallet_address: str, collateral_token: str) -> Dict[str, Any]:
        """Get information about a user's Trove for a specific collateral"""
        if not self.w3:
            return {
                "exists": False,
                "collateral_amount": 0,
                "debt": 0,
                "collateral_ratio": 0,
                "interest_rate": 0
            }
            
        try:
            # Get the appropriate branch contracts
            _, trove_manager, _ = self._get_branch_contracts(collateral_token)
            
            # Check if the Trove exists
            trove_exists = self.safely_call_contract(
                trove_manager.functions.containsTrove(
                    self.w3.to_checksum_address(wallet_address)
                ).call,
                False
            )
            
            if not trove_exists:
                return {
                    "exists": False,
                    "collateral_amount": 0,
                    "debt": 0,
                    "collateral_ratio": 0,
                    "interest_rate": 0
                }
            
            # Get Trove details
            trove_debt = self.safely_call_contract(
                trove_manager.functions.getTroveDebt(
                    self.w3.to_checksum_address(wallet_address)
                ).call,
                0
            )
            
            trove_coll = self.safely_call_contract(
                trove_manager.functions.getTroveColl(
                    self.w3.to_checksum_address(wallet_address)
                ).call,
                0
            )
            
            # Get interest rate
            interest_rate = self.safely_call_contract(
                trove_manager.functions.getTroveInterestRateSimple(
                    self.w3.to_checksum_address(wallet_address)
                ).call,
                0
            )
            
            # Convert values to human-readable format
            debt_decimal = Decimal(trove_debt) / Decimal(10 ** self.DECIMALS["USDQ"])
            coll_decimal = Decimal(trove_coll) / Decimal(10 ** self.DECIMALS[collateral_token.upper()])
            interest_rate_decimal = Decimal(interest_rate) / Decimal(1e18)  # Assuming 18 decimals
            
            # Calculate collateral ratio
            collateral_ratio = 0
            if debt_decimal > 0:
                # In a real implementation, we would need to get the collateral price
                # For this example, let's use a placeholder price
                collateral_price = self.get_collateral_price(collateral_token)
                collateral_value = coll_decimal * collateral_price
                collateral_ratio = collateral_value / debt_decimal
            
            return {
                "exists": True,
                "collateral_amount": float(coll_decimal),
                "debt": float(debt_decimal),
                "collateral_ratio": float(collateral_ratio),
                "interest_rate": float(interest_rate_decimal)
            }
            
        except Exception as e:
            print(f"Error getting Trove info: {e}")
            return {
                "exists": False,
                "collateral_amount": 0,
                "debt": 0,
                "collateral_ratio": 0,
                "interest_rate": 0
            }

    def get_collateral_price(self, collateral_token: str) -> Decimal:
        """Get the current price of a collateral token in USD"""
        # In a real implementation, this would query the price feed contracts
        # For this example, let's use hardcoded prices
        collateral_prices = {
            "ETH": Decimal("2000"),
            "WETH": Decimal("2000"),
            "wstETH": Decimal("2100"),  # Slight premium for staked ETH
            "weETH": Decimal("2080"),   # Slight premium for staked ETH
            "SRC": Decimal("10")
        }
        
        return collateral_prices.get(collateral_token.upper(), Decimal("0"))

    def get_max_borrowable_amount(self, collateral_token: str, collateral_amount: Decimal) -> Decimal:
        """Calculate maximum borrowable amount for a given collateral amount"""
        try:
            # Get collateral price
            collateral_price = self.get_collateral_price(collateral_token)
            
            # Get minimum collateral ratio
            min_ratio = self.MIN_COLLATERAL_RATIOS.get(collateral_token.upper(), Decimal("1.5"))
            
            # Calculate max borrowable amount (collateral_value / min_ratio)
            collateral_value = collateral_amount * collateral_price
            max_borrowable = collateral_value / min_ratio
            
            return max_borrowable
            
        except Exception as e:
            print(f"Error calculating max borrowable amount: {e}")
            return Decimal("0")

    def estimate_stability_pool_apy(self) -> Decimal:
        """Estimate the APY for providing to the stability pool"""
        # In a real implementation, this would be calculated based on protocol data
        # For this example, let's use a hardcoded estimate
        return Decimal("0.05")  # 5% APY

    def get_market_data(self) -> Dict[str, Any]:
        """Get market data for Quill Finance"""
        try:
            # In a real implementation, this would fetch data from the contracts
            # For this example, let's use hardcoded estimates
            
            # Estimate stability pool APY
            stability_pool_apy = self.estimate_stability_pool_apy()
            
            # Get collateral factors
            collateral_factors = {}
            for token in ["ETH", "wstETH", "weETH", "SRC"]:
                collateral_factors[token] = {
                    "min_collateral_ratio": float(self.MIN_COLLATERAL_RATIOS.get(token, 1.1)),
                    "price": float(self.get_collateral_price(token))
                }
            
            return {
                "stability_pool_apy": float(stability_pool_apy) * 100,  # Convert to percentage
                "collateral_factors": collateral_factors,
                "borrowing_fee": 0.005,  # 0.5% borrowing fee
                "redemption_fee": 0.01,  # 1% redemption fee
                "interest_rates": {
                    "min": 0.06,  # 6%
                    "max": 3.50,  # 350%
                    "recommended": {
                        "low_risk": 0.06,    # 6%
                        "medium_risk": 0.10,  # 10%
                        "high_risk": 0.15    # 15%
                    }
                }
            }
            
        except Exception as e:
            print(f"Error getting Quill market data: {e}")
            return {
                "stability_pool_apy": 5.0,  # 5%
                "collateral_factors": {
                    "ETH": {"min_collateral_ratio": 1.1, "price": 2000.0},
                    "wstETH": {"min_collateral_ratio": 1.1, "price": 2100.0},
                    "weETH": {"min_collateral_ratio": 1.1, "price": 2080.0},
                    "SRC": {"min_collateral_ratio": 1.15, "price": 10.0}
                },
                "borrowing_fee": 0.005,
                "redemption_fee": 0.01,
                "interest_rates": {
                    "min": 0.06,
                    "max": 3.50,
                    "recommended": {
                        "low_risk": 0.06,
                        "medium_risk": 0.10,
                        "high_risk": 0.15
                    }
                }
            }