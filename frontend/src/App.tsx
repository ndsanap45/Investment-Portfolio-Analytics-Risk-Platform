import {
  Navigate,
  Route,
  Routes,
  useLocation,
} from 'react-router-dom'

import Layout from './components/Layout'

import Dashboard from './pages/Dashboard'
import Portfolios from './pages/Portfolios'
import Transactions from './pages/Transactions'
import Performance from './pages/Performance'
import Risk from './pages/Risk'
import StressTesting from './pages/StressTesting'
import Alerts from './pages/Alerts'
import Reports from './pages/Reports'
import Settings from './pages/Settings'
import Login from './pages/login'

function ProtectedLayout() {
  const location = useLocation()

  if (!localStorage.getItem('access_token')) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />
  }

  return <Layout />
}

function App() {
  return (
    <Routes>

      <Route path="/login" element={<Login />} />

      <Route
        path="/"
        element={
          <Navigate
            to="/dashboard"
            replace
          />
        }
      />

      <Route
        element={<ProtectedLayout />}
      >

        <Route
          path="/dashboard"
          element={<Dashboard />}
        />

        <Route
          path="/portfolios"
          element={<Portfolios />}
        />

        <Route
          path="/transactions"
          element={<Transactions />}
        />

        <Route
          path="/performance"
          element={<Performance />}
        />

        <Route
          path="/risk"
          element={<Risk />}
        />

        <Route
          path="/stress-testing"
          element={<StressTesting />}
        />

        <Route
          path="/alerts"
          element={<Alerts />}
        />

        <Route
          path="/reports"
          element={<Reports />}
        />

        <Route
          path="/settings"
          element={<Settings />}
        />

      </Route>

    </Routes>
  )
}

export default App