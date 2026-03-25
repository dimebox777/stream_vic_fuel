import requests
import pandas as pd

import streamlit as st
##import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


SUPABASE_URL="https://oxasehqygbnohwzbdbgp.supabase.co"
SUPABASE_KEY="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Im94YXNlaHF5Z2Jub2h3emJkYmdwIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2Nzc4NjQ3MCwiZXhwIjoyMDgzMzYyNDcwfQ.KVHiRhoZkEvZLUE3sXnVqZPtaA2d2X97A-liv5MnUic"




if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Supabase URL or Key not set in .env")

headers = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json"
}

##response = requests.get('https://jsonplaceholder.typicode.com/users/1/todos')
##response = requests.get('https://jsonplaceholder.org/users')
##https://jsonplaceholder.org/users

##print(data[0]['title'])

##response = requests.get("http://127.0.0.1:8000/api/posts/1")
##print(response.json())

##o = response.json()
##readable_json = json.dumps(o, indent=4)
##print(readable_json)



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

def get_api():
    try:
        response = requests.get("https://supab-fastapi.onrender.com/items")
        print(response.json()["results"][0])
    except requests.exceptions.RequestException as e:
        print("request failed", e)    

##get_api()

def get_api_supa():
    
    try:
        ##headers = headers + {"Prefer":"return=representation,count=exact"}
        headers.update( {"Prefer":"return=representation,count=exact"})
        response = requests.get(f"{SUPABASE_URL}/rest/v1/users",headers=headers
                                ,params={"select": "id,name,email"})
        print(len(response.json()))
        
        print(response.status_code)
        print(response.json())
        print(response.headers.get("Content-Range"))
    except requests.exceptions.RequestException as e:
        print("request failed", e)    

##get_api_supa()
##print(headers)

def get_api_supa_cx_survey1():
    params = {
    'select': '*',
    'limit': '300'
    }
    
    try:
        ##headers = headers + {"Prefer":"return=representation,count=exact"}
        ##headers.update( {"Prefer":"return=representation,count=exact"})
        response = requests.get(f"{SUPABASE_URL}/rest/v1/cx_survey1_view",headers=headers
                                ,params=params)
                                
                                
        print(len(response.json()))
        
        print(response.status_code)
        ##print(response.json())
        ##print(response.json())
        json_data = response.json()
        ##print(response.headers.get("Content-Range"))
    except requests.exceptions.RequestException as e:
        print("request failed", e)

    df = pd.DataFrame(json_data)

    # Convert to datetime (invalid dates or empty strings become NaT)
    df["survey_date"] = pd.to_datetime(df["survey_date"], errors='coerce')

    # Drop all NaT/Nulls
    df = df.dropna(subset=["survey_date"])

    # Convert survey_date to datetime objects for analysis
    ##df['survey_date'] = pd.to_datetime(df['survey_date'])
    df['survey_year'] = df["survey_date"].dt.year
    df["csat_group"]  = df["csat_rating"].apply(
        lambda x: "Satisfied" if x >= 4 else ("Neutral" if x == 3 else "Unsatisfied")
    )


    # Display the first few rows
    print(df.head(1))
    ##print(df['suburb'].value_counts())
    team_counts = df.groupby(['department', 'team']).size()
    ##print(team_counts)
    print(df.groupby(['postcode','suburb']).size())
    return df
##get_api_supa_cx_survey1()

def load_data():
    params = {
    'select': '*',
    ##'limit': '300'
    'survey_date': 'not.is.null,not.eq.' 
    }
    
    try:
        ##headers = headers + {"Prefer":"return=representation,count=exact"}
        ##headers.update( {"Prefer":"return=representation,count=exact"})
        response = requests.get(f"{SUPABASE_URL}/rest/v1/cx_survey1_view",headers=headers
                               ,params=params)
                                
                                
        ##print(len(response.json()))
        
        ##print(response.status_code)
        ##print(response.json())
        ##print(response.json())
        json_data = response.json()
        ##print(response.headers.get("Content-Range"))
    except requests.exceptions.RequestException as e:
        print("request failed", e)

    df = pd.DataFrame(json_data)

    # Convert to datetime (invalid dates or empty strings become NaT)
    ##df["survey_date"] = pd.to_datetime(df["survey_date"], errors='coerce')

    # Drop all NaT/Nulls
    ##df = df.dropna(subset=["survey_date"])
    # Convert survey_date to datetime objects for analysis
    df['survey_date'] = pd.to_datetime(df['survey_date'])
    
    df["year"]        = df["survey_date"].dt.year
    df["year_month"]  = df["survey_date"].dt.to_period("M").astype(str)
    df["csat_group"]  = df["csat_rating"].apply(
        lambda x: "Satisfied" if x >= 4 else ("Neutral" if x == 3 else "Unsatisfied")
    )


    # Display the first few rows
    ##print(df.head(1))
    ##print(df['suburb'].value_counts())
    ##team_counts = df.groupby(['department', 'team']).size()
    ##print(team_counts)
    ##print(df.groupby(['postcode','suburb']).size())
    return df

df = load_data()

##st.write(df.columns)

# ── Sidebar filters ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔎 Filters")
    years = ["All"] + sorted(df["year"].unique().tolist())
    sel_year = st.selectbox("Year", years)

    depts = ["All"] + sorted(df["department"].dropna().unique().tolist())
    sel_dept = st.selectbox("Department", depts)

    nps_groups = st.multiselect("NPS Group", ["Promoter", "Passive", "Detractor"],
                                default=["Promoter", "Passive", "Detractor"])


filtered = df.copy()
if sel_year != "All":
    filtered = filtered[filtered["year"] == int(sel_year)]
if sel_dept != "All":
    filtered = filtered[filtered["department"] == sel_dept]

if nps_groups:

    filtered = filtered[filtered["nps_group"].isin(nps_groups)]

n = len(filtered)

TOTAL_RESP = len(df)

st.set_page_config(layout="wide")

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
    <h1>🏛️ City of Casey — CX Survey Dashboard</h1>
    <p>Victoria, Australia &nbsp;·&nbsp; Customer Experience Insights &nbsp;·&nbsp; {n:,} of {TOTAL_RESP:,} responses shown</p>
</div>
""", unsafe_allow_html=True)

# st.markdown("""
# <style>
#     /* ── Plotly chart wrapper ─────────────────────────────────── */
#     [data-testid="stPlotlyChart"] {
#         border: 1.5px solid #cbd5e1;
#         border-radius: 20px;
#         overflow: hidden !important;
#         padding: 0 !important; 
#         background-color: white;
#         box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
#     }

#     /* ── Metric cards ─────────────────────────────────────────── */
#     [data-testid="stMetric"] {
#         border: 1.5px solid #cbd5e1;
#         border-radius: 12px;
#         padding: 16px;
#         background-color: white;
#         box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
#     }

#     /* ── Dataframe / table ────────────────────────────────────── */
#     /*[data-testid="stDataFrame"] {
#         border: 1.5px solid #cbd5e1;
#         border-radius: 12px;
#         padding: 8px;
#         overflow: hidden;
#         box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
#     }*/

