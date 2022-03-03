from unittest import skip
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import pandas as pd
import dash_bootstrap_components as dbc

###############################################
########## Read and wrangle the data ##########
###############################################

# Reading in data
df = pd.read_csv("Superstore.csv")

# Removing outlier
df = df.drop(df[df.Profit == -6599.9780].index)

# To sum profit and sales over all cities, for each state
df = df.groupby(
    ["State", "Category", "Sub-Category", "Ship Mode", "Segment"], as_index=False
)[["Sales", "Profit"]].sum()
df = pd.DataFrame(df)

# Adding column for profit margin
df["Profit Margin"] = df["Profit"] / df["Sales"]

# Adding id (ansi code) to corresponding state in order to do chloropleth map

# https://stackoverflow.com/questions/66892810/using-transform-lookup-for-an-altair-choropleth-figure
states = alt.topo_feature(data.us_10m.url, feature="states")

# per https://gist.github.com/mbostock/4090848#gistcomment-2102151
ansi = pd.read_csv("https://www2.census.gov/geo/docs/reference/state.txt", sep="|")
ansi.columns = ["id", "abbr", "State", "statens"]
ansi = ansi[["id", "abbr", "State"]]

# getting the id to match with the state from the original dataframe
df = pd.merge(df, ansi, how="left", on="State")


#########################################
######## Layout Elements ################
#########################################

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

############ Cards to display info on top of map ##############
sales_card = dbc.Card(
    [
        dbc.CardHeader("Sales", class_name="text-center"),
        dbc.CardBody(
            [
                html.H4("Card title", className="text-center", id="sales_card"),
            ]
        ),
    ]
)

profit_card = dbc.Card(
    [
        dbc.CardHeader("Profit", class_name="text-center"),
        dbc.CardBody(
            [
                html.H4("Card title", className="text-center", id="profit_card"),
            ]
        ),
    ]
)
margin_card = dbc.Card(
    [
        dbc.CardHeader("Profit Margin", class_name="text-center"),
        dbc.CardBody(
            [
                html.H4("Card title", className="text-center", id="margin_card"),
            ]
        ),
    ]
)

############ Map ###############


def plot_map(metric):
    """_summary_

    Args:
        metric (str): Variable according to which we wish to show the chloropleth map (one of either Sales, Profit or Profit Margin)

    Returns:
        altair chart: A map of the United States where each state is colored in proportion to the metric chosen.
    """

    highlight = alt.selection_single(on="click", fields=["State"], empty="none")

    if metric == "Profit Margin":
        metric_format = ".0%"
    else:
        metric_format = "$.0f"
    chart = (
        alt.Chart(states)
        .mark_geoshape(stroke="black")
        .encode(
            stroke=alt.condition(highlight, alt.value("black"), alt.value("#ffffff00")),
            color=alt.Color(
                f"{metric}:Q",
                legend=alt.Legend(format=metric_format),
                scale=alt.Scale(scheme="purpleblue"),
            ),
            tooltip=[
                alt.Tooltip("State:N"),
                alt.Tooltip(f"{metric}:Q", format=metric_format),
            ],
        )
        .transform_lookup(
            lookup="id", from_=alt.LookupData(df, "id", [metric, "State"])
        )
        .properties(width=500, height=300)
        .add_selection(highlight)
        .project("albersUsa")
    )

    return chart.to_html()


##############################
######## layout ##############
##############################

app.layout = dbc.Container(
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
                        srcDoc=plot_map(metric="Sales"),
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
                        {"label": "Profit Margin", "value": "Profit Margin"},
                        {"label": "Sales", "value": "Sales"},
                    ],
                    value="Sales",
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
                        # value="Colorado",  # REQUIRED to show the plot on the first page load
                        options=[
                            {"label": state, "value": state}
                            for state in sorted(df["State"].unique())
                        ],
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        placeholder="Select a shipment mode",
                        id="dropdown_ship_mode",
                        # value="First Class",  # REQUIRED to show the plot on the first page load
                        options=[
                            {"label": mode, "value": mode}
                            for mode in sorted(df["Ship Mode"].unique())
                        ],
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        placeholder="Select a segment",
                        id="dropdown_segment",
                        # value="Consumer",  # REQUIRED to show the plot on the first page load
                        options=[
                            {"label": seg, "value": seg}
                            for seg in sorted(df["Segment"].unique())
                        ],
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        placeholder="Select a category",
                        id="dropdown_category",
                        # value="Furniture",  # REQUIRED to show the plot on the first page load
                        options=[
                            {"label": cat, "value": cat}
                            for cat in sorted(df["Category"].unique())
                        ],
                    )
                ),
                dbc.Col(
                    dcc.Dropdown(
                        placeholder="Select a sub-category",
                        id="dropdown_sub_category",
                        options=[]
                        # value="Bookcases",  # REQUIRED to show the plot on the first page load
                        # options=[
                        #     {"label": sub, "value": sub}
                        #     for sub in sorted(df["Sub-Category"].unique())
                        # ],
                    )
                ),
            ]
        ),
    ]
)

##############################
######## Callbacks ###########
##############################

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
    sales = df.loc[
        (df["Ship Mode"] == ship_mode)
        & (df["Segment"] == segment)
        & (df["State"] == state)
        & (df["Category"] == category)
        & (df["Sub-Category"] == sub_category),
        "Sales",
    ]

    profit = df.loc[
        (df["Ship Mode"] == ship_mode)
        & (df["Segment"] == segment)
        & (df["State"] == state)
        & (df["Category"] == category)
        & (df["Sub-Category"] == sub_category),
        "Profit",
    ]

    margin = df.loc[
        (df["Ship Mode"] == ship_mode)
        & (df["Segment"] == segment)
        & (df["State"] == state)
        & (df["Category"] == category)
        & (df["Sub-Category"] == sub_category),
        "Profit Margin",
    ]

    if len(sales) != 0:
        sales_formatted = "${:,.2f}".format(sales[0])
        profit_formatted = "${:,.2f}".format(profit[0])
        margin_formatted = "{:,.2f}%".format(margin[0] * 100)

    else:
        sales_formatted = "-"
        profit_formatted = "-"
        margin_formatted = "-"

    return sales_formatted, profit_formatted, margin_formatted


# Updates map
@app.callback(Output("map", "srcDoc"), Input("radiobutton_map", "value"))
def update_map(metric):
    return plot_map(metric)


if __name__ == "__main__":
    app.run_server(debug=True)
