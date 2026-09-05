import yfinance as yf
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models import Asset, Price


def fetch_historical_prices(
    symbol: str,
    period: str = "1y",
    interval: str = "1d"
):
    ticker_symbol = f"{symbol}.NS"

    ticker = yf.Ticker(ticker_symbol)

    history = ticker.history(
        period=period,
        interval=interval,
        auto_adjust=False
    )

    if history.empty:
        raise ValueError(
            f"No market data found for {ticker_symbol}"
        )

    return history


def sync_asset_market_data(
    db: Session,
    asset_id: int,
    period: str = "1y",
    interval: str = "1d"
):
    asset = (
        db.query(Asset)
        .filter(Asset.id == asset_id)
        .first()
    )

    if not asset:
        raise ValueError(
            f"Asset with ID {asset_id} not found"
        )

    history = fetch_historical_prices(
        asset.symbol,
        period,
        interval
    )

    records_inserted = 0

    for timestamp, row in history.iterrows():

        timestamp = timestamp.to_pydatetime()

        if timestamp.tzinfo is not None:
            timestamp = timestamp.replace(
                tzinfo=None
            )

        existing_price = (
            db.query(Price)
            .filter(
                Price.asset_id == asset.id,
                Price.timestamp == timestamp
            )
            .first()
        )

        if existing_price:
            continue

        price_record = Price(
            asset_id=asset.id,
            price=Decimal(str(row["Close"])),
            open_price=Decimal(str(row["Open"])),
            high_price=Decimal(str(row["High"])),
            low_price=Decimal(str(row["Low"])),
            close_price=Decimal(str(row["Close"])),
            volume=Decimal(str(row["Volume"]))
            if row["Volume"] is not None
            else None,
            timestamp=timestamp
        )

        db.add(price_record)

        records_inserted += 1

    db.commit()

    return {
        "asset_id": asset.id,
        "symbol": asset.symbol,
        "records_inserted": records_inserted,
        "data_source": "Yahoo Finance via yfinance"
    }


def sync_portfolio_market_data(
    db: Session,
    portfolio_id: int,
    period: str = "1y",
    interval: str = "1d"
):
    from app.models import Portfolio, Transaction

    portfolio = (
        db.query(Portfolio)
        .filter(Portfolio.id == portfolio_id)
        .first()
    )

    if not portfolio:
        raise ValueError(
            f"Portfolio with ID {portfolio_id} not found"
        )

    asset_ids = (
        db.query(Transaction.asset_id)
        .filter(
            Transaction.portfolio_id == portfolio_id
        )
        .distinct()
        .all()
    )

    results = []

    for (asset_id,) in asset_ids:
        try:
            result = sync_asset_market_data(
                db=db,
                asset_id=asset_id,
                period=period,
                interval=interval
            )

            results.append({
                **result,
                "status": "success"
            })

        except Exception as e:
            results.append({
                "asset_id": asset_id,
                "status": "failed",
                "error": str(e)
            })

    return {
        "portfolio_id": portfolio_id,
        "results": results
    }