#     /* ── Expander ─────────────────────────────────────────────── */
#     /*
#         [data-testid="stExpander"] {
#         border: 1.5px solid #cbd5e1 !important;
#         border-radius: 12px !important;
#         padding: 4px;
#         background-color: white;
#         box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
#     }*/

#     /* ── Selectbox ────────────────────────────────────────────── */
#     /*[data-testid="stSelectbox"] > div {
#         border: 1.5px solid #cbd5e1;
#         border-radius: 12px;
#         padding: 4px;
#         background-color: white;
#     }*/

#     /* ── Multiselect ──────────────────────────────────────────── */
#     /*[data-testid="stMultiSelect"] > div {
#         border: 1.5px solid #cbd5e1;
#         border-radius: 12px;
#         padding: 4px;
#         background-color: white;
#     }*/

#     /* ── Sidebar ──────────────────────────────────────────────── */
#     /*[data-testid="stSidebar"] {
#         border-right: 1.5px solid #cbd5e1;
#         background-color: #f8fafc;
#     }*/

#     /* ── Columns (card-like) ──────────────────────────────────── */
#     /*[data-testid="stColumn"] {
#         border: 1.5px solid #cbd5e1;
#         border-radius: 12px;
#         padding: 12px;
#         background-color: white;
#         box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
#     }*/
# </style>
# """, unsafe_allow_html=True)


st.markdown("""
<style>
    /* ── Outer wrapper ────────────────────────────────────────── */
    [data-testid="stPlotlyChart"] {
        border: 1.5px solid #cbd5e1 !important;
        border-radius: 12px !important;
        overflow: hidden !important;        /* ✅ clips inner content to border radius */
        background-color: white;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.06);
        padding: 0 !important;             /* ✅ remove padding that breaks border */
    }

    /* ── Inner Plotly div ─────────────────────────────────────── */
    [data-testid="stPlotlyChart"] > div {
        border-radius: 12px !important;
        overflow: hidden !important;
    }

    /* ── Iframe (Streamlit renders Plotly inside an iframe) ───── */
    [data-testid="stPlotlyChart"] iframe {
        border-radius: 12px !important;
        display: block !important;         /* ✅ removes bottom gap caused by inline element */
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)


# st.markdown("""
# <style>

# /* Container for charts using PowerBI style toolbar */
# .powerbi-toolbar [data-testid="stPlotlyChart"] .modebar{
#     left: -40px !important;
#     right: auto !important;
#     top: 50% !important;
#     transform: translateY(-50%);
#     display: flex !important;
#     flex-direction: column !important;
#     background-color: rgba(255,255,255,0.95);
#     border: 1px solid #d1d5db;
#     border-radius: 6px;
#     padding: 4px;
# }

# /* Modebar icons spacing */
# .powerbi-toolbar [data-testid="stPlotlyChart"] .modebar-btn{
#     margin: 3px 0px !important;
# }

# </style>
# """, unsafe_allow_html=True)

# st.markdown("""
# <style>

# /* Move Plotly modebar to left and stack vertically */
# .powerbi-toolbar .js-plotly-plot .modebar {
#     left: -45px !important;
#     right: auto !important;
#     top: 50% !important;
#     transform: translateY(-50%);
#     display: flex !important;
#     flex-direction: column !important;
#     background: rgba(255,255,255,0.95);
#     border: 1px solid #d1d5db;
#     border-radius: 6px;
#     padding: 4px;
# }

# /* Space icons vertically */
# .powerbi-toolbar .js-plotly-plot .modebar-btn {
#     margin: 4px 0px !important;
# }

# </style>
# """, unsafe_allow_html=True)

# st.markdown("""
# <style>

# /* Move modebar to left */
# .js-plotly-plot .modebar {
#     left: 10px !important;
#     right: auto !important;
# }

# /* Stack icons vertically */
# /*.js-plotly-plot .modebar-group {
#     display: flex !important;
#     flex-direction: column !important;
# }*/

# /* spacing */
# .js-plotly-plot .modebar-btn {
#     margin: 4px 0 !important;
# }

# </style>
# """, unsafe_allow_html=True)


# ── KPIs ──────────────────────────────────────────────────────────────────────
promoters  = (filtered["nps_group"] == "Promoter").sum()
detractors = (filtered["nps_group"] == "Detractor").sum()
nps_score  = round(((promoters - detractors) / n * 100) if n else 0, 1)
avg_csat   = round(filtered["csat_rating"].mean(), 2) if n else 0
pct_satisfied = round((filtered["csat_group"] == "Satisfied").sum() / n * 100, 1) if n else 0

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("📋 Respondents",   f"{n:,}")
k2.metric("📊 NPS Score",     f"{nps_score}")
k3.metric("⭐ Avg CSAT",      f"{avg_csat} / 5")
k4.metric("😊 % Satisfied",   f"{pct_satisfied}%")
k5.metric("🎯 Promoters",     f"{promoters:,}")


# ── Colours ───────────────────────────────────────────────────────────────────
NPS_COLORS  = {"Promoter": "#10b981", "Passive": "#f59e0b", "Detractor": "#ef4444"}
CSAT_COLORS = {"Satisfied": "#10b981", "Neutral": "#f59e0b", "Unsatisfied": "#ef4444"}
BLUE_SEQ    = ["#003865", "#00527a", "#007b99", "#00a8c6", "#6dd5ed"]



# ════════════════════════════════════════════════════════════════════════════
# ROW 1 — NPS per Year  |  CSAT per Year
# ════════════════════════════════════════════════════════════════════════════
st.divider()

nps_yr_v1 = (
        filtered.groupby("year").apply(
            lambda g: round(
                (((g["nps_group"] == "Promoter").sum() - (g["nps_group"] == "Detractor").sum()) / len(g)) * 100, 1
            ),include_groups=False
        )
        .reset_index(name="NPS Score")
    )
st.dataframe(nps_yr_v1)

st.divider()

# nps_by_bank_v2 = (
#     filtered.groupby("year")
#     .apply(lambda x:
#         ((x["nps_group"].eq("Promoter").mean()
#          - x["nps_group"].eq("Detractor").mean()) * 100)
#     )
#     .reset_index(name="NPS")
#     .sort_values("NPS")
# )

# nps_by_bank_v2 = (
#     filtered[["year", "nps_group"]]   # ✅ select only needed columns before groupby
#     .groupby("year")
#     .apply(lambda x:
#         ((x["nps_group"].eq("Promoter").mean()
#           - x["nps_group"].eq("Detractor").mean()) * 100)
#     )
#     .reset_index(name="NPS")
#     .sort_values("NPS")
# )

nps_by_bank_v2 = (
    filtered.groupby("year")["nps_group"]   # ✅ select Series directly — no warning
    .agg(lambda x:
        ((x.eq("Promoter").mean()
          - x.eq("Detractor").mean()) * 100)
    )
    .reset_index(name="NPS")
    .sort_values("NPS")
)


st.markdown('nps_by_bank_v2')
st.dataframe(nps_by_bank_v2)
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-title">NPS Score per Year</p>', unsafe_allow_html=True)
    # nps_yr = (
    #     filtered.groupby("year").apply(
    #         lambda g: round(
    #             (((g["nps_group"] == "Promoter").sum() - (g["nps_group"] == "Detractor").sum()) / len(g)) * 100, 1
    #         ),include_groups=False
    #     )
    #     .reset_index(name="NPS Score")
    # )

    # nps_yr = (
    #     filtered.groupby("year").apply(
    #         lambda g: round(
    #             (((g["nps_group"] == "Promoter").sum() - (g["nps_group"] == "Detractor").sum()) / len(g)) * 100, 1
    #         )
    #         ##,include_groups=False
    #     )
    #     .reset_index(name="NPS Score")
    # )


    # nps_yr_v2 = (
    #     filtered[["year", "nps_group"]]    # ✅ select only needed columns before groupby
    #     .groupby("year")
    #     .apply(lambda g: round(
    #         (((g["nps_group"] == "Promoter").sum() - (g["nps_group"] == "Detractor").sum()) / len(g)) * 100, 1
    #     ))
    #     .reset_index(name="NPS Score")
    # )

    nps_yr_v3 = (
        filtered.groupby("year")["nps_group"]    # ✅ SeriesGroupBy — no warning
        .apply(lambda g: round(
            (((g == "Promoter").sum() - (g == "Detractor").sum()) / len(g)) * 100, 1
        ))
        .reset_index(name="NPS Score")
    )


    nps_yr_v4 = (
    filtered.groupby("year")["nps_group"]
    .agg(
        Size=lambda g: g.size,                          # total rows including NaN
        Count=lambda g: g.count(),                      # non-null rows
        Promoters=lambda g: (g == "Promoter").sum(),
        Passives=lambda g: (g == "Passive").sum(),
        Detractors=lambda g: (g == "Detractor").sum(),
        NPS_Score=lambda g: round(
            (((g == "Promoter").sum() - (g == "Detractor").sum()) / len(g)) * 100, 1
        ),
    )
    .reset_index()
    .rename(columns={"NPS_Score": "NPS Score"})
    )




    fig_nps_yr = px.bar(
        nps_yr_v4, x="year", y="NPS Score",
        text="NPS Score",
        color="NPS Score",
        color_continuous_scale=["#ef4444", "#f59e0b", "#10b981"],
        range_color=[-100, 100],
        hover_data={
        "year":True,    
        "NPS Score": True,    
        "Size": False, 
        "Count": True,
        "Promoters": True, 
        "Passives": True, 
        "Detractors": True,
        
        }
    )
    fig_nps_yr.update_traces(textposition="outside", texttemplate="%{text}")
    fig_nps_yr.add_hline(y=0, line_dash="dot", line_color="#94a3b8")
    fig_nps_yr.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        coloraxis_showscale=False,
        xaxis=dict(tickmode="linear", dtick=1, title=""),
        yaxis=dict(title="NPS Score", range=[-100, 100]),
        margin=dict(t=20, b=20),
        #
    )

    fig_nps_yr.update_layout(
    paper_bgcolor="white", 
    plot_bgcolor="white",
    coloraxis_showscale=False,
    xaxis=dict(tickmode="linear", dtick=1, title=""),
    yaxis=dict(title="NPS Score", range=[-100, 100]),
    margin=dict(t=30, b=30, l=30, r=30),
    

    ##border line
    # ADD THIS SECTION:
    shapes=[dict(
        type='rect',
        xref='paper', yref='paper',
        ##x0=-0.05, y0=-0.05, x1=1.05, y1=1.05, # Adjust these to change border padding
        x0=0, y0=0, x1=1, y1=1,
        line=dict(
            color="#cbd5e1", # Light slate gray
            width=2,
        )
    )]
)

    st.plotly_chart(fig_nps_yr, width='content', key="nps_per_year")
   
    

