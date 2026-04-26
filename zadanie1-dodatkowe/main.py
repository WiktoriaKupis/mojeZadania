import pandas as pd

# wczytanie danych
df = pd.read_csv("sales_raw.csv")
print("DANE:")
print(df.head())

# nowa kolumna total_value
df["total_value"] = df["quantity"] * df["unit_price"]
print("\nDODANO total_value:")
print(df.head())

# sprzedaż wg kraju
sales_by_country = df.groupby("country")["total_value"].sum()
print("\nSPRZEDAŻ WG KRAJU:")
print(sales_by_country)

# sprzedaż wg produktu
sales_by_product = df.groupby("product_name")["total_value"].sum()
print("\nSPRZEDAŻ WG PRODUKTU:")
print(sales_by_product)

# filtrowanie > 1000
df_high_value = df[df["total_value"] > 1000]

# zapis do pliku
df_high_value.to_csv("high_value_sales.csv", index=False)
print("\nZAPISANO high_value_sales.csv")

# liczba transakcji wg kraju (tylko >1000)
transactions_by_country = df_high_value.groupby("country").size()
print("\nLICZBA TRANSAKCJI WG KRAJU:")
print(transactions_by_country)