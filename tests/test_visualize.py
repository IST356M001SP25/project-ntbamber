import pandas as pd
from assignment_code.visualize import plot_distribution_by_group, plot_mortality_by_state

def test_plot_distribution_by_group_runs():
    df = pd.DataFrame({
        "state": ["NY", "CA"],
        "year": [2020, 2020],
        "value": [10.1, 9.5],
        "group": ["Male", "Female"],
        "group_type": ["Sex", "Sex"],
        "datavalueunit": ["%", "%"],
        "question": ["Percent of adults aged 18 years and older who have been told by a doctor that they have diabetes"] * 2
    })
    fig = plot_distribution_by_group(df, state="NY", year=2020, group_type="Sex")
    assert fig.data

def test_plot_mortality_by_state_runs():
    df = pd.DataFrame({
        "state": ["NY", "CA"],
        "year": [2020, 2020],
        "value": [18.2, 21.4],
        "group": ["Male", "Female"],
        "group_type": ["Sex", "Sex"],
        "datavalueunit": ["cases per 100,000", "cases per 100,000"],
        "datavaluetype": ["Age-adjusted Rate", "Age-adjusted Rate"],
        "question": ["Diabetes mortality among all people, underlying or contributing cause"] * 2
    })
    fig = plot_mortality_by_state(df, year=2020, group="Male")
    assert fig.data
