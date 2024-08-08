import pymssql
from os import getenv
from datetime import datetime, timedelta
import streamlit as st
import altair as alt
import pandas as pd
from dotenv import load_dotenv

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


def get_botanists():
    """Obtains data about botanists from the RDS database"""
    load_dotenv()
    conn = get_connection()
    query = """SELECT * FROM alpha.botanist;"""
    with conn.cursor() as cur:
        cur.execute(query)
        all_data = cur.fetchall()
    conn.commit()
    return all_data

def get_temp_vs_moist(conn):
    now = datetime.now()
    a_minute_ago = (now - timedelta(minutes=700)).strftime("%Y-%m-%d %H:%M")
    print('minute', a_minute_ago)
    now = (datetime.strptime(a_minute_ago,"%Y-%m-%d %H:%M") + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M")
    print('now', now)
    query = """
    SELECT plant_id, soil_moisture, temperature 
    FROM alpha.plant_health
    WHERE recording_time > %s AND recording_time < %s;
    """
    with conn.cursor() as cur:
        cur.execute(query,(a_minute_ago, now)) #cur.execute(query,a_minute_ago, now)
        all_data = cur.fetchall()
    conn.commit()
    data_df = pd.DataFrame(all_data, columns =['plant_id', 'soil_moisture', 'temperature'])
    return data_df

def temp_vs_moist(data):
    """
    Scatter graph showing the relationship between temperature and soil moisture
    """
    moist_temp = alt.Chart(data).mark_circle(size=60).encode(
    x=alt.X('temperature', scale=alt.Scale(domain=[5, 20])),
    y=alt.Y('soil_moisture', scale=alt.Scale(domain=[0, 110])),
    color=alt.Color('plant_id:N',legend=None)).interactive()

    return moist_temp

def outliers(data):
    #decided based on average values
    soil_outliers = (data['soil_moisture'] < 10) | ((data['soil_moisture'] > 30) & (data['soil_moisture'] < 95))
    temp_outliers = (data['temperature'] < 8) | (data['temperature'] > 31)
    return (data.loc[soil_outliers], data.loc[temp_outliers])

def warnings(data):
    st.subheader(':rotating_light: **:red[WARNINGS:]**', help='Plants that need checking')
    for idx, i in data[0].iterrows():
        st.checkbox(f"""**Plant with ID {i['plant_id'].item()} has soil moisture: {round(i['soil_moisture'].item(),2)}**""")
    for idx, i in data[1].iterrows():
        st.checkbox(f"""**Plant with ID {i['plant_id'].item()} has temperature: {i['temperature'].item()}**""")

def filter_data(conn):
    botanist_choices = [i[1] for i in get_botanists()]
    print(tuple(botanist_choices))
    botanist_selected = st.sidebar.multiselect(
        "Filter by Botanist", botanist_choices)
    if botanist_selected:
        query = """
        WITH combined AS(
            SELECT b.name, ph.plant_id, ph.soil_moisture, ph.temperature, ph.recording_time
            FROM alpha.plant p, alpha.botanist b, alpha.plant_health ph
            WHERE b.botanist_id = p.botanist_id AND ph.plant_id = p.plant_id
            )
        SELECT plant_id, soil_moisture, temperature, recording_time
        FROM combined
        WHERE name in %s;
        """
        with conn.cursor() as cur:
            cur.execute(query,tuple(botanist_selected))
            all_data = cur.fetchall()
        conn.commit()
        data_df = pd.DataFrame(all_data, columns =['plant_id', 'soil_moisture', 'temperature', 'recording_time'])
        return data_df

if __name__ == "__main__":
    load_dotenv()
    connection = get_connection()
    #print(filter_data(connection))
    tab1, tab2 = st.tabs(["Live", "Historical"])

    with tab1:
        st.sidebar.multiselect('Choose a botanist',['a','b','c'])
        errors = outliers(get_temp_vs_moist(connection))
        if not (errors[0].empty and errors[1].empty):
            warnings(errors)
        st.header("Temperature and Moisture of the last minute")
        graph = temp_vs_moist(get_temp_vs_moist(connection))
        st.altair_chart(graph, use_container_width=True)
