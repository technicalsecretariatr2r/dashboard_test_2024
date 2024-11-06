## LIBRARIES

import streamlit as st
import pandas as pd
import numpy as np
import os
import io
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as ticker
from matplotlib.ticker import MaxNLocator
from matplotlib.ticker import ScalarFormatter
from matplotlib.ticker import FuncFormatter
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
from numerize.numerize import numerize
from datetime import datetime


## WebStructure

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



#Funciones DATA

@st.cache_data
def load_data_cleaned_df_solution_stories():
    from etl_process import df_solution_stories
    return df_solution_stories

# Updata Upload
@st.cache_data
def load_data_cleaned_df_to_find_partner():
    from etl_process import df_to_find_partner
    return df_to_find_partner


@st.cache_data
def load_data_cleaned_df_gi():
    from etl_process import df_gi
    return df_gi

@st.cache_data
def load_data_cleaned_df_gi_summary():
    from etl_process import df_gi_summary
    return df_gi_summary



@st.cache_data
def load_data_cleaned_df_partner_campaign():
    from etl_process import df_partner_campaign
    return df_partner_campaign

@st.cache_data 
def load_data_df_hazards_pledge_plan_vertical():
    from etl_process import df_hazards_pledge_plan_vertical
    return df_hazards_pledge_plan_vertical


@st.cache_data
def load_data_cleaned_df_pledge_summary():
    from etl_process import df_pledge_summary
    return df_pledge_summary

@st.cache_data
def load_data_cleaned_df_m_countries_vertical():
    from etl_process import df_m_countries_vertical
    return df_m_countries_vertical

@st.cache_data
def load_data_cleaned_df_pledge():
    from etl_process import df_pledge
    return df_pledge

# Data Geo Country
@st.cache_resource
def load_countries():
        political_countries_url = "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
        return political_countries_url
political_countries_url = load_countries()

# Plan Consolidated By Partner
@st.cache_data 
def load_data_plan_consolided_by_partner():
    from etl_process import df_2023_plan_summary_by_partner
    return df_2023_plan_summary_by_partner

@st.cache_data 
def load_plan():
    from etl_process import df_2023_plan
    return df_2023_plan

@st.cache_data 
def load_plan_summary():
    from etl_process import df_2023_plan_summary
    return df_2023_plan_summary

@st.cache_data 
def partners_summary():
    from etl_process import df_all_partners_summary
    return df_all_partners_summary

@st.cache_data 
def summary_partner_tracking_table():
    from etl_process import df_partner_campaign
    return df_partner_campaign

@st.cache_data 
def data_gaps():
    from etl_process import df_gaps_all
    return df_gaps_all


## Calling the funcions and creating datasets
df_all_partners_summary = partners_summary()
df_partner_campaign_tracker = summary_partner_tracking_table()
df_partner_campaign = load_data_cleaned_df_partner_campaign()
df_to_find_partner = load_data_cleaned_df_to_find_partner()

df_gi = load_data_cleaned_df_gi()
df_gi_summary = load_data_cleaned_df_gi_summary()


df_solution_stories = load_data_cleaned_df_solution_stories()
df_m_countries_vertical = load_data_cleaned_df_m_countries_vertical()

df_pledge = load_data_cleaned_df_pledge()
df_pledge_summary = load_data_cleaned_df_pledge_summary()
df_hazards_pledge_plan_vertical = load_data_df_hazards_pledge_plan_vertical()

df_2023_plan = load_plan()
df_2023_plan_summary = load_plan_summary()
df_2023_plan_summary_by_partner = load_data_plan_consolided_by_partner()

df_gaps_all = data_gaps()


## FILTER
df_all_partners_summary = df_all_partners_summary[df_all_partners_summary['Reporting Status'].isin(['Reporting Partner', 'New Partner'])]
df_partner_campaign_tracker = df_partner_campaign_tracker[df_partner_campaign_tracker['Org_Type'].isin(['Reporting Partner', 'New Partner ','Member'])]



df_to_find_partner = df_to_find_partner[df_to_find_partner['Org_Type'].isin(['Reporting Partner', 'New Partner', 'Member'])]
df_partner_campaign = df_partner_campaign[df_partner_campaign['Org_Type'].isin(['Reporting Partner', 'New Partner', 'Member'])]


