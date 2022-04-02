from numpy import imag
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from sqlalchemy import create_engine

# UI Changes


st.set_page_config(layout="wide", page_title='Forecast')
st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 

# Loading Data
@st.cache(allow_output_mutation=True)
def load_data():
    engine = create_engine('postgresql://awsuser:Password1@redshift-cluster-1.cdryosszv1il.ap-south-1.redshift.amazonaws.com:5439/dev')
    data = pd.read_sql('SELECT * FROM demandforecast;', engine)
    data['ds']=pd.to_datetime(data['ds'])
    return data

def view_forecast(client):
    # Manipulating Data
    df = data[data['client'] == client]
    
    startdate = st.sidebar.date_input('Start Date', value=df.ds.min(), min_value=df.ds.min(), max_value=df.ds.max(), key = 1) 
    enddate   = st.sidebar.date_input('End Date',   value=df.ds.max(), min_value=df.ds.min(), max_value=df.ds.max(), key = 2)
    df = df[(df['ds'].dt.date >= startdate) & (df['ds'].dt.date <= enddate)]

    # MAPE = round(df['Statistical_APE'].mean()*100,2)
    # st.write('##### MAPE : ' + str(MAPE) + ' %' )

    # Creating Plotly charts
    fig1 = go.Figure()
    fig2 = go.Figure()

    fig1.add_trace(go.Scatter(x = df.ds, y = df['actual'], name = 'Actual'))
    fig1.add_trace(go.Scatter(x = df.ds, y = df['statistical forecast'], name = 'Statistical Forecast'))
    fig1.update_layout(title='Actual vs Forecast', yaxis_title='Shipped Units')
    st.plotly_chart(fig1, use_container_width=True)

    # fig2.add_trace(go.Scatter(x = df.date, y = df['Client Forecast'], name = 'Client Forecast'))
    # fig2.add_trace(go.Scatter(x = df.date, y = df['Statistical Forecast'], name = 'Statistical Forecast', line = dict(dash='dash')))
    # fig2.update_layout(title='Client vs Statistical Forecast', yaxis_title='Shipped Units')
    # st.plotly_chart(fig2, use_container_width=True)


# Navigation using Side bar
menu = ["Home","View Forecast"]
choice = st.sidebar.radio("Go to", menu)

if choice == "Home":
    st.subheader("Forecast Model Details and Visualization")
    st.write('Details about Forecast')

elif choice == "View Forecast":
    st.header("Forecast") 
    data = load_data() 
    client_list = data['client'].unique()
    client = st.sidebar.radio('Select Client',client_list)
    view_forecast(client)
