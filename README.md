# Sales Dashboard

A data analysis dashboard built with **Python**, **Pandas**, **Matplotlib**, and **Streamlit**.

## Project Structure

```
sales_dashboard/
├── app.py            # Streamlit app — entry point
├── analysis.py       # Pandas data processing & KPI calculations
├── charts.py         # Matplotlib chart generators
├── requirements.txt  # Python dependencies
└── data/
    └── sales.csv     # Sample sales dataset (120 orders, 2024)
```

## Features

- **KPI cards** — Total Revenue, Orders, Avg Order Value, Top Category (with period-over-period deltas)
- **Monthly Revenue** — bar chart with trend line overlay
- **Revenue by Category** — donut chart
- **Revenue by Region** — horizontal bar chart
- **Quarterly Revenue** — bar chart
- **Top Products** — table with orders, units sold, revenue
- **Sidebar filters** — filter by Quarter, Category, Region
- **Raw Data Explorer** — view and download filtered CSV

## Setup

### 1. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the app

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

## Using Your Own Data

Replace `data/sales.csv` with your own CSV. Make sure it contains these columns:

| Column       | Type     | Example          |
|--------------|----------|------------------|
| `order_id`   | int      | 1001             |
| `date`       | date     | 2024-01-03       |
| `product`    | string   | Wireless Earbuds |
| `category`   | string   | Electronics      |
| `quantity`   | int      | 2                |
| `unit_price` | float    | 60.0             |
| `revenue`    | float    | 120.0            |
| `region`     | string   | North            |
| `status`     | string   | completed        |

## Extending the Project

Ideas for next steps:
- Add a **date range picker** in the sidebar
- Connect to a **SQLite or PostgreSQL** database instead of CSV
- Add **forecasting** with `statsmodels` or `prophet`
- Deploy to **Streamlit Community Cloud** (free)
- Add **user authentication** with `streamlit-authenticator`
