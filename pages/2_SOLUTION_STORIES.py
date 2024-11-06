import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
# from wordcloud import WordCloud, STOPWORDS
from streamlit_folium import st_folium
import folium
import plotly.graph_objects as go
# import squarify
import seaborn as sns
import plotly.express as px
import sys
import re
import openpyxl
from openpyxl.styles import Border, Side
from io import BytesIO
from numerize.numerize import numerize
import requests
#News
from datetime import datetime
import pydeck as pdk


def structure_and_format():
    im = Image.open("R2R_RGB_PINK_BLUE.png")
    st.set_page_config(page_title="RtR DATA EXPLORER", layout="wide", initial_sidebar_state="expanded")
    st.logo(im, size="large")
    
    css_path = "style.css"

    with open(css_path) as css:
        st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
    
    ##
    ##Hide footer streamlit
    ##
    hide_streamlit_style = """
                <style>
                #MainMenu {visibility: hidden;}
                footer {visibility: hidden;}
                </style>
                """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    ## Hide index when showing a table. CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    ##
    ## Inject CSS with Markdown
    ##
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

structure_and_format()


##Uploading Data

@st.cache_data
def solution_stories():
    # file_path_solution_stories = "solution_stories_rtr_231201.csv"
    file_path_solution_stories = "solution_stories_rtr_241105.csv"
    df_solution_stories = pd.read_csv(file_path_solution_stories, sep=';') 
    return df_solution_stories
df_solution_stories = solution_stories()



### CSV Country GeoInfo
@st.cache_data
def geo_info():
    file_path_country_geo_info = "countries_geoinfo.csv"
    df_country = pd.read_csv(file_path_country_geo_info,sep=';')
    return df_country
df_country = geo_info()



## Data Cleaning


df_solution_stories['Onclick'] = df_solution_stories['Cities'].astype(str) + ", " + df_solution_stories['All_Countries'].astype(str)
# df_solution_stories['Onclick']

def convert_date(date_string):
    try:
        # Parse the date string in the given format
        date_obj = datetime.strptime(date_string, '%B %d, %Y')
        # Convert the date object to a standard format, e.g., "YYYY-MM-DD"
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        # Return None or some default value if the parsing fails
        return None

# # Apply the conversion function to the 'Date' column
# df_solution_stories['Date'] = df_solution_stories['Date'].apply(convert_date)



#Treatment of countries. Treat as a funcion in the future. 
# Total Number of Countries
#Creating a list of all country names 
# Split each row by the delimiter and flatten the resulting list
all_countries = [country.strip() for sublist in df_solution_stories['All_Countries'].str.split(';') for country in sublist if country.strip()]
# Get unique country names using set
unique_countries = list(set(all_countries))
# Create a new DataFrame
df_unique_countries = pd.DataFrame(unique_countries, columns=['Country'])
# Display the result
# st.write(df_unique_countries)

#creating a list of countries depending of its continent
Africa = df_country[df_country['continent']== 'Africa']
Asia = df_country[df_country['continent']== 'Asia']
Europe = df_country[df_country['continent']== 'Europe']
LATAMC = df_country[df_country['continent']== 'Latin America and the Caribbean']
Northern_America = df_country[df_country['continent']== 'Northern America']
Oceania = df_country[df_country['continent']== 'Oceania']

Africa_list = Africa['Country'].tolist()
Asia_list = Asia['Country'].tolist()
Europe_list = Europe['Country'].tolist()
LATAMC_list = LATAMC['Country'].tolist()
Northern_America_list = Northern_America['Country'].tolist()
Oceania_list = Oceania['Country'].tolist()

df_solution_stories['Africa'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Africa_list for country in x])), 'Africa', '')
df_solution_stories['Asia'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Asia_list for country in x])), 'Asia', '')
df_solution_stories['Europe'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Europe_list for country in x])), 'Europe', '')
df_solution_stories['LATAMC'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in LATAMC_list for country in x])), 'Latin America and the Caribbean', '')
df_solution_stories['Northern_America'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
df_solution_stories['Oceania'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Oceania_list for country in x])), 'Oceania', '')

continents_pledge_list = ['Africa','Asia','Europe','LATAMC','Northern_America','Oceania']
# st.write(df_solution_stories[continents_pledge_list])

