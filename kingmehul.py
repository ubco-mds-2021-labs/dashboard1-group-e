import dash
from dash import Dash, dcc, html, Input, Output
from vega_datasets import data

# from asyncio.windows_events import NULL
# from tkinter import ALL
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import altair as alt
import base64

alt.data_transformers.disable_max_rows()
# Read data
df = pd.read_csv("data/Superstore.csv")

df = df.drop_duplicates()
df = df.drop(df[df.Profit == -6599.9780].index)


###################################
######### Wrangling ###############
###################################


######### Data wrangling: Plot 1
df_plot1 = df.groupby(["State", "Category", "Sub-Category"], as_index=False)[
    ["Sales", "Profit"]
].sum()

######### Data wrangling: Plot 2
states = sorted(df["State"].unique())
######### Data wrangling: Plot 3
subcat = sorted(df["Sub-Category"].unique())
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

######### Data wrangling: Plot 6

#####################################
############ App ####################
#####################################

# Create instance of app
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
server = app.server


######################################
########### Components ###############
######################################


########## Component logo
logo = html.Img(src=app.get_asset_url("logo.png"), style={"height": "100%"})

########## Component Plot 1
plot1 = html.Div(
    dbc.Container(
        [  # here, I have created a container to stack plot and dropdown
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
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
                                        style={
                                            "height": "45px",
                                            "width": "100%",
                                            "font-size": "120%",
                                        },
                                    )
                                ]
                            ),
                        ],
                        style={
                            "width": "10",
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
    style={
        "width": "100%",
        "border": "6px lightgray solid",
        "backgroundColor": "#f9f8eb",
    },
)  # styling for overall dashboard

########## Component Plot 2
plot2 = dbc.Container(
    [
        dbc.Row(
            dcc.Graph(
                id="pie-graph-with-radio2", style={"width": "100%", "height": "100%"}
            )
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
                        style={
                            "font-size": "150%",
                        },
                    )
                ],
                # style={"width": "10", "font-weight": "bold", "padding-left": "450px"},
                width={"size": 15, "offset": 1},
            ),
            justify="end",
        ),
    ],
    style={"padding": "2rem 1rem", "border": "6px lightgray solid"},
)

########## Component Plot 3
plot3 = dbc.Container(
    [
        dbc.Row(
            html.H4(
                id="output-title",
                style={"color": "#36465D", "fontSize": 25, "fontFamily": "Verdana"},
            )
        ),
        dbc.Row(dcc.Graph(id="bar-graph-top-items")),
    ],
    style={
        "backgroundColor": "#f9f8eb",
        "border": "6px lightgray solid",
        "height": "100%",
    },
)

