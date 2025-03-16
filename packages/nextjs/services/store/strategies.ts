import { create } from "zustand";
import { TokenBalances } from "~~/types/balances";
import { Strategy } from "~~/types/strategy";

interface StrategiesState {
  strategies: Strategy[];
  setStrategies: (strategies: Strategy[]) => void;
  generateStrategies: (address: string, balances: TokenBalances) => Promise<boolean>;
}

export const useStrategiesStore = create<StrategiesState>(set => ({
  strategies: [],

  setStrategies: (strategies: Strategy[]) => {
    console.log("Setting strategies:", strategies);
    set({ strategies });
  },

  generateStrategies: async (address, balances) => {
    try {
      const response = await fetch("https://bulwark-scroll.onrender.com/api/generate-strategies", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          address: address,
          balances: balances,
        }),
      });

      if (!response.ok) {
        throw new Error("Failed to generate strategies");
      }

      const data = await response.json();
      set({ strategies: data });
      return true;
    } catch (error) {
      console.error("Error generating strategies:", error);
      return false;
    }
  },
}));
