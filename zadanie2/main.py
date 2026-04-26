import pandas as pd

# ZADANIE 1 – WCZYTANIE DANYCH

url = "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/07_Visualization/Online_Retail/Online_Retail.csv"

df = pd.read_csv(url, encoding="ISO-8859-1")

print("ZADANIE 1 – STAGING")
print("Liczba rekordów:", df.shape[0])
print("Liczba kolumn:", df.shape[1])
print("\nPierwsze 5 wierszy:")
print(df.head())


# ZADANIE 2 – IDENTYFIKACJA ENCJI

print("\nZADANIE 2 – ENCJE")
print("""
Potencjalne encje:
1. Customers
   PK: CustomerID
   Atrybuty: Country

2. Products
   PK: StockCode
   Atrybuty: Description

3. Orders
   PK: InvoiceNo
   FK: CustomerID
   Atrybuty: InvoiceDate

4. OrderItems
   PK: InvoiceNo + StockCode
   FK: InvoiceNo, StockCode
   Atrybuty: Quantity, UnitPrice

5. Date
   PK: InvoiceDate
   Atrybuty: Year, Month, DayOfWeek, Quarter
""")


# ZADANIE 3 – MODEL 3NF / INMON

customers = df[["CustomerID", "Country"]].drop_duplicates()
products = df[["StockCode", "Description"]].drop_duplicates()
orders = df[["InvoiceNo", "InvoiceDate", "CustomerID"]].drop_duplicates()
order_items = df[["InvoiceNo", "StockCode", "Quantity", "UnitPrice"]]

dates = pd.DataFrame()
dates["InvoiceDate"] = df["InvoiceDate"].drop_duplicates()
dates["InvoiceDate"] = pd.to_datetime(dates["InvoiceDate"])
dates["Year"] = dates["InvoiceDate"].dt.year
dates["Month"] = dates["InvoiceDate"].dt.month
dates["DayOfWeek"] = dates["InvoiceDate"].dt.day_name()
dates["Quarter"] = dates["InvoiceDate"].dt.quarter

print("\nZADANIE 3 – UTWORZONE TABELE 3NF")
print("Customers:", customers.shape)
print("Products:", products.shape)
print("Orders:", orders.shape)
print("OrderItems:", order_items.shape)
print("Date:", dates.shape)

print("\nPrzykład tabeli Customers:")
print(customers.head())

print("\nPrzykład tabeli Products:")
print(products.head())

print("\nPrzykład tabeli Orders:")
print(orders.head())

print("\nPrzykład tabeli OrderItems:")
print(order_items.head())

print("\nPrzykład tabeli Date:")
print(dates.head())


# SPRAWDZANIE KLUCZY

print("\nSPRAWDZANIE KLUCZY")

print("Czy CustomerID jest unikalny?")
print(customers["CustomerID"].is_unique)

print("Czy StockCode jest unikalny?")
print(products["StockCode"].is_unique)

print("Czy InvoiceNo jest unikalny?")
print(orders["InvoiceNo"].is_unique)

print("Czy StockCode w OrderItems istnieje w Products?")
print(order_items["StockCode"].isin(products["StockCode"]).all())

print("Czy InvoiceNo w OrderItems istnieje w Orders?")
print(order_items["InvoiceNo"].isin(orders["InvoiceNo"]).all())


# ZAPIS TABEL DO PLIKÓW CSV

customers.to_csv("customers.csv", index=False)
products.to_csv("products.csv", index=False)
orders.to_csv("orders.csv", index=False)
order_items.to_csv("order_items.csv", index=False)
dates.to_csv("dates.csv", index=False)

print("\nZapisano pliki CSV:")
print("customers.csv")
print("products.csv")
print("orders.csv")
print("order_items.csv")
print("dates.csv")


# ZADANIE 4 – REFLEKSJA

print("\nZADANIE 4 – REFLEKSJA")
print("""
Model 3NF nie jest wygodny do analiz OLAP, ponieważ dane są mocno podzielone
na wiele tabel. Aby przygotować raport sprzedaży, trzeba łączyć ze sobą
kilka tabel, np. Orders, OrderItems, Products, Customers oraz Date.

Wiele joinów byłoby potrzebnych przy analizach takich jak:
- sprzedaż według kraju,
- sprzedaż według produktu,
- sprzedaż według miesiąca,
- liczba zamówień klientów,
- wartość sprzedaży w czasie.

Model 3NF dobrze ogranicza redundancję i porządkuje dane, ale nie jest
najwygodniejszy do szybkiego raportowania i analiz wielowymiarowych.
Do OLAP wygodniejszy będzie model Kimballa, czyli schemat gwiazdy.
""")