########## Component Plot 4
plot4 = html.Div(
    dbc.Container(
        [  # here, I have created a container to stack plot and dropdown
            dbc.Col(
                [
                    dbc.Row(
                        [
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="category-widget4",  # ID for dropdown
                                        value="Furniture",
                                        options=[
                                            {"label": category, "value": category}
                                            for category in sorted(
                                                df_plot1["Category"].unique()
                                            )
                                        ],
                                        placeholder="Select a category",
                                    )
                                ]
                            ),
                            dbc.Col(
                                [
                                    dcc.Dropdown(
                                        id="state-widget4",
                                        value="New York",
                                        options=[
                                            {"label": state, "value": state}
                                            for state in sorted(
                                                df_plot1["State"].unique()
                                            )
                                        ],
                                        placeholder="Select a state",
                                    )
                                ]
                            ),
                        ],
                        style={
                            "width": "10",
                            "font-weight": "bold",
                            "padding-left": "550px",
                        },
                    ),  # styling for dropdown
                    dbc.Row(
                        html.Iframe(
                            id="barchart4",  # ID for bar chart
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
    style={
        "width": "100%",
        "border": "6px lightgray solid",
        "backgroundColor": "#f9f8eb",
    },
)  # styling for overall dashboard


########## Component Plot 5
sales_card = dbc.Card(
    [
        dbc.CardHeader("Sales", class_name="text-center", style={"font-size": "160%"}),
        dbc.CardBody(
            [
                html.H3(
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
        dbc.CardHeader("Profit", class_name="text-center", style={"font-size": "160%"}),
        dbc.CardBody(
            [
                html.H3(children="", className="text-center", id="profit_card"),
            ]
        ),
    ]
)
margin_card = dbc.Card(
    [
        dbc.CardHeader(
            "Profit Margin", class_name="text-center", style={"font-size": "160%"}
        ),
        dbc.CardBody(
            [
                html.H3(children="", className="text-center", id="margin_card"),
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
        mid_scale_color = 0
        color_theme = "redblue"
    else:
        mid_scale_color = 0
        color_theme = "blues"

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
                legend=alt.Legend(
                    format=metric_format, orient="bottom-left", direction="horizontal"
                ),
                scale=alt.Scale(scheme=color_theme, domainMid=mid_scale_color),
            ),
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
        .properties(width=760, height=760)
        .project("albersUsa")
        .configure_view(strokeWidth=0)
        .configure_legend(
            gradientLength=250, gradientThickness=20, titleFontSize=20, labelFontSize=18
        )
    )

    return chart.to_html()


plot5 = html.Div(
    [
        dbc.Row([dbc.Col(sales_card), dbc.Col(profit_card), dbc.Col(margin_card)]),
        dbc.Row(
            dbc.Col(
                html.Div(
                    html.Iframe(
                        srcDoc=plot_map(),
                        id="map",
                        style={"width": "100%", "height": "800px", "border": "0"},
                    ),
                ),
                width={"offset": 3},
            ),
        ),
        # Radio button for the map, to select if we want to see sales, profit or profit margin
        dbc.Row(
            dbc.Col(
                [
                    dcc.RadioItems(
                        id="radiobutton_map",
                        options=[
                            {"label": "Profit", "value": "Profit"},
                            {"label": "Sales", "value": "Sales"},
                            {"label": "Profit Margin", "value": "Profit_Margin"},
                        ],
                        style={
                            "font-size": "150%",
                        },
                        value="Profit",
                        inline=True,
                        inputStyle={"margin-right": "5px", "margin-left": "20px"},
                    ),
                    html.Br(),
                    html.H1(),
                    html.Br(),
                ],
                width={"offset": 9},
            )
        ),
        # Displays the 5 dropdowns
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H4("Shipment mode"),
                        dcc.Dropdown(
                            placeholder="Select a shipment mode",
                            id="dropdown_ship_mode",
                            value="First Class",  # REQUIRED to show the plot on the first page load
                            options=[
                                {"label": mode, "value": mode}
                                for mode in sorted(df_plot5["Ship Mode"].unique())
                            ],
                            style={
                                "height": "45px",
                                "width": "100%",
                                "font-size": "120%",
                            },
                        ),
                        html.Br(),
                    ],
                ),
                dbc.Col(
                    [
                        html.H4("Segment"),
                        dcc.Dropdown(
                            placeholder="Select a segment",
                            id="dropdown_segment",
                            value="Consumer",  # REQUIRED to show the plot on the first page load
                            options=[
                                {"label": seg, "value": seg}
                                for seg in sorted(df_plot5["Segment"].unique())
                            ],
                            style={
                                "height": "45px",
                                "width": "100%",
                                "font-size": "120%",
                            },
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.H4("Category"),
                        dcc.Dropdown(
                            placeholder="Select a category",
                            id="dropdown_category",
                            value="Furniture",  # REQUIRED to show the plot on the first page load
                            options=[
                                {"label": cat, "value": cat}
                                for cat in sorted(df_plot5["Category"].unique())
                            ],
                            style={
                                "height": "45px",
                                "width": "100%",
                                "font-size": "120%",
                            },
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        html.H4("Sub-category"),
                        dcc.Dropdown(
                            placeholder="Select a sub-category",
                            id="dropdown_sub_category",
                            options=[],
                            value="Bookcases",
                            style={
                                "height": "45px",
                                "width": "100%",
                                "font-size": "120%",
                            },
                        ),
                    ]
                ),
            ]
        ),
    ],
    style={"width": "100%", "border": "6px lightgray solid"},
)

collapse = html.Div(
    [
        dbc.Button(
            "Learn more",
            id="collapse-button",
            className="mb-3",
            outline=False,
            style={
                "margin-top": "10px",
                "width": "150px",
                "background-color": "white",
                "color": "steelblue",
            },
        ),
    ]
)

sidebar = dbc.Col(
    [
        dbc.Row(
            [
                dbc.Col(logo),
                html.Br(),
                html.H1(),
                html.Br(),
                html.H1(),
                html.Br(),
                html.H1(),
                html.Br(),
            ]
        ),
        dbc.Row(
            [
                html.H3(
                    "Tracking sales and profit metrics across different states for the American Superstore market chain has never been easier!"
                ),
                html.Br(),
                html.H1(),
                html.H4(),
                html.H3(
                    "Select a state below and see how the sales, profit and profit margin change for different product lines."
                ),
                html.Br(),
                html.H1(),
                html.Br(),
                html.H1(),
                html.Br(),
                html.H1(),
                html.Br(),
                html.H1(),
                html.Br(),
                html.H3("Select a state"),
                dcc.Dropdown(
                    placeholder="Select a state",
                    id="dropdown_state",
                    value="Colorado",  # REQUIRED to show the plot on the first page load
                    options=[
                        {"label": state, "value": state}
                        for state in sorted(df_plot5["State"].unique())
                    ],
                    style={
                        "height": "45px",
                        "width": "100%",
                        "font-size": "120%",
                    },
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("Introblabla"),
                        dbc.Collapse(
                            html.P(
                                """
                        This dashboard is helping you understand x, y, and z, 
                        which are really important because a, b, c.
                        Start using the dashboard by clicking on 1, 2, 3
                        and pulling i, ii, and iii.""",
                                style={"color": "white", "width": "50%"},
                            ),
                            id="collapse",
                        ),
                    ],
                    md=10,
                ),
                dbc.Col([collapse]),
            ],
        ),
    ],
    md=2,
    style={
        "width": "100%",
        "border": "6px lightgray solid",
        "background-color": "#e6e6e6",
        "padding": 15,
        "border-radius": 3,
    },
)


##############################
########## Layout  ###########
##############################


app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [dbc.Row([sidebar], className="g-0", style={"height": "100%"})],
                    width=2,
                ),
                dbc.Col(
                    [
                        dbc.Container(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                dbc.Row(
                                                    [plot5],
                                                    className="g-0",
                                                    style={"height": "100%"},
                                                )
                                            ]
                                        ),
                                        dbc.Col(
                                            [
                                                dbc.Row(
                                                    [plot1],
                                                    className="g-0",
                                                    style={"height": "50%"},
                                                ),
                                                dbc.Row(
                                                    [plot2],
                                                    className="g-0",
                                                    style={"height": "50%"},
                                                ),
                                            ],
                                            width=4,
                                        ),
                                    ],
                                    className="g-0",
                                ),
                                dbc.Row(
                                    [dbc.Col([plot4]), dbc.Col([plot3], width=4)],
                                    className="g-0",
                                ),
                            ],
                            style={"width": "100%", "backgroundColor": "#f9f8eb"},
                            fluid=True,
                        )
                    ],
                    width=10,
                ),
            ],
            className="g-0",
        )
    ],
    style={"width": "100%", "backgroundColor": "#f9f8eb"},
    fluid=True,
)

