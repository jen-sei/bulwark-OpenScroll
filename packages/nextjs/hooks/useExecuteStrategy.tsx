"use client";

import { parseUnits } from "viem";
import { useAccount, useWriteContract } from "wagmi";
import aaveStrategyAbi from "~~/abi/aave_strategy.json";
import { STRATEGY_ADDRESS } from "~~/const";
import { Strategy } from "~~/types/strategy";

/**
 * Hook to execute simple strategy
 * @param amount Amount in USDC (as a string, e.g. "1000" for 1000 USDC)
 * @returns Object containing write function, status, and error information
 */
export const useExecuteStrategy = (amount: string, strategy: Strategy) => {
  const { address } = useAccount();
  const { writeContract, writeContractAsync, isPending, isSuccess, isError, error, data } = useWriteContract();

  console.log(strategy);

  // Convert amount to the correct format (USDC has 6 decimals)
  const parsedAmount = parseUnits(amount || "0", 6);

  const executeStrategy = () => {
    if (!address || !amount || parseFloat(amount) <= 0) return;

    console.log("executeStrategy in HOOk");

    writeContract({
      address: STRATEGY_ADDRESS,
      abi: aaveStrategyAbi,
      functionName: "executeSimpleStrategy",
      args: [parsedAmount],
    });
  };

  const executeStrategyAsync = async () => {
    if (!address || !amount || parseFloat(amount) <= 0) return;

    return writeContractAsync({
      address: STRATEGY_ADDRESS,
      abi: aaveStrategyAbi,
      functionName: "executeSimpleStrategy",
      args: [parsedAmount],
    });
  };

  return {
    executeStrategy,
    executeStrategyAsync,
    isPending,
    isSuccess,
    isError,
    error,
    txData: data,
  };
};
