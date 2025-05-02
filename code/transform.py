import json
import pandas as pd
import os

INPUT_FILE = "cache/raw_disease_data.json" # Path to the raw JSON data
OUTPUT_FILE = "cache/cleaned_diabetes_data.csv" # Path to save the cleaned CSV data

def load_json(path=INPUT_FILE): # Load the JSON data
    with open(path, "r") as f: # Open the file in read mode
        return json.load(f) # Load the JSON data into a Python object

def clean_diabetes_data(records): #function def
    df = pd.DataFrame(records) # Convert JSON to DataFrame
    # Keep only relevant fields
    df = df[[
        "locationabbr", "locationdesc", "yearstart", "yearend",
        "topic", "question", "datavalue", "datavaluetype",
        "datavalueunit", "stratificationcategory1", "stratification1"
    ]]
    # Rename for clarity
    df = df.rename(columns={
        "locationabbr": "state_abbr",
        "locationdesc": "state",
        "yearstart": "year",
        "datavalue": "value",
        "stratificationcategory1": "group_type",
        "stratification1": "group"
    })
    # Drop rows with missing or non-numeric values
    df = df[df["value"].notna()]
    df["value"] = pd.to_numeric(df["value"], errors="coerce")
    df = df.dropna(subset=["value"])
    # Convert year to integer
    df["year"] = pd.to_numeric(df["year"], errors="coerce").astype("Int64")
    return df # Cleaned DataFrame

def save_clean_csv(df, output_path=OUTPUT_FILE): # Save the cleaned DataFrame to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True) # Create directory if it doesn't exist
    df.to_csv(output_path, index=False) # Save DataFrame to CSV
    print(f"Saved cleaned data to {output_path} ({len(df)} rows)") # feedback

if __name__ == "__main__": # Main function to run the script
    data = load_json() # Load the JSON data
    clean_df = clean_diabetes_data(data) # Clean the data
    save_clean_csv(clean_df) # Save the cleaned data to CSV
