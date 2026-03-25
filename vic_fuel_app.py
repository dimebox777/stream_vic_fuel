import requests
import pandas as pd

import uuid

import streamlit as st
##import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

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


##st.markdown(df['suburb'].unique())
## Create a scatter map using the aggregated station data
fig = px.scatter_mapbox(station_plot_df,
                        lat="latitude",
                        lon="longitude",
                        hover_name="station_name", # Display station name on hover
                        hover_data={
                                    "address": True,
                                    "postcode": False,
                                    "price_updatedAt_au": True, # Include in hover_data
                                    "all_fuel_prices_available": True, # New aggregated info for all fuel types and prices
                                    "latitude": False,
                                    "longitude": False
                                    },
                        labels={
                                  "all_fuel_prices_available":"Fuel Available",
                                  "price_updatedAt_au": 'Last Updated' # Rename in hover tooltip
                                    },
                        zoom=11,
                        center=CASEY_CENTER,
                        ##center={"lat": -38.05, "lon": 145.33},
                        size_max=10,
                        height=560,
                        ##map_style="open-street-map",
                        title="Fuel Stations in Victoria by Postcode")

##fig.update_layout(mapbox_style="open-street-map")
fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        coloraxis_colorbar=dict(
            ##title=metric,
            thickness=14,
            len=0.6,
            tickfont=dict(size=10),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        mapbox_style="open-street-map"
    )
st.plotly_chart(fig,width='content', key="map_chart")
##fig.show()  


fig = px.scatter_mapbox(station_plot_df,
                        lat="latitude",
                        lon="longitude",
                        hover_name="station_name",
                        hover_data={
                            "address": True,
                            "postcode": False,
                            "price_updatedAt_au": True,
                            "all_fuel_prices_available": True,
                            "latitude": False,
                            "longitude": False
                        },
                        labels={
                            "all_fuel_prices_available": "Fuel Available",
                            "price_updatedAt_au": 'Last Updated'
                        },
                        zoom=11,
                        center=CASEY_CENTER,
                        height=560,
                        title="Fuel Stations in Victoria by Postcode")

# FIXED: Manually set marker size and style
fig.update_traces(
    marker=dict(
        size=12,  # Set marker size
        opacity=0.8,
        color='#0083B8'  # Optional: set color
    )
)

fig.update_layout(
    margin=dict(t=0, b=0, l=0, r=0),
    coloraxis_colorbar=dict(
        thickness=14,
        len=0.6,
        tickfont=dict(size=10),
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    mapbox_style="open-street-map"
)

st.plotly_chart(fig, use_container_width=True, key="map_chart2")