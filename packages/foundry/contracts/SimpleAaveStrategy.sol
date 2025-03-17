// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

// Import required interfaces for AAVE
import "./interfaces.sol";

/**
 * @title SimpleAaveStrategy
 * @dev Simple contract for executing a basic AAVE supply strategy
 */
contract SimpleAaveStrategy {
    // AAVE Pool contract address on Scroll
    address public constant AAVE_POOL =
        0x11fCfe756c05AD438e312a7fd934381537D3cFfe;

    // USDC token address on Scroll
    address public constant USDC = 0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4;

    /**
     * @dev Execute a simple lending strategy
     * @param amount Amount of USDC to lend to AAVE
     */
    function executeSimpleStrategy(uint256 amount) external {
        // Transfer USDC from sender to this contract
        IERC20(USDC).transferFrom(msg.sender, address(this), amount);

        // Approve AAVE pool to spend USDC
        IERC20(USDC).approve(AAVE_POOL, amount);

        // Supply USDC to AAVE
        IPool(AAVE_POOL).supply(
            USDC, // asset
            amount, // amount
            msg.sender, // onBehalfOf (credit goes to the sender)
            0 // referralCode
        );
    }

    /**
     * @dev Allow the contract to receive ETH
     */
    receive() external payable {}
}
