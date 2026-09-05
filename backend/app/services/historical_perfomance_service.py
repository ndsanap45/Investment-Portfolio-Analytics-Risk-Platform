from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import (
    Asset,
    Price,
    PortfolioPerformance,
    Transaction,
)


def calculate_historical_performance(
    db: Session,
    portfolio_id: int,
):
    transactions = (
        db.query(Transaction)
        .filter(
            Transaction.portfolio_id == portfolio_id
        )
        .order_by(
            Transaction.transaction_date.asc()
        )
        .all()
    )

    if not transactions:
        return {
            "portfolio_id": portfolio_id,
            "data": [],
        }

    # --------------------------------------------------
    # Build final portfolio quantities
    # --------------------------------------------------

    holdings = {}

    for transaction in transactions:
        asset_id = transaction.asset_id

        holdings.setdefault(
            asset_id,
            Decimal("0"),
        )

        if transaction.transaction_type.upper() == "BUY":
            holdings[asset_id] += transaction.quantity

        elif transaction.transaction_type.upper() == "SELL":
            holdings[asset_id] -= transaction.quantity

    holdings = {
        asset_id: quantity
        for asset_id, quantity in holdings.items()
        if quantity > 0
    }

    if not holdings:
        return {
            "portfolio_id": portfolio_id,
            "data": [],
        }

    asset_ids = list(holdings.keys())

    # --------------------------------------------------
    # Get portfolio asset prices
    # --------------------------------------------------

    price_rows = (
        db.query(Price)
        .filter(
            Price.asset_id.in_(asset_ids)
        )
        .order_by(
            Price.timestamp.asc()
        )
        .all()
    )

    if not price_rows:
        return {
            "portfolio_id": portfolio_id,
            "data": [],
        }

    price_map = {}

    for row in price_rows:
        price_date = row.timestamp.date()

        price_map.setdefault(
            price_date,
            {},
        )

        price_map[
            price_date
        ][row.asset_id] = Decimal(
            str(row.close_price)
        )

    # --------------------------------------------------
    # Get NIFTY50
    # --------------------------------------------------

    benchmark_asset = (
        db.query(Asset)
        .filter(
            Asset.symbol == "NIFTY50",
            Asset.asset_type == "INDEX",
        )
        .first()
    )

    if not benchmark_asset:
        return {
            "portfolio_id": portfolio_id,
            "data": [],
            "message": "NIFTY50 benchmark not found",
        }

    benchmark_rows = (
        db.query(Price)
        .filter(
            Price.asset_id == benchmark_asset.id
        )
        .order_by(
            Price.timestamp.asc()
        )
        .all()
    )

    if not benchmark_rows:
        return {
            "portfolio_id": portfolio_id,
            "data": [],
            "message": "NIFTY50 price history not found",
        }

    benchmark_prices = {}

    for row in benchmark_rows:
        benchmark_prices[
            row.timestamp.date()
        ] = Decimal(
            str(row.close_price)
        )

    # --------------------------------------------------
    # Find common dates
    # --------------------------------------------------

    common_dates = sorted(
        set(price_map.keys())
        & set(benchmark_prices.keys())
    )

    if not common_dates:
        return {
            "portfolio_id": portfolio_id,
            "data": [],
            "message": "No common dates between portfolio and benchmark",
        }

    # --------------------------------------------------
    # Calculate daily portfolio value
    # --------------------------------------------------

    portfolio_values = {}

    for current_date in common_dates:

        daily_prices = price_map.get(
            current_date,
            {},
        )

        portfolio_value = Decimal("0")

        for asset_id, quantity in holdings.items():

            price = daily_prices.get(asset_id)

            if price is None:
                continue

            portfolio_value += (
                quantity * price
            )

        if portfolio_value > 0:
            portfolio_values[
                current_date
            ] = portfolio_value

    if len(portfolio_values) < 2:
        return {
            "portfolio_id": portfolio_id,
            "data": [],
            "message": "Insufficient portfolio history",
        }

    valid_dates = sorted(
        portfolio_values.keys()
    )

    # --------------------------------------------------
    # Normalize NIFTY50
    # --------------------------------------------------

    first_date = valid_dates[0]

    initial_portfolio_value = (
        portfolio_values[first_date]
    )

    initial_benchmark_price = (
        benchmark_prices[first_date]
    )

    if initial_benchmark_price <= 0:
        return {
            "portfolio_id": portfolio_id,
            "data": [],
            "message": "Invalid benchmark price",
        }

    # --------------------------------------------------
    # Build performance series
    # --------------------------------------------------

    results = []

    previous_portfolio_value = None
    previous_benchmark_value = None

    for current_date in valid_dates:

        portfolio_value = (
            portfolio_values[current_date]
        )

        benchmark_price = (
            benchmark_prices[current_date]
        )

        benchmark_value = (
            initial_portfolio_value
            * benchmark_price
            / initial_benchmark_price
        )

        if previous_portfolio_value is None:

            portfolio_return = Decimal("0")
            benchmark_return = Decimal("0")

        else:

            portfolio_return = (
                portfolio_value
                / previous_portfolio_value
            ) - Decimal("1")

            benchmark_return = (
                benchmark_value
                / previous_benchmark_value
            ) - Decimal("1")

        excess_return = (
            portfolio_return
            - benchmark_return
        )

        results.append({
            "date": current_date,
            "portfolio_value": portfolio_value,
            "benchmark_value": benchmark_value,
            "portfolio_return": portfolio_return,
            "benchmark_return": benchmark_return,
            "excess_return": excess_return,
        })

        previous_portfolio_value = (
            portfolio_value
        )

        previous_benchmark_value = (
            benchmark_value
        )

    # --------------------------------------------------
    # Save performance history
    # --------------------------------------------------

    db.query(
        PortfolioPerformance
    ).filter(
        PortfolioPerformance.portfolio_id
        == portfolio_id
    ).delete(
        synchronize_session=False
    )

    for item in results:

        performance = PortfolioPerformance(
            portfolio_id=portfolio_id,
            date=item["date"],
            portfolio_return=item[
                "portfolio_return"
            ],
            benchmark_return=item[
                "benchmark_return"
            ],
            excess_return=item[
                "excess_return"
            ],
            portfolio_value=item[
                "portfolio_value"
            ],
            benchmark_value=item[
                "benchmark_value"
            ],
        )

        db.add(performance)

    db.commit()

    return {
        "portfolio_id": portfolio_id,
        "start_date": valid_dates[0],
        "end_date": valid_dates[-1],
        "data": results,
    }