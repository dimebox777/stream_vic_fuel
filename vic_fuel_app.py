import requests
import pandas as pd

import uuid

import streamlit as st
##import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

import folium
from streamlit_folium import st_folium

import pydeck as pdk

# Generate a random UUID v4 object
x_transactionid = str(uuid.uuid4())

x_consumer_id = "76765b63d1a2646c786d6714e6209707"
##print(x_transactionid)            # e.g., 'fbd204a7-318e-4dd3-86e0-e6d524fc3f98'
##print(type(x_transactionid))  




SUPABASE_URL="https://oxasehqygbnohwzbdbgp.supabase.co"
SUPABASE_KEY=""

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}



def new_post(user_id: int, title:str, content: str):

    headers = {
    "Content-Type": "application/json"
    }

    json={
            "title":title,
            "content":content,
            "user_id":user_id

    }
    try:
        response = requests.post("http://127.0.0.1:8000/api/posts",json=json,headers=headers)
        ##response = requests.post("https://fastapi-blog-5j9q.onrender.com//api/posts",json=json,headers=headers)
        print(response.status_code)
        print(response.json())
    except requests.exceptions.RequestException as e:
        print("request failed", e)

##new_post(3,"6 new title here for barry","6 new content here for barry")

def get_price_vic():
    headers = {
    "User-Agent": "MyApp/1.0",
    "x-consumer-id": x_consumer_id,
    "x-transactionid": x_transactionid
    }
    
    try:
        response = requests.get("https://api.fuel.service.vic.gov.au/open-data/v1/fuel/prices",headers=headers)
        ##print(response.json()["results"][0])
        ##print(response.json()["fuelPriceDetails"][1]["fuelStation"])
        print(response.json()["fuelPriceDetails"][0])
        print(len(response.json()["fuelPriceDetails"]))
        data = response.json()
    except requests.exceptions.RequestException as e:
        print("request failed", e)    


    df = pd.json_normalize(
    data['fuelPriceDetails'], 
    record_path=['fuelPrices'], 
    meta=[
        ['fuelStation', 'id'], 
        ['fuelStation', 'name'], 
        ['fuelStation', 'brandId'], 
        ['fuelStation', 'address'], 
        ['fuelStation', 'location', 'latitude'], 
        ['fuelStation', 'location', 'longitude'],
        'updatedAt'
    ],
    record_prefix='price_'
    )

    # 2. Clean up column names for a better CSV header
    df.columns = [c.replace('fuelStation.', '').replace('.', '_') for c in df.columns]

    # 3. Export to CSV
    df.to_csv('melbourne_fuel_prices.csv', index=False)

    print("CSV Created successfully!")
    print(df.head())

##get_price_vic()



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

def get_price_vic_chk():
    headers = {
    "User-Agent": "MyApp/1.0",
    "x-consumer-id": x_consumer_id,
    "x-transactionid": x_transactionid
    }
    
    try:
        response = requests.get("https://api.fuel.service.vic.gov.au/open-data/v1/fuel/prices",headers=headers)
        ##print(response.json()["results"][0])
        ##print(response.json()["fuelPriceDetails"][1]["fuelStation"])
        print(response.json()["fuelPriceDetails"][1])
        print(len(response.json()["fuelPriceDetails"]))
        ##data = response.json()["fuelPriceDetails"]
        ##df = pd.read_json(data)
    except requests.exceptions.RequestException as e:
        print("request failed", e)    
    ##print(df.head())
##get_price_vic_chk()



def get_price_vic3():
    headers = {
        "User-Agent": "MyApp/1.0",
        "x-consumer-id": x_consumer_id,
        "x-transactionid": x_transactionid
    }
    
    try:
        response = requests.get("https://api.fuel.service.vic.gov.au/open-data/v1/fuel/prices", headers=headers)
        response.raise_for_status() # Check for HTTP errors
        
        raw_data = response.json()
        
        # Use json_normalize to flatten the nested 'fuelPrices' list
        df = pd.json_normalize(
            raw_data["fuelPriceDetails"], 
            record_path=["fuelPrices"], 
            meta=[
                ["fuelStation", "name"], 
                ["fuelStation", "address"],
                ["fuelStation", "id"],
                "updatedAt"
            ],
            record_prefix="price_"
        )
        
        print(f"Successfully processed {len(df)} price records.")
        print(df.head())
        return df

    except requests.exceptions.RequestException as e:
        print("Request failed:", e)
        return None

