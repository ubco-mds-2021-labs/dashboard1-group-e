from dash import Dash, dcc, html, Input, Output
import plotly.express as px

import pandas as pd

df = pd.read_csv('../data/Superstore.csv')

app = Dash(__name__)

app.layout = html.Div([
    dcc.Graph(id='pie-graph-with-radio', style={'width': 500, 'height': 500}),
    dcc.RadioItems(
                options=['Sales', 'Profit', 'Quantity'],
                value='Sales',
                id='metrics',
                inline=False
            )

])


@app.callback(
    Output('pie-graph-with-radio', 'figure'),
    Input('metrics', 'value'))
def update_figure(selected_metrics):
    fig = px.pie(df, 
                values=selected_metrics, 
                names='Segment', 
                color='Segment',
                color_discrete_map={'Consumer':'red',
                                 'Corporate':'midnightblue',
                                 'Home Office':'lightgray'},
                title='Metrics Proportion by Segment')
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
