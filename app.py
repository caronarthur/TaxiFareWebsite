import streamlit as st
import datetime
import requests
import pandas as pd
import pydeck as pdk
import geopandas as gpd
import geopy

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

from streamlit.state.session_state import Value

'''
# TaxiFareModel application

please add the following information in the side bar to have an estimation of the taxi fare price:

'''

st.sidebar.markdown('''
Can you select the different parameters below:''')
'''
- date and time
'''
pickupdate = st.sidebar.date_input("Insert a pickup date")

pickuptime = st.sidebar.time_input("insert a pickup time")

'''
- insert the pickup street, city, province and country
'''
p_street = st.sidebar.text_input("Street", value = "5th avenue")
p_city = st.sidebar.text_input("City", value = "New York", key = "city 1")
p_country = st.sidebar.text_input("Country", value = "Usa", key = "country 1")

p_geolocator = Nominatim(user_agent="GTA Lookup")
p_geocode = RateLimiter(p_geolocator.geocode, min_delay_seconds=1)
p_location = p_geolocator.geocode(p_street+", "+p_city+", "+p_country)

p_latitude = p_location.latitude
p_longitude = p_location.longitude

'''
- insert the dropoff street, city, province and country
'''

d_street = st.sidebar.text_input("Street", value = "767 5th Ave")
d_city = st.sidebar.text_input("City", value = "New York", key = "city 2")
d_country = st.sidebar.text_input("Country", value ="Usa", key = "country 2")

d_geolocator = Nominatim(user_agent="GTA Lookup")
d_geocode = RateLimiter(d_geolocator.geocode, min_delay_seconds=1)
d_location = d_geolocator.geocode(d_street+", "+d_city+", "+d_country)

d_latitude = d_location.latitude
d_longitude = d_location.longitude

'''
- passenger count
'''
"""
## Please find below the map of New York

In blue you have the pickup location and in red the dropoff one
"""
p_count = st.sidebar.number_input('Insert the passenger count', step = 1)

pickupdatetime = str(pickupdate) + " " +str(pickuptime)

data = {"date and time" : pickupdatetime,
       "pickup longitude" : p_longitude,
       "pickup latitude" : p_latitude,
       "dropoff longitude" : d_longitude,
       "dropoff latitude": d_latitude,
       "passenger count": p_count
        }

url = f'https://taxifare.lewagon.ai/predict?pickup_datetime={pickupdatetime}&pickup_longitude={p_longitude}&pickup_latitude={p_latitude}&dropoff_longitude={d_longitude}&dropoff_latitude={d_latitude}&passenger_count={p_count}'

response = requests.get(url)

if response is None:
    prediction = 0
    st.markdown("# please fill in the parameters")
else:
    prediction = round(response.json()['prediction'], 2)
    dict_map = {'lat': [p_latitude, d_latitude], 'lon' : [p_longitude, d_longitude]}
    df = pd.DataFrame(dict_map)
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
         latitude=40.6643,
         longitude=-73.9385,
         zoom=11,
         pitch=50,
     ),
        layers=[
         pdk.Layer(
             'ScatterplotLayer',
             data=df[0:1],
             get_position='[lon, lat]',
             get_color='[0, 96, 255, 160]',
             get_radius=200,
         ),
         pdk.Layer(
             'ScatterplotLayer',
             data=df[1:2],
             get_position='[lon, lat]',
             get_color='[200, 30, 0, 160]',
             get_radius=200,
         ),
     ],
    ))
    if prediction > 0:
        prediction = round(response.json()['prediction'], 2)
        st.markdown(f'# the prediction of the taxe fare price is {prediction} dollars ! ')
    else:
        st.markdown("# please fill in the parameters")
        

    