#######========
    



with col2:
    st.markdown('<p class="section-title">Average CSAT Rating per Year</p>', unsafe_allow_html=True)
    csat_yr = filtered.groupby("year")["csat_rating"].mean().round(2).reset_index()
    csat_yr.columns = ["Year", "Avg CSAT"]

    ##csat_yr_v2 = filtered.groupby("year")["csat_rating"].mean().round(2).reset_index()

    csat_yr_v2 = (
        filtered.groupby("year")
        .agg(
            Avg_CSAT=("csat_rating", "mean"),
            Raw_Count=("csat_rating", "count")   # add raw count
        )
        .reset_index()
        ##.sort_values("year")
    )

    csat_yr_v2.columns = ["Year", "Avg CSAT", 'Count']

    csat_yr_v2["Avg CSAT"] = csat_yr_v2["Avg CSAT"].round(2)


    csat_yr_v3 = (
    filtered.groupby("year")
        .agg(
            Avg_CSAT=("csat_rating", "mean"),
            Raw_Count=("csat_rating", "count"),
            Satisfied=("csat_group", lambda x: (x == "Satisfied").sum()),
            Neutral=("csat_group", lambda x: (x == "Neutral").sum()),
            Unsatisfied=("csat_group", lambda x: (x == "Unsatisfied").sum()),
            Avg_NPS=("nps_rating", "mean"),
        )
        .reset_index()
    )

    csat_yr_v3.columns = ["Year", "Avg CSAT", 'Count', 'Satisfied', 'Neutral', 'Unsatisfied','Avg NPS']
    csat_yr_v3["Avg CSAT"] = csat_yr_v3["Avg CSAT"].round(2)
    csat_yr_v3["Avg NPS"] = csat_yr_v3["Avg NPS"].round(2)
    


    # ---- Calculate percentages
    csat_yr_v3["Satisfied_pct"] = (csat_yr_v3["Satisfied"] / csat_yr_v3["Count"] * 100)
    csat_yr_v3["Neutral_pct"] = (csat_yr_v3["Neutral"] / csat_yr_v3["Count"] * 100)
    csat_yr_v3["Unsatisfied_pct"] = (csat_yr_v3["Unsatisfied"] / csat_yr_v3["Count"] * 100)

    y_min = max(1, csat_yr_v3["Avg CSAT"].min() - 0.3)  # floor at 1
    y_max = min(5, csat_yr_v3["Avg CSAT"].max() + 0.3)  # ceiling at 5

    ##st.dataframe(csat_yr_v3)
    ##st.dataframe(csat_yr_v2)

    ##csat_nps_yr = pd.concat([csat_yr_v3, nps_by_bank_v2], ignore_index=True)
    ##csat_nps_yr = csat_yr_v3.merge(nps_by_bank_v2,'inner', on='Year')
    ##st.dataframe(csat_nps_yr)


    csat_nps_yr = (
    filtered.groupby("year")
        .agg(
            Avg_CSAT=("csat_rating", "mean"),
            Raw_Count=("csat_rating", "count"),
            Satisfied=("csat_group", lambda x: (x == "Satisfied").sum()),
            Neutral=("csat_group", lambda x: (x == "Neutral").sum()),
            Unsatisfied=("csat_group", lambda x: (x == "Unsatisfied").sum()),
            Avg_NPS_Rating=("nps_rating", "mean"), # This is the 0-10 average
            NPS_Score=("nps_group", lambda x: (x.eq("Promoter").mean() - x.eq("Detractor").mean()) * 100) # This is the KPI
        )
        .reset_index()
    )

    # Rename columns to your preferred display names
    csat_nps_yr.columns = [
        "Year", "Avg CSAT", "Count", "Satisfied", 
        "Neutral", "Unsatisfied", "Avg NPS", "NPS Score"
    ]

    csat_nps_yr["Avg CSAT"] = csat_nps_yr["Avg CSAT"].round(2)
    csat_nps_yr["Avg NPS"] = csat_nps_yr["Avg NPS"].round(2)

    # ---- Calculate percentages
    csat_nps_yr["Satisfied_pct"] = (csat_nps_yr["Satisfied"] / csat_nps_yr["Count"] * 100)
    csat_nps_yr["Neutral_pct"] = (csat_nps_yr["Neutral"] / csat_nps_yr["Count"] * 100)
    csat_nps_yr["Unsatisfied_pct"] = (csat_nps_yr["Unsatisfied"] / csat_nps_yr["Count"] * 100)
    
    
    ##csat_nps_yr["Year"] = csat_nps_yr["Year"].astype(str)
    csat_nps_yr["Avg NPS"] = csat_nps_yr["Avg NPS"].astype(float)
    csat_nps_yr["Avg CSAT"] = csat_nps_yr["Avg CSAT"].astype(float)
    ##csat_nps_yr["Year"] = pd.Categorical(csat_nps_yr["Year"].astype(str))
    ##csat_nps_yr["Year"] = "'" + csat_nps_yr["Year"].astype(str)
    ##csat_nps_yr["Year"] = csat_nps_yr["Year"].astype(str) + " "
    ##csat_nps_yr["Year"] = csat_nps_yr["Year"].astype("int64").astype(str)
    ##st.dataframe(csat_nps_yr)
    
    # Show me what this looks like
    st.write(csat_nps_yr.dtypes)
    st.write(csat_nps_yr["Year"].values)

    fig_csat_yr = px.line(
        ##csat_yr_v3, x="Year", y="Avg CSAT",
        csat_nps_yr, x="Year", y="Avg CSAT",
        markers=True, text="Avg CSAT",
        color_discrete_sequence=["#003865"],
        custom_data=["Count", 'Satisfied', 'Neutral', 'Unsatisfied', 'Satisfied_pct', 'Neutral_pct', 'Unsatisfied_pct','Avg NPS','NPS Score'],
        hover_data={
        "Year":True,    
        "Avg CSAT": True,
        "Count": True,
        }

    )
    fig_csat_yr.update_traces(
        textposition="top center",
        line=dict(width=3),
        marker=dict(size=10, color="#007b99"),
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Average: <b>%{y}</b><br>"
            "Response Count: <b>%{customdata[0]}</b><br>"
            "Satisfied Count: <b>%{customdata[1]}</b><br>"
            "Neutral Count: <b>%{customdata[2]}</b><br>"
            "Unsatisfied Count: <b>%{customdata[3]}</b><br>"
            "Satisfied: %{customdata[4]:.2f}%<br>"
            "Neutral: %{customdata[5]:.2f}%<br>"
            "Unsatisfied: %{customdata[6]:.2f}%<br>"
            "NPS Average: %{customdata[7]}<br>"
            "NPS Score: %{customdata[8]:.1f}"
            

            "<extra></extra>"
        ),
    )
    fig_csat_yr.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(tickmode="linear", dtick=1, title=""),
        yaxis=dict(title="Avg CSAT (1–5)", range=[y_min, y_max],
        tickmode="auto",
        ##tickvals=[1, 2, 3, 4, 5],
        ##ticktext=["1", "2", "3", "4", "5"],
        
        ),
        margin=dict(t=20, b=20),
    )

    fig_csat_yr.add_hrect(y0=4, y1=5, fillcolor="#10b981", opacity=0.07, line_width=0)
    st.plotly_chart(fig_csat_yr, width='content', key="csat_per_year")



    ##csat_nps_yr["Year"] = csat_nps_yr["Year"].astype(str)
    fig_csat_nps_yr = px.line(
    csat_nps_yr, 
    x="Year", 
    y=["Avg CSAT", "Avg NPS"],  # <--- Pass both here
    markers=True, 
    color_discrete_sequence=["#003865", "#FF6B35"], 
    # color_discrete_map={
    #     "Avg CSAT": "#003865", 
    #     "Avg NPS": "#ef4444"    # Assign a different color to NPS
    # },
    custom_data=["Count", 'Satisfied', 'Neutral', 'Unsatisfied', 'Avg NPS', 'NPS Score']
    )

    fig_csat_nps_yr.update_traces(textposition="top center")
    ##st.write(csat_nps_yr.dtypes)
    ##st.write(csat_nps_yr.head())
    st.plotly_chart(fig_csat_nps_yr, width='content', key="csat_nps_per_year")

    
    ##csat_nps_yr["Year"] = csat_nps_yr["Year"].astype("int64").astype(str)
    # fig_csat_yr = px.line(
    # csat_nps_yr,
    # x="Year",
    # y=["Avg CSAT", "Avg NPS"],
    # markers=True,
    # color_discrete_sequence=["#003865", "#FF6B35"],
    # custom_data=["Count", "Satisfied", "Neutral", "Unsatisfied",
    #              "Satisfied_pct", "Neutral_pct", "Unsatisfied_pct",
    #              "NPS Score"],
    # labels={"value": "", "variable": "Metric"},
    # )

    # # Fix 2: Avg NPS is on a different scale — add a secondary y-axis
    # fig_csat_yr.update_traces(
    #     selector={"name": "Avg NPS"},
    #     yaxis="y2"
    # )

    # fig_csat_yr.update_layout(
    #     yaxis=dict(title="Avg CSAT", range=[1, 5]),
    #     yaxis2=dict(
    #         title="Avg NPS",
    #         overlaying="y",
    #         side="right",
    #         range=[0, 10],
    #         showgrid=False,
    #     ),
    # )

    # fig_csat_yr.update_traces(textposition="top center")
    
    # st.plotly_chart(fig_csat_yr, width='content', key="scsat_nps_per_year")




    ##csat_nps_yr["Year"] = csat_nps_yr["Year"].astype("int64").astype(str)

    fig_csat_yr = go.Figure()

    fig_csat_yr.add_trace(go.Scatter(
        x=csat_nps_yr["Year"],
        y=csat_nps_yr["Avg CSAT"],
        mode="lines+markers+text",
        name="Avg CSAT",
        text=csat_nps_yr["Avg CSAT"].round(2),
        textposition="top center",
        line=dict(color="#003865"),
        marker=dict(size=6),
        customdata=csat_nps_yr[["Count", "Satisfied", "Neutral", "Unsatisfied",
                                "Satisfied_pct", "Neutral_pct", "Unsatisfied_pct",
                                "NPS Score"]].values,
        yaxis="y1",
    ))

    fig_csat_yr.add_trace(go.Scatter(
        x=csat_nps_yr["Year"],
        y=csat_nps_yr["Avg NPS"],
        mode="lines+markers",
        name="Avg NPS",
        line=dict(color="#FF6B35"),
        marker=dict(size=6),
        yaxis="y2",
    ))

    fig_csat_yr.update_layout(
        xaxis=dict(type="category"),
        yaxis=dict(title="Avg CSAT", range=[1, 5]),
        yaxis2=dict(
            title="Avg NPS",
            overlaying="y",
            side="right",
            range=[0, 10],
            showgrid=False,
        ),
        legend=dict(title="Metric"),
    )

    st.plotly_chart(fig_csat_yr, use_container_width=True, key="scsat_nps_per_year")