# Execute
##df = get_price_vic3()
##print(df.head())


def get_fuel_vic_station():
    headers = {
    "User-Agent": "MyApp/1.0",
    "x-consumer-id": x_consumer_id,
    "x-transactionid": x_transactionid
    }
    
    try:
        response = requests.get("https://api.fuel.service.vic.gov.au/open-data/v1/fuel/reference-data/stations",headers=headers)
        ##print(response.json()["results"][0])
        ##print(response.json()["fuelPriceDetails"][1]["fuelStation"])
        dd = response.json()
        # Method A: Using list conversion (easiest)
        first_column = list(dd.keys())[0]

        # Method B: Using an iterator (more memory efficient)
        #first_column = next(iter(dd))

        f_column = list(dd.keys())
        print(dd.keys())
        print(first_column) # Output: e.g., 'id'
        ##print(f_column)


        ee = response.json()["fuelStations"][0] # Get the first station record

        # Get all keys except the first one
        ##all_cols_except_first = list(ee.keys())[1:]
        all_cols_except_first = list(ee.keys())

        print(all_cols_except_first) 



        ##print(response.json()["fuelStations"][0])
        ##print(len(response.json()["fuelStations"]))
        data = response.json()["fuelStations"]
        ##df = pd.DataFrame(data)
        df = pd.json_normalize(data,sep="_")
        ##print(df.columns)
    except requests.exceptions.RequestException as e:
        print("request failed", e)

##get_fuel_vic_station()


def get_fuel_brands():
    headers = {
    "User-Agent": "MyApp/1.0",
    "x-consumer-id": x_consumer_id,
    "x-transactionid": x_transactionid
    }
    
    try:
        response = requests.get("https://api.fuel.service.vic.gov.au/open-data/v1/fuel/reference-data/brands",headers=headers)
        ##print(response.json()["results"][0])
        ##print(response.json()["fuelPriceDetails"][1]["fuelStation"])
        print(response.json()["brands"])
        print(len(response.json()["brands"]))
        ##data = response.json()["fuelPriceDetails"]
        ##df = pd.read_json(data)
    except requests.exceptions.RequestException as e:
        print("request failed", e)
    df = pd.DataFrame(response.json()["brands"])
    print(df.head())
    print(df["name"].value_counts())
    df.to_csv("api_vic_fuel_brands.csv", index=False, encoding="utf-8")
    
##get_fuel_brands()






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

# # Diagnostic prints to verify dataframes
# print(f"Number of rows in original filtered_df: {len(filtered_df)}")
# print(f"Number of unique stations in filtered_df: {filtered_df['station_id'].nunique()}")
# print(f"Number of rows in station_plot_df (one per station): {len(station_plot_df)}")
# print("Sample of station_plot_df:")
# print(station_plot_df[['station_name', 'postcode', 'all_fuel_prices_available']].head())


# ##st.markdown(df['suburb'].unique())
# ## Create a scatter map using the aggregated station data
# fig = px.scatter_mapbox(station_plot_df,
#                         lat="latitude",
#                         lon="longitude",
#                         hover_name="station_name", # Display station name on hover
#                         hover_data={
#                                     "address": True,
#                                     "postcode": False,
#                                     "price_updatedAt_au": True, # Include in hover_data
#                                     "all_fuel_prices_available": True, # New aggregated info for all fuel types and prices
#                                     "latitude": False,
#                                     "longitude": False
#                                     },
#                         labels={
#                                   "all_fuel_prices_available":"Fuel Available",
#                                   "price_updatedAt_au": 'Last Updated' # Rename in hover tooltip
#                                     },
#                         zoom=11,
#                         center=CASEY_CENTER,
#                         ##center={"lat": -38.05, "lon": 145.33},
#                         size_max=10,
#                         height=560,
#                         ##map_style="open-street-map",
#                         title="Fuel Stations in Victoria by Postcode")

