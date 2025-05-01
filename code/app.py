# code/app.py
import streamlit as st
import pandas as pd
from visualize import plot_distribution_by_group, plot_mortality_by_state

# --- Load Data ---
DATA_PATH = "cache/cleaned_diabetes_data.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

df = load_data()

# --- Sidebar Filters ---
st.sidebar.title("Filter Options")

# Dynamic filter options
states = sorted(df["state"].dropna().unique())
groups = sorted(df["group"].dropna().unique())
group_types = sorted(df["group_type"].dropna().unique())
year_range = (int(df["year"].min()), int(df["year"].max()))

# Filter widgets
selected_state = st.sidebar.selectbox("Select a state:", ["All"] + states)
selected_group = st.sidebar.selectbox("Select a demographic group:", ["All"] + groups)
selected_group_type = st.sidebar.selectbox("Select group type:", group_types)
selected_year = st.sidebar.slider("Select a year:", *year_range, step=1)

# Apply filters
state_filter = None if selected_state == "All" else selected_state
group_filter = None if selected_group == "All" else selected_group

# --- Title ---
st.title("🩺 Diabetes Data Explorer")
st.markdown("Explore CDC-reported diabetes prevalence and mortality across U.S. states and demographics.")

# --- Plot 1: Box plot by group ---
st.subheader("📊 Diabetes Rate Distribution by Group")
st.plotly_chart(
    plot_distribution_by_group(
        df,
        state=state_filter,
        year=selected_year,
        group_type=selected_group_type
    ),
    use_container_width=True
)

# --- Plot 2: Mortality bar chart ---
st.subheader("🪦 Diabetes Mortality Rate by State")
st.plotly_chart(
    plot_mortality_by_state(
        df,
        year=selected_year,
        group=group_filter
    ),
    use_container_width=True
)

# --- Optional Data Preview ---
with st.expander("🔍 Show filtered data table"):
    filtered_df = df.copy()
    if state_filter:
        filtered_df = filtered_df[filtered_df["state"] == state_filter]
    if group_filter:
        filtered_df = filtered_df[filtered_df["group"] == group_filter]
    st.dataframe(filtered_df)
