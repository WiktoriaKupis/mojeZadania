import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# ==============================
# ŚCIEŻKI DO FOLDERÓW
# ==============================

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# ==============================
# 1. WCZYTANIE DANYCH Z GITHUBA
# ==============================

url = "https://raw.githubusercontent.com/guipsamora/pandas_exercises/master/07_Visualization/Online_Retail/Online_Retail.csv"

df = pd.read_csv(url, encoding="ISO-8859-1")

# zapisujemy kopię pobranego pliku do folderu data
df.to_csv(DATA_DIR / "Online_Retail.csv", index=False)

print("PIERWSZE WIERSZE PO WCZYTANIU DANYCH:")
print(df.head())

print("\nLICZBA WIERSZY I KOLUMN:")
print(df.shape)

# ==============================
# 2. CZYSZCZENIE DANYCH
# ==============================

print("\nBRAKI DANYCH PRZED CZYSZCZENIEM:")
print(df.isnull().sum())

df = df.dropna(subset=["CustomerID"])
df = df[df["Quantity"] > 0]

df["TotalPrice"] = df["Quantity"] * df["UnitPrice"]

print("\nDANE PO CZYSZCZENIU:")
print(df.head())

print("\nLICZBA WIERSZY I KOLUMN PO CZYSZCZENIU:")
print(df.shape)

# ==============================
# 3. CZAS JAKO WYMIAR
# ==============================

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

df["Year"] = df["InvoiceDate"].dt.year
df["Month"] = df["InvoiceDate"].dt.month

print("\nDANE Z DODANYM ROKIEM I MIESIĄCEM:")
print(df[["InvoiceDate", "Year", "Month"]].head())

print("\nLICZBA WIERSZY I KOLUMN PO DODANIU CZASU:")
print(df.shape)

# ==============================
# 4. MODEL OLAP
# ==============================

print("\nMODEL OLAP")
print("Fakty: TotalPrice, Quantity")
print("Wymiary: Country, Year, Month, StockCode")


# ==============================
# 5. ROLL-UP
# Sprzedaż według roku
# ==============================

rollup_year = df.groupby("Year")["TotalPrice"].sum()

print("\nROLL-UP: SPRZEDAŻ WEDŁUG ROKU")
print(rollup_year)

rollup_year.plot(kind="bar", title="Sprzedaż według roku")
plt.xlabel("Rok")
plt.ylabel("Sprzedaż")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "wykres_rollup_sprzedaz_rok.png")
plt.show()

# ==============================
# 6. DRILL-DOWN
# Sprzedaż według roku i miesiąca
# ==============================

drilldown_month = df.groupby(["Year", "Month"])["TotalPrice"].sum()

print("\nDRILL-DOWN: SPRZEDAŻ WEDŁUG ROKU I MIESIĄCA")
print(drilldown_month)


# ==============================
# 7. SLICE
# Dane tylko dla jednego kraju
# ==============================

uk_data = df[df["Country"] == "United Kingdom"]

print("\nSLICE: DANE DLA UNITED KINGDOM")
print(uk_data.head())


# ==============================
# 8. DICE
# Dane dla kraju United Kingdom i roku 2011
# ==============================

uk_2011 = df[(df["Country"] == "United Kingdom") & (df["Year"] == 2011)]

print("\nDICE: UNITED KINGDOM W ROKU 2011")
print(uk_2011.head())

# ==============================
# 9. PIVOT TABLE / KOSTKA DANYCH
# Kraj jako wiersze, rok jako kolumny, sprzedaż jako wartości
# ==============================

cube_year = pd.pivot_table(
    df,
    values="TotalPrice",
    index="Country",
    columns="Year",
    aggfunc="sum",
    fill_value=0
)

print("\nKOSTKA DANYCH: KRAJ X ROK")
print(cube_year.head())

# ==============================
# ZADANIE 1
# Top 10 krajów pod względem sprzedaży
# ==============================

top10_countries = df.groupby("Country")["TotalPrice"].sum().sort_values(ascending=False).head(10)

print("\nZADANIE 1: TOP 10 KRAJÓW POD WZGLĘDEM SPRZEDAŻY")
print(top10_countries)

top10_countries.plot(kind="bar", title="Top 10 krajów pod względem sprzedaży")
plt.xlabel("Kraj")
plt.ylabel("Sprzedaż")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "wykres_top10_krajow.png")
plt.show()


# ==============================
# ZADANIE 2
# Znajdź miesiąc o największej sprzedaży
# ==============================

sales_by_month = df.groupby(["Year", "Month"])["TotalPrice"].sum().sort_values(ascending=False)

best_month = sales_by_month.head(1)

print("\nZADANIE 2: MIESIĄC O NAJWIĘKSZEJ SPRZEDAŻY")
print(best_month)

# ==============================
# ZADANIE 3
# Kostka: wiersze = kraj, kolumny = miesiąc, wartości = sprzedaż
# ==============================

cube_country_month = pd.pivot_table(
    df,
    values="TotalPrice",
    index="Country",
    columns="Month",
    aggfunc="sum",
    fill_value=0
)

print("\nZADANIE 3: KOSTKA KRAJ X MIESIĄC")
print(cube_country_month.head())


# ==============================
# ZADANIE 4
# Dla każdego kraju znajdź rok z najwyższą sprzedażą
# ==============================

country_year_sales = df.groupby(["Country", "Year"])["TotalPrice"].sum().reset_index()

best_year_per_country = country_year_sales.loc[
    country_year_sales.groupby("Country")["TotalPrice"].idxmax()
]

print("\nZADANIE 4: NAJLEPSZY ROK SPRZEDAŻY DLA KAŻDEGO KRAJU")
print(best_year_per_country)


# ==============================
# ZADANIE 5
# Top 5 produktów w każdym kraju
# ==============================

product_country_sales = df.groupby(
    ["Country", "StockCode", "Description"]
)["TotalPrice"].sum().reset_index()

top5_products_each_country = product_country_sales.sort_values(
    ["Country", "TotalPrice"],
    ascending=[True, False]
).groupby("Country").head(5)

print("\nZADANIE 5: TOP 5 PRODUKTÓW W KAŻDYM KRAJU")
print(top5_products_each_country)

# ==============================
# 10. ZAPIS WYNIKÓW DO PLIKÓW
# ==============================

rollup_year.to_csv(OUTPUT_DIR / "wynik_rollup_sprzedaz_rok.csv")
drilldown_month.to_csv(OUTPUT_DIR / "wynik_drilldown_rok_miesiac.csv")
cube_year.to_csv(OUTPUT_DIR / "wynik_kostka_kraj_rok.csv")

top10_countries.to_csv(OUTPUT_DIR / "wynik_top10_krajow.csv")
best_month.to_csv(OUTPUT_DIR / "wynik_najlepszy_miesiac.csv")
cube_country_month.to_csv(OUTPUT_DIR / "wynik_kostka_kraj_miesiac.csv")
best_year_per_country.to_csv(OUTPUT_DIR / "wynik_najlepszy_rok_dla_kraju.csv", index=False)
top5_products_each_country.to_csv(OUTPUT_DIR / "wynik_top5_produkty_kraj.csv", index=False)

print("\nZAPISANO WYNIKI DO FOLDERU OUTPUT.")