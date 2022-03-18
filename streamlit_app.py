import datetime
import os
import streamlit as st
from pfss_notebook_lib import get_pfss_hmimap, symlog_pspiral

# replace with some sunpy function!!!
from pfss_notebook_lib import au_to_km

filepath = os.getcwd()  # "/home/chospa/solar_mach/pfss/"
email = "jan.gieseler@utu.fi"

carrington_rot = 2250


names = ['Stereo A']  # names of the object(s) (optional)
sw = [376]  # solar wind speeds at the objects in km/s
distance = au_to_km([0.9583])  # distance to the objects in km
lon = [232.716]  # carrington longitude of the objects
lat = [7.169]  # carrington latitude of the objects

# produce additional dummy field lines in a ring around the pfss footpoint and how many
vary = True
n_varies = 3


with st.sidebar.container():
    # set starting parameters from URL if available, otherwise use defaults
    def_d = datetime.datetime.strptime(st.session_state["date"][0], "%Y%m%d") if "date" in st.session_state else datetime.date.today()-datetime.timedelta(days=2)
    # def_t = datetime.datetime.strptime(st.session_state["time"][0], "%H%M") if "time" in st.session_state else datetime.time(0, 0)
    d = st.sidebar.date_input("Select date", def_d)  # , on_change=clear_url)
    # t = st.sidebar.time_input('Select time', def_t)  # , on_change=clear_url)
    # date = datetime.datetime.combine(d, t).strftime("%Y-%m-%d %H:%M:%S")
    date = d.strftime("%Y/%m/%d")

    # save query parameters to URL
    # sdate = d.strftime("%Y%m%d")
    # stime = t.strftime("%H%M")
    # set_query_params["date"] = [sdate]
    # set_query_params["time"] = [stime]
    # st.session_state["date"] = [sdate]
    # st.session_state["time"] = [stime]

with st.sidebar.container():
    st.header('Selected parameters:')
    st.write(f'carrington_rot = {carrington_rot}')
    st.write(f'date = {date}')
    st.write(f'names = {names}')
    st.write(f'sw = {sw}')
    st.write(f'distance = {distance}')
    st.write(f'lon = {lon}')
    st.write(f'lat = {lat}')
    st.write(f'vary = {vary}')
    st.write(f'n_varies = {n_varies}')

if st.button('Run PFSS for selected parameters'):
    with st.spinner('Running...'):
        title = date.replace('/', '-')  # title of the figure

        # User need not touch the function call
        hmimap = get_pfss_hmimap(filepath, email, carrington_rot, date)

        # No need to touch the function call; just run the cell
        flines = symlog_pspiral(sw=sw, distance=distance, longitude=lon, latitude=lat, hmimap=hmimap, names=names, title=title,
                                vary=vary, n_varies=n_varies, save=False)
    st.success('Done!')
