import requests
import os
import json

API_URL = "https://data.cdc.gov/resource/hksd-2xuw.json" #API Url
CACHE_FILE = "cache/raw_disease_data.json" # Cache file path
APP_TOKEN = "fWXQM3KDN7DyxSZs1E9vvy5Rh"  #api token

HEADERS = {"X-App-Token": APP_TOKEN} #headers

def fetch_disease_data(topics=None, location=None, limit=1000): #fetch disease data, default limit is 1000
    os.makedirs("cache", exist_ok=True) # Create cache directory if it doesn't exist
    all_results = [] # List to store all results
    for topic in topics or ["Diabetes"]: # Default to "Diabetes" if no topics are provided
        offset = 0 #intialize offset
        #print(f"\nFetching: {topic} data...") #feedback
        while True: # Loop until no more records are found
            params = {"topic": topic, "$limit": limit, "$offset": offset} #parameters for API request
            if location: # If location is provided, add it to the parameters
                params["locationabbr"] = location
            response = requests.get(API_URL, headers=HEADERS, params=params) # Make the API request
            if response.status_code == 200: # Check if the request was successful
                data = response.json() # Parse the response JSON
                if not data: # If no data is returned, break the loop
                    break  # exit loop if no data
                all_results.extend(data) # Add the data to the results list
                #print(f"  +{len(data)} records at offset {offset}") #feedback
                offset += limit # Increment the offset for the next request
            else: # If the request failed, print the error and break the loop
                print(f"Failed: {response.status_code} | {response.text}") #feedback
                break # exit loop
    with open(CACHE_FILE, "w") as f: # Save the results to the cache file
        json.dump(all_results, f, indent=2) # Save the data in JSON format
    print(f"\nSaved {len(all_results)} total records to {CACHE_FILE}") #feedback
if __name__ == "__main__": # Main function to run the script
    fetch_disease_data(topics=["Diabetes"]) # Fetch data for "Diabetes" topic
