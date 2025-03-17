"use client";

import { create } from "zustand";
import { TokenBalances } from "~~/types/balances";

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
