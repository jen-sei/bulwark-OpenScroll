import { TokenBalances } from "~~/types/balances";

/**
 * Checks if all token balances are zero
 * @param balances The token balances object
 * @returns true if all balances are zero, false otherwise
 */
const areAllBalancesZero = (balances: TokenBalances): boolean => {
  if (!balances || Object.keys(balances).length === 0) {
    return true;
  }

  return Object.values(balances).every(balance => {
    // Convert to number and check if zero or very close to zero (for floating point precision)
    const numBalance = parseFloat(balance || "0");
    return numBalance === 0 || numBalance < 0.000001;
  });
};

export default areAllBalancesZero;
