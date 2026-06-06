import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import pandas as pd


# ── Shared style ──────────────────────────────────────────────────────────────
COLORS = {
    "blue":   "#185FA5",
    "teal":   "#1D9E75",
    "amber":  "#BA7517",
    "coral":  "#D85A30",
    "pink":   "#D4537E",
    "gray":   "#888780",
}

PALETTE = list(COLORS.values())

def _style_axes(ax, grid_axis="y"):
    """Apply clean, minimal styling to an Axes object."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#E0DFDB")
    ax.spines["bottom"].set_color("#E0DFDB")
    ax.tick_params(colors="#888780", labelsize=10)
    if grid_axis:
        ax.grid(axis=grid_axis, color="#E0DFDB", linewidth=0.6, linestyle="--")
        ax.set_axisbelow(True)


# ── Chart functions ───────────────────────────────────────────────────────────

def monthly_revenue_bar(monthly: pd.DataFrame) -> plt.Figure:
    """Bar chart of monthly revenue with a trend line overlay."""
    fig, ax = plt.subplots(figsize=(10, 4))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    x = range(len(monthly))
    bars = ax.bar(
        x,
        monthly["revenue"],
        color=COLORS["blue"],
        alpha=0.85,
        width=0.65,
        zorder=3,
    )

    # trend line
    ax.plot(
        x,
        monthly["revenue"],
        color=COLORS["teal"],
        linewidth=2,
        marker="o",
        markersize=5,
        zorder=4,
        label="Trend",
    )

    ax.set_xticks(list(x))
    ax.set_xticklabels(monthly["month_label"], rotation=0)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}K"))
    ax.set_title("Monthly Revenue", fontsize=13, fontweight="bold", pad=12, loc="left")
    _style_axes(ax)
    plt.tight_layout()
    return fig


def category_donut(cat_series: pd.Series) -> plt.Figure:
    """Donut chart for revenue by category."""
    fig, ax = plt.subplots(figsize=(5, 4))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    wedges, texts, autotexts = ax.pie(
        cat_series.values,
        labels=cat_series.index,
        autopct="%1.0f%%",
        startangle=90,
        colors=PALETTE,
        wedgeprops={"width": 0.55, "edgecolor": "white", "linewidth": 2},
        pctdistance=0.75,
    )
    for t in texts:
        t.set_fontsize(10)
        t.set_color("#5F5E5A")
    for at in autotexts:
        at.set_fontsize(9)
        at.set_fontweight("bold")
        at.set_color("white")

    ax.set_title("Revenue by Category", fontsize=13, fontweight="bold", pad=12, loc="left")
    plt.tight_layout()
    return fig


def region_bar(region_series: pd.Series) -> plt.Figure:
    """Horizontal bar chart for revenue by region."""
    fig, ax = plt.subplots(figsize=(5, 3.5))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    bars = ax.barh(
        region_series.index,
        region_series.values,
        color=[COLORS["blue"], COLORS["teal"], COLORS["amber"], COLORS["coral"]],
        height=0.55,
        zorder=3,
    )
    ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}K"))
    ax.set_title("Revenue by Region", fontsize=13, fontweight="bold", pad=12, loc="left")
    ax.invert_yaxis()
    _style_axes(ax, grid_axis="x")
    plt.tight_layout()
    return fig


def quarterly_grouped_bar(quarterly: pd.DataFrame) -> plt.Figure:
    """Bar chart of quarterly revenue totals."""
    fig, ax = plt.subplots(figsize=(6, 3.5))
    fig.patch.set_alpha(0)
    ax.set_facecolor("none")

    x = range(len(quarterly))
    ax.bar(x, quarterly["total_revenue"], color=COLORS["teal"], width=0.5, zorder=3)
    ax.set_xticks(list(x))
    ax.set_xticklabels(quarterly["quarter"], rotation=10, ha="right")
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"${v/1000:.0f}K"))
    ax.set_title("Quarterly Revenue", fontsize=13, fontweight="bold", pad=12, loc="left")
    _style_axes(ax)
    plt.tight_layout()
    return fig
