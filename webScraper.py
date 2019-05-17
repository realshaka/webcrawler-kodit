from bs4 import BeautifulSoup
import requests
import re
import json
import ast
import datetime as dt
import csv, sys
import pandas as pd

source_link = "https://kodit.io/fi/buy/"
source = requests.get(source_link)
soup_source = BeautifulSoup(source.content, "html.parser")
result = []


def return_PriceComparison(city, rooms, price_sqm):
    filename = "stat.csv"
    df = pd.read_csv(filename, encoding="unicode-escape")

    if rooms == 1:
        roomsStr = "One-room flat"
    elif rooms == 2:
        roomsStr = "Two-room flat"
    elif rooms >= 3:
        roomsStr = "Three-room flat+"
    else:
        return "no data"

    try:
        if df["Region"].str.contains(city).any():
            price_df = df[(df["Region"] == city) & (df["Number of rooms"] == roomsStr)]
            avg_price = int(price_df["Price per square meter"])
            if price_sqm > avg_price * 1.05:
                return "This price is high"
            elif price_sqm < avg_price * 0.95:
                return "This price is low"
            else:
                return "This price is ok"
        else:
            return "no data"
    except KeyError:
        return "no data"


for link in soup_source.findAll(
    "a", attrs={"class": "Apartment-Card Grid-Cell w(100%)"}
):
    apartment_source = requests.get("https://kodit.io" + link.get("href"))
    soup_apartment = BeautifulSoup(apartment_source.content, "html.parser")
    apartment = soup_apartment.find("meta", attrs={"name": "kodit:apartment"})[
        "content"
    ]
    # print(apartment)
    apartment_dict = dict(json.loads(apartment))
    try:
        comparedPrice = return_PriceComparison(
            apartment_dict["address_city"],
            apartment_dict["rooms"],
            apartment_dict["price_sqm"],
        )
    except KeyError:
        comparedPrice = "no data"
    apartment_dict.update({"compared_price": comparedPrice})
    # print(comparedPrice)
    result.append(apartment_dict)

payload = {
    "who_rules": "kodit.io",
    "date": dt.datetime.now().strftime("%Y-%m-%d"),
    "results": result,
}

with open("result.json", "w") as f:
    json.dump(payload, f)

# r = requests.post(
#     "https://cc677kr6sc.execute-api.eu-central-1.amazonaws.com/data", json=payload
# )


# Test with local json server
r = requests.post("http://localhost:3000/data", json=payload)

print(r)