# ##fig.update_layout(mapbox_style="open-street-map")
# fig.update_layout(
#         margin=dict(t=0, b=0, l=0, r=0),
#         coloraxis_colorbar=dict(
#             ##title=metric,
#             thickness=14,
#             len=0.6,
#             tickfont=dict(size=10),
#         ),
#         paper_bgcolor="rgba(0,0,0,0)",
#         mapbox_style="open-street-map"
#     )
# st.plotly_chart(fig,width='content', key="map_chart")
# ##fig.show()  

##option

# ## Before creating the map, verify your data
# st.write(f"Number of stations: {len(station_plot_df)}")
# st.write(f"Latitude range: {station_plot_df['latitude'].min()} to {station_plot_df['latitude'].max()}")
# st.write(f"Longitude range: {station_plot_df['longitude'].min()} to {station_plot_df['longitude'].max()}")
# st.write("Sample data:")
# st.dataframe(station_plot_df.head())

# fig = px.scatter_mapbox(station_plot_df,
#                         lat="latitude",
#                         lon="longitude",
#                         hover_name="station_name",
#                         hover_data={
#                             "address": True,
#                             "postcode": False,
#                             "price_updatedAt_au": True,
#                             "all_fuel_prices_available": True,
#                             "latitude": False,
#                             "longitude": False
#                         },
#                         labels={
#                             "all_fuel_prices_available": "Fuel Available",
#                             "price_updatedAt_au": 'Last Updated'
#                         },
#                         color="postcode",  # Color by postcode
#                         size=[12] * len(station_plot_df),  # Fixed size
#                         size_max=15,
#                         zoom=11,
#                         center=CASEY_CENTER,
#                         height=560,
#                         color_continuous_scale="Viridis",
#                         title="Fuel Stations in Victoria by Postcode")

# fig.update_layout(
#     margin=dict(t=0, b=0, l=0, r=0),
#     coloraxis_colorbar=dict(
#         thickness=14,
#         len=0.6,
#         tickfont=dict(size=10),
#     ),
#     paper_bgcolor="rgba(0,0,0,0)",
#     mapbox_style="open-street-map"
# )

# st.plotly_chart(fig, use_container_width=True, key="map_chart")







# # ##debug
# # # STEP 1: Debug your data first
# st.write("### Debug Information")
# st.write(f"DataFrame shape: {station_plot_df.shape}")
# st.write(f"Number of rows: {len(station_plot_df)}")
# st.write(f"Columns: {station_plot_df.columns.tolist()}")

# # Check for missing values
# st.write("Missing values:")
# st.write(station_plot_df[['latitude', 'longitude', 'station_name']].isnull().sum())

# # Show sample data
# st.write("Sample data (first 5 rows):")
# st.dataframe(station_plot_df.head())

# # Check data types
# st.write("Data types:")
# st.write(station_plot_df[['latitude', 'longitude']].dtypes)

# # Check coordinate ranges
# st.write(f"Latitude range: {station_plot_df['latitude'].min()} to {station_plot_df['latitude'].max()}")
# st.write(f"Longitude range: {station_plot_df['longitude'].min()} to {station_plot_df['longitude'].max()}")

# # STEP 2: Clean the data
# # Remove any rows with null coordinates
# station_plot_df_clean = station_plot_df.dropna(subset=['latitude', 'longitude']).copy()

# # Ensure coordinates are numeric
# station_plot_df_clean['latitude'] = pd.to_numeric(station_plot_df_clean['latitude'], errors='coerce')
# station_plot_df_clean['longitude'] = pd.to_numeric(station_plot_df_clean['longitude'], errors='coerce')

# # Remove any rows that became NaN after conversion
# station_plot_df_clean = station_plot_df_clean.dropna(subset=['latitude', 'longitude'])

# st.write(f"Clean data rows: {len(station_plot_df_clean)}")

# # STEP 3: Try the simplest possible map first
# st.write("### Test Map 1: Minimal Configuration")

# fig_test = px.scatter_mapbox(
#     station_plot_df_clean,
#     lat="latitude",
#     lon="longitude",
#     zoom=10,
#     height=600
# )

# fig_test.update_layout(mapbox_style="open-street-map")
# st.plotly_chart(fig_test, use_container_width=True)

# # STEP 4: Add basic customization
# st.write("### Test Map 2: With Markers")

# fig_test2 = px.scatter_mapbox(
#     station_plot_df_clean,
#     lat="latitude",
#     lon="longitude",
#     zoom=10,
#     height=600
# )

