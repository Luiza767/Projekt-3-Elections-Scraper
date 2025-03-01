import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_region_link(region_code):
    """returns url for region that contains table of all municipalities

    Keyword arguments:
    region_code -- code of the region
    """
    url = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if cols and cols[0].text.strip() == region_code:
                a_tag = cols[-1].find("a")
                if a_tag:
                    return "https://www.volby.cz/pls/ps2017nss/" + a_tag["href"]
                else:
                    raise Exception("Region code found but no href found")
    raise Exception("Region code not found")

def get_municipality_links(region_url):
    """returns dictionary
    key = code of municipality
    value = tuple containing name of municipality and url for final data

    Keyword arguments:
    region_url -- url of region (see get_region_link)
    """
    response = requests.get(region_url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = {}
    tables = soup.find_all("table")
    for table in tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if cols:
                code = cols[0].text.strip()
                name = cols[1].text.strip()
                a_tag = cols[0].find("a")
                if a_tag:
                    links[code] = (name, "https://www.volby.cz/pls/ps2017nss/" + a_tag["href"])
    return links

def get_voters_data(municipality_url):
    response = requests.get(municipality_url)
    soup = BeautifulSoup(response.text, "html.parser")

    voters = {}
    summary_table = soup.find("table", {"id":"ps311_t1"})
    if not summary_table:
        raise Exception("Summary table not found")

    summary_table_cols = summary_table.find_all("td")
    if summary_table_cols:
        registered_voters_count = summary_table_cols[3].text.strip()
        issued_envelopes = summary_table_cols[4].text.strip()
        valid_votes = summary_table_cols[7].text.strip()
    else:
        raise Exception("Summary table not found")

    summary_data = [registered_voters_count,issued_envelopes,valid_votes]

    political_party_tables = []
    tables = soup.find_all('table')
    for table in tables:
        if table.find('th', string='Strana'):
            political_party_tables.append(table)

    party_data = []

    for table in political_party_tables:
        rows = table.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if cols:
                party_name = cols[1].text.strip()
                party_votes = cols[2].text.strip()
                party_data.append((party_name,party_votes))

    return (summary_data,party_data)

def scrape_election_data(region_code, output_csv="election_results.csv"):
    try:
        obec_links = get_region_link(region_code)
    except:
        print("Wrong region code")

    municipality_links = get_municipality_links(obec_links)
    if not municipality_links:
        print("No municipalities found")
        return
    csv_data = []


    csv_columns = ['Code', 'Municipality', 'Registered voters','Issued envelopes','Valid votes']
    add_partynames_as_columns = True


    for code, (name, municipality_url) in municipality_links.items():
        voters_data = get_voters_data(municipality_url)
        result_data = [code, name]
        result_data.extend(voters_data[0])
        result_data.extend([value for name, value in voters_data[1]])
        csv_data.append(result_data)
        if(add_partynames_as_columns):
            add_partynames_as_columns = False
            csv_columns.extend([name for name, value in voters_data[1]])

    df = pd.DataFrame(csv_data, columns=csv_columns)
    if df is not None:
        df.to_csv("election_results.csv", sep=';', index=False, encoding='utf-8')
    else:
         print("Error")

scrape_election_data("CZ0204")


