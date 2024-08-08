import pymssql
from os import getenv
from datetime import datetime, timezone, timedelta, date
import streamlit as st
import altair as alt
import pandas as pd
import numpy as np
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

#get all the variables required for the filters and filter
def get_botanists(conn):
    """Obtains all possible botanists' names"""
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

def get_plant_ids(conn):
    """Obtains all possible plant ids"""
    query = """SELECT plant_id FROM alpha.plant_health"""
    with conn.cursor() as cur:
        cur.execute(query)
        all_data = cur.fetchall()
    conn.commit()
    ids = sorted(list(set([id[0] for id in all_data])))
    return ids

def filter_data(conn):
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

    #filtered by plant id
    plant_choices = get_plant_ids(connection)
    plants_selected = st.sidebar.multiselect(
        "**Filter by Plant ID**", plant_choices)
    if plants_selected:
        if len(plants_selected) == 1:
            plants_selected = f"('{plants_selected[0]}')"
        else:
            plants_selected = tuple(plants_selected)
        all_data = f"""{all_data},
        plant_data AS(
            SELECT *
            FROM {data}
            WHERE plant_id in {plants_selected})
        """
        data = 'plant_data'

    #filtered by botanist
    botanist_choices = get_botanists(conn)
    botanist_selected = st.sidebar.multiselect(
        "**Filter by] Botanist**", botanist_choices)
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
        "**Filter by Continent**", continent_choices)
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

    # filter by only today's data
    now = str((datetime.now(timezone.utc).strftime('%H.%M')))
    col1, col2 = st.sidebar.columns(2)
    with col1:
        hour = st.number_input("For a specific hour", value=int(now[:2]), min_value=0,
                               max_value=int(now[:2]))
    with col2:
        if hour == int(now[:2]):
            max_min = int(now[3:])
        else:
            max_min = 59
        minute = st.number_input("For a specific minute", value=int(now[3:]), min_value=0,
                                 max_value=max_min)
    today = str(datetime.now().strftime('%Y-%m-%d'))
    end_time = datetime.strptime(today+str(hour)+'.'+str(minute), '%Y-%m-%d%H.%M')
    live_time = end_time - timedelta(minutes=1)
    delayed_time = end_time - timedelta(minutes=10)

    delayed_data = f"""{all_data},
    live_data AS(
        SELECT *
        FROM {data}
        WHERE recording_time > '{delayed_time}' AND recording_time < '{end_time}')
    """
    delayed_query = f"""{delayed_data} SELECT * FROM live_data;"""

    all_data = f"""{all_data},
    live_data AS(
        SELECT *
        FROM {data}
        WHERE recording_time > '{live_time}' AND recording_time < '{end_time}')
    """
    data = 'live_data'

    live_query = f"""{all_data} SELECT * FROM {data};"""


    with conn.cursor() as cur:
        cur.execute(live_query)
        live_points = cur.fetchall()
        cur.execute(delayed_query)
        delayed_points = cur.fetchall()
    conn.commit()

    live_df = pd.DataFrame(live_points, columns =['name', 'continent_name', 'plant_name',
                                                  'recording_time','soil_moisture', 'temperature', 
                                                  'last_watered', 'plant_id'])
    delayed_df = pd.DataFrame(delayed_points, columns =['name', 'continent_name', 'plant_name',
                                                'recording_time','soil_moisture', 'temperature',
                                                'last_watered', 'plant_id'])
    return (live_df, delayed_df)

def filter_graph_range():
     #add min max values for the soil moisture
    st.sidebar.divider()
    st.sidebar.write('**Soil Moisture range**')
    col1, col2 = st.sidebar.columns(2)
    with col1:
        s_min = st.number_input("Min %", value=10, min_value=0, max_value=99)
    with col2:
        s_max = st.number_input("Max %", value=110, min_value=1, max_value=110)
    st.sidebar.write('**Temperature range**')
    col1, col2 = st.sidebar.columns(2)
    with col1:
        t_min = st.number_input("Min C", value=5, min_value=0, max_value=99)
    with col2:
        t_max = st.number_input("Max c", value=20, min_value=1, max_value=100)
    return(s_min,s_max,t_min,t_max)

def outliers(data):
    soil_outliers = data[(data['soil_moisture'] < 10) | ((data['soil_moisture'] > 100))]
    soil_errors = {}
    if not soil_outliers.empty:
        for i, val in soil_outliers.iterrows():
            id = val['plant_id']
            soil_errors[id] = soil_errors.get(id, 0) + 1
    temp_outliers = data[(data['temperature'] < 8) | (data['temperature'] > 18)]
    temp_errors = {}
    if not temp_outliers.empty:
        for i, val in temp_outliers.iterrows():
            id = val['plant_id']
            temp_errors[id] = temp_errors.get(id, 0) + 1
    return(temp_errors, soil_errors)

