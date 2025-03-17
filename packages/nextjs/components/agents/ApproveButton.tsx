"use client";

import { useEffect, useState } from "react";
import { STRATEGY_ADDRESS } from "~~/const";
import { useApprove } from "~~/hooks/useApprove";

interface ApproveButtonProps {
  tokenAddress: string;
  amount: string;
  decimals?: number;
  onSuccess?: () => void;
  onError?: (error: Error) => void;
}

const ApproveButton: React.FC<ApproveButtonProps> = ({ tokenAddress, amount, decimals = 6, onSuccess, onError }) => {
  const [isApproving, setIsApproving] = useState(false);
  const { approveAsync, isPending, isSuccess, isError, error } = useApprove(
    tokenAddress,
    STRATEGY_ADDRESS,
    amount,
    decimals,
  );

  const handleApprove = async () => {
    setIsApproving(true);
    try {
      await approveAsync();
    } catch (e) {
      console.error("Approval error:", e);
    }
  };

  useEffect(() => {
    if (isSuccess) {
      setIsApproving(false);
      onSuccess?.();
    }

    if (isError && error) {
      setIsApproving(false);
      onError?.(error as Error);
    }
  }, [isSuccess, isError, error, onSuccess, onError]);

  return (
    <button
      className="w-48 bg-brand-cream text-black font-medium rounded-md p-3 hover:bg-brand-cream/80 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      onClick={handleApprove}
      disabled={isApproving || isPending}
    >
      {isApproving || isPending ? "Deploying..." : "Deploy"}
    </button>
  );
};

export default ApproveButton;