#creating a list of countries depending of its region_wb
South_Asia = df_country[df_country['region_wb']== 'South Asia']
Europe_Central_Asia = df_country[df_country['region_wb']== 'Europe & Central Asia']
Middle_East_North_Africa = df_country[df_country['region_wb']== 'Middle East & North Africa']
Sub_Saharan_Africa = df_country[df_country['region_wb']== 'Sub-Saharan Africa']
Latin_America_Caribbean = df_country[df_country['region_wb']== 'Latin America & Caribbean']
East_Asia_Pacific = df_country[df_country['region_wb']== 'East Asia & Pacific']
North_America = df_country[df_country['region_wb']== 'North America']

South_Asia_list = South_Asia['Country'].tolist()
Europe_Central_Asia_list = Europe_Central_Asia['Country'].tolist()
Middle_East_North_Africa_list = Middle_East_North_Africa['Country'].tolist()
Sub_Saharan_Africa_list = Sub_Saharan_Africa['Country'].tolist()
Latin_America_Caribbean_list = Latin_America_Caribbean['Country'].tolist()
East_Asia_Pacific_list = East_Asia_Pacific['Country'].tolist()
North_America_list = North_America['Country'].tolist()

df_solution_stories['South_Asia'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in South_Asia_list for country in x])), 'South Asia', '')
df_solution_stories['Europe_Central_Asia'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Europe_Central_Asia_list for country in x])), 'Europe & Central Asia', '')
df_solution_stories['Middle_East_North_Africa'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Middle_East_North_Africa_list for country in x])), 'Middle East & North Africa', '')
df_solution_stories['Sub_Saharan_Africa'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Sub_Saharan_Africa_list for country in x])), 'Sub-Saharan Africa', '')
df_solution_stories['Latin_America_Caribbean'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Latin_America_Caribbean_list for country in x])), 'Latin America & Caribbean', '')
df_solution_stories['East_Asia_Pacific'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in East_Asia_Pacific_list for country in x])), 'East Asia & Pacific', '')
df_solution_stories['North_America'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in North_America_list for country in x])), 'North America', '')

regions_pledge_list = ['South_Asia','Europe_Central_Asia','Middle_East_North_Africa','Sub_Saharan_Africa','Latin_America_Caribbean','East_Asia_Pacific','North_America']
# st.write(df_solution_stories[regions_pledge_list])

Southern_Asia= df_country[df_country['subregion']== 'Southern Asia']
Southern_Europe= df_country[df_country['subregion']== 'Southern Europe']
Northern_Africa= df_country[df_country['subregion']== 'Northern Africa']
Middle_Africa= df_country[df_country['subregion']== 'Middle Africa']
Caribbean= df_country[df_country['subregion']== 'Caribbean']
South_America= df_country[df_country['subregion']== 'South America']
Western_Asia= df_country[df_country['subregion']== 'Western Asia']
Australia_and_New_Zealand= df_country[df_country['subregion']== 'Australia and New Zealand']
Western_Europe= df_country[df_country['subregion']== 'Western Europe']
Eastern_Europe= df_country[df_country['subregion']== 'Eastern Europe']
Central_America= df_country[df_country['subregion']== 'Central America']
Western_Africa= df_country[df_country['subregion']== 'Western Africa']
Southern_Africa= df_country[df_country['subregion']== 'Southern Africa']
Eastern_Africa= df_country[df_country['subregion']== 'Eastern Africa']
South_Eastern_Asia= df_country[df_country['subregion']== 'South-Eastern Asia']
Northern_America= df_country[df_country['subregion']== 'Northern America']
Eastern_Asia= df_country[df_country['subregion']== 'Eastern Asia']
Northern_Europe= df_country[df_country['subregion']== 'Northern Europe']
Central_Asia= df_country[df_country['subregion']== 'Central Asia']
Melanesia= df_country[df_country['subregion']== 'Melanesia']
Polynesia= df_country[df_country['subregion']== 'Polynesia']
Micronesia= df_country[df_country['subregion']== 'Micronesia']

Southern_Asia_list = Southern_Asia['Country'].tolist()
Southern_Europe_list = Southern_Europe['Country'].tolist()
Northern_Africa_list = Northern_Africa['Country'].tolist()
Middle_Africa_list = Middle_Africa['Country'].tolist()
Caribbean_list = Caribbean['Country'].tolist()
South_America_list = South_America['Country'].tolist()
Western_Asia_list = Western_Asia['Country'].tolist()
Australia_and_New_Zealand_list = Australia_and_New_Zealand['Country'].tolist()
Western_Europe_list = Western_Europe['Country'].tolist()
Eastern_Europe_list = Eastern_Europe['Country'].tolist()
Central_America_list = Central_America['Country'].tolist()
Western_Africa_list = Western_Africa['Country'].tolist()
Southern_Africa_list = Southern_Africa['Country'].tolist()
Eastern_Africa_list = Eastern_Africa['Country'].tolist()
South_Eastern_Asia_list = South_Eastern_Asia['Country'].tolist()
Northern_America_list = Northern_America['Country'].tolist()
Eastern_Asia_list = Eastern_Asia['Country'].tolist()
Northern_Europe_list = Northern_Europe['Country'].tolist()
Central_Asia_list = Central_Asia['Country'].tolist()
Melanesia_list = Melanesia['Country'].tolist()
Polynesia_list = Polynesia['Country'].tolist()
Micronesia_list = Micronesia['Country'].tolist()