# , style={"width": "100%", "backgroundColor": "#f9f8eb"}, fluid=True

##############################
########## Callback  #########
##############################

## Callback for learn more button
# @app.callback(
#     Output("collapse", "is_open"),
#     Input("collapse-button", "n_clicks"),
#     State("collapse", "is_open"),
# )
# def toggle_collapse(n, is_open):
#     if n:
#         return not is_open
#     return is_open


## Callback: Plot 1
@app.callback(  # dash decorator function
    Output("barchart", "srcDoc"),
    [Input("dropdown_state", "value"), Input("category-widget", "value")],
)
def my_plot(state, category):  # callback function

    sub_categories = [
        sub_cat
        for sub_cat in df_plot1[
            (df_plot1["State"] == state) & (df_plot1["Category"] == category)
        ]["Sub-Category"].unique()
    ]
    sales = [
        sales
        for sales in df_plot1[
            (df_plot1["State"] == state) & (df_plot1["Category"] == category)
        ]["Sales"]
    ]
    profit = [
        sales
        for sales in df_plot1[
            (df_plot1["State"] == state) & (df_plot1["Category"] == category)
        ]["Profit"]
    ]

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
        xaxis=dict(tickfont=dict(size=16)),
        yaxis=dict(tickfont=dict(size=16)),
        hovermode="x",
        hoverlabel=dict(
            font_size=20,
        ),
        yaxis_tickformat="$.0f",
    )  # styling for plot
    fig.update_yaxes(tickprefix="<b>", ticksuffix="</b><br>")
    fig.update_xaxes(tickprefix="<b>", ticksuffix="</b><br>", title_font_size=22)

    if category == "Office Supplies":
        fig.update_xaxes(tickprefix="<b>", ticksuffix="</b><br>", tickangle=20)

    return fig.to_html()