# fig_test2.update_traces(marker=dict(size=15, color='red'))
# fig_test2.update_layout(mapbox_style="open-street-map")
# st.plotly_chart(fig_test2, use_container_width=True)

# # STEP 5: Full version with all features
# st.write("### Full Map with All Features")

# CASEY_CENTER = {"lat": -38.05, "lon": 145.33}

# fig = px.scatter_mapbox(
#     station_plot_df_clean,
#     lat="latitude",
#     lon="longitude",
#     hover_name="station_name",
#     hover_data={
#         "address": True,
#         "price_updatedAt_au": True,
#         "all_fuel_prices_available": True,
#         "latitude": False,
#         "longitude": False
#     },
#     zoom=11,
#     center=CASEY_CENTER,
#     height=600
# )

# # Explicitly set marker properties
# fig.update_traces(
#     marker=dict(
#         size=15,
#         color='#0083B8',
#         opacity=0.8
#     ),
#     hovertemplate='<b>%{hovertext}</b><br>' +
#                   'Address: %{customdata[0]}<br>' +
#                   'Last Updated: %{customdata[1]}<br>' +
#                   'Fuel Available: %{customdata[2]}<br>' +
#                   '<extra></extra>'
# )

# fig.update_layout(
#     mapbox_style="open-street-map",
#     margin=dict(t=30, b=0, l=0, r=0),
#     title="Fuel Stations in Victoria by Postcode",
#     showlegend=False
# )

# st.plotly_chart(fig, use_container_width=True, key="map_chart")








#####
# # Prepare hover text
# hover_text = []
# for idx, row in station_plot_df_clean.iterrows():
#     hover_text.append(
#         f"<b>{row['station_name']}</b><br>" +
#         f"Address: {row['address']}<br>" +
#         f"Last Updated: {row['price_updatedAt_au']}<br>" +
#         f"Fuel Available: {row['all_fuel_prices_available']}"
#     )

# fig = go.Figure(go.Scattermapbox(
#     lat=station_plot_df_clean['latitude'],
#     lon=station_plot_df_clean['longitude'],
#     mode='markers',
#     marker=dict(
#         size=15,
#         color='#0083B8',
#         opacity=0.8
#     ),
#     text=hover_text,
#     hoverinfo='text'
# ))

# fig.update_layout(
#     mapbox=dict(
#         style="open-street-map",
#         center=dict(lat=-38.05, lon=145.33),
#         zoom=11
#     ),
#     margin=dict(t=30, b=0, l=0, r=0),
#     height=600,
#     title="Fuel Stations in Victoria by Postcode"
# )

# st.plotly_chart(fig, use_container_width=True)







# # Your CASEY_CENTER
# CASEY_CENTER = {"lat": -38.05, "lon": 145.33}

# # Create hover text manually for better control
# hover_texts = []
# for idx, row in station_plot_df.iterrows():
#     hover_text = (
#         f"<b>{row['station_name']}</b><br>"
#         f"Address: {row['address']}<br>"
#         f"Postcode: {row['postcode']}<br>"
#         f"Last Updated: {row['price_updatedAt_au']}<br>"
#         f"Fuel Available: {row['all_fuel_prices_available']}"
#     )
#     hover_texts.append(hover_text)

# # Create the map using graph_objects (more reliable than px)
# fig = go.Figure()

# fig.add_trace(go.Scattermapbox(
#     lat=station_plot_df['latitude'],
#     lon=station_plot_df['longitude'],
#     mode='markers',
#     marker=dict(
#         size=14,
#         color='#0083B8',
#         opacity=0.7
#     ),
#     text=hover_texts,
#     hoverinfo='text',
#     name='Fuel Stations'
# ))

# fig.update_layout(
#     mapbox=dict(
#         style="open-street-map",
#         center=CASEY_CENTER,
#         zoom=11
#     ),
#     height=560,
#     margin=dict(t=40, b=0, l=0, r=0),
#     title="Fuel Stations in Victoria by Postcode",
#     showlegend=False,
#     hovermode='closest'
# )

# st.plotly_chart(fig, use_container_width=True, key="map_chart")






