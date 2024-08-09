"""Using streamlit to display an informative dashboard about all plant data"""
from os import getenv
from datetime import datetime, timezone, timedelta
from math import ceil, floor
import pymssql
from pymssql._pymssql import Connection
import streamlit as st
import altair as alt
import pandas as pd
from dotenv import load_dotenv
from get_long_term import get_long_term_data


st.set_page_config(layout="wide")

def get_connection() -> Connection:
    """
    Establishes a connection to the database
    """
    return pymssql.connect(
        host=getenv("DB_HOST"),
        user=getenv("DB_USER"),
        password=getenv("DB_PASSWORD"),
        database=getenv("DB_NAME"),
        port=getenv("DB_PORT"),
        tds_version="7.0",
    )


def get_botanists(conn: Connection) -> list[str]:
    """
    Obtains all possible botanists' names
    """
    query = """SELECT name FROM alpha.botanist"""
    with conn.cursor() as cur:
        cur.execute(query)
        all_data = cur.fetchall()
    conn.commit()
    names = [name[0] for name in all_data]
    return names


def get_origin_continent(conn: Connection) -> set:
    """
    Obtains all possible continents' names
    """
    query = """SELECT continent_name FROM alpha.origin_location"""
    with conn.cursor() as cur:
        cur.execute(query)
        all_data = cur.fetchall()
    conn.commit()
    names = sorted({name[0] for name in all_data})
    return names

def get_plant_ids(conn: Connection) -> set:
    """
    Obtains all possible plant ids
    """
    query = """SELECT plant_id FROM alpha.plant_health"""
    with conn.cursor() as cur:
        cur.execute(query)
        all_data = cur.fetchall()
    conn.commit()
    ids = sorted({id[0] for id in all_data})
    ids.remove(0)
    return ids

def filter_data(conn: Connection) -> tuple[pd.DataFrame]:
    """
    Returns only the data that has been filtered based on the options chosen through the sidebar
    """
    all_data = """
    WITH all_data AS(
        SELECT b.name, o.continent_name, p.plant_name, ph.recording_time, ph.soil_moisture, ph.temperature, ph.last_watered, ph.plant_id
        FROM alpha.botanist b, alpha.origin_location o, alpha.plant p, alpha.plant_health ph
        WHERE b.botanist_id = p.botanist_id AND o.origin_location_id=p.origin_location_id AND ph.plant_id=p.plant_id
        )"""
    data = 'all_data'
    plant_choices = get_plant_ids(conn)
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

    botanist_choices = get_botanists(conn)
    botanist_selected = st.sidebar.multiselect(
        "**Filter by Botanist**", botanist_choices)
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

def filter_graph_range(d_min_s: int,d_max_s: int,d_min_t: int,d_max_t: int) -> tuple[int]:
    """
    Display a defined range for the temperature vs moisture graph
    """
    st.sidebar.write('**Soil Moisture range**')
    col1, col2 = st.sidebar.columns(2)
    with col1:
        s_min = st.number_input("Min %", value=d_min_s)
    with col2:
        s_max = st.number_input("Max %", value=d_max_s)
    st.sidebar.write('**Temperature range**')
    col1, col2 = st.sidebar.columns(2)
    with col1:
        t_min = st.number_input("Min C", value=d_min_t)
    with col2:
        t_max = st.number_input("Max c", value=d_max_t)
    return (s_min,s_max,t_min,t_max)

def outliers(data: pd.DataFrame) -> tuple[dict]:
    """
    Finds any values determined as outliers 
    Defined as: moisture < 10 and > 100, temperature < 8 or >18
    """
    soil_outliers = data[(data['soil_moisture'] < 10) | ((data['soil_moisture'] > 100))]
    soil_errors = {}
    if not soil_outliers.empty:
        for _, val in soil_outliers.iterrows():
            p_id = val['plant_id']
            soil_errors[p_id] = soil_errors.get(p_id, 0) + 1
    temp_outliers = data[(data['temperature'] < 8) | (data['temperature'] > 18)]
    temp_errors = {}
    if not temp_outliers.empty:
        for _, val in temp_outliers.iterrows():
            p_id = val['plant_id']
            temp_errors[p_id] = temp_errors.get(p_id, 0) + 1
    return(temp_errors, soil_errors)

def remove_outliers(data: pd.DataFrame, included: bool=True) -> tuple[pd.DataFrame, int, int, int, int]:
    """
    Removes outliers if they are more than 1.5 IQR away from the IQR
    """
    if included:
        s_min = int(floor(min(data['soil_moisture'])))
        s_max = int(ceil(max(data['soil_moisture'])))
        t_min = int(floor(min(data['temperature'])))
        t_max = int(ceil(max(data['temperature'])))
    sq1 = data['soil_moisture'].quantile(0.25)
    sq3 = data['soil_moisture'].quantile(0.75)
    siqr = sq3 - sq1
    threshold = 1.5
    outlying_points = data[(data['soil_moisture'] < sq1 - threshold * siqr) |
                    (data['soil_moisture'] > sq3 + threshold * siqr)]
    data = data.drop(outlying_points.index)
    tq1 = data['temperature'].quantile(0.25)
    tq3 = data['temperature'].quantile(0.75)
    tiqr = tq3 - tq1
    outlying_points = data[(data['temperature'] < tq1 - threshold * tiqr) |
                    (data['temperature'] > tq3 + threshold * tiqr)]
    data = data.drop(outlying_points.index)
    if not included:
        s_min = int(floor(min(data['soil_moisture'])))
        s_max = int(ceil(max(data['soil_moisture'])))
        t_min = int(floor(min(data['temperature'])))
        t_max = int(ceil(max(data['temperature'])))
    return (data, s_min-1,s_max+1,t_min-1,t_max+1)

