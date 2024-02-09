#############################################################################################
###Program Name: NYC.py
###Programmer: Aaliyah Raderberg
###Project: Build a Data Science Web App with Streamlit and Python (Coursera Project Network)
#############################################################################################

import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px

DATA_URL = ('https://raw.githubusercontent.com/araderberg/Streamlit/main/data/nyc_crashes.csv')

st.set_page_config(page_title='NYC MVC - Streamlit', page_icon=":car:")

st.image('https://aaliyahraderberg.files.wordpress.com/2024/02/araderberg_alogo.png', use_column_width=True )

st.title("🚗 Motor Vehicle Collisions in NYC")
st.markdown("Uncover collision patterns in any city! This interactive Streamlit app lets you visualize and analyze "
" traffic accidents. (New York City data pre-loaded*)")

@st.cache_resource
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, parse_dates=[['CRASH_DATE', 'CRASH_TIME']])
    data.dropna(subset=['LATITUDE', 'LONGITUDE'], inplace=True)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data.rename(columns={'crash_date_crash_time': 'date/time'}, inplace=True)
    return data

data = load_data(5000)
original_data = data

#get closer to Manhattan, NY
st.subheader("🧑‍🦯 Where are the most people injured in NYC?")
injured_pedestrians = st.slider("Number of persons injured in vehicle collisions", 0, 19)
df = df = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [40.72833, -73.99417],
    columns=['latitude', 'longitude'])

st.map(df)

st.header("🚦How many collisions occur during a given time of day?")
hour = st.slider("Hour to look at", 0, 23)
#hour = st.sidebar.slider("Hour to look at", 0, 23)
#hour = st.selectbox("Hour to look at", range(0, 24), 1)
data = data[data['date/time'].dt.hour == hour]

st.markdown("🚘Vehicle Collisions between %i:00 and %i:00" % (hour, (hour + 1) %24))
midpoint = (np.average(data['latitude']), np.average(data['longitude']))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data[['date/time', 'latitude', 'longitude']],
        get_position=['longitude', 'latitude'],
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0,1000],
        ),
    ],
))

st.subheader("⌛ Breakdown by Minute between %i:00 and %i:00" %(hour, (hour + 1) %24))
filtered = data[
    (data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))
]
hist = np.histogram(filtered['date/time'].dt.minute, bins=60, range=(0,60))[0]
chart_data = pd.DataFrame({'minute': range(60), 'crashes':hist})
fig = px.bar(chart_data, x='minute', y='crashes', hover_data=['minute', 'crashes'], height=400)
st.write(fig)

st.header("🚷🚴🚗 Top 5 Dangerous Streets by Collision Type")
select = st.selectbox('Affected Type of People', ['Cyclists', 'Motorists', 'Pedestrians'])

if select == 'Pedestrians':
    st.write(original_data.query("injured_pedestrians >= 1")[["on_street_name","injured_pedestrians"]].sort_values(by=['injured_pedestrians'], ascending=False).dropna(how='any')[:5])
elif select == 'Cyclists':
    st.write(original_data.query("injured_cyclists >= 1")[["on_street_name","injured_cyclists"]].sort_values(by=['injured_cyclists'], ascending=False).dropna(how='any')[:5])
else:
    st.write(original_data.query("injured_motorists >= 1")[["on_street_name","injured_motorists"]].sort_values(by=['injured_motorists'], ascending=False).dropna(how='any')[:5])

if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)


st.markdown("""<h6 style='text-align: center; color: grey;'>Citations: Learning Streamlit and posting this app is inspired by </br>Coursera Hands-on project network <a href="https://www.coursera.org/projects/data-science-streamlit-python">[Snehan Kekre]</a>
</br>*Due to data size restrictions, only a small subset of the data from 2020 - 2017 was used.
</br>NYC Collision Data Analysis Project | Feb 2024 | <a href="https://www.linkedin.com/in/ikhouvanwesties/">[Aaliyah Raderberg]</a></h6>""", unsafe_allow_html=True)


