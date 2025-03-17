// SPDX-License-Identifier: MIT
pragma solidity ^0.8.23;

import "./interfaces.sol";

interface IWETHGateway {
    function depositETH(
        address pool,
        address onBehalfOf,
        uint16 referralCode
    ) external payable;
    function withdrawETH(address pool, uint256 amount, address to) external;
    function borrowETH(
        address pool,
        uint256 amount,
        uint256 interestRateMode,
        uint16 referralCode
    ) external;
    function repayETH(
        address pool,
        uint256 amount,
        uint256 interestRateMode,
        address onBehalfOf
    ) external payable;
}

interface ICrocSwapRouter {
    function exactInputSingle(
        address tokenIn,
        address tokenOut,
        uint24 poolIdx,
        uint256 amountIn,
        uint256 amountOutMinimum,
        uint160 priceLimit,
        address to,
        uint256 deadline
    ) external returns (uint256 amountOut);
}

interface IQuillBorrowerOperations {
    function openTrove(
        uint256 _maxFeePercentage,
        uint256 _USDQAmount,
        uint256 _interestRate,
        address _upperHint,
        address _lowerHint
    ) external payable;
}

interface IQuillStabilityPool {
    function provideToSP(uint256 _amount) external;
}

/**
 * @title StrategyExecutor
 * @dev Contract for executing multi-protocol DeFi strategies on Scroll
 */
