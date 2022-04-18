import streamlit as st
import streamlit.components.v1 as components
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import os
import pickle
import pydeck as pdk
from pydeck.types import String

st.set_page_config(
     page_title="Indian Housing Data",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded",
     menu_items={
         'Get Help': 'https://www.extremelycoolapp.com/help',
         'Report a bug': "https://www.extremelycoolapp.com/bug",
         'About': "# This is a header. This is an *extremely* cool app!"
     }
 )
st.markdown(
  """
  <style>
  [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {width: 120px;}
  </style>
  """,
  unsafe_allow_html=True,)
rad = st.sidebar.radio('Navigation',['Home','Search'])




if rad =='Search':
  path='app/PartA_df/'
  files=os.listdir(path)

  @st.cache(allow_output_mutation=True,suppress_st_warning=True)
  def ind(i):
    return pd.read_csv(path+i).drop(['State Code','District Code'],axis=1)


  for j,i in enumerate(files):
    nam=i.split('.')[0]
    globals()[nam]=ind(i)

  dic_={
  "Ameneties":df_assets,
  "Bathroom type":df_bath,
  "Condition of house":df_condn,
  "Couple":df_couple,
  "Material of Floor":df_floor,
  "Fuel for cooking":df_fuel,
  "Household size":df_hhold,
  "House type":df_house,
  "Kitchen":df_kitchen,
  "Lighting source":df_light,
  "Ownership status":df_owner,
  "Material of Roof":df_roof,
  "No of Rooms":df_room,
  "Toilet facillities":df_toilet,
  "Material of Wall":df_wall,
  "Waste Outlet":df_waste,
  "Water source and location":df_water
  }

  @st.cache(allow_output_mutation=True,suppress_st_warning=True)
  def fil(dic_):
    for i,j in dic_.items():
      if i=='Ameneties':
        B=j.iloc[:,:2]
      B=pd.concat([B,j.iloc[:,2:]],axis=1,join='inner')
    B['temp2']=B['District Name']+' '+B['State Name']
#     lat_long=pd.read_csv('app\scrapped_lat_long\lat_long.csv')
#     B=pd.merge(B,lat_long,how='inner',left_on='temp2',right_on='Unnamed: 0')
#     B.drop(['temp2','Unnamed: 0'],axis=1,inplace=True)
    return B
  B=fil(dic_)
#   st.write(B[:1000])
  


  
