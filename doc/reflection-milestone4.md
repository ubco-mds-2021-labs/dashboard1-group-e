# Reflection

## What you have implemented:

As part of milestone 4, we implemented several features in response to some of the issues and feedback we received. First, we created a centralized dropdown that controls the selection of the states for all the plots in our dashboard. Then, we changed the layout to include this dropdown and made the plots more uniform in size. The new dashboard layout includes a vertical section on the left that have some description about our dashboard, a centralized dropdown menu, and a learn more button that describes the dashboard in more detail. Since the map plot is the main visual point of our dashboard, we moved it to the top left corner to ensure that our user finds it right away. Additionally, we made sure all the fonts in the dashboard are the same for a more professional appearance.

## What is not yet implemented: 

• **The user can also click on the map to select which state they want to view and this will also change the rest of the dashboards.**

As the feature might not be as obvious as selecting an option from a dropdown menu, we decided not to include it. 

• **Make a chained callback for each dropdown below the map plot so that only the combinations with a row in the dataset are offered as options.**

To truly reflect the state of our dataset, we have decided not to reduce our data to only include combinations where the data is available, but rather show “NA” instead.

• **Adding the option for the user to select multiple options for each dropdown and the results show an aggregate of the metrics (sales/profit) for this selection.**

In the absence of data for some combinations of variables in the dataset, this feature would be ineffective since there will be many "NA"s.

## Feedback that we decide not to implement:

We received feedback in milestone 1 to add or change one of our plots of the top five states that sold a particular item. Unfortunately, this plot does not blend well with the rest of the plots as it won’t change with the centralized states dropdown.

## Has it been easy to use your app?

In general, our classmates find it easy to understand how to use our dashboard (which features to click and what they represent). However, we do receive some useful feedbacks to make our dashboard even easier to use and we have implemented these for our milestone 4.

## Are there reoccurring themes in your feedback on what is good and what can be improved?

One reoccurring theme in the feedbacks is to try to standardize the layout of our dashboard. This include adjusting the fonts and size of the plots. 

## Is there any feedback (or other insight) that you have found particularly valuable during your dashboard development?

A classmate suggested that we include some text that would draw attention to our dashboard. We found this useful and therefore added a description and a learn more button to our dashboard.
