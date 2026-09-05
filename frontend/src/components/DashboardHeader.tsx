import { RefreshCw } from 'lucide-react'

interface Props {
  onRefresh: () => void
  loading: boolean
}

function DashboardHeader({ onRefresh, loading }: Props) {
  return (
    <header className="dashboard-header">
      <div>
        <div className="eyebrow">INVESTMENT ANALYTICS</div>

        <h1>Portfolio Dashboard</h1>

        <p>
          Real-time portfolio performance and risk analytics
        </p>
      </div>

      <button
        className="refresh-button"
        onClick={onRefresh}
        disabled={loading}
      >
        <RefreshCw
          size={17}
          className={loading ? 'spin' : ''}
        />

        {loading ? 'Refreshing...' : 'Refresh Data'}
      </button>
    </header>
  )
}

export default DashboardHeader