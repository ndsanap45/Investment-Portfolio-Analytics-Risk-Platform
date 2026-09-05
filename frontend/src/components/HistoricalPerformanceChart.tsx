import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'

import type {
  HistoricalPerformanceItem,
} from '../types/portfolio'

interface Props {
  data: HistoricalPerformanceItem[]
}

function HistoricalPerformanceChart({
  data,
}: Props) {
  const chartData = data.map((item) => ({
    date: item.date,
    portfolio: Number(item.portfolio_value),
    benchmark: Number(item.benchmark_value),
  }))

  return (
    <section className="panel historical-panel">

      <div className="panel-header">
        <div>
          <h2>Portfolio vs NIFTY50</h2>

          <p>
            Historical portfolio performance compared
            with the NIFTY50 benchmark
          </p>
        </div>
      </div>

      <div className="historical-chart">

        <ResponsiveContainer
          width="100%"
          height={360}
        >
          <LineChart
            data={chartData}
            margin={{
              top: 10,
              right: 20,
              left: 10,
              bottom: 10,
            }}
          >

            <CartesianGrid
              strokeDasharray="3 3"
            />

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
                `₹${Number(value).toLocaleString(
                  'en-IN',
                  {
                    notation: 'compact',
                  }
                )}`
              }
            />

            <Tooltip
              formatter={(value) =>
                `₹${Number(value).toLocaleString(
                  'en-IN',
                  {
                    maximumFractionDigits: 0,
                  }
                )}`
              }
            />

            <Legend />

            <Line
              type="monotone"
              dataKey="portfolio"
              name="Portfolio"
              stroke="#2563eb"
              strokeWidth={3}
              dot={false}
            />

            <Line
              type="monotone"
              dataKey="benchmark"
              name="NIFTY50"
              stroke="#64748b"
              strokeWidth={2}
              dot={false}
            />

          </LineChart>
        </ResponsiveContainer>

      </div>

    </section>
  )
}

export default HistoricalPerformanceChart