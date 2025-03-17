"use client";

import { useEffect, useState } from "react";
import { STRATEGY_ADDRESS, TOKEN_ADDRESSES } from "~~/const";
import { useTargetNetwork } from "~~/hooks/scaffold-eth/useTargetNetwork";
import { useApprove } from "~~/hooks/useApprove";
import { useExecuteStrategy } from "~~/hooks/useExecuteStrategy";
import { Strategy } from "~~/types/strategy";

interface ExecuteStrategyButtonProps {
  strategy: Strategy;
  amount: string;
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

const ExecuteStrategyButton: React.FC<ExecuteStrategyButtonProps> = ({ amount, onSuccess, onError, strategy }) => {
  const [isExecuting, setIsExecuting] = useState(false);
  const [currentStep, setCurrentStep] = useState<"idle" | "approving" | "executing" | "success">("idle");
  const { targetNetwork } = useTargetNetwork();

  // Get USDC token address for current chain
  const chainId = targetNetwork.id.toString();
  const usdcAddress = TOKEN_ADDRESSES[chainId]?.USDC || "";

  // Hooks for approve and execute
  const {
    approveAsync,
    isPending: isApprovePending,
    isSuccess: isApproveSuccess,
    isError: isApproveError,
    error: approveError,
  } = useApprove(usdcAddress, STRATEGY_ADDRESS, amount);

  const {
    executeStrategyAsync,
    isPending: isExecutePending,
    isSuccess: isExecuteSuccess,
    isError: isExecuteError,
    error: executeError,
  } = useExecuteStrategy(amount, strategy);

  const handleExecute = async () => {
    try {
      setIsExecuting(true);

      // Step 1: Approve tokens
      setCurrentStep("approving");
      console.log("Approving tokens...");
      const approveTx = await approveAsync();
      console.log("Approval tx hash:", approveTx);

      console.log("Approving tokens... done");

      // Step 2: Execute strategy (only if approval was successful)
      setCurrentStep("executing");
      console.log("Executing strategy...");
      const executeTx = await executeStrategyAsync();
      console.log("Strategy execution tx hash:", executeTx);

      console.log("Strategy execution complete");
      setCurrentStep("success");
    } catch (e) {
      console.error("Transaction failed:", e);
      onError?.(e as Error);
    } finally {
      setIsExecuting(false);
    }
  };

  // Handle state changes from hooks
  useEffect(() => {
    // Handle approval errors
    if (isApproveError && approveError && currentStep === "approving") {
      setIsExecuting(false);
      setCurrentStep("idle");
      onError?.(approveError as Error);
    }

    // Handle execution errors
    if (isExecuteError && executeError && currentStep === "executing") {
      setIsExecuting(false);
      setCurrentStep("idle");
      onError?.(executeError as Error);
    }

    // Handle success
    if (isExecuteSuccess && currentStep === "executing") {
      setIsExecuting(false);
      setCurrentStep("idle");
      onSuccess?.();
    }
  }, [
    isApproveSuccess,
    isApproveError,
    approveError,
    isExecuteSuccess,
    isExecuteError,
    executeError,
    currentStep,
    onSuccess,
    onError,
  ]);

  console.log("isApproveSuccess", isApproveSuccess);

  // Determine button text based on current state
  const getButtonText = () => {
    if (isExecuting) {
      if (currentStep === "approving") return "Approving...";
      if (currentStep === "executing") return "Deploying...";
      if (currentStep === "success") return "Success!";
      return "Processing...";
    }
    return "Deploy";
  };

  return (
    <button
      className="w-48 bg-[#fff9e8] text-black font-medium rounded-md p-3 hover:bg-[#fff0c4] transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      onClick={handleExecute}
      disabled={isExecuting || isApprovePending || isExecutePending}
    >
      {getButtonText()}
    </button>
  );
};

export default ExecuteStrategyButton;
