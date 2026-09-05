export interface Holding {
  asset_id: number
  symbol: string
  name: string
  quantity: number
  average_cost: number
  current_price: number
  market_value: number
  unrealized_pnl: number
  unrealized_pnl_percent: number
}

export interface HoldingsResponse {
  portfolio_id: number
  holdings: Holding[]
}

export interface PerformanceResponse {
  portfolio_id: number
  invested_amount: number
  current_value: number
  unrealized_pnl: number
  return_percent: number
}

export interface AllocationItem {
  asset_id: number
  symbol: string
  name: string
  market_value: number
  allocation_percent: number
}

export interface SectorAllocation {
  sector: string
  market_value: number
  allocation_percent: number
}

export interface AllocationResponse {
  portfolio_id: number
  total_value: number
  asset_allocation: AllocationItem[]
  sector_allocation: SectorAllocation[]
  top_holdings: AllocationItem[]
  concentration_risk: string
  diversification_score: number
}

export interface RiskResponse {
  portfolio_id: number
  volatility: number
  sharpe_ratio: number
  sortino_ratio: number
  max_drawdown: number
  var_95: number
  var_99: number
  expected_shortfall: number
  risk_score: number
}

export interface DrawdownItem {
  date: string
  portfolio_value: number
  peak_value: number
  drawdown_percent: number
}

export interface DrawdownResponse {
  portfolio_id: number
  current_value: number
  peak_value: number
  current_drawdown_percent: number
  maximum_drawdown_percent: number
  peak_date: string
  worst_date: string
  data: DrawdownItem[]
}

export interface StressTestScenario {
  id?: number
  scenario_name: string
  market_shock_percent: number
  portfolio_value?: number
  estimated_loss: number
  estimated_loss_percent: number
  stressed_portfolio_value?: number
  created_at?: string
}

export interface StressTestResponse {
  portfolio_id: number
  current_portfolio_value?: number
  scenarios: StressTestScenario[]
}

export interface HistoricalPerformanceItem {
  date: string
  portfolio_value: number
  benchmark_value: number
  portfolio_return: number
  benchmark_return: number
  excess_return: number
}

export interface HistoricalPerformanceResponse {
  portfolio_id: number
  start_date: string
  end_date: string
  data: HistoricalPerformanceItem[]
}