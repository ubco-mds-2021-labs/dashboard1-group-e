from unittest import skip
from dash import Dash, html, dcc
from dash.dependencies import Input, Output
import altair as alt
from vega_datasets import data
import pandas as pd
import dash_bootstrap_components as dbc

# Read and wrangle the data

df = pd.read_csv("Superstore.csv")
df = df.drop(df[df.Profit == -6599.9780].index)

# To sum profit and sales over all cities, for each state
df = df.groupby(
    ["State", "Category", "Sub-Category", "Ship Mode", "Segment"], as_index=False
)[["Sales", "Profit"]].sum()
df = pd.DataFrame(df)


# Setup app and layout/frontend
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Cards to display info on top of map
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
##############################
########## map ###############
##############################

# https://stackoverflow.com/questions/66892810/using-transform-lookup-for-an-altair-choropleth-figure
states = alt.topo_feature(data.us_10m.url, feature="states")

# per https://gist.github.com/mbostock/4090848#gistcomment-2102151
ansi = pd.read_csv("https://www2.census.gov/geo/docs/reference/state.txt", sep="|")
ansi.columns = ["id", "abbr", "State", "statens"]
ansi = ansi[["id", "abbr", "State"]]

# getting the id to match with the state from the original dataframe
full = pd.merge(df, ansi, how="left", on="State")

highlight = alt.selection_single(on="click", fields=["State"], empty="none")


chart = (
    alt.Chart(states)
    .mark_geoshape(stroke="black")
    .encode(
        stroke=alt.condition(highlight, alt.value("black"), alt.value("#ffffff00")),
        color="Sales:Q",
        tooltip=["State:N", "Sales:Q"],
    )
    .transform_lookup(lookup="id", from_=alt.LookupData(full, "id", ["Sales", "State"]))
    .properties(width=500, height=300)
    .add_selection(highlight)
    .project("albersUsa")
)

chart


##############################
######## layout ##############
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
                        srcDoc=chart.to_html(),
                        id="map",
                        style={"border-width": "0", "width": "100%", "height": "400px"},
                    ),
                    width=12,
                )
            ]
        ),
        # Displays the 5 dropdowns
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        placeholder="Select a state",
                        id="state",
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
                        id="ship_mode",
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
                        id="segment",
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
                        id="category",
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
                        id="sub_category",
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

# Makes sure that options in sub-category are those that make up category (ex: cant have chairs(sub-category) as a choice when you choose technology as the category)
@app.callback(Output("sub_category", "options"), Input("category", "value"))
def set_subcategory_options(selected_category):
    return [{"label": sub, "value": sub} for sub in all_category[selected_category]]


@app.callback(
    [
        Output("sales_card", "children"),
        Output("profit_card", "children"),
        Output("margin_card", "children"),
    ],
    [
        Input("ship_mode", "value"),
        Input("segment", "value"),
        Input("state", "value"),
        Input("category", "value"),
        Input("sub_category", "value"),
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

    if len(sales) != 0:
        sales_formatted = "${:,.2f}".format(sales[0])
        profit_formatted = "${:,.2f}".format(profit[0])

        margin = (profit / sales) * 100
        margin_formatted = "{:,.2f}%".format(margin[0])

    else:
        sales_formatted = "-"
        profit_formatted = "-"
        margin_formatted = "-"

    return sales_formatted, profit_formatted, margin_formatted


if __name__ == "__main__":
    app.run_server(debug=True)
