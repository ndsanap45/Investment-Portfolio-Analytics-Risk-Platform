from decimal import Decimal

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models import (
    Transaction,
    Price,
    PortfolioPerformance
)


def calculate_portfolio_performance(
    db: Session,
    portfolio_id: int
):
    # --------------------------------
    # 1. Get all BUY/SELL transactions
    # --------------------------------
    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.portfolio_id == portfolio_id
        )
        .order_by(Transaction.transaction_date.asc())
        .all()
    )

    if not transactions:
        return {
            "portfolio_id": portfolio_id,
            "invested_amount": Decimal("0"),
            "current_value": Decimal("0"),
            "unrealized_pnl": Decimal("0"),
            "return_percent": Decimal("0")
        }

    # --------------------------------
    # 2. Calculate invested amount
    # --------------------------------
    invested_amount = Decimal("0")

    for transaction in transactions:

        transaction_value = (
            transaction.quantity * transaction.price
        )

        fees = transaction.fees or Decimal("0")

        if transaction.transaction_type.upper() == "BUY":
            invested_amount += transaction_value + fees

        elif transaction.transaction_type.upper() == "SELL":
            invested_amount -= transaction_value - fees

    # --------------------------------
    # 3. Calculate current portfolio value
    # --------------------------------
    current_value = Decimal("0")

    holdings = {}

    for transaction in transactions:

        asset_id = transaction.asset_id

        if asset_id not in holdings:
            holdings[asset_id] = Decimal("0")

        if transaction.transaction_type.upper() == "BUY":
            holdings[asset_id] += transaction.quantity

        elif transaction.transaction_type.upper() == "SELL":
            holdings[asset_id] -= transaction.quantity

    for asset_id, quantity in holdings.items():

        if quantity <= 0:
            continue

        latest_price = (
            db.query(Price)
            .filter(
                Price.asset_id == asset_id
            )
            .order_by(
                Price.timestamp.desc()
            )
            .first()
        )

        if latest_price:
            current_value += (
                quantity * latest_price.price
            )

    # --------------------------------
    # 4. P&L
    # --------------------------------
    unrealized_pnl = (
        current_value - invested_amount
    )

    # --------------------------------
    # 5. Return %
    # --------------------------------
    if invested_amount > 0:
        return_percent = (
            unrealized_pnl
            / invested_amount
        ) * Decimal("100")
    else:
        return_percent = Decimal("0")

    return {
        "portfolio_id": portfolio_id,
        "invested_amount": invested_amount,
        "current_value": current_value,
        "unrealized_pnl": unrealized_pnl,
        "return_percent": return_percent
    }