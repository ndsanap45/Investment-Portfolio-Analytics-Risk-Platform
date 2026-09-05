import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

import type {
  SectorAllocation,
} from '../types/portfolio'

interface Props {
  data: SectorAllocation[]
}

const COLORS = [
  '#0f766e',
  '#9333ea',
  '#ca8a04',
  '#be123c',
  '#0369a1',
]

function SectorChart({ data }: Props) {
  return (
    <section className="panel chart-panel">

      <div className="panel-header">
        <div>
          <h2>Sector Exposure</h2>
          <p>Portfolio concentration by sector</p>
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
              nameKey="sector"
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
            key={item.sector}
          >
            <div>
              <span
                className="legend-dot"
                style={{
                  backgroundColor:
                    COLORS[index % COLORS.length],
                }}
              />

              {item.sector}
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

export default SectorChart