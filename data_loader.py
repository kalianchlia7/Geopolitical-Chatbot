import pandas as pd
import os

#load OFAC sanctions data
ofac = pd.read_csv("/Users/kalianchlia/Downloads/Coding Projects/ML Projects/Project 3/data/OFAC Sanctions List.csv")

#load WTO MFN tariff data
wto = pd.read_csv("/Users/kalianchlia/Downloads/Coding Projects/ML Projects/Project 3/data/Trade-weighted MFN applied tariff average - all products (Percent).csv")

#print(ofac.columns)
#print(wto.columns)

def lookup_sanctions(name):
    #search OFAC for entity name

    name = name.lower()

    #Column 1: entity name, Column 3: country
    matches = ofac[ofac.iloc[:, 1].str.lower().str.contains(name)]
    
    if len(matches) == 0:
        return "No sanctions found for that name."
    
    # Return top 5 matches with name and country
    return matches.iloc[:, [1, 3]].head(5).to_string(index=False)


def lookup_tariff(reporting_country, partner_country=None, year=None):
    """
    Search WTO MFN tariff CSV for a reporting economy.
    """
    df = wto[wto['Reporting Economy'].str.lower() == reporting_country.lower()]
    
    if partner_country:
        df = df[df['Partner Economy'].str.lower() == partner_country.lower()]
    
    if year:
        df = df[df['Year'] == int(year)]
    
    if len(df) == 0:
        return "No tariff data found."
    
    return df[['Reporting Economy', 'Partner Economy', 'Year', 'Value']].to_string(index=False)
