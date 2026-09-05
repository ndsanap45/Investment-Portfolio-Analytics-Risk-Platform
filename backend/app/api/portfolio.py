from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.portfolio_service import (
    calculate_portfolio_holdings,
    sync_holdings
)

from app.services.risk_service import (
    calculate_risk_metrics,
    save_risk_metrics
)

router = APIRouter(
    prefix="/portfolios",
    tags=["Portfolios"]
)


@router.get("/{portfolio_id}/holdings")
def get_portfolio_holdings(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    holdings = calculate_portfolio_holdings(
        db,
        portfolio_id
    )

    if not holdings:
        raise HTTPException(
            status_code=404,
            detail="No holdings found for this portfolio"
        )

    return {
        "portfolio_id": portfolio_id,
        "holdings": holdings
    }


@router.post("/{portfolio_id}/sync-holdings")
def sync_portfolio_holdings(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    holdings = sync_holdings(
        db,
        portfolio_id
    )

    return {
        "message": "Holdings synchronized successfully",
        "portfolio_id": portfolio_id,
        "holdings": holdings
    }

@router.get("/{portfolio_id}/risk")
def get_portfolio_risk(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    return calculate_risk_metrics(
        db,
        portfolio_id
    )


@router.post("/{portfolio_id}/risk/calculate")
def calculate_and_save_risk(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    metrics = save_risk_metrics(
        db,
        portfolio_id
    )

    return {
        "message": "Risk metrics calculated successfully",
        "portfolio_id": portfolio_id,
        "metrics": metrics
    }