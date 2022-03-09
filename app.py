import dash
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import altair as alt
import base64

alt.data_transformers.disable_max_rows()
# Read data
df = pd.read_csv("data/Superstore.csv")

#########################################
######## Wrangling for each plot ########
#########################################


######### Data wrangling: Plot1
df_plot1 = df.groupby(["Category", "Sub-Category"], as_index=False)[
    ["Sales", "Profit"]
].sum()

# No wrangling needed for plot 2

######## Data wrangling: Plot 3
df_plot3 = df.groupby(
    ["State", "Category", "Sub-Category", "Ship Mode", "Segment"], as_index=False
)[["Sales", "Profit", "Discount"]].sum()
df_plot3 = pd.DataFrame(df_plot3)

# Adding column for profit margin
df_plot3["Profit Margin"] = df_plot3["Profit"] / df_plot3["Sales"]


def categorise(row):
    if row["Discount"] > 0:
        return "Yes"
    return "No"


df_plot3["Discount_Status"] = df_plot3.apply(lambda row: categorise(row), axis=1)
# dataset = df.groupby(['Category', 'Sub-Category','Discount_Status']).sum(['Sales']).reset_index()
category_list = list(df_plot3["Category"].unique())
category_list.append("All")

######### Data wrangling: Plot 4

######### Data wrangling: Plot 5 (map)


def wrangle_data(unwrangled_data):
    """Takes an unwrangled data set and formats it in the appropriate way

    Args:
        unwrangled_data (pandas dataframe): Data that needs to be wrangled

    Returns:
        pandas dataframe: A dataframe with a Profit_Margin column where the profit and sales are grouped over all cities. New columns are also
                            added for the abbreviation of the name of the state and its ID.

    """
    # Removing outlier
    df = unwrangled_data.drop(
        unwrangled_data[unwrangled_data.Profit == -6599.9780].index
    )

    # To sum profit and sales over all cities, for each state
    df = df.groupby(
        ["State", "Category", "Sub-Category", "Ship Mode", "Segment"], as_index=False
    )[["Sales", "Profit"]].sum()
    df = pd.DataFrame(df)

    # Adding column for profit margin
    df["Profit_Margin"] = df["Profit"] / df["Sales"]

    # For rows that don't have sales (when calculating profit margin we get 0/0 = NaN --> replace with 0)
    df = df.fillna(0)

    # Adding id (ansi code) to corresponding state in order to do chloropleth map
    # per https://gist.github.com/mbostock/4090848#gistcomment-2102151
    ansi = pd.read_csv("https://www2.census.gov/geo/docs/reference/state.txt", sep="|")
    ansi.columns = ["id", "abbr", "State", "statens"]
    ansi = ansi[["id", "abbr", "State"]]

    # getting the id to match with the state from the original dataframe
    df = pd.merge(df, ansi, how="left", on="State")
    return df


df_plot5 = wrangle_data(df)


# Create instance of app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server

#########################################
######## Layout Components ##############
#########################################

## Components: Logo
### Reference: https://community.plotly.com/t/adding-local-image/4896/9
logo = html.Img(src=app.get_asset_url("logo.png"), style={"height": "75%"})

## Components: Plot 1
plot1 = html.Div(
    dbc.Container(
        [  # here, I have created a container to stack plot and dropdown
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dcc.Dropdown(
                                id="category-widget",  # ID for dropdown
                                value="Furniture",
                                options=[
                                    {"label": category, "value": category}
                                    for category in sorted(
                                        df_plot1["Category"].unique()
                                    )
                                ],
                                placeholder="Select a category",
                            )
                        ],
                        style={
                            "width": "10",
                            "font-weight": "bold",
                            "padding-left": "550px",
                        },
                    ),  # styling for dropdown
                    dbc.Row(
                        html.Iframe(
                            id="barchart",  # ID for bar chart
                            style={
                                "border-width": "0",
                                "width": "100%",
                                "height": "500px",
                            },
                        )
                    ),
                ]
            )
        ]
    ),  # styling for plot
    style={"width": "100%", "border": "12px lightgray solid"},
)  # styling for overall dashboard

## Components: Plot 2
plot2 = html.Div(
    [
        dcc.Graph(
            id="pie-graph-with-radio2", style={"width": "100%", "height": "100%"}
        ),
        dbc.Row(
            dbc.Col(
                [
                    dcc.RadioItems(
                        options=["Sales", "Profit", "Quantity"],
                        value="Sales",
                        id="metrics2",
                        inline=False,
                        inputStyle={"margin-left": "10px", "margin-right": "2px"},
                    )
                ],
                style={"width": "10", "font-weight": "bold", "padding-left": "450px"},
                width={"size": 15, "offset": 1},
            )
        ),
    ],
    style={"padding": "2rem 1rem", "border": "12px lightgray solid"},
)

