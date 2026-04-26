import pandas as pd


# Laboratorium 2 – Zadanie indywidualne
# Temat: Wymiary danych w hurtowni danych
# Podejście: Kimball (schemat gwiazdy)




# 1. WCZYTANIE DANYCH


# Źródło danych (plik CSV z GitHub)
url = "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/07_Visualization/Online_Retail/Online_Retail.csv"

# Wczytanie danych do DataFrame
df = pd.read_csv(url, encoding="ISO-8859-1")

print("WCZYTANE DANE")
print("Liczba rekordów:", df.shape[0])
print("Liczba kolumn:", df.shape[1])
print(df.head())


# 2. PRZYGOTOWANIE DANYCH


# Usunięcie rekordów bez identyfikatora klienta
df = df.dropna(subset=["CustomerID"])

# Usunięcie anulowanych faktur (InvoiceNo zaczyna się od 'C')
df = df[~df["InvoiceNo"].astype(str).str.startswith("C")]

# Usunięcie zwrotów (ujemne ilości)
df = df[df["Quantity"] > 0]

# Usunięcie błędnych cen
df = df[df["UnitPrice"] > 0]

# Konwersja kolumny daty do formatu datetime
df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

# Utworzenie miary sprzedaży
df["SalesAmount"] = df["Quantity"] * df["UnitPrice"]

print("\nDANE PO CZYSZCZENIU")
print("Liczba rekordów:", df.shape[0])
print(df.head())



# 3. MODEL LOGICZNY – SCHEMAT GWIAZDY


# Wymiar klienta
dim_customer = df[["CustomerID", "Country"]].drop_duplicates()

# Wymiar produktu 
dim_product = df[["StockCode", "Description"]].drop_duplicates()

# Wymiar kraju
dim_country = df[["Country"]].drop_duplicates().reset_index(drop=True)
dim_country["CountryID"] = dim_country.index + 1  # sztuczny klucz

# Wymiar daty
dim_date = df[["InvoiceDate"]].drop_duplicates()
dim_date["Year"] = dim_date["InvoiceDate"].dt.year
dim_date["Month"] = dim_date["InvoiceDate"].dt.month
dim_date["Day"] = dim_date["InvoiceDate"].dt.day
dim_date["DayOfWeek"] = dim_date["InvoiceDate"].dt.day_name()
dim_date["Quarter"] = dim_date["InvoiceDate"].dt.quarter

# Tabela faktów
# Dodanie kluczy do wymiarów
fact_sales = df.merge(dim_country, on="Country", how="left")

fact_sales = fact_sales[
    [
        "InvoiceNo",
        "StockCode",
        "CustomerID",
        "CountryID",
        "InvoiceDate",
        "Quantity",
        "UnitPrice",
        "SalesAmount",
    ]
]

print("\nMODEL LOGICZNY")
print("Tabela faktów: fact_sales")
print("Wymiary: dim_customer, dim_product, dim_country, dim_date")

# Ziarnistość danych
print("\nZiarnistość: jedna pozycja produktu na fakturze")



# 4. ANALIZA BIZNESOWA


# Sprzedaż według krajów
sales_by_country = (
    df.groupby("Country")["SalesAmount"]
    .sum()
    .reset_index()
    .sort_values(by="SalesAmount", ascending=False)
)

print("\nSPRZEDAŻ WG KRAJÓW")
print(sales_by_country.head(10))

# Trend sprzedaży w czasie
df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)

sales_trend = (
    df.groupby("YearMonth")["SalesAmount"]
    .sum()
    .reset_index()
    .sort_values(by="YearMonth")
)

print("\nTREND SPRZEDAŻY")
print(sales_trend)



# 5. ZAPIS WYNIKÓW


dim_customer.to_csv("dim_customer.csv", index=False)
dim_product.to_csv("dim_product.csv", index=False)
dim_country.to_csv("dim_country.csv", index=False)
dim_date.to_csv("dim_date.csv", index=False)
fact_sales.to_csv("fact_sales.csv", index=False)

sales_by_country.to_csv("sales_by_country.csv", index=False)
sales_trend.to_csv("sales_trend.csv", index=False)

print("\nZAPISANO PLIKI CSV")



# 6. UZASADNIENIE (KIMBALL)


print("""
Zadanie zostało wykonane w podejściu Kimballa.

Zaczynamy od procesu biznesowego sprzedaży i tworzymy model wymiarowy
(składający się z tabeli faktów i wymiarów).

Tabela faktów przechowuje miary (SalesAmount),
a wymiary umożliwiają analizę danych według różnych perspektyw:
klienta, produktu, kraju i czasu.

Model ten jest wygodny do analiz OLAP.
""")