df_solution_stories['Southern_Asia'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Asia_list for country in x])), 'Southern Asia', '')
df_solution_stories['Southern_Europe'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Europe_list for country in x])), 'Southern Europe', '')
df_solution_stories['Northern_Africa'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_Africa_list for country in x])), 'Northern Africa', '')
df_solution_stories['Middle_Africa'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Middle_Africa_list for country in x])), 'Middle Africa', '')
df_solution_stories['Caribbean'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Caribbean_list for country in x])), 'Caribbean', '')
df_solution_stories['South_America'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in South_America_list for country in x])), 'South America', '')
df_solution_stories['Western_Asia'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Asia_list for country in x])), 'Western Asia', '')
df_solution_stories['Australia_and_New_Zealand'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Australia_and_New_Zealand_list for country in x])), 'Australia and New Zealand', '')
df_solution_stories['Western_Europe'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Europe_list for country in x])), 'Western Europe', '')
df_solution_stories['Eastern_Europe'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Europe_list for country in x])), 'Eastern Europe', '')
df_solution_stories['Central_America'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Central_America_list for country in x])), 'Central America', '')
df_solution_stories['Western_Africa'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Africa_list for country in x])), 'Western Africa', '')
df_solution_stories['Southern_Africa'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Africa_list for country in x])), 'Southern Africa', '')
df_solution_stories['Eastern_Africa'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Africa_list for country in x])), 'Eastern Africa', '')
df_solution_stories['South_Eastern_Asia'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in South_Eastern_Asia_list for country in x])), 'South-Eastern Asia', '')
df_solution_stories['Northern_America'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
df_solution_stories['Eastern_Asia'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Asia_list for country in x])), 'Eastern Asia', '')
df_solution_stories['Northern_Europe'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_Europe_list for country in x])), 'Northern Europe', '')
df_solution_stories['Central_Asia'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Central_Asia_list for country in x])), 'Central Asia', '')
df_solution_stories['Melanesia'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Melanesia_list for country in x])), 'Melanesia', '')
df_solution_stories['Polynesia'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Polynesia_list for country in x])), 'Polynesia', '')
df_solution_stories['Micronesia'] = np.where(df_solution_stories['All_Countries'].str.split(';').apply(lambda x: any([country.strip() in Micronesia_list for country in x])), 'Micronesia', '')

subregions_pledge_list = ['Southern_Asia','Southern_Europe','Northern_Africa','Middle_Africa','Caribbean','South_America',
                          'Western_Asia','Australia_and_New_Zealand','Western_Europe','Eastern_Europe','Central_America',
                          'Western_Africa','Southern_Africa','Eastern_Africa','South_Eastern_Asia','Northern_America','Eastern_Asia',
                          'Northern_Europe','Central_Asia','Melanesia','Polynesia','Micronesia',]

# st.write(df_solution_stories[subregions_pledge_list])

# #Concatenating columns
df_solution_stories['country_continents_all'] = df_solution_stories[continents_pledge_list].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_solution_stories['country_region_all'] = df_solution_stories[regions_pledge_list].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
df_solution_stories['country_subregion_all'] = df_solution_stories[subregions_pledge_list].apply(lambda x:'; '.join(x.dropna().astype(str)),axis=1)
# st.write(df_solution_stories[['country_continents_all','country_region_all','country_subregion_all']])



##Welcome 
col1,col2 = st.columns([1,1])
col1.markdown('# SOLUTION STORIES')
col2.markdown("")
col2.markdown("")
col2.markdown("##### *RtR Partners sharing experiencies and solutions*")

st.markdown('The Solution Stories selection tool is designed to provide users with access to a comprehensive collection of case studies and narratives focused on climate resilience solutions. These stories highlight successful strategies and initiatives aligned with the Sharm El Sheikh Adaptation Agenda (SAA) Priority Systems. By filtering the available solution stories based on specific criteria users can tailor their search to find relevant examples of adaptation and resilience in response to climate change challenges.')


