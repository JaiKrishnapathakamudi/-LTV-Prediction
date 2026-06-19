import pandas as pd

# Load cleaned dataset
data = pd.read_csv("data/online_retail.csv")

# Remove missing values
data.dropna(inplace=True)

# Remove duplicates
data.drop_duplicates(inplace=True)

# Remove negative values
data = data[data['Quantity'] > 0]
data = data[data['UnitPrice'] > 0]

# Create TotalPrice column
data['TotalPrice'] = data['Quantity'] * data['UnitPrice']

# -----------------------------
# TOP 10 CUSTOMERS
# -----------------------------
top_customers = data.groupby('CustomerID')['TotalPrice'].sum()

top_customers = top_customers.sort_values(ascending=False).head(10)

print("\nTOP 10 CUSTOMERS\n")
print(top_customers)

# -----------------------------
# TOP COUNTRIES
# -----------------------------
top_countries = data.groupby('Country')['TotalPrice'].sum()

top_countries = top_countries.sort_values(ascending=False).head(10)

print("\nTOP COUNTRIES\n")
print(top_countries)

# -----------------------------
# BEST SELLING PRODUCTS
# -----------------------------
top_products = data.groupby('Description')['Quantity'].sum()

top_products = top_products.sort_values(ascending=False).head(10)

print("\nBEST SELLING PRODUCTS\n")
print(top_products)