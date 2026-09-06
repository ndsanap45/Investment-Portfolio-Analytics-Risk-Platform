import {
  LayoutDashboard,
  BriefcaseBusiness,
  ArrowLeftRight,
  TrendingUp,
  ShieldAlert,
  FlaskConical,
  Bell,
  FileText,
  Settings,
} from 'lucide-react'

import { NavLink } from 'react-router-dom'

const navigation = [
  {
    name: 'Dashboard',
    path: '/dashboard',
    icon: LayoutDashboard,
  },
  {
    name: 'Portfolios',
    path: '/portfolios',
    icon: BriefcaseBusiness,
  },
  {
    name: 'Transactions',
    path: '/transactions',
    icon: ArrowLeftRight,
  },
  {
    name: 'Performance',
    path: '/performance',
    icon: TrendingUp,
  },
  {
    name: 'Risk Analytics',
    path: '/risk',
    icon: ShieldAlert,
  },
  {
    name: 'Stress Testing',
    path: '/stress-testing',
    icon: FlaskConical,
  },
  {
    name: 'Alerts',
    path: '/alerts',
    icon: Bell,
  },
  {
    name: 'Reports',
    path: '/reports',
    icon: FileText,
  },
  {
    name: 'Settings',
    path: '/settings',
    icon: Settings,
  },
]

function Sidebar() {
  return (
    <aside className="sidebar">

      <div className="sidebar-brand">

        <div className="brand-icon">
          P
        </div>

        <div>
          <h1>Portfolio</h1>
          <span>Analytics Platform</span>
        </div>

      </div>

      <nav className="sidebar-nav">

        {navigation.map((item) => {

          const Icon = item.icon

          return (
            <NavLink
              key={item.path}
              to={item.path}
              className={({ isActive }) =>
                `sidebar-link ${
                  isActive
                    ? 'sidebar-link-active'
                    : ''
                }`
              }
            >

              <Icon size={19} />

              <span>
                {item.name}
              </span>

            </NavLink>
          )
        })}

      </nav>

      <div className="sidebar-footer">

        <div className="user-avatar">
          D
        </div>

        <div>
          <strong>Demo User</strong>
          <span>Investor</span>
        </div>

      </div>

    </aside>
  )
}

export default Sidebar