df_gi = df_gi[df_gi['Org_Type'].isin(['Reporting Partner', 'New Partner', 'Member'])]
df_gi_summary = df_gi_summary[df_gi_summary['Org_Type'].isin(['Reporting Partner', 'New Partner', 'Member'])]
df_pledge = df_pledge[df_pledge['Org_Type'].isin(['Reporting Partner', 'New Partner', 'Member'])]
df_pledge_summary = df_pledge_summary[df_pledge_summary['Org_Type'].isin(['Reporting Partner', 'New Partner', 'Member'])]
df_2023_plan = df_2023_plan[df_2023_plan['Org_Type'].isin(['Reporting Partner', 'New Partner', 'Member'])]
df_2023_plan_summary = df_2023_plan_summary[df_2023_plan_summary['Org_Type'].isin(['Reporting Partner', 'New Partner', 'Member'])]
df_2023_plan_summary_by_partner = df_2023_plan_summary_by_partner[df_2023_plan_summary_by_partner['Org_Type'].isin(['Reporting Partner', 'New Partner', 'Member'])]
df_gaps_all = df_gaps_all[df_gaps_all['Org_Type'].isin(['Reporting Partner', 'New Partner', 'Member'])]
df_m_countries_vertical = df_m_countries_vertical[df_m_countries_vertical['Org_Type'].isin(['Reporting Partner', 'New Partner', 'Member'])]
df_2023_plan = df_2023_plan[df_2023_plan['Org_Type'].isin(['Reporting Partner', 'New Partner', 'Member'])]

# st.write('df_all_partners_summary')
# df_all_partners_summary

# st.write('df_partner_campaign_tracker')
# df_partner_campaign_tracker

# st.write('df_to_find_partner')
# df_to_find_partner.columns

# st.write('df_to_find_partner')
# df_partner_campaign





# ____________________________________
# ____________________________________
# ____________________________________
# END PARTNER SELECTOR
# ____________________________________
# ____________________________________
# ____________________________________




# ____________________________________
# ____________________________________
# ____________________________________
# INICIO
# ____________________________________
# ____________________________________
# ____________________________________




st.markdown('# PARTNER FINDER')
# st.markdown('Partners are at the heart of the campaign, they represent the initiatives that embody the work of the campaign on the ground for building resilience against climate hazards. RtR partners take action in different parts of the world, pursuing different targets and different action focuses, with the common goal of finding ways to contribute to the resilience of vulnerable communities. The Partner Finder enables users to navigate the data provided by our partners, allowing them to search and review information based on customized criteria.')
st.markdown("""Partners drive the campaign’s on-the-ground resilience work against climate hazards worldwide, targeting diverse goals to support vulnerable communities. 
            The Partner Finder helps users explore partner data, enabling searches based on custom criteria.
            """)

Instructions = """
    **INSTRUCTIONS:** Enter criteria and press SEARCH to see matching RtR partners. Select a partner for details, or view all if no criteria are entered.
"""

st.markdown(f"""
    <style>
    .disclaimer {{
        color: #112E4D; /* Dark blue text color */
        background-color: rgba(255, 55, 213, 0.1); /* Light pink background */
        padding: 10px;
        border-radius: 5px;
        border: 2px solid #FF37D5; /* Pink border */
        font-size: 16px;
        margin-bottom: 10px; /* Adds space below the disclaimer */
    }}
    </style>
    <div class="disclaimer">
        {Instructions}
    </div>
    """, 
    unsafe_allow_html=True)
    
st.sidebar.markdown("[CRITERIA-BASED PARTNER FINDER](#criteria-based-partner-finder)")

# ____________________________________
# ____________________________________
# ____________________________________
# END INICIO
# ____________________________________
# ____________________________________
# ____________________________________


#__________________________________________________________________________________________________________________________________________________________________
# Multiselector: organization of the data
#__________________________________________________________________________________________________________________________________________________________________
#

#Indentifing unique names of countries in "All Countries"
countries = df_to_find_partner['all_countries'].str.split(';').explode()
# Removing any leading/trailing whitespace and filtering out empty or whitespace-only strings
countries = countries.str.strip()
countries = countries[countries != '']
# Getting unique values
unique_countries = countries.unique()
# Converting to a list
unique_countries_list_cats_deg = list(unique_countries)
unique_countries_list_cats_deg.append(",''")
unique_countries_list_options = list(unique_countries)


