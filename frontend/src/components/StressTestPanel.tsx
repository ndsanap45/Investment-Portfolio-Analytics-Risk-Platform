import type {
  StressTestScenario,
} from '../types/portfolio'

interface Props {
  scenarios: StressTestScenario[]
}

function StressTestPanel({ scenarios }: Props) {
  return (
    <section className="panel stress-panel">
      <div className="panel-header">
        <div>
          <h2>Stress Testing</h2>
          <p>
            Estimated portfolio impact under market shock
            scenarios
          </p>
        </div>
      </div>

      <div className="stress-grid">
        {scenarios.map((scenario) => (
          <div
            className="stress-card"
            key={scenario.scenario_name}
          >
            <div className="stress-card-top">
              <span>
                {scenario.scenario_name}
              </span>

              <strong>
                {Number(
                  scenario.market_shock_percent
                ).toFixed(0)}
                %
              </strong>
            </div>

            <div className="stress-loss">
              -₹
              {Number(
                scenario.estimated_loss
              ).toLocaleString('en-IN', {
                maximumFractionDigits: 0,
              })}
            </div>

            <div className="stress-meta">
              Estimated Portfolio Loss
            </div>

            {scenario.stressed_portfolio_value !==
              undefined && (
              <div className="stress-value">
                Portfolio after shock: ₹
                {Number(
                  scenario.stressed_portfolio_value
                ).toLocaleString('en-IN', {
                  maximumFractionDigits: 0,
                })}
              </div>
            )}
          </div>
        ))}
      </div>
    </section>
  )
}

export default StressTestPanel