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

from app.services.allocation_service import (
    calculate_portfolio_allocation
)

from app.services.portfolio_performance_service import (
    calculate_portfolio_performance
)

from app.services.market_data_service import (
    sync_asset_market_data,
    sync_portfolio_market_data
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

@router.get("/{portfolio_id}/performance")
def get_portfolio_performance(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    performance = calculate_portfolio_performance(
        db,
        portfolio_id
    )

    return performance


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

@router.get("/{portfolio_id}/allocation")
def get_portfolio_allocation(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    return calculate_portfolio_allocation(
        db,
        portfolio_id
    )

@router.post("/{portfolio_id}/market-data/sync")
def sync_market_data(
    portfolio_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = sync_portfolio_market_data(
            db=db,
            portfolio_id=portfolio_id,
            period="1y",
            interval="1d"
        )

        return {
            "message": "Market data synchronized successfully",
            **result
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@router.post("/{portfolio_id}/assets/{asset_id}/market-data/sync")
def sync_asset_data(
    portfolio_id: int,
    asset_id: int,
    db: Session = Depends(get_db)
):
    try:
        result = sync_asset_market_data(
            db=db,
            asset_id=asset_id,
            period="1y",
            interval="1d"
        )

        return {
            "message": "Asset market data synchronized successfully",
            **result
        }

    except ValueError as e:
        raise HTTPException(
            status_code=404,
            detail=str(e)
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )