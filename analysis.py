import pandas as pd
from pathlib import Path


DATA_PATH = Path(__file__).parent / "data" / "sales.csv"


def load_data() -> pd.DataFrame:
    """Load and preprocess sales data."""
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    df["month"] = df["date"].dt.to_period("M")
    df["month_name"] = df["date"].dt.strftime("%b %Y")
    df["quarter"] = df["date"].dt.to_period("Q").astype(str)
    df["year"] = df["date"].dt.year
    return df


def summary_metrics(df: pd.DataFrame) -> dict:
    """Compute top-level KPI metrics."""
    total_revenue = df["revenue"].sum()
    total_orders = len(df)
    avg_order_value = df["revenue"].mean()
    top_category = df.groupby("category")["revenue"].sum().idxmax()
    top_category_pct = (
        df.groupby("category")["revenue"].sum().max() / total_revenue * 100
    )

    # period-over-period: compare last 6 months vs previous 6
    df_sorted = df.sort_values("date")
    midpoint = df_sorted["date"].median()
    recent = df_sorted[df_sorted["date"] >= midpoint]["revenue"].sum()
    prior = df_sorted[df_sorted["date"] < midpoint]["revenue"].sum()
    revenue_delta = ((recent - prior) / prior * 100) if prior else 0

    recent_orders = len(df_sorted[df_sorted["date"] >= midpoint])
    prior_orders = len(df_sorted[df_sorted["date"] < midpoint])
    orders_delta = ((recent_orders - prior_orders) / prior_orders * 100) if prior_orders else 0

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "avg_order_value": avg_order_value,
        "top_category": top_category,
        "top_category_pct": top_category_pct,
        "revenue_delta": revenue_delta,
        "orders_delta": orders_delta,
    }


def monthly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue and orders by month."""
    monthly = (
        df.groupby(df["date"].dt.to_period("M"))
        .agg(revenue=("revenue", "sum"), orders=("order_id", "count"))
        .reset_index()
    )
    monthly["month_label"] = monthly["date"].dt.strftime("%b")
    return monthly


def revenue_by_category(df: pd.DataFrame) -> pd.Series:
    """Revenue breakdown by product category."""
    return df.groupby("category")["revenue"].sum().sort_values(ascending=False)


def revenue_by_region(df: pd.DataFrame) -> pd.Series:
    """Revenue breakdown by region."""
    return df.groupby("region")["revenue"].sum().sort_values(ascending=False)


def top_products(df: pd.DataFrame, n: int = 5) -> pd.DataFrame:
    """Top N products by total revenue."""
    return (
        df.groupby("product")
        .agg(
            orders=("order_id", "count"),
            units_sold=("quantity", "sum"),
            revenue=("revenue", "sum"),
        )
        .sort_values("revenue", ascending=False)
        .head(n)
        .reset_index()
    )


def quarterly_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Revenue grouped by quarter."""
    return (
        df.groupby("quarter")["revenue"]
        .sum()
        .reset_index()
        .rename(columns={"revenue": "total_revenue"})
    )


def filter_by_quarter(df: pd.DataFrame, quarter: str) -> pd.DataFrame:
    """Filter dataframe to a specific quarter string like '2024Q1'."""
    if quarter == "All":
        return df
    return df[df["quarter"] == quarter]
