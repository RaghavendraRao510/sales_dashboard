import streamlit as st
import pandas as pd

import analysis
import charts

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown(
    """
    <style>
      [data-testid="stMetricValue"] { font-size: 1.8rem; font-weight: 600; }
      [data-testid="stMetricDelta"] { font-size: 0.85rem; }
      .block-container { padding-top: 1.5rem; }
      h1 { font-size: 1.6rem !important; font-weight: 700; }
      h2 { font-size: 1.1rem !important; font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Load data ─────────────────────────────────────────────────────────────────
@st.cache_data
def get_data():
    return analysis.load_data()

df_full = get_data()

# ── Sidebar filters ───────────────────────────────────────────────────────────
st.sidebar.title("Filters")

quarters = ["All"] + sorted(df_full["quarter"].unique().tolist())
selected_q = st.sidebar.selectbox("Quarter", quarters, index=0)

categories = ["All"] + sorted(df_full["category"].unique().tolist())
selected_cat = st.sidebar.selectbox("Category", categories, index=0)

regions = ["All"] + sorted(df_full["region"].unique().tolist())
selected_region = st.sidebar.selectbox("Region", regions, index=0)

st.sidebar.markdown("---")
st.sidebar.markdown("**Data source:** `data/sales.csv`")
st.sidebar.markdown(f"**Total records:** {len(df_full):,}")

# ── Apply filters ─────────────────────────────────────────────────────────────
df = df_full.copy()
if selected_q != "All":
    df = df[df["quarter"] == selected_q]
if selected_cat != "All":
    df = df[df["category"] == selected_cat]
if selected_region != "All":
    df = df[df["region"] == selected_region]

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📊 Sales Dashboard")
st.caption("2024 · Python · Pandas · Matplotlib · Streamlit")

if len(df) == 0:
    st.warning("No data matches the current filters. Try adjusting the sidebar.")
    st.stop()

# ── KPI Metrics ───────────────────────────────────────────────────────────────
metrics = analysis.summary_metrics(df)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Revenue",
        f"${metrics['total_revenue']:,.0f}",
        delta=f"{metrics['revenue_delta']:+.1f}% vs prior",
    )
with col2:
    st.metric(
        "Total Orders",
        f"{metrics['total_orders']:,}",
        delta=f"{metrics['orders_delta']:+.1f}% vs prior",
    )
with col3:
    st.metric(
        "Avg Order Value",
        f"${metrics['avg_order_value']:.2f}",
    )
with col4:
    st.metric(
        "Top Category",
        metrics["top_category"],
        delta=f"{metrics['top_category_pct']:.0f}% of revenue",
        delta_color="off",
    )

st.markdown("---")

# ── Charts: row 1 ─────────────────────────────────────────────────────────────
monthly = analysis.monthly_revenue(df)

st.subheader("Monthly Revenue")
fig_monthly = charts.monthly_revenue_bar(monthly)
st.pyplot(fig_monthly, use_container_width=True)

st.markdown("---")

# ── Charts: row 2 ─────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    cat_series = analysis.revenue_by_category(df)
    fig_cat = charts.category_donut(cat_series)
    st.pyplot(fig_cat, use_container_width=True)

with col_right:
    region_series = analysis.revenue_by_region(df)
    fig_region = charts.region_bar(region_series)
    st.pyplot(fig_region, use_container_width=True)

st.markdown("---")

# ── Charts: row 3 — Quarterly ─────────────────────────────────────────────────
quarterly = analysis.quarterly_revenue(df)
col_q, col_table = st.columns([1, 1])

with col_q:
    fig_q = charts.quarterly_grouped_bar(quarterly)
    st.pyplot(fig_q, use_container_width=True)

with col_table:
    st.subheader("Top Products")
    top = analysis.top_products(df)
    top["revenue"] = top["revenue"].apply(lambda x: f"${x:,.0f}")
    top.columns = ["Product", "Orders", "Units Sold", "Revenue"]
    st.dataframe(top, use_container_width=True, hide_index=True)

st.markdown("---")

# ── Raw data explorer ─────────────────────────────────────────────────────────
with st.expander("🔍 Raw Data Explorer"):
    st.dataframe(
        df[["order_id", "date", "product", "category", "quantity", "unit_price", "revenue", "region"]]
        .sort_values("date", ascending=False)
        .reset_index(drop=True),
        use_container_width=True,
        height=320,
    )
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="⬇ Download filtered data as CSV",
        data=csv,
        file_name="sales_filtered.csv",
        mime="text/csv",
    )