cats_defs = [
        ['priority_groups_gi_concat',  ['Women and girls','LGBTQIA+ people','Elderly','Children & Youth','Indigenous and traditional communities','Ethnic or religious minorities','Refugees','Disabled People','Low Income Communities','']],
        ['saa_p_systems_gi_concat',      ['Food and Agriculture','Health','Human Settlements','Coastal and Oceans','Infrastructure','Water and Nature','Planning and Policy: Cross-cutting','Finance: Cross-cutting','']],
        ['action_clusters_gi_concat',['Monitoring and mapping of hazards and vulnerabilities','Climate services and modelling','Generation and processing of data','Early warning systems','Emergency preparedness','Environmental governance and resource management systems','Environmental laws and regulatory framework','Building regulations and standards for climate resilience','Protected areas and property rights definitions','Institutional-led climate adaptation planning processes','Measures to improve air quality and reduce pollution','Green infrastructure and other engineered nature-based solutions','Conservation and restoration of terrestrial and aquatic ecosystems','Critical Infrastructure and Protective Systems','Coastal Infrastructure Protection','Energy efficiency and renewable energy technologies','Water security and quality','Health services','Food safety and sustainable services','Agricultural, livestock, forestry and aquiacultural practices actions','Social protection actions','Community-based inclusive and participatory risk reduction','Climate hazard communication, information, and technology awareness','Knowledge building for resilience','Research and collaboration actions','Livelihood diversification and social economy','Climate insurance and risk transfer','Financial and investment tools in case of climate disasters','Economic incentives','']],  
        ['hazards_all_pledge_concat',['Water stress (urban focus)', 'Water stress (rural focus)', 'Extreme heat','Extreme cold', 'Drought (agriculture focus)', 'Drought (other sectors)','Urban flood', 'River flood', 'Coastal flood', 'Tropical Cyclone','Snow, Ice', 'Wildfire', 'Extreme wind', 'Oceanic Events','Other coastal events','']],
        ['p_benefic_pledge_concat',['Individuals','Companies','Regions','Cities','Natural-Systems','']],
        ['all_countries',['Afghanistan','Albania','Algeria','Andorra','Angola','Antigua and Barbuda','Argentina','Armenia','Australia','Austria','Azerbaijan','Bahamas','Bahrain','Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bhutan','Bolivia, Plurinational State of','Bosnia and Herzegovina','Botswana','Brazil','Brunei Darussalam','Bulgaria','Burkina Faso','Burundi','Cambodia','Cameroon','Canada','Cape Verde','Central African Republic','Chad','Chile','China','Colombia','Comoros','Congo','Congo, the Democratic Republic of the','Costa Rica',"Côte d'Ivoire",'Croatia','Cuba','Cyprus','Czech Republic','Denmark','Djibouti','Dominica','Dominican Republic','Ecuador','Egypt','El Salvador','Equatorial Guinea','Eritrea','Estonia','Ethiopia','Finland','France','Gabon','Gambia','Georgia','Germany','Ghana','Greece','Grenada','Guatemala','Guinea','Guinea-Bissau','Guyana','Haiti','Honduras','Hungary','Iceland','India','Indonesia','Iran, Islamic Republic of','Iraq','Ireland','Israel','Italy','Jamaica','Japan','Jordan','Kazakhstan','Kenya','Korea, Republic of','Kuwait','Kyrgyzstan',"Lao People's Democratic Republic",'Latvia','Lebanon','Lesotho','Liberia','Libyan Arab Jamahiriya','Liechtenstein','Lithuania','Luxembourg','Macedonia, the former Yugoslav Republic of','Madagascar','Malawi','Malaysia','Mali','Malta','Mauritania','Mauritius','Mexico','Micronesia, Federated States of','Moldova, Republic of','Mongolia','Montenegro','Morocco','Mozambique','Myanmar','Namibia','Nepal','Netherlands','New Zealand','Nicaragua','Niger','Nigeria','North Korea','Norway','Oman','Pakistan','Palestinian Territory, Occupied','Panama','Papua New Guinea','Paraguay','Peru','Philippines','Poland','Portugal','Puerto Rico','Qatar','Romania','Russian Federation','Rwanda','Saint Vincent and the Grenadines','Samoa','Sao Tome and Principe','Saudi Arabia','Senegal','Serbia','Sierra Leone','Singapore','Slovakia','Slovenia','Solomon Islands','Somalia','Somaliland','South Africa','South Sudan','Spain','Sri Lanka','Sudan','Suriname','Swaziland','Sweden','Switzerland','Syrian Arab Republic','Taiwan, Province of China','Tajikistan','Tanzania, United Republic of','Thailand','Timor-Leste','Togo','Tonga','Trinidad and Tobago','Tunisia','Turkey','Turkmenistan','Uganda','Ukraine','United Arab Emirates','United Kingdom','United States of America','Uruguay','Uzbekistan','Vanuatu','Venezuela, Bolivarian Republic of','Viet Nam','Western Sahara','Yemen','Zambia','Zimbabwe','']],
        ['country_continents_all', ['Africa', 'Asia', 'Europe', 'Latin America and the Caribbean', 'Northern America', 'Oceania','']],
        ['country_region_all',['South Asia', 'Europe & Central Asia', 'Middle East & North Africa', 'Sub-Saharan Africa', 'Latin America & Caribbean', 'East Asia & Pacific', 'North America','']],
        ['country_subregion_all',['Southern Asia','Southern Europe','Northern Africa','Middle Africa','Caribbean','South America','Western Asia','Australia and New Zealand','Western Europe','Eastern Europe','Central America','Western Africa','Southern Africa','Eastern Africa','South-Eastern Asia','Northern America','Eastern Asia','Northern Europe','Central Asia','Melanesia','Polynesia','Micronesia','']],
        ]  


