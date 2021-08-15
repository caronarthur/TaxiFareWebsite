import streamlit as st
import datetime
import requests
import pandas as pd
import pydeck as pdk

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
- pickup longitude
'''
p_longitude = st.sidebar.number_input('Insert the pickup longitude', value = -73.9385)

'''
- pickup latitude
'''
p_latitude = st.sidebar.number_input('Insert the pickup latitude', value= 40.6643)
'''
- dropoff longitude
'''
d_longitude = st.sidebar.number_input('Insert the dropoff longitude', value = -73.9385)
'''
- dropoff latitude
'''
d_latitude = st.sidebar.number_input('Insert the dropoff latitude', value= 40.6643)
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
        

    