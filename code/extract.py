import requests
import os
import json

API_URL = "https://data.cdc.gov/resource/hksd-2xuw.json"
CACHE_FILE = "cache/raw_disease_data.json"
APP_TOKEN = "fWXQM3KDN7DyxSZs1E9vvy5Rh"  # ← Replace with your actual token

HEADERS = {
    "X-App-Token": APP_TOKEN
}

def fetch_disease_data(topics=None, location=None, limit=1000):
    os.makedirs("cache", exist_ok=True)
    all_results = []

    for topic in topics or ["Diabetes"]:
        offset = 0
        print(f"\nFetching: {topic} data...")
        while True:
            params = {
                "topic": topic,
                "$limit": limit,
                "$offset": offset
            }
            if location:
                params["locationabbr"] = location

            response = requests.get(API_URL, headers=HEADERS, params=params)

            if response.status_code == 200:
                data = response.json()
                if not data:
                    break  # no more records
                all_results.extend(data)
                print(f"  +{len(data)} records at offset {offset}")
                offset += limit
            else:
                print(f"Failed: {response.status_code} | {response.text}")
                break

    with open(CACHE_FILE, "w") as f:
        json.dump(all_results, f, indent=2)

    print(f"\nSaved {len(all_results)} total records to {CACHE_FILE}")

if __name__ == "__main__":
    fetch_disease_data(topics=["Diabetes", "Obesity", "Heart Disease"])