cats = [cats_defs[0][0],                                  cats_defs[1][0]                           , cats_defs[2][0]                              ,cats_defs[3][0],                               cats_defs[4][0],                                              cats_defs[5][0],                           cats_defs[6][0],                                       cats_defs[7][0],                                 cats_defs[8][0]     ]  #list of question categories
defs = [cats_defs[0][1],                                  cats_defs[1][1]                           , cats_defs[2][1]                              ,cats_defs[3][1],                               cats_defs[4][1],                                              cats_defs[5][1],                           cats_defs[6][1],                                       cats_defs[7][1],                                 cats_defs[8][1]     ]  #list of possible answers
poss = [df_to_find_partner['priority_groups_gi_concat'].tolist(), df_to_find_partner['saa_p_systems_gi_concat'].tolist(), df_to_find_partner['action_clusters_gi_concat'].tolist(),df_to_find_partner['hazards_all_pledge_concat'].tolist(),df_to_find_partner['p_benefic_pledge_concat'].tolist(),df_to_find_partner['all_countries'].tolist(),df_to_find_partner['country_continents_all'].tolist(),df_to_find_partner['country_region_all'].tolist(),df_to_find_partner['country_subregion_all'].tolist(),]


priority_options = ['Women and girls','LGBTQIA+ people','Elderly','Children & Youth','Indigenous and traditional communities','Ethnic or religious minorities','Refugees','Disabled People','Low Income Communities',]
saa_options = ['Food and Agriculture','Health','Human Settlements','Coastal and Oceans','Infrastructure','Water and Nature','Planning and Policy: Cross-cutting','Finance: Cross-cutting']
actioncluster_options = ['Monitoring and mapping of hazards and vulnerabilities','Climate services and modelling','Generation and processing of data','Early warning systems','Emergency preparedness','Environmental governance and resource management systems','Environmental laws and regulatory framework','Building regulations and standards for climate resilience','Protected areas and property rights definitions','Institutional-led climate adaptation planning processes','Measures to improve air quality and reduce pollution','Green infrastructure and other engineered nature-based solutions','Conservation and restoration of terrestrial and aquatic ecosystems','Critical Infrastructure and Protective Systems','Coastal Infrastructure Protection','Energy efficiency and renewable energy technologies','Water security and quality','Health services','Food safety and sustainable services','Agricultural, livestock, forestry and aquiacultural practices actions','Social protection actions','Community-based inclusive and participatory risk reduction','Climate hazard communication, information, and technology awareness','Knowledge building for resilience','Research and collaboration actions','Livelihood diversification and social economy','Climate insurance and risk transfer','Financial and investment tools in case of climate disasters','Economic incentives',]
hazard_options = ['Water stress (urban focus)', 'Water stress (rural focus)', 'Extreme heat','Extreme cold', 'Drought (agriculture focus)', 'Drought (other sectors)','Urban flood', 'River flood', 'Coastal flood', 'Tropical Cyclone','Snow, Ice', 'Wildfire', 'Extreme wind', 'Oceanic Events','Other coastal events']
p_beneficiaries_options =['Individuals','Companies','Regions','Cities','Natural-Systems',]
All_Countries_options =['Afghanistan','Albania','Algeria','Andorra','Angola','Antigua and Barbuda','Argentina','Armenia','Australia','Austria','Azerbaijan','Bahamas','Bahrain','Bangladesh','Barbados','Belarus','Belgium','Belize','Benin','Bhutan','Bolivia, Plurinational State of','Bosnia and Herzegovina','Botswana','Brazil','Brunei Darussalam','Bulgaria','Burkina Faso','Burundi','Cambodia','Cameroon','Canada','Cape Verde','Central African Republic','Chad','Chile','China','Colombia','Comoros','Congo','Congo, the Democratic Republic of the','Costa Rica',"Côte d'Ivoire",'Croatia','Cuba','Cyprus','Czech Republic','Denmark','Djibouti','Dominica','Dominican Republic','Ecuador','Egypt','El Salvador','Equatorial Guinea','Eritrea','Estonia','Ethiopia','Finland','France','Gabon','Gambia','Georgia','Germany','Ghana','Greece','Grenada','Guatemala','Guinea','Guinea-Bissau','Guyana','Haiti','Honduras','Hungary','Iceland','India','Indonesia','Iran, Islamic Republic of','Iraq','Ireland','Israel','Italy','Jamaica','Japan','Jordan','Kazakhstan','Kenya','Korea, Republic of','Kuwait','Kyrgyzstan',"Lao People's Democratic Republic",'Latvia','Lebanon','Lesotho','Liberia','Libyan Arab Jamahiriya','Liechtenstein','Lithuania','Luxembourg','Macedonia, the former Yugoslav Republic of','Madagascar','Malawi','Malaysia','Mali','Malta','Mauritania','Mauritius','Mexico','Micronesia, Federated States of','Moldova, Republic of','Mongolia','Montenegro','Morocco','Mozambique','Myanmar','Namibia','Nepal','Netherlands','New Zealand','Nicaragua','Niger','Nigeria','North Korea','Norway','Oman','Pakistan','Palestinian Territory, Occupied','Panama','Papua New Guinea','Paraguay','Peru','Philippines','Poland','Portugal','Puerto Rico','Qatar','Romania','Russian Federation','Rwanda','Saint Vincent and the Grenadines','Samoa','Sao Tome and Principe','Saudi Arabia','Senegal','Serbia','Sierra Leone','Singapore','Slovakia','Slovenia','Solomon Islands','Somalia','Somaliland','South Africa','South Sudan','Spain','Sri Lanka','Sudan','Suriname','Swaziland','Sweden','Switzerland','Syrian Arab Republic','Taiwan, Province of China','Tajikistan','Tanzania, United Republic of','Thailand','Timor-Leste','Togo','Tonga','Trinidad and Tobago','Tunisia','Turkey','Turkmenistan','Uganda','Ukraine','United Arab Emirates','United Kingdom','United States of America','Uruguay','Uzbekistan','Vanuatu','Venezuela, Bolivarian Republic of','Viet Nam','Western Sahara','Yemen','Zambia','Zimbabwe']
country_continents_all_options =['Africa', 'Asia', 'Europe', 'Latin America and the Caribbean', 'Northern America', 'Oceania']
country_region_all_options = ['South Asia', 'Europe & Central Asia', 'Middle East & North Africa', 'Sub-Saharan Africa', 'Latin America & Caribbean', 'East Asia & Pacific', 'North America']
country_subregion_all_options = ['Southern Asia','Southern Europe','Northern Africa','Middle Africa','Caribbean','South America','Western Asia','Australia and New Zealand','Western Europe','Eastern Europe','Central America','Western Africa','Southern Africa','Eastern Africa','South-Eastern Asia','Northern America','Eastern Asia','Northern Europe','Central Asia','Melanesia','Polynesia','Micronesia',]


