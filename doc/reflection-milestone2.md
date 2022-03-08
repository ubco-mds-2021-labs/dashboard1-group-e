# Reflection

## What we have implemented

We split the tasks according to the different plots. Everybody was working on at least one plot (Evelyn worked on two). This is a short description of what we have implemented so far:

- Justine implemented the map plot (which includes the radio buttons to select which metric to display on the map, the five dropdowns for the segment to analyze and the 3 cards above it to display the sales, profit and profit margin). There is a chained callback between the category and sub-category dropdown. When the user selects a state in the dropdown, the said state is outlined on the map. This allows the user to see how the selected state performs versus all the other states for the chosen metric (chosen using the radio button). The user can also hover over the states on the map and see the chosen metric displayed.  

- Evelyn implemented a pie chart to display the proportion of metrics (sales, profit, or quantity) by customer segments. This chart will help the target audience to know the performance of each customer segment and which to improve upon. The different customer segments (consumer, corporate, and home office) are represented by the different colors in the bar chart. Whereas the metrics can be specified by selecting it through the radio button at the bottom of the chart. She also added a bar chart to rank the top 5 items sold in a particular state. The user can select which states they want to view by selecting it through the dropdown menu at the bottom of the map. 

- Val implemented a bar plot to answer whether or not discount has an impact on the bottom line of our store. This plot focuses on answering our research question based on the effect of discount in terms of sales and profit. This plot displays the sales figures as well as the profit margin for all categories as well as sub-categories of products.There’s a radio button that enables the user to filter between Sales and Profit Margin as well as a dropdown to switch between different Categories of products. If the user wants to view the metrics of all the categories, there’s a dropdown option to view it for all of the subcategories.

- Mehul implemented a bar plot that displays the sales and profit of the store with respect to each sub-category for a chosen category. He added a dropdown which allows the user to select a category (furniture, office supplies, and technology). The bars for profit and sales are differentiated by red and blue colors. The user can hover around the plot to see the sales and profit values. 

## What is not yet implemented (and we are hoping to implement for milestone 4)

- Callbacks to connect all the graphs together (i.e., when a user selects a state from the map, all the other graphs should be updated to reflect data of that particular state. Currently only the 3 cards above the map are linked and the rest of the plots show the sum for all the states).

- The sizing of the graph inside the dashboard is still a work in progress. Currently our dashboard is bigger than it should be. Also, we want to make the map graph take up all the remaining space. 

- The user can also click on the map to select which state they want to view and this will also change the rest of the dashboards. 

- Make a chained callback for each dropdown below the map plot so that only the combinations with a row in the dataset are offered as options.

- Adding the option for the user to choose only a category (no sub-category) and the sum of the sales and profit for all sub-categories within this category is shown.

- Adding the option for the user  to select multiple options for each dropdown and the results show an aggregate of the metrics (sales/profit) for this selection. 

- Make the plots more uniform (ex: same font for titles)

- Adding a description for the dashboard and making it more obvious that the dropdowns below the map will eventually be global controls

-  Making sure the plots automatically resize to adjust to the size of the screen (right now we need to be in 50% zoom to have an appropriate display)

## What we know is not working

- Callbacks to connect all the graphs together (i.e., when a user selects a state from the map, all the other graphs should be updated to reflect data of that particular state. Currently only the 3 cards above the map are linked and the rest of the plots show the sum for all the states).

## Limitations (what we can't improve but wished we could)

The size of our dataset. Not all states have a value for sales and profit for every possible combination of variables (`segment`, `ship_mode`, `category`, `sub-category`). This makes our visualizations less insightful.

## Future improvements (after milestone 4)

It would have been interesting to have a section (maybe on a different tab) with a predictive model that would allow the user to predict the number of sales and profit for a given combination of variables. Because of the size of the dataset (too small) and the lack of time, we were not able to implement this. 