#Making a data set for selection. 
df_selection_list = ['InitName','SAA Priority Systems','All_Countries','country_continents_all', 'country_region_all', 'country_subregion_all']
df_selection = df_solution_stories[df_selection_list]
# df_selection


#Making selector
cats_defs = [
        ['SAA Priority Systems',['Food and Agriculture','Health','Human Settlements','Coastal and Oceans','Infrastructure','Water and Nature','Planning and Policy: Cross-cutting','Finance: Cross-cutting','']],
        ['All_Countries',['Afghanistan','Albania','Algeria','Andorra','Angola','Antigua and Barbuda','Argentina','Armenia','Australia','Austria','Azerbaijan','Bahamas','Bahrain','Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bhutan','Bolivia, Plurinational State of','Bosnia and Herzegovina','Botswana','Brazil','Brunei Darussalam','Bulgaria','Burkina Faso','Burundi','Cambodia','Cameroon','Canada','Cape Verde','Central African Republic','Chad','Chile','China','Colombia','Comoros','Congo','Congo, the Democratic Republic of the','Costa Rica',"Côte d'Ivoire",'Croatia','Cuba','Cyprus','Czech Republic','Denmark','Djibouti','Dominica','Dominican Republic','Ecuador','Egypt','El Salvador','Equatorial Guinea','Eritrea','Estonia','Ethiopia','Finland','France','Gabon','Gambia','Georgia','Germany','Ghana','Greece','Grenada','Guatemala','Guinea','Guinea-Bissau','Guyana','Haiti','Honduras','Hungary','Iceland','India','Indonesia','Iran, Islamic Republic of','Iraq','Ireland','Israel','Italy','Jamaica','Japan','Jordan','Kazakhstan','Kenya','Korea, Republic of','Kuwait','Kyrgyzstan',"Lao People's Democratic Republic",'Latvia','Lebanon','Lesotho','Liberia','Libyan Arab Jamahiriya','Liechtenstein','Lithuania','Luxembourg','Macedonia, the former Yugoslav Republic of','Madagascar','Malawi','Malaysia','Mali','Malta','Mauritania','Mauritius','Mexico','Micronesia, Federated States of','Moldova, Republic of','Mongolia','Montenegro','Morocco','Mozambique','Myanmar','Namibia','Nepal','Netherlands','New Zealand','Nicaragua','Niger','Nigeria','North Korea','Norway','Oman','Pakistan','Palestinian Territory, Occupied','Panama','Papua New Guinea','Paraguay','Peru','Philippines','Poland','Portugal','Puerto Rico','Qatar','Romania','Russian Federation','Rwanda','Saint Vincent and the Grenadines','Samoa','Sao Tome and Principe','Saudi Arabia','Senegal','Serbia','Sierra Leone','Singapore','Slovakia','Slovenia','Solomon Islands','Somalia','Somaliland','South Africa','South Sudan','Spain','Sri Lanka','Sudan','Suriname','Swaziland','Sweden','Switzerland','Syrian Arab Republic','Taiwan, Province of China','Tajikistan','Tanzania, United Republic of','Thailand','Timor-Leste','Togo','Tonga','Trinidad and Tobago','Tunisia','Turkey','Turkmenistan','Uganda','Ukraine','United Arab Emirates','United Kingdom','United States of America','Uruguay','Uzbekistan','Vanuatu','Venezuela, Bolivarian Republic of','Viet Nam','Western Sahara','Yemen','Zambia','Zimbabwe','']],
        ['country_region_all',['South Asia', 'Europe & Central Asia', 'Middle East & North Africa', 'Sub-Saharan Africa', 'Latin America & Caribbean', 'East Asia & Pacific', 'North America','']],
       ]  

cats = [cats_defs[0][0],                            cats_defs[1][0],                         cats_defs[2][0],                     ]  #list of question categories
defs = [cats_defs[0][1],                            cats_defs[1][1],                         cats_defs[2][1],                     ]  #list of possible answers
poss = [df_selection['SAA Priority Systems'].tolist(),df_selection['All_Countries'].tolist(),df_selection['country_region_all'].tolist()]


cats = [cats_defs[0][0],                            cats_defs[1][0],                         cats_defs[2][0],                       ]  #list of question categories
defs = [cats_defs[0][1],                            cats_defs[1][1],                         cats_defs[2][1],                       ]  #list of possible answers
poss = [df_selection['SAA Priority Systems'].tolist(),df_selection['All_Countries'].tolist(),df_selection['country_region_all'].tolist()]