with st.form("my_form",clear_on_submit=True):
    
    col1, col2, col3 = st.columns(3)
    with col1: 
        saa_selection = st.multiselect("SAA Systems",      saa_options)
        hazard_selection = st.multiselect("Climate Hazards",      hazard_options)
        continent_selection = st.multiselect("Continent",      country_continents_all_options)

    with col2: 
        priority_selection = st.multiselect('Priority Groups',   priority_options)
        p_beneficiaries_selection = st.multiselect('Target Beneficiaries',   p_beneficiaries_options)
        region_selection = st.multiselect("Region",      country_region_all_options)
        
    with col3:
        action_cluster_selection = st.multiselect('Action Cluster',   actioncluster_options)
        All_Countries_selection = st.multiselect('Country',   All_Countries_options)
        subregion_selection = st.multiselect("Sub Region",      country_subregion_all_options)
        
        
        submitted = st.form_submit_button("SEARCH")
if submitted:
    st.markdown("")

selection = [priority_selection,saa_selection,action_cluster_selection,hazard_selection,p_beneficiaries_selection,All_Countries_selection,continent_selection,region_selection,subregion_selection]

# selection = [['LGBTQIA+ people', 'Elderly'], [], []]


#__________________________________________________________________________________________________________________________________________________________________
# END: mULTISELECTOR. ORGANIZATION OF THE DATA
#__________________________________________________________________________________________________________________________________________________________________







