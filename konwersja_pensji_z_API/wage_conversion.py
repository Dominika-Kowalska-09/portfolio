
import urllib.request as url
from datetime import datetime, timedelta
import json
import pandas as pd
import matplotlib.pyplot as plt

# funkcja - pobieranie kursów walut
def get_currency_rates(currency, start_date, end_date):
    api_url = f'https://api.nbp.pl/api/exchangerates/rates/A/{currency}/{start_date}/{end_date}/?format=json'
    nbp = url.urlopen(api_url)
    exchange_rates = json.loads(nbp.read())
    average_rates = [rate['mid'] for rate in exchange_rates['rates']]
    return average_rates

# funkcja - oblicznie średniego kursu rocznego
def calculate_annual_average_exchange_rate(currency, year):
    start_date = f'{year}-01-01'
    end_date = f'{year}-12-31'
    rates = get_currency_rates(currency, start_date, end_date)
    if rates:
        return sum(rates) / len(rates)
    return None

# wybór waluty na podstawie inicjałów
currency_mapping = {
    'A': 'USD',
    'B': 'AUD',
    'C': 'HKD',
    'Ć': 'HKD',
    'D': 'CAD',
    'E': 'EUR',
    'F': 'HUF',
    'G': 'CHF',
    'H': 'CYP',
    'I': 'GBP',
    'J': 'UAH',
    'K': 'JPY',
    'L': 'CZK',
    'Ł': 'CZK',
    'M': 'DKK',
    'N': 'ISK',
    'O': 'NOK',
    'P': 'BRL',
    'Q': 'MXN',
    'R': 'SEK',
    'S': 'INR',
    'Ś': 'INR',
    'T': 'ILS',
    'U': 'CNY',
    'V': 'CNY',
    'W': 'ZAR',
    'Z': 'KRW',
    'Ż': 'KRW',
    'Ź': 'KRW'
}

# funkcja - wybór walut na podstawie inicjałów
def get_currency(initials):
    currencies = set()
    initials_split = initials.split()
    if len(initials_split) >= 2:
        first_initial = initials_split[0][0].upper()
        second_initial = initials_split[1][0].upper()
    else:
        return []
    if first_initial in currency_mapping:
        currencies.add(currency_mapping[first_initial])
    if second_initial in currency_mapping:
        currencies.add(currency_mapping[second_initial])
    return list(currencies)

# wprowadzenie imienia i nazwiska
initials = "Dominika Kowalska"
selected_currencies = get_currency(initials)
print(f"Wybrane waluty dla '{initials}' to {selected_currencies}")

# oblicznie średnich rocznch kursów walut
years = range(2005, 2022)
kursy_walut = {currency: {} for currency in selected_currencies}
for currency in selected_currencies:
    for year in years:
        avg_rate = calculate_annual_average_exchange_rate(currency, year)
        if avg_rate:
            kursy_walut[currency][year] = avg_rate


# wgranie pliku csv ze średnimi wynagordzeniami
plik = 'Przeciętne_miesięczne_wynagrodzenie_w_gospodarce_narodowej_w_latach_1950-2021.csv'
wynagrodzenia = pd.read_csv(plik, delimiter = ';', encoding = 'windows-1250')
dane = wynagrodzenia[['Rok', 'Wartość']]
dane = dane[dane['Rok'].between(2005, 2021)]
print(dane.head())


# przeliczanie wynagrodzen na wybrane wlauty
przeliczone_dane_waluta = {currency: [] for currency in selected_currencies}
for currency in selected_currencies:
    for _, row in dane.iterrows():
        rok = int(row['Rok'])
        wynagrodzenie_pln = float(row['Wartość'].replace(',', '.'))
        kurs = kursy_walut.get(currency, {}).get(rok)
        if kurs:
            wynagrodzenie_w_walucie = wynagrodzenie_pln/kurs
            przeliczone_dane_waluta[currency].append({
                'Rok': rok,
                'Waluta': currency,
                'Wynagrodzenie_PLN': wynagrodzenie_pln,
                'Kurs': kurs,
                'Wynagrodzenie_Waluta': wynagrodzenie_w_walucie
            })

# utworzenie ramki danych z wynikami
dataframes = {currency: pd.DataFrame(data) for currency, data in przeliczone_dane_waluta.items()}
for currency, df in dataframes.items():
    print(f'\nDane dla waluty {currency}:')
    print(df.head())
    

# tworzenie wykresów
# oddzielny wykres dla każdej z walut
for currency, df in dataframes.items():
    plt.figure(figsize = (10, 6))
    plt.plot(df['Rok'], df['Wynagrodzenie_Waluta'], marker = 'o', label = f'wynagrodzenie w {currency}')
    plt.title(f'wynagrodzenia z PLN przeliczone na {currency}')
    plt.xlabel('rok')
    plt.ylabel(f'wartość wynagrodzenia w {currency}')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# wspólny wykres z dwoma osiami y
currencies = list(dataframes.keys())
if len(currencies) == 2:
    currency1, currency2 = currencies
    df1, df2 = dataframes[currency1], dataframes[currency2]
    fig, ax1 = plt.subplots(figsize = (12, 7))
    ax1.set_xlabel('rok')
    ax1.set_ylabel(f'wartość wynagrodzenia w {currency1}', color = 'blue')
    ax1.plot(df1['Rok'], df1['Wynagrodzenie_Waluta'], marker = 'o', label = f'{currency1}', color = 'blue')
    ax1.tick_params(axis = 'y', labelcolor = 'blue')
    ax1.grid(True)
    ax2 = ax1.twinx()
    ax2.set_ylabel(f'wartość wynagrodzenia w {currency2}', color = 'red')
    ax2.plot(df2['Rok'], df2['Wynagrodzenie_Waluta'], marker = 'o', label = f'{currency2}', color = 'red')
    ax2.tick_params(axis = 'y', labelcolor = 'red')
    plt.title(f'wynagrodzenia z PLN przeliczone na {currency1} i na {currency2}')
    fig.tight_layout()
    plt.show()