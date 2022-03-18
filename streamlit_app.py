import datetime
import os
import streamlit as st
from pfss_notebook_lib import get_pfss_hmimap, symlog_pspiral

# replace with some sunpy function!!!
from pfss_notebook_lib import au_to_km

filepath = os.getcwd()  # "/home/chospa/solar_mach/pfss/"
email = "jan.gieseler@utu.fi"

# names = ['Stereo A']  # names of the object(s) (optional)
# sw = [376]  # solar wind speeds at the objects in km/s
# distance = au_to_km([0.9583])  # distance to the objects in km
# lon = [232.716]  # carrington longitude of the objects
# lat = [7.169]  # carrington latitude of the objects

with st.sidebar.container():
    # set starting parameters from URL if available, otherwise use defaults
    def_d = datetime.datetime.strptime(st.session_state["date"][0], "%Y%m%d") if "date" in st.session_state else datetime.date.today()-datetime.timedelta(days=2)
    # def_t = datetime.datetime.strptime(st.session_state["time"][0], "%H%M") if "time" in st.session_state else datetime.time(0, 0)
    d = st.sidebar.date_input("Date", def_d)  # , on_change=clear_url)
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

    carrington_rot = st.number_input('Carrington rotation number', value=2250)

st.sidebar.subheader('Define SC & corresponding parameters')
with st.sidebar.container():
    body_list = \
        st.sidebar.text_area('Bodies/spacecraft',
                            'STEREO A, Solar Orbiter',
                            height=50)
    vsw_list = \
        st.sidebar.text_area('Solar wind speed per body/SC (mind the order!)', '400, 400',
                            height=50)
    distance_list = \
        st.sidebar.text_area('Distance in AU per body/SC (mind the order!)', '0.9583, 0.76',
                            height=50) 
    long_list = \
        st.sidebar.text_area('Longitude per body/SC (mind the order!)', '232.716, 2',
                            height=50)  
    lat_list = \
        st.sidebar.text_area('Latitude per body/SC (mind the order!)', '7.169, 0',
                            height=50)                           
    body_list = body_list.split(',')
    vsw_list = vsw_list.split(',')
    distance_list = distance_list.split(',')
    long_list = long_list.split(',')
    lat_list = lat_list.split(',')
    body_list = [body_list[i].strip() for i in range(len(body_list))]

    wrong_value = False
    try: 
        vsw_list = [int(vsw_list[i].strip()) for i in range(len(vsw_list))]
        distance_list = [float(distance_list[i].strip()) for i in range(len(distance_list))]
        long_list = [float(long_list[i].strip()) for i in range(len(long_list))]
        lat_list = [float(lat_list[i].strip()) for i in range(len(lat_list))]
    except ValueError:
        wrong_value = True

    names = body_list
    sw = vsw_list
    distance = distance_list
    lon = long_list
    lat = lat_list
    distance = au_to_km(distance)

with st.sidebar.container():
    with st.expander("additional field lines", expanded=True):
        vary = st.checkbox('vary', help='produce additional dummy field lines in a ring around the pfss footpoint and how many', value=True)
        n_varies = st.number_input('n_varies', value=3)

if wrong_value:
    st.error('ERROR: There is something wrong in the input parameters! Maybe some missing or wrong comma?')
    st.stop()

if st.button('Run PFSS for selected parameters'):
    with st.spinner('Running...'):
        title = date.replace('/', '-')  # title of the figure

        # User need not touch the function call
        hmimap = get_pfss_hmimap(filepath, email, carrington_rot, date)

        # No need to touch the function call; just run the cell
        flines = symlog_pspiral(sw=sw, distance=distance, longitude=lon, latitude=lat, hmimap=hmimap, names=names, title=title,
                                vary=vary, n_varies=n_varies, save=False)

with st.expander("Parameters", expanded=True):
    st.write(f'carrington_rot = {carrington_rot}')
    st.write(f'date = {date}')
    st.write(f'names = {names}')
    st.write(f'lon = {lon}')
    st.write(f'lat = {lat}')
    st.write(f'sw = {sw}')
    st.write(f'distance = {distance}')
