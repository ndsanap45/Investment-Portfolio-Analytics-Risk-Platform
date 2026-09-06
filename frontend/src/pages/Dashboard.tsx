import { useEffect, useState } from 'react'

import DashboardHeader from '../components/DashboardHeader'
import SummaryCards from '../components/SummaryCards'
import HoldingsTable from '../components/HoldingsTable'
import AllocationChart from '../components/AllocationChart'
import SectorChart from '../components/SectorChart'
import PerformanceChart from '../components/PerformanceChart'
import RiskMetrics from '../components/RiskMetrics'
import HistoricalPerformanceChart from '../components/HistoricalPerformanceChart'
import DrawdownChart from '../components/DrawdownChart'
import StressTestPanel from '../components/StressTestPanel'

import {
  getHoldings,
  getPerformance,
  getAllocation,
  getRisk,
  getHistoricalPerformance,
  getDrawdown,
  runStressTest,
} from '../services/api'

import type {
  Holding,
  PerformanceResponse,
  AllocationResponse,
  RiskResponse,
  HistoricalPerformanceResponse,
  DrawdownResponse,
  StressTestResponse,
} from '../types/portfolio'

function Dashboard() {
  const portfolioId = 1

  const [holdings, setHoldings] =
    useState<Holding[]>([])

  const [performance, setPerformance] =
    useState<PerformanceResponse | null>(null)

  const [allocation, setAllocation] =
    useState<AllocationResponse | null>(null)

  const [risk, setRisk] =
    useState<RiskResponse | null>(null)

  const [historicalPerformance, setHistoricalPerformance] =
    useState<HistoricalPerformanceResponse | null>(null)

  const [drawdown, setDrawdown] =
    useState<DrawdownResponse | null>(null)

  const [stressTest, setStressTest] =
    useState<StressTestResponse | null>(null)

  const [loading, setLoading] =
    useState(true)

  const [error, setError] =
    useState<string | null>(null)

  async function loadDashboard() {
    try {
      setLoading(true)
      setError(null)

      const [
        holdingsData,
        performanceData,
        allocationData,
        riskData,
        historicalData,
        drawdownData,
        stressData,
      ] = await Promise.all([
        getHoldings(portfolioId),
        getPerformance(portfolioId),
        getAllocation(portfolioId),
        getRisk(portfolioId),
        getHistoricalPerformance(portfolioId),
        getDrawdown(portfolioId),
        runStressTest(portfolioId),
      ])

      setHoldings(
        holdingsData.holdings
      )

      setPerformance(
        performanceData
      )

      setAllocation(
        allocationData
      )

      setRisk(
        riskData
      )

      setHistoricalPerformance(
        historicalData
      )

      setDrawdown(
        drawdownData
      )

      setStressTest(
        stressData
      )

    } catch (err) {
      console.error(err)

      setError(
        'Unable to load portfolio data. Make sure the backend is running.'
      )

    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadDashboard()
  }, [])

  /* =========================
     Loading State
  ========================= */

  if (loading) {
    return (
      <div className="loading-screen">

        <div className="loading-spinner" />

        <h2>
          Loading Portfolio
        </h2>

        <p>
          Fetching market and risk analytics...
        </p>

      </div>
    )
  }

  /* =========================
     Error State
  ========================= */

  if (error) {
    return (
      <div className="error-screen">

        <h2>
          Something went wrong
        </h2>

        <p>
          {error}
        </p>

        <button
          className="refresh-button"
          onClick={loadDashboard}
        >
          Try Again
        </button>

      </div>
    )
  }

  /* =========================
     Dashboard
  ========================= */

  return (
    <div className="app">

      <main className="dashboard-container">

        {/* =========================
            Header
        ========================= */}

        <DashboardHeader
          onRefresh={loadDashboard}
          loading={loading}
        />

        {/* =========================
            Portfolio Summary
        ========================= */}

        {performance && (
          <SummaryCards
            invested={
              Number(
                performance.invested_amount
              )
            }

            currentValue={
              Number(
                performance.current_value
              )
            }

            pnl={
              Number(
                performance.unrealized_pnl
              )
            }

            returnPercent={
              Number(
                performance.return_percent
              )
            }
          />
        )}

        {/* =========================
            Current Performance
        ========================= */}

        {performance && (
          <PerformanceChart
            invested={
              Number(
                performance.invested_amount
              )
            }

            currentValue={
              Number(
                performance.current_value
              )
            }
          />
        )}

        {/* =========================
            Holdings
        ========================= */}

        <HoldingsTable
          holdings={holdings}
        />

        {/* =========================
            Asset & Sector Allocation
        ========================= */}

        {allocation && (
          <div className="charts-grid">

            <AllocationChart
              data={
                allocation.asset_allocation
              }
            />

            <SectorChart
              data={
                allocation.sector_allocation
              }
            />

          </div>
        )}

        {/* =========================
            Risk Metrics
        ========================= */}

        {risk && (
          <RiskMetrics
            risk={risk}
          />
        )}

        {/* =========================
            Portfolio Insights
        ========================= */}

        {allocation && (
          <section className="insight-banner">

            <div>
              <span>
                Portfolio Diversification
              </span>

              <strong>
                {Number(
                  allocation.diversification_score
                ).toFixed(0)}
                /100
              </strong>
            </div>

            <div>
              <span>
                Concentration Risk
              </span>

              <strong>
                {allocation.concentration_risk}
              </strong>
            </div>

            <div>
              <span>
                Portfolio Assets
              </span>

              <strong>
                {holdings.length}
              </strong>
            </div>

          </section>
        )}

        {/* =========================
            Historical Performance
        ========================= */}

        {historicalPerformance &&
          historicalPerformance.data.length > 0 && (
            <HistoricalPerformanceChart
              data={
                historicalPerformance.data
              }
            />
          )}

        {/* =========================
            Drawdown Analysis
        ========================= */}

        {drawdown &&
          drawdown.data.length > 0 && (
            <>

              <section className="risk-summary-grid">

                {/* Maximum Drawdown */}

                <div className="risk-summary-card">

                  <span>
                    Maximum Drawdown
                  </span>

                  <strong>
                    {Number(
                      drawdown.maximum_drawdown_percent
                    ).toFixed(2)}
                    %
                  </strong>

                </div>

                {/* Current Drawdown */}

                <div className="risk-summary-card">

                  <span>
                    Current Drawdown
                  </span>

                  <strong>
                    {Number(
                      drawdown.current_drawdown_percent
                    ).toFixed(2)}
                    %
                  </strong>

                </div>

                {/* Peak Portfolio Value */}

                <div className="risk-summary-card">

                  <span>
                    Peak Portfolio Value
                  </span>

                  <strong>
                    ₹
                    {Number(
                      drawdown.peak_value
                    ).toLocaleString(
                      'en-IN',
                      {
                        maximumFractionDigits: 0,
                      }
                    )}
                  </strong>

                </div>

                {/* Peak Date */}

                <div className="risk-summary-card">

                  <span>
                    Peak Date
                  </span>

                  <strong>
                    {drawdown.peak_date
                      ? new Date(
                          drawdown.peak_date
                        ).toLocaleDateString(
                          'en-IN'
                        )
                      : 'N/A'}
                  </strong>

                </div>

              </section>

              <DrawdownChart
                data={
                  drawdown.data
                }
              />

            </>
          )}

        {/* =========================
            Stress Testing
        ========================= */}

        {stressTest &&
          stressTest.scenarios.length > 0 && (
            <StressTestPanel
              scenarios={
                stressTest.scenarios
              }
            />
          )}

        {/* =========================
            Footer
        ========================= */}

        <footer>

        
        <span>
          •
        </span>  
          Copytright © 2026
     

        <span>
          •
        </span>

          Developed by Nagesh

        </footer>

      </main>

    </div>
  )
}

export default Dashboard