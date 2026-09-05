from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import PortfolioPerformance


def calculate_drawdown(
    db: Session,
    portfolio_id: int,
):
    performance_rows = (
        db.query(PortfolioPerformance)
        .filter(
            PortfolioPerformance.portfolio_id == portfolio_id
        )
        .order_by(
            PortfolioPerformance.date.asc()
        )
        .all()
    )

    if not performance_rows:
        return {
            "portfolio_id": portfolio_id,
            "data": [],
        }

    results = []

    peak_value = Decimal("0")
    peak_date = None

    max_drawdown = Decimal("0")
    max_drawdown_date = None
    max_drawdown_peak_date = None

    for row in performance_rows:

        portfolio_value = Decimal(
            str(row.portfolio_value)
        )

        current_date = row.date

        # Update running peak
        if portfolio_value > peak_value:
            peak_value = portfolio_value
            peak_date = current_date

        # Calculate drawdown
        if peak_value > 0:
            drawdown = (
                (portfolio_value - peak_value)
                / peak_value
            ) * Decimal("100")
        else:
            drawdown = Decimal("0")

        # Track maximum drawdown
        if drawdown < max_drawdown:
            max_drawdown = drawdown
            max_drawdown_date = current_date
            max_drawdown_peak_date = peak_date

        results.append({
            "date": current_date,
            "portfolio_value": portfolio_value,
            "peak_value": peak_value,
            "drawdown_percent": drawdown,
        })

    latest = results[-1]

    return {
        "portfolio_id": portfolio_id,

        "current_value": latest["portfolio_value"],

        "peak_value": latest["peak_value"],

        "current_drawdown_percent": latest[
            "drawdown_percent"
        ],

        "maximum_drawdown_percent": max_drawdown,

        "peak_date": max_drawdown_peak_date,

        "worst_date": max_drawdown_date,

        "data": results,
    }