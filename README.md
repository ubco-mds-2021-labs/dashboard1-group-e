# Superstore Sales Dashboard (Group E)

Managing one of the biggest supermarket chain in Canada is no easy task. Tracking sales and profit figures across different states and segments can be challenging as there is a lot of data to process. Data visualization tools such as a sales dashboard can help paint a clear picture of the performance of the stores in each state and segments. Our app will enable the target audience to explore different sales metrics for each state in order to better understand what factors contribute to a higher profit. This app also offers a tool that predicts the daily profit margin given certain variables such as the shipment mode, the state and the product category. Finally, this tool will help the marketing team target which category of products they should focus their efforts on.

## Team Members

- Evelyn Sugihermanto: I love watching k-dramas in my spare time.
- Person 2: one sentence about you!
- Person 3: one sentence about you!
- Person 4: one sentence about you!

## Describe your topic/interest in about 150-200 words

The main topic of interest that our dashboard aims to achieve is to track and predict the sales and profit performance of Superstore. Tracking of sales and profit can be achieved by visualizing the sales and profit figures across different variables of interest such as Ship Mode, Market Segment, States, Category and Sub-category of items. Tracking the sales and profit figures across different variables of interest is essential as it would help the audience better understand the current situation of the stores and which factors contribute most to the sales and profit. Apart from that, we are also interested to incorporate a prediction feature in our dashboard through some machine learning models such as Random Forest, Boosting, etc. to predict the sales and profit figures. The prediction feature hopes to help the audience predict which Ship Mode, Market Segment, States, Category and Sub-category of items will bring in more sales and profit.This will hopefully enable our target audience to focus on improving categories with lower sales and profit and maintain categories that has higher sales and profit.

## About this Dashboard

Our dashboard aims to present the sales and profit performance of Superstore. There are five main components in our dashboard which are:

**1. Sales by Category Bar Plot**      
This plot shows the sales and profit of the stores with respect to different sub-categories in the x-axis. This plot will have a drop-down menu which will filter the data by category (furniture, office supplies, and technology). Sales and profit figures are differentiated by different colored bars.

**2. Metrics Proportion by Segment Pie Chart**     
This plot shows the metrics proportion by segment. There are three segments in our data (consumer, corporate, and home office), each will have a different color and three metrics (sales, profit, and items sold) that the user can choose from the radio button options.

**3. Sales and Profit by Ship Mode Line Chart**       
This plot shows the sales and profit figures for each shipment mode. The shipment mode will be on the x-axis, the sales and profit figures will be on the y-axis.  

**4. Top Five Items Sold Bar plot**      
This plot shows the top five items sold in a particular state. The states data for this plot will change if the user selects a different state through the US Map or the state drop-down menu below the US Map. 

**5. US Map**      
There are three components inside this plot. The first one is a drop-down menu that the user can select to filter the data. Changing the selection of the drop-down menu will change which state is highlighted in the US Map, the predicted sales, profit, and profit margin figures, and all the other four plots discussed above. The user can also click on the map to select which state they want to view and this will also change the rest of the dashboards.

<img src ="images/dashboard_sketch.png">

## Describe your dataset in about 150-200 words

The dataset contains details for the orders of a Superstore in the US, sourced from Kaggle [https://www.kaggle.com/nazarmahadialseied/superstore-sales]. This dataset will help us to understand which attribute has affected the sales and profit for the superstore sales. The dataset consists of 13 different attributes of a sample of entries. Attributes are ordinal, categorical and quantitative. Each of the rows (9994 samples) corresponds to a combination of attributes like ship mode, segment, country, city, stat, postal code, region category, sub-category, quantity, and discount with the sales and profit associated with them. The goal of this data is to establish value insights from their sales such as average sales, profits from different regions, categories, etc. which could help the Superstores make good strategies for their business future plan in the market. These estimates could be used to identify which sector of the market is under loss and which sector is making huge profits which supports the business to make appropriate decisions.

## Acknowledgements and references 

Dataset link: https://www.kaggle.com/nazarmahadialseied/superstore-sales