## Components: Plot 3
plot3 = html.Div(
    dbc.Container(
        [  # here, I have created a container to stack plot and dropdown
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dcc.RadioItems(
                                id="type-radio",
                                options=[
                                    {"label": k, "value": k}
                                    for k in ["Sales", "Profit Margin"]
                                ],
                                value="Sales",
                                style={
                                    "width": "20",
                                    "font-weight": "bold",
                                    "padding-left": "50px",
                                },
                                inputStyle={
                                    "margin-right": "5px",
                                    "margin-left": "10px",
                                },
                            )
                        ]
                    ),  # styling for dropdown
                    dbc.Row(
                        dcc.Dropdown(
                            id="Category-dropdown",
                            options=[{"label": k, "value": k} for k in category_list],
                            value="Furniture",
                            style={
                                "width": "50%",
                                "height": "25%",
                                "font-weight": "bold",
                                "padding-left": "50px",
                            },
                        )
                    ),
                    dbc.Row(dcc.Graph(id="mkt_graph")),
                ]
            )
        ]
    ),
    style={
        "width": "100%",
        "backgroundColor": "#F9F8EB",
        "border": "11px lightgray solid",
        "height": "50",
    },
)
# styling for overall dashboard

## Components: Plot 4
states = sorted(df["State"].unique())
plot4 = html.Div(
    [
        html.H4(id="output-title", style={"fontSize": 30}),
        html.Br(),
        dcc.Dropdown(
            states,
            "New York",
            id="states-dropdown",
            style={"width": "22.5%", "font-weight": "bold", "padding-left": "100px"},
        ),
        dcc.Graph(id="bar-graph-top-items", style={"width": "100%", "height": "420px"}),
    ],
    style={
        "backgroundColor": "#f9f8eb",
        "border": "10px lightgray solid",
        "height": "100%",
    },
)

## Components: Plot 5

sales_card = dbc.Card(
    [
        dbc.CardHeader("Sales", class_name="text-center"),
        dbc.CardBody(
            [
                html.H4(
                    children="",
                    className="text-center",
                    id="sales_card",
                ),
            ]
        ),
    ]
)

profit_card = dbc.Card(
    [
        dbc.CardHeader("Profit", class_name="text-center"),
        dbc.CardBody(
            [
                html.H4(children="", className="text-center", id="profit_card"),
            ]
        ),
    ]
)
margin_card = dbc.Card(
    [
        dbc.CardHeader("Profit Margin", class_name="text-center"),
        dbc.CardBody(
            [
                html.H4(children="", className="text-center", id="margin_card"),
            ]
        ),
    ]
)

############ Map ###############


def update_data(
    ship_mode,
    segment,
    category,
    sub_category,
):
    """Appends lines for the states that have no sales for the specified combination of arguments (thus not present in the original dataframe).
        Their sales and profit are set to 0.

    Args:
        ship_mode (str, optional): Mode of shipment (can be one of First Class, Second Class, Same Day or Standard Class). Defaults to "First Class".
        segment (str, optional): . Component of a business (can be one of Consumer, Corporate or Home Office). Defaults to "Consumer".
        category (str, optional): Category of product (can be one of Furniture, Office Supplies or Technology). Defaults to "Furniture".
        sub_category (str, optional): Sub-Category of product (ex: sub-category of Furniture is Chairs). Defaults to "Bookcases".

    Returns:
        pandas dataframe: Returns a dataframe with all the rows resulting from the selected parameters for all the States. The states that
                          don't have sales for this combination of arguments have sales/profit/profit margin equal to 0.
    """

    all_states = [state for state in df_plot5["State"].unique()]

    # dataframe limited to what the user chooses with the dropdown (excluding state parameter)
    selected_df = df_plot5[
        (df_plot5["Category"] == category)
        & (df_plot5["Sub-Category"] == sub_category)
        & (df_plot5["Ship Mode"] == ship_mode)
        & (df_plot5["Segment"] == segment)
    ]

    # states that occur at least one for the chosen selection
    selected_states = [state for state in selected_df["State"].unique()]

    # list of states that are not in our selection (so no sales for this set of parameters)
    state_no_sales = list(set(all_states).difference(selected_states))

    # Appending lines for the states that have no sales for that specific selection and putting their sales and profit = 0.
    # If we dont do this, we get a map with blank states. Instead we want the states to have an outline but be considered in the chloropleth as
    # not having sales

    new_lines = pd.DataFrame(
        {
            "State": [state for state in state_no_sales],
            "Category": [category for i in range(len(state_no_sales))],
            "Sub-Category": [sub_category for i in range(len(state_no_sales))],
            "Ship Mode": [ship_mode for i in range(len(state_no_sales))],
            "Segment": [segment for i in range(len(state_no_sales))],
            "Sales": [0 for i in range(len(state_no_sales))],
            "Profit": [0 for i in range(len(state_no_sales))],
        }
    )

    updated_data = pd.concat([df_plot5, new_lines], ignore_index=True)

    # using wrangle_data() to add the `id` and `abbr` column necessary for the map plot (or else the rows for the appended lines are NaN for these columns)
    return wrangle_data(updated_data)


