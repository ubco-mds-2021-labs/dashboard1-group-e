from asyncio.windows_events import NULL
from tkinter import ALL
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

# Wrangling data (made it a function, because have to rewrangle data when doing map --> see update_data() function)
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


df = wrangle_data(df)

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

    all_states = [state for state in df["State"].unique()]

    # dataframe limited to what the user chooses with the dropdown (excluding state parameter)
    selected_df = df[
        (df["Category"] == category)
        & (df["Sub-Category"] == sub_category)
        & (df["Ship Mode"] == ship_mode)
        & (df["Segment"] == segment)
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

    updated_data = pd.concat([df, new_lines], ignore_index=True)

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
        mid_scale_color = NULL
        color_theme = "blues"

    updated_df = update_data(
        ship_mode=ship_mode,
        segment=segment,
        category=category,
        sub_category=sub_category,
    )

    chart = (
        alt.Chart(states)
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
                scale=alt.Scale(scheme=color_theme, domainMid=mid_scale_color),
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
                            for state in sorted(df["State"].unique())
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
                            for mode in sorted(df["Ship Mode"].unique())
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
                            for seg in sorted(df["Segment"].unique())
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
                            for cat in sorted(df["Category"].unique())
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
    updated_df = df[
        (df["Category"] == category)
        & (df["Sub-Category"] == sub_category)
        & (df["State"] == state)
        & (df["Ship Mode"] == ship_mode)
        & (df["Segment"] == segment)
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


if __name__ == "__main__":
    app.run_server(debug=True)
