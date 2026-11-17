# Assignment 3: Visual Exploration Dashboard — Notebook Guide

Use these headings in your `Assignment3.ipynb` notebook. The assignment asks for a narrative notebook of about 1,500 words plus screenshots. Replace every bracketed prompt with your own observations after running the dashboard.

## 1. Introduction
This project explores NBA playoff team performance from 2010–2024. It asks how team scoring, rebounding, assists, and game outcomes vary across teams and seasons. The dashboard is intended for readers who want to compare team-game records interactively rather than rely on a single summary table.

Add:
- Screenshot of your working dashboard.
- Public dashboard link after deployment.

## 2. Library choice and fit
**Chosen tools:** Streamlit for the dashboard interface and Plotly for interactive charts.

Explain in your own words:
- Streamlit is an open-source Python framework created by Streamlit, Inc. and released under the Apache 2.0 license.
- Plotly is an open-source graphing library; Plotly.py is distributed under the MIT license.
- Install with `python -m pip install streamlit plotly`.
- Streamlit uses a procedural Python script to define the app; Plotly charts are built from data and chart specifications.
- They work well together because Streamlit embeds Plotly figures and provides widgets that can filter multiple charts.
- Limitation: Streamlit reruns the script when controls change; very large datasets or expensive calculations may need caching or optimization.
- Alternative considered: Bokeh or Dash. Explain why you selected Streamlit + Plotly instead.

Verify current library background and licenses from the official project documentation before submitting.

## 3. Data
**Source:** NocturneBear, NBA-Data-2010-2024, https://github.com/NocturneBear/NBA-Data-2010-2024  
**License:** MIT (as stated in the repository).  
**Scope:** NBA playoff team-game totals from 2010–2024.

Describe the exact file and columns used after you download it. Explain the cleaning in `prepare_data()`:
1. Standardize column names.
2. Convert numeric performance fields to numeric values.
3. Parse dates where available.
4. Fill or normalize missing win/loss labels as `Unknown`.
5. Remove rows missing team, points, rebounds, or assists.
6. Create scoring bands for the Sankey visualization.

Record the actual number of rows and columns from the real downloaded data. Do not use the preview file's counts as real-data statistics.

## 4. Visualization techniques
For each chart, explain what it shows, why it is useful for this dataset, and when it may be misleading:
- Bar chart: compares average points by team; not ideal for showing detailed distributions or uncertainty.
- Scatterplot: examines the relationship between points and rebounds; can become crowded with many records.
- Line chart: compares average points across seasons; only appropriate when season order is meaningful.
- Sankey diagram (new-to-class): traces records from team to result to scoring band; useful for multi-stage categorical flow, but can become cluttered with too many teams or categories.

Explain how the four views complement each other.

## 5. Building and exploring
Document the process:
1. Load and clean the CSV.
2. Build the bar chart.
3. Add the scatterplot and line chart.
4. Add the Sankey diagram.
5. Add the season and team filters.
6. Test that one filter updates at least two charts (in this app, the controls filter all four charts).

Exploration narrative — complete after you interact:
- Question you started with: [write your question].
- Filter/interaction you tried: [name the season/team selection].
- What changed across the views: [describe what you observed].
- Finding visible only after interaction: [state a specific evidence-backed finding, including selected filter and values].
- Dead end or surprising result: [describe what did not work or what surprised you].

Do not invent a finding. Use the actual dashboard output as evidence.

## 6. AI log and troubleshooting
Disclose that ChatGPT helped plan and draft parts of the code and documentation. Use `AI_LOG_TEMPLATE.md`; record at least three real entries. The assignment requires at least two entries describing something AI got wrong or designed poorly, how you noticed, and how you fixed it. Do not claim a problem occurred unless it actually happened. If the generated code works without those issues, test deliberately, document real limitations you find, and ask your instructor how to satisfy the required troubleshooting evidence honestly.

## 7. Deployment instructions
Describe your actual deployment process and include the public URL. If you use Streamlit Community Cloud, connect the project repository, choose `app.py` as the entry point, and verify that the dashboard opens without local setup.
