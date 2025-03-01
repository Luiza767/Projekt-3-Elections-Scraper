import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_election_data(region_code):
    
    url = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    response = requests.get(url)
    response.encoding = response.apparent_encoding  # Oprava kódování
    
    if response.status_code != 200:
        print("Chyba při načítání stránky")
        return None
    
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.find_all('table')
    
    if len(tables) < 2:
        print("Tabulky nebyly nalezeny")
        return None
    
    # Druhá tabulka obsahuje hlasovací výsledky
    rows = tables[1].find_all('tr')
    data = []
    
    for row in rows[1:]:  # Přeskakujeme hlavičku tabulky
        cols = row.find_all('td')
        if len(cols) >= 2:
            party = cols[0].text.strip()
            votes = cols[1].text.strip().replace('\xa0', '')  # Odstranění pevné mezery
            data.append([party, votes])
    
    df = pd.DataFrame(data, columns=['Strana', 'Hlasy'])
    return df


df = scrape_election_data()
if df is not None:
    print(df)
    df.to_csv("election_results.csv", index=False, encoding='utf-8')