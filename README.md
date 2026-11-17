# NBA Sports Statistics & Team Performance Dashboard

A beginner-friendly Streamlit + Plotly project for Visual Studio Code.

## What is included
- `app.py` — complete interactive dashboard code.
- `data/sample_preview.csv` — small illustrative preview so the dashboard can open even if the data host is temporarily unreachable.
- `requirements.txt` — Python packages.
- `Assignment3_Notebook_Guide.md` — narrative notebook outline and prompts.
- `AI_LOG_TEMPLATE.md` — transparent AI-use log template.

## Important dataset note
The app attempts to download the public NBA playoff team-game totals dataset from:

https://github.com/NocturneBear/NBA-Data-2010-2024

The repository states that it is licensed under the MIT License. The app stores the downloaded CSV at `data/nba_playoff_team_games.csv` for later runs. The bundled `sample_preview.csv` is illustrative fallback data only; do not present its results as real NBA findings.

The source describes NBA playoff box scores from 2010–2024. This is not a complete regular-season dataset. Cite the source and license in your notebook and dashboard.

## Run in Visual Studio Code

1. Install Python 3.10 or newer.
2. Install Visual Studio Code and the Microsoft Python extension.
3. Unzip this project.
4. In VS Code, choose **File → Open Folder** and select `NBA_Sports_Statistics_Dashboard`.
5. Open **Terminal → New Terminal**.
6. Create a virtual environment:

   Windows:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```

   macOS/Linux:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

7. Install the libraries:

   ```bash
   python -m pip install -r requirements.txt
   ```

8. Start the dashboard:

   ```bash
   streamlit run app.py
   ```

9. Streamlit will show a local address, usually `http://localhost:8501`. Open it in your browser.

If PowerShell blocks environment activation, you can install with `python -m pip install -r requirements.txt` and run `python -m streamlit run app.py` without activating the environment.

## Libraries used
- **Streamlit**: dashboard layout, controls, and app hosting.
- **Plotly Express / Graph Objects**: interactive charts.
- **Pandas**: data loading and cleaning.

Matplotlib and pandas `.plot()` are not used.

## Dashboard features
The season and team multiselect controls update all visualizations:
1. Bar chart: average points by team.
2. Scatterplot: points versus rebounds, colored by win/loss.
3. Line chart: average points across seasons.
4. Sankey diagram: flow from team to game outcome to scoring band.

The Sankey diagram is the new-to-class method in this project. It shows how records flow across multiple categorical stages; a standard bar chart does not show those connected paths as directly.

## Before submitting
- Run the app using the actual downloaded data, not only the sample preview.
- Check that the source CSV column names map correctly. If the source changes, update `standardize_columns()` in `app.py`.
- Explore the filters and record at least one specific finding that only became clear after interacting with the dashboard.
- Capture screenshots of the finished dashboard.
- Publish the Streamlit app (for example, with Streamlit Community Cloud) and test the link in a private/incognito browser.
- Record a narrated video within the assignment's time limit.
- Complete the notebook and AI log using your own observations and actual troubleshooting experience.