#__________________________________________________________________________________________________________________________________________________________________
## SEARCH ALGORITM
#__________________________________________________________________________________________________________________________________________________________________

##Showing results 
if all(not s for s in selection):
    st.write('All RtR partners are available for selection and exploration.')
    st.sidebar.markdown('All RtR partners are available for selection and exploration.')
else:
    st.markdown('<span style="color:#FF37D5; font-weight:bold">YOU SELECTED:</span>', unsafe_allow_html=True)
    selected_options = []
    for s in selection:
        if s:
            selected_options.extend(s)
    selected_options_str = ', '.join(selected_options)
    st.write(selected_options_str)
    st.sidebar.markdown("**You Selected:** "+ selected_options_str)

df_to_find_partner_len = len(df_to_find_partner.index)

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

final_list = list(range(0,df_to_find_partner_len+1))
j = 0
while j < len(selection):
        temp_list  = list(set(index_selection_results(selection[j],poss[j]))) #avoidung index duplications
        final_list = list(set(common_member(temp_list,final_list)))
        j = j+1

# df_filtered = df_to_find_partner.iloc[final_list].reset_index().sort_values(by = 'InitName')
df_filtered = df_to_find_partner.iloc[final_list].reset_index(drop=True).sort_values(by='InitName')

# df_filtered.set_index("Master ID", inplace = True)
#__________________________________________________________________________________________________________________________________________________________________
## END SEARCH ALGORITM
#__________________________________________________________________________________________________________________________________________________________________






#__________________________________________________________________________________________________________________________________________________________________
# RESULT FROM THE SELECTION
#__________________________________________________________________________________________________________________________________________________________________
list_partners = df_filtered.InitName.unique()
count_partners = str(df_filtered['InitName'].count())

# Create a markdown list by appending each item with a preceding '* '
markdown_list = '\n'.join(['* ' + item for item in list_partners])

# st.markdown('<span style="color:#FF37D5; font-weight:bold">RESULTS:</span>', unsafe_allow_html=True)
# Concatenate the markdown list with the count of partners

result = f"There are **{count_partners}** RtR Initiatives that meet your selection criteria:\n{markdown_list}"

# result = f"There are **{count_partners}** RtR Initiatives that meet your selection criteria."


if count_partners == str(35):
    pass
else:
    st.sidebar.markdown(f"There are **{count_partners}** RtR Initiatives that meet your selection criteria")

from selection_all import selection_all

if selection == selection_all:
     
    disclaimer = (f"To know more about RtR partners, please use the Partner Selector below.")
    
    st.markdown(f"""
    <style>
    .disclaimer {{
        color: #112E4D; /* Dark blue text color */
        background-color: rgba(255, 55, 213, 0.1); /* Light pink background */
        padding: 10px;
        border-radius: 5px;
        border: 2px solid #FF37D5; /* Pink border */
        font-size: 16px;
        margin-bottom: 10px; /* Adds space below the disclaimer */
    }}
    </style>
    <div class="disclaimer">
        {disclaimer}
    </div>
    """, 
    unsafe_allow_html=True)
    # st.markdown("If you'd like to know more about what each of our partners does within the campaign, please select them from the Partner Selector below.")

else:
    st.markdown('')
    st.write(result)







# # _________________________________________
# # Making the Multiselector for partners
# # _________________________________________

### INFORMATION BY PARTNER
#FILTER SelectBox por partner
df = df_filtered
options = list(df['InitName'].unique())
options.append("") 

def custom_sort_key(options):
        order = {
            '': 1,
        }
        
        if options in order:
            return order[options]
        return 2

    # Sort the unique_sources list using the custom sorting key
options = sorted(options, key=custom_sort_key)




