"use client";

import { useEffect, useMemo } from "react";
import { erc20Abi, formatEther, formatUnits } from "viem";
import { useAccount, useBalance, useReadContracts } from "wagmi";
import { TOKEN_ADDRESSES, TOKEN_DECIMALS } from "~~/const";
import { useTargetNetwork } from "~~/hooks/scaffold-eth/useTargetNetwork";
import { useBalancesStore } from "~~/services/store/balances";
import { TokenBalances } from "~~/types/balances";

export function useBalances() {
  const { address } = useAccount();
  const { targetNetwork } = useTargetNetwork();
  const { balances, isLoading, error, setBalances, setLoading, setError } = useBalancesStore();

  // Get ETH balance
  const {
    data: ethBalanceData,
    isLoading: isEthLoading,
    refetch: refetchEth,
  } = useBalance({
    address,
    chainId: targetNetwork.id,
  });

  // Get token addresses for current chain
  const chainId = targetNetwork.id.toString();

  // Memoize tokenAddresses to prevent unnecessary re-renders
  const tokenAddresses = useMemo(() => {
    return TOKEN_ADDRESSES[chainId] || {};
  }, [chainId]);

  // Prepare contract calls for ERC20 tokens
  const contractCalls = useMemo(() => {
    return Object.entries(tokenAddresses).map(([token, tokenAddress]) => ({
      address: tokenAddress,
      abi: erc20Abi,
      functionName: "balanceOf" as const,
      args: [address as `0x${string}`],
    }));
  }, [tokenAddresses, address]);

  // Get token balances
  const {
    data: tokenBalancesData,
    isLoading: isTokensLoading,
    refetch: refetchTokens,
  } = useReadContracts({
    contracts: contractCalls,
  });

  // Update balances in store when data changes
  useEffect(() => {
    if (address) {
      setLoading(isEthLoading || isTokensLoading);

      if (!isEthLoading && ethBalanceData && !isTokensLoading) {
        const formattedBalances: TokenBalances = {
          ETH: formatEther(ethBalanceData.value),
        };

        // Add token balances
        if (tokenBalancesData) {
          Object.keys(tokenAddresses).forEach((token, index) => {
            const balance = tokenBalancesData[index]?.result;
            if (balance) {
              formattedBalances[token] = formatUnits(balance, TOKEN_DECIMALS[token] || 18);
            } else {
              formattedBalances[token] = "0";
            }
          });
        }

        setBalances(formattedBalances);
        setError(null);
      }
    } else {
      // Reset balances when disconnected
      setBalances({});
    }
  }, [
    address,
    ethBalanceData,
    tokenBalancesData,
    isEthLoading,
    isTokensLoading,
    setBalances,
    setLoading,
    setError,
    tokenAddresses,
  ]);

  const refreshBalances = () => {
    if (address) {
      refetchEth();
      refetchTokens();
    }
  };

  return {
    balances,
    isLoading: isLoading || isEthLoading || isTokensLoading,
    error,
    refreshBalances,
  };
}
