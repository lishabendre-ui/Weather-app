import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "data/weather.db"

# Set browser page title and layout
st.set_page_config(page_title="Weather Data Pipeline Dashboard", layout="wide")

def load_data():
    """Load weather data joined with cities from SQLite."""
    conn = sqlite3.connect(DB_PATH)
    query = """
    SELECT 
        c.city_name,
        w.date,
        w.temp_max_c,
        w.temp_min_c,
        w.precipitation_mm
    FROM weather_daily w
    JOIN cities c ON w.city_id = c.city_id
    ORDER BY w.date ASC;
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    df["date"] = pd.to_datetime(df["date"])
    return df

# Main dashboard app
def main():
    st.title("🌤️ Weather Data Pipeline Dashboard")
    st.write("An end-to-end data pipeline: Open-Meteo API ➔ Python (pandas) ➔ SQLite ➔ Streamlit.")
    
    # Load data from SQLite
    df = load_data()
    
    if df.empty:
        st.warning("No data found in the database! Please run the pipeline first.")
        return

    # Top KPI Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Cities", df["city_name"].nunique())
    with col2:
        st.metric("Total Days Tracked", df["date"].nunique())
    with col3:
        hottest_temp = df["temp_max_c"].max()
        hottest_city = df.loc[df["temp_max_c"] == hottest_temp, "city_name"].values[0]
        st.metric("Hottest City", f"{hottest_city} ({hottest_temp}°C)")
    with col4:
        total_rain = round(df["precipitation_mm"].sum(), 1)
        st.metric("Total Rainfall", f"{total_rain} mm")

    st.divider()

    # City Selector Dropdown
    cities = sorted(df["city_name"].unique())
    selected_city = st.selectbox("Select a City to View Forecast:", cities)

    # Filter data for selected city
    city_df = df[df["city_name"] == selected_city].copy()

    # Layout for charts
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader(f"🌡️ Temperature Trends: {selected_city}")
        # Chart with Max and Min temps over time
        temp_chart_data = city_df.set_index("date")[["temp_max_c", "temp_min_c"]]
        st.line_chart(temp_chart_data)

    with chart_col2:
        st.subheader("🌧️ Total Rainfall Comparison (All Cities)")
        rain_summary = df.groupby("city_name")["precipitation_mm"].sum().reset_index()
        st.bar_chart(rain_summary.set_index("city_name"))

    st.divider()

    # Raw Data Table with expandable section
    with st.expander("🔍 View Raw Database Records"):
        st.dataframe(df, use_container_width=True)

if __name__ == "__main__":
    main()