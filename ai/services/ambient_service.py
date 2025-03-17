# ai/services/ambient_service.py
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
from .abis.croc_swap_router_abi import CROC_SWAP_ROUTER_ABI
from .abis.croc_query_abi import CROC_QUERY_ABI
from .abis.croc_impact_abi import CROC_IMPACT_ABI

class AmbientService:
    """Service for interacting with Ambient (CrocSwap) protocol on Scroll network"""
    
    # Scroll network constants with actual values
    SCROLL_RPC_URL = os.getenv("WEB3_PROVIDER_URI", "https://rpc.scroll.io/")
    
    # Ambient contract addresses on Scroll
    CROC_SWAP_DEX = "0xaaaaAAAACB71BF2C8CaE522EA5fa455571A74106"
    CROC_SWAP_ROUTER = "0xfB5f26851E03449A0403Ca945eBB4201415fd1fc"
    CROC_QUERY = "0x62223e90605845Cf5CC6DAE6E0de4CDA130d6DDf"
    CROC_IMPACT = "0xc2c301759B5e0C385a38e678014868A33E2F3ae3"
    
    # Token addresses on Scroll
    TOKENS = {
        "ETH": "0x5300000000000000000000000000000000000004",  # WETH on Scroll
        "USDC": "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4",
        "SRC": "0xd29687c813D741E2F938F4aC377128810E217b1b"
    }
    
    # Token decimals
    DECIMALS = {
        "ETH": 18,
        "USDC": 6,
        "SRC": 18
    }
    
    # Default pool index for Ambient
    DEFAULT_POOL_IDX = 420
    
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
                self.router = self.w3.eth.contract(
                    address=self.w3.to_checksum_address(self.CROC_SWAP_ROUTER),
                    abi=CROC_SWAP_ROUTER_ABI
                )
                
                self.query = self.w3.eth.contract(
                    address=self.w3.to_checksum_address(self.CROC_QUERY),
                    abi=CROC_QUERY_ABI
                )
                
                self.impact = self.w3.eth.contract(
                    address=self.w3.to_checksum_address(self.CROC_IMPACT),
                    abi=CROC_IMPACT_ABI
                )
                
                print("Ambient contracts initialized successfully")
            except Exception as e:
                print(f"Error initializing Ambient contracts: {e}")
                self.w3 = None

    def safely_call_contract(self, contract_method, fallback_value=None, *args, **kwargs):
        """Safely call a contract method with fallback value on error"""
        try:
            return contract_method(*args, **kwargs)
        except Exception as e:
            print(f"Error calling contract method {contract_method.__name__ if hasattr(contract_method, '__name__') else 'unknown'}: {e}")
            return fallback_value

    def get_token_pair(self, token1: str, token2: str) -> (str, str, bool):
        """
        Returns the base and quote tokens in the correct order.
        In Ambient, the base token must always be the token with the lower address.
        
        Returns:
            (base_token, quote_token, is_reversed)
        """
        token1_addr = self.TOKENS.get(token1)
        token2_addr = self.TOKENS.get(token2)
        
        if not token1_addr or not token2_addr:
            raise ValueError(f"Unknown token: {token1 if not token1_addr else token2}")
        
        if int(token1_addr, 16) < int(token2_addr, 16):
            return token1_addr, token2_addr, False
        else:
            return token2_addr, token1_addr, True

    def get_pool_price(self, token1: str, token2: str) -> Decimal:
        """Get the current price between two tokens from Ambient"""
        if not self.w3:
            # Fallback prices if we can't connect
            if (token1 == "ETH" and token2 == "USDC") or (token1 == "USDC" and token2 == "ETH"):
                return Decimal("2000.0")  # ETH/USDC price
            elif (token1 == "ETH" and token2 == "SRC") or (token1 == "SRC" and token2 == "ETH"):
                return Decimal("0.005")  # SRC/ETH price
            elif (token1 == "USDC" and token2 == "SRC") or (token1 == "SRC" and token2 == "USDC"):
                return Decimal("0.01")  # SRC/USDC price
            return Decimal("1.0")
            
        try:
            # Get the base and quote tokens in correct order
            base_addr, quote_addr, is_reversed = self.get_token_pair(token1, token2)
            
            # Query the price from the contract
            raw_price = self.safely_call_contract(
                self.query.functions.queryPrice(
                    base_addr, 
                    quote_addr, 
                    self.DEFAULT_POOL_IDX
                ).call,
                0
            )
            
            # Convert the Q64.64 fixed point representation to a decimal
            # In Ambient, prices are represented as square roots, so we need to square it
            price_sqrt = Decimal(raw_price) / Decimal(2**64)
            price = price_sqrt * price_sqrt
            
            # If the tokens were reversed from the input order, invert the price
            if is_reversed:
                # Check if price is non-zero before inverting
                if price == 0:
                    return Decimal("0")
                price = Decimal("1") / price
                
            return price
        except Exception as e:
            print(f"Error getting pool price: {e}")
            # Return fallback prices
            if (token1 == "ETH" and token2 == "USDC") or (token1 == "USDC" and token2 == "ETH"):
                return Decimal("2000.0")  # ETH/USDC price
            elif (token1 == "ETH" and token2 == "SRC") or (token1 == "SRC" and token2 == "ETH"):
                return Decimal("0.005")  # SRC/ETH price
            elif (token1 == "USDC" and token2 == "SRC") or (token1 == "SRC" and token2 == "USDC"):
                return Decimal("0.01")  # SRC/USDC price
            return Decimal("1.0")

    def calculate_swap_impact(self, from_token: str, to_token: str, amount: Decimal) -> Dict[str, Any]:
        """
        Calculate the impact of swapping a certain amount of tokens.
        
        Args:
            from_token: Token to swap from
            to_token: Token to swap to
            amount: Amount of from_token to swap
            
        Returns:
            Dictionary with swap details including output amount and price impact
        """
        if not self.w3:
            # Return fallback values
            return {
                "input_amount": float(amount),
                "output_amount": float(amount) * float(self.get_pool_price(from_token, to_token)),
                "price_impact": 0.01,  # 1% fallback slippage
                "from_token": from_token,
                "to_token": to_token
            }
            
        try:
            # Get the base and quote tokens in correct order
            base_addr, quote_addr, is_reversed = self.get_token_pair(from_token, to_token)
            
            # Convert amount to the correct unit based on token decimals
            amount_in_wei = int(amount * (10 ** self.DECIMALS.get(from_token, 18)))
            
            # Determine if this is a buy or sell
            # In Ambient:
            # - isBuy=true means pay base, receive quote
            # - isBuy=false means pay quote, receive base
            is_buy = False
            in_base_qty = True
            
            if is_reversed:
                # If tokens are reversed, we need to adjust buy/sell parameters
                if from_token == base_addr:
                    is_buy = False  # Sell base for quote
                    in_base_qty = True  # Input is base
                else:
                    is_buy = True  # Buy base with quote
                    in_base_qty = False  # Input is quote
            else:
                if from_token == base_addr:
                    is_buy = True  # Buy quote with base
                    in_base_qty = True  # Input is base
                else:
                    is_buy = False  # Sell quote for base
                    in_base_qty = False  # Input is quote
            
            # Set a reasonable limit price (very high/low to ensure the swap completes)
            limit_price = 2**128 - 1 if is_buy else 1
            
            # Calculate impact using the CrocImpact contract
            result = self.safely_call_contract(
                self.impact.functions.calcImpact(
                    base_addr,
                    quote_addr,
                    self.DEFAULT_POOL_IDX,
                    is_buy,
                    in_base_qty,
                    amount_in_wei,
                    0,  # tip
                    limit_price
                ).call,
                (0, 0, 0)  # fallback
            )
            
            base_flow, quote_flow, final_price = result
            
            # Determine the output amount (negative flow means received by user)
            if from_token == base_addr:
                output_amount = abs(quote_flow) / (10 ** self.DECIMALS.get(to_token, 18))
            else:
                output_amount = abs(base_flow) / (10 ** self.DECIMALS.get(to_token, 18))
                
            # Calculate price impact
            current_price = self.get_pool_price(from_token, to_token)
            final_sqrt_price = Decimal(final_price) / Decimal(2**64)
            final_actual_price = final_sqrt_price * final_sqrt_price
            
            if is_reversed:
                if final_actual_price == 0:
                    price_impact = 0
                else:
                    final_actual_price = Decimal("1") / final_actual_price
                    
            price_impact = abs((final_actual_price - current_price) / current_price)
            
            return {
                "input_amount": float(amount),
                "output_amount": float(output_amount),
                "price_impact": float(price_impact),
                "from_token": from_token,
                "to_token": to_token
            }
            
        except Exception as e:
            print(f"Error calculating swap impact: {e}")
            # Return fallback values
            price = self.get_pool_price(from_token, to_token)
            return {
                "input_amount": float(amount),
                "output_amount": float(amount) * float(price),
                "price_impact": 0.01,  # 1% fallback slippage
                "from_token": from_token,
                "to_token": to_token
            }

    def get_pool_liquidity(self, token1: str, token2: str) -> Dict[str, Any]:
        """Get liquidity information for a pool"""
        if not self.w3:
            # Return fallback values
            return {
                "total_liquidity": 1000000,
                "price": float(self.get_pool_price(token1, token2))
            }
            
        try:
            # Get the base and quote tokens in correct order
            base_addr, quote_addr, is_reversed = self.get_token_pair(token1, token2)
            
            # Query the liquidity from the contract
            liquidity = self.safely_call_contract(
                self.query.functions.queryLiquidity(
                    base_addr,
                    quote_addr,
                    self.DEFAULT_POOL_IDX
                ).call,
                0
            )
            
            # Get the current price
            price = self.get_pool_price(token1, token2)
            
            return {
                "total_liquidity": liquidity,
                "price": float(price)
            }
            
        except Exception as e:
            print(f"Error getting pool liquidity: {e}")
            # Return fallback values
            return {
                "total_liquidity": 1000000,
                "price": float(self.get_pool_price(token1, token2))
            }

    def get_market_data(self) -> Dict[str, Any]:
        """Get comprehensive market data from Ambient on Scroll"""
        market_data = {
            "dex": "Ambient",
            "pools": {},
            "swap_fees": 0.003  # 0.3% standard fee
        }
        
        # Get data for key token pairs
        pairs = [
            ("ETH", "USDC"),
            ("ETH", "SRC"),
            ("USDC", "SRC")
        ]
        
        for token1, token2 in pairs:
            try:
                price = self.get_pool_price(token1, token2)
                liquidity_data = self.get_pool_liquidity(token1, token2)
                
                pair_key = f"{token1}-{token2}"
                market_data["pools"][pair_key] = {
                    "price": float(price),
                    "total_liquidity": float(liquidity_data["total_liquidity"]),
                    "volume_24h": 1000000,  # Placeholder - would need external API for this
                    "fee": 0.003,  # 0.3% standard fee
                }
            except Exception as e:
                print(f"Error getting market data for {token1}-{token2}: {e}")
                # Add fallback data
                pair_key = f"{token1}-{token2}"
                fallback_price = 1.0
                if token1 == "ETH" and token2 == "USDC":
                    fallback_price = 2000.0
                elif token1 == "ETH" and token2 == "SRC":
                    fallback_price = 0.005
                elif token1 == "USDC" and token2 == "SRC":
                    fallback_price = 0.01
                    
                market_data["pools"][pair_key] = {
                    "price": fallback_price,
                    "total_liquidity": 1000000,
                    "volume_24h": 1000000,
                    "fee": 0.003
                }
        
        return market_data