# loading libraries
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import dash_bootstrap_components as dbc

# loading dataset
df = pd.read_csv("Superstore.csv")

# data wrangling required for the plot
df = df.drop_duplicates()
df = df.drop(df[df.Sales < 100].index)
df = df.drop(df[df.Profit == -6599.9780].index)
df_furniture = df[df["Category"]=="Furniture"]
df_office = df[df["Category"]=="Office Supplies"]
df_tech = df[df["Category"]=="Technology"]
dff = df_furniture[["Sub-Category", "Sales", "Profit"]]
df_furniture = dff.groupby('Sub-Category').sum().reset_index()
dfo = df_office[["Sub-Category", "Sales", "Profit"]]
df_office = dfo.groupby('Sub-Category').sum().reset_index()
dft = df_tech[["Sub-Category", "Sales", "Profit"]]
df_tech = dft.groupby('Sub-Category').sum().reset_index()

#creating lists for plot
catf = df_furniture['Sub-Category'].tolist()
fsales = df_furniture['Sales'].tolist()
fprofit = df_furniture['Profit'].tolist()
cato = df_office['Sub-Category'].tolist()
osales = df_office['Sales'].tolist()
oprofit = df_office['Profit'].tolist()
catt = df_tech['Sub-Category'].tolist()
tsales = df_tech['Sales'].tolist()
tprofit = df_tech['Profit'].tolist()
ls = ["Furniture", "Office Supplies", "Technology"]

app = Dash(__name__)    #initialising dash app
app.config['suppress_callback_exceptions'] = True  # to avoid warnings 
app.layout = html.Div(dbc.Container([   # here, I have created a container to stack plot and dropdown
    dbc.Col([
        dbc.Row([
            dcc.Dropdown(
        id='category-widget',  # ID for dropdown
        value='Furniture',  
        options=[{'label': col, 'value': col} for col in ls], placeholder="Select a category")], style={'width':'22.5%', 
        "font-weight": "bold", 'padding-left' : '475px'}),  # styling for dropdown
        dbc.Row(
            html.Iframe(
        id='barchart',    # ID for bar chart
        style={'border-width': '0', 'width': '100%', 'height': '500px'}))])]), # styling for plot
        style={'width':'50%',"border":"6px hotpink solid", 
        'backgroundColor':'black'}) # styling for overall dashboard
   

@app.callback(          # dash decorator function
    Output('barchart', 'srcDoc'),
    Input('category-widget', 'value'))     

def my_plot(category):            # callback function
    
    if category == "Furniture":
        cat=catf
        cat_sales=fsales
        cat_profit=fprofit
    elif category == "Office Supplies":
        cat=cato
        cat_sales=osales
        cat_profit=oprofit
    else:
        cat=catt
        cat_sales=tsales
        cat_profit=tprofit
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
    x=cat,
    y=cat_sales,
    name='Sales',
    marker_color='purple'
    ))
    fig.add_trace(go.Bar(
    x=cat,
    y=cat_profit,
    name='Profit',
    marker_color='hotpink'
    ))

    fig.update_layout(barmode='group', xaxis_tickangle=0, title="Overall Sales & Profit by Category", 
                  title_font_size=25, title_x=0.339, title_y=0.96, xaxis_title="Sub-categories",
                 template = "plotly_dark", margin=dict(l=20, r=20, t=45, b=9), 
                 legend=dict(y=0.6, font_size=15), xaxis = dict(tickfont = dict(size=12)))             # styling for plot
    fig.update_yaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    fig.update_xaxes(tickprefix="<b>",ticksuffix ="</b><br>")
    
    return fig.to_html()       


if __name__ == '__main__':
    app.run_server(port=8052, debug=True)