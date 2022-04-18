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
    lat_long=pd.read_csv('app\scrapped_lat_long\lat_long.csv')
    B=pd.merge(B,lat_long,how='inner',left_on='temp2',right_on='Unnamed: 0')
    B.drop(['temp2','Unnamed: 0'],axis=1,inplace=True)
    return B
  B=fil(dic_)
#   st.write(B[:1000])
  


  m1=st.multiselect('Facilities to choose',dic_.keys())
  if m1:
    st.markdown('<hr>',True)
  
  m_lst=[['Latitude','Longitude']]  # Put Lat, Long in 
  for i in m1:
    A=dic_[i]
    m1_A=st.multiselect(f'Choose further from {i}',A.columns[2:]) # User chooses from the column names 
    m_lst.append(m1_A)
  m_lst_f=sum(m_lst, []) # flatten the user chosen choices

  # Code for three sliders used to control number of city/states to show etc
  slider = st.slider('Number of data entries to show', min_value=0,
                    max_value=100, value= 10, key='my_slider')
  if 'k1' not in st.session_state:
    st.session_state.k1=7
  if 'k2' not in st.session_state:
    st.session_state.k2=5
  width = st.slider("Plot width", 1, 25, 3,key='k1')
  height = st.slider("Plot height", 1, 25, 1,key='k2')
  
  rad_a=st.radio('Show by:',['City','State']) # Making radio buttons
  #The state radio button
  if rad_a=='State':
    temp_=B.groupby('State Name').mean()[m_lst_f] #Groupby a user chosen value
    temp_['sum']=np.sum(temp_.drop(['Latitude','Longitude'],axis=1),axis=1).values # sum the means of the columns chosen

    if st.button("Filter") :  #Press Filter
      st.markdown('<hr>',True)   #Horizontal line
      fig1, ax = plt.subplots(figsize=(width, height))

      temp_=temp_.sort_values('sum',ascending=False)[:slider]     # Sort values according to the sum of all column values
      temp_.drop(['Latitude','Longitude','sum'],axis=1).plot(kind='barh',colormap='Set1',  # Plot after dropping lat, long,sum
                                    stacked=True,ax=ax)

      plt.legend(bbox_to_anchor=(0.5, -0.25, 0.3, 0.2)) # Legend below the graph

      st.pyplot(fig1)

  if rad_a=='City':
    temp_=B.groupby('District Name').mean()[m_lst_f]
    temp_['sum']=np.sum(temp_.drop(['Latitude','Longitude'],axis=1),axis=1).values
    if st.button("Filter") :
      st.markdown('<hr>',True)
      fig2, ax = plt.subplots(figsize=(width, height))
      temp_=temp_.sort_values('sum',ascending=False)
      temp_.drop(['Latitude','Longitude','sum'],axis=1)[:slider].plot(kind='barh',colormap='Set1',
                                    stacked=True,ax=ax)
      plt.legend(bbox_to_anchor=(0.5, -0.25, 0.3, 0.2))

      st.subheader('Map')
      x='sum'
      layer = pdk.Layer(
          'ColumnLayer', #Layer to use
          temp_,   # Dat to load
          get_position=['Longitude', 'Latitude'],   # Columns with Lat Long
          radius=5000,    #Radius upto which to aggregate values
          auto_highlight=True,
          get_elevation=x,  # Column which decides the elevation
          get_fill_color=[f'{x}*10',f'{x}*5',f'{x}*1'],  # Color of the columns in [R,G,B]
          elevation_scale=1500,  # Number by which elevation is scaled
          pickable=True,
          elevation_range=[0, 3000],
          extruded=True,  # whether or not columns should be raised
          )
      layer1 = pdk.Layer(
          'HeatmapLayer',    
          temp_.sort_values('sum',ascending=False),
          get_position=['Longitude', 'Latitude'],
          getWeight=x
          )

      # Set the viewport location
      view_state = pdk.ViewState(
          longitude=80, 
          latitude=18,
          zoom=4,
          min_zoom=3.5,
          max_zoom=15,
          pitch=40.5,
          bearing=0)  

      st.pydeck_chart(pdk.Deck(layers=[layer,layer1], initial_view_state=view_state,map_style='light'))
      
      st.markdown('<hr>',True)
      st.subheader('Plot')

      st.pyplot(fig2)