# st.markdown("## SELECT A PARTNER")
st.markdown("## PARTNER SELECTOR")
partner = st.selectbox(
    "Select a RtR Partner:",
    options=options)


df_gi_select_filtered = df_gi.query('InitName == @partner')
df_partner_campaign_filtered  = df_partner_campaign.query('InitName == @partner')
df_hazards_pledge_plan_vertical_filtered  = df_hazards_pledge_plan_vertical.query('InitName == @partner')
df_2023_plan_summary_by_partner_filtered  = df_2023_plan_summary_by_partner.query('InitName == @partner')
df_pledge_summary_filtered  = df_pledge_summary.query('InitName == @partner')
df_gi_summary_filtered = df_gi_summary.query('InitName == @partner')

df_to_find_partner_filtered  = df_to_find_partner.query('InitName == @partner')
df_m_countries_vertical_filtered  = df_m_countries_vertical.query('InitName == @partner')
df_pledge_filtered  = df_pledge.query('InitName == @partner')
df_2023_plan_filtered  = df_2023_plan.query('InitName == @partner')
df_solution_stories_filtered  = df_solution_stories.query('InitName == @partner')

df_all_partners_summary  = df_all_partners_summary.rename(columns={'Partner Name': 'InitName'})
df_all_partners_summary_filtered  = df_all_partners_summary.query('InitName == @partner')


st.markdown("____")
st.sidebar.markdown('[SELECT A PARTNER](#partner-selector)', unsafe_allow_html=True)
st.sidebar.markdown('**Partner Selected:** '+partner, unsafe_allow_html=True)


st.write("### Summary Tables")
st.write("###### Section under development. Key information is already available in table format.")


# Description table
st.write("#### Description")
if df_all_partners_summary["InitName"].notna().any():
    st.write(df_all_partners_summary_filtered )
else:
    st.write("No description information has yet been reported by the selected partner.")

# Reporting Status table
st.write("#### Reporting Status")
if df_partner_campaign["InitName"].notna().any():
    st.write(df_partner_campaign_filtered )
else:
    st.write("No reporting status information has yet been reported by the selected partner.")

# Solution Stories table
st.write("### Solution Stories")
if df_solution_stories["InitName"].notna().any():
    st.write("#### Solution Stories")
    st.write(df_solution_stories_filtered )
else:
    st.write("No solution stories information has yet been reported by the selected partner.")

st.write("### Reporting Tools")
# General Information table in Reporting Tools
if df_gi_summary["InitName"].notna().any():
    st.write("#### General Information")
    st.write(df_gi_summary_filtered)
else:
    st.write("No general information has yet been reported by the selected partner.")

st.write("#### Pledge Statement")
# Pledge Statement table in Reporting Tools
if df_pledge_summary["InitName"].notna().any():
    st.write(df_pledge_summary_filtered)
else:
    st.write("No pledge statement information has yet been reported by the selected partner.")

# Plan table in Reporting Tools
st.write("#### Plan")
if df_2023_plan_summary_by_partner["InitName"].notna().any():
    st.write(df_2023_plan_summary_by_partner_filtered)
else:
    st.write("No plan information has yet been reported by the selected partner.")

# ____________________________________
# ____________________________________
# ____________________________________
# END PARTNER SELECTOR
# ____________________________________
# ____________________________________
# ____________________________________





# ___________________________________
# ___________________________________
# ___________________________________
# RESULT
# ___________________________________
# ___________________________________

try:
    p_short_name = df_partner_campaign['short_name'].iloc[0]
    p_full_name = df_partner_campaign['name_only'].iloc[0]
    try:
        logo = df_partner_campaign['logo'].iloc[0]
        image = Image.open(logo+'.png')
        col1, col2 = st.columns([0.3,1.7])
        col1.image(image, width=100)
        col2.header((p_full_name + " - " + p_short_name).upper())

    except Exception as e:
        st.header((p_full_name + " - " + p_short_name).upper())
except Exception as e:
    pass



# from presentation_partner import presentation_parter
# from reporting_status import reporting_status
# from aggregated_metrics_summary_parter_finder import aggregated_metrics_partner_finder
# from globalreach_partner_finder import global_reach_partner_finder
# from self_description_partner_finder import selfdescription_partner_finder
# from saa_campaign_partner_finder import saa_partner_finder
# from target_beneficiaries_partner_finder import priority_groups_partnerfinder
# from ra_campaign_partner_finder import ra_campaign_partner_finder
# from action_cluster_to_partner_finder import action_cluster_to_partner_finder
# from hazards_partner_finder import hazards_partner_finder
# from solution_stories_partner_finder import solution_stories_partner_finder
















