import json
import requests

from geopy.distance import distance
import folium

import os
from dotenv import load_dotenv


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(
        base_url,
        params={
            "geocode": address,
            "apikey": apikey,
            "format": "json",
        },
    )
    response.raise_for_status()
    found_places = response.json()["response"]["GeoObjectCollection"]["featureMember"]

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant["GeoObject"]["Point"]["pos"].split(" ")
    return lon, lat


def main():
    load_dotenv()
    apikey = os.getenv("APIKEY")
    with open("coffee.json", "r", encoding="CP1251") as coffee:
        file_contents = coffee.read()
    coffeeshops = json.loads(file_contents)
    question = input("Где вы находитесь?: ")
    coords = fetch_coordinates(apikey, question)
    m = folium.Map(location=coords[::-1], zoom_start=12)
    nearest_coffee = sorted(
        coffeeshops,
        key=lambda coffee: distance(
            coords[::-1], coffee["geoData"]["coordinates"][::-1]
        ).km,
    )[:5]

    for coffee in nearest_coffee:
        name = coffee["Name"]
        lon, lat = coffee["geoData"]["coordinates"]
        folium.Marker(
            location=[lat, lon],
            tooltip="Click me!",
            popup=name,
            icon=folium.Icon(icon="cloud"),
        ).add_to(m)

        m.save("index.html")


if __name__ == "__main__":
    main()