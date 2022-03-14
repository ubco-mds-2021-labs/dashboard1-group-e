# Reflection

## What we have implemented

- Justine implemented the map plot (which includes the radio buttons to select which metric to display on the map, the five dropdowns for the segment to analyze and the 3 cards above it to display the sales, profit and profit margin). 

- Evelyn implemented a pie chart to display the proportion of metrics (sales, profit, or quantity) by customer segments. She also added a bar chart to rank the top 5 items sold in a particular state. The user can select which states they want to view by selecting it through the dropdown menu at the bottom of the map. 

- Val implemented a bar plot to answer whether or not discount has an impact on the bottom line of our store. There’s a radio button that enables the user to filter between Sales and Profit Margin as well as a dropdown to switch between different Categories of products. If the user wants to view the metrics of all the categories, there’s a dropdown option to view it for all of the subcategories. We ended up not adding this plot in the final layout as there was issues when combining it to the overall layout.

- Mehul implemented a bar plot that displays the sales and profit of the store with respect to each sub-category for a chosen category. He added a dropdown which allows the user to select a category (furniture, office supplies, and technology). 

## What is not yet implemented (and we are hoping to implement for milestone 4)

- Callbacks to connect all the graphs together (i.e., when a user selects a state from the map, all the other graphs should be updated to reflect data of that particular state. Currently only the 3 cards above the map are linked and the rest of the plots show the sum for all the states).

- The sizing of the graph inside the dashboard is still a work in progress. Currently our dashboard is bigger than it should be.  

## Experience of implementing Dash in R

Implementing our dashboard in R was not too difficult as the syntax for dash R versus dash is pretty similar. We did find that the documentation and the stackoverflow community for dash R was more limited which made it more challenging to fix bugs.

