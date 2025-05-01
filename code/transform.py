import json
import pandas as pd
import os

INPUT_FILE = "cache/raw_disease_data.json"
OUTPUT_FILE = "cache/cleaned_diabetes_data.csv"

def load_json(path=INPUT_FILE):
    with open(path, "r") as f:
        return json.load(f)

def clean_diabetes_data(records):
    df = pd.DataFrame(records)

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

    return df

def save_clean_csv(df, output_path=OUTPUT_FILE):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Saved cleaned data to {output_path} ({len(df)} rows)")

if __name__ == "__main__":
    data = load_json()
    clean_df = clean_diabetes_data(data)
    save_clean_csv(clean_df)
