from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import (
    Holding,
    StressTest,
)


DEFAULT_SCENARIOS = [
    {
        "name": "Mild Correction",
        "shock": Decimal("-5"),
    },
    {
        "name": "Market Correction",
        "shock": Decimal("-10"),
    },
    {
        "name": "Bear Market",
        "shock": Decimal("-20"),
    },
    {
        "name": "Severe Market Crash",
        "shock": Decimal("-30"),
    },
]


def calculate_stress_tests(
    db: Session,
    portfolio_id: int,
    user_id: int | None = None,
):
    holdings = (
        db.query(Holding)
        .filter(
            Holding.portfolio_id == portfolio_id
        )
        .all()
    )

    if not holdings:
        return {
            "portfolio_id": portfolio_id,
            "scenarios": [],
        }

    total_value = sum(
        (
            Decimal(str(h.market_value or 0))
            for h in holdings
        ),
        Decimal("0"),
    )

    if total_value <= 0:
        return {
            "portfolio_id": portfolio_id,
            "scenarios": [],
        }

    scenarios = []

    for scenario in DEFAULT_SCENARIOS:

        shock = scenario["shock"]

        estimated_loss = (
            total_value
            * abs(shock)
            / Decimal("100")
        )

        stressed_value = (
            total_value - estimated_loss
        )

        loss_percent = (
            estimated_loss
            / total_value
        ) * Decimal("100")

        stress_result = {
            "scenario_name": scenario["name"],
            "market_shock_percent": shock,
            "portfolio_value": total_value,
            "estimated_loss": estimated_loss,
            "estimated_loss_percent": loss_percent,
            "stressed_portfolio_value": stressed_value,
        }

        scenarios.append(stress_result)

        # Save result
        stress_record = StressTest(
            portfolio_id=portfolio_id,
            scenario_name=scenario["name"],
            market_shock_percent=shock,
            estimated_loss=estimated_loss,
            estimated_loss_percent=loss_percent,
            created_by=user_id,
        )

        db.add(stress_record)

    db.commit()

    return {
        "portfolio_id": portfolio_id,
        "current_portfolio_value": total_value,
        "scenarios": scenarios,
    }


def get_stress_tests(
    db: Session,
    portfolio_id: int,
):
    rows = (
        db.query(StressTest)
        .filter(
            StressTest.portfolio_id == portfolio_id
        )
        .order_by(
            StressTest.created_at.desc()
        )
        .all()
    )

    return {
        "portfolio_id": portfolio_id,
        "scenarios": [
            {
                "id": row.id,
                "scenario_name": row.scenario_name,
                "market_shock_percent": row.market_shock_percent,
                "estimated_loss": row.estimated_loss,
                "estimated_loss_percent": row.estimated_loss_percent,
                "created_at": row.created_at,
            }
            for row in rows
        ],
    }