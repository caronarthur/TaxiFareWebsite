import streamlit as st
import datetime
import requests
import pandas as pd

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
p_longitude = st.sidebar.number_input('Insert the pickup longitude')

'''
- pickup latitude
'''
p_latitude = st.sidebar.number_input('Insert the pickup latitude')
'''
- dropoff longitude
'''
d_longitude = st.sidebar.number_input('Insert the dropoff longitude')
'''
- dropoff latitude
'''
d_latitude = st.sidebar.number_input('Insert the dropoff latitude')
'''
- passenger count
'''

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

if p_longitude == 0 and p_latitude == 0 and d_longitude == 0 and d_latitude == 0:
    prediction = 0
    st.markdown("# please fill in the parameters")
else:
    prediction = round(response.json()['prediction'], 2)
    st.markdown(f'# the prediction of the taxe fare price is {prediction} dollars ! ')
    







