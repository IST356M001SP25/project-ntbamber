import pandas as pd
import plotly.express as px

def plot_distribution_by_group(df, state=None, year=None, group_type="Sex"): #def function
    plot_df = df.copy() #load data

    if state: #state filter
        plot_df = plot_df[plot_df["state"] == state]
    if year: #year filter
        plot_df = plot_df[plot_df["year"] == year]

    # Filter to a single group type
    plot_df = plot_df[plot_df["group_type"] == group_type]

    # Clean values
    plot_df = plot_df[(plot_df["value"] > 0) & (plot_df["value"] < 100)]
    plot_df = plot_df[plot_df["group"].notna()]

    # Extract unit for axis label
    unit_label = plot_df["datavalueunit"].dropna().unique()
    y_label = unit_label[0] if len(unit_label) == 1 else "Reported Value"

    # Create a box plot
    fig = px.box(
        plot_df,
        x="group",
        y="value",
        title=f"Diabetes Rate Distribution by {group_type}"
              f"{' in ' + state if state else ''}"
              f"{' for ' + str(year) if year else ''}",
        labels={"value": y_label},
        points=False
    )
    fig.update_layout(xaxis_title=group_type, yaxis_title=y_label)
    return fig #Return plot

def plot_mortality_by_state(df, year=None, group=None): #def function
    plot_df = df.copy() #load data

    # Filter to only diabetes mortality entries
    plot_df = plot_df[
        (plot_df["question"] == "Diabetes mortality among all people, underlying or contributing cause") &
        (plot_df["datavalueunit"] == "cases per 100,000") &
        (plot_df["datavaluetype"].str.contains("Age-adjusted", case=False, na=False))
    ]

    if year: #year filter
        plot_df = plot_df[plot_df["year"] == year]
    if group: #group filter
        plot_df = plot_df[plot_df["group"] == group]

    # Remove national-level summary
    plot_df = plot_df[plot_df["state"] != "United States"]

    # Drop invalid rows
    plot_df = plot_df[(plot_df["value"] > 0) & (plot_df["value"] < 1000)]

    # group by state and calculate mean & sort values
    avg_df = (
        plot_df.groupby("state", as_index=False)
        .agg({"value": "mean"})
        .sort_values("value", ascending=False)
    )
    # Create a bar plot
    fig = px.bar(
        avg_df,
        x="state",
        y="value",
        title=f"Diabetes Mortality Rate by State (Age-Adjusted){' - ' + str(year) if year else ''}",
        labels={"value": "Deaths per 100,000"}
    )
    fig.update_layout(xaxis_tickangle=-45)
    return fig #Return plot

