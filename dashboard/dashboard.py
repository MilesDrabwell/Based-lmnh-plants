import pymssql
from os import getenv
from datetime import datetime, timedelta
import streamlit as st
import altair as alt
import pandas as pd
from dotenv import load_dotenv

#establish a connection
def get_connection():
    """
    Establishes a connection to the database
    """
    return pymssql.connect(
        host=getenv("DB_HOST"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        database=getenv("DB_NAME"),
        port=getenv("DB_PORT")
    )

#get all the variables required for the filters
def get_botanists(conn):
    """Obtains data about botanists from the RDS database"""
    query = """SELECT * FROM alpha.botanist"""
    with conn.cursor() as cur:
        cur.execute(query)
        all_data = cur.fetchall()
    conn.commit()
    return all_data

def get_time_range():
    pass

def get_origin_countries():
    pass

def temp_vs_moist(data:pd.DataFrame):# -> alt.Chart? type says <class 'altair.vegalite.v5.api.Chart'>
    """
    Scatter graph showing the relationship between temperature and soil moisture
    """
    moist_temp = alt.Chart(data).mark_circle(size=60).encode(
    x=alt.X('temperature', scale=alt.Scale(domain=[5, 20])),
    y=alt.Y('soil_moisture', scale=alt.Scale(domain=[0, 110])),
    color=alt.Color('plant_id:N',legend=None)).interactive()

    return moist_temp

def outliers(data:pd.DataFrame)->tuple[pd.DataFrame]:
    #decided based on average values
    soil_outliers = (data['soil_moisture'] < 10) | ((data['soil_moisture'] > 30) & (data['soil_moisture'] < 95))
    temp_outliers = (data['temperature'] < 8) | (data['temperature'] > 31)
    return (data.loc[soil_outliers], data.loc[temp_outliers])

def warnings(data:tuple[pd.DataFrame]):
    """
    Displays warnings for any plants that need attention
    Has these as a list with checkboxes so that you can keep track of which plants you have checked
    (the input 'data' is a tuple, data[0] is the outliers based on the moisture, data[1] is based ont he temperature)
    """
    st.subheader(':rotating_light: **:red[WARNINGS:]**', help='Plants that need checking')
    for idx, i in data[0].iterrows():
        st.checkbox(f"""**Plant with ID {i['plant_id']} has soil moisture: {round(i['soil_moisture'],2)}**""")
    for idx, i in data[1].iterrows():
        st.checkbox(f"""**Plant with ID {i['plant_id']} has temperature: {i['temperature']}**""")

def filter_data(conn, live=True):
    """
    Returns only the data that has been filtered based on the options chosen through the sidebar
    """
    all_data = """
    WITH all_data AS(
        SELECT b.name, o.continent_name, p.plant_name, ph.recording_time, ph.soil_moisture, ph.temperature, ph.last_watered, ph.plant_id
        FROM alpha.botanist b, alpha.origin_location o, alpha.plant p, alpha.plant_health ph
        WHERE b.botanist_id = p.botanist_id AND o.origin_location_id=p.origin_location_id AND ph.plant_id=p.plant_id
        )
    """
    data = 'all_data'

    botanist_choices = [i[1] for i in get_botanists(conn)]
    botanist_selected = st.sidebar.multiselect(
        "Filter by Botanist", botanist_choices)
    if botanist_selected:
        if len(botanist_selected) == 1:
            botanist_selected = f"('{botanist_selected[0]}')"
        else:
            botanist_selected = tuple(botanist_selected)
        all_data = f"""{all_data},
        botanist_data AS(
            SELECT *
            FROM {data}
            WHERE name in {botanist_selected})
        """
        data = 'botanist_data'

    if live:
        now = datetime.now()
        a_minute_ago = (now - timedelta(minutes=1240)).strftime("%Y-%m-%d %H:%M")
        print('minute', a_minute_ago)
        now = (datetime.strptime(a_minute_ago,"%Y-%m-%d %H:%M") + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M")
        print('now', now)
        print('data from',data)
        all_data = f"""{all_data},
        live_data AS(
            SELECT *
            FROM {data}
            WHERE recording_time > '2024-08-07 13:48' AND recording_time < '2024-08-07 13:49')
        """
        data = 'live_data'

    query = f"""{all_data} SELECT * FROM {data};"""
    with conn.cursor() as cur:
        cur.execute(query)
        data_points = cur.fetchall()
    conn.commit()
    data_df = pd.DataFrame(data_points, columns =['name', 'continent_name', 'plant_name', 'recording_time',
                                                        'soil_moisture', 'temperature', 'last_watered', 'plant_id'])
    return data_df

if __name__ == "__main__":
    load_dotenv()
    connection = get_connection()
    tab1, tab2 = st.tabs(["Live", "Historical"])

    with tab1:
        live_data = filter_data(connection)
        errors = outliers(live_data)
        if not (errors[0].empty and errors[1].empty):
            warnings(errors)
        st.header("Temperature and Moisture of the last minute")
        graph = temp_vs_moist(live_data)
        st.altair_chart(graph, use_container_width=True)