saa_options = ['Food and Agriculture','Health','Human Settlements','Coastal and Oceans','Infrastructure','Water and Nature','Planning and Policy: Cross-cutting','Finance: Cross-cutting']
All_Countries_options =['Afghanistan','Albania','Algeria','Andorra','Angola','Antigua and Barbuda','Argentina','Armenia','Australia','Austria','Azerbaijan','Bahamas','Bahrain','Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bhutan','Bolivia, Plurinational State of','Bosnia and Herzegovina','Botswana','Brazil','Brunei Darussalam','Bulgaria','Burkina Faso','Burundi','Cambodia','Cameroon','Canada','Cape Verde','Central African Republic','Chad','Chile','China','Colombia','Comoros','Congo','Congo, the Democratic Republic of the','Costa Rica',"Côte d'Ivoire",'Croatia','Cuba','Cyprus','Czech Republic','Denmark','Djibouti','Dominica','Dominican Republic','Ecuador','Egypt','El Salvador','Equatorial Guinea','Eritrea','Estonia','Ethiopia','Finland','France','Gabon','Gambia','Georgia','Germany','Ghana','Greece','Grenada','Guatemala','Guinea','Guinea-Bissau','Guyana','Haiti','Honduras','Hungary','Iceland','India','Indonesia','Iran, Islamic Republic of','Iraq','Ireland','Israel','Italy','Jamaica','Japan','Jordan','Kazakhstan','Kenya','Korea, Republic of','Kuwait','Kyrgyzstan',"Lao People's Democratic Republic",'Latvia','Lebanon','Lesotho','Liberia','Libyan Arab Jamahiriya','Liechtenstein','Lithuania','Luxembourg','Macedonia, the former Yugoslav Republic of','Madagascar','Malawi','Malaysia','Mali','Malta','Mauritania','Mauritius','Mexico','Micronesia, Federated States of','Moldova, Republic of','Mongolia','Montenegro','Morocco','Mozambique','Myanmar','Namibia','Nepal','Netherlands','New Zealand','Nicaragua','Niger','Nigeria','North Korea','Norway','Oman','Pakistan','Palestinian Territory, Occupied','Panama','Papua New Guinea','Paraguay','Peru','Philippines','Poland','Portugal','Puerto Rico','Qatar','Romania','Russian Federation','Rwanda','Saint Vincent and the Grenadines','Samoa','Sao Tome and Principe','Saudi Arabia','Senegal','Serbia','Sierra Leone','Singapore','Slovakia','Slovenia','Solomon Islands','Somalia','Somaliland','South Africa','South Sudan','Spain','Sri Lanka','Sudan','Suriname','Swaziland','Sweden','Switzerland','Syrian Arab Republic','Taiwan, Province of China','Tajikistan','Tanzania, United Republic of','Thailand','Timor-Leste','Togo','Tonga','Trinidad and Tobago','Tunisia','Turkey','Turkmenistan','Uganda','Ukraine','United Arab Emirates','United Kingdom','United States of America','Uruguay','Uzbekistan','Vanuatu','Venezuela, Bolivarian Republic of','Viet Nam','Western Sahara','Yemen','Zambia','Zimbabwe']
# country_continents_all_options =['Africa', 'Asia', 'Europe', 'Latin America and the Caribbean', 'Northern America', 'Oceania']
country_region_all_options = ['South Asia', 'Europe & Central Asia', 'Middle East & North Africa', 'Sub-Saharan Africa', 'Latin America & Caribbean', 'East Asia & Pacific', 'North America']
# country_subregion_all_options = ['Southern Asia','Southern Europe','Northern Africa','Middle Africa','Caribbean','South America','Western Asia','Australia and New Zealand','Western Europe','Eastern Europe','Central America','Western Africa','Southern Africa','Eastern Africa','South-Eastern Asia','Northern America','Eastern Asia','Northern Europe','Central Asia','Melanesia','Polynesia','Micronesia',]


# with st.form("my_form",clear_on_submit=True):
#     col1, col2, col3 = st.columns(3)
#     with col1: 
#         saa_selection = st.multiselect("SAA Priority Systems",      saa_options)
        
#     with col2:
#         country_selection = st.multiselect("Country",      All_Countries_options)
#         # subregion_selection = st.multiselect("Sub Region",      country_subregion_all_options)
        
