# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
import plotly.express as px
import plotly.graph_objects as go
import plotly as py
import pandas as pd
from plotly import tools
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash import Dash

###################################################################################################
app = Dash(__name__)
app.config['suppress_callback_exceptions'] = True

# Reading in data
df = pd.read_csv("Superstore.csv")
# Removing outlier
df = df.drop(df[df.Profit == -6599.9780].index)
# To sum profit and sales over all cities, for each state
df = df.groupby(["State", "Category", "Sub-Category", "Ship Mode", "Segment"], as_index=False)[["Sales", "Profit","Discount"]].sum()
df = pd.DataFrame(df)
# Adding column for profit margin
df['Profit Margin'] = df['Profit']/df['Sales']
                                      
def categorise(row):
    if row['Discount'] > 0:
        return 'Yes'
    return 'No'
df['Discount_Status'] = df.apply(lambda row: categorise(row), axis=1)
#dataset = df.groupby(['Category', 'Sub-Category','Discount_Status']).sum(['Sales']).reset_index()
category_list = list(dataset["Category"].unique())
category_list.append("All")  
####################################################################################################
import dash_bootstrap_components as dbc
from dash import html
   
graph1 =  html.Div(
    [

    html.Br(),
    html.Br(),

    dcc.RadioItems(
        id='type-radio',
        options=[{'label': k, 'value': k} for k in ['Sales', 'Profit Margin']],
        value='Sales',
    ),
    html.Br(),
    html.Br(),
        dcc.Dropdown(
        id='Category-dropdown',
      options=[{'label': k, 'value': k} for k in category_list],
        value='Furniture',
            ),

    html.Hr(),
    html.Br(),
    html.Br(),
    html.Div(id='display-selected-values'),
    dcc.Graph(id="mkt_graph"),
    ])




app.layout = graph1

# Make a figure based on the selections
@app.callback( # Columns 2m_temp_prod, or....
    Output('mkt_graph', 'figure'),
    [
     Input('Category-dropdown', 'value'),
     Input('type-radio', 'value'),])
     
     
def make_graph(levels,type_graph):
    if type_graph != "Profit Margin":
        group_by_profit = df.groupby(["Sub-Category","Category","Discount_Status"],as_index=False)[["Sales", "Profit Margin","Discount"]].sum()
    else:
        group_by_profit = df.groupby(["Sub-Category","Category","Discount_Status"],as_index=False)[["Sales","Profit Margin"]].mean()
        #group_by_profit["Profit Margin"] = group_by_profit["Profit Margin"]*100

    title_all =  "All Categories"
    
    if levels != "All":
        title_all = levels
        group_by_profit = group_by_profit[group_by_profit["Category"]==levels]
    if type_graph!="Profit Margin":
        fig = px.bar(group_by_profit, x="Sub-Category", y="Sales", color="Discount_Status", barmode='group', height=1000,color_discrete_sequence=["Red","midnightblue"])
        
        fig.update_layout(
            title={'text': "<b>Sales by "+str(title_all)+"<b>",'y':1,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            font_family="Calibri",
            font_size=20,
            font_color="black",
#            title_font_family="Times New Roman",
            title_font_color="black",
            legend_title_font_color="black",
            legend_title_font_size=20,
            legend_title = "Discount Applied?",
        )
        fig.update_xaxes()
    
        
        
        
        
    else:
        
        
        fig = px.bar(group_by_profit, x="Sub-Category", y="Profit Margin", color="Discount_Status", barmode='group', height=1000 ,color_discrete_sequence=["Red","midnightblue"] )
        
        fig.update_layout(
            title={'text': "<b>Profit/Loss by "+str(title_all)+'<b>','y':1,'x':0.5,'xanchor': 'center','yanchor': 'top'},
            font_family="Calibri",
            font_size=20,
            font_color="black",
#            title_font_family="Times New Roman",
            title_font_color="black",
            legend_title_font_color="black",
            legend_title_font_size=20,
            legend_title = "Discount Applied?",
            
    
        
        )
        fig.update_xaxes(title={'text':str(levels)})
        
        fig.update_yaxes(tickformat=",.0%", title=None)
    fig.update_layout(
    legend=dict(
        x=0,
        y=1,
        traceorder="reversed",
#        title_font_family="Times New Roman",
        font=dict(
            family="Courier",
            size=12,
            color="black"
        ),
        bgcolor="lightgray",
        bordercolor="Black",
        borderwidth=2
    )
)
 
    
    return fig

# -

print("loaded all , now running the server")
#if __name__ == '__main__':
app.run_server(debug=False)


