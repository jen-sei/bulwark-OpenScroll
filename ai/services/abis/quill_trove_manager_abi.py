# ai/services/abis/quill_trove_manager_abi.py

TROVE_MANAGER_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "_borrowerOperationsAddress", "type": "address"},
            {"internalType": "address", "name": "_activePoolAddress", "type": "address"},
            {"internalType": "address", "name": "_defaultPoolAddress", "type": "address"},
            {"internalType": "address", "name": "_stabilityPoolAddress", "type": "address"},
            {"internalType": "address", "name": "_gasPoolAddress", "type": "address"},
            {"internalType": "address", "name": "_collSurplusPoolAddress", "type": "address"},
            {"internalType": "address", "name": "_sortedTrovesAddress", "type": "address"},
            {"internalType": "address", "name": "_usdqToken", "type": "address"},
            {"internalType": "address", "name": "_collTokenAddress", "type": "address"}
        ],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_borrower", "type": "address"}
        ],
        "name": "getTroveDebt",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_borrower", "type": "address"}
        ],
        "name": "getTroveColl",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_borrower", "type": "address"}
        ],
        "name": "getTroveInterestRateSimple",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_borrower", "type": "address"}
        ],
        "name": "getTroveStatus",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_borrower", "type": "address"}
        ],
        "name": "containsTrove",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getTroveOwnersCount",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getUSDQGasCompensation",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getMCR",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]