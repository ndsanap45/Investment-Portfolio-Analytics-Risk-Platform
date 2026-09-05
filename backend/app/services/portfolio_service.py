from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Asset, Holding, Price, Transaction


def calculate_portfolio_holdings(
    db: Session,
    portfolio_id: int
):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.portfolio_id == portfolio_id)
        .all()
    )

    holdings = {}

    # --------------------------------
    # 1. Calculate quantity & cost
    # --------------------------------
    for transaction in transactions:

        asset_id = transaction.asset_id

        if asset_id not in holdings:
            holdings[asset_id] = {
                "quantity": Decimal("0"),
                "total_cost": Decimal("0")
            }

        if transaction.transaction_type.upper() == "BUY":

            holdings[asset_id]["quantity"] += transaction.quantity

            holdings[asset_id]["total_cost"] += (
                transaction.quantity * transaction.price
                + (transaction.fees or Decimal("0"))
            )

        elif transaction.transaction_type.upper() == "SELL":

            current_quantity = holdings[asset_id]["quantity"]

            if current_quantity > 0:

                average_cost = (
                    holdings[asset_id]["total_cost"]
                    / current_quantity
                )

                holdings[asset_id]["quantity"] -= transaction.quantity

                holdings[asset_id]["total_cost"] -= (
                    transaction.quantity * average_cost
                )

    # --------------------------------
    # 2. Calculate current market value
    # --------------------------------
    result = []

    for asset_id, data in holdings.items():

        quantity = data["quantity"]
        total_cost = data["total_cost"]

        if quantity <= 0:
            continue

        average_cost = total_cost / quantity

        # Latest price
        latest_price = (
            db.query(Price)
            .filter(Price.asset_id == asset_id)
            .order_by(Price.timestamp.desc())
            .first()
        )

        current_price = (
            latest_price.price
            if latest_price
            else Decimal("0")
        )

        market_value = quantity * current_price

        unrealized_pnl = market_value - total_cost

        unrealized_pnl_percent = (
            (unrealized_pnl / total_cost) * Decimal("100")
            if total_cost > 0
            else Decimal("0")
        )

        asset = (
            db.query(Asset)
            .filter(Asset.id == asset_id)
            .first()
        )

        result.append({
            "asset_id": asset_id,
            "symbol": asset.symbol,
            "name": asset.name,
            "quantity": quantity,
            "average_cost": average_cost,
            "current_price": current_price,
            "market_value": market_value,
            "unrealized_pnl": unrealized_pnl,
            "unrealized_pnl_percent": unrealized_pnl_percent
        })

    return result


def sync_holdings(
    db: Session,
    portfolio_id: int
):
    calculated_holdings = calculate_portfolio_holdings(
        db,
        portfolio_id
    )

    for data in calculated_holdings:

        holding = (
            db.query(Holding)
            .filter(
                Holding.portfolio_id == portfolio_id,
                Holding.asset_id == data["asset_id"]
            )
            .first()
        )

        if not holding:

            holding = Holding(
                portfolio_id=portfolio_id,
                asset_id=data["asset_id"]
            )

            db.add(holding)

        holding.quantity = data["quantity"]
        holding.average_cost = data["average_cost"]
        holding.current_price = data["current_price"]
        holding.market_value = data["market_value"]
        holding.unrealized_pnl = data["unrealized_pnl"]
        holding.unrealized_pnl_percent = (
            data["unrealized_pnl_percent"]
        )

    db.commit()

    return calculated_holdings