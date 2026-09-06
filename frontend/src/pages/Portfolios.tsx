import { useEffect, useState } from 'react'
import {
  Plus,
  Pencil,
  Trash2,
  BriefcaseBusiness,
  X,
} from 'lucide-react'

import {
  getPortfolios,
  createPortfolio,
  updatePortfolio,
  deletePortfolio,
} from '../services/api'

import type { Portfolio } from '../services/api'

function Portfolios() {
  const [portfolios, setPortfolios] = useState<Portfolio[]>([])
  const [loading, setLoading] = useState(true)

  const [showModal, setShowModal] = useState(false)
  const [editingPortfolio, setEditingPortfolio] =
    useState<Portfolio | null>(null)

  const [name, setName] = useState('')
  const [benchmark, setBenchmark] = useState('NIFTY50')

  const [saving, setSaving] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function loadPortfolios() {
    try {
      setLoading(true)
      setError(null)

      const response = await getPortfolios()

      setPortfolios(response.portfolios)
    } catch (err) {
      console.error(err)
      setError('Unable to load portfolios.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadPortfolios()
  }, [])

  function openCreateModal() {
    setEditingPortfolio(null)
    setName('')
    setBenchmark('NIFTY50')
    setError(null)
    setShowModal(true)
  }

  function openEditModal(portfolio: Portfolio) {
    setEditingPortfolio(portfolio)
    setName(portfolio.name)
    setBenchmark(portfolio.benchmark)
    setError(null)
    setShowModal(true)
  }

  function closeModal() {
    if (saving) return

    setShowModal(false)
    setEditingPortfolio(null)
    setName('')
    setBenchmark('NIFTY50')
  }

  async function handleSubmit(
    event: React.FormEvent
  ) {
    event.preventDefault()

    if (!name.trim()) {
      setError('Portfolio name is required.')
      return
    }

    try {
      setSaving(true)
      setError(null)

      if (editingPortfolio) {
        await updatePortfolio(
          editingPortfolio.id,
          name,
          benchmark
        )
      } else {
        await createPortfolio(
          name,
          benchmark
        )
      }

      closeModal()
      await loadPortfolios()
    } catch (err) {
      console.error(err)

      setError(
        'Unable to save portfolio. Please try again.'
      )
    } finally {
      setSaving(false)
    }
  }

  async function handleDelete(
    portfolio: Portfolio
  ) {
    const confirmed = window.confirm(
      `Delete "${portfolio.name}"?`
    )

    if (!confirmed) return

    try {
      setError(null)

      await deletePortfolio(portfolio.id)

      await loadPortfolios()
    } catch (err) {
      console.error(err)

      setError(
        'Unable to delete portfolio.'
      )
    }
  }

  if (loading) {
    return (
      <div className="page-container">
        <div className="page-loading">
          Loading portfolios...
        </div>
      </div>
    )
  }

  return (
    <div className="page-container">

      <div className="page-header">
        <div>
          <span className="page-eyebrow">
            PORTFOLIO MANAGEMENT
          </span>

          <h1>Portfolios</h1>

          <p>
            Create and manage investment portfolios
            and their benchmark configuration.
          </p>
        </div>

        <button
          className="primary-button"
          onClick={openCreateModal}
        >
          <Plus size={18} />
          Create Portfolio
        </button>
      </div>

      {error && (
        <div className="page-error">
          {error}
        </div>
      )}

      {portfolios.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">
            <BriefcaseBusiness size={28} />
          </div>

          <h2>No portfolios yet</h2>

          <p>
            Create your first investment portfolio
            to start tracking performance and risk.
          </p>

          <button
            className="primary-button"
            onClick={openCreateModal}
          >
            <Plus size={18} />
            Create Portfolio
          </button>
        </div>
      ) : (
        <div className="portfolio-grid">

          {portfolios.map((portfolio) => (
            <div
              className="portfolio-card"
              key={portfolio.id}
            >

              <div className="portfolio-card-top">

                <div className="portfolio-icon">
                  <BriefcaseBusiness size={22} />
                </div>

                <div className="portfolio-actions">

                  <button
                    className="icon-button"
                    title="Edit portfolio"
                    onClick={() =>
                      openEditModal(portfolio)
                    }
                  >
                    <Pencil size={17} />
                  </button>

                  <button
                    className="icon-button danger"
                    title="Delete portfolio"
                    onClick={() =>
                      handleDelete(portfolio)
                    }
                  >
                    <Trash2 size={17} />
                  </button>

                </div>

              </div>

              <div className="portfolio-card-body">

                <h2>{portfolio.name}</h2>

                <div className="portfolio-meta">

                  <div>
                    <span>Portfolio ID</span>
                    <strong>
                      #{portfolio.id}
                    </strong>
                  </div>

                  <div>
                    <span>Benchmark</span>
                    <strong>
                      {portfolio.benchmark}
                    </strong>
                  </div>

                </div>

              </div>

              <div className="portfolio-card-footer">
                <span>Investment Portfolio</span>

                <span className="status-badge">
                  Active
                </span>
              </div>

            </div>
          ))}

        </div>
      )}

      {showModal && (
        <div
          className="modal-overlay"
          onMouseDown={(event) => {
            if (
              event.target === event.currentTarget
            ) {
              closeModal()
            }
          }}
        >

          <div className="modal">

            <div className="modal-header">

              <div>
                <h2>
                  {editingPortfolio
                    ? 'Edit Portfolio'
                    : 'Create Portfolio'}
                </h2>

                <p>
                  Configure your investment portfolio.
                </p>
              </div>

              <button
                className="modal-close"
                onClick={closeModal}
              >
                <X size={20} />
              </button>

            </div>

            <form
              onSubmit={handleSubmit}
              className="portfolio-form"
            >

              <div className="form-group">

                <label htmlFor="portfolio-name">
                  Portfolio Name
                </label>

                <input
                  id="portfolio-name"
                  type="text"
                  placeholder="e.g. Growth Portfolio"
                  value={name}
                  onChange={(event) =>
                    setName(event.target.value)
                  }
                  autoFocus
                />

              </div>

              <div className="form-group">

                <label htmlFor="benchmark">
                  Benchmark
                </label>

                <select
                  id="benchmark"
                  value={benchmark}
                  onChange={(event) =>
                    setBenchmark(event.target.value)
                  }
                >
                  <option value="NIFTY50">
                    NIFTY 50
                  </option>

                  <option value="SENSEX">
                    BSE SENSEX
                  </option>

                  <option value="NIFTY100">
                    NIFTY 100
                  </option>
                </select>

              </div>

              {error && (
                <div className="form-error">
                  {error}
                </div>
              )}

              <div className="modal-footer">

                <button
                  type="button"
                  className="secondary-button"
                  onClick={closeModal}
                  disabled={saving}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="primary-button"
                  disabled={saving}
                >
                  {saving
                    ? 'Saving...'
                    : editingPortfolio
                      ? 'Save Changes'
                      : 'Create Portfolio'}
                </button>

              </div>

            </form>

          </div>

        </div>
      )}

    </div>
  )
}

export default Portfolios  