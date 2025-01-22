import plotly.graph_objects as go
import pandas as pd

#1. Load the file shopping_trends.csv from the eportal. Print out several initial
#records.
shopping_trends_data = pd.read_csv('shopping_trends.csv')
print(shopping_trends_data.head(11))

# 2. Identify customers who meet the following criteria: they have an active subscription,
#they have completed more than 40 previous purchases, and their purchase amount
#exceeds 90 USD . Filter the dataset to find such customers and display their key
#details, including their Customer ID, the total number of previous purchases, and
#their purchase amount. Finally, save the results to a new CSV file.
print()
shopping_trends_data.info()

filtered_customers = shopping_trends_data[
    (shopping_trends_data['Subscription Status'] == 'Yes') &
    (shopping_trends_data['Previous Purchases'] > 40) &
    (shopping_trends_data['Purchase Amount (USD)'] > 90)
]

result = filtered_customers[['Customer ID','Previous Purchases','Purchase Amount (USD)']]
result.to_csv('filtered_customers.csv', index=False)

print(result)

#3. Create a bar chart that illustrates the total purchase amount for each season (Spring,
#Summer, Autumn, Winter) using the provided dataset. What is the difference in
#total purchase amounts between the season with the highest and the lowest revenue?

print()
season_totals =shopping_trends_data.groupby('Season')['Purchase Amount (USD)'].sum().reset_index()
fig= go.Figure()

fig.add_trace(go.Bar(x=season_totals['Season'],y=season_totals['Purchase Amount (USD)'],marker_color='lightblue'))
fig.update_layout(title_text="total purchase amount by season",xaxis_title="season",yaxis_title="total purchase amount (USD)",
barmode="group")

fig.show()

max_purchase_amount=season_totals['Purchase Amount (USD)'].max()
min_purchase_amount=season_totals['Purchase Amount (USD)'].min()
difference=max_purchase_amount-min_purchase_amount

print(f"What is the difference in total purchase amounts between the season with the highest and the lowest revenue?: ${difference}")
# It's 4241 dolarów.