def plot_map(
    metric="Sales",
    state="Colorado",
    ship_mode="First Class",
    segment="Consumer",
    category="Furniture",
    sub_category="Bookcases",
):
    """_summary_

    Args:
        metric (str): Variable according to which we wish to show the chloropleth map (one of either Sales, Profit or Profit Margin)
        ship_mode (str, optional): Mode of shipment (can be one of First Class, Second Class, Same Day or Standard Class). Defaults to "First Class".
        segment (str, optional): . Component of a business (can be one of Consumer, Corporate or Home Office). Defaults to "Consumer".
        category (str, optional): Category of product (can be one of Furniture, Office Supplies or Technology). Defaults to "Furniture".
        sub_category (str, optional): Sub-Category of product (ex: sub-category of Furniture is Chairs). Defaults to "Bookcases".

    Returns:
        altair chart: A map of the United States where each state is colored in proportion to the metric chosen.
    """

    # https://stackoverflow.com/questions/66892810/using-transform-lookup-for-an-altair-choropleth-figure
    states = alt.topo_feature(data.us_10m.url, feature="states")

    # Formatting for tooltip and chloropleth legend (depends on whether we have sales/proft ($) or margin (%))
    if metric == "Profit_Margin":
        metric_format = ".0%"

    else:
        metric_format = "$.0f"

    # Formatting for color scheme and mid-range of legend
    if (metric == "Profit_Margin") or (metric == "Profit"):
        scale_metric = alt.Scale(scheme="redblue", domainMid=0)
    else:
        scale_metric = alt.Scale(scheme="blues")

    updated_df = update_data(
        ship_mode=ship_mode,
        segment=segment,
        category=category,
        sub_category=sub_category,
    )

    chart = (
        alt.Chart(states, background="#F9F8EB")
        .mark_geoshape(stroke="black")
        .encode(
            stroke=alt.condition(
                alt.datum.State == state, alt.value("black"), alt.value("black")
            ),
            strokeWidth=alt.condition(
                alt.datum.State == state, alt.value(4), alt.value(0.5)
            ),
            color=alt.condition(
                f"datum.{metric} != 0",
                f"{metric}:Q",
                alt.value("white"),
                legend=alt.Legend(format=metric_format),
                scale=scale_metric,
            ),
            # color=alt.Color(
            #     f"{metric}:Q",
            #     legend=alt.Legend(format=metric_format),
            #     scale=alt.Scale(scheme="redblue"),
            # ),
            tooltip=[
                alt.Tooltip("State:N"),
                alt.Tooltip(f"{metric}:Q", format=metric_format),
            ],
        )
        .transform_lookup(
            lookup="id",
            from_=alt.LookupData(
                updated_df[
                    (updated_df["Category"] == category)
                    & (updated_df["Sub-Category"] == sub_category)
                    & (updated_df["Ship Mode"] == ship_mode)
                    & (updated_df["Segment"] == segment)
                ],
                "id",
                [metric, "State"],
            ),
        )
        .properties(width=500, height=300)
        .project("albersUsa")
    )

    return chart.to_html()