# # Set Plotly config for GitHub deployment
# config = {
#     'displayModeBar': True,
#     'displaylogo': False,
#     'modeBarButtonsToRemove': ['pan2d', 'lasso2d']
# }

# # Create the map
# fig = go.Figure()

# fig.add_trace(go.Scattermapbox(
#     lat=station_plot_df['latitude'],
#     lon=station_plot_df['longitude'],
#     mode='markers',
#     marker=dict(size=14, color='#0083B8'),
#     text=station_plot_df['station_name'],
#     customdata=station_plot_df[['address', 'postcode', 'price_updatedAt_au', 'all_fuel_prices_available']],
#     hovertemplate=(
#         '<b>%{text}</b><br>' +
#         'Address: %{customdata[0]}<br>' +
#         'Postcode: %{customdata[1]}<br>' +
#         'Last Updated: %{customdata[2]}<br>' +
#         'Fuel Available: %{customdata[3]}<br>' +
#         '<extra></extra>'
#     )
# ))

# fig.update_layout(
#     mapbox=dict(
#         style="open-street-map",
#         center={"lat": -38.05, "lon": 145.33},
#         zoom=11
#     ),
#     height=560,
#     margin=dict(t=40, b=0, l=0, r=0),
#     title="Fuel Stations in Victoria by Postcode"
# )

# st.plotly_chart(fig, use_container_width=True, config=config, key="map_chart")


# # Absolute simplest version possible
# fig = px.scatter_mapbox(
#     station_plot_df,
#     lat="latitude",
#     lon="longitude",
#     text="station_name"
# )

# fig.update_traces(marker={'size': 20, 'color': 'red'})
# fig.update_layout(
#     mapbox={'style': "open-street-map", 'zoom': 11, 'center': {"lat": -38.05, "lon": 145.33}},
#     height=600
# )

# st.plotly_chart(fig)





# # Streamlit's map needs columns named 'lat' and 'lon'
# map_data = station_plot_df[['latitude', 'longitude', 'station_name']].copy()
# map_data = map_data.rename(columns={'latitude': 'lat', 'longitude': 'lon'})

# st.map(map_data, zoom=11, use_container_width=True)

# # Show station details below the map
# st.subheader("Station Details")
# st.dataframe(
#     station_plot_df[['station_name', 'address', 'postcode', 'all_fuel_prices_available', 'price_updatedAt_au']],
#     use_container_width=True,
#     hide_index=True
# )






# # Prepare the view state
# view_state = pdk.ViewState(
#     latitude=-38.05,
#     longitude=145.33,
#     zoom=11,
#     pitch=0
# )

# # Create the scatterplot layer
# layer = pdk.Layer(
#     'ScatterplotLayer',
#     data=station_plot_df,
#     get_position='[longitude, latitude]',
#     get_color='[0, 131, 184, 200]',  # Blue color in RGBA
#     get_radius=150,
#     pickable=True,
#     auto_highlight=True
# )

# # Create tooltip
# tooltip = {
#     "html": """
#     <b>{station_name}</b><br/>
#     Address: {address}<br/>
#     Postcode: {postcode}<br/>
#     Last Updated: {price_updatedAt_au}<br/>
#     Fuel Available: {all_fuel_prices_available}
#     """,
#     "style": {
#         "backgroundColor": "#0083B8",
#         "color": "white",
#         "padding": "10px",
#         "borderRadius": "5px"
#     }
# }

# # Render the deck
# st.pydeck_chart(pdk.Deck(
#     layers=[layer],
#     initial_view_state=view_state,
#     tooltip=tooltip,
#     map_style='mapbox://styles/mapbox/satellite-streets-v11'
#     ##map_style='mapbox://styles/mapbox/streets-v11'
#     ##map_style='mapbox://styles/mapbox/light-v9'
# ))





# Sidebar controls
#st.sidebar.subheader("Map Settings")

# # Map style selector
# map_styles = {
#     'Light': 'mapbox://styles/mapbox/light-v9',
#     'Dark': 'mapbox://styles/mapbox/dark-v9',
#     'Streets': 'mapbox://styles/mapbox/streets-v11',
#     'Outdoors': 'mapbox://styles/mapbox/outdoors-v11',
#     'Satellite': 'mapbox://styles/mapbox/satellite-v9',
#     'Satellite + Streets': 'mapbox://styles/mapbox/satellite-streets-v11'
# }