st.divider()

with st.expander("Click to view chart"):
    st.markdown('<p class="section-title">NPS Score per Year</p>', unsafe_allow_html=True)

    nps_yr = (
        filtered.groupby("year").apply(
            lambda g: round(
                (((g["nps_group"] == "Promoter").sum() - (g["nps_group"] == "Detractor").sum()) / len(g)) * 100, 1
            ), include_groups=False
        )
        .reset_index(name="NPS Score")
    )
    st.write("nps_yr")
    st.dataframe(nps_yr)
    total_row = pd.DataFrame([{
    "year":       "Total",
    "NPS Score":  round(
        ((filtered["nps_group"] == "Promoter").sum() - (filtered["nps_group"] == "Detractor").sum()) / n * 100, 1
    )
    }])

    ##nps_yr["year"] = nps_yr["year"].astype(str)
    nps_yr_str = nps_yr.copy()
    nps_yr_str["year"] = nps_yr_str["year"].astype(str)

    nps_yr_con = pd.concat([nps_yr_str, total_row], ignore_index=True)
    st.dataframe(total_row)
    st.dataframe(nps_yr_con)
    # Raw counts per year
    nps_counts = (
        filtered.groupby("year").agg(
            Total=("nps_rating", "count"),
            Promoters=("nps_group", lambda x: (x == "Promoter").sum()),
            Passives=("nps_group", lambda x: (x == "Passive").sum()),
            Detractors=("nps_group", lambda x: (x == "Detractor").sum()),
        ).reset_index()
    )
    st.dataframe(nps_counts)
    nps_yr = nps_yr.merge(nps_counts, on="year")
    ##nps_yr_str = nps_yr_str.merge(nps_counts, on="year")
    st.dataframe(nps_yr)
    ##st.dataframe(nps_yr_str)
   
    nps_counts_str = (
        filtered.groupby("year").agg(
            Total=("nps_rating", "count"),
            Promoters=("nps_group", lambda x: (x == "Promoter").sum()),
            Passives=("nps_group", lambda x: (x == "Passive").sum()),
            Detractors=("nps_group", lambda x: (x == "Detractor").sum()),
        ).reset_index()
    )

    nps_counts_str["year"] = nps_counts_str["year"].astype(str)
    nps_yr_str = nps_yr_str.merge(nps_counts_str, on="year")
   
    st.dataframe(nps_yr_str)


    fig_nps_yr = px.bar(
        nps_yr, x="year", y="NPS Score",
        text="NPS Score",
        color="NPS Score",
        color_continuous_scale=["#ef4444", "#f59e0b", "#10b981"],
        range_color=[-100, 100],
        title="Yearly NPS",
        ##custom_data=["Total", "Promoters", "Passives", "Detractors"],
        custom_data=["Total"],
        hover_data={
        "year":False,    
        "NPS Score": False,    
        "Total": True,  # Set to True to keep it
        "Promoters": True, 
        "Passives": True, 
        "Detractors": True,
        
        }
        
    )
    fig_nps_yr.update_traces(
        textposition="outside",
        texttemplate="%{text}",
        # hovertemplate=(
        #     "<b>%{x}</b><br>"
        #     "NPS Score: <b>%{y}</b><br>"
        #     "─────────────────<br>"
        #     "Total Respondents: <b>%{customdata[0]}</b><br>"
        #     "Promoters: <b>%{customdata[1]}</b><br>"
        #     "Passives: <b>%{customdata[2]}</b><br>"
        #     "Detractors: <b>%{customdata[3]}</b>"
        #     "<extra></extra>"
        # ),

        hovertemplate=(
            "<b>%{x}</b><br>"
            "NPS Score: <b>%{y}</b><br>"
            "counts: <b>%{customdata[0]}</b><br>"
            "<extra></extra>"
        ),
    )

    fig_nps_yr.add_hline(y=0, line_dash="dot", line_color="#94a3b8")
    fig_nps_yr.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        coloraxis_showscale=False,
        xaxis=dict(tickmode="linear", dtick=1, title=""),
        yaxis=dict(title="NPS Score", range=[-100, 100]),
        margin=dict(t=30, b=30, l=30, r=30),
        shapes=[dict(
            type="rect",
            xref="paper", yref="paper",
            x0=0, y0=0, x1=1, y1=1,
            line=dict(color="#cbd5e1", width=2),
        )]
    )
    st.plotly_chart(fig_nps_yr, width='stretch', key="nps_per_year2")




    