contract StrategyExecutor {
    address public owner;

    // Protocol contracts on Scroll
    address public constant AAVE_POOL =
        0x11fCfe756c05AD438e312a7fd934381537D3cFfe;
    address public constant WETH_GATEWAY =
        0x7003E7B7186f0E6601203b99F7B8DECBfA391cf9;
    address public constant CROC_SWAP_ROUTER =
        0xfB5f26851E03449A0403Ca945eBB4201415fd1fc;

    // Quill protocol addresses on Scroll
    address public constant QUILL_ETH_BORROWER_OPS =
        0x05B229f984584589D9Af5F768eb4BfCCB3f8324F;
    address public constant QUILL_SRC_BORROWER_OPS =
        0xF02433e0f4d85216915502b800490C7172Dc23E8;
    address public constant QUILL_ETH_STABILITY_POOL =
        0x2c627886421eE62E1c51a4b4248a751089Ae57B6;
    address public constant QUILL_SRC_STABILITY_POOL =
        0xBCB64a2EFf9CD8D10f24b5Fc74031a157391A496;

    // Token addresses on Scroll
    address public constant WETH = 0x5300000000000000000000000000000000000004;
    address public constant USDC = 0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4;
    address public constant SRC = 0xd29687c813D741E2F938F4aC377128810E217b1b;
    address public constant USDQ = 0x6F2A1A886Dbf8E36C4fa9F25a517861A930fBF3A;

    // Protocol identifiers
    uint8 private constant PROTOCOL_AAVE = 1;
    uint8 private constant PROTOCOL_AMBIENT = 2;
    uint8 private constant PROTOCOL_QUILL = 3;

    // Action identifiers
    uint8 private constant ACTION_SUPPLY = 1;
    uint8 private constant ACTION_BORROW = 2;
    uint8 private constant ACTION_WITHDRAW = 3;
    uint8 private constant ACTION_REPAY = 4;
    uint8 private constant ACTION_SWAP = 5;
    uint8 private constant ACTION_ADD_LIQUIDITY = 6;
    uint8 private constant ACTION_REMOVE_LIQUIDITY = 7;
    uint8 private constant ACTION_BORROW_USDQ = 8;
    uint8 private constant ACTION_REPAY_USDQ = 9;
    uint8 private constant ACTION_PROVIDE_STABILITY = 10;

    // Default values
    uint16 private constant DEFAULT_REFERRAL_CODE = 0;
    uint256 private constant DEFAULT_INTEREST_RATE_MODE = 2; // Variable rate
    uint160 private constant MAX_PRICE_LIMIT = type(uint160).max;
    uint24 private constant DEFAULT_POOL_IDX = 420; // Default Ambient pool index
    uint256 private constant MAX_FEE_PERCENTAGE = 1000; // 1%

    struct StrategyStep {
        uint8 protocol;
        uint8 action;
        address token;
        uint256 amount;
        bytes extraData; // Additional parameters for specific actions
    }

    event StrategyExecuted(address indexed user, uint256 stepCount);
    event StepExecuted(
        uint8 protocol,
        uint8 action,
        address token,
        uint256 amount
    );
    event ExecutionFailed(uint8 protocol, uint8 action, string reason);

    modifier onlyOwner() {
        require(msg.sender == owner, "Caller is not the owner");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /**
     * @dev Execute a simple AAVE supply strategy (for testing)
     * @param asset Asset to supply
     * @param amount Amount to supply
     */
    function executeSimpleAaveSupply(address asset, uint256 amount) external {
        // Transfer tokens from sender to this contract
        IERC20(asset).transferFrom(msg.sender, address(this), amount);

        // Approve AAVE pool to spend tokens
        IERC20(asset).approve(AAVE_POOL, amount);

        // Supply tokens to AAVE
        IPool(AAVE_POOL).supply(
            asset, // asset
            amount, // amount
            msg.sender, // onBehalfOf (credit goes to the sender)
            0 // referralCode
        );

        emit StrategyExecuted(msg.sender, 1);
    }

    /**
     * @dev Execute a multi-step strategy
     * @param steps Array of strategy steps to execute
     */
    function executeStrategy(StrategyStep[] calldata steps) external payable {
        uint256 ethBalance = address(this).balance;

        for (uint256 i = 0; i < steps.length; i++) {
            StrategyStep memory step = steps[i];
            bool success = executeStep(step);

            if (!success) {
                emit ExecutionFailed(
                    step.protocol,
                    step.action,
                    "Step execution failed"
                );
                // Continue to next step instead of reverting
                continue;
            }

            emit StepExecuted(
                step.protocol,
                step.action,
                step.token,
                step.amount
            );
        }

        // Return any remaining ETH to the sender
        uint256 remainingEth = address(this).balance;
        if (remainingEth > 0 && remainingEth != ethBalance) {
            (bool sent, ) = msg.sender.call{value: remainingEth}("");
            require(sent, "Failed to send remaining ETH");
        }

        emit StrategyExecuted(msg.sender, steps.length);
    }

    function executeStep(StrategyStep memory step) internal returns (bool) {
        bool success;

        if (step.protocol == PROTOCOL_AAVE) {
            try this.executeAaveStep(step) returns (bool _success) {
                success = _success;
            } catch (bytes memory reason) {
                emit ExecutionFailed(
                    step.protocol,
                    step.action,
                    string(reason)
                );
                return false;
            }
        } else if (step.protocol == PROTOCOL_AMBIENT) {
            try this.executeAmbientStep(step) returns (bool _success) {
                success = _success;
            } catch (bytes memory reason) {
                emit ExecutionFailed(
                    step.protocol,
                    step.action,
                    string(reason)
                );
                success = false;
            }
        } else if (step.protocol == PROTOCOL_QUILL) {
            try this.executeQuillStep(step) returns (bool _success) {
                success = _success;
            } catch (bytes memory reason) {
                emit ExecutionFailed(
                    step.protocol,
                    step.action,
                    string(reason)
                );
                success = false;
            }
        } else {
            emit ExecutionFailed(
                step.protocol,
                step.action,
                "Unknown protocol"
            );
            success = false;
        }

        return success;
    }

    /**
     * @dev Execute a step on AAVE protocol
     * @param step Strategy step to execute
     * @return success Whether the step executed successfully
     */
    function executeAaveStep(StrategyStep memory step) external returns (bool) {
        // Transfer tokens from sender if needed (except for ETH)
        if (
            step.token != WETH &&
            step.action != ACTION_WITHDRAW &&
            step.action != ACTION_REPAY
        ) {
            IERC20(step.token).transferFrom(
                msg.sender,
                address(this),
                step.amount
            );
            IERC20(step.token).approve(AAVE_POOL, step.amount);
        }

        if (step.action == ACTION_SUPPLY) {
            if (step.token == WETH) {
                // For ETH, use the WETH gateway
                IWETHGateway(WETH_GATEWAY).depositETH{value: step.amount}(
                    AAVE_POOL,
                    msg.sender,
                    DEFAULT_REFERRAL_CODE
                );
            } else {
                // For ERC20 tokens
                IPool(AAVE_POOL).supply(
                    step.token,
                    step.amount,
                    msg.sender,
                    DEFAULT_REFERRAL_CODE
                );
            }
            return true;
        } else if (step.action == ACTION_BORROW) {
            if (step.token == WETH) {
                // For borrowing ETH
                IWETHGateway(WETH_GATEWAY).borrowETH(
                    AAVE_POOL,
                    step.amount,
                    DEFAULT_INTEREST_RATE_MODE,
                    DEFAULT_REFERRAL_CODE
                );
            } else {
                // For borrowing ERC20 tokens
                IPool(AAVE_POOL).borrow(
                    step.token,
                    step.amount,
                    DEFAULT_INTEREST_RATE_MODE,
                    DEFAULT_REFERRAL_CODE,
                    msg.sender
                );
            }
            return true;
        } else if (step.action == ACTION_WITHDRAW) {
            if (step.token == WETH) {
                // For withdrawing ETH
                IWETHGateway(WETH_GATEWAY).withdrawETH(
                    AAVE_POOL,
                    step.amount,
                    msg.sender
                );
            } else {
                // For withdrawing ERC20 tokens
                IPool(AAVE_POOL).withdraw(step.token, step.amount, msg.sender);
            }
            return true;
        } else if (step.action == ACTION_REPAY) {
            if (step.token == WETH) {
                // For repaying ETH
                IWETHGateway(WETH_GATEWAY).repayETH{value: step.amount}(
                    AAVE_POOL,
                    step.amount,
                    DEFAULT_INTEREST_RATE_MODE,
                    msg.sender
                );
            } else {
                // For repaying ERC20 tokens
                IPool(AAVE_POOL).repay(
                    step.token,
                    step.amount,
                    DEFAULT_INTEREST_RATE_MODE,
                    msg.sender
                );
            }
            return true;
        }

        return false; // Unknown action
    }

    /**
     * @dev Execute a step on Ambient DEX
     * @param step Strategy step to execute
     * @return success Whether the step executed successfully
     */
    function executeAmbientStep(
        StrategyStep memory step
    ) external returns (bool) {
        if (step.action == ACTION_SWAP) {
            // Parse extraData for token_to
            (address tokenTo, uint256 minAmountOut) = abi.decode(
                step.extraData,
                (address, uint256)
            );

            // Transfer tokens from sender
            IERC20(step.token).transferFrom(
                msg.sender,
                address(this),
                step.amount
            );
            IERC20(step.token).approve(CROC_SWAP_ROUTER, step.amount);

            // Execute swap
            ICrocSwapRouter(CROC_SWAP_ROUTER).exactInputSingle(
                step.token,
                tokenTo,
                DEFAULT_POOL_IDX,
                step.amount,
                minAmountOut,
                MAX_PRICE_LIMIT,
                msg.sender,
                block.timestamp + 15 minutes
            );

            return true;
        } else if (step.action == ACTION_ADD_LIQUIDITY) {
            // For the hackathon MVP, we're not implementing full liquidity provision
            // as it would require a more complex interaction with Ambient's contracts
            return false;
        } else if (step.action == ACTION_REMOVE_LIQUIDITY) {
            // For the hackathon MVP, we're not implementing liquidity removal
            return false;
        }

        return false; // Unknown action
    }

    /**
     * @dev Execute a step on Quill protocol
     * @param step Strategy step to execute
     * @return success Whether the step executed successfully
     */
    function executeQuillStep(
        StrategyStep memory step
    ) external returns (bool) {
        if (step.action == ACTION_BORROW_USDQ) {
            // Parse extraData for USDQ amount and interest rate
            (uint256 usdqAmount, uint256 interestRate) = abi.decode(
                step.extraData,
                (uint256, uint256)
            );

            address borrowerOps;
            if (step.token == WETH || step.token == address(0)) {
                borrowerOps = QUILL_ETH_BORROWER_OPS;
            } else if (step.token == SRC) {
                borrowerOps = QUILL_SRC_BORROWER_OPS;
            } else {
                return false; // Unsupported collateral
            }

            // Transfer tokens from sender if needed
            if (step.token != WETH && step.token != address(0)) {
                IERC20(step.token).transferFrom(
                    msg.sender,
                    address(this),
                    step.amount
                );
                IERC20(step.token).approve(borrowerOps, step.amount);
            }

            // For ETH, use the value parameter
            uint256 msgValue = (step.token == WETH || step.token == address(0))
                ? step.amount
                : 0;

            // Open trove and borrow USDQ
            IQuillBorrowerOperations(borrowerOps).openTrove{value: msgValue}(
                MAX_FEE_PERCENTAGE,
                usdqAmount,
                interestRate,
                address(0), // No hints for simplicity
                address(0)
            );

            // Transfer USDQ to the user
            IERC20(USDQ).transfer(msg.sender, usdqAmount);

            return true;
        } else if (step.action == ACTION_PROVIDE_STABILITY) {
            // Transfer USDQ from sender
            IERC20(USDQ).transferFrom(msg.sender, address(this), step.amount);

            // Determine which stability pool to use based on token
            address stabilityPool;
            if (step.token == WETH || step.token == address(0)) {
                stabilityPool = QUILL_ETH_STABILITY_POOL;
            } else if (step.token == SRC) {
                stabilityPool = QUILL_SRC_STABILITY_POOL;
            } else {
                return false; // Unsupported token
            }

            // Approve stability pool to spend USDQ
            IERC20(USDQ).approve(stabilityPool, step.amount);

            // Provide to stability pool
            IQuillStabilityPool(stabilityPool).provideToSP(step.amount);

            return true;
        }

        return false; // Unknown action
    }

    /**
     * @dev Update the contract owner
     * @param newOwner Address of the new owner
     */
    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "New owner is the zero address");
        owner = newOwner;
    }

    /**
     * @dev Encode extra data for Ambient swap step
     * @param tokenTo Target token to swap to
     * @param minAmountOut Minimum amount to receive (for slippage protection)
     * @return encodedData Encoded extra data
     */
    function encodeAmbientSwapData(
        address tokenTo,
        uint256 minAmountOut
    ) external pure returns (bytes memory) {
        return abi.encode(tokenTo, minAmountOut);
    }

    /**
     * @dev Encode extra data for Quill borrow step
     * @param usdqAmount Amount of USDQ to borrow
     * @param interestRate Interest rate for the loan
     * @return encodedData Encoded extra data
     */
    function encodeQuillBorrowData(
        uint256 usdqAmount,
        uint256 interestRate
    ) external pure returns (bytes memory) {
        return abi.encode(usdqAmount, interestRate);
    }

    /**
     * @dev Allow the contract to receive ETH
     */
    receive() external payable {}
}
