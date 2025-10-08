# Data Dictionary

Synthetic SPM dataset includes:

- portfolios.csv
  - portfolio_id: string
  - avg_return: float
  - volatility: float
  - sharpe_ratio: float
  - size: float (AUM)
  - equity_weight, bond_weight, alt_weight: floats summing to ~1
  - factor_mkt, factor_size, factor_value, factor_mom: floats
  - risk_level: {low, medium, high}
