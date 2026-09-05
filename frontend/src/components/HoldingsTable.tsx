import type { Holding } from '../types/portfolio'

interface Props {
  holdings: Holding[]
}

function formatCurrency(value: number) {
  return `₹${value.toLocaleString('en-IN', {
    maximumFractionDigits: 2,
  })}`
}

function HoldingsTable({ holdings }: Props) {
  return (
    <section className="panel">

      <div className="panel-header">
        <div>
          <h2>Portfolio Holdings</h2>
          <p>Current positions and unrealized performance</p>
        </div>

        <span className="count-badge">
          {holdings.length} Assets
        </span>
      </div>

      <div className="table-wrapper">

        <table>

          <thead>
            <tr>
              <th>Asset</th>
              <th>Quantity</th>
              <th>Avg. Cost</th>
              <th>Current Price</th>
              <th>Market Value</th>
              <th>P&L</th>
              <th>Return</th>
            </tr>
          </thead>

          <tbody>

            {holdings.map((holding) => {

              const positive =
                holding.unrealized_pnl >= 0

              return (
                <tr key={holding.asset_id}>

                  <td>
                    <div className="asset-cell">
                      <div className="asset-avatar">
                        {holding.symbol.substring(0, 2)}
                      </div>

                      <div>
                        <strong>
                          {holding.symbol}
                        </strong>

                        <small>
                          {holding.name}
                        </small>
                      </div>
                    </div>
                  </td>

                  <td>
                    {holding.quantity}
                  </td>

                  <td>
                    {formatCurrency(
                      holding.average_cost
                    )}
                  </td>

                  <td>
                    {formatCurrency(
                      holding.current_price
                    )}
                  </td>

                  <td>
                    <strong>
                      {formatCurrency(
                        holding.market_value
                      )}
                    </strong>
                  </td>

                  <td
                    className={
                      positive
                        ? 'positive'
                        : 'negative'
                    }
                  >
                    {positive ? '+' : ''}
                    {formatCurrency(
                      holding.unrealized_pnl
                    )}
                  </td>

                  <td>
                    <span
                      className={
                        positive
                          ? 'pnl-badge positive-bg'
                          : 'pnl-badge negative-bg'
                      }
                    >
                      {positive ? '+' : ''}
                      {holding.unrealized_pnl_percent.toFixed(2)}%
                    </span>
                  </td>

                </tr>
              )
            })}

          </tbody>

        </table>

      </div>

    </section>
  )
}

export default HoldingsTable