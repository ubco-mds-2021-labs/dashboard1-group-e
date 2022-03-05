import dash
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import base64

# Read data
df = pd.read_csv('../data/Superstore.csv')

# Create instance of app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Components

## Components: Logo
### Reference: https://community.plotly.com/t/adding-local-image/4896/9
logo = html.Img(src=app.get_asset_url('logo.png'), style={'height':'75%'})

## Components: Plot 1
plot1 = html.Div([
    dcc.Graph(id='pie-graph-with-radio1', style={'width': 300, 'height': 300}),
    dbc.Row(
        dbc.Col(
            [dcc.RadioItems(
                options=['Sales', 'Profit', 'Quantity'],
                value='Sales',
                id='metrics1',
                inline=False,
                inputStyle={"margin-left": "20px", "margin-right": "2px"})], 
            width={"size": 10, "offset": 1}  
        )
    )
], style={'padding': '2rem 1rem', 'border':'1px lightgray solid'})

## Components: Plot 2
plot2 = html.Div([
    dcc.Graph(id='pie-graph-with-radio2', style={'width': 300, 'height': 300}),
    dbc.Row(
        dbc.Col(
            [dcc.RadioItems(
                options=['Sales', 'Profit', 'Quantity'],
                value='Sales',
                id='metrics2',
                inline=False,
                inputStyle={"margin-left": "20px", "margin-right": "2px"})], 
            width={"size": 10, "offset": 1}  
        )
    )
], style={'padding': '2rem 1rem', 'border':'1px lightgray solid'})

## Components: Plot 3
plot3 = html.Div([
    dcc.Graph(id='pie-graph-with-radio3', style={'width': 300, 'height': 300}),
    dbc.Row(
        dbc.Col(
            [dcc.RadioItems(
                options=['Sales', 'Profit', 'Quantity'],
                value='Sales',
                id='metrics3',
                inline=False,
                inputStyle={"margin-left": "20px", "margin-right": "2px"})], 
            width={"size": 10, "offset": 1}  
        )
    )
], style={'padding': '2rem 1rem', 'border':'1px lightgray solid'})

## Components: Plot 4
states = sorted(df['State'].unique())
plot4 = html.Div([
    html.Div(id='output-title4'),
    dcc.Dropdown(states, 'New York', id='states-dropdown', style={'width': 200, 'height': 20}),
    dcc.Graph(id='bar-graph-top-items', style={'width': 700, 'height': 150})
], style={'border':'1px lightgray solid'})

## Components: Plot 5
plot5 = html.Div([
    dcc.Graph(id='pie-graph-with-radio5', style={'width': 700, 'height': 690}),
    dbc.Row(
        dbc.Col(
            [dcc.RadioItems(
                options=['Sales', 'Profit', 'Quantity'],
                value='Sales',
                id='metrics5',
                inline=False,
                inputStyle={"margin-left": "20px", "margin-right": "2px"})], 
            width={"size": 10, "offset": 1}  
        )
    )
], style={'padding': '2rem 1rem', 'border':'1px lightgray solid'})


## Components: Plot 6
subcat = sorted(df['Sub-Category'].unique())
plot6 = html.Div([
    html.Div(id='output-title6'),
    dcc.Dropdown(subcat, 'Binders', id='subcat-dropdown', style={'width': 200, 'height': 20}),
    dcc.Graph(id='bar-graph-top-states', style={'width': 700, 'height': 150})
], style={'border':'1px lightgray solid'})

# Layout
app.layout = html.Div([
    dbc.Row(dbc.Col(logo)),

    dbc.Row([dbc.Col(plot1, width=4), 
            dbc.Col([dbc.Row(plot4), dbc.Row(plot6)], width=8)
            ]),

    dbc.Row([
            dbc.Col([
                dbc.Row(dbc.Col(plot2)),
                dbc.Row(dbc.Col(plot3))], width=4),
            dbc.Col([
                dbc.Row(dbc.Col(plot5))], width=8)
           ]) 
    ])

# Callback
## Callback: Plot 1
@app.callback(
    Output('pie-graph-with-radio1', 'figure'),
    Input('metrics1', 'value'))
def update_figure(selected_metrics):
    fig = px.pie(df, 
                values=selected_metrics, 
                names='Segment', 
                color='Segment',
                color_discrete_map={'Consumer':'red',
                                 'Corporate':'midnightblue',
                                 'Home Office':'lightgray'},
                title='Metrics Proportion by Segment')
    fig.update_layout(transition_duration=500).update_layout(
        margin=dict(l=25, r=0, t=25, b=0))
    return fig

## Callback: Plot 2
@app.callback(
    Output('pie-graph-with-radio2', 'figure'),
    Input('metrics2', 'value'))
def update_figure(selected_metrics):
    fig = px.pie(df, 
                values=selected_metrics, 
                names='Segment', 
                color='Segment',
                color_discrete_map={'Consumer':'red',
                                 'Corporate':'midnightblue',
                                 'Home Office':'lightgray'},
                title='Metrics Proportion by Segment')
    fig.update_layout(transition_duration=500).update_layout(
        margin=dict(l=25, r=0, t=25, b=0))
    return fig

## Callback: Plot 3
@app.callback(
    Output('pie-graph-with-radio3', 'figure'),
    Input('metrics3', 'value'))
def update_figure(selected_metrics):
    fig = px.pie(df, 
                values=selected_metrics, 
                names='Segment', 
                color='Segment',
                color_discrete_map={'Consumer':'red',
                                 'Corporate':'midnightblue',
                                 'Home Office':'lightgray'},
                title='Metrics Proportion by Segment')
    fig.update_layout(transition_duration=500).update_layout(
        margin=dict(l=25, r=0, t=25, b=0))
    return fig

## Callback: Plot 4
@app.callback(
    Output('output-title4', 'children'),
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
    ).update_yaxes(visible=False)
    

    return f'Top 5 Items Sold in: {selected_state}', fig

## Callback: Plot 5
@app.callback(
    Output('pie-graph-with-radio5', 'figure'),
    Input('metrics5', 'value'))
def update_figure(selected_metrics):
    fig = px.pie(df, 
                values=selected_metrics, 
                names='Segment', 
                color='Segment',
                color_discrete_map={'Consumer':'red',
                                 'Corporate':'midnightblue',
                                 'Home Office':'lightgray'},
                title='Metrics Proportion by Segment')
    fig.update_layout(transition_duration=500).update_layout(
        margin=dict(l=25, r=0, t=25, b=0))
    return fig


## Callback: Plot 6
@app.callback(
    Output('output-title6', 'children'),
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
    ).update_yaxes(visible=False)

    return f'Top 5 States With Highest Quantity Sold in: {selected_item} ', fig

# Run server
if __name__ == '__main__':
    app.run_server(debug=True)
