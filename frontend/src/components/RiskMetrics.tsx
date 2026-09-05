import {
  ShieldAlert,
  Gauge,
  TrendingDown,
  BarChart3,
} from 'lucide-react'

import type { RiskResponse } from '../types/portfolio'

interface Props {
  risk: RiskResponse
}

function RiskMetrics({ risk }: Props) {

  const riskScore = Number(risk.risk_score)

  let riskLabel = 'Low'

  if (riskScore >= 70) {
    riskLabel = 'High'
  } else if (riskScore >= 40) {
    riskLabel = 'Moderate'
  }

  return (
    <section className="panel">

      <div className="panel-header">

        <div>
          <h2>Risk Analytics</h2>
          <p>Portfolio risk and performance indicators</p>
        </div>

        <div className="risk-score">

          <span>Risk Score</span>

          <strong>
            {riskScore.toFixed(0)}
          </strong>

          <small>
            {riskLabel}
          </small>

        </div>

      </div>

      <div className="risk-grid">

        <div className="risk-card">
          <BarChart3 size={20} />

          <span>Volatility</span>

          <strong>
            {(Number(risk.volatility) * 100).toFixed(2)}%
          </strong>
        </div>

        <div className="risk-card">
          <Gauge size={20} />

          <span>Sharpe Ratio</span>

          <strong>
            {Number(risk.sharpe_ratio).toFixed(2)}
          </strong>
        </div>

        <div className="risk-card">
          <TrendingDown size={20} />

          <span>Max Drawdown</span>

          <strong>
            {(Number(risk.max_drawdown) * 100).toFixed(2)}%
          </strong>
        </div>

        <div className="risk-card">
          <ShieldAlert size={20} />

          <span>VaR 95%</span>

          <strong>
            ₹{Number(risk.var_95).toLocaleString('en-IN', {
              maximumFractionDigits: 0,
            })}
          </strong>
        </div>

        <div className="risk-card">

          <span>VaR 99%</span>

          <strong>
            ₹{Number(risk.var_99).toLocaleString('en-IN', {
              maximumFractionDigits: 0,
            })}
          </strong>

        </div>

        <div className="risk-card">

          <span>Expected Shortfall</span>

          <strong>
            ₹{Number(
              risk.expected_shortfall
            ).toLocaleString('en-IN', {
              maximumFractionDigits: 0,
            })}
          </strong>

        </div>

      </div>

    </section>
  )
}

export default RiskMetrics
