import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_plotly_events import plotly_events

import requests

import uuid


import plotly.graph_objects as go

import folium
from streamlit_folium import st_folium

import pydeck as pdk

# Generate a random UUID v4 object
x_transactionid = str(uuid.uuid4())

x_consumer_id = "76765b63d1a2646c786d6714e6209707"
##print(x_transactionid)            # e.g., 'fbd204a7-318e-4dd3-86e0-e6d524fc3f98'
##print(type(x_transactionid))  


def get_price_vic2():
    headers = {
    "User-Agent": "MyApp/1.0",
    "x-consumer-id": x_consumer_id,
    "x-transactionid": x_transactionid
    }
    
    try:
        response = requests.get("https://api.fuel.service.vic.gov.au/open-data/v1/fuel/prices",headers=headers)
        ##print(response.raise_for_status())
        status_code = response.status_code
        ##print(status_code)
        ##print(response.json()["results"][0])
        ##print(response.json()["fuelPriceDetails"][1]["fuelStation"])
        ##print(response.json()["fuelPriceDetails"][0])
        ##print(len(response.json()["fuelPriceDetails"]))
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("request failed", e)    

    
    rows = []
    for entry in data["fuelPriceDetails"]:
        station = entry["fuelStation"]
        for fuel in entry["fuelPrices"]:
            rows.append({
                # Station fields
                "station_id":        station["id"],
                "station_name":      station["name"],
                "brand_id":          station["brandId"],
                "address":           station["address"],
                "contact_phone":     station["contactPhone"],
                "latitude":          station["location"]["latitude"],
                "longitude":         station["location"]["longitude"],
                "station_updatedAt": entry["updatedAt"],
                # Fuel price fields
                "fuel_type":         fuel["fuelType"],
                "price":             fuel["price"],
                "is_available":      fuel["isAvailable"],
                "price_updatedAt":   fuel["updatedAt"],
            })

    df = pd.DataFrame(rows)
    
    ##df['postcode'] = df['address'].str.split(',').str[-1].str.strip()
    ##df['suburb'] = df['address'].str.split(',').str[-2].str.strip().str.capitalize()
    ##df[['street', 'suburb', 'postcode']] = df['address'].str.split(',', expand=True).apply(lambda x: x.str.strip())
    df['address_len'] = df['address'].str.split(',').str.len()
    # 1. Split the address into a list
    parts = df['address'].str.split(',')

    def extract_street(p_list):
        length = len(p_list)
        
        # If Length is 5: Combine indices 0, 1, and 2
        if length == 5:
            return ", ".join(p_list[0:3]).strip()
        
        # If Length is 4: Combine indices 0 and 1
        elif length == 4:
            return ", ".join(p_list[0:2]).strip()
        
        # Default (Length 3 or other): Just take the first part
        else:
            return p_list[0].strip()

    # Apply the function to create the 'street' column
    df['street'] = parts.apply(extract_street)

    # Always get Suburb and Postcode from the end
    df['suburb'] = parts.str[-2].str.strip().str.upper()
    df['postcode'] = parts.str[-1].str.strip()

    ##print(df[['street', 'suburb', 'postcode']])

    # ── Save to CSV ───────────────────────────────────────────────────────────────
    ##df.to_csv("api_vic_fuel_prices.csv", index=False, encoding="utf-8")
    ##df.to_csv("fuel_prices.csv", index=False, encoding="utf-8-sig")

    ##print(df.to_string(index=False))
    ##unique_count = df['station_id'].nunique()

    return df
    ##print(f"Total Unique Records: {unique_count}")  

##get_price_vic2()


df = get_price_vic2()
##print(df.columns)
df["price_updatedAt_au"] = pd.to_datetime(df["price_updatedAt"])
df["price_updatedAt_au"] = df["price_updatedAt_au"].dt.tz_convert('Australia/Sydney')
fil_sub = ['BERWICK','BEACONSFIELD',
           'CRANBOURNE','CRANBOURNE NORTH','CRANBOURNE SOUTH','CRANBOURNE EAST',
           'NARRE WARREN','NARRE WARREN NORTH','NARRE WARREN SOUTH',
           'CLYDE','CLYDE NORTH',
           'HALLAM','EUMEMMERRING','HAMPTON PARK'
           ]
filtered_df = df[
    (df["is_available"] == True) &
    (df['suburb'].isin(fil_sub))
]

CASEY_CENTER = {"lat": -38.0554, "lon": 145.2998}

# Aggregate fuel types and prices for each station into a single string for hover
# Also get the most recent update time for the station
station_fuel_details = filtered_df.groupby(['station_id', 'station_name', 'address', 'latitude', 'longitude', 'postcode']).apply(
    lambda x: pd.Series({
        'all_fuel_prices_available': '<br>' + '<br>'.join([f"{row['fuel_type']}: {row['price']}" for index, row in x.iterrows()]),
        'price_updatedAt_au': x['price_updatedAt_au'].max() # Get the most recent update time for the station
    }), include_groups=False
).reset_index()

st.set_page_config(
    page_title="Servo",
    page_icon="🍁",
    layout="wide",
)

