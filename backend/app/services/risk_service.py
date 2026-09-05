import math
from decimal import Decimal

import numpy as np
from sqlalchemy.orm import Session

from app.models import Price, RiskMetric


TRADING_DAYS = 252
RISK_FREE_RATE = 0.06


def calculate_risk_metrics(
    db: Session,
    portfolio_id: int
):
    # ---------------------------------------
    # 1. Get portfolio holdings
    # ---------------------------------------
    from app.services.portfolio_service import (
        calculate_portfolio_holdings
    )

    holdings = calculate_portfolio_holdings(
        db,
        portfolio_id
    )

    if not holdings:
        return {
            "portfolio_id": portfolio_id,
            "message": "No holdings found"
        }

    # ---------------------------------------
    # 2. Build portfolio daily values
    # ---------------------------------------
    portfolio_prices = {}

    for holding in holdings:

        asset_id = holding["asset_id"]
        quantity = float(holding["quantity"])

        prices = (
            db.query(Price)
            .filter(Price.asset_id == asset_id)
            .order_by(Price.timestamp.asc())
            .all()
        )

        for price in prices:

            date = price.timestamp.date()

            if date not in portfolio_prices:
                portfolio_prices[date] = 0

            portfolio_prices[date] += (
                quantity * float(price.price)
            )

    if len(portfolio_prices) < 2:
        return {
            "portfolio_id": portfolio_id,
            "message": "Insufficient price history"
        }

    # ---------------------------------------
    # 3. Daily returns
    # ---------------------------------------
    dates = sorted(portfolio_prices.keys())

    values = np.array(
        [portfolio_prices[d] for d in dates],
        dtype=float
    )

    returns = np.diff(values) / values[:-1]

    if len(returns) == 0:
        return {
            "portfolio_id": portfolio_id,
            "message": "Unable to calculate returns"
        }

    # ---------------------------------------
    # 4. Volatility
    # ---------------------------------------
    daily_volatility = np.std(
        returns,
        ddof=1
    )

    annualized_volatility = (
        daily_volatility
        * math.sqrt(TRADING_DAYS)
    )

    # ---------------------------------------
    # 5. Sharpe Ratio
    # ---------------------------------------
    annualized_return = (
        np.mean(returns)
        * TRADING_DAYS
    )

    sharpe_ratio = (
        (annualized_return - RISK_FREE_RATE)
        / annualized_volatility
        if annualized_volatility > 0
        else 0
    )

    # ---------------------------------------
    # 6. Sortino Ratio
    # ---------------------------------------
    downside_returns = returns[
        returns < 0
    ]

    if len(downside_returns) > 0:

        downside_deviation = (
            np.std(
                downside_returns,
                ddof=1
            )
            * math.sqrt(TRADING_DAYS)
        )

    else:
        downside_deviation = 0

    sortino_ratio = (
        (annualized_return - RISK_FREE_RATE)
        / downside_deviation
        if downside_deviation > 0
        else 0
    )

    # ---------------------------------------
    # 7. Maximum Drawdown
    # ---------------------------------------
    running_max = np.maximum.accumulate(values)

    drawdowns = (
        values - running_max
    ) / running_max

    max_drawdown = abs(
        np.min(drawdowns)
    )

    # ---------------------------------------
    # 8. VaR 95%
    # ---------------------------------------
    var_95_percent = np.percentile(
        returns,
        5
    )

    var_99_percent = np.percentile(
        returns,
        1
    )

    current_portfolio_value = values[-1]

    var_95 = abs(
        var_95_percent
        * current_portfolio_value
    )

    var_99 = abs(
        var_99_percent
        * current_portfolio_value
    )

    # ---------------------------------------
    # 9. Expected Shortfall
    # ---------------------------------------
    tail_returns = returns[
        returns <= var_95_percent
    ]

    if len(tail_returns) > 0:

        expected_shortfall = abs(
            np.mean(tail_returns)
            * current_portfolio_value
        )

    else:
        expected_shortfall = var_99

    # ---------------------------------------
    # 10. Risk Score
    # ---------------------------------------
    risk_score = calculate_risk_score(
        annualized_volatility,
        max_drawdown,
        sharpe_ratio
    )

    return {
        "portfolio_id": portfolio_id,
        "volatility": annualized_volatility,
        "sharpe_ratio": sharpe_ratio,
        "sortino_ratio": sortino_ratio,
        "max_drawdown": max_drawdown,
        "var_95": var_95,
        "var_99": var_99,
        "expected_shortfall": expected_shortfall,
        "risk_score": risk_score
    }


def calculate_risk_score(
    volatility,
    max_drawdown,
    sharpe_ratio
):
    score = 0

    # Volatility
    if volatility > 0.30:
        score += 40
    elif volatility > 0.20:
        score += 30
    elif volatility > 0.10:
        score += 20
    else:
        score += 10

    # Drawdown
    if max_drawdown > 0.30:
        score += 30
    elif max_drawdown > 0.20:
        score += 20
    elif max_drawdown > 0.10:
        score += 10

    # Sharpe
    if sharpe_ratio < 0:
        score += 30
    elif sharpe_ratio < 1:
        score += 20
    elif sharpe_ratio < 2:
        score += 10

    return min(score, 100)


def save_risk_metrics(
    db: Session,
    portfolio_id: int
):
    from datetime import date

    metrics = calculate_risk_metrics(
        db,
        portfolio_id
    )

    if "message" in metrics:
        return metrics

    risk_metric = RiskMetric(
        portfolio_id=portfolio_id,
        calculation_date=date.today(),
        volatility=Decimal(
            str(metrics["volatility"])
        ),
        sharpe_ratio=Decimal(
            str(metrics["sharpe_ratio"])
        ),
        sortino_ratio=Decimal(
            str(metrics["sortino_ratio"])
        ),
        max_drawdown=Decimal(
            str(metrics["max_drawdown"])
        ),
        var_95=Decimal(
            str(metrics["var_95"])
        ),
        var_99=Decimal(
            str(metrics["var_99"])
        ),
        expected_shortfall=Decimal(
            str(metrics["expected_shortfall"])
        ),
        risk_score=Decimal(
            str(metrics["risk_score"])
        )
    )

    db.add(risk_metric)
    db.commit()
    db.refresh(risk_metric)

    return metrics