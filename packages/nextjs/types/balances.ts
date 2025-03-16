export type TokenBalances = {
  USDC?: string;
  ETH?: string;
  SRC?: string;
  [tokenSymbol: string]: string | undefined;
};
