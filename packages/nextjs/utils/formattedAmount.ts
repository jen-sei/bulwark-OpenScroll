export const formattedAmount = (amount: string | undefined | number) => {
  if (!amount) return "0";

  const numAmount = typeof amount === "number" ? amount : parseFloat(amount.toString()) || 0;

  const withDecimals = numAmount.toFixed(6);
  return withDecimals.replace(/\.?0+$/, "");
};
