import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
data = pd.read_csv("data/online_retail.csv")

# Cleaning
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)

data = data[data['Quantity'] > 0]
data = data[data['UnitPrice'] > 0]

# Revenue column
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

# -----------------------------
# TOP 10 COUNTRIES
# -----------------------------
top_countries = data.groupby('Country')['TotalPrice'].sum()

top_countries = top_countries.sort_values(ascending=False).head(10)

# Plot
plt.figure(figsize=(12,6))

sns.barplot(
    x=top_countries.values,
    y=top_countries.index
)

plt.title("Top 10 Countries by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Country")

plt.show()

# -----------------------------
# TOP PRODUCTS
# -----------------------------
top_products = data.groupby('Description')['Quantity'].sum()

top_products = top_products.sort_values(ascending=False).head(10)

# Plot
plt.figure(figsize=(12,6))

sns.barplot(
    x=top_products.values,
    y=top_products.index
)

plt.title("Top 10 Best Selling Products")
plt.xlabel("Quantity Sold")
plt.ylabel("Product")

plt.show()