st.divider()
col3, col4 = st.columns(2)
with col3:
    st.markdown('<p class="section-title">NPS Score per Year</p>', unsafe_allow_html=True)

    nps_yr = (
        filtered.groupby("year").apply(
            lambda g: round(
                (((g["nps_group"] == "Promoter").sum() - (g["nps_group"] == "Detractor").sum()) / len(g)) * 100, 1
            ), include_groups=False
        )
        .reset_index(name="NPS Score")
    )

    ##st.dataframe(nps_yr)
    # Raw counts per year
    nps_counts = (
        filtered.groupby("year").agg(
            Total=("nps_rating", "count"),
            Promoters=("nps_group", lambda x: (x == "Promoter").sum()),
            Passives=("nps_group", lambda x: (x == "Passive").sum()),
            Detractors=("nps_group", lambda x: (x == "Detractor").sum()),
        ).reset_index()
    )

    ##st.dataframe(nps_counts)
    nps_yr = nps_yr.merge(nps_counts, on="year")

    ##st.dataframe(nps_yr)

    nps_yr_3 = (
    filtered.groupby("year").apply(
        lambda g: pd.Series({
            "NPS Score": round(
                ((g["nps_group"] == "Promoter").sum() - (g["nps_group"] == "Detractor").sum()) / len(g) * 100, 1
            ),
            "Total":      len(g),
            "Promoters":  (g["nps_group"] == "Promoter").sum(),
            "Passives":   (g["nps_group"] == "Passive").sum(),
            "Detractors": (g["nps_group"] == "Detractor").sum(),
            "% Promoters":  round((g["nps_group"] == "Promoter").sum() / len(g) * 100, 1),
            "% Passives":   round((g["nps_group"] == "Passive").sum()  / len(g) * 100, 1),
            "% Detractors": round((g["nps_group"] == "Detractor").sum()/ len(g) * 100, 1),
        }), include_groups=False
    )
    .reset_index()
    )

    ##st.dataframe(nps_yr_3)



    fig_nps_yr = px.bar(
        nps_yr, x="year", y="NPS Score",
        text="NPS Score",
        color="NPS Score",
        color_continuous_scale=["#ef4444", "#f59e0b", "#10b981"],
        range_color=[-100, 100],
        custom_data=["Total", "Promoters", "Passives", "Detractors"],
    )
    fig_nps_yr.update_traces(
        textposition="outside",
        texttemplate="%{text}",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "NPS Score: <b>%{y}</b><br>"
            "count: <b>%{customdata[0]}</b>"
            "<extra></extra>"
        ),
    )

    fig_nps_yr.add_hline(y=1, line_dash="dot", line_color="#94a3b8")
    fig_nps_yr.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        coloraxis_showscale=False,
        xaxis=dict(tickmode="linear", dtick=1, title=""),
        yaxis=dict(title="NPS Score", range=[-100, 100]),
        margin=dict(t=30, b=30, l=30, r=30),
        shapes=[dict(
            type="rect",
            xref="paper", yref="paper",
            x0=0, y0=0, x1=1, y1=1,
            line=dict(color="#cbd5e1", width=1.5),
        )]
    )
    st.plotly_chart(fig_nps_yr, width='stretch', key="nps_per_year3")

