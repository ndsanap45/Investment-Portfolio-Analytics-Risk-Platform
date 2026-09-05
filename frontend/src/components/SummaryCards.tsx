    import {
  Wallet,
  TrendingUp,
  IndianRupee,
  Activity,
} from 'lucide-react'

interface Props {
  invested: number
  currentValue: number
  pnl: number
  returnPercent: number
}

function formatCurrency(value: number) {
  return `₹${value.toLocaleString('en-IN', {
    maximumFractionDigits: 2,
  })}`
}

function SummaryCards({
  invested,
  currentValue,
  pnl,
  returnPercent,
}: Props) {
  const pnlPositive = pnl >= 0

  return (
    <section className="summary-grid">

      <div className="summary-card">
        <div className="card-icon">
          <Wallet size={20} />
        </div>

        <div>
          <span>Invested Amount</span>
          <strong>{formatCurrency(invested)}</strong>
        </div>
      </div>

      <div className="summary-card">
        <div className="card-icon">
          <IndianRupee size={20} />
        </div>

        <div>
          <span>Current Value</span>
          <strong>{formatCurrency(currentValue)}</strong>
        </div>
      </div>

      <div className="summary-card">
        <div className="card-icon">
          <TrendingUp size={20} />
        </div>

        <div>
          <span>Total P&L</span>

          <strong
            className={
              pnlPositive
                ? 'positive'
                : 'negative'
            }
          >
            {pnlPositive ? '+' : ''}
            {formatCurrency(pnl)}
          </strong>
        </div>
      </div>

      <div className="summary-card">
        <div className="card-icon">
          <Activity size={20} />
        </div>

        <div>
          <span>Total Return</span>

          <strong
            className={
              returnPercent >= 0
                ? 'positive'
                : 'negative'
            }
          >
            {returnPercent >= 0 ? '+' : ''}
            {returnPercent.toFixed(2)}%
          </strong>
        </div>
      </div>

    </section>
  )
}

export default SummaryCards