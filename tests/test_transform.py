import os
import pandas as pd
from assignment_code.transform import load_json, clean_diabetes_data, save_clean_csv, OUTPUT_FILE

def test_clean_diabetes_data_structure():
    raw_data = [{
        "locationabbr": "NY",
        "locationdesc": "New York",
        "yearstart": 2020,
        "yearend": 2020,
        "topic": "Diabetes",
        "question": "Percent of adults...",
        "datavalue": "9.5",
        "datavaluetype": "Crude Rate",
        "datavalueunit": "%",
        "stratificationcategory1": "Sex",
        "stratification1": "Male"
    }]
    df = clean_diabetes_data(raw_data)
    expected_cols = {"state", "year", "value", "group", "group_type"}
    assert expected_cols.issubset(df.columns)
    assert not df.empty

def test_save_creates_file(tmp_path):
    df = pd.DataFrame({
        "state": ["NY"],
        "year": [2020],
        "value": [9.5],
        "group": ["Male"],
        "group_type": ["Sex"]
    })
    path = tmp_path / "test_output.csv"
    save_clean_csv(df, output_path=str(path))
    assert path.exists()
