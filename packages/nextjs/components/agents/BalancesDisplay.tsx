"use client";

import { useBalances } from "~~/hooks/useBalances";

const formattedAmount = (amount: string | undefined) => {
  if (!amount) return "0.00";
  return parseFloat(amount).toFixed(2);
};

const BalancesDisplay = () => {
  const { balances, isLoading, error } = useBalances();

  if (isLoading) {
    return (
      <div className="border border-brand-cream rounded-xl p-2 px-4 md:p-4 border-opacity-20 bg-brand-background font-inter">
        <h2 className="text-xl font-medium mb-2">Your Balance</h2>
        <div className="animate-pulse flex flex-col md:flex-row gap-2 items-center justify-center">
          <div className="h-20 bg-neutral-800 rounded w-3/4 md:w-1/4 mb-2"></div>
          <div className="h-20 bg-neutral-800 rounded w-3/4 md:w-1/4 mb-2"></div>
          <div className="h-20 bg-neutral-800 rounded w-3/4 md:w-1/4 mb-2"></div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="border border-brand-cream rounded-xl p-2 px-4 md:p-4 border-opacity-20 bg-brand-background font-inter">
        <h2 className="text-xl font-medium mb-2">Your Balance</h2>
        <p className="text-red-500">Error loading balances: {error}</p>
      </div>
    );
  }

  return (
    <div className="border border-brand-cream rounded-xl p-2 px-4 md:p-4 border-opacity-20 bg-brand-background font-inter">
      <h2 className="text-xl font-medium mb-4">Your Balance</h2>
      <div className=" flex flex-col md:flex-row gap-2 items-center justify-center">
        {Object.entries(balances).map(([token, amount]) => (
          <div key={token} className="bg-neutral-800 rounded-lg p-3 flex flex-col items-center w-3/4 md:w-1/4 ">
            <span className="text-brand-orange-accent font-medium">{token}</span>
            <span className="text-xl font-bold text-brand-cream">{formattedAmount(amount)}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default BalancesDisplay;
