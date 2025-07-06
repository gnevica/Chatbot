import plotly.express as px

def plot_uploaded_csv(df, user_query):
    # Auto-detect x and y based on query
    chart_type = "line" if "line" in user_query else "bar"
    x = df.columns[0]
    y = df.columns[1]

    if chart_type == "line":
        fig = px.line(df, x=x, y=y)
    else:
        fig = px.bar(df, x=x, y=y)
    return fig