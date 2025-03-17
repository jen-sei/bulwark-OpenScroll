# ai/services/abis/quill_borrower_operations_abi.py

QUILL_BORROWER_OPERATIONS_ABI = [
    {
        "inputs": [
            {"internalType": "address", "name": "_troveManagerAddress", "type": "address"},
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
            {"internalType": "uint256", "name": "_maxFeePercentage", "type": "uint256"},
            {"internalType": "uint256", "name": "_USDQAmount", "type": "uint256"},
            {"internalType": "uint256", "name": "_interestRate", "type": "uint256"},
            {"internalType": "address", "name": "_upperHint", "type": "address"},
            {"internalType": "address", "name": "_lowerHint", "type": "address"}
        ],
        "name": "openTrove",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_maxFeePercentage", "type": "uint256"},
            {"internalType": "uint256", "name": "_collateralAdd", "type": "uint256"},
            {"internalType": "uint256", "name": "_USDQChange", "type": "uint256"},
            {"internalType": "bool", "name": "_isDebtIncrease", "type": "bool"},
            {"internalType": "uint256", "name": "_interestRate", "type": "uint256"},
            {"internalType": "address", "name": "_upperHint", "type": "address"},
            {"internalType": "address", "name": "_lowerHint", "type": "address"}
        ],
        "name": "adjustTrove",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_USDQAmount", "type": "uint256"},
            {"internalType": "address", "name": "_upperHint", "type": "address"},
            {"internalType": "address", "name": "_lowerHint", "type": "address"}
        ],
        "name": "closeTrove",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "_USDQAmount", "type": "uint256"}
        ],
        "name": "repayUSDQ",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getCollateralToken",
        "outputs": [{"internalType": "contract IERC20", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "getUSDQToken",
        "outputs": [{"internalType": "contract IUSDQToken", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "BORROWING_FEE_FLOOR",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "MAX_BORROWING_FEE",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    }
]