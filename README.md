# Scraper volebních dat

Tento projekt je webový scraper, který extrahuje volební data z českého volebního webu. Skript získává volební statistiky pro obce v určeném regionu a ukládá data do CSV souboru.

## Instalace

Ujistěte se, že máte na svém systému nainstalovaný Python. Poté nainstalujte požadované knihovny pomocí:

```sh
pip install -r requirements.txt
```

## Použití

Pro spuštění scraperu použijte následující příkaz:

```sh
python main.py <URL> <výstupní_soubor>
```

### Příklad:

```sh
python main.py "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2104" vysledky.csv
```

## Soubory
- `main.py` - Hlavní skript obsahující logiku scraperu.
- `requirements.txt` - Seznam závislostí potřebných ke spuštění skriptu.
- `vysledky.csv` - Výstupní soubor obsahující extrahovaná volební data.

## Závislosti
Skript vyžaduje následující Python knihovny:
- `requests`
- `beautifulsoup4`
- `pandas`

## Ošetření chyb
Pokud během scrapingového procesu dojde k chybě, skript zobrazí odpovídající chybovou zprávu a ukončí se.

## Autor
**Gordiyenko Svitlana**

Pro jakékoliv dotazy kontaktujte: `parostok.root@seznam.cz`

