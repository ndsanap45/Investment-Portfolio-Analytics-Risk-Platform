from decimal import Decimal

from sqlalchemy.orm import Session

from app.services.portfolio_service import calculate_portfolio_holdings


def calculate_portfolio_allocation(
    db: Session,
    portfolio_id: int
):
    holdings = calculate_portfolio_holdings(
        db,
        portfolio_id
    )

    if not holdings:
        return {
            "portfolio_id": portfolio_id,
            "total_value": Decimal("0"),
            "asset_allocation": [],
            "sector_allocation": [],
            "top_holdings": [],
            "concentration_risk": "LOW",
            "diversification_score": Decimal("0")
        }

    total_value = sum(
        holding["market_value"]
        for holding in holdings
    )

    if total_value <= 0:
        return {
            "portfolio_id": portfolio_id,
            "total_value": Decimal("0"),
            "asset_allocation": [],
            "sector_allocation": [],
            "top_holdings": [],
            "concentration_risk": "LOW",
            "diversification_score": Decimal("0")
        }

    # -----------------------------
    # Asset Allocation
    # -----------------------------

    asset_allocation = []

    for holding in holdings:
        allocation_percent = (
            holding["market_value"]
            / total_value
        ) * Decimal("100")

        asset_allocation.append({
            "asset_id": holding["asset_id"],
            "symbol": holding["symbol"],
            "name": holding["name"],
            "market_value": holding["market_value"],
            "allocation_percent": allocation_percent
        })

    asset_allocation.sort(
        key=lambda x: x["market_value"],
        reverse=True
    )

    # -----------------------------
    # Sector Allocation
    # -----------------------------

    sector_values = {}

    for holding in holdings:
        sector = get_sector(
            db,
            holding["asset_id"]
        )

        if not sector:
            sector = "Other"

        if sector not in sector_values:
            sector_values[sector] = Decimal("0")

        sector_values[sector] += holding["market_value"]

    sector_allocation = []

    for sector, value in sector_values.items():
        allocation_percent = (
            value / total_value
        ) * Decimal("100")

        sector_allocation.append({
            "sector": sector,
            "market_value": value,
            "allocation_percent": allocation_percent
        })

    sector_allocation.sort(
        key=lambda x: x["market_value"],
        reverse=True
    )

    # -----------------------------
    # Top Holdings
    # -----------------------------

    top_holdings = asset_allocation[:5]

    # -----------------------------
    # Concentration Risk
    # -----------------------------

    largest_holding_percent = (
        asset_allocation[0]["allocation_percent"]
        if asset_allocation
        else Decimal("0")
    )

    if largest_holding_percent > Decimal("40"):
        concentration_risk = "HIGH"
    elif largest_holding_percent > Decimal("25"):
        concentration_risk = "MEDIUM"
    else:
        concentration_risk = "LOW"

    # -----------------------------
    # Diversification Score
    # -----------------------------

    number_of_assets = len(holdings)

    if number_of_assets >= 10:
        diversification_score = Decimal("100")
    elif number_of_assets >= 7:
        diversification_score = Decimal("80")
    elif number_of_assets >= 5:
        diversification_score = Decimal("65")
    elif number_of_assets >= 3:
        diversification_score = Decimal("45")
    elif number_of_assets >= 2:
        diversification_score = Decimal("25")
    else:
        diversification_score = Decimal("10")

    # Reduce score for concentration

    if largest_holding_percent > Decimal("40"):
        diversification_score -= Decimal("30")
    elif largest_holding_percent > Decimal("25"):
        diversification_score -= Decimal("15")

    diversification_score = max(
        Decimal("0"),
        diversification_score
    )

    return {
        "portfolio_id": portfolio_id,
        "total_value": total_value,
        "asset_allocation": asset_allocation,
        "sector_allocation": sector_allocation,
        "top_holdings": top_holdings,
        "concentration_risk": concentration_risk,
        "diversification_score": diversification_score
    }


def get_sector(
    db: Session,
    asset_id: int
):
    from app.models import Asset

    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if asset:
        return asset.sector

    return None