def remove_outliers(data):
    sq1 = data['soil_moisture'].quantile(0.25)
    sq3 = data['soil_moisture'].quantile(0.75)
    siqr = sq3 - sq1
    threshold = 1.5
    outliers = data[(data['soil_moisture'] < sq1 - threshold * siqr) |
                    (data['soil_moisture'] > sq3 + threshold * siqr)]
    data = data.drop(outliers.index)
    tq1 = data['temperature'].quantile(0.25)
    tq3 = data['temperature'].quantile(0.75)
    tiqr = tq3 - tq1
    outliers = data[(data['temperature'] < tq1 - threshold * tiqr) |
                    (data['temperature'] > tq3 + threshold * tiqr)]
    data = data.drop(outliers.index)
    # replace outliers with median value
    # data.loc[z > threshold, 'Height'] = df['Height'].median()
    return data



# To be displayed
def temp_vs_moist(data:pd.DataFrame, s_min,s_max,t_min,t_max):# -> alt.Chart? type says <class 'altair.vegalite.v5.api.Chart'>
    """
    Scatter graph showing the relationship between temperature and soil moisture
    """
    moist_temp = alt.Chart(data).mark_circle(size=60).encode(
    x=alt.X('temperature:Q', title='Temperature °C',scale=alt.Scale(domain=[t_min, t_max])),
    y=alt.Y('soil_moisture:Q', title='Soil Moisture %', scale=alt.Scale(domain=[s_min, s_max])),
    color=alt.Color('plant_id:N',legend=None)).interactive()

    band1 = alt.Chart(data).mark_errorband(extent="stdev", opacity=0.15).encode(
    alt.Y("soil_moisture:Q", title=''))

    band2 = alt.Chart(data).mark_errorband(extent="stdev", opacity=0.1).encode(
    alt.X("temperature:Q", title=''))

    # rule1 = alt.Chart(data).mark_rule(opacity=0.3, stroke='red').encode(
    # x='mean(temperature):Q')

    # rule2 = alt.Chart(data).mark_rule(opacity=0.3, stroke='red').encode(
    # y='mean(soil_moisture):Q')

    moist_temp = moist_temp+band1+band2#+rule1+rule2
    return moist_temp.configure_axis(gridColor='grey')

def warnings(temp=None, soil=None):
    """
    Displays warnings for any plants that need attention
    Has these as a list with checkboxes so that you can keep track of which plants you have checked
    (the input 'data' is a tuple, data[0] is the outliers based on the moisture, data[1] is based ont he temperature)
    """
    if (temp or soil):
        st.subheader(':rotating_light: **:red[WARNINGS:]**', help='Plants that have had more than 3 concerning value in the last 10 minutes')
        for t in temp:
            st.markdown(f"""**Plant {t}'s temperature is too high**""", help='\\> 31°C')
        for s in soil:
            st.markdown(f"""**Plant {s} has a low soil moisture**""", help='\\< 20%')
        st.divider()

def display_warnings(data):
    temp_fault = faulty_readings[0]
    soil_fault = faulty_readings[1]
    bad_temp = []
    if temp_fault:
        for element, value in temp_fault.items():
            if value >=3:
                bad_temp.append(element)
    bad_soil = []
    if soil_fault:
        for element, value in soil_fault.items():
            if value >=3:
                bad_soil.append(element)
    warnings(bad_temp, bad_soil)

if __name__ == "__main__":
    load_dotenv()
    connection = get_connection()
    data = filter_data(connection)
    current_data = data[0]

    live_tab, historical_tab = st.tabs(["Live", "Historical"])

    current_data = remove_outliers(current_data)
    with live_tab:
        data = data[1]
        faulty_readings = outliers(data)
        display_warnings(faulty_readings)
        
        col1, col2 = st.columns([1,4])
        with col1:
            st.write('')
        with col2:
            st.markdown("""<span style="font-size:2em;"><b>Plant Moisture and Temperature</b></span>""", unsafe_allow_html=True, help='of all plants - recorded in the last minute')
        
        (min_s,max_s,min_t,max_t) = filter_graph_range()
        graph = temp_vs_moist(current_data, min_s,max_s,min_t,max_t)
        st.altair_chart(graph, use_container_width=True)

        #consider:https://altair-viz.github.io/gallery/multiline_highlight.html
        #also: altair has interpolation if we want to add eg an average line