with col4:
    st.markdown('<p class="section-title">6-Month Rolling Average CSAT</p>', unsafe_allow_html=True)

    monthly_csat = (
        filtered.groupby("year_month")
        .agg(
            Avg_CSAT=("csat_rating", "mean"),
            Raw_Count=("csat_rating", "count"),   # add raw count
            Raw_SUM=("csat_rating", "sum")   # add raw count
        )
        .reset_index()
        .sort_values("year_month")
    )

    monthly_csat["Month_Label"] = pd.to_datetime(
        monthly_csat["year_month"]
        ).dt.strftime("%b %Y")

    monthly_csat.columns = ["Month", "Avg CSAT", "Raw Count", "Raw Sum","Month Label"]
    monthly_csat["Avg CSAT"] = monthly_csat["Avg CSAT"].round(2)
    monthly_csat["6M Rolling Avg"] = monthly_csat["Avg CSAT"].rolling(window=6, min_periods=1).mean().round(2)
    monthly_csat["6M Rolling Count"] = monthly_csat["Raw Count"].rolling(window=6, min_periods=1).sum().astype(int)
    monthly_csat["6M Rolling SUM"] = monthly_csat["Raw Sum"].rolling(window=6, min_periods=1).sum().astype(int)

    

    ##6M Rolling revised V2
    monthly_csat["6M Rolling AvgV2"] = (
        (
            monthly_csat["Avg CSAT"] * monthly_csat["Raw Count"]   # sum of ratings per week
        )
        .rolling(window=6, min_periods=1).sum()
        /
        monthly_csat["Raw Count"]
        .rolling(window=6, min_periods=1).sum()
    ).round(2)
    
    monthly_csat["6M Rolling AvgV3"] = (monthly_csat["6M Rolling SUM"] / monthly_csat["6M Rolling Count"]).round(2)
    


    # 12M Rolling ✅
    ##monthly_csat["12M Rolling Avg"]   = monthly_csat["Avg CSAT"].rolling(window=12, min_periods=1).mean().round(2)
    ##monthly_csat["12M Rolling Count"] = monthly_csat["Raw Count"].rolling(window=12, min_periods=1).sum().astype(int)

    # 3M Rolling ✅
    monthly_csat["3M Rolling Avg"]   = monthly_csat["Avg CSAT"].rolling(window=3, min_periods=1).mean().round(2)
    monthly_csat["3M Rolling Count"] = monthly_csat["Raw Count"].rolling(window=3, min_periods=1).sum().astype(int)
    monthly_csat["3M Rolling Sum"] = monthly_csat["Raw Sum"].rolling(window=3, min_periods=1).sum().astype(int)

    monthly_csat["3M Rolling AvgV2"] = (
        (
            monthly_csat["Avg CSAT"] * monthly_csat["Raw Count"]   # sum of ratings per week
        )
        .rolling(window=3, min_periods=1).sum()
        /
        monthly_csat["Raw Count"]
        .rolling(window=3, min_periods=1).sum()
    ).round(2)

    ##st.dataframe(monthly_csat)
    fig_rolling = go.Figure()

    # Monthly Avg bars — raw count in tooltip
    fig_rolling.add_trace(go.Bar(
        x=monthly_csat["Month Label"],
        y=monthly_csat["Avg CSAT"],
        name="Monthly Avg",
        marker_color="#c7dff7",
        opacity=0.7,
        customdata=monthly_csat[["Raw Count"]],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Monthly Avg CSAT: <b>%{y}</b><br>"
            "Raw Count: <b>%{customdata[0]}</b> respondents"
            "<extra></extra>"
        ),
    ))

    # 6M Rolling Avg line — rolling count in tooltip
    fig_rolling.add_trace(go.Scatter(
        x=monthly_csat["Month Label"],
        y=monthly_csat["6M Rolling Avg"],
        name="6M Rolling Avg",
        mode="lines+markers",
        line=dict(color="#003865", width=3),
        marker=dict(size=7, color="#007b99"),
        customdata=monthly_csat[["6M Rolling Count"]],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "6M Rolling Avg CSAT: <b>%{y}</b><br>"
            "Rolling Raw Count: <b>%{customdata[0]}</b> respondents"
            "<extra></extra>"
        ),
    ))


    ##6 Months V2
    fig_rolling.add_trace(go.Scatter(
        x=monthly_csat["Month Label"],
        y=monthly_csat["6M Rolling AvgV2"],
        name="6M Rolling AvgV2",
        mode="lines+markers",
        ##line=dict(color="#ef4444", width=3, dash="dash"),  # dashed to distinguish from 6M
        line=dict(color="#ef4444", width=0.5, dash="solid"),  # dashed to distinguish from 6M
        marker=dict(size=7, color="#ef4444"),
        customdata=monthly_csat[["6M Rolling Count"]],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "V2 6M Rolling Avg CSAT: <b>%{y}</b><br>"
            "V2 Rolling Raw Count: <b>%{customdata[0]}</b> respondents"
            "<extra></extra>"
        ),
    ))