# selected_map = st.sidebar.selectbox(
#     "Select Map Type:",
#     options=list(map_styles.keys()),
#     index=0
# )

# # Marker size control
# marker_size = st.sidebar.slider("Marker Size:", 50, 300, 150)

# # View state
# view_state = pdk.ViewState(
#     latitude=-38.05,
#     longitude=145.33,
#     zoom=11,
#     pitch=0
# )

# # Layer
# layer = pdk.Layer(
#     'ScatterplotLayer',
#     data=station_plot_df,
#     get_position='[longitude, latitude]',
#     get_color='[0, 131, 184, 200]',
#     get_radius=marker_size,
#     pickable=True,
#     auto_highlight=True
# )

# # Tooltip
# tooltip = {
#     "html": """
#     <b>{station_name}</b><br/>
#     Address: {address}<br/>
#     Postcode: {postcode}<br/>
#     Last Updated: {price_updatedAt_au}<br/>
#     Fuel Available: {all_fuel_prices_available}
#     """,
#     "style": {
#         "backgroundColor": "#0083B8",
#         "color": "white",
#         "padding": "10px",
#         "borderRadius": "5px"
#     }
# }

# # Render
# st.pydeck_chart(pdk.Deck(
#     layers=[layer],
#     initial_view_state=view_state,
#     tooltip=tooltip,
#     map_style=map_styles[selected_map]
# ))



######



st.title("Fuel Stations Map")

# Map style selector
map_styles = {
    'Light': 'mapbox://styles/mapbox/light-v9',
    'Streets': 'mapbox://styles/mapbox/streets-v11',
    'Satellite Streets': 'mapbox://styles/mapbox/satellite-streets-v11'
}

selected_map = st.sidebar.selectbox("Map Style:", list(map_styles.keys()), index=0)

# View state
view_state = pdk.ViewState(
    latitude=-38.05,
    longitude=145.33,
    zoom=11,
    pitch=0
)

# Layer
layer = pdk.Layer(
    'ScatterplotLayer',
    data=station_plot_df,
    get_position='[longitude, latitude]',
    get_color='[0, 131, 184, 200]',
    get_radius=150,
    pickable=True,
    auto_highlight=True
)

# Tooltip
tooltip = {
    "html": """
    <b>{station_name}</b><br/>
    Address: {address}<br/>
    Postcode: {postcode}<br/>
    Last Updated: {price_updatedAt_au}<br/>
    Fuel Available: {all_fuel_prices_available}
    """,
    "style": {
        "backgroundColor": "#0083B8",
        "color": "white",
        "padding": "10px",
        "borderRadius": "5px"
    }
}

# Render map and capture click events
deck = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip,
    map_style=map_styles[selected_map]
)

# Display map and get the clicked object
event = st.pydeck_chart(deck, on_select="rerun", selection_mode="single-object")

st.markdown("---")

# Display clicked station details
if event and event.selection and "indices" in event.selection:
    # Get the clicked row index
    clicked_indices = event.selection["indices"]
    
    if clicked_indices:
        clicked_index = clicked_indices[0]
        clicked_station = station_plot_df.iloc[clicked_index]
        
        # Display selected station info
        st.subheader(f"📍 Selected Station: {clicked_station['station_name']}")
        
        # Create a nice display
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"**Address:** {clicked_station['address']}")
            st.markdown(f"**Postcode:** {clicked_station['postcode']}")
        
        with col2:
            st.markdown(f"**Last Updated:** {clicked_station['price_updatedAt_au']}")
            st.markdown(f"**Fuel Available:** {clicked_station['all_fuel_prices_available']}")
        
        # Show full details in dataframe
        st.markdown("#### Full Station Details")
        st.dataframe(
            pd.DataFrame([clicked_station]).T.rename(columns={clicked_index: "Value"}),
            use_container_width=True
        )
else:
    st.info("👆 Click on a marker on the map to see station details")

# Optional: Show all stations below
with st.expander("📋 View All Stations"):
    st.dataframe(
        station_plot_df[[
            'station_name', 
            'address', 
            'postcode', 
            'all_fuel_prices_available', 
            'price_updatedAt_au'
        ]],
        use_container_width=True,
        hide_index=True
    )