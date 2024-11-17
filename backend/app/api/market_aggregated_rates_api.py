from fastapi import APIRouter, Depends
import pandas as pd
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.database_settings import SessionLocal
from app.cruds.user_rate import get_distinct_user_rates, get_user_rates
from app.cruds.aggregated_market_rate import create_aggregated_rate, get_aggregated_rate

router = APIRouter()

def get_session_local():
    yield SessionLocal()


@router.get("/aggregated_and_user_rates/")
async def get_market_aggregated_and_user_rates(db: Session = Depends(get_session_local)):
    """
    Fetch market aggregated rates and user rates, and calculate potential savings.
    """
    user_rates_combinations = get_distinct_user_rates(db)
    results = []

    for expiry_date, effective_date, origin, destination, price, annual_volume in user_rates_combinations:
        # Check or calculate aggregated market rates
        aggregated_data = get_aggregated_rate(db, expiry_date, effective_date, origin, destination)
        # create and calculate aggregated data
        if not aggregated_data:
            market_query = text("""
            SELECT price, date, origin, destination
            FROM market_rates
            WHERE date < :expiry_date AND date >= :effective_date AND origin = :origin AND destination = :destination
            """)
            market_data = db.execute(
                market_query, {"expiry_date": expiry_date,"effective_date": effective_date ,"origin": origin, "destination": destination}
            ).fetchall()
            if market_data:
                market_df = pd.DataFrame(market_data, columns=["price", "date", "origin", "destination"])
                market_df["price"] = market_df["price"].astype(float)
                # Group by (date, origin, destination) and calculate aggregates
                aggregated_group = market_df.groupby(["date", "origin", "destination"]).agg(
                    min_price=("price", "min"),
                    percentile_10_price=("price", lambda x: x.quantile(0.10)),
                    median_price=("price", lambda x: x.median()),
                    percentile_90_price=("price", lambda x: x.quantile(0.90)),
                    max_price=("price", "max")
                ).reset_index()
                
                # Create a record for each aggregated group
                for _, row in aggregated_group.iterrows():
                    aggregated_values = {
                        "date": row["date"],
                        "origin": row["origin"],
                        "destination": row["destination"],
                        "min_price": row["min_price"],
                        "percentile_10_price": row["percentile_10_price"],
                        "median_price": row["median_price"],
                        "percentile_90_price": row["percentile_90_price"],
                        "max_price": row["max_price"]
                    }
                    create_aggregated_rate(db, aggregated_values)
                aggregated_data = get_aggregated_rate(db, expiry_date, effective_date, origin, destination)

            else:
                continue
        for row in aggregated_data:
            savings = {
                "potential_savings_min_price": (row.min_price - price) * annual_volume,
                "potential_savings_percentile_10_price": (row.percentile_10_price - price) * annual_volume,
                "potential_savings_median_price": (row.median_price - price) * annual_volume,
                "potential_savings_percentile_90_price": (row.percentile_90_price - price) * annual_volume,
                "potential_savings_max_price": (row.max_price - price) * annual_volume,
            }

            # Compile response entry
            results.append({
                "date": row.date,
                "origin": origin,
                "destination": destination,
                "user_price": price,
                "min_price": row.min_price,
                "percentile_10_price": row.percentile_10_price,
                "median_price": row.median_price,
                "percentile_90_price": row.percentile_90_price,
                "max_price": row.max_price,
                **savings,
            })
    return {"results": results}