plot5 = dbc.Container(
    [
        # Display sales and profit info at top of map
        dbc.Row(
            [
                dbc.Col(sales_card, width=4),
                dbc.Col(profit_card, width=4),
                dbc.Col(margin_card, width=4),
            ]
        ),
        # Displays the map
        dbc.Row(
            [
                dbc.Col(
                    html.Iframe(
                        srcDoc=plot_map(),
                        id="map",
                        style={"width": "100%", "height": "400px"},
                    ),
                    width=10,
                ),
            ]
        ),
        # Radio button for the map, to select if we want to see sales, profit or profit margin
        dbc.Row(
            dbc.Col(
                dcc.RadioItems(
                    id="radiobutton_map",
                    options=[
                        {"label": "Profit", "value": "Profit"},
                        {"label": "Sales", "value": "Sales"},
                        {"label": "Profit Margin", "value": "Profit_Margin"},
                    ],
                    value="Profit",
                    inline=True,
                    inputStyle={"margin-right": "5px", "margin-left": "20px"},
                )
            )
        ),
        # Displays the 5 dropdowns
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        placeholder="Select a state",
                        id="dropdown_state",
                        value="Colorado",  # REQUIRED to show the plot on the first page load
                        options=[
                            {"label": state, "value": state}
                            for state in sorted(df_plot5["State"].unique())
                        ],
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        placeholder="Select a shipment mode",
                        id="dropdown_ship_mode",
                        value="First Class",  # REQUIRED to show the plot on the first page load
                        options=[
                            {"label": mode, "value": mode}
                            for mode in sorted(df_plot5["Ship Mode"].unique())
                        ],
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        placeholder="Select a segment",
                        id="dropdown_segment",
                        value="Consumer",  # REQUIRED to show the plot on the first page load
                        options=[
                            {"label": seg, "value": seg}
                            for seg in sorted(df_plot5["Segment"].unique())
                        ],
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        placeholder="Select a category",
                        id="dropdown_category",
                        value="Furniture",  # REQUIRED to show the plot on the first page load
                        options=[
                            {"label": cat, "value": cat}
                            for cat in sorted(df_plot5["Category"].unique())
                        ],
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        placeholder="Select a sub-category",
                        id="dropdown_sub_category",
                        options=[],
                        value="Bookcases",  # REQUIRED to show the plot on the first page load
                    )
                ),
            ]
        ),
    ],
    style={"width": "100%", "border": "12px lightgray solid"},
)

## Components: Plot 6
subcat = sorted(df["Sub-Category"].unique())
plot6 = html.Div(
    [
        html.Div(id="output-title6", style={"fontSize": 30}),
        html.Br(),
        dcc.Dropdown(
            subcat, "Binders", id="subcat-dropdown", style={"width": 200, "height": 20}
        ),
        html.Br(),
        dcc.Graph(
            id="bar-graph-top-states", style={"width": "100%", "height": "410px"}
        ),
    ],
    style={
        "border": "1px lightgray solid",
        "border": "10px lightgray solid",
        "height": "100%",
    },
)

##############################
########## Layout  ###########
##############################
app.layout = html.Div(
    [
        dbc.Row(dbc.Col(logo)),
        dbc.Row(
            [
                dbc.Col([dbc.Col(plot1)], width=4),
                dbc.Col([dbc.Col(plot4)], width=4),
                dbc.Col([dbc.Col(plot6)], width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dbc.Row(dbc.Col(plot2)), dbc.Row(dbc.Col(plot3))], width=4),
                dbc.Col([dbc.Row(dbc.Col(plot5))], width=8),
            ]
        ),
    ],
    style={"backgroundColor": "#f9f8eb"},
)

##############################
######## Callbacks ###########
##############################

## Callback: Plot 1
@app.callback(  # dash decorator function
    Output("barchart", "srcDoc"), Input("category-widget", "value")
)
def my_plot(category):  # callback function

    sub_categories = [
        sub_cat
        for sub_cat in df_plot1[df_plot1["Category"] == category][
            "Sub-Category"
        ].unique()
    ]
    sales = [sales for sales in df_plot1[df_plot1["Category"] == category]["Sales"]]
    profit = [sales for sales in df_plot1[df_plot1["Category"] == category]["Profit"]]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=sub_categories, y=sales, name="Sales", marker_color="red"))
    fig.add_trace(
        go.Bar(x=sub_categories, y=profit, name="Profit", marker_color="midnightblue")
    )

    fig.update_layout(
        barmode="group",
        xaxis_tickangle=0,
        title="Overall Sales & Profit by Category",
        title_font_size=25,
        title_x=0.339,
        title_y=0.96,
        xaxis_title="Sub-categories",
        margin=dict(l=20, r=20, t=45, b=9),
        plot_bgcolor="#f9f8eb",
        paper_bgcolor="#f9f8eb",
        legend=dict(y=0.6, font_size=25),
        xaxis=dict(tickfont=dict(size=12)),
        hovermode="x unified",
    )  # styling for plot
    fig.update_yaxes(tickprefix="<b>", ticksuffix="</b><br>")
    fig.update_xaxes(tickprefix="<b>", ticksuffix="</b><br>")

    return fig.to_html()


