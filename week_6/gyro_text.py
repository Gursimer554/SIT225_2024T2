# File: app.py
# pip install dash plotly pandas

import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

CSV_PATH = "gyro.csv"  # produced by logger OR simulator
df = pd.read_csv(CSV_PATH)
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(df["timestamp"])
else:
    # build a datetime index from ms if present
    if "timestamp_ms" in df.columns:
        df["timestamp"] = pd.to_timedelta(df["timestamp_ms"], unit="ms")

app = Dash(__name__)
app.title = "Gyroscope Dashboard"

GRAPH_TYPES = [
    {"label": "Line", "value": "line"},
    {"label": "Scatter", "value": "scatter"},
    {"label": "Distribution (Histogram)", "value": "hist"},
    {"label": "Box", "value": "box"},
]

app.layout = html.Div([
    html.H2("Gyroscope Data Dashboard (x, y, z)"),
    html.Div([
        html.Div([
            html.Label("Graph type"),
            dcc.Dropdown(id="graph-type", options=GRAPH_TYPES, value="line", clearable=False)
        ], style={"minWidth":"220px", "marginRight":"1rem"}),

        html.Div([
            html.Label("Variables"),
            dcc.Dropdown(
                id="vars",
                options=[{"label": c.upper(), "value": c} for c in ["x","y","z"]],
                value=["x","y","z"], multi=True
            ),
        ], style={"minWidth":"240px", "marginRight":"1rem"}),

        html.Div([
            html.Label("Samples per page"),
            dcc.Input(id="n", type="number", min=50, step=50, value=500),
        ], style={"minWidth":"180px"})
    ], style={"display":"flex", "flexWrap":"wrap", "alignItems":"end"}),

    html.Div([
        html.Button("Previous", id="prev", n_clicks=0, style={"marginRight":"0.5rem"}),
        html.Button("Next", id="next", n_clicks=0),
        html.Span(id="page-info", style={"marginLeft":"1rem"})
    ], style={"margin":"0.8rem 0"}),

    dcc.Graph(id="graph"),
    html.H3("Summary (visible window)"),
    html.Div(id="summary")
], style={"maxWidth":"1100px","margin":"0 auto","fontFamily":"sans-serif"})

@app.callback(
    Output("graph","figure"),
    Output("summary","children"),
    Output("page-info","children"),
    Input("graph-type","value"),
    Input("vars","value"),
    Input("n","value"),
    Input("prev","n_clicks"),
    Input("next","n_clicks"),
)
def update(gtype, vars_sel, n, prev_clicks, next_clicks):
    if not vars_sel:
        vars_sel = ["x"]
    n = max(50, min(int(n or 500), len(df)))
    page = max(0, (next_clicks - prev_clicks))
    start = page * n
    end = min(start + n, len(df))
    if start >= len(df):
        start, end = max(0, len(df)-n), len(df)
    view = df.iloc[start:end].reset_index(drop=True)

    # Figure
    if gtype == "line":
        fig = px.line(view, x="timestamp", y=vars_sel)
    elif gtype == "scatter":
        fig = px.scatter(view, x="timestamp", y=vars_sel)
    elif gtype == "box":
        m = view[vars_sel].melt(var_name="axis", value_name="value")
        fig = px.box(m, x="axis", y="value")
    else:
        m = view[vars_sel].melt(var_name="axis", value_name="value")
        fig = px.histogram(m, x="axis", y="value", histfunc="avg", barmode="group")

    fig.update_layout(margin=dict(l=20,r=20,t=40,b=20), height=500)

    # Summary table
    stats = view[vars_sel].describe().T[["count","mean","std","min","50%","max"]].round(4)
    header = [html.Tr([html.Th("variable")] + [html.Th(c) for c in stats.columns])]
    rows = [html.Tr([html.Td(idx)] + [html.Td(stats.loc[idx, c]) for c in stats.columns]) for idx in stats.index]
    table = html.Table(header + rows, style={"borderCollapse":"collapse","width":"100%"})

    page_text = f"Showing {start+1:,}–{end:,} of {len(df):,} (page {page+1})"
    return fig, table, page_text

if __name__ == "__main__":
    app.run_server(debug=True)