#     with col3:
#         region_selection = st.multiselect("Region",      country_region_all_options)
#         # continent_selection = st.multiselect("Continent",      country_continents_all_options)
#         submitted = st.form_submit_button("SEARCH")
# if submitted:
#     st.markdown("")

# with st.sidebar:
st.write('#### FILTER SOLUTION STORIES')
with st.form("my_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    saa_selection = col1.multiselect("**SAA Priority Systems**", saa_options)
    country_selection = col2.multiselect("**Country**", All_Countries_options)
    region_selection = col3.multiselect("**Region**", country_region_all_options)
    submitted = st.form_submit_button("SEARCH")
        
if submitted:
    st.markdown("Your search has been submitted.")


# selection = [saa_selection,country_selection,continent_selection,region_selection,subregion_selection]
selection = [saa_selection,country_selection,region_selection]


# selection = [['LGBTQIA+ people', 'Elderly'], [], []]

selection_all = [[
    "Food and Agriculture",
    "Health",
    "Human Settlements",
    "Coastal and Oceans",
    "Infrastructure",
    "Water and Nature",
    "Planning and Policy: Cross-cutting",
    "Finance: Cross-cutting",
    ""
  ],
  [
    "Afghanistan",
    "Albania",
    "Algeria",
    "Andorra",
    "Angola",
    "Antigua and Barbuda",
    "Argentina",
    "Armenia",
    "Australia",
    "Austria",
    "Azerbaijan",
    "Bahamas",
    "Bahrain",
    "Bangladesh",
    "Barbados",
    "Belarus",
    "Belgium",
    "Belize",
    "Benin",
    "Bhutan",
    "Bolivia, Plurinational State of",
    "Bosnia and Herzegovina",
    "Botswana",
    "Brazil",
    "Brunei Darussalam",
    "Bulgaria",
    "Burkina Faso",
    "Burundi",
    "Cambodia",
    "Cameroon",
    "Canada",
    "Cape Verde",
    "Central African Republic",
    "Chad",
    "Chile",
    "China",
    "Colombia",
    "Comoros",
    "Congo",
    "Congo, the Democratic Republic of the",
    "Costa Rica",
    "Côte d'Ivoire",
    "Croatia",
    "Cuba",
    "Cyprus",
    "Czech Republic",
    "Denmark",
    "Djibouti",
    "Dominica",
    "Dominican Republic",
    "Ecuador",
    "Egypt",
    "El Salvador",
    "Equatorial Guinea",
    "Eritrea",
    "Estonia",
    "Ethiopia",
    "Finland",
    "France",
    "Gabon",
    "Gambia",
    "Georgia",
    "Germany",
    "Ghana",
    "Greece",
    "Grenada",
    "Guatemala",
    "Guinea",
    "Guinea-Bissau",
    "Guyana",
    "Haiti",
    "Honduras",
    "Hungary",
    "Iceland",
    "India",
    "Indonesia",
    "Iran, Islamic Republic of",
    "Iraq",
    "Ireland",
    "Israel",
    "Italy",
    "Jamaica",
    "Japan",
    "Jordan",
    "Kazakhstan",
    "Kenya",
    "Korea, Republic of",
    "Kuwait",
    "Kyrgyzstan",
    "Lao People's Democratic Republic",
    "Latvia",
    "Lebanon",
    "Lesotho",
    "Liberia",
    "Libyan Arab Jamahiriya",
    "Liechtenstein",
    "Lithuania",
    "Luxembourg",
    "Macedonia, the former Yugoslav Republic of",
    "Madagascar",
    "Malawi",
    "Malaysia",
    "Mali",
    "Malta",
    "Mauritania",
    "Mauritius",
    "Mexico",
    "Micronesia, Federated States of",
    "Moldova, Republic of",
    "Mongolia",
    "Montenegro",
    "Morocco",
    "Mozambique",
    "Myanmar",
    "Namibia",
    "Nepal",
    "Netherlands",
    "New Zealand",
    "Nicaragua",
    "Niger",
    "Nigeria",
    "North Korea",
    "Norway",
    "Oman",
    "Pakistan",
    "Palestinian Territory, Occupied",
    "Panama",
    "Papua New Guinea",
    "Paraguay",
    "Peru",
    "Philippines",
    "Poland",
    "Portugal",
    "Puerto Rico",
    "Qatar",
    "Romania",
    "Russian Federation",
    "Rwanda",
    "Saint Vincent and the Grenadines",
    "Samoa",
    "Sao Tome and Principe",
    "Saudi Arabia",
    "Senegal",
    "Serbia",
    "Sierra Leone",
    "Singapore",
    "Slovakia",
    "Slovenia",
    "Solomon Islands",
    "Somalia",
    "Somaliland",
    "South Africa",
    "South Sudan",
    "Spain",
    "Sri Lanka",
    "Sudan",
    "Suriname",
    "Swaziland",
    "Sweden",
    "Switzerland",
    "Syrian Arab Republic",
    "Taiwan, Province of China",
    "Tajikistan",
    "Tanzania, United Republic of",
    "Thailand",
    "Timor-Leste",
    "Togo",
    "Tonga",
    "Trinidad and Tobago",
    "Tunisia",
    "Turkey",
    "Turkmenistan",
    "Uganda",
    "Ukraine",
    "United Arab Emirates",
    "United Kingdom",
    "United States of America",
    "Uruguay",
    "Uzbekistan",
    "Vanuatu",
    "Venezuela, Bolivarian Republic of",
    "Viet Nam",
    "Western Sahara",
    "Yemen",
    "Zambia",
    "Zimbabwe",
    ""
  ],
  [
    "South Asia",
    "Europe & Central Asia",
    "Middle East & North Africa",
    "Sub-Saharan Africa",
    "Latin America & Caribbean",
    "East Asia & Pacific",
    "North America",
    ""
  ],
]
#__________________________________________________________________________________________________________________________________________________________________
# END: mULTISELECTOR. ORGANIZATION OF THE DATA
#__________________________________________________________________________________________________________________________________________________________________

#__________________________________________________________________________________________________________________________________________________________________
## SEARCH ALGORITM
#__________________________________________________________________________________________________________________________________________________________________

##Showing results 
if all(not s for s in selection):
    st.markdown('#### All solution stories are available for selection and exploration.')
    st.sidebar.markdown('All solution stories are available for selection and exploration.')
#     st.markdown("""
# **Click on a pin for a popup with key details on the solution stories**.
# """, unsafe_allow_html=True)


else:
    st.markdown('<span style="color:#FF37D5; font-weight:bold">YOU SELECTED:</span>', unsafe_allow_html=True)
    selected_options = []
    for s in selection:
        if s:
            selected_options.extend(s)
    selected_options_str = ', '.join(selected_options)
    st.write(selected_options_str)
    st.sidebar.markdown("**You Selected:** "+ selected_options_str)

# FIltering
df_selection_len = len(df_selection.index)


# len(df.index)  
i=0
while i < len(selection):
    if len(selection[i])==0:
        selection[i]=defs[i]
    i=i+1

def index_selection_results(sel, col):
    results_index = []
    for i, col_value in enumerate(col):    # Iterate over the DataFrame column
        for elem in sel:                   # Iterate over the selected elements
            if elem in col_value:          # Check if the selected element is in the DataFrame column value
                results_index.append(i)    # Add the index to the results list
    return list(set(results_index))        # Return unique indices

def common_member(a, b):                   #used to intersect any two lists
    result = [i for i in a if i in b]
    return result

final_list = list(range(0,df_selection_len+1))
j = 0
while j < len(selection):
        temp_list  = list(set(index_selection_results(selection[j],poss[j]))) #avoidung index duplications
        final_list = list(set(common_member(temp_list,final_list)))
        j = j+1

# df_filtered = df_solution_stories.iloc[final_list].reset_index().sort_values(by = 'InitName')
df_filtered = df_solution_stories.iloc[final_list].reset_index(drop=True).sort_values(by='InitName')

# df_filtered.set_index("Master ID", inplace = True)
#__________________________________________________________________________________________________________________________________________________________________
## END SEARCH ALGORITM
#__________________________________________________________________________________________________________________________________________________________________




#__________________________________________________________________________________________________________________________________________________________________
# RESULT FROM THE SELECTION
#__________________________________________________________________________________________________________________________________________________________________

count_solutions = str(df_filtered['Title'].count())
# df_solution_stories['Description']
total_counts_solutions = str(df_solution_stories['Title'].count())
# Create a markdown list by appending each item with a preceding '* '

#Title Only
list_solutions_link = df_filtered.Link.unique()
list_solutions_title = df_filtered.Title.unique()
markdown_list = '\n'.join([f'* [{title}]({link})' for title, link in zip(df_filtered['Title'], df_filtered['Link'])])
result = f"### There are {count_solutions} RtR Solution Stories that meet your selection criteria:\n{markdown_list}"


# from selection_all import selection_all
if count_solutions == total_counts_solutions: 
    pass
else:
    st.markdown('')
    st.write(result)
    st.sidebar.markdown(result)
#     st.markdown("""
# ##### Discover More with Detailed Popups

# Click on a pin for a popup with key details on the solution stories.
# """, unsafe_allow_html=True)


st.markdown("Explore Solution Stories")
st.write(df_filtered)

st.write("WORLDMAP WITH SOLUTION STORIES PENDING")

# ## CHARTS

# ## Chart
# df = df_solution_stories.dropna(subset=['lat', 'lon'])


# world_map_solution_stories = folium.Map(location=[0, 0], zoom_start=2, tiles="cartodbpositron")

# # Loop through the data and add markers.
# for index, row in df.iterrows():
#     # Check and prepare 'Video Description' link if available
#     # video_description_link = f'<a href="{row["Video_Description"]}" target="_blank"><b>Video Description</b></a><br>' if row['Video_Description'] != "No Available" else ""

#     # Check and prepare 'Beneficiaries / Impact:' if available
#     # beneficiaries_impact = f'<b>Beneficiaries / Impact:</b> {row["Beneficiaries / Impact:"]}<br>' if row['Beneficiaries / Impact:'] != "No Available" else ""

#     # Create popup HTML including only available information
#     # popup_html = f"""
#     # <div>
#     #     <b style="color:#FF37D5;">RtR SOLUTION STORY</b><br>
#     #     <b>Title:</b> {row['Title']}<b>.</b><br>
#     #     <b>Date:</b> {row['Date']}<br>
#     #     <b>Partner:</b> {row['InitName']}<br>
#     #     <b>Location:</b> {row['Onclick']}<br> 
#     #     <b>Implementers:</b> {row['Implementers']}<br>
#     #     <b>SAA Priority Systems:</b> {row['SAA Priority Systems']}<br>
#     #     {beneficiaries_impact}
#     #     <b>Description:</b> {row['Description']}<br>
#     #     {video_description_link}
#     #     <a href="{row['Official_Link']}" target="_blank"><b>Read full solution story here!</b></a>
#     # </div>
#     # """
    
#     popup_html = f"""
#     <div>
#         <b style="color:#FF37D5;">RtR SOLUTION STORY</b><br>
#         <b>Title:</b> {row['Title']}<b>.</b><br>
#         <b>Year:</b> {row['Year']}<br>
#         <b>Partner:</b> {row['InitName']}<br>
#         <b>Location:</b> {row['Onclick']}<br> 
#         <b>SAA Priority Systems:</b> {row['SAA Priority Systems']}<br>
#     </div>
#     """

#     popup = folium.Popup(popup_html, max_width=300)
#     folium.Marker(
#         location=[row["lat"], row["lon"]],
#         popup=popup,
#         tooltip=row['Onclick'],
#     ).add_to(world_map_solution_stories)

# # Display the map in Streamlit.
# st_folium(world_map_solution_stories, width=725, key="map_solution_stories", returned_objects=[])


# solution_studies_table_public_list = ['InitName',
# 'Title',
# 'Description',
# 'Date',
# 'SAA Priority Systems',
# 'Implementers',
# 'Beneficiaries / Impact:',
# 'Official_Link',
# 'Video_Description',
# 'Cities',
# 'All_Countries',
# 'country_continents_all',
# 'country_region_all',
# 'country_subregion_all',]


# with st.expander("Solution Stories Data Set: Filtered Based on Selection Criteria"):
#     st.dataframe(df_filtered[solution_studies_table_public_list])
    






st.write("___")
st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

st.markdown("""
<style>
    a {
        text-decoration: none; /* Remove underline */
        color: #000000; /* Set link color */
    }
    a:hover {
        color: #FF37D5; /* Set hover color */
        text-decoration: underline; /* Underline on hover for better UX */
    }
    .link-list {
        line-height: 1.6; /* Adjust line spacing */
    }
</style>
<div class="link-list">
    <ul>
        <li>To get an overview of the campaign as a whole, <a href="/HOME" target="_self"><strong>click here</strong></a></li>
        <li>To search for the contribution of specific partners, <a href="/PARTNER_FINDER" target="_self"><strong>click here</strong></a></li>
        <li>To explore our Metrics Framework, <a href="/METRICS_FRAMEWORK" target="_self"><strong>click here</strong></a></li>
        <li>To get more information on this data explorer, <a href="/ABOUT_THE_DATA_EXPLORER" target="_self"><strong>click here</strong></a></li>
    </ul>
</div>
""", unsafe_allow_html=True)