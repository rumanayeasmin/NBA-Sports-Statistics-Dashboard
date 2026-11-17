from pathlib import Path
import urllib.request

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="NBA Performance Explorer", page_icon="🏀", layout="wide")

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
LOCAL_DATA = DATA_DIR / "nba_playoff_team_games.csv"
SAMPLE_DATA = DATA_DIR / "sample_preview.csv"

# Public dataset: NBA playoff team-game totals, 2010–2024.
# The repository describes the data fields and provides an MIT license.
DATA_URL = (
    "https://raw.githubusercontent.com/NocturneBear/"
    "NBA-Data-2010-2024/main/play_off_totals_2010_2024.csv"
)

@st.cache_data(show_spinner=False)
def load_data():
    """Load the public CSV once and cache it for this Streamlit session."""
    if LOCAL_DATA.exists():
        return pd.read_csv(LOCAL_DATA), "Local downloaded dataset"
    try:
        request = urllib.request.Request(
            DATA_URL, headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            content = response.read()
        LOCAL_DATA.write_bytes(content)
        return pd.read_csv(LOCAL_DATA), "Public NBA dataset (downloaded)"
    except Exception as exc:
        # The included preview file makes the app demonstrable without internet.
        preview = pd.read_csv(SAMPLE_DATA)
        return preview, f"Preview data (live download unavailable: {exc})"

def standardize_columns(frame):
    """Normalize common column-name variations without changing values."""
    df = frame.copy()
    df.columns = [str(c).strip().upper().replace(" ", "_") for c in df.columns]
    aliases = {
        "TEAM": "TEAM_NAME",
        "TEAMNAME": "TEAM_NAME",
        "SEASON": "SEASON_YEAR",
        "SEASONYEAR": "SEASON_YEAR",
        "GAME_DATE_EST": "GAME_DATE",
        "DATE": "GAME_DATE",
        "POINTS": "PTS",
        "REBOUNDS": "REB",
        "ASSISTS": "AST",
        "THREE_PM": "FG3M",
        "THREES_MADE": "FG3M",
        "WIN_LOSS": "WL",
        "RESULT": "WL",
    }
    for old, new in aliases.items():
        if old in df.columns and new not in df.columns:
            df = df.rename(columns={old: new})
    return df

def prepare_data(frame):
    df = standardize_columns(frame)
    required = ["TEAM_NAME", "PTS", "REB", "AST"]
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise ValueError(
            "The downloaded file is missing expected columns: "
            + ", ".join(missing)
            + ". Check the data source or update the column mapping in app.py."
        )

    numeric_cols = ["PTS", "REB", "AST", "FG3M", "FG3_PCT", "FG_PCT",
                    "PLUS_MINUS", "MIN", "TOV", "STL", "BLK"]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "SEASON_YEAR" not in df.columns:
        if "GAME_DATE" in df.columns:
            dates = pd.to_datetime(df["GAME_DATE"], errors="coerce")
            df["SEASON_YEAR"] = dates.dt.year.astype("Int64").astype(str)
        else:
            df["SEASON_YEAR"] = "Season not supplied"

    if "WL" not in df.columns:
        df["WL"] = "Unknown"
    df["WL"] = df["WL"].fillna("Unknown").astype(str).str.upper().str.strip()
    df.loc[~df["WL"].isin(["W", "L"]), "WL"] = "Unknown"

    if "GAME_DATE" in df.columns:
        df["GAME_DATE"] = pd.to_datetime(df["GAME_DATE"], errors="coerce")

    # Remove rows that cannot support the core team-performance comparisons.
    df = df.dropna(subset=["TEAM_NAME", "PTS", "REB", "AST"]).copy()
    df["TEAM_NAME"] = df["TEAM_NAME"].astype(str).str.strip()
    df = df[df["TEAM_NAME"] != ""]
    df["SCORING_GROUP"] = pd.cut(
        df["PTS"],
        bins=[-float("inf"), 89, 109, 129, float("inf")],
        labels=["Under 90", "90–109", "110–129", "130+"]
    ).astype(str)
    return df

st.title("🏀 NBA Sports Statistics & Team Performance")
st.markdown(
    "Explore how NBA playoff teams performed from 2010–2024. "
    "Use the filters to compare teams and seasons across several linked views."
)

with st.sidebar:
    st.header("Dashboard filters")
    st.caption("These selections update every chart below.")

try:
    raw, data_status = load_data()
    df = prepare_data(raw)
except Exception as error:
    st.error(f"Could not prepare the dataset: {error}")
    st.info("Check your internet connection and the dataset column names.")
    st.stop()

st.sidebar.success(data_status)
seasons = sorted(df["SEASON_YEAR"].dropna().astype(str).unique().tolist())
teams = sorted(df["TEAM_NAME"].dropna().unique().tolist())

selected_seasons = st.sidebar.multiselect(
    "Season(s)", seasons, default=seasons
)
selected_teams = st.sidebar.multiselect(
    "Team(s)", teams, default=teams
)

filtered = df[
    df["SEASON_YEAR"].astype(str).isin(selected_seasons)
    & df["TEAM_NAME"].isin(selected_teams)
].copy()

if filtered.empty:
    st.warning("No rows match those filters. Select at least one season and team.")
    st.stop()

# Summary cards
games_or_rows = len(filtered)
team_count = filtered["TEAM_NAME"].nunique()
avg_points = filtered["PTS"].mean()
avg_rebounds = filtered["REB"].mean()

m1, m2, m3, m4 = st.columns(4)
m1.metric("Team-game records", f"{games_or_rows:,}")
m2.metric("Teams selected", f"{team_count:,}")
m3.metric("Average points", f"{avg_points:.1f}")
m4.metric("Average rebounds", f"{avg_rebounds:.1f}")

st.divider()

# Chart 1: team scoring comparison
st.subheader("1. Average points by team")
team_summary = (
    filtered.groupby("TEAM_NAME", as_index=False)
    .agg(average_points=("PTS", "mean"), records=("PTS", "size"))
    .sort_values("average_points", ascending=False)
)
fig_bar = px.bar(
    team_summary, x="TEAM_NAME", y="average_points",
    color="average_points", hover_data=["records"],
    labels={"TEAM_NAME": "Team", "average_points": "Average points"},
    title="Which selected teams scored the most per team-game?"
)
fig_bar.update_layout(xaxis_tickangle=-35)
st.plotly_chart(fig_bar, use_container_width=True)

# Chart 2: relationship between scoring and rebounding
st.subheader("2. Scoring versus rebounding")
scatter_cols = ["TEAM_NAME", "PTS", "REB", "AST", "WL"]
hover_cols = [c for c in ["AST", "WL", "SEASON_YEAR"] if c in filtered.columns]
fig_scatter = px.scatter(
    filtered, x="REB", y="PTS", color="WL",
    hover_name="TEAM_NAME", hover_data=hover_cols,
    opacity=0.65,
    labels={"REB": "Rebounds", "PTS": "Points", "WL": "Game result"},
    title="Do higher-rebounding team-games also score more?"
)
st.plotly_chart(fig_scatter, use_container_width=True)

# Chart 3: scoring trend by season
st.subheader("3. Average scoring across seasons")
season_summary = (
    filtered.groupby("SEASON_YEAR", as_index=False)
    .agg(average_points=("PTS", "mean"), average_assists=("AST", "mean"))
)
season_summary["SEASON_YEAR"] = season_summary["SEASON_YEAR"].astype(str)
season_summary = season_summary.sort_values("SEASON_YEAR")
fig_line = px.line(
    season_summary, x="SEASON_YEAR", y="average_points",
    markers=True,
    labels={"SEASON_YEAR": "Season", "average_points": "Average points"},
    title="How did average team-game scoring change over time?"
)
st.plotly_chart(fig_line, use_container_width=True)

# Chart 4: Sankey flow, a method not listed among the course's covered methods.
st.subheader("4. Sankey: team → game result → scoring group")
st.caption(
    "The flow width represents the number of team-game records in each path. "
    "This reveals how each team's records are distributed across outcomes and scoring bands."
)
sankey_data = (
    filtered[filtered["WL"].isin(["W", "L"])]
    .groupby(["TEAM_NAME", "WL", "SCORING_GROUP"], observed=True)
    .size().reset_index(name="count")
)
if not sankey_data.empty:
    labels = (
        sankey_data["TEAM_NAME"].astype(str).tolist()
        + ["Win", "Loss"]
        + ["Under 90", "90–109", "110–129", "130+"]
    )
    # Build unique nodes while retaining a clear three-stage flow.
    team_nodes = sorted(sankey_data["TEAM_NAME"].unique().tolist())
    result_nodes = ["Win", "Loss"]
    score_nodes = ["Under 90", "90–109", "110–129", "130+"]
    node_labels = team_nodes + result_nodes + score_nodes
    node_index = {name: i for i, name in enumerate(node_labels)}
    sources, targets, values = [], [], []
    for _, row in sankey_data.iterrows():
        result_label = "Win" if row["WL"] == "W" else "Loss"
        sources.append(node_index[row["TEAM_NAME"]])
        targets.append(node_index[result_label])
        values.append(int(row["count"]))
        sources.append(node_index[result_label])
        targets.append(node_index[str(row["SCORING_GROUP"])])
        values.append(int(row["count"]))
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(label=node_labels, pad=14, thickness=16),
        link=dict(source=sources, target=targets, value=values)
    )])
    fig_sankey.update_layout(title_text="Distribution of team-game records", height=560)
    st.plotly_chart(fig_sankey, use_container_width=True)
else:
    st.info("The selected rows do not contain W/L outcomes for the Sankey chart.")

with st.expander("Explore the filtered data table"):
    st.dataframe(filtered, use_container_width=True)

with st.expander("Data source, license, and cleaning notes"):
    st.markdown(
        """
        - **Dataset:** NBA playoff team-game totals, 2010–2024.
        - **Source:** NocturneBear, `NBA-Data-2010-2024` on GitHub.
        - **License:** MIT, as stated by the repository.
        - **Source page:** https://github.com/NocturneBear/NBA-Data-2010-2024
        - **Cleaning:** column names are standardized; numeric fields are converted
          to numbers; invalid values become missing; rows without team, points,
          rebounds, or assists are removed; season and outcome labels are normalized.
        - **Limitation:** this dataset covers playoff team-game records, not every
          regular-season NBA game. The dataset's scope should be kept in mind when
          interpreting results.
        """
    )

st.caption(
    "Created for a data-visualization learning project. "
    "Statistics describe the selected dataset and filters; they do not predict future games."
)
