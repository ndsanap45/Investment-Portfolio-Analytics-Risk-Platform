import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

import type { DrawdownItem } from '../types/portfolio'

interface Props {
  data: DrawdownItem[]
}

function DrawdownChart({ data }: Props) {
  const chartData = data.map((item) => ({
    date: item.date,
    drawdown: Number(item.drawdown_percent),
  }))

  return (
    <section className="panel drawdown-panel">
      <div className="panel-header">
        <div>
          <h2>Portfolio Drawdown</h2>
          <p>
            Historical decline from the portfolio's
            previous peak
          </p>
        </div>
      </div>

      <div className="drawdown-chart">
        <ResponsiveContainer
          width="100%"
          height={320}
        >
          <AreaChart
            data={chartData}
            margin={{
              top: 10,
              right: 20,
              left: 10,
              bottom: 10,
            }}
          >
            <CartesianGrid strokeDasharray="3 3" />

            <XAxis
              dataKey="date"
              tickFormatter={(value) =>
                new Date(value).toLocaleDateString(
                  'en-IN',
                  {
                    month: 'short',
                    year: '2-digit',
                  }
                )
              }
            />

            <YAxis
              tickFormatter={(value) =>
                `${Number(value).toFixed(0)}%`
              }
            />

            <Tooltip
              formatter={(value) =>
                `${Number(value).toFixed(2)}%`
              }
            />

            <Area
              type="monotone"
              dataKey="drawdown"
              name="Drawdown"
              fillOpacity={0.25}
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}

export default DrawdownChart