df_P95 = filtered_df[filtered_df['fuel_type'] == 'P95']
df_P95_top3 = df_P95[['station_name','price','address','latitude', 'longitude',"price_updatedAt_au",'station_id']].sort_values("price", ascending=True).head(3)
with st.sidebar:
    st.markdown("### 🔎 Filters")
   
    f_address  = st.selectbox('Address',df_P95_top3["address"].unique().tolist())
    
st.write(f_address)
df_top_3 = df_P95_top3['station_id'].unique().tolist()
new_df = filtered_df[filtered_df['station_id'].isin(df_top_3)].sort_values("station_id", ascending=True)
##st.write(df_top_3)
with st.expander("Click to view table"):
    st.dataframe(new_df[['station_name','fuel_type','price','address']],hide_index=True)
station_coords = df[(df['address'] == f_address)& (df['fuel_type'] == 'P95')][['latitude', 'longitude']]
st.write(station_coords)
# if not station_coords.empty:
#     st.map(station_coords)
st.dataframe(df_P95_top3[['station_name','price','address','latitude', 'longitude',"price_updatedAt_au"]],hide_index=True)

st.dataframe(station_fuel_details[['station_name', 'address', 'latitude', 'longitude', 'postcode']],hide_index=True)
# This aggregated DataFrame (station_fuel_details) now has one row per unique station
station_plot_df = station_fuel_details.copy()






# --- PREP DATA ---
df = station_plot_df.copy()

# # Ensure proper types
# df["latitude"] = df["latitude"].astype(float)
# df["longitude"] = df["longitude"].astype(float)
# df["price_updatedAt_au"] = pd.to_datetime(
#     df["price_updatedAt_au"], errors="coerce"
# ).dt.strftime("%d %b %Y %I:%M %p")

# # --- SIDEBAR FILTERS ---
# st.sidebar.header("🔎 Filters")

# postcode_filter = st.sidebar.multiselect(
#     "Filter by Postcode",
#     options=sorted(df["postcode"].dropna().unique())
# )

# fuel_filter = st.sidebar.text_input(
#     "Filter Fuel Type (e.g. U91, Diesel)"
# )

# # Apply filters
# if postcode_filter:
#     df = df[df["postcode"].isin(postcode_filter)]

# if fuel_filter:
#     df = df[df["all_fuel_prices_available"].str.contains(fuel_filter, case=False, na=False)]

# # --- MAP ---
# fig = px.scatter_mapbox(
#     df,
#     lat="latitude",
#     lon="longitude",
#     hover_name="station_name",
#     hover_data={
#         "address": True,
#         "postcode": True,
#         "price_updatedAt_au": True,
#         "latitude": False,
#         "longitude": False
#     },
#     zoom=11,
#     height=550
# )

# fig.update_layout(
#     mapbox_style="open-street-map",
#     margin={"r":0,"t":0,"l":0,"b":0}
# )

# # --- CLICK EVENTS ---
# selected_points = plotly_events(fig, click_event=True, hover_event=False)

# st.plotly_chart(fig, use_container_width=True)

# # --- HANDLE CLICK ---
# if selected_points:
#     idx = selected_points[0]["pointIndex"]
#     selected_station = df.iloc[idx]

#     st.markdown("## 📍 Selected Station")

#     col1, col2 = st.columns(2)

#     with col1:
#         st.markdown(f"**Name:** {selected_station['station_name']}")
#         st.markdown(f"**Address:** {selected_station['address']}")
#         st.markdown(f"**Postcode:** {selected_station['postcode']}")

#     with col2:
#         st.markdown(f"**Last Updated:** {selected_station['price_updatedAt_au']}")
#         st.markdown(f"**Fuel Available:** {selected_station['all_fuel_prices_available']}")

#     st.markdown("### 📊 Full Details")
#     st.dataframe(
#         pd.DataFrame(selected_station).T,
#         use_container_width=True
#     )

# else:
#     st.info("👆 Click on a station on the map to view details")

# # --- OPTIONAL TABLE ---
# with st.expander("📋 View Filtered Stations"):
#     st.dataframe(df, use_container_width=True)


df = station_plot_df.copy()

df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

df = df.dropna(subset=["latitude", "longitude"])

st.write("Rows after cleaning:", len(df))

# fig = px.scatter_mapbox(
#     df,
#     lat="latitude",
#     lon="longitude",
#     hover_name="station_name",
#     zoom=10,
#     height=500
# )

# fig.update_layout(mapbox_style="open-street-map")

# fig.update_traces(marker=dict(size=10))

# st.plotly_chart(fig, use_container_width=True)

st.write("Columns:", df.columns)
st.write("Row count:", len(df))
st.write(df[["latitude", "longitude"]].head(10))

test_df = pd.DataFrame({
    "latitude": [-37.8136, -37.82],
    "longitude": [144.9631, 144.97],
    "station_name": ["Test 1", "Test 2"]
})

fig = px.scatter_mapbox(
    test_df,
    lat="latitude",
    lon="longitude",
    hover_name="station_name",
    zoom=10,
    height=500
)

fig.update_layout(mapbox_style="open-street-map")

st.plotly_chart(fig, use_container_width=True)