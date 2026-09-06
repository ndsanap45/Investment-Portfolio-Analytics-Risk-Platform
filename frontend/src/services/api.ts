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
  const token = localStorage.getItem('access_token')
  const headers = new Headers(options?.headers)

  if (token) {
    headers.set('Authorization', `Bearer ${token}`)
  }

  const response = await fetch(
    `${API_BASE_URL}${endpoint}`,
    { ...options, headers }
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

export interface Portfolio {
  id: number
  name: string
  benchmark: string
}

export interface PortfoliosResponse {
  portfolios: Portfolio[]
}

export function getPortfolios(): Promise<PortfoliosResponse> {
  return fetchApi<PortfoliosResponse>('/portfolios')
}

export function createPortfolio(
  name: string,
  benchmark: string
): Promise<Portfolio> {
  return fetchApi<Portfolio>('/portfolios', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name,
      benchmark,
    }),
  })
}

export function updatePortfolio(
  portfolioId: number,
  name: string,
  benchmark: string
): Promise<Portfolio> {
  return fetchApi<Portfolio>(
    `/portfolios/${portfolioId}`,
    {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name,
        benchmark,
      }),
    }
  )
}

export function deletePortfolio(
  portfolioId: number
): Promise<{ message: string; portfolio_id: number }> {
  return fetchApi<{
    message: string
    portfolio_id: number
  }>(`/portfolios/${portfolioId}`, {
    method: 'DELETE',
  })
}

export interface AuthUser {
  id: number
  name: string
  email: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: AuthUser
}

export function login(
  email: string,
  password: string
): Promise<AuthResponse> {
  return fetchApi<AuthResponse>('/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
}