#     ##12 Months
#     fig_rolling.add_trace(go.Scatter(
#     x=monthly_csat["Month"],
#     y=monthly_csat["12M Rolling Avg"],
#     name="12M Rolling Avg",
#     mode="lines+markers",
#     line=dict(color="#ef4444", width=3, dash="dash"),  # dashed to distinguish from 6M
#     marker=dict(size=7, color="#ef4444"),
#     customdata=monthly_csat[["12M Rolling Count"]],
#     hovertemplate=(
#         "<b>%{x}</b><br>"
#         "12M Rolling Avg CSAT: <b>%{y}</b><br>"
#         "Rolling Raw Count: <b>%{customdata[0]}</b> respondents"
#         "<extra></extra>"
#     ),
# ))

    # ##3 Months
    # fig_rolling.add_trace(go.Scatter(
    #     x=monthly_csat["Month"],
    #     y=monthly_csat["3M Rolling Avg"],
    #     name="3M Rolling Avg",
    #     mode="lines+markers",
    #     line=dict(color="#ef4444", width=3, dash="dash"),  # dashed to distinguish from 6M
    #     marker=dict(size=7, color="#ef4444"),
    #     customdata=monthly_csat[["3M Rolling Count"]],
    #     hovertemplate=(
    #         "<b>%{x}</b><br>"
    #         "3M Rolling Avg CSAT: <b>%{y}</b><br>"
    #         "Rolling Raw Count: <b>%{customdata[0]}</b> respondents"
    #         "<extra></extra>"
    #     ),
    # ))


    fig_rolling.add_hline(y=3, line_dash="dot", line_color="#ef4444", opacity=0.5,
                          annotation_text="Neutral threshold", annotation_position="bottom right")
    
    y_min = max(1, monthly_csat["Avg CSAT"].min() - 0.3)  # floor at 1
    y_max = min(5, monthly_csat["Avg CSAT"].max() + 0.3)  # ceiling at 5


    fig_rolling.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(title="", tickangle=-45, tickfont=dict(size=9)),
        yaxis=dict(title="CSAT (1–5)", range=[y_min, y_max],
        tickmode="auto",
        ##tickvals=[1, 2, 3, 4, 5],
        ##ticktext=["1", "2", "3", "4", "5"],
        
        ),
        ##legend on top
        ##legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        ##margin=dict(t=30, b=40),

        ##set legend to bottom center
        legend=dict(orientation="h", yanchor="top", y=-0.3, xanchor="center", x=0.5),
        margin=dict(t=30, b=40),

        modebar=dict(
        orientation="h"
        ),
        ##showlegend=False
        
    )

    # fig_rolling.update_layout(
    #     paper_bgcolor="white", plot_bgcolor="white",
    #     xaxis=dict(title="", tickangle=-45, tickfont=dict(size=9)),
    #     yaxis=dict(title="CSAT (1–5)", range=[1, 5.5],
    #     tickmode="array",
    #     tickvals=[1, 2, 3, 4, 5],
    #     ticktext=["1", "2", "3", "4", "5"],
        
    #     ),
    #     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    #     margin=dict(t=30, b=40),
    # )

    # config = {
    # "displayModeBar": "hover",
    # "displaylogo": False,
    # "modeBarPosition": "left",   # ✅ "left" | "right" | "top" | "bottom"
    # "scrollZoom": True,
    # "modeBarButtonsToRemove": [
    #     "select2d",
    #     "lasso2d",
    #     "hoverClosestCartesian",
    #     "hoverCompareCartesian",
    #     "toggleSpikelines",
    # ],
    # }

    # st.markdown("""
    # <style>
    #     /* Move modebar to the left */
    #     .modebar-container {
    #         left: 0 !important;
    #         right: auto !important;
    #     }
    #     .powerbi-toolbar .modebar {
    # left: 0px !important;
    # right: auto !important;
    # }
    # </style>
    # """, unsafe_allow_html=True)

    # config = {
    # "displaylogo": False,
    # "modeBarButtonsToRemove": [
    #     "lasso2d",
    #     "select2d",
    #     "autoScale2d",
    #     "zoomIn2d",
    #     "zoomOut2d"
    # ]
    # }

    ##st.markdown('<div class="powerbi-toolbar">', unsafe_allow_html=True)
    st.plotly_chart(fig_rolling, width='stretch', key="rolling_csat")
    ##st.markdown('</div>', unsafe_allow_html=True)

    

st.divider()


st.dataframe(monthly_csat)

st.divider()



with st.expander("Click to view chart"):
    st.markdown('<p class="section-title">NPS Score per Year</p>', unsafe_allow_html=True)
    filtered["year"] = pd.to_numeric(filtered["year"], errors='coerce').fillna(0).astype(int).astype(str)
    nps_yr = (
    filtered.groupby("year").apply(
        lambda g: pd.Series({
            "NPS Score":  round(
                ((g["nps_group"] == "Promoter").sum() - (g["nps_group"] == "Detractor").sum()) / len(g) * 100, 1
            ),
            "Total":      len(g),
            "Promoters":  (g["nps_group"] == "Promoter").sum(),
            "Passives":   (g["nps_group"] == "Passive").sum(),
            "Detractors": (g["nps_group"] == "Detractor").sum(),
        }), include_groups=False
    )
    .reset_index()
)

    # Overall / Total row
    total_row = pd.DataFrame([{
        "year":       "Total",
        "NPS Score":  round(
            ((filtered["nps_group"] == "Promoter").sum() - (filtered["nps_group"] == "Detractor").sum()) / n * 100, 1
        ),
        "Total":      n,
        "Promoters":  (filtered["nps_group"] == "Promoter").sum(),
        "Passives":   (filtered["nps_group"] == "Passive").sum(),
        "Detractors": (filtered["nps_group"] == "Detractor").sum(),
    }])

    ##nps_yr = pd.concat([nps_yr, total_row], ignore_index=True)

    
    nps_yr_con = pd.concat([nps_yr, total_row], ignore_index=True)
    ##st.dataframe(total_row)
    ##st.dataframe(nps_yr_con)

    nps_yr_con = pd.concat([nps_yr, total_row], ignore_index=True)

    # Clean the year column: convert 2024.0 -> "2024" but keep "Total" as "Total"
    nps_yr_con["year"] = nps_yr_con["year"].apply(lambda x: str(int(x)) if isinstance(x, float) else str(x))

    nps_yr_con = nps_yr_con[nps_yr_con["year"] != "0"]
    st.dataframe(nps_yr_con)

    # This will now print ['2024', '2025', '2026', 'Total'] (or similar)
    st.write(nps_yr_con["year"].tolist())

    # Now this will match your yr_list properly
    yr_list = ["Total", "2024", "2025", "2026"]

    # nps_yr_con = nps_yr_con.copy()
    # nps_yr_con["year"] = nps_yr_con["year"].astype(str)

    # nps_yr_con = nps_yr_con.reset_index(drop=True)

    # st.write(nps_yr_con["year"].tolist())
    
    # yr_list = ["Total", "2024","2025","2026"]  

    ##st.write(total_row['year']== '')

    YR_NPS_COLOR = {"Total":"#10b981","2024":"#ef4444","2025":"#ef4444","2026":"#ef4444"}
    ##NPS_SCORE_COLOR = {"Total":"#10b981"}
    fig_nps_yr = px.bar(
        nps_yr_con, x="year", y="NPS Score",
        text="NPS Score",
        ##color="NPS Score",
        color="year",
        ##color_discrete_sequence=
        color_discrete_map=YR_NPS_COLOR,
        ##color_continuous_scale=["#ef4444", "#f59e0b", "#10b981"],
        ##range_color=[-100, 100],
        custom_data=["Total", "Promoters", "Passives", "Detractors"],
        category_orders={"year": yr_list},  # preserve order
    )
    fig_nps_yr.update_traces(
        textposition="outside",
        texttemplate="%{text}",
        hovertemplate=(
            "<b>%{x}</b><br>"
            "─────────────────<br>"
            "Total Respondents: <b>%{customdata[0]}</b><br>"
            "Promoters: <b>%{customdata[1]}</b><br>"
            "Passives: <b>%{customdata[2]}</b><br>"
            "Detractors: <b>%{customdata[3]}</b>"
            "<extra></extra>"
        ),
    )
    fig_nps_yr.update_layout(
        showlegend=False,  # This hides the 'year' annotation and color boxes
        paper_bgcolor="white", plot_bgcolor="white",
        #coloraxis_showscale=False,
        xaxis=dict(title="", type="category"),  # force categorical axis
        yaxis=dict(title="NPS Score", range=[-100, 100]),
        margin=dict(t=30, b=30, l=30, r=30),
    )

    st.plotly_chart(fig_nps_yr, width='stretch', key="nps_per_year4")




