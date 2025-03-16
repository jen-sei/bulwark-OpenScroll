/**
 * Represents a single step in a strategy
 */
export interface StrategyStep {
  protocol: string;
  action: "supply" | "borrow";
  token: string;
  amount: number;
  expected_apy: number;
}

/**
 * Represents a complete investment strategy
 */
export interface Strategy {
  risk_level: number;
  steps: StrategyStep[];
  explanation: string;
  total_expected_apy: number;
  risk_factors: string[];
}
