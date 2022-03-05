from ctypes import alignment
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# Read data
df = pd.read_csv('../data/Superstore.csv')
subcat = sorted(df['Sub-Category'].unique())

# Create instance of app
app = Dash(__name__,external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = html.Div([
    html.H1(id='output-title'),
    html.Br(),
    dcc.Dropdown(subcat, 'Binders', id='subcat-dropdown'),
    dcc.Graph(id='bar-graph-top-states')

])

# Callback
@app.callback(
    Output('output-title', 'children'),
    Output('bar-graph-top-states', 'figure'),
    Input('subcat-dropdown', 'value'))
def update_figure(selected_item):
    filtered_df = df[['State','Sub-Category','Quantity']]
    filtered_df = filtered_df[filtered_df['Sub-Category']==selected_item].groupby('State').sum()
    filtered_df = filtered_df.sort_values(by='Quantity',ascending=False)[0:5].reset_index()

    fig = px.bar(filtered_df, x='State', y='Quantity')
    fig.update_traces(
        marker_color='midnightblue'
    ).update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
    }).update_layout(
        transition_duration=500
    )

    return f'Top 5 States With Highest Quantity Sold in: {selected_item}', fig


if __name__ == '__main__':
    app.run_server(debug=True)
