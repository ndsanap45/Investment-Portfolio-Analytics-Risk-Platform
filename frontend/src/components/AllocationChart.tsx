import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

import type { AllocationItem } from '../types/portfolio'

interface Props {
  data: AllocationItem[]
}

const COLORS = [
  '#2563eb',
  '#7c3aed',
  '#059669',
  '#ea580c',
  '#dc2626',
  '#0891b2',
]

function AllocationChart({ data }: Props) {
  return (
    <section className="panel chart-panel">

      <div className="panel-header">
        <div>
          <h2>Asset Allocation</h2>
          <p>Portfolio exposure by asset</p>
        </div>
      </div>

      <div className="chart-container">

        <ResponsiveContainer
          width="100%"
          height={280}
        >
          <PieChart>

            <Pie
              data={data}
              dataKey="market_value"
              nameKey="symbol"
              cx="50%"
              cy="50%"
              outerRadius={95}
              innerRadius={55}
              paddingAngle={3}
            >

              {data.map((_, index) => (
                <Cell
                  key={index}
                  fill={
                    COLORS[index % COLORS.length]
                  }
                />
              ))}

            </Pie>

            <Tooltip
              formatter={(value) =>
                `₹${Number(value).toLocaleString('en-IN')}`
              }
            />

          </PieChart>
        </ResponsiveContainer>

      </div>

      <div className="legend-list">

        {data.map((item, index) => (
          <div
            className="legend-item"
            key={item.asset_id}
          >
            <div>
              <span
                className="legend-dot"
                style={{
                  backgroundColor:
                    COLORS[index % COLORS.length],
                }}
              />

              {item.symbol}
            </div>

            <strong>
              {Number(
                item.allocation_percent
              ).toFixed(1)}
              %
            </strong>
          </div>
        ))}

      </div>

    </section>
  )
}

export default AllocationChart