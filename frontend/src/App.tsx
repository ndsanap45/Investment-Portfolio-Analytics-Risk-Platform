import {
  Navigate,
  Route,
  Routes,
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

function App() {
  return (
    <Routes>

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
        element={<Layout />}
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