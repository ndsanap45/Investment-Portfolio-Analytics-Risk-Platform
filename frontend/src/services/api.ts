import type {
  HoldingsResponse,
  PerformanceResponse,
  AllocationResponse,
  RiskResponse,
  HistoricalPerformanceResponse,
  DrawdownResponse,
  StressTestResponse,
} from '../types/portfolio'

const API_BASE_URL = 'http://127.0.0.1:8000'

async function fetchApi<T>(
  endpoint: string,
  options?: RequestInit
): Promise<T> {
  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    options
  )

  if (!response.ok) {
    throw new Error(
      `API request failed: ${response.status}`
    )
  }

  return response.json()
}

/* =========================
   Holdings
========================= */

export function getHoldings(
  portfolioId: number
): Promise<HoldingsResponse> {
  return fetchApi<HoldingsResponse>(
    `/portfolios/${portfolioId}/holdings`
  )
}

/* =========================
   Performance
========================= */

export function getPerformance(
  portfolioId: number
): Promise<PerformanceResponse> {
  return fetchApi<PerformanceResponse>(
    `/portfolios/${portfolioId}/performance`
  )
}

/* =========================
   Allocation
========================= */

export function getAllocation(
  portfolioId: number
): Promise<AllocationResponse> {
  return fetchApi<AllocationResponse>(
    `/portfolios/${portfolioId}/allocation`
  )
}

/* =========================
   Risk
========================= */

export function getRisk(
  portfolioId: number
): Promise<RiskResponse> {
  return fetchApi<RiskResponse>(
    `/portfolios/${portfolioId}/risk`
  )
}

/* =========================
   Historical Performance
========================= */

export function getHistoricalPerformance(
  portfolioId: number
): Promise<HistoricalPerformanceResponse> {
  return fetchApi<HistoricalPerformanceResponse>(
    `/portfolios/${portfolioId}/historical-performance`
  )
}

/* =========================
   Drawdown
========================= */

export function getDrawdown(
  portfolioId: number
): Promise<DrawdownResponse> {
  return fetchApi<DrawdownResponse>(
    `/portfolios/${portfolioId}/drawdown`
  )
}

/* =========================
   Stress Testing
========================= */

export function runStressTest(
  portfolioId: number
): Promise<StressTestResponse> {
  return fetchApi<StressTestResponse>(
    `/portfolios/${portfolioId}/stress-test`,
    {
      method: 'POST',
    }
  )
}