st.divider()
col5, col6 = st.columns(2)
with col5:

    fig = go.Figure(go.Indicator(
        mode = "number+delta",
        value = nps_yr_con.loc[nps_yr_con['year'] == 'Total', 'NPS Score'].values[0],
        delta = {'reference': -40, 'relative': True, 'position': "top"},
        number = {'suffix': "%", 'font': {'size': 50, 'color': '#1e293b'}},
        title = {"text": "NPS Performance", 'font': {'size': 16}},
        domain = {'x': [0, 1], 'y': [0, 1]}
    ))

    fig.update_layout(
        paper_bgcolor="white",
        height=200,
        margin=dict(t=20, b=20, l=20, r=20),
        # Add your thin border shape here too!
        shapes=[dict(type='rect', xref='paper', yref='paper', x0=0, y0=0, x1=1, y1=1,
                    line=dict(color="#cbd5e1", width=1))]
    )

    st.plotly_chart(fig, width='content')


with col6:
    
    st.markdown('<p class="section-title">6-Month Rolling Average CSAT</p>', unsafe_allow_html=True)

    monthly_csat = (
        filtered.groupby("year_month")
        .agg(
            Avg_CSAT=("csat_rating", "mean"),
            Raw_Count=("csat_rating", "count")   # add raw count
        )
        .reset_index()
        .sort_values("year_month")
    )
    monthly_csat.columns = ["Month", "Avg CSAT", "Raw Count"]
    monthly_csat["Avg CSAT"] = monthly_csat["Avg CSAT"].round(2)
    monthly_csat["6M Rolling Avg"] = monthly_csat["Avg CSAT"].rolling(window=6, min_periods=1).mean().round(2)
    monthly_csat["6M Rolling Count"] = monthly_csat["Raw Count"].rolling(window=6, min_periods=1).sum().astype(int)

    fig_rolling = go.Figure()

    # Monthly Avg bars — raw count in tooltip
    fig_rolling.add_trace(go.Bar(
        x=monthly_csat["Month"],
        y=monthly_csat["Avg CSAT"],
        name="Monthly Avg",
        marker_color="#c7dff7",
        opacity=0.7,
        customdata=monthly_csat[["Raw Count"]],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "Monthly Avg CSAT: <b>%{y}</b><br>"
            "Raw Count: <b>%{customdata[0]}</b> respondents"
            "<extra></extra>"
        ),
    ))

    # 6M Rolling Avg line — rolling count in tooltip
    fig_rolling.add_trace(go.Scatter(
        x=monthly_csat["Month"],
        y=monthly_csat["6M Rolling Avg"],
        name="6M Rolling Avg",
        mode="lines+markers",
        line=dict(color="#003865", width=3),
        marker=dict(size=7, color="#007b99"),
        customdata=monthly_csat[["6M Rolling Count"]],
        hovertemplate=(
            "<b>%{x}</b><br>"
            "6M Rolling Avg CSAT: <b>%{y}</b><br>"
            "Rolling Raw Count: <b>%{customdata[0]}</b> respondents"
            "<extra></extra>"
        ),
    ))

    ##fig_rolling.add_hline(y=3, line_dash="dot", line_color="#ef4444", opacity=0.5,
    ##                      annotation_text="Neutral threshold", annotation_position="bottom right")
    
    y_min = max(1, monthly_csat["Avg CSAT"].min() - 0.3)  # floor at 1
    y_max = min(5, monthly_csat["Avg CSAT"].max() + 0.3)  # ceiling at 5


    fig_rolling.update_layout(
        paper_bgcolor="white", plot_bgcolor="white",
        xaxis=dict(title="", tickangle=-45, tickfont=dict(size=9)),
        yaxis=dict(title="CSAT (1–5)", range=[y_min, y_max],
        ##tickmode="auto",
        ##yaxis=dict(title="CSAT (1–5)", range=[1, 5.5],
        tickmode="array",
        tickvals=[1, 2, 3, 4, 5],
        ticktext=["1", "2", "3", "4", "5"],
        
        ),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        margin=dict(t=30, b=40),
    )

    # fig_rolling.update_layout(
    #     paper_bgcolor="white", plot_bgcolor="white",
    #     xaxis=dict(title="", tickangle=-45, tickfont=dict(size=9)),
    #     yaxis=dict(title="CSAT (1–5)", range=[1, 5.5],
    #     tickmode="array",
    #     tickvals=[1, 2, 3, 4, 5],
    #     ticktext=["1", "2", "3", "4", "5"],
        
    #     ),
    #     legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    #     margin=dict(t=30, b=40),
    # )
    st.plotly_chart(fig_rolling, width='stretch', key="rolling_csat2")

st.markdown('<p class="section-title">Attribute Ratings</p>', unsafe_allow_html=True)

attr_cols = ['attr_rating_1', 'attr_rating_2', 'attr_rating_3','attr_rating_4', 'attr_rating_5']

# Diagnose — check dtype and sample values before converting
##st.write(filtered[attr_cols].dtypes)
##st.write(filtered[attr_cols].head())
filtered[attr_cols] = filtered[attr_cols].astype(int)
##st.write(filtered[attr_cols].dtypes)

##totals_attr = filtered[attr_cols].mean().round(1).reset_index()
##totals_attr.columns = ['Attributes', 'Total']
totals_attr = (filtered[attr_cols]
               .agg(['size', 'count', 'mean'])
               .T
               .round(1)
               .reset_index())
totals_attr.columns = ['Attributes', 'Total Size', 'Count', 'Average']

##totals_attr['Total'] = totals_attr['Total'].astype(int)
totals_attr['Attributes'] = totals_attr['Attributes'].replace({
    'attr_rating_1': 'Attribute 1',
    'attr_rating_2': 'Attribute 2',
    'attr_rating_3': 'Attribute 3',
    'attr_rating_4': 'Attribute 4',
    'attr_rating_5': 'Attribute 5',
})

st.dataframe(totals_attr)
fig_total_attr = px.bar(
    totals_attr,
    x='Attributes',
    y='Average',
    text='Average',
    color='Attributes',
    title='Total per Attributes',
    
)
fig_total_attr.update_traces(textposition='outside')
##fig_total_attr.update_layout(showlegend=False,)
##figss.show()


st.plotly_chart(fig_total_attr, width='stretch', key="fig_total_attr")