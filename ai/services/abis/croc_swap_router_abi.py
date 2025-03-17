# ai/services/abis/croc_swap_router_abi.py

CROC_SWAP_ROUTER_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "base", "type": "address"},
            {"internalType": "address", "name": "quote", "type": "address"},
            {"internalType": "uint256", "name": "poolIdx", "type": "uint256"},
            {"internalType": "bool", "name": "isBuy", "type": "bool"},
            {"internalType": "bool", "name": "inBaseQty", "type": "bool"},
            {"internalType": "uint128", "name": "qty", "type": "uint128"},
            {"internalType": "uint16", "name": "tip", "type": "uint16"},
            {"internalType": "uint128", "name": "limitPrice", "type": "uint128"},
            {"internalType": "uint128", "name": "minOut", "type": "uint128"},
            {"internalType": "uint8", "name": "reserveFlags", "type": "uint8"}
        ],
        "name": "swap",
        "outputs": [
            {"internalType": "int128", "name": "baseFlow", "type": "int128"},
            {"internalType": "int128", "name": "quoteFlow", "type": "int128"}
        ],
        "stateMutability": "payable",
        "type": "function"
    }
]