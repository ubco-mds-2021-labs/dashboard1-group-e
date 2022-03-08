# Superstore Sales Dashboard (Group E)

Managing one of the biggest supermarket chain in the United States is no easy task. Tracking sales and profit figures across different states and segments can be challenging as there is a lot of data to process. Data visualization tools such as a sales dashboard can help paint a clearer picture of the performance of the stores in each state and segments. Our app will enable the target audience to explore different sales metrics for each state in order to better understand what factors contribute to a higher profit. Finally, this tool will help the marketing team target which category of products they should focus their efforts on.

## Team Members

- Evelyn Sugihermanto: I love watching k-dramas in my spare time.
- Justine Filion: I love skiing and art journaling. 
- Mehul Bhargava: I love bird watching, gardening, observing wildlife, and marker art.
- Val Veeramani: I love going out on adventures in nature!

## Describe your topic/interest in about 150-200 words

Our dashboard aims to track the sales, profit and profit margin for all the *American Superstore*[^1] stores across the United States. Tracking of sales, profit and profit margin can be achieved by visualizing these metrics across different variables of interest such as `Ship Mode`, `Market Segment`, `State`, `Category` and `Sub-category` of items. Tracking sales and profits across different variables of interest is essential as it helps the audience better understand the current situation of the stores and enables them to notice which factors contribute most to the sales and profit. In doing so, better decisions can be made in order to guarantee the *American Superstore*'s success. 

## About this Dashboard

Our dashboard aims to present the sales, profit and profit margin for all American Superstore stores across the United States. There are five main components in our dashboard which are:

**1. Sales by Category Bar Plot**      
This plot shows the sales and profit of the stores with respect to different sub-categories in the x-axis. This plot will have a drop-down menu which will filter the data by category (furniture, office supplies, and technology). Sales and profit figures are differentiated by different colored bars.

**2. Metrics Proportion by Segment Pie Chart**     
This plot shows the metrics proportion by segment. There are three segments in our data (consumer, corporate, and home office), each will have a different color and three metrics (sales, profit, and items sold) that the user can choose from the radio button options.

**3. Sales and Profit by Ship Mode Line Chart**       
This plot shows the sales and profit figures for each shipment mode. The shipment mode will be on the x-axis, the sales and profit figures will be on the y-axis.  

**4. Top Five Items Sold Bar plot**      
This plot shows the top five items sold in a particular state. The states data for this plot will change if the user selects a different state through the US Map or the state drop-down menu below the US Map. 

**6. US Map**      
There are three components inside this plot. The first one is a drop-down menu that the user can select to filter the data for the whole dashboard. Changing the selection of the drop-down menu will update which state is highlighted in the US Map, the sales card, the profit card, the profit margin card as well as the selection for the other five plots discussed above. 

<img src ="images/dashboard_sketch.png">

## Describe your dataset in about 150-200 words

The dataset contains details for the orders of a supermarket chain in the United States, sourced from Kaggle [https://www.kaggle.com/nazarmahadialseied/superstore-sales]. This dataset will help us to understand which attribute has affected the sales and profit for the superstore sales. The dataset consists of 13 different attributes of a sample of entries. Attributes are ordinal, categorical and quantitative. Each of the rows (9994 samples) corresponds to a combination of attributes like ship mode, segment, country, city, state, postal code, region category, sub-category, quantity, and discount with the sales and profit associated with them. The goal of this data is to illustrate valuable insights such as average sales, profits for different regions, categories, etc. This could help the stores in building better marketing strategies. These estimates could also be used to identify which sector of the market is under loss and which sector is making the most profit. This would lead the business team in making better decisions to ensure the stores' profitability.

## Acknowledgements and references 

Dataset link: https://www.kaggle.com/nazarmahadialseied/superstore-sales

[^1]: This is a fictional name.
