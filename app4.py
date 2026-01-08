import streamlit as st

st.set_page_config(page_title="NYC Taxi Revenue Analytics", layout="wide")
st.title("NYC Taxi Revenue Analytics")


try:
    conn = st.connection("snowflake")
except Exception as e:
    st.error("Could not create Snowflake connection.")
    st.exception(e)
    st.stop()


try:
    boroughs_df = conn.query("""
        SELECT DISTINCT borough
        FROM NYC_TAXI_DB.ANALYTICS.HIGH_TIP_BOROUGH_STATS
        WHERE borough IS NOT NULL
        ORDER BY borough
    """)
except Exception as e:
    st.error("Failed to load borough options.")
    st.exception(e)
    st.stop()

boroughs_df.columns = [c.lower() for c in boroughs_df.columns]
options = ["All"] + list(boroughs_df["borough"].unique())

borough_filter = st.sidebar.selectbox("Select a Borough", options)

normalize_hourly = st.sidebar.checkbox("Normalize hourly trips (pattern view)", value=False)


safe_borough = borough_filter.replace("'", "''")


base_borough_sql = """
    SELECT borough, total_revenue, trip_count
    FROM NYC_TAXI_DB.ANALYTICS.BOROUGH_REVENUE_STATS_GOLD
"""

if borough_filter != "All":
    borough_query = f"""
        {base_borough_sql}
        WHERE borough = '{safe_borough}'
        ORDER BY total_revenue DESC
    """
else:
    borough_query = f"""
        {base_borough_sql}
        ORDER BY total_revenue DESC
    """

try:
    df = conn.query(borough_query)
except Exception as e:
    st.error("Snowflake query failed for borough stats.")
    st.exception(e)
    st.stop()

df.columns = [c.lower() for c in df.columns]


total_revenue_all = df["total_revenue"].sum()
total_trips_all = df["trip_count"].sum()

m1, m2 = st.columns(2)
with m1:
    st.metric("Total Revenue", f"${total_revenue_all:,.0f}")
with m2:
    st.metric("Total Trips", f"{total_trips_all:,.0f}")

st.divider()

base_hourly_sql = """
    SELECT borough, pickup_hour, hour_label, total_trips, total_fare
    FROM NYC_TAXI_DB.ANALYTICS.hourly_patterns
"""

if borough_filter != "All":
    hourly_query = f"""
        {base_hourly_sql}
        WHERE borough = '{safe_borough}'
        ORDER BY pickup_hour
    """
else:
    hourly_query = f"""
        {base_hourly_sql}
        ORDER BY pickup_hour
    """

try:
    hourly_df = conn.query(hourly_query)
except Exception as e:
    st.error("Snowflake query failed for hourly patterns.")
    st.exception(e)
    st.stop()

hourly_df.columns = [c.lower() for c in hourly_df.columns]


if borough_filter == "All":
    hourly_df = (
        hourly_df
        .groupby(["pickup_hour", "hour_label"], as_index=False)
        .agg(
            total_trips=("total_trips", "sum"),
            total_fare=("total_fare", "sum"),
        )
        .sort_values("pickup_hour")
    )


hourly_df["avg_fare"] = hourly_df["total_fare"] / hourly_df["total_trips"]


plot_hourly_df = hourly_df.copy()
if normalize_hourly and len(plot_hourly_df) > 0:
    max_trips = plot_hourly_df["total_trips"].max()
    if max_trips and max_trips > 0:
        plot_hourly_df["total_trips"] = plot_hourly_df["total_trips"] / max_trips


left, right = st.columns(2)

with left:
    st.subheader("Revenue by Borough")
    bar_df = df.set_index("borough")[["total_revenue"]]
    st.bar_chart(bar_df)

with right:
    st.subheader(f"Hourly Trip Pattern ({borough_filter})")
    line_df = plot_hourly_df.set_index("pickup_hour")[["total_trips"]]
    st.line_chart(line_df)

st.divider()
st.subheader("Borough Stats (Table)")
st.dataframe(df, use_container_width=True)


st.subheader("Revenue by Trip Type")

# Query the new view
type_df = conn.query("SELECT * FROM NYC_TAXI_DB.ANALYTICS.TRIP_TYPE_STATS")
type_df.columns = [c.lower() for c in type_df.columns]

# Create a layout with a chart 
c1, c2 = st.columns([1.5, 1])

with c1:
    # A horizontal bar chart 
    st.bar_chart(type_df.set_index("trip_type")["total_revenue"])

with c2:
    # Show the average tip per trip type"
    st.write("Top Tipping Trip Types")
    st.dataframe(type_df[["trip_type", "avg_tip"]].sort_values("avg_tip", ascending=False))