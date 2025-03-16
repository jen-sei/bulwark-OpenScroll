// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

interface IAavePool {
    function supply(
        address asset,
        uint256 amount,
        address onBehalfOf,
        uint16 referralCode
    ) external;
    function borrow(
        address asset,
        uint256 amount,
        uint256 interestRateMode,
        uint16 referralCode,
        address onBehalfOf
    ) external;
    function withdraw(
        address asset,
        uint256 amount,
        address to
    ) external returns (uint256);
    function repay(
        address asset,
        uint256 amount,
        uint256 interestRateMode,
        address onBehalfOf
    ) external returns (uint256);
    function setUserUseReserveAsCollateral(
        address asset,
        bool useAsCollateral
    ) external;
}

interface IAmbientRouter {
    function swapExactTokensForTokens(
        uint amountIn,
        uint amountOutMin,
        address[] calldata path,
        address to,
        uint deadline
    ) external returns (uint[] memory amounts);
}

contract StrategyExecutor is Ownable {
    // AAVE Pool address on Scroll
    IAavePool public aavePool =
        IAavePool(0x11fCfe756c05AD438e312a7fd934381537D3cFfe);

    // Ambient Router address (to be replaced with actual Ambient Router address)
    address public ambientRouter;

    // Protocol identifiers
    uint8 constant AAVE = 1;
    uint8 constant AMBIENT = 2;

    // Action identifiers
    uint8 constant SUPPLY = 1;
    uint8 constant BORROW = 2;
    uint8 constant WITHDRAW = 3;
    uint8 constant REPAY = 4;
    uint8 constant SWAP = 5;
    uint8 constant SET_COLLATERAL = 6;

    // Token addresses on Scroll
    mapping(string => address) public tokenAddresses;

    constructor(address _ambientRouter) {
        ambientRouter = _ambientRouter;

        // Set up token addresses with actual Scroll addresses
        tokenAddresses["USDC"] = 0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4;
        tokenAddresses["ETH"] = 0x5300000000000000000000000000000000000004; // WETH
        tokenAddresses["SRC"] = 0xd29687c813D741E2F938F4aC377128810E217b1b;
    }

    // Structure defining a step in the strategy
    struct StrategyStep {
        uint8 protocol; // Which protocol to use (AAVE, AMBIENT)
        uint8 action; // Which action to perform (SUPPLY, BORROW, SWAP, etc.)
        string tokenIn; // Input token symbol
        uint256 amount; // Amount to use
        string tokenOut; // Output token symbol (for swaps)
        uint256 slippage; // Slippage tolerance in basis points (e.g., 50 = 0.5%)
        bool useAsCollateral; // For SET_COLLATERAL action
    }

    // Execute a multi-step strategy
    function executeStrategy(StrategyStep[] calldata steps) external {
        for (uint i = 0; i < steps.length; i++) {
            StrategyStep memory step = steps[i];

            if (step.protocol == AAVE) {
                executeAaveStep(step);
            } else if (step.protocol == AMBIENT) {
                executeAmbientStep(step);
            }
        }
    }

    // Execute a step on AAVE
    function executeAaveStep(StrategyStep memory step) internal {
        address token = tokenAddresses[step.tokenIn];

        // Approve token if needed
        if (step.action == SUPPLY || step.action == REPAY) {
            IERC20(token).approve(address(aavePool), step.amount);
        }

        if (step.action == SUPPLY) {
            aavePool.supply(token, step.amount, msg.sender, 0);
        } else if (step.action == BORROW) {
            aavePool.borrow(token, step.amount, 2, 0, msg.sender); // Always use variable rate (2)
        } else if (step.action == WITHDRAW) {
            aavePool.withdraw(token, step.amount, msg.sender);
        } else if (step.action == REPAY) {
            aavePool.repay(token, step.amount, 2, msg.sender); // Always use variable rate (2)
        } else if (step.action == SET_COLLATERAL) {
            aavePool.setUserUseReserveAsCollateral(token, step.useAsCollateral);
        }
    }

    // Execute a step on Ambient
    function executeAmbientStep(StrategyStep memory step) internal {
        if (step.action == SWAP) {
            address tokenIn = tokenAddresses[step.tokenIn];
            address tokenOut = tokenAddresses[step.tokenOut];

            // Approve token if needed
            IERC20(tokenIn).approve(ambientRouter, step.amount);

            // Calculate minimum amount out based on slippage
            uint256 amountOutMin = calculateMinAmountOut(
                step.amount,
                step.slippage
            );

            // Create path for swap
            address[] memory path = new address[](2);
            path[0] = tokenIn;
            path[1] = tokenOut;

            // Execute swap
            IAmbientRouter(ambientRouter).swapExactTokensForTokens(
                step.amount,
                amountOutMin,
                path,
                msg.sender,
                block.timestamp + 15 minutes
            );
        }
    }

    // Simple helper function to calculate minimum amount out based on slippage
    function calculateMinAmountOut(
        uint256 amountIn,
        uint256 slippageBps
    ) internal pure returns (uint256) {
        return (amountIn * (10000 - slippageBps)) / 10000;
    }

    // Function to update token addresses (admin only)
    function setTokenAddress(
        string calldata symbol,
        address tokenAddress
    ) external onlyOwner {
        tokenAddresses[symbol] = tokenAddress;
    }

    // Function to update the Ambient Router address (admin only)
    function setAmbientRouter(address _ambientRouter) external onlyOwner {
        ambientRouter = _ambientRouter;
    }

    // Function to update the AAVE Pool address (admin only)
    function setAavePool(address _aavePool) external onlyOwner {
        aavePool = IAavePool(_aavePool);
    }

    // Rescue function for any tokens accidentally sent to the contract
    function rescueTokens(address token, uint256 amount) external onlyOwner {
        IERC20(token).transfer(owner(), amount);
    }

    // Receive function to allow contract to receive ETH
    receive() external payable {}
}
