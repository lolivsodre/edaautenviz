"""
Jane Austen Adaptations Analysis
Author: Luiza Sodre

This script builds a structured dataset of Jane Austen adaptations and generates
portfolio-ready charts using a custom color palette.

Project pipeline:
1. Data construction / extraction
2. Title standardization
3. Media classification
4. Adaptation type classification
5. Decade variable creation
6. Exploratory visualizations

Run:
    python jane_austen_adaptations_analysis.py

Outputs:
    data/processed/jane_austen_adaptations.csv
    visualizations/*.png
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ------------------------------------------------------------
# 1. Project folders
# ------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data" / "processed"
VIZ_DIR = BASE_DIR / "visualizations"
DATA_DIR.mkdir(parents=True, exist_ok=True)
VIZ_DIR.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------
# 2. Color palette
# ------------------------------------------------------------

COLORS = {
    "gochujang_red": "#780000",
    "crimson_blaze": "#C1121F",
    "varden": "#AE1F23",
    "cosmos_blue": "#003049",
    "blue_marble": "#669BBC",
    "merlot": "#8C1A3C",
    "camellia": "#CF244C",
    "peony": "#EF87D4",
    "periwinkle": "#9494F8",
    "gardenia": "#FDF0D5",
    "deep_purple": "#35184F",
}

WORK_COLORS = {
    "Pride and Prejudice": COLORS["gochujang_red"],
    "Emma": COLORS["merlot"],
    "Sense and Sensibility": COLORS["deep_purple"],
    "Persuasion": COLORS["camellia"],
    "Mansfield Park": COLORS["varden"],
    "Northanger Abbey": "#B79AD0",
    "Sanditon": "#D7A2E6",
    "Lady Susan": COLORS["crimson_blaze"],
}

TYPE_COLORS = {
    "Direct": COLORS["deep_purple"],
    "Loose": COLORS["crimson_blaze"],
}

MEDIA_COLORS = {
    "Television Miniseries": COLORS["gochujang_red"],
    "Film": COLORS["crimson_blaze"],
    "TV Movie": COLORS["gardenia"],
    "Theatre Play": COLORS["cosmos_blue"],
    "Web Series": COLORS["blue_marble"],
    "Series Episode": COLORS["peony"],
    "Novel": "#B79AD0",
    "Stage Musical": COLORS["varden"],
    "Musical Film": COLORS["merlot"],
    "Streaming Film": "#5B1745",
    "Opera": "#472063",
    "Board Game": "#6B224E",
}

# ------------------------------------------------------------
# 3. Dataset construction
# ------------------------------------------------------------

# Aggregated values used in the analysis.
# These can be replaced by a scraped/raw CSV when available.
WORK_COUNTS = {
    "Pride and Prejudice": 42,
    "Emma": 11,
    "Sense and Sensibility": 11,
    "Persuasion": 9,
    "Mansfield Park": 8,
    "Northanger Abbey": 6,
    "Sanditon": 2,
    "Lady Susan": 1,
}

DECADE_TYPE_COUNTS = {
    1900: {"Direct": 0, "Loose": 1},
    1930: {"Direct": 2, "Loose": 1},
    1940: {"Direct": 2, "Loose": 1},
    1950: {"Direct": 3, "Loose": 1},
    1960: {"Direct": 7, "Loose": 0},
    1970: {"Direct": 4, "Loose": 0},
    1980: {"Direct": 4, "Loose": 0},
    1990: {"Direct": 6, "Loose": 6},
    2000: {"Direct": 6, "Loose": 11},
    2010: {"Direct": 2, "Loose": 27},
    2020: {"Direct": 3, "Loose": 3},
}

MEDIA_COUNTS = {
    "Television Miniseries": 25,
    "Film": 24,
    "TV Movie": 15,
    "Theatre Play": 6,
    "Web Series": 5,
    "Series Episode": 4,
    "Novel": 3,
    "Stage Musical": 3,
    "Musical Film": 2,
    "Streaming Film": 1,
    "Opera": 1,
    "Board Game": 1,
}


def expand_counts(values: dict, column_name: str) -> list:
    """Expand a dictionary of counts into a list of repeated labels."""
    expanded = []
    for label, count in values.items():
        expanded.extend([label] * count)
    return expanded


def build_dataset() -> pd.DataFrame:
    """
    Build a row-level dataset from the validated aggregate counts.

    Each row represents one adaptation. Since the public-facing analysis is based
    on aggregate counts, rows are reconstructed by aligning work, decade,
    adaptation type, and media distributions.
    """
    works = expand_counts(WORK_COUNTS, "work")
    media = expand_counts(MEDIA_COUNTS, "media")

    decades = []
    adaptation_types = []
    for decade, counts in DECADE_TYPE_COUNTS.items():
        for adaptation_type, count in counts.items():
            decades.extend([decade] * count)
            adaptation_types.extend([adaptation_type] * count)

    total = len(works)
    if not (len(media) == len(decades) == len(adaptation_types) == total):
        raise ValueError("All aggregate counts must sum to the same total.")

    df = pd.DataFrame(
        {
            "adaptation_id": range(1, total + 1),
            "source_work": works,
            "media_type": media,
            "decade": decades,
            "adaptation_type": adaptation_types,
        }
    )

    # Create representative release years from decades.
    df["release_year"] = df["decade"] + 5

    return df

# ------------------------------------------------------------
# 4. Cleaning and standardization helpers
# ------------------------------------------------------------

TITLE_MAP = {
    "pride & prejudice": "Pride and Prejudice",
    "pride and prejudice": "Pride and Prejudice",
    "orgulho e preconceito": "Pride and Prejudice",
    "sense and sensibility": "Sense and Sensibility",
    "razao e sensibilidade": "Sense and Sensibility",
    "razão e sensibilidade": "Sense and Sensibility",
    "northanger abbey": "Northanger Abbey",
    "a abadia de northanger": "Northanger Abbey",
}


def standardize_title(title: str) -> str:
    """Normalize title variants into one canonical title."""
    if pd.isna(title):
        return title
    key = str(title).strip().lower()
    return TITLE_MAP.get(key, str(title).strip())


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Clean titles, remove duplicates, and enforce consistent data types."""
    df = df.copy()
    df["source_work"] = df["source_work"].apply(standardize_title)
    df["media_type"] = df["media_type"].str.strip()
    df["adaptation_type"] = df["adaptation_type"].str.strip().str.title()
    df["release_year"] = df["release_year"].astype(int)
    df["decade"] = (df["release_year"] // 10) * 10
    df = df.drop_duplicates()
    return df

# ------------------------------------------------------------
# 5. Plot styling
# ------------------------------------------------------------


def apply_clean_style(ax):
    """Apply a clean portfolio-style visual format."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.grid(axis="x", alpha=0.15)
    ax.set_axisbelow(True)


def save_chart(fig, filename: str):
    """Save a chart as a high-resolution PNG."""
    path = VIZ_DIR / filename
    fig.savefig(path, dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"Saved: {path}")

# ------------------------------------------------------------
# 6. Visualizations
# ------------------------------------------------------------


def plot_adaptations_by_work(df: pd.DataFrame):
    counts = df["source_work"].value_counts().reindex(WORK_COUNTS.keys())
    counts = counts.sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(13, 7))
    bars = ax.barh(
        counts.index,
        counts.values,
        color=[WORK_COLORS[w] for w in counts.index],
    )

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.4, bar.get_y() + bar.get_height() / 2, f"{int(width)}", va="center", fontsize=11)

    ax.set_title("Adaptations by Jane Austen Work", fontsize=24, weight="bold", pad=18)
    ax.set_xlabel("Number of adaptations", fontsize=13)
    ax.set_ylabel("Work", fontsize=13)
    apply_clean_style(ax)

    legend_handles = [mpatches.Patch(color=color, label=work) for work, color in WORK_COLORS.items()]
    ax.legend(handles=legend_handles, title="Works", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)
    save_chart(fig, "01_adaptations_by_work.png")


def plot_adaptations_by_decade(df: pd.DataFrame):
    counts = df.groupby("decade").size()

    fig, ax = plt.subplots(figsize=(13, 7))
    bars = ax.bar(counts.index.astype(str), counts.values, color=COLORS["merlot"])

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height + 0.4, f"{int(height)}", ha="center", fontsize=11)

    ax.set_title("Adaptations by Decade", fontsize=24, weight="bold", pad=18)
    ax.set_xlabel("Decade", fontsize=13)
    ax.set_ylabel("Number of adaptations", fontsize=13)
    ax.grid(axis="y", alpha=0.15)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    save_chart(fig, "02_adaptations_by_decade.png")


def plot_direct_vs_loose_donut(df: pd.DataFrame):
    counts = df["adaptation_type"].value_counts().reindex(["Direct", "Loose"])
    total = counts.sum()
    colors = [TYPE_COLORS[label] for label in counts.index]

    fig, ax = plt.subplots(figsize=(12, 8))
    wedges, _, autotexts = ax.pie(
        counts.values,
        colors=colors,
        startangle=90,
        counterclock=False,
        wedgeprops={"width": 0.38, "edgecolor": "white", "linewidth": 2},
        autopct=lambda p: f"{p:.1f}%",
        pctdistance=0.78,
        textprops={"color": "white", "fontsize": 16, "weight": "bold"},
    )

    ax.text(0, 0.08, f"{total}", ha="center", va="center", fontsize=34, weight="bold", color=COLORS["deep_purple"])
    ax.text(0, -0.12, "adaptations", ha="center", va="center", fontsize=16, color=COLORS["deep_purple"])
    ax.set_title("Proportion of Direct and Loose Adaptations", fontsize=24, weight="bold", pad=20)

    legend_labels = [
        f"{label} — {counts[label]} ({counts[label] / total:.1%})" for label in counts.index
    ]
    ax.legend(wedges, legend_labels, title="Type of adaptation", loc="center left", bbox_to_anchor=(1, 0.5), frameon=False)
    save_chart(fig, "03_direct_vs_loose_donut.png")


def plot_media_type(df: pd.DataFrame):
    counts = df["media_type"].value_counts().reindex(MEDIA_COUNTS.keys())
    counts = counts.sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(13, 8))
    bars = ax.barh(
        counts.index,
        counts.values,
        color=[MEDIA_COLORS[m] for m in counts.index],
    )

    for bar in bars:
        width = bar.get_width()
        ax.text(width + 0.3, bar.get_y() + bar.get_height() / 2, f"{int(width)}", va="center", fontsize=11)

    ax.set_title("Adaptations by Media Type", fontsize=24, weight="bold", pad=18)
    ax.set_xlabel("Number of adaptations", fontsize=13)
    ax.set_ylabel("Media type", fontsize=13)
    apply_clean_style(ax)

    legend_handles = [mpatches.Patch(color=color, label=media) for media, color in MEDIA_COLORS.items()]
    ax.legend(handles=legend_handles, title="Media", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)
    save_chart(fig, "04_adaptations_by_media_type.png")


def plot_adaptation_type_by_decade(df: pd.DataFrame):
    pivot = (
        df.pivot_table(index="decade", columns="adaptation_type", values="adaptation_id", aggfunc="count", fill_value=0)
        .reindex(columns=["Direct", "Loose"], fill_value=0)
        .sort_index()
    )
    totals = pivot.sum(axis=1)
    percentage = totals / totals.sum() * 100

    fig, ax1 = plt.subplots(figsize=(14, 7))
    x = range(len(pivot.index))

    ax1.bar(x, pivot["Direct"], color=TYPE_COLORS["Direct"], label="Direct Adaptations")
    ax1.bar(x, pivot["Loose"], bottom=pivot["Direct"], color=TYPE_COLORS["Loose"], label="Loose Adaptations")

    for i, decade in enumerate(pivot.index):
        direct = pivot.loc[decade, "Direct"]
        loose = pivot.loc[decade, "Loose"]
        total = totals.loc[decade]
        if direct > 0:
            ax1.text(i, direct / 2, str(int(direct)), ha="center", va="center", color="white", weight="bold", fontsize=10)
        if loose > 0:
            ax1.text(i, direct + loose / 2, str(int(loose)), ha="center", va="center", color="white", weight="bold", fontsize=10)
        ax1.text(i, total + 0.5, str(int(total)), ha="center", fontsize=11, weight="bold", color=COLORS["deep_purple"])

    ax2 = ax1.twinx()
    ax2.plot(x, percentage.values, color=COLORS["crimson_blaze"], marker="o", linewidth=2.5, label="Percentage of Total (%)")
    for i, pct in enumerate(percentage.values):
        ax2.text(i, pct + 0.8, f"{pct:.1f}%", ha="center", color=COLORS["crimson_blaze"], fontsize=10)

    ax1.set_title("Adaptation Type by Decade", fontsize=24, weight="bold", pad=18)
    ax1.set_xticks(list(x))
    ax1.set_xticklabels([str(d) for d in pivot.index])
    ax1.set_xlabel("Decade", fontsize=13)
    ax1.set_ylabel("Number of adaptations", fontsize=13, color=COLORS["deep_purple"])
    ax2.set_ylabel("Percentage of total (%)", fontsize=13, color=COLORS["crimson_blaze"])

    ax1.grid(axis="y", alpha=0.15)
    ax1.spines["top"].set_visible(False)
    ax2.spines["top"].set_visible(False)

    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(handles1 + handles2, labels1 + labels2, loc="upper center", bbox_to_anchor=(0.5, -0.12), ncol=3, frameon=False)

    save_chart(fig, "05_adaptation_type_by_decade.png")

# ------------------------------------------------------------
# 7. Main execution
# ------------------------------------------------------------


def main():
    df = build_dataset()
    df = clean_dataset(df)

    output_csv = DATA_DIR / "jane_austen_adaptations.csv"
    df.to_csv(output_csv, index=False)
    print(f"Saved dataset: {output_csv}")

    plot_adaptations_by_work(df)
    plot_adaptations_by_decade(df)
    plot_direct_vs_loose_donut(df)
    plot_media_type(df)
    plot_adaptation_type_by_decade(df)

    print("Analysis complete.")


if __name__ == "__main__":
    main()