# # Create a multi-select widget in the sidebar to choose sections
# # Create a radial (radio button) selection widget in the sidebar

# selected_section = st.sidebar.radio(
#     '*SELECT A SECTION TO DISPLAY*',
#     ['Presentation Level', 'Aggregated Metrics', 'Global Outreach','SAA Priority Systems', 'Climate Hazards','Target Beneficiaries','Resilience Action Clusters','Resilience Attributes', 'Reporting Status']
# )

# # Display selected sections based on user's choice

# if 'Presentation Level' in selected_section:
#     try:
#         presentation_parter(df_partner_campaign, df_gi_select)
#         selfdescription_partner_finder(df_gi_select, p_short_name)
#         # st.write("___")
#         # st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

        
#         # Check if 'InitName' column in df_solution_stories is not empty
#         if df_solution_stories['InitName'].notna().any():
#             solution_stories_partner_finder(df_solution_stories, p_short_name)
#             st.write("___")
#             st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

#         else:
#             st.write("")
#             # st.write("No Solution Stories Available")
#     except Exception as e:
#         pass
    

# if 'Reporting Status' in selected_section:
#     try:
#         reporting_status(df_m_countries_vertical, df_partner_campaign)
#         st.write("___")
#         st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")
#     except Exception as e:
#         pass

# if 'Aggregated Metrics' in selected_section:
#     try:
#         aggregated_metrics_partner_finder(df_to_find_partner,df_pledge_summary,df_pledge,df_m_countries_vertical,df_partner_campaign,df_2022_2023_plan_consolidated_by_partner)
#         st.write("___")
#         st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

#     except Exception as e:
#         pass

# if 'Outreach' in selected_section:
#     try:
#         global_reach_partner_finder(df_partner_campaign, df_m_countries_vertical, political_countries_url)
#         st.write("___")
#         st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

#     except Exception as e:
#         pass
    
# if 'Target Beneficiaries' in selected_section:
#     try:
#         priority_groups_partnerfinder(df_gi_select,p_short_name)
#         st.write("___")
#         st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

#     except Exception as e:
#         st.markdown("#### TARGET BENEFICIARIES")
#         st.markdown("No Information Available")
#         pass
# if 'SAA Priority Systems' in selected_section:
#     try:
#         n_reporting_partners = 1
#         saa_partner_finder(df_gi_select,n_reporting_partners,p_short_name)
#         st.write("___")
#         st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

#     except Exception as e:
#         n_reporting_partners = 1
#         p_short_name = 'No Info'
#         saa_partner_finder(df_gi_select,n_reporting_partners,p_short_name)
#         st.write("___")
#         st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")
#         pass

# if 'Resilience Attributes' in selected_section:
#     try:
#         ra_campaign_partner_finder(df_2022_2023_plan_consolidated,p_short_name)
#         st.write("___")
#         st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

#     except Exception as e:
#         st.markdown("#### RESILIENCE ATTRIBUTES")
#         st.markdown("No Information Available")
        
#         pass

# if 'Resilience Action Clusters' in selected_section:
#     try:
#         action_cluster_to_partner_finder(df_gi_select,ac_atypes,p_short_name)
#         st.write("___")
#         st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

#     except Exception as e:
#         st.markdown("#### RESILIENCE ACTION CLUSTERS")
#         st.markdown("No Information Available")
#         st.write("___")
#         st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

#         pass
    
# if 'Climate Hazards' in selected_section:
#     try:
#         hazards_partner_finder(df_hazards_pledge_plan_vertical,p_short_name)
#         st.write("___")
#         st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

#     except Exception as e:
#         st.markdown("#### CLIMATE HAZARDS")
#         st.markdown("No Information Available")
#         st.write("___")
#         st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

#         pass



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
        <li>To search for partners solution stories, <a href="/SOLUTION_STORIES" target="_self"><strong>click here</strong></a></li>
        <li>To explore our Metrics Framework, <a href="/METRICS_FRAMEWORK" target="_self"><strong>click here</strong></a></li>
        <li>To get more information on this data explorer, <a href="/ABOUT_THE_DATA_EXPLORER" target="_self"><strong>click here</strong></a></li>
    </ul>
</div>
""", unsafe_allow_html=True)
