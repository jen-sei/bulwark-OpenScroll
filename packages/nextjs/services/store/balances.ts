"use client";

import { useEffect } from "react";
import { formatEther, formatUnits } from "viem";
import { useAccount, useBalance, useReadContracts } from "wagmi";
import { create } from "zustand";
import { useTargetNetwork } from "~~/hooks/scaffold-eth/useTargetNetwork";
import { TokenBalances } from "~~/types/balances";

const erc20Abi = [
  {
    inputs: [{ name: "account", type: "address" }],
    name: "balanceOf",
    outputs: [{ name: "balance", type: "uint256" }],
    stateMutability: "view",
    type: "function",
  },
] as const;

const TOKEN_ADDRESSES: Record<string, Record<string, `0x${string}`>> = {
  // Scroll addresses
  534352: {
    USDC: "0x06eFdBFf2a14a7c8E15944D1F4A48F9F95F663A4" as `0x${string}`,
    SRC: "0xd29687c813D741E2F938F4aC377128810E217b1b" as `0x${string}`,
  },

  // TODO delete this
  100: {
    USDC: "0x2a22f9c3b484c3629090FeED35F17Ff8F88f76F0" as `0x${string}`,
    SRC: "0xcB444e90D8198415266c6a2724b7900fb12FC56E" as `0x${string}`,
  },
};

// Token decimals
const TOKEN_DECIMALS: Record<string, number> = {
  USDC: 6,
  ETH: 18,
  SRC: 18,
};

// Store interface
interface BalancesState {
  balances: TokenBalances;
  isLoading: boolean;
  error: string | null;
  setBalances: (balances: TokenBalances) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
}

// Create the store
export const useBalancesStore = create<BalancesState>(set => ({
  balances: {},
  isLoading: false,
  error: null,
  setBalances: balances => set({ balances }),
  setLoading: isLoading => set({ isLoading }),
  setError: error => set({ error }),
}));

export { erc20Abi, TOKEN_ADDRESSES, TOKEN_DECIMALS };
// interface BalancesState {
//   balances: TokenBalances;
//   isLoading: boolean;
//   error: string | null;
//   fetchBalances: (address: `0x${string}`) => Promise<void>;
// }

// export const useBalancesStore = create<BalancesState>(set => ({
//   balances: {},
//   isLoading: false,
//   error: null,
//   fetchBalances: async (address: `0x${string}`) => {
//     if (!address) {
//       set({ error: "No address provided", isLoading: false });
//       return;
//     }

//     set({ isLoading: true, error: null });

//     try {
//       // Use the targetNetwork from the hook
//       const { targetNetwork } = useTargetNetwork();
//       const chainId = targetNetwork.id.toString();

//       // Get token addresses for the current chain
//       const tokenAddresses = TOKEN_ADDRESSES[chainId] || {};

//       // Fetch ETH balance using wagmi hooks instead of fetch
//       const ethBalanceResult = useBalance({
//         address,
//         chainId: targetNetwork.id,
//       }).data;

//       const ethBalance = ethBalanceResult ? formatEther(ethBalanceResult.value) : "0";

//       // Prepare contract calls for ERC20 tokens
//       const contractCalls = Object.entries(tokenAddresses).map(([token, tokenAddress]) => ({
//         address: tokenAddress,
//         abi: erc20Abi,
//         functionName: "balanceOf",
//         args: [address],
//       }));

//       // Execute contract calls using wagmi directly instead of fetch
//       const tokenBalancesData = await useReadContracts({
//         contracts: contractCalls,
//       }).data;

//       // Format token balances
//       const formattedBalances: TokenBalances = { ETH: ethBalance };

//       if (tokenBalancesData) {
//         Object.keys(tokenAddresses).forEach((token, index) => {
//           const balance = tokenBalancesData[index]?.result;
//           if (balance) {
//             formattedBalances[token] = formatUnits(balance, TOKEN_DECIMALS[token] || 18);
//           } else {
//             formattedBalances[token] = "0";
//           }
//         });
//       }

//       set({
//         balances: formattedBalances,
//         isLoading: false,
//       });
//     } catch (error) {
//       console.error("Error fetching balances:", error);
//       set({
//         error: "Failed to fetch balances",
//         isLoading: false,
//       });
//     }
//   },
// }));
