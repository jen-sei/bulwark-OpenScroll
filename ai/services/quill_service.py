# ai/services/quill_service.py
import os
from decimal import Decimal
from typing import Dict, List, Optional, Any

# Try different imports for Web3 middleware based on version
try:
    from web3 import Web3
    from web3.middleware import geth_poa_middleware
    has_geth_middleware = True
except ImportError:
    try:
        from web3 import Web3
        from web3.middleware.geth import geth_poa_middleware
        has_geth_middleware = True
    except ImportError:
        try:
            from web3 import Web3
            from web3.geth import geth_poa_middleware
            has_geth_middleware = True
        except ImportError:
            from web3 import Web3
            has_geth_middleware = False
            print("Couldn't import geth_poa_middleware, continuing without it")

# Import ABIs
from .abis.quill_borrower_operations_abi import QUILL_BORROWER_OPERATIONS_ABI
from .abis.quill_trove_manager_abi import QUILL_TROVE_MANAGER_ABI
from .abis.quill_stability_pool_abi import QUILL_STABILITY_POOL_ABI
from .abis.quill_price_feed_abi import QUILL_PRICE_FEED_ABI
from .abis.quill_usdq_token_abi import USDQ_TOKEN_ABI

class QuillService:
    """Service for interacting with Quill Finance on Scroll network"""
    
    # Quill contract addresses
    COLLATERAL_REGISTRY = "0xcc4f29f9d1b03c8e77fc0057a120e2c370d6863d"
    USDQ_TOKEN = "0x6f2a1a886dbf8e36c4fa9f25a517861a930fbf3a"
    
    # Address mappings for different collaterals
    COLLATERAL_TYPES = {
        "ETH": {
            "registry": "0x22cb3cfe6205e0edbad751de8cf3612625cefe80",
            "token": "0x5300000000000000000000000000000000000004",
            "borrower_operations": "0x05b229f984584589d9af5f768eb4bfccb3f8324f",
            "trove_manager": "0x8df7b9f31db3980732a1541c49e50bda62846655",
            "stability_pool": "0x2c627886421ee62e1c51a4b4248a751089ae57b6",
            "price_feed": "0xf42fb3da9628e86476f26f71cf608cb1b109e8e8",
            "min_collateral_ratio": Decimal("1.1"),  # 110%
            "liquidation_reserve": Decimal("200"),  # USDQ
            "decimals": 18
        },
        "SRC": {
            "registry": "0xdc60fc54fcb9e690b1d328e2e7507d484e528c85",
            "token": "0xd29687c813d741e2f938f4ac377128810e217b1b",
            "borrower_operations": "0xf02433e0f4d85216915502b800490c7172dc23e8",
            "trove_manager": "0x64493522dd375890fd2eb25324e3555279b505b2",
            "stability_pool": "0xbcb64a2eff9cd8d10f24b5fc74031a157391a496",
            "price_feed": "0xf564fdd6c5414d88ab954ca1af1be7ae18e36737",
            "min_collateral_ratio": Decimal("1.15"),  # 115% (higher due to SRC volatility)
            "liquidation_reserve": Decimal("200"),  # USDQ
            "decimals": 18
        },
        "wstETH": {
            "registry": "0xfba16199038b5b347cf8b1f2c769ac3347797b60",
            "token": "0xf610a9dfb7c89644979b4a0f27063e9e7d7cda32",
            "borrower_operations": "0xb141f8b767e55099cea16cf969d23d6e0cb2db95",
            "trove_manager": "0x511973b7e39682f258ce9a5745c7450ce6af3d11",
            "stability_pool": "0x4c05eecd9193e0ac8bc80e3e4248e7808d89eb9b",
            "price_feed": "0xa316e6f3245c5dbbdae1fc9ad0cbe87f75087f7f",
            "min_collateral_ratio": Decimal("1.15"),  # 115%
            "liquidation_reserve": Decimal("200"),  # USDQ
            "decimals": 18
        },
        "weETH": {
            "registry": "0x177798337a5239eb48909c3efe2b1199c1cb7ff7",
            "token": "0x01f0a31698c4d065659b9bdc21b3610292a1c506",
            "borrower_operations": "0x7260e429473f872307f67b2a6267695353b413c9",
            "trove_manager": "0xee7a132c4775d22ff204f017a7f3200df9eb1eaa",
            "stability_pool": "0x01149666c61f5a605d2f9296d9da3b49165e04ec",
            "price_feed": "0x2c310980e94e8e9fb5f67e1db171729f71c5a896",
            "min_collateral_ratio": Decimal("1.15"),  # 115%
            "liquidation_reserve": Decimal("200"),  # USDQ
            "decimals": 18
        }
    }
    
    # RPC URL
    SCROLL_RPC_URL = os.environ.get("WEB3_PROVIDER_URI", "https://rpc.scroll.io/")
    
    def __init__(self):
        """Initialize the Quill service with Web3 connection"""
        print("Initializing Quill service...")
        try:
            # Initialize Web3 connection
            self.w3 = Web3(Web3.HTTPProvider(self.SCROLL_RPC_URL))
            
            # Add middleware for POA chains
            if has_geth_middleware:
                self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
                print("POA middleware injected successfully")
            
            if not self.w3.is_connected():
                print(f"Failed to connect to {self.SCROLL_RPC_URL}")
                self.w3 = None
            else:
                print(f"Connected to {self.SCROLL_RPC_URL}")
                
                # Initialize contracts
                self.initialize_contracts()
                print("Quill contracts initialized successfully")
        except Exception as e:
            print(f"Error initializing Quill service: {e}")
            self.w3 = None
    
    def initialize_contracts(self):
        """Initialize all contract interfaces"""
        # Initialize contracts for each collateral type
        for collateral, addresses in self.COLLATERAL_TYPES.items():
            try:
                # Initialize price feed contract
                price_feed_address = self.w3.to_checksum_address(addresses["price_feed"])
                addresses["price_feed_contract"] = self.w3.eth.contract(
                    address=price_feed_address,
                    abi=QUILL_PRICE_FEED_ABI
                )
                
                # Initialize borrower operations contract
                borrower_ops_address = self.w3.to_checksum_address(addresses["borrower_operations"])
                addresses["borrower_operations_contract"] = self.w3.eth.contract(
                    address=borrower_ops_address,
                    abi=QUILL_BORROWER_OPERATIONS_ABI
                )
                
                # Initialize trove manager contract
                trove_manager_address = self.w3.to_checksum_address(addresses["trove_manager"])
                addresses["trove_manager_contract"] = self.w3.eth.contract(
                    address=trove_manager_address,
                    abi=QUILL_TROVE_MANAGER_ABI
                )
                
                # Initialize stability pool contract
                stability_pool_address = self.w3.to_checksum_address(addresses["stability_pool"])
                addresses["stability_pool_contract"] = self.w3.eth.contract(
                    address=stability_pool_address,
                    abi=QUILL_STABILITY_POOL_ABI
                )
            except Exception as e:
                print(f"Error initializing contracts for {collateral}: {e}")
    
    def safely_call_contract(self, contract, method_name, *args, **kwargs):
        """Safely call a contract method with error handling"""
        try:
            method = getattr(contract.functions, method_name)
            result = method(*args, **kwargs).call()
            return result
        except Exception as e:
            print(f"Error calling contract method {method_name}: {e}")
            return None
    
    def get_collateral_price(self, collateral: str) -> Optional[Decimal]:
        """Get the current price of a collateral asset in USD"""
        if self.w3 is None:
            return None
        
        collateral = collateral.upper()
        if collateral not in self.COLLATERAL_TYPES:
            print(f"Unsupported collateral type: {collateral}")
            return None
        
        try:
            price_feed = self.COLLATERAL_TYPES[collateral]["price_feed_contract"]
            # Try to get the price, fall back to lastGoodPrice if fetchPrice fails
            try:
                price = self.safely_call_contract(price_feed, "fetchPrice")
                if price is None:
                    price = self.safely_call_contract(price_feed, "lastGoodPrice")
            except Exception:
                price = self.safely_call_contract(price_feed, "lastGoodPrice")
            
            if price is None:
                # Use fallback prices for testing
                fallback_prices = {
                    "ETH": Decimal("2000"),
                    "SRC": Decimal("10"),
                    "wstETH": Decimal("2100"),
                    "weETH": Decimal("2080")
                }
                return fallback_prices.get(collateral, Decimal("0"))
            
            # Convert to human-readable decimal (Quill prices are in 1e18 format)
            return Decimal(price) / Decimal(10**18)
        except Exception as e:
            print(f"Error getting price for {collateral}: {e}")
            # Use fallback prices for testing
            fallback_prices = {
                "ETH": Decimal("2000"),
                "SRC": Decimal("10"),
                "wstETH": Decimal("2100"),
                "weETH": Decimal("2080")
            }
            return fallback_prices.get(collateral, Decimal("0"))
    
    def get_trove_data(self, wallet_address: str, collateral: str) -> Optional[Dict[str, Any]]:
        """Get data for a specific trove owned by the wallet"""
        if self.w3 is None:
            return None
        
        collateral = collateral.upper()
        if collateral not in self.COLLATERAL_TYPES:
            print(f"Unsupported collateral type: {collateral}")
            return None
        
        try:
            wallet_address = self.w3.to_checksum_address(wallet_address)
            trove_manager = self.COLLATERAL_TYPES[collateral]["trove_manager_contract"]
            
            # Get trove data - implementations may vary, check the specific method
            debt = self.safely_call_contract(trove_manager, "getTroveDebt", wallet_address)
            coll = self.safely_call_contract(trove_manager, "getTroveColl", wallet_address)
            status = self.safely_call_contract(trove_manager, "getTroveStatus", wallet_address)
            
            # If we couldn't get data or trove doesn't exist (status 0)
            if debt is None or coll is None or status is None or status == 0:
                return None
            
            # Convert values to human-readable format
            debt_decimal = Decimal(debt) / Decimal(10**18)  # USDQ has 18 decimals
            coll_decimal = Decimal(coll) / Decimal(10**self.COLLATERAL_TYPES[collateral]["decimals"])
            
            # Get current price to calculate collateral ratio
            price = self.get_collateral_price(collateral)
            if price is None:
                return {
                    "debt": debt_decimal,
                    "collateral": coll_decimal,
                    "status": status,
                    "collateral_value_usd": None,
                    "collateral_ratio": None
                }
            
            collateral_value_usd = coll_decimal * price
            collateral_ratio = collateral_value_usd / debt_decimal if debt_decimal > 0 else Decimal("999")
            
            return {
                "debt": debt_decimal,
                "collateral": coll_decimal,
                "status": status,
                "collateral_value_usd": collateral_value_usd,
                "collateral_ratio": collateral_ratio
            }
        except Exception as e:
            print(f"Error getting trove data for {wallet_address} with {collateral}: {e}")
            return None
    
    def get_max_borrowable_amount(self, collateral: str, amount: Decimal) -> Optional[Decimal]:
        """Calculate the maximum USDQ that can be borrowed for a given collateral amount"""
        collateral = collateral.upper()
        if collateral not in self.COLLATERAL_TYPES:
            print(f"Unsupported collateral type: {collateral}")
            return Decimal("0")
        
        try:
            # Get the price of the collateral
            price = self.get_collateral_price(collateral)
            if price is None:
                # Fallback to hardcoded prices for testing
                fallback_prices = {
                    "ETH": Decimal("2000"),
                    "SRC": Decimal("10"),
                    "wstETH": Decimal("2100"),
                    "weETH": Decimal("2080")
                }
                price = fallback_prices.get(collateral, Decimal("0"))
                if price == Decimal("0"):
                    return Decimal("0")
            
            # Calculate the total value of the collateral
            collateral_value_usd = amount * price
            
            # Calculate max borrowable amount based on minimum collateral ratio
            min_ratio = self.COLLATERAL_TYPES[collateral]["min_collateral_ratio"]
            liquidation_reserve = self.COLLATERAL_TYPES[collateral]["liquidation_reserve"]
            
            # Maximum borrowable is (collateral_value / min_ratio) - liquidation_reserve
            max_borrowable = (collateral_value_usd / min_ratio) - liquidation_reserve
            
            # For smaller amounts, we need to be more conservative to avoid negative values
            if max_borrowable <= 0:
                # For smaller amounts, just set a small proportion of the collateral value
                max_borrowable = collateral_value_usd * Decimal("0.7")  # 70% of collateral value
            
            # Apply additional scaling for SRC due to higher volatility
            if collateral == "SRC":
                max_borrowable = max_borrowable * Decimal("0.5")  # More conservative with SRC
            
            # For hackathon testing, cap the maximum USDQ at 50 to avoid unreasonable values
            max_borrowable = min(max_borrowable, Decimal("50"))
            
            # Ensure we don't return a negative value
            return max(Decimal("0"), max_borrowable)
        except Exception as e:
            print(f"Error calculating max borrowable amount: {e}")
            return Decimal("0")
    
    def get_stability_pool_data(self, collateral: str) -> Optional[Dict[str, Any]]:
        """Get data about the stability pool for a specific collateral"""
        if self.w3 is None:
            return None
        
        collateral = collateral.upper()
        if collateral not in self.COLLATERAL_TYPES:
            print(f"Unsupported collateral type: {collateral}")
            return None
        
        try:
            stability_pool = self.COLLATERAL_TYPES[collateral]["stability_pool_contract"]
            
            # Get total USDQ deposits
            total_deposits = self.safely_call_contract(stability_pool, "getTotalUSDQDeposits")
            
            # Get pool collateral
            pool_eth = self.safely_call_contract(stability_pool, "getETH")
            
            if total_deposits is None or pool_eth is None:
                return {
                    "total_deposits_usdq": Decimal("0"),
                    "pool_collateral": Decimal("0"),
                    "pool_collateral_value_usd": Decimal("0")
                }
            
            # Convert to human-readable format
            total_deposits_decimal = Decimal(total_deposits) / Decimal(10**18)
            pool_eth_decimal = Decimal(pool_eth) / Decimal(10**18)
            
            # Get collateral price for USD value
            price = self.get_collateral_price(collateral)
            if price is None:
                return {
                    "total_deposits_usdq": total_deposits_decimal,
                    "pool_collateral": pool_eth_decimal,
                    "pool_collateral_value_usd": Decimal("0")
                }
            
            pool_value_usd = pool_eth_decimal * price
            
            return {
                "total_deposits_usdq": total_deposits_decimal,
                "pool_collateral": pool_eth_decimal,
                "pool_collateral_value_usd": pool_value_usd
            }
        except Exception as e:
            print(f"Error getting stability pool data for {collateral}: {e}")
            return {
                "total_deposits_usdq": Decimal("0"),
                "pool_collateral": Decimal("0"),
                "pool_collateral_value_usd": Decimal("0")
            }
    
    def get_user_stability_pool_data(self, wallet_address: str, collateral: str) -> Optional[Dict[str, Any]]:
        """Get data about a user's deposits in the stability pool"""
        if self.w3 is None:
            return None
        
        collateral = collateral.upper()
        if collateral not in self.COLLATERAL_TYPES:
            print(f"Unsupported collateral type: {collateral}")
            return None
        
        try:
            wallet_address = self.w3.to_checksum_address(wallet_address)
            stability_pool = self.COLLATERAL_TYPES[collateral]["stability_pool_contract"]
            
            # Get user's deposit
            deposit = self.safely_call_contract(stability_pool, "getCompoundedUSDQDeposit", wallet_address)
            
            # Get user's collateral gain
            collateral_gain = self.safely_call_contract(stability_pool, "getDepositorCollateralGain", wallet_address)
            
            # Get user's USDQ gain
            usdq_gain = self.safely_call_contract(stability_pool, "getDepositorUSDQGain", wallet_address)
            
            if deposit is None or collateral_gain is None or usdq_gain is None:
                return {
                    "deposit_usdq": Decimal("0"),
                    "collateral_gain": Decimal("0"),
                    "usdq_gain": Decimal("0"),
                    "collateral_gain_value_usd": Decimal("0")
                }
            
            # Convert to human-readable format
            deposit_decimal = Decimal(deposit) / Decimal(10**18)
            collateral_gain_decimal = Decimal(collateral_gain) / Decimal(10**18)
            usdq_gain_decimal = Decimal(usdq_gain) / Decimal(10**18)
            
            # Get collateral price for USD value
            price = self.get_collateral_price(collateral)
            if price is None:
                return {
                    "deposit_usdq": deposit_decimal,
                    "collateral_gain": collateral_gain_decimal,
                    "usdq_gain": usdq_gain_decimal,
                    "collateral_gain_value_usd": Decimal("0")
                }
            
            collateral_gain_value_usd = collateral_gain_decimal * price
            
            return {
                "deposit_usdq": deposit_decimal,
                "collateral_gain": collateral_gain_decimal,
                "usdq_gain": usdq_gain_decimal,
                "collateral_gain_value_usd": collateral_gain_value_usd
            }
        except Exception as e:
            print(f"Error getting user stability pool data for {wallet_address} with {collateral}: {e}")
            return {
                "deposit_usdq": Decimal("0"),
                "collateral_gain": Decimal("0"),
                "usdq_gain": Decimal("0"),
                "collateral_gain_value_usd": Decimal("0")
            }
    
    def calculate_borrow_apr(self, interest_rate: int) -> Decimal:
        """Calculate the APR for a given interest rate setting (6% to 350%)"""
        # The interest rate is a user-selected parameter in Quill
        # Represent it as a decimal percentage
        return Decimal(str(interest_rate)) / Decimal("100")
    
    def calculate_stability_pool_apr(self, collateral: str) -> Decimal:
        """Estimate the APR for providing liquidity to the stability pool"""
        # This is a simplified calculation - real APR depends on liquidations
        # For now, provide an estimate based on historical data or set rates
        collateral = collateral.upper()
        
        # Default APRs based on collateral type (these are estimates)
        default_aprs = {
            "ETH": Decimal("5.0"),    # 5% APR for ETH stability pool
            "SRC": Decimal("7.0"),    # 7% APR for SRC stability pool
            "WSTETH": Decimal("5.5"), # 5.5% APR for wstETH stability pool
            "WEETH": Decimal("5.5"),  # 5.5% APR for weETH stability pool
        }
        
        return default_aprs.get(collateral, Decimal("5.0"))
    
    def get_market_data(self) -> Dict[str, Any]:
        """Get market data for Quill Finance"""
        market_data = {
            "protocol": "Quill",
            "collaterals": {},
            "stability_pools": {},
            "interest_rates": {
                "min": 6,   # 6% minimum interest rate
                "max": 350  # 350% maximum interest rate
            }
        }
        
        # Get data for each collateral type
        for collateral in self.COLLATERAL_TYPES.keys():
            # Get collateral price
            price = self.get_collateral_price(collateral)
            
            # Get stability pool data
            stability_pool_data = self.get_stability_pool_data(collateral)
            
            # Calculate APRs
            borrow_apr_low = self.calculate_borrow_apr(6)  # Lowest rate
            borrow_apr_med = self.calculate_borrow_apr(50) # Medium rate
            borrow_apr_high = self.calculate_borrow_apr(100) # Higher rate
            stability_apr = self.calculate_stability_pool_apr(collateral)
            
            # Add to market data
            market_data["collaterals"][collateral] = {
                "price_usd": float(price) if price is not None else None,
                "min_collateral_ratio": float(self.COLLATERAL_TYPES[collateral]["min_collateral_ratio"]),
                "liquidation_reserve": float(self.COLLATERAL_TYPES[collateral]["liquidation_reserve"])
            }
            
            # Add stability pool data
            if stability_pool_data:
                market_data["stability_pools"][collateral] = {
                    "total_deposits_usdq": float(stability_pool_data["total_deposits_usdq"]),
                    "pool_collateral": float(stability_pool_data["pool_collateral"]),
                    "estimated_apr": float(stability_apr)
                }
            else:
                market_data["stability_pools"][collateral] = {
                    "total_deposits_usdq": 0,
                    "pool_collateral": 0,
                    "estimated_apr": float(stability_apr)
                }
        
        return market_data
    
    def get_user_positions(self, wallet_address: str) -> Dict[str, Any]:
        """Get all Quill positions for a user across all collateral types"""
        positions = {
            "troves": {},
            "stability_deposits": {}
        }
        
        # Get trove data for each collateral type
        for collateral in self.COLLATERAL_TYPES.keys():
            trove_data = self.get_trove_data(wallet_address, collateral)
            if trove_data and trove_data.get("status", 0) > 0:  # If trove exists
                positions["troves"][collateral] = {
                    "debt_usdq": float(trove_data["debt"]),
                    "collateral_amount": float(trove_data["collateral"]),
                    "collateral_value_usd": float(trove_data["collateral_value_usd"]) if trove_data["collateral_value_usd"] else None,
                    "collateral_ratio": float(trove_data["collateral_ratio"]) if trove_data["collateral_ratio"] else None
                }
            
            # Get stability pool deposits
            sp_data = self.get_user_stability_pool_data(wallet_address, collateral)
            if sp_data and sp_data.get("deposit_usdq", 0) > 0:
                positions["stability_deposits"][collateral] = {
                    "deposit_usdq": float(sp_data["deposit_usdq"]),
                    "collateral_gain": float(sp_data["collateral_gain"]),
                    "usdq_gain": float(sp_data["usdq_gain"])
                }
        
        return positions
    
    def get_recommended_strategies(self, wallet_balances: Dict[str, float]) -> List[Dict[str, Any]]:
        """Get recommended Quill strategies based on user's wallet balances"""
        strategies = []
        
        # Check if we have enough collateral for strategies
        for collateral, amount in wallet_balances.items():
            if collateral.upper() in self.COLLATERAL_TYPES and amount > 0:
                amount_decimal = Decimal(str(amount))
                max_borrowable = self.get_max_borrowable_amount(collateral, amount_decimal)
                
                if max_borrowable and max_borrowable > 0:
                    # Borrowing strategy
                    strategies.append({
                        "name": f"{collateral} Borrowing Strategy",
                        "steps": [
                            {
                                "protocol": "Quill",
                                "action": "borrow_usdq",
                                "token": collateral,
                                "amount": float(amount_decimal),
                                "usdq_amount": float(max_borrowable),
                                "interest_rate": 30,  # Medium interest rate
                                "expected_apy": -30   # Negative APY since this is cost to borrow
                            }
                        ],
                        "expected_outcome": f"Borrow {float(max_borrowable):.2f} USDQ at 30% interest using {collateral} as collateral",
                        "risk_level": 3  # Medium risk
                    })
                    
                    # Stability pool strategy
                    strategies.append({
                        "name": f"USDQ Stability Pool Strategy",
                        "steps": [
                            {
                                "protocol": "Quill",
                                "action": "provide_stability",
                                "token": "USDQ",
                                "amount": float(max_borrowable),
                                "expected_apy": 5.0   # Typical stability pool APR
                            }
                        ],
                        "expected_outcome": f"Earn approximately 5% APR by providing {float(max_borrowable):.2f} USDQ to the stability pool",
                        "risk_level": 2  # Lower risk
                    })
        
        return strategies