// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "forge-std/Script.sol";
import "../contracts/SimpleAaveStrategy.sol";
import "../contracts/StrategyExecutor.sol";

contract DeployBulwark is Script {
    function run() external {
        uint256 deployerPrivateKey = vm.envUint("PRIVATE_KEY");
        vm.startBroadcast(deployerPrivateKey);

        // Deploy the simple strategy contract for testing
        SimpleAaveStrategy simpleStrategy = new SimpleAaveStrategy();
        console.log("SimpleAaveStrategy deployed at:", address(simpleStrategy));

        // Deploy the full strategy executor contract
        StrategyExecutor strategyExecutor = new StrategyExecutor();
        console.log("StrategyExecutor deployed at:", address(strategyExecutor));

        vm.stopBroadcast();
    }
}