## Callback: Plot 2
@app.callback(
    Output("pie-graph-with-radio2", "figure"),
    Input("metrics2", "value"),
    Input("dropdown_state", "value"),
)
def update_figure(selected_metrics, selected_state):

    df_plot2 = df[df["State"] == selected_state]

    fig = px.pie(
        df_plot2,
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
    fig.update_traces(textfont_size=20)
    fig.update_layout(
        transition_duration=500,
        legend=dict(y=0.5, font_size=25),
        margin=dict(l=20, r=0, t=35, b=0),
        title_font_size=25,
        plot_bgcolor="#f9f8eb",
        paper_bgcolor="#f9f8eb",
        hovermode="x",
        hoverlabel=dict(font_size=20),
    )

    return fig


## Callback: Plot 3
@app.callback(
    Output("output-title", "children"),
    Output("bar-graph-top-items", "figure"),
    Input("dropdown_state", "value"),
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
    fig.update_xaxes(tickprefix="<b>", ticksuffix="</b><br>", title_font_size=22)
    fig.update_yaxes(tickprefix="<b>", ticksuffix="</b><br>", title_font_size=22)
    fig.update_traces(marker_color="midnightblue").update_layout(
        margin=dict(l=20, r=20, t=40, b=9),
        plot_bgcolor="#f9f8eb",
        paper_bgcolor="#f9f8eb",
        xaxis=dict(tickfont=dict(size=16)),
        yaxis=dict(tickfont=dict(size=16)),
        xaxis_title=None,
        hovermode="x",
        hoverlabel=dict(font_size=20),
    )

    return f"Top 5 Items Sold in: {selected_state}", fig


## Callback: Plot 4
@app.callback(  # dash decorator function
    Output("barchart4", "srcDoc"),
    [Input("state-widget4", "value"), Input("category-widget4", "value")],
)
def my_plot(state, category):  # callback function

    sub_categories = [
        sub_cat
        for sub_cat in df_plot1[
            (df_plot1["State"] == state) & (df_plot1["Category"] == category)
        ]["Sub-Category"].unique()
    ]
    sales = [
        sales
        for sales in df_plot1[
            (df_plot1["State"] == state) & (df_plot1["Category"] == category)
        ]["Sales"]
    ]
    profit = [
        sales
        for sales in df_plot1[
            (df_plot1["State"] == state) & (df_plot1["Category"] == category)
        ]["Profit"]
    ]

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
        sales_formatted = "NA"
        profit_formatted = "NA"
        margin_formatted = "NA"

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


# Run server
if __name__ == "__main__":
    app.run_server(port=8052, debug=True)
