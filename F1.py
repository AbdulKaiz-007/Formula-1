import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
@st.cache_data(persist="disk")
def load_data():
    races = pd.read_csv('races.csv')
    results = pd.read_csv('results.csv')
    drivers = pd.read_csv('drivers.csv')
    return races, results, drivers

races, results, drivers = load_data()

# Merge datasets
results_merged = results.merge(races[['raceId', 'year']], on='raceId')
results_merged = results_merged.merge(drivers[['driverId', 'forename', 'surname', 'nationality']], on='driverId')
results_merged['driver_name'] = results_merged['forename'] + ' ' + results_merged['surname']

# Streamlit App
st.title("F1 Driver Performance Analysis")
st.markdown("### A comprehensive analysis of F1 drivers' performance")

# Set page background color
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Driver selection sidebar
st.sidebar.header("Driver Selection")
driver_names = results_merged['driver_name'].unique()
selected_driver = st.sidebar.selectbox("Select Driver:", driver_names)

# Filter data based on selected driver
filtered_data = results_merged[results_merged['driver_name'] == selected_driver]

# Display driver information
st.header(f"Driver Information: {selected_driver}")
if not filtered_data.empty:
    driver_info = filtered_data[['driverId', 'driver_name', 'nationality']].iloc[0]
    st.write(driver_info)
else:
    st.write("No data available for this driver")

# Display driver performance metrics
st.header("Performance Metrics")
if not filtered_data.empty:
    st.metric("Total Races", filtered_data.shape[0], delta_color="off")
    average_position = filtered_data['positionOrder'].mean()
    st.metric("Average Pitstop Time", f"{average_position:.2f}", delta_color="off")
else:
    st.write("No data available for this driver")

# Display race results table
st.subheader("Race Results")
if not filtered_data.empty:
    columns_to_display = ['year', 'positionOrder']
    if all(col in filtered_data.columns for col in columns_to_display):
        st.dataframe(filtered_data[columns_to_display].style.set_properties(**{'background-color': 'white', 'color': 'black', 'border-color': 'black', 'border-width': '1px', 'border-style': 'solid'}))
    else:
        st.write("Some columns are missing from the data")
else:
    st.write("No data available for this driver")

# Add a pie graph
st.subheader("Races Won")
if not filtered_data.empty:
    wins = filtered_data[filtered_data['positionOrder'] == 1]  # Filter for wins
    wins_count = wins['raceId'].nunique()  # Count unique races won
    fig = px.pie(values=[wins_count, filtered_data.shape[0]-wins_count], names=['Wins', 'Other'], title='Race Wins')
    fig.update_layout({'plot_bgcolor': 'rgba(0,0,0,0)', 'paper_bgcolor': 'rgba(0,0,0,0)', 'font': {'color': 'black'}})
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write("No data available for this driver")

# Add a footer
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f5f5f5;
        color: #333;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
    © 2024 - Developed by Abdul Kaiz
    </div>
    """,
    unsafe_allow_html=True
)