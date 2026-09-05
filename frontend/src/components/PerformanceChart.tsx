interface Props {
  invested: number
  currentValue: number
}

function PerformanceChart({
  invested,
  currentValue,
}: Props) {
  const change = currentValue - invested

  const percentage =
    invested > 0
      ? (change / invested) * 100
      : 0

  return (
    <section className="panel performance-panel">

      <div className="panel-header">
        <div>
          <h2>Portfolio Performance</h2>
          <p>Investment value vs current portfolio value</p>
        </div>

        <span
          className={
            percentage >= 0
              ? 'performance-status positive'
              : 'performance-status negative'
          }
        >
          {percentage >= 0 ? '+' : ''}
          {percentage.toFixed(2)}%
        </span>
      </div>

      <div className="performance-visual">

        <div className="performance-bar">

          <div
            className="performance-current"
            style={{
              width: `${Math.min(
                Math.max(
                  (currentValue / invested) * 50,
                  10
                ),
                100
              )}%`,
            }}
          />

        </div>

        <div className="performance-values">

          <div>
            <span>Invested</span>
            <strong>
              ₹{invested.toLocaleString('en-IN')}
            </strong>
          </div>

          <div>
            <span>Current Value</span>
            <strong>
              ₹{currentValue.toLocaleString('en-IN')}
            </strong>
          </div>

        </div>

      </div>

    </section>
  )
}

export default PerformanceChart