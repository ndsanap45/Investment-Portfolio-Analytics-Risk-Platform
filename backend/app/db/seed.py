from datetime import datetime, timedelta
from decimal import Decimal

from app.db.database import SessionLocal
from app.models import User, Portfolio, Asset, Transaction, Price


def seed_database():
    db = SessionLocal()

    try:
        # -------------------------
        # 1. User
        # -------------------------
        user = db.query(User).filter(
            User.email == "demo@portfolio.com"
        ).first()

        if not user:
            user = User(
                name="Demo Investor",
                email="demo@portfolio.com",
                password_hash="demo-password",
                role="user",
                is_active=True
            )
            db.add(user)
            db.flush()

        # -------------------------
        # 2. Portfolio
        # -------------------------
        portfolio = db.query(Portfolio).filter(
            Portfolio.user_id == user.id,
            Portfolio.name == "Growth Portfolio"
        ).first()

        if not portfolio:
            portfolio = Portfolio(
                user_id=user.id,
                name="Growth Portfolio",
                description="Demo investment portfolio",
                base_currency="INR",
                benchmark="NIFTY50"
            )
            db.add(portfolio)
            db.flush()

        # -------------------------
        # 3. Assets
        # -------------------------
        assets_data = [
            {
                "symbol": "RELIANCE",
                "name": "Reliance Industries",
                "asset_type": "EQUITY",
                "exchange": "NSE",
                "currency": "INR",
                "sector": "Energy"
            },
            {
                "symbol": "TCS",
                "name": "Tata Consultancy Services",
                "asset_type": "EQUITY",
                "exchange": "NSE",
                "currency": "INR",
                "sector": "Information Technology"
            },
            {
                "symbol": "INFY",
                "name": "Infosys",
                "asset_type": "EQUITY",
                "exchange": "NSE",
                "currency": "INR",
                "sector": "Information Technology"
            },
            {
                "symbol": "HDFCBANK",
                "name": "HDFC Bank",
                "asset_type": "EQUITY",
                "exchange": "NSE",
                "currency": "INR",
                "sector": "Financial Services"
            },
            {
                "symbol": "ICICIBANK",
                "name": "ICICI Bank",
                "asset_type": "EQUITY",
                "exchange": "NSE",
                "currency": "INR",
                "sector": "Financial Services"
            },
        ]

        assets = {}

        for data in assets_data:
            asset = db.query(Asset).filter(
                Asset.symbol == data["symbol"],
                Asset.exchange == data["exchange"]
            ).first()

            if not asset:
                asset = Asset(**data)
                db.add(asset)
                db.flush()

            assets[data["symbol"]] = asset

        # -------------------------
        # 4. Transactions
        # -------------------------
        transactions = [
            ("RELIANCE", "BUY", 10, 2850),
            ("TCS", "BUY", 8, 3950),
            ("INFY", "BUY", 12, 1650),
            ("HDFCBANK", "BUY", 15, 1750),
            ("ICICIBANK", "BUY", 10, 1200),
        ]

        for symbol, transaction_type, quantity, price in transactions:

            existing = db.query(Transaction).filter(
                Transaction.portfolio_id == portfolio.id,
                Transaction.asset_id == assets[symbol].id
            ).first()

            if not existing:
                transaction = Transaction(
                    portfolio_id=portfolio.id,
                    asset_id=assets[symbol].id,
                    transaction_type=transaction_type,
                    quantity=Decimal(str(quantity)),
                    price=Decimal(str(price)),
                    fees=Decimal("0"),
                    transaction_date=datetime.utcnow(),
                    notes="Initial demo investment"
                )

                db.add(transaction)

        # -------------------------
        # 5. Price History
        # -------------------------
        current_prices = {
            "RELIANCE": 2920,
            "TCS": 4100,
            "INFY": 1725,
            "HDFCBANK": 1810,
            "ICICIBANK": 1275,
        }

        for symbol, current_price in current_prices.items():

            asset = assets[symbol]

            existing_price = db.query(Price).filter(
                Price.asset_id == asset.id
            ).first()

            if not existing_price:
                for days_ago in range(30, -1, -1):

                    price = current_price * (
                        1 + ((30 - days_ago) * 0.001)
                    )

                    price_record = Price(
                        asset_id=asset.id,
                        price=Decimal(str(round(price, 2))),
                        open_price=Decimal(str(round(price - 5, 2))),
                        high_price=Decimal(str(round(price + 10, 2))),
                        low_price=Decimal(str(round(price - 10, 2))),
                        close_price=Decimal(str(round(price, 2))),
                        volume=Decimal("1000000"),
                        timestamp=datetime.utcnow() - timedelta(days=days_ago)
                    )

                    db.add(price_record)

        db.commit()

        print("✅ Database seeded successfully!")
        print(f"User ID: {user.id}")
        print(f"Portfolio ID: {portfolio.id}")
        print("Assets: 5")
        print("Transactions: 5")
        print("Price history: 31 days")

    except Exception as e:
        db.rollback()
        print("❌ Seed failed:", e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_database()