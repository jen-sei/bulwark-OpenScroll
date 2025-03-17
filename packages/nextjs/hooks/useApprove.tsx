"use client";

import { parseUnits } from "viem";
import { useAccount, useWriteContract } from "wagmi";
import erc20Abi from "~~/abi/erc20.json";

/**
 * Hook to approve ERC20 token spending
 * @param tokenAddress Address of the ERC20 token
 * @param spenderAddress Address to approve for spending
 * @param amount Amount to approve (as a string)
 * @param decimals Token decimals (defaults to 6 for USDC)
 * @returns Object containing approve function and status information
 */
export const useApprove = (tokenAddress: string, spenderAddress: string, amount: string, decimals = 6) => {
  const { address } = useAccount();
  const { writeContract, writeContractAsync, isPending, isSuccess, isError, error, data } = useWriteContract();

  // Convert amount to the correct format with proper decimals
  const parsedAmount = parseUnits(amount || "0", decimals);

  const approve = () => {
    if (!address || !tokenAddress || !spenderAddress || !amount || parseFloat(amount) <= 0) return;

    writeContract({
      address: tokenAddress as `0x${string}`,
      abi: erc20Abi,
      functionName: "approve",
      args: [spenderAddress as `0x${string}`, parsedAmount],
    });
  };

  const approveAsync = async () => {
    if (!address || !tokenAddress || !spenderAddress || !amount || parseFloat(amount) <= 0) return;

    return writeContractAsync({
      address: tokenAddress as `0x${string}`,
      abi: erc20Abi,
      functionName: "approve",
      args: [spenderAddress as `0x${string}`, parsedAmount],
    });
  };

  return {
    approve,
    approveAsync,
    isPending,
    isSuccess,
    isError,
    error,
    txData: data,
  };
};