def temp_vs_moist(data:pd.DataFrame, s_min: int,s_max: int,t_min:int, t_max:int) -> alt.Chart:
    """
    Scatter graph showing the relationship between temperature and soil moisture
    """
    moist_temp = alt.Chart(data).mark_circle(size=60).encode(
    x=alt.X('temperature:Q', title='Temperature °C',scale=alt.Scale(domain=[t_min, t_max])),
    y=alt.Y('soil_moisture:Q', title='Soil Moisture %', scale=alt.Scale(domain=[s_min, s_max])),
    color=alt.Color('plant_id:N',legend=None)).interactive()

    band1 = alt.Chart(data).mark_errorband(extent="stdev", opacity=0.1, borders=True).encode(
    y=alt.Y("soil_moisture:Q", title=''))

    band2 = alt.Chart(data).mark_errorband(extent="stdev", opacity=0.1, borders=True).encode(
    alt.X("temperature:Q", title=''))

    moist_temp = moist_temp+band1+band2
    return moist_temp.configure_axis(gridColor='grey')

def warnings(temp:bool=None, soil:bool=None) -> None:
    """
    Displays warnings for any plants that need attention
    Has these as a list with checkboxes so that you can keep track of which plants you have checked
    """
    if (temp or soil):
        st.subheader(':rotating_light: **:red[WARNINGS:]**',
                    help='Plants that have had more than 3 concerning value in the last 10 minutes')
        for t in temp:
            st.markdown(f"""**Plant {t}'s temperature is too high**""", help='\\> 31°C')
        for s in soil:
            st.markdown(f"""**Plant {s} has a low soil moisture**""", help='\\< 20%')
        st.divider()

def display_warnings(data: pd.DataFrame) -> None:
    """
    Shows the ID of any outlier if they have occurred > 3 times in the last 10 minutes
    """
    temp_fault = data[0]
    soil_fault = data[1]
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

#linfan woz ere
#HI :)))))

def get_botanists_mapping(conn: Connection) -> dict:
    """
    Obtains botanist mapping
    """
    query = """SELECT botanist_id, name FROM alpha.botanist"""
    with conn.cursor(as_dict=True) as cur:
        cur.execute(query)
        rows= cur.fetchall()
    conn.commit()
    botanists = {row["botanist_id"]: row["name"] for row in rows}
    return botanists

def get_origin_continent_mapping(conn: Connection) -> dict:
    """
    Obtains continent mapping
    """
    query = """SELECT origin_location_id, continent_name FROM alpha.origin_location"""
    with conn.cursor(as_dict=True) as cur:
        cur.execute(query)
        rows= cur.fetchall()
    conn.commit()
    continents = {row["origin_location_id"]: row["continent_name"] for row in rows}
    return continents

def get_plant_mapping(conn: Connection) -> dict:
    """
    Obtains mapping for primary and foreign keys in plant table
    """
    query = """SELECT plant_id, botanist_id, origin_location_id FROM alpha.plant"""
    with conn.cursor() as cur:
        cur.execute(query)
        data= cur.fetchall()
    conn.commit()
    df = pd.DataFrame(data, columns=['plant_id', 'botanist_id', 'origin_location_id'])
    return df

def historical_join_mappings(df_historical: pd.DataFrame, df_mapping:  pd.DataFrame) -> pd.DataFrame:
    """
    Joins historical data with botanists and continents
    """
    df = pd.merge(df_historical, df_mapping, how='inner', on='plant_id')
    df = df.replace({"botanist_id": get_botanists_mapping(get_connection())})
    df = df.replace({"origin_location_id": get_origin_continent_mapping(get_connection())})
    df = df.rename(columns={'botanist_id': 'name', 'origin_location_id': 'continent_name'})
    return df

def graph_numbers_in_column(number_of_graphs: int, column_number: int) -> list[int]:
    """
    Finds the graph indices that should be plotted in a given column index
    """
    number_of_columns = floor(number_of_graphs**0.5)
    number_of_rows = ceil(number_of_graphs / number_of_columns)
    graph_numbers = []
    for r in range(1, number_of_rows + 1):
        n = (r - 1) * number_of_columns + column_number
        if n <= number_of_graphs:
            graph_numbers.append(n)
    return graph_numbers

