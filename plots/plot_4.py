from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import pandas as pd

df = pd.read_csv('../data/Superstore.csv')
states = sorted(df['State'].unique())

app = Dash(__name__)

app.layout = html.Div([
    html.H1(id='output-title'),
    html.Br(),
    dcc.Dropdown(states, 'New York', id='states-dropdown'),
    dcc.Graph(id='bar-graph-top-items')

])


@app.callback(
    Output('output-title', 'children'),
    Output('bar-graph-top-items', 'figure'),
    Input('states-dropdown', 'value'))
def update_figure(selected_state):
    filtered_df = df[['State','Sub-Category','Quantity']]
    filtered_df = filtered_df[filtered_df['State']==selected_state].groupby('Sub-Category').sum()
    filtered_df = filtered_df.sort_values(by='Quantity',ascending=False)[0:5].reset_index()

    fig = px.bar(filtered_df, x='Sub-Category', y='Quantity')
    fig.update_traces(
        marker_color='midnightblue'
    ).update_layout({
        'plot_bgcolor': 'rgba(0,0,0,0)',
        'paper_bgcolor': 'rgba(0,0,0,0)'
    }).update_layout(
        transition_duration=500
    )

    return f'Top 5 Items Sold in: {selected_state}', fig


if __name__ == '__main__':
    app.run_server(debug=True)