## Callback: Plot 2
@app.callback(Output("pie-graph-with-radio2", "figure"), Input("metrics2", "value"))
def update_figure(selected_metrics):
    fig = px.pie(
        df,
        values=selected_metrics,
        names="Segment",
        color="Segment",
        color_discrete_map={
            "Consumer": "red",
            "Corporate": "midnightblue",
            "Home Office": "lightgray",
        },
        title="Metrics Proportion by Segment",
    )

    fig.update_layout(
        transition_duration=500,
        legend=dict(y=0.5, font_size=25),
        margin=dict(l=20, r=0, t=35, b=0),
        title_font_size=25,
        plot_bgcolor="#f9f8eb",
        paper_bgcolor="#f9f8eb",
    )

    return fig


## Callback: Plot 3
@app.callback(  # Columns 2m_temp_prod, or....
    Output("mkt_graph", "figure"),
    [
        Input("Category-dropdown", "value"),
        Input("type-radio", "value"),
    ],
)
def make_graph(levels, type_graph):
    if type_graph != "Profit Margin":
        group_by_profit = df_plot3.groupby(
            ["Sub-Category", "Category", "Discount_Status"], as_index=False
        )[["Sales", "Profit Margin", "Discount"]].sum()
    else:
        group_by_profit = df_plot3.groupby(
            ["Sub-Category", "Category", "Discount_Status"], as_index=False
        )[["Sales", "Profit Margin"]].mean()
        # group_by_profit["Profit Margin"] = group_by_profit["Profit Margin"]*100
    title_all = "All Categories"
    if levels != "All":
        title_all = levels
        group_by_profit = group_by_profit[group_by_profit["Category"] == levels]
    if type_graph != "Profit Margin":
        fig = px.bar(
            group_by_profit,
            x="Sub-Category",
            y="Sales",
            color="Discount_Status",
            barmode="group",
            height=1000,
            color_discrete_sequence=["Red", "midnightblue"],
        )
        fig.update_layout(
            title={
                "text": "<b>Sales by " + str(title_all) + "<b>",
                "y": 1,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            font_family="Calibri",
            font_size=20,
            font_color="black",
            #            title_font_family="Times New Roman",
            title_font_color="black",
            legend_title_font_color="black",
            legend_title_font_size=20,
            legend_title="Discount Applied?",
            plot_bgcolor="#F9F8EB",
            paper_bgcolor="#F9F8EB",
            title_font_size=25,
            xaxis=dict(tickfont=dict(size=30)),
            yaxis=dict(tickfont=dict(size=30)),
            margin=dict(l=20, r=20, t=60, b=10),
        )
        fig.update_xaxes()
    else:
        fig = px.bar(
            group_by_profit,
            x="Sub-Category",
            y="Profit Margin",
            color="Discount_Status",
            barmode="group",
            height=1000,
            color_discrete_sequence=["Red", "midnightblue"],
        )
        fig.update_layout(
            title={
                "text": "<b>Profit/Loss by " + str(title_all) + "<b>",
                "y": 1,
                "x": 0.5,
                "xanchor": "center",
                "yanchor": "top",
            },
            font_family="Calibri",
            font_size=20,
            font_color="black",
            #            title_font_family="Times New Roman",
            title_font_color="black",
            legend_title_font_color="black",
            legend_title_font_size=28,
            legend_title="Discount Applied?",
            paper_bgcolor="#F9F8EB",
        )
        fig.update_xaxes(title={"text": str(levels)})
        fig.update_yaxes(tickformat=",.0%", title=None)
    fig.update_layout(
        plot_bgcolor="#F9F8EB",
        title_font_size=25,
        paper_bgcolor="#F9F8EB",
        xaxis=dict(tickfont=dict(size=30)),
        yaxis=dict(tickfont=dict(size=30)),
        margin=dict(l=20, r=20, t=60, b=10),
        legend=dict(
            y=1,
            font_size=20,
            # traceorder="reversed",
            #
            font=dict(color="black"),
        ),
    )
    return fig


## Callback: Plot 4
@app.callback(
    Output("output-title", "children"),
    Output("bar-graph-top-items", "figure"),
    Input("states-dropdown", "value"),
)
def update_figure(selected_state):
    filtered_df = df[["State", "Sub-Category", "Quantity"]]
    filtered_df = (
        filtered_df[filtered_df["State"] == selected_state]
        .groupby("Sub-Category")
        .sum()
    )
    filtered_df = filtered_df.sort_values(by="Quantity", ascending=False)[
        0:5
    ].reset_index()

    fig = px.bar(filtered_df, x="Sub-Category", y="Quantity")
    fig.update_traces(marker_color="midnightblue").update_layout(
        margin=dict(l=20, r=20, t=40, b=9),
        plot_bgcolor="#f9f8eb",
        paper_bgcolor="#f9f8eb",
    ).update_layout(transition_duration=500)

    return f"Top 5 Items Sold in: {selected_state}", fig


## Callback: Plot 5
# In order to have a chained callback for category and sub-category
all_category = {
    "Furniture": ["Bookcases", "Chairs", "Furnishings", "Tables"],
    "Office Supplies": [
        "Appliances",
        "Art",
        "Binders",
        "Envelopes",
        "Fasteners",
        "Labels",
        "Paper",
        "Storage",
        "Supplies",
    ],
    "Technology": ["Accesories", "Copiers", "Machines", "Phones"],
}

# Makes sure that options in sub-category are those that make up category (ex: cant have chairs(sub-category) as a choice when you choose technology as the category)
@app.callback(
    Output("dropdown_sub_category", "options"), Input("dropdown_category", "value")
)
def set_subcategory_options(selected_category):
    return [{"label": sub, "value": sub} for sub in all_category[selected_category]]


# Updates cards
@app.callback(
    [
        Output("sales_card", "children"),
        Output("profit_card", "children"),
        Output("margin_card", "children"),
    ],
    [
        Input("dropdown_ship_mode", "value"),
        Input("dropdown_segment", "value"),
        Input("dropdown_state", "value"),
        Input("dropdown_category", "value"),
        Input("dropdown_sub_category", "value"),
    ],
)
def update_cards(ship_mode, segment, state, category, sub_category):
    updated_df = df_plot5[
        (df_plot5["Category"] == category)
        & (df_plot5["Sub-Category"] == sub_category)
        & (df_plot5["State"] == state)
        & (df_plot5["Ship Mode"] == ship_mode)
        & (df_plot5["Segment"] == segment)
    ][["Sales", "Profit", "Profit_Margin"]]

    sales = updated_df["Sales"]
    profit = updated_df["Profit"]
    margin = (updated_df["Profit_Margin"]) * 100

    if len(sales) != 0:
        sales_formatted = sales.map("${:,.2f}".format)
        profit_formatted = profit.map("${:,.2f}".format)
        margin_formatted = margin.map("{:,.2f}%".format)

    else:
        sales_formatted = "-"
        profit_formatted = "-"
        margin_formatted = "-"

    return sales_formatted, profit_formatted, margin_formatted


# Updates map


@app.callback(
    Output("map", "srcDoc"),
    [
        Input("radiobutton_map", "value"),
        Input("dropdown_state", "value"),
        Input("dropdown_ship_mode", "value"),
        Input("dropdown_segment", "value"),
        Input("dropdown_category", "value"),
        Input("dropdown_sub_category", "value"),
    ],
)
def update_map(metric, state, ship_mode, segment, category, sub_category):
    return plot_map(metric, state, ship_mode, segment, category, sub_category)


## Callback: Plot 6
@app.callback(
    Output("output-title6", "children"),
    Output("bar-graph-top-states", "figure"),
    Input("subcat-dropdown", "value"),
)
def update_figure(selected_item):
    filtered_df = df[["State", "Sub-Category", "Quantity"]]
    filtered_df = (
        filtered_df[filtered_df["Sub-Category"] == selected_item].groupby("State").sum()
    )
    filtered_df = filtered_df.sort_values(by="Quantity", ascending=False)[
        0:5
    ].reset_index()

    fig = px.bar(filtered_df, x="State", y="Quantity")
    fig.update_traces(marker_color="midnightblue").update_layout(
        {"plot_bgcolor": "#f9f8eb", "paper_bgcolor": "#f9f8eb"}
    ).update_layout(
        transition_duration=500, margin=dict(l=20, r=20, t=40, b=9)
    ).update_yaxes(
        visible=False
    )

    return f"Top 5 States With Highest Quantity Sold in: {selected_item} ", fig


# Run server
if __name__ == "__main__":
    app.run_server(port=8052, debug=True)