def historical_sidebar(conn: Connection) -> tuple[list]:
    """
    Adds filters for the sidebar for historic dataset
    """
    st.sidebar.divider()
    st.sidebar.title('Historical Data Filters')

    plant_choices = get_plant_ids(conn)
    plants_selected = st.sidebar.multiselect(
        "**Filter historical by Plant ID**", plant_choices, key = "plant_hist")
    if not plants_selected:
        plants_selected = plant_choices


    botanist_choices = get_botanists(conn)
    botanist_selected = st.sidebar.multiselect(
        "**Filter historical by Botanist**", botanist_choices ,key = "bot_hist")
    if not botanist_selected:
        botanist_selected = botanist_choices


    continent_choices = get_origin_continent(conn)
    continent_selected = st.sidebar.multiselect(
        "**Filter historical by Continent**", continent_choices, key = "cont_hist")
    if not continent_selected:
        continent_selected = continent_choices

    return plants_selected, botanist_selected, continent_selected

def plot_historic_graphs(df: pd.DataFrame) -> alt.Chart:
    """
    Line graph of soil moisture and temperature over time
    """

    source = df

    chart_base = alt.Chart(source).encode(
    x=alt.X(
        'recording_time:T', 
        axis=alt.Axis(title='Recording Time'),
        scale=alt.Scale(zero=False)
        )
    )

    soil_moisture_line = chart_base.mark_line(color='blue', size=1,point=True).encode(
        y=alt.Y('soil_moisture:Q', axis=alt.Axis(title='Soil Moisture (%)'))
    )

    temperature_line = chart_base.mark_line(color='red', size=1, point=True).encode(
        y=alt.Y('temperature:Q', axis=alt.Axis(title='Temperature (°C)'))
    )

    return alt.layer(soil_moisture_line, temperature_line).properties(
        title=f'Plant ID {df["plant_id"].iloc[0]}'
    ).resolve_scale(y='independent')


def display_live_tab(conn: Connection) -> None:
    """
    Combining everything that will belong to the live tab
    """
    st.sidebar.title('Live Data Filters')
    show_outliers = st.sidebar.toggle('Include outliers', help='Anything outside 1.5 x IQR')
    zoom_out = st.sidebar.toggle('Zoom out')
    data = filter_data(conn)
    current_data = data[0]
    (def_min_s,def_max_s,def_min_t,def_max_t)=remove_outliers(current_data)[1:]
    if not show_outliers:
        current_data = remove_outliers(current_data, False)[0]
        (def_min_s,def_max_s,def_min_t,def_max_t)=remove_outliers(current_data, False)[1:]
    if zoom_out:
        (def_min_s,def_max_s,def_min_t,def_max_t)=(0,100,5,25)
    data = data[1]
    faulty_readings = outliers(data)
    display_warnings(faulty_readings)
    st.markdown(
    """
    <span style="font-size:2em;"><b>Plant Moisture and Temperature</b></span>
    """,
    unsafe_allow_html=True,
    help='of all plants - recorded in the last minute'
    )
    st.write('')
    (min_s,max_s,min_t,max_t) = filter_graph_range(def_min_s,def_max_s,def_min_t,def_max_t)
    graph = temp_vs_moist(current_data, min_s,max_s,min_t,max_t)
    st.altair_chart(graph, use_container_width=True)


def display_historic_tab(conn: Connection) -> None:
    """
    Combining everything that will belong to the historical tab
    """
    old_data = historical_sidebar(conn)
    plants_selected, botanist_selected, continent_selected=old_data[0], old_data[1], old_data[2]
    df = historical_join_mappings(get_long_term_data(), get_plant_mapping(conn))
    filtered_df = df[(df['plant_id'].isin(plants_selected)) &
                (df['name'].isin(botanist_selected)) &
                (df['continent_name'].isin(continent_selected))]

    plants_df_list = []
    for plant in sorted(filtered_df['plant_id'].unique()):
        if len(plants_df_list) < 12:
            plants_df_list.append(filtered_df[filtered_df['plant_id']==plant])
        else:
            break

    number_of_columns = floor(len(plants_df_list)**0.5)

    if number_of_columns > 0:
        cols = st.columns(number_of_columns)
        for col in range(number_of_columns):
            with cols[col]:
                nums= graph_numbers_in_column(len(plants_df_list), col+1)
                for num in nums:
                    df_hist = plants_df_list[num-1]
                    st.write('')
                    graph = plot_historic_graphs(df_hist)
                    st.altair_chart(graph, use_container_width=True)


def dashboard() -> None:
    """
    Main function to display the dashboard
    """
    load_dotenv()
    connection = get_connection()

    st.title('LMNH Plant Environment Monitoring :seedling:')
    live_tab, historical_tab = st.tabs(["Live", "Historical"])
    with live_tab:
        display_live_tab(connection)

    with historical_tab:
        st.subheader('LMNH Plant Historical Data')
        st.write('The first 12 plots matching the sidebar search filters are shown below:')
        st.divider()
        st.write('**Plotting Legend**')
        st.write(':red_circle: Temperature (°C)')
        st.write(':large_blue_circle: Soil Moisture (%)')

        display_historic_tab(connection)


if __name__ == "__main__":
    dashboard()
