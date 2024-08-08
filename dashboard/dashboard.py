import pymssql
from os import getenv
from datetime import datetime, timezone, timedelta, date
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
    """Obtains all possible botanists (only name is retrieved as it is the only thing we need for the moment)"""
    query = """SELECT name FROM alpha.botanist"""
    with conn.cursor() as cur:
        cur.execute(query)
        all_data = cur.fetchall()
    conn.commit()
    names = [name[0] for name in all_data]
    return names

def get_time_range(conn):
    """Obtains the time range of all data"""
    query = """SELECT min(recording_time), max(recording_time) FROM alpha.plant_health"""
    with conn.cursor() as cur:
        cur.execute(query)
        all_data = cur.fetchall()
    conn.commit()
    return all_data[0]

def get_origin_continent(conn):
    """Obtains all possible continents' names"""
    query = """SELECT continent_name FROM alpha.origin_location"""
    with conn.cursor() as cur:
        cur.execute(query)
        all_data = cur.fetchall()
    conn.commit()
    names = sorted(list(set([name[0] for name in all_data])))
    return names

# Main chart for live data
def temp_vs_moist(data:pd.DataFrame):# -> alt.Chart? type says <class 'altair.vegalite.v5.api.Chart'>
    """
    Scatter graph showing the relationship between temperature and soil moisture
    """
    moist_temp = alt.Chart(data).mark_circle(size=60).encode(
    x=alt.X('temperature', title='Temperature °C',scale=alt.Scale(domain=[5, 20])),
    y=alt.Y('soil_moisture', title='Soil Moisture %', scale=alt.Scale(domain=[0, 110])),
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
        st.checkbox(f"""**Plant with ID {i['plant_id']} has soil moisture: {round(i['soil_moisture'],2)} %**""", key = idx)
    for idx, i in data[1].iterrows():
        st.checkbox(f"""**Plant with ID {i['plant_id']} has temperature: {i['temperature']} °C**""", key = idx)

def filter_data(conn, live=True):
    """
    Returns only the data that has been filtered based on the options chosen through the sidebar
    """
    #main query - gets all possible data if no filters
    all_data = """
    WITH all_data AS(
        SELECT b.name, o.continent_name, p.plant_name, ph.recording_time, ph.soil_moisture, ph.temperature, ph.last_watered, ph.plant_id
        FROM alpha.botanist b, alpha.origin_location o, alpha.plant p, alpha.plant_health ph
        WHERE b.botanist_id = p.botanist_id AND o.origin_location_id=p.origin_location_id AND ph.plant_id=p.plant_id
        )"""
    data = 'all_data'

    #filtered by botanist
    botanist_choices = get_botanists(conn)
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

    #filtered by continent
    continent_choices = get_origin_continent(conn)
    continent_selected = st.sidebar.multiselect(
        "Filter by Continent", continent_choices)
    if continent_selected:
        if len(continent_selected) == 1:
            continent_selected = f"('{continent_selected[0]}')"
        else:
            continent_selected = tuple(continent_selected)
        all_data = f"""{all_data},
        continent_data AS(
            SELECT *
            FROM {data}
            WHERE continent_name in {continent_selected})
        """
        data = 'continent_data'

    #filtered by only today's data
    if live:
        now = str((datetime.now(timezone.utc).strftime('%H.%M')))
        col1, col2 = st.sidebar.columns(2)
        with col1:
            hour = st.number_input("For a specific hour", value=int(now[:2]), max_value=int(now[:2]))
        with col2:
            if hour == int(now[:2]):
                max_min = int(now[3:])
            else:
                max_min = 59
            minute = st.number_input("For a specific minute", value=int(now[3:]), max_value=max_min)
            if not minute:
                minute=int(now[3:]) - 1
        today = str(datetime.now().strftime('%Y-%m-%d'))
        all_data = f"""{all_data},
        live_data AS(
            SELECT *
            FROM {data}
            WHERE recording_time > '{today} {hour}:{minute}' AND recording_time < '{today} {hour}:{minute+1}')
        """
        data = 'live_data'
    if not live:
        time_choice = get_time_range(connection)
        time_range = st.sidebar.date_input("Change date range: (will not affect live data)", value=[time_choice[0].date(), time_choice[1].date()], min_value=time_choice[0].date(), max_value=time_choice[1].date(), format='DD-MM-YYYY')
        if len(time_range) == 2:
            start = time_range[0].strftime("%Y-%m-%d")
            end = time_range[1].strftime("%Y-%m-%d")
            all_data = f"""{all_data},
            time_data AS(
                SELECT *
                FROM {data}
                WHERE recording_time > '{start}' AND recording_time <= '{end} 23:59:59')
            """
            data = 'time_data'
            print('found time range', time_range)

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
    #print(get_time_range(connection)[0].date())
    tab1, tab2 = st.tabs(["Live", "Historical"])

    with tab1:
        live_data = filter_data(connection, True)
        # errors = outliers(live_data)
        # if not (errors[0].empty and errors[1].empty):
        #     warnings(errors)
        st.header("Temperature and Moisture of the last minute")
        graph = temp_vs_moist(live_data)
        st.altair_chart(graph, use_container_width=True)
        

        # now = datetime.now()
        # a_minute_ago = (now - timedelta(minutes=1523)).strftime("%Y-%m-%d %H:%M")
        # print('minute', a_minute_ago)
        # now = (datetime.strptime(a_minute_ago,"%Y-%m-%d %H:%M") + timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M")
        # print('now', now)