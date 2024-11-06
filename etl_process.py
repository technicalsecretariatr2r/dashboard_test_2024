import streamlit as st
import pandas as pd
import numpy as np
import os
import re
import openpyxl
from openpyxl.styles import Border, Side
import io
from io import BytesIO
import plotly.express as px
from datetime import datetime, timedelta

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.cm as cm

from streamlit_folium import st_folium
import folium
import seaborn as sns
from matplotlib.colors import LinearSegmentedColormap


# import geopandas as gpd
import requests

# headers = {
#     "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
# }
# url = "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
# response = requests.get(url, headers=headers)
# data = response.json()

# gdf = gpd.GeoDataFrame.from_features(data["features"])

# df_geoinfo = gdf.drop(columns='geometry')

# st.write(df_geoinfo)

# # Save the DataFrame to a CSV file
# df_geoinfo.to_csv('countries_data_geojson.csv', index=False)


#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________________________
# IMPORT DATA
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________

#File Paths
file_path_partner_list = "RtR_Partner_List.csv"
file_path_countries_pledge_plan = "pledge_plan_for _country_20231121.csv"
file_path_solution_stories = "solution_stories_rtr_231201.csv"
file_path_responses_evaluated = 'RtR_Partner_Responses_Qualitative_Evaluation.csv'

file_path_data_pledge_2022 = "data_pledge_2022.csv" 
file_path_data_plan_2022 = "data_plan_2022.csv" 
file_path_data_ra_2022 = "RA_24-02.csv" 
file_path_campaign_index = "index_campaign.csv" 

file_path_ac_atypes = "action_cluster_to_Action_Types.csv"
file_path_ac_atypes_plan = "action_cluster_to_action_types_plan.csv"

file_path_country_geo_info = "countries_geoinfo.csv"

# file_path_gi = "GI_231208.csv"
# file_path_pledge = "PLEDGE_231121.csv"
# file_path_plan = "PLAN_240229.csv"

# file_path_gi = "GI_240409.csv"
# file_path_pledge = "PLEDGE_240409.csv"
# file_path_plan = "PLAN_240409.csv"

# file_path_gi = "GI_240416.csv"
# file_path_pledge = "PLEDGE_240416.csv"
# file_path_plan = "PLAN_240416.csv"

# file_path_gi = "GI_240430.csv"
# file_path_pledge = "PLEDGE_240430.csv"
# file_path_plan = "PLAN_240430.csv"

# file_path_gi = "GI_240503.csv"
# file_path_pledge = "PLEDGE_240503.csv"
# file_path_plan = "PLAN_240503.csv"

# file_path_gi = "GI_240508.csv"
# file_path_pledge = "PLEDGE_240508.csv"
# file_path_plan = "PLAN_240508.csv"

# file_path_gi = "GI_240514.csv"
# file_path_pledge = "PLEDGE_240514.csv"
# # file_path_plan = "PLAN_240514.csv"
# file_path_plan = "PLAN_240521.csv"

# file_path_gi = "GI_240814.csv"
# file_path_pledge = "PLEDGE_240814.csv"
# file_path_plan = "PLAN_240814.csv"

# file_path_gi = "GI_240903.csv"
# file_path_pledge = "PLEDGE_240903.csv"
# file_path_plan = "PLAN_240903.csv"

# file_path_gi = "GI_240905.csv"
# file_path_pledge = "PLEDGE_240905.csv"
# file_path_plan = "PLAN_240905.csv"


# file_path_gi = "GI_240905.csv"
# file_path_gi = "GI_241002.csv"
# file_path_pledge = "PLEDGE_240905.csv"
# file_path_pledge = "PLEDGE_241021.csv"
# file_path_plan = "PLAN_240909.csv"
# file_path_plan = "PLAN_241021.csv"


file_path_gi = "GI_241029.csv"
file_path_pledge = "PLEDGE_241029.csv"
file_path_plan = "Plan_241029.csv"










#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________________________
# LOAD DATA
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________

## Load evaluation of responses files
df_responses_evaluated = pd.read_csv(file_path_responses_evaluated, sep=';') 
# st.write(df_responses_evaluated)

## Load Case Studies
df_solution_stories = pd.read_csv(file_path_solution_stories, sep=';') 

## Country Pledge Plan
df_ind_countries_pledge_plan = pd.read_csv(file_path_countries_pledge_plan, sep=';') 

## 2022 Data
### 2022 Plan INfo 
df_2022_plan = pd.read_csv(file_path_data_plan_2022, sep=';', header=None).iloc[2:]
df_2022_plan.columns = ['x' + str(col) for col in df_2022_plan.columns]
# st.write("2022 Plan Info")
# st.write(df_2022_plan)

### 2022 Pledge Info
df_2022_pledge = pd.read_csv(file_path_data_pledge_2022, sep=';') 
#st.write(df_2022_pledge)

### 2022 RA Info
df_2022_ra = pd.read_csv(file_path_data_ra_2022,sep=';', header=None).iloc[2:]
df_2022_ra.columns = ['y' + str(col) for col in df_2022_ra.columns]
# df_2022_ra

#Other Data Set
# st.sidebar.markdown("# Last Updated Dates for Files")
### CSV Partner's Name File
df_partners_name = pd.read_csv(file_path_partner_list, sep=';') 
#st.write(df_partners_name)

### CSV Action Cluster & Action Types (General Information)
ac_atypes = pd.read_csv(file_path_ac_atypes, sep=';') 
#st.write(ac_atypes)

### CSV Action Cluster & Action Types (plan)
ac_atypes_plan = pd.read_csv(file_path_ac_atypes_plan, sep=';') 
# st.write(ac_atypes_plan)

### CSV Country GeoInfo
df_country = pd.read_csv(file_path_country_geo_info,sep=';')    
# st.write(df_country)

### Index RtR Campaging_Different Stages of Partners
df_index_rtrcampaign = pd.read_csv(file_path_campaign_index,sep=';')    
# st.write(df_index_rtrcampaign)

### GENERAL INFORMATION SURVEY 2023
# Extracting the date of the data
filename_gi = file_path_gi
date_string_gi = os.path.splitext(filename_gi)[0][-6:]  # extract date part from filename
year = "20" + date_string_gi[:2]
month = date_string_gi[2:4]
day = date_string_gi[4:6]
formatted_date_gi = f"{year}/{month}/{day}"
# st.sidebar.markdown("General Information Survey, Update File: "+formatted_date_gi)

# CSV GIS File
df_gi = pd.read_csv(filename_gi, sep=',', header=None).iloc[2:]
df_gi.columns = ['q' + str(col) for col in df_gi.columns]
#st.write("General Information Survey")
#st.write(df_gi)

### PLEDGE STATEMENT SURVEY 2023
# Extracting the date of the data
filename_pledge = file_path_pledge
date_string_pledge = os.path.splitext(filename_pledge)[0][-6:]  # extract date part from filename
year = "20" + date_string_pledge[:2]
month = date_string_pledge[2:4]
day = date_string_pledge[4:6]
formatted_date_pledge = f"{year}/{month}/{day}"
# st.sidebar.markdown("Pledge Statement, Update File: "+formatted_date_pledge)

# CSV Pledge File
df_pledge = pd.read_csv(filename_pledge, sep=',', header=None).iloc[2:]
df_pledge.columns = ['s' + str(col) for col in df_pledge.columns]
#st.write("Pledge Statement Survey")
#st.write(df_pledge)

### RESILIENCE-BUILDING PLAN SURVEY 2023
# Extracting the date of the data
filename_plan = file_path_plan
date_string_plan = os.path.splitext(filename_plan)[0][-6:]  # extract date part from filename
year = "20" + date_string_plan[:2]
month = date_string_plan[2:4]
day = date_string_plan[4:6]
formatted_date_plan = f"{year}/{month}/{day}"
# st.sidebar.markdown(f"Resilience Building Plan, Update File: {formatted_date_plan}")

# CSV RESILIENCE-BUILIDING PLAN SURVEY 2023
df_2023_plan = pd.read_csv(filename_plan, sep=',', header=None).iloc[2:]
df_2023_plan.columns = ['r' + str(col) for col in df_2023_plan.columns]
#st.write("Resilience Building Plan")
#st.write(df_2023_plan)




######____________________________________________
##### FUNCTIONS
######____________________________________________

# Create a new column for pending identification based on a threshold for variables _status
def identify_req_status(row):
    pending_items = []
    for col in index_list:
        if row[col] == False:  # Placeholder condition
            pending_items.append(col)
    return ";".join(pending_items)


# Clean long texts entries. 
def clean_text(text):
    # Check if the text is a string
    if not isinstance(text, str):
        return "Not available yet"  # Return this if input is not a string

    # Normalize whitespaces and strip leading/trailing whitespace
    text = ' '.join(text.split())
    text = text.replace('"', '')

    # Function to handle the capitalization and proper line spacing
    def adjust_sentences(match):
        # Capitalize the first letter of the next sentence and add a newline
        return f"{match.group(1)}\n\n{match.group(2).upper()}"

    # Apply the adjustments to the text
    # This regex looks for a period followed by a space and any character, but not a digit
    text = re.sub(r"([!?:])\s*(\w)", adjust_sentences, text)

    # Format numerical lists properly: Move "number)" to a new line if it's not already
    text = re.sub(r"(\n?)(\b[1-9]\))", r"\n\n\2", text)

    # Ensure there is a space after the numerical indicator if it's not there
    text = re.sub(r"(\b[1-9]\))(\S)", r"\1 \2", text)

    # Handle cases like " - National Planning, ": Start on a new line with correct formatting
    text = re.sub(r"(\n?)( - [A-Z][a-z])", r"\n\n\2", text)

    return text.strip()

######____________________________________________
######____________________________________________



#####___________________________________________________________________________
#####___________________________________________________________________________
#####___________________________________________________________________________
#####___________________________________________________________________________
#####___________________________________________________________________________
##### TABLE WITH SECONDARY SOURCES OF INFORMATION: df_ind_countries_pledge_plan
#####___________________________________________________________________________
#####___________________________________________________________________________
#####___________________________________________________________________________
#####___________________________________________________________________________


# df_ind_countries_pledge_plan
#Cleaning Countries whit no info
mask = ~((df_ind_countries_pledge_plan['Ind_Pledge'].isin([0, np.nan])) & 
         (df_ind_countries_pledge_plan['Ind_Plan'].isin([0, np.nan])))

df_ind_countries_pledge_plan = df_ind_countries_pledge_plan[mask]

# Replace np.nan with "No Info" in 'Partners_Pledge' column
df_ind_countries_pledge_plan['Partners_Pledge'] = df_ind_countries_pledge_plan['Partners_Pledge'].fillna("None")

# Replace np.nan with "No Info" in 'Plans' column
df_ind_countries_pledge_plan['Plans'] = df_ind_countries_pledge_plan['Plans'].fillna("None")

#Rename Countries
df_ind_countries_pledge_plan['Country'] = df_ind_countries_pledge_plan['Country'].replace("Taiwan","Taiwan, Province of China").fillna('').astype(str)
df_ind_countries_pledge_plan['Country'] = df_ind_countries_pledge_plan['Country'].replace("United States","United States of America").fillna('').astype(str)

# Helper function to count words with length >= 2 (excluding ";")
def count_valid_words(text):
    return sum(1 for word in text.split() if len(word) >= 2 and word != "None" and word !=";")

# Applying the functions to the DataFrame
df_ind_countries_pledge_plan['Partners_Pledge_Count'] = df_ind_countries_pledge_plan['Partners_Pledge'].apply(count_valid_words)
df_ind_countries_pledge_plan['Partners_Plans_Count'] = df_ind_countries_pledge_plan['Plans'].apply(count_valid_words)

rename_plans = {'Plans': 'Partners_Plans','TB':'Total Population (2022)'}
df_ind_countries_pledge_plan = df_ind_countries_pledge_plan.rename(columns=rename_plans)

df_ind_countries_pledge_plan['%TP Pledge'] = (df_ind_countries_pledge_plan['Ind_Pledge'] / df_ind_countries_pledge_plan['Total Population (2022)']) * 100
df_ind_countries_pledge_plan['%TP Plan'] = (df_ind_countries_pledge_plan['Ind_Plan'] / df_ind_countries_pledge_plan['Total Population (2022)']) * 100
df_ind_countries_pledge_plan['dif'] = df_ind_countries_pledge_plan['%TP Pledge'] - df_ind_countries_pledge_plan['%TP Plan']


# Define a function to concatenate and remove duplicates
def concatenate_and_deduplicate(partners_pledge, partners_plans):
    # Combine the strings using ";" as the delimiter and split into words
    combined = partners_pledge + ";" + partners_plans
    words = combined.split(";")
    # Trim leading and trailing spaces from each word
    words = [word.strip() for word in words]
    # Remove duplicates by converting to a set and then back to a list
    unique_words = list(set(words))
    # Join the unique words back into a single string with ";" as the delimiter
    return '; '.join(unique_words)

# Apply the function to each row in the DataFrame
df_ind_countries_pledge_plan['Total Partners'] = df_ind_countries_pledge_plan.apply(lambda row: concatenate_and_deduplicate(row['Partners_Pledge'], row['Partners_Plans']), axis=1)

# Function to remove 'None' from the string
def remove_none(text):
    # Split the string by ';' and filter out 'None' and empty parts
    parts = [part.strip() for part in text.split(';') if part.strip().lower() != 'none']

    # Join the parts back together
    return '; '.join(parts)

# Apply the function to the 'Total Partners' column
df_ind_countries_pledge_plan['Total Partners'] = df_ind_countries_pledge_plan['Total Partners'].apply(remove_none)

df_ind_countries_pledge_plan['Total Partners_Counts']  = df_ind_countries_pledge_plan['Total Partners'].apply(count_valid_words)
order_countries_list =['Country','Total Partners', 'Total Partners_Counts', 'Total Population (2022)', 'Ind_Pledge','Partners_Pledge','Partners_Pledge_Count', 'Ind_Plan', 'Partners_Plans','Partners_Plans_Count','%TP Pledge','%TP Plan','dif']
df_ind_countries_pledge_plan = df_ind_countries_pledge_plan[order_countries_list]
# st.write(df_ind_countries_pledge_plan)
















#####__________________________________________________________________________________________________________________________________________________________________
#####__________________________________________________________________________________________________________________________________________________________________
#####_________________________________________________________________________________________________________________________________________________________________
#####  DATA CLEANING ### GENERAL INFORMATION SURVEY
#####__________________________________________________________________________________________________________________________________________________________________
#####__________________________________________________________________________________________________________________________________________________________________
#####__________________________________________________________________________________________________________________________________________________________________

### GENERAL INFORMATION SURVEY 2023

# st.markdown("# GENERAL INFORMATION SURVEY")

#Cleaning
#Renaming and excluding partners not longer part of the race
replacements = {
    "Climate-KIC Accelerator-international Innovation Clusters work (KIC-FRR)": "Climate Knowledge and Innovation Community (Climate-KIC)",
    "BFA Global (BFA)": "BFA Global/ CIFAR Alliance (BFA)",
    "Cities Race to Zero (Resilience) Coalition (CitiesR2R)": "Cities Race to Resilience (CitiesR2R)",
    "Global Fund for Coral Reef (GFCR)": "Global Fund for Coral Reefs (GFCR)",
    "United Nations Office for Disaster Risk Reduction - ARISE (Private Sector Alliance for Disaster Resilient Societies) (UN ARISE)": "ARISE - United Nations Office for Disaster Risk Reduction (UN ARISE)",
    "WBCSDs food & agriculture climate workstream (WBCSD)": "Agriculture 1.5 - WBCSD’s food & agriculture climate workstream (WBCSD)",
    "Sanitation and Water for All  (SWA)": "Sanitation and Water for All (SWA)",
    "Urban Sustainability Directors Network (USDN) Resilience Hubs (USDN)": "Urban Sustainability Directors Network (USDN)",
    "RegionsAdapt (Regions4)": "RegionsAdapt (RegionsAdapt)",
    'Efficiency for Access Coalition (EfoA)':'Efficiency for Access Coalition (EforA)',
    'Efficiency for Access Coalition':'Efficiency for Access Coalition (EforA)',
    'Just Rural Transition (JRT)':'Just Rural Transition',
    'Least Developed Countries Universities Consortium on Climate Change (LUCCC)':'Least Developed Countries Universities Consortium on Climate Change (LUCCC) (ICCCAD)',}
df_gi['q9'] = df_gi['q9'].replace(replacements)

rename_gi = {
    'q57':'confirmation_if_has_members_status',
    'q63':'n_members_official',
    'q21':'responder_gi',
    'q29':'responder_email_gi',
    }
df_gi = df_gi.rename(columns = rename_gi)

rename_df_gi = {'q9': 'InitName','q3':'enddate_gi'}
df_gi = df_gi.rename(columns=rename_df_gi)

#Merging Data with ID MASTER and making sure the data has all members name
df_gi = pd.merge(df_gi, df_partners_name, on='InitName', how='outer')

# st.markdown("Lista Nombres GI")
# st.write(len(df_gi['InitName']))
# st.write(df_gi[['InitName','Master ID','Org_Type']])

#Set index
df_gi.set_index('Master ID', inplace = True)
df_gi.index.names = ['Master ID']
# st.write(df_gi)
df_gi = df_gi.dropna(how = 'all')

#Replace "Please Complete", "Would you kindly confirm, please?", "Would you kindly confirm, please? ", and "" (empty string) with np.nan
df_gi = df_gi.replace(["Please Complete","Please Complete ","please@complete.com","Please@complete.com", "Would you kindly confirm, please?", "Would you kindly confirm, please? ", ""], np.nan)

#Additional step to ensure all blank spaces are also treated as np.nan
df_gi = df_gi.applymap(lambda x: np.nan if isinstance(x, str) and x.strip()=="" else x)
for col in df_gi.columns:
    df_gi[col] = df_gi[col].replace({"": np.nan, " ": np.nan})

#Treatment of "OTHERS" when providing the names
# use numpy where to replace 'Other' in Respondant column with OtherName values
# df['Respondant'] = np.where(df['Respondant'] == 'Other', df['OtherName'], df['Respondant'])

#Making a variable to indentify if the survey has been open or not. 
# Convert the date and time column to datetime data type
df_gi['enddate_gi'] = pd.to_datetime(df_gi['enddate_gi'], infer_datetime_format=True, errors='coerce')
last_survey_view_list = ['enddate_gi']
start_date = pd.to_datetime('07/08/2023 00:00:00', format='%m/%d/%Y %H:%M:%S', errors='coerce')
df_gi['survey_reviewed_gi'] = df_gi['enddate_gi'] >= start_date
#st.write(df_gi[last_survey_view_list+['InitName','survey_reviewed_gi']])

#Making a validation colum for thouse that have provided information about the repondant. 
contact_info_list_gi = ['responder_gi', 'responder_email_gi']
df_gi['respondent_validation_gi'] = df_gi[contact_info_list_gi].notna().all(axis=1)
# st.write(df_gi[contact_info_list_gi+['respondent_validation_gi']])


# st.write("#COUNTRIES TREATMENT")

# st.subheader("LOCATION OF HEADQUARTERS")
# st.caption("**Q4. Indicate the location of your initiative's headquarters. If none, write No HQ and move to the next question.**")
# partner_address= df_gi['q24'].count()
# partner_city= df_gi['q26'].count()
# partner_country= df_gi['q29'].count()
# st.caption("Q4. Total Answers. Address: "+str(partner_address)+"; City: "+str(partner_city)+"; Country: "+str(partner_country))


# _____________________________
# MAKING DATA SET FOR MAPS
# _____________________________

df_gi = df_gi.rename(columns={'q31': 'description_general'})
df_gi = df_gi.rename(columns={'q32': 'resilience_definition'})

rename_df_gi = {'q18': 'country_hq','q15':'city_hq','q33':'website'}
df_gi = df_gi.rename(columns=rename_df_gi)


df_gi['country_hq'] = df_gi['country_hq'].replace({
        'USA/SWITCHZERLAND ': 'United States of America',
        'USA': 'United States of America',
        'United States of America': 'United States of America',
        'United States': 'United States of America',
        'United Kingdom': 'United Kingdom',
        'U.K': 'United Kingdom',
        'The United States of America': 'United States of America',
        'Switzerland': 'Switzerland',
        'South Africa': 'South Africa',
        'No HQ':'',
        'Italy': 'Italy',
        'Germany': 'Germany',
        'Belgique': 'Belgium',
        'Australia ': 'Australia',
        })

df_gi['city_hq'] = df_gi['city_hq'].replace({
    'Washington, DC 20005':'Washington DC',
    'Washington, DC':'Washington DC',
    'Washington DC':'Washington DC',
    'Sanford, NC ':'Sanford, NC',
    'Roma':'Rome',
    'Oakland':'Oakland',
    'No HQ':'',
    'New York / Geneva':'New York',
    'Melbourne ':'Melbourne',
    'London /Cardiff':'London /Cardiff',
    'London':'London',
    ' London ':'London',
    'Genève':'Geneva',
    'Geneva':'Geneva',
    'Denver':'Denver',
    'Cape Town':'Cape Town',
    'Brussels':'Brussels',
    'Bonn':'Bonn',
    'Berlin ':'Berlin',
        })


columns_list = ['city_hq', 'country_hq']

# Replace empty strings with np.nan in selected columns
df_gi[columns_list] = df_gi[columns_list].replace("", np.nan)

# Replace numbers with numbers followed by a parenthesis, but only if there's no existing parenthesis
df_gi['description_general'] = df_gi['description_general'].str.replace(r'(\d+)\.', lambda x: f'{x.group(1)})' if int(x.group(1)) < 10 else x.group(0), regex=True)

# Apply the function clean_text in the data frame to your DataFrame
# 'description_general' is the self description of the initiative
df_gi['description_general'] = df_gi['description_general'].apply(clean_text)

# Display the cleaned text to confirm
# st.markdown(df_gi['description_general'].iloc[0])
# st.markdown(df_gi['description_general'].iloc[6])
# st.markdown(df_gi['description_general'].iloc[9])
# st.markdown(df_gi['description_general'].iloc[12])






###_______________________________________________________________________
###_______________________________________________________________________
###_______________________________________________________________________
### GI COMPLETENESS INDEX:  IT SHOWS THE % OF COMPLETNESS OF THE SURVEY
###_______________________________________________________________________
###_______________________________________________________________________
###_______________________________________________________________________


## Partners GI General Information Sub Index  partner_info_gi_subidx
# Initiative Information: In this section, we ask you to provide general information about the initiative that you represent as an RtR Partner.
description_list = ['description_general','country_hq','city_hq','website']
df_gi['descrip_n_location_gi_status'] = df_gi[description_list].notna().all(axis=1)
# st.write(df_gi[description_list + ['descrip_n_location_gi_status']])

# priority_groups_gi_question = ["Do the actions of your initiative related to RtR target any of these priority groups?"]
priority_g_list = ['q35', 'q36', 'q37', 'q38', 'q39', 'q40', 'q41', 'q42', 'q43','q44']
priority_g_list_to_partner_finder =  ['q35', 'q36', 'q37', 'q38', 'q39', 'q40', 'q41', 'q42', 'q43']

df_gi['priority_groups_gi_status'] = df_gi[priority_g_list].notna().any(axis=1)
# st.write(df_gi[priority_g_list + ['priority_groups_gi_status']])

df_gi['priority_groups_gi_concat'] = df_gi[priority_g_list_to_partner_finder].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_gi['priority_groups_gi_concat'] = df_gi.apply(lambda row: row['priority_groups_gi_concat'] + '; Other' if pd.notna(row['q43']) else row['priority_groups_gi_concat'], axis=1)
df_gi['priority_groups_gi_concat'] = df_gi['priority_groups_gi_concat'].apply(lambda x: "Other" if x == "; Other" else x)
# st.write(df_gi[priority_g_list + ['priority_groups_gi_concat','priority_groups_gi_status']])

regions_list= ['q46', 'q47', 'q48', 'q49', 'q50', 'q51', 'q52', 'q53', 'q54', 'q55','q56']
df_gi['regions_gi_status'] = df_gi[regions_list].notna().any(axis=1)
# st.write(df_gi[regions_list + ['regions_gi_status']])


#Making the SubIndex partner_info_gi_subidx
partner_info_gi_subidx_list = ['descrip_n_location_gi_status', 'priority_groups_gi_status','regions_gi_status']

weights = {
    'descrip_n_location_gi_status':0.45,
    'priority_groups_gi_status':0.45,
    'regions_gi_status':0.1,
    }
# Calculate the weighted sum of the components for partner_info_gi_subidx
df_gi['partner_info_gi_subidx'] = df_gi.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_gi['partner_info_gi_subidx'] = (df_gi['partner_info_gi_subidx'] * 100).astype(int)


## Indentifying info required
index_list = partner_info_gi_subidx_list
# Apply the function to each row
df_gi['partner_info_gi_req'] = df_gi.apply(identify_req_status, axis=1)


# Summary List partner_info_gi_all_list
partner_info_gi_responses_list = ['resilience_definition','priority_groups_gi_concat']
partner_info_gi_results_list  = ['partner_info_gi_subidx','partner_info_gi_req',]           
partner_info_gi_subidx_list = partner_info_gi_subidx_list
partner_info_gi_all_list = partner_info_gi_responses_list + partner_info_gi_results_list + partner_info_gi_subidx_list
  ##
##  ##
 ##
## Confirm results sub index partner_info_gi_subidx
# st.write('Partners Information',df_gi[['InitName']+partner_info_gi_all_list])



##______________________________________
##______________________________________
##______________________________________
##____  MEMBERS IN GENERAL INFORMATION
##______________________________________
##______________________________________
##______________________________________



## Adding Info Members 2022 for GI Confidence analysis. 
#Combining Data Set with Member information 2022
df_members2022 = df_2022_pledge[['s9','MembersCount2022']]
rename_member2022 = {'s9': 'InitName', 'MembersCount2022': 'members2022total'}
df_members2022 = df_members2022.rename(columns=rename_member2022)
# st.write('members2022')
# st.write(df_members2022)

# Merging datasets # Data Members 2022
df_gi = pd.merge(df_gi, df_members2022, on='InitName', how='outer')

# Merging datasets # Data Responses Reviewed
df_gi = pd.merge(df_gi, df_responses_evaluated, on='InitName', how='outer')


## CONFIRMATION OF MEMBERS INFORMATION INDEXES

# Members Information: In this segment, we request details about your members. These members could be implementers, collaborators (partner organizations), endorsers, or donors - entities that directly contribute to the pledge, plan, and resilience actions reported by your initiative to the campaign. These entities have also given their consent to be associated with the RtR through the partner initiative. For this section, a template will be provided for you to report detailed information about members.
df_gi['members_type_gi_status_all'] = df_gi['q59'].astype(str) + ' ' + df_gi['q60'].astype(str) + ' ' + df_gi['q61'].astype(str)+ ' ' + df_gi['q62'].astype(str)


# st.write("## MEMBERS GI")
# df_gi['members_type_gi_status_all'] 


# st.write("df_gi['members_evaluation']") ## REVISAR NO ENCUENTRO LA VARIABLE. 
# df_gi['members_evaluation']


## member_confirmation_gi_status_list   #works
member_confirmation_gi_status_list = ['confirmation_if_has_members_status']
df_gi['member_confirmation_gi_status'] = df_gi[member_confirmation_gi_status_list].notna().all(axis=1)
df_gi.loc[df_gi['confirmation_if_has_members_status'] == "Unsure (please specify)", 'confirmation_if_has_members_status'] = "Unsure"
df_gi.loc[(df_gi['confirmation_if_has_members_status'] == "Unsure"), 'member_confirmation_gi_status'] = False
df_gi.loc[(df_gi['survey_reviewed_gi'] == False), 'member_confirmation_gi_status'] = False


# st.write("member_confirmation_gi_status_list ## ANTES",df_gi[member_confirmation_gi_status_list+['InitName', 'member_confirmation_gi_status']])

##adjudment prefilling gap. 
df_gi.loc[(df_gi['partner_info_gi_subidx'] == 0), 'confirmation_if_has_members_status'] = False

# st.write("member_confirmation_gi_status_list ## DESPUES",df_gi[member_confirmation_gi_status_list+['InitName', 'member_confirmation_gi_status']])

## members_type_gi_status #works
members_type_gi_status_list = ['q59','q60',	'q61','q62']
df_gi['members_type_gi_status'] = df_gi[members_type_gi_status_list].notna().any(axis=1)
# st.write(df_gi[members_type_gi_status_list+['members_type_gi_status']])
df_gi.loc[(df_gi['confirmation_if_has_members_status'] == "No"), 'members_type_gi_status'] = True

replace_dict = {
    "Implementer: An organization that carries out resilience activities on the ground.": "Implementer",
    "Collaborator/Partner Organization: Supports the initiative's operations without implementing actions on the ground.": "Collaborator/Partner Organization",
    "Endorser: Provides other types of support.": "Endorser",
    "Donor: Funds the initiative.": "Donor",
}
# Iterate through the columns in members_type_gi_status_list and apply the replacements
for col in members_type_gi_status_list:
    df_gi[col] = df_gi[col].replace(replace_dict)   
# st.write('## members_type_gi_status',df_gi[['confirmation_if_has_members_status']+members_type_gi_status_list+['members_type_gi_status']])

## members_general_info_gi  ## works
members_text_data = ['q65', 'q66','q67']
df_gi[members_text_data] = df_gi[members_text_data].applymap(lambda x: np.nan if len(str(x)) < 7 else x)

members_general_info_gi_status_list = ['q64','q65','q66','q67',]
df_gi['members_general_info_gi_status'] = df_gi[members_general_info_gi_status_list].notna().all(axis=1)    
df_gi.loc[(df_gi['confirmation_if_has_members_status'] == "No"), 'members_general_info_gi_status'] = True

# st.write('## members_general_info_gi_status_list',df_gi[['confirmation_if_has_members_status']+members_general_info_gi_status_list+['members_general_info_gi_status']])


## 'Members_n_reported_gi_status' ## works
members_numbers_list = ['n_members_official']
df_gi['n_members_official'] = df_gi['n_members_official'].replace('0', np.nan)
df_gi['members_n_reported_gi_status'] = df_gi[members_numbers_list ].notna().all(axis=1)
df_gi.loc[(df_gi['confirmation_if_has_members_status'] == "No"), 'members_n_reported_gi_status'] = True
# st.write(df_gi[['n_members_official','members_n_reported_gi_status']])
# st.write('## Members_n_reported_gi_status', df_gi[members_numbers_list+['InitName','members_n_reported_gi_status']]) 


## 'members_data_upload_gi_status'
list_to_no_answer = ["We have not collected consent from our members to be associated with the RTR through the GMA. In the future we could consider promoting RTR among our members as reporting on resilience outcomes become clearer."]
df_gi.loc[df_gi['q69'].isin(list_to_no_answer), 'q69'] = np.nan

members_data_upload_gi_status_list = ['q68','q69']
df_gi['members_data_upload_gi_status'] = df_gi[members_data_upload_gi_status_list].notna().any(axis=1)
df_gi.loc[(df_gi['confirmation_if_has_members_status'] == "No"), 'members_data_upload_gi_status'] = True

# st.write('## members_data_upload_gi_status')
# df_gi[['confirmation_if_has_members_status']+members_data_upload_gi_status_list+['members_data_upload_gi_status']]


## Making subindex members_info_gi_subidx
members_info_gi_subidx_list = ['member_confirmation_gi_status', 
                               'members_type_gi_status',
                               'members_general_info_gi_status',
                               'members_n_reported_gi_status',
                               'members_data_upload_gi_status']

weights = {
    'member_confirmation_gi_status': 0.05,
    'members_type_gi_status': 0.05,
    'members_general_info_gi_status': 0.1,
    'members_n_reported_gi_status': 0.4,
    'members_data_upload_gi_status': 0.4,
}

df_gi['members_info_gi_subidx'] = df_gi.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items()), 
    axis=1
)


# Convert the result to a percentage and then to an integer
df_gi['members_info_gi_subidx'] = (df_gi['members_info_gi_subidx'] * 100).astype(int)
df_gi.loc[(df_gi['confirmation_if_has_members_status'] == "No"), 'members_info_gi_subidx'] = 100
# df_gi[['members_info_gi_subidx']+members_info_gi_subidx_list]


## Indentifying info required
index_list = members_info_gi_subidx_list
# Apply the function to each row
df_gi['members_info_gi_req'] = df_gi.apply(identify_req_status, axis=1)
df_gi.loc[(df_gi['confirmation_if_has_members_status'] == "No"), 'members_info_gi_req'] = ""

# st.write("Pre")
# df_gi['Org_Type']






##
## Confidence in GI Analisis 2024
##

## Two variables are needed here: If they have members as "yes", then they need to provide information abut the numbers of members and upload info. Based on that the confidence index will be done. 

# confidence_n_members_status

## Number of Members Available? #WORKS
members_variables_list = ['n_members_official']
# Replace NaN with 0 in the columns before addition
for column in members_variables_list:
     df_gi[column].fillna(0, inplace=True)

n_members_accepted = "Accepted: Number of members available"
n_members_accepted_nomembers = "Accepted: Does not have Members"
n_members_not_accepted = "Not Accepted: No number of members reported"
n_members_not_accepted_unsure =  "Not Accepted. They are unsure. Need help to confirm the status of their members."

df_gi['n_members_official'] = pd.to_numeric(df_gi['n_members_official'], errors='coerce')
df_gi.loc[df_gi['n_members_official'] > 0, 'confidence_n_members_status'] = n_members_accepted
df_gi.loc[df_gi['n_members_official'] == 0, 'confidence_n_members_status'] = n_members_not_accepted 
df_gi.loc[(df_gi['confirmation_if_has_members_status'] == "No"), 'confidence_n_members_status'] = n_members_accepted_nomembers
df_gi.loc[(df_gi['confirmation_if_has_members_status'] == "Unsure"), 'confidence_n_members_status'] = n_members_not_accepted_unsure

# st.write('## Number of Members Available?',df_gi[['confirmation_if_has_members_status','confidence_n_members_status']])

# confidence_members_uploaded_file_status
members_upload_accepted = "Accepted. Members Upload Data Available"
members_upload_accepted_nomembers = "Accepted: Does not have Members"
members_upload_no_accepted = "Not Accepted. Upload Data of Members Missing"
members_upload_no_accepted_unsure = "Not Accepted. They are unsure. Need help to confirm the status of their members"

# Use the syntax for conditions and assignments
df_gi['confidence_members_uploaded_file_status'] = df_gi['members_data_upload_gi_status'].apply(
    lambda x: members_upload_accepted if x else members_upload_no_accepted
)
df_gi.loc[(df_gi['confirmation_if_has_members_status'] == "Unsure"), 'confidence_members_uploaded_file_status'] = members_upload_no_accepted_unsure
df_gi.loc[(df_gi['confirmation_if_has_members_status'] == "No"), 'confidence_members_uploaded_file_status'] = members_upload_accepted_nomembers

# df_gi[['confirmation_if_has_members_status','confidence_n_members_status','confidence_members_uploaded_file_status']]


## Results
high_reliability_members_info = "High. Members Information Available."
high_reliability_not_has_members = "High. It Has No Members."
medium_reliability_missing_upload_member_data = "Medium. Member Data Upload Not Available."
medium_reliability_missing_n_members = "Medium. Number of Members Not Available."
low_reliability_members_unsure = "Low. Unsure about having Members (No Data Available)."
low_reliability_no_members_any_data= "Very Low. No information about Members Received."

## High Reliability
df_gi.loc[
    (df_gi['confidence_n_members_status'] == n_members_accepted) &
    (df_gi['confidence_members_uploaded_file_status'] == members_upload_accepted),
    'confidence_members_overall_gi_status'
] = high_reliability_members_info


df_gi.loc[
    (df_gi['confidence_n_members_status'] == n_members_accepted_nomembers ) &
    (df_gi['confidence_members_uploaded_file_status'] == members_upload_accepted_nomembers),
    'confidence_members_overall_gi_status'
] = high_reliability_not_has_members


## Medium Reliability
df_gi.loc[
    (df_gi['confidence_n_members_status'] == n_members_accepted ) &
    (df_gi['confidence_members_uploaded_file_status'] == members_upload_no_accepted),
    'confidence_members_overall_gi_status'
] = medium_reliability_missing_upload_member_data


df_gi.loc[
    (df_gi['confidence_n_members_status'] == n_members_not_accepted ) &
    (df_gi['confidence_members_uploaded_file_status'] == members_upload_accepted),
    'confidence_members_overall_gi_status'
] = medium_reliability_missing_n_members


## Low
df_gi.loc[
    (df_gi['confidence_n_members_status'] == n_members_not_accepted ) &
    (df_gi['confidence_members_uploaded_file_status'] == members_upload_no_accepted),
    'confidence_members_overall_gi_status'
] = low_reliability_no_members_any_data


## Low
df_gi.loc[
    (df_gi['confidence_n_members_status'] == n_members_not_accepted_unsure ) &
    (df_gi['confidence_members_uploaded_file_status'] == members_upload_no_accepted_unsure),
    'confidence_members_overall_gi_status'
] = low_reliability_members_unsure

conditions_dictionary_gi_members_overall_idx_list ={
    high_reliability_members_info : 2/2,   #100
    high_reliability_not_has_members : 2/2, #100
    medium_reliability_missing_upload_member_data : 1/2, #50
    medium_reliability_missing_n_members : 1/2, #50
    low_reliability_no_members_any_data : 0/2, #0
    low_reliability_members_unsure : 0.5/2,} #25
df_gi['gi_confidence_members_overall_idx'] = df_gi['confidence_members_overall_gi_status'].map(conditions_dictionary_gi_members_overall_idx_list)

confidence_gi_responses_list = ['n_members_official','gi_confidence_members_overall_idx','confidence_members_overall_gi_status','confidence_n_members_status','confidence_members_uploaded_file_status']
# st.write('confidence_gi_responses_list')
# df_gi[confidence_gi_responses_list]


# Official list of Variables for Members information in GI
members_info_gi_responses_list = member_confirmation_gi_status_list
members_info_gi_results_list  = ['members_info_gi_subidx','members_info_gi_req',]           
members_info_gi_subidx_list = members_info_gi_subidx_list
members_info_gi_all_list = members_info_gi_responses_list + members_info_gi_results_list + members_info_gi_subidx_list
  ##
##  ##
 ##
# st.write("Members Info",df_gi[['InitName']+confidence_gi_responses_list+ members_info_gi_all_list])

relibility_gi_text = """
The Confidence GI Survey, identified by the variable `confidence_members_22_23_dif_status`, primarily focuses on responses regarding Members. Effective reporting should include information about members, as the core information relies on partners and their members. If there is insufficient knowledge about them, the reliability of the reported data is compromised.
"""
# st.markdown(relibility_gi_text)


##ATENTION. WHEN BY DEFAULT RESPONSE IS UNSURE (Bug after pre-filling data 2022 en reporting tools 2023). 
# Adjustement is done at the after the  




# ## ______________________________________________________________________________
## ______________________________________________________________________________
## ______________________________________________________________________________
## METRICS STRATEGIES, DATA VALIDATION AND TRACKIG IN GENERAL INFORMATION SURVEY
## ______________________________________________________________________________
## ______________________________________________________________________________
## ______________________________________________________________________________

# q69	Q17 [METRICS] How do you approach tracking progress, collecting data, and utilising your organisation's metrics to evaluate your member organisation's performance? Please include methods, processes and type of data/analysis that you actually use to obtain information about your work on the ground.
# q71	Q19 [DATA VALIDATION] How do you verify the accuracy and reliability of the data you receive from your member organisations?

rename_gi = {
    'q70':'tracking_collecting_data_how',
    'q72':'data_validation_how',
    }
df_gi = df_gi.rename(columns = rename_gi)
metrics_list = ['tracking_collecting_data_how','data_validation_how']

df_gi['metrics_info_gi_status'] = df_gi[metrics_list ].notna().all(axis=1)
# st.write(df_gi[metrics_list +['InitName','metrics_info_gi_status']]) 

metrics_upload_list = ['q71','q73','q75','q76']
df_gi['metrics_upload_file_gi_status'] = df_gi[metrics_upload_list].notna().any(axis=1)
# st.write(df_gi[metrics_upload_list +['InitName','metrics_upload_file_gi_status']]) 

## Making subindex metrics_gi_subidx
metrics_index_list = ['metrics_info_gi_status','metrics_upload_file_gi_status']

weights = {
    'metrics_info_gi_status': 0.91,
    'metrics_upload_file_gi_status': 0.09,
}

df_gi['metrics_gi_subidx'] = df_gi.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items()), 
    axis=1
)

# Convert the result to a percentage and then to an integer
df_gi['metrics_gi_subidx'] = (df_gi['metrics_gi_subidx'] * 100).astype(int)
# df_gi[['metrics_gi_subidx']+metrics_index_list]

## Indentifying info required
index_list = metrics_index_list
# Apply the function to each row
df_gi['metrics_gi_req'] = df_gi.apply(identify_req_status, axis=1)


# Official list of Variables for Members information in GI
metrics_info_gi_responses_list = metrics_list
metrics_info_gi_results_list  = ['metrics_gi_subidx','metrics_gi_req',]    
metrics_info_gi_subidx_list = metrics_index_list
metrics_info_gi_all_list = metrics_info_gi_responses_list + metrics_info_gi_results_list + metrics_info_gi_subidx_list
  ##
##  ##
 ##
# st.write("Metrics Info",df_gi[['InitName']+metrics_info_gi_all_list])



##_____________________________________________
##_____________________________________________
##_____________________________________________
##_____________________________________________
## Sharm-El-Sheikh Adaptation Agenda (SAA) 
##_____________________________________________
##_____________________________________________
##_____________________________________________
##_____________________________________________

# Sharm-El-Sheikh Adaptation Agenda (SAA) Impact Systems & Cross-Cutting Enablers: This part is dedicated to your involvement in the SAA Impact Systems and any associated cross-cutting enablers.
df_gi['q136'] = df_gi['q136'].replace('Not Sure', "Unsure")
df_gi['q136'] = df_gi['q136'].replace('No', "Not Related")
df_gi['q136'] = df_gi['q136'].replace('Yes', "Directly related")

foodandagriculturesystems = ['q77']
waterandnaturalsystems = ['q86']
humansettlementssystems = ['q99']
coastalandoceanicsystems = ['q112']
insfraestructuresystems = ['q123']
healthsystems = ['q136']
planing_crosscutting = ['q138']
finance_crosscutting = ['q148']    
all_saa_list = ['q77','q86','q99','q112','q123','q136','q138','q148']


df_gi['Food and Agriculture'] = df_gi['q77'].apply(lambda x: 'Food and Agriculture' if x in ["Indirectly related", "Directly related"] else None)
df_gi['Water and Nature'] = df_gi['q86'].apply(lambda x: 'Water and Nature' if x in ["Indirectly related", "Directly related"] else None)
df_gi['Human Settlements'] = df_gi['q99'].apply(lambda x: 'Human Settlements' if x in ["Indirectly related", "Directly related"] else None)
df_gi['Coastal and Oceans'] = df_gi['q112'].apply(lambda x: 'Coastal and Oceans' if x in ["Indirectly related", "Directly related"] else None)
df_gi['Infrastructure'] = df_gi['q123'].apply(lambda x: 'Infrastructure' if x in ["Indirectly related", "Directly related"] else None)
df_gi['Health'] = df_gi['q136'].apply(lambda x: 'Health' if x in ["Indirectly related", "Directly related"] else None)
df_gi['Planning and Policy: Cross-cutting'] = df_gi['q138'].apply(lambda x: 'Planning and Policy: Cross-cutting' if x in ["Indirectly related", "Directly related"] else None)
df_gi['Finance: Cross-cutting'] = df_gi['q148'].apply(lambda x: 'Finance: Cross-cutting' if x in ["Indirectly related", "Directly related"] else None)

priority_systems_list = ['Food and Agriculture','Health','Human Settlements','Coastal and Oceans','Infrastructure','Water and Nature','Planning and Policy: Cross-cutting','Finance: Cross-cutting']
df_gi['saa_p_systems_gi_concat']  =  df_gi[priority_systems_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_gi['count_saa_p_systems'] = df_gi['saa_p_systems_gi_concat'].apply(lambda x: len(x.split(';')) if x else 0)

##Cleaning Health Priority System because it does not have outcometargets
df_gi.loc[df_gi['Health'] != "Health", 'q137'] = np.nan
# df_gi[['Health','q137']]

## Making saa_responded_gi_status. It indicates if the main question about SAA has been responded. 
# Set 'saa_confirmation' to True by default
df_gi['saa_responded_gi_status'] = True
# Create a temporary DataFrame where 'Unsure' is replaced by NaN
temp_df = df_gi[all_saa_list].replace('Unsure', np.nan)

# If all values in a row of the temporary DataFrame are NaN, set the corresponding 'saa_confirmation' to False
df_gi.loc[temp_df.isna().all(axis=1), 'saa_responded_gi_status'] = False

# Additionally, if 'survey_reviewed' is False, set 'saa_confirmation' to False as well
df_gi.loc[df_gi['survey_reviewed_gi'] == False, 'saa_responded_gi_status'] = False
# st.write(df_gi[all_saa_list+['InitName', 'saa_responded_gi_status']])

## Making the outcome target list reporting to SAA
foodandagriculturesystems_out_target_list = ['q79','q80','q81','q82']
waterandnaturalsystems_out_target_list = ['q88','q89','q90','q91','q92','q93']
humansettlementssystems_out_target_list = ['q101','q102','q103','q104','q105']
coastalandoceanicsystems_out_target_list = ['q114','q115','q116','q117','q118']
insfraestructuresystems_out_target_list = ['q125','q126','q127','q128','q129','q130']
healthsystems_out_target_list = ['q137',] ## ADD HERE FUTURE OUTCOMETARGETS
planing_crosscutting_out_target_list = ['q140','q141','q142','q143',] 
finance_crosscutting_out_target_list = ['q150','q151','q152','q153']    


##Optional Questions about they connect to the Priority System. 
foodandagriculturesystems_how_list = ['q78',]
waterandnaturalsystems_how_list = ['q87',]
humansettlementssystems_how_list = ['q100',]
coastalandoceanicsystems_how_list = ['q113',]
insfraestructuresystems_how_list = ['q124',]
healthsystems_how_list = ['q137',]
planing_crosscutting_how_list = ['q139',]
finance_crosscutting_how_list = ['q149',]

taskforce_how_saa_list = foodandagriculturesystems_how_list + waterandnaturalsystems_how_list + humansettlementssystems_how_list + coastalandoceanicsystems_how_list + insfraestructuresystems_how_list + healthsystems_how_list + planing_crosscutting_how_list + finance_crosscutting_how_list
#clening not enough responses about the description of how connect to SAA taskforces
df_gi[taskforce_how_saa_list] = df_gi[taskforce_how_saa_list].replace(['bla bla', ""], np.nan)


df_gi['foodandagriculture_outtarg_status'] = df_gi[foodandagriculturesystems_out_target_list].any(axis=1)
df_gi['waterandnatural_outtarg_status'] = df_gi[waterandnaturalsystems_out_target_list].any(axis=1)
df_gi['humansettlements_outtarg_status'] = df_gi[humansettlementssystems_out_target_list].any(axis=1)
df_gi['coastalandoceanic_outtarg_status'] = df_gi[coastalandoceanicsystems_out_target_list].any(axis=1)
df_gi['insfraestructure_outtarg_status'] = df_gi[insfraestructuresystems_out_target_list].any(axis=1)
df_gi['health_outtarg_status'] = df_gi[healthsystems_out_target_list].any(axis=1)
df_gi['planing_cross_outtarg_status'] = df_gi[planing_crosscutting_out_target_list].any(axis=1)
df_gi['finance_cross_outtarg_status']= df_gi[finance_crosscutting_out_target_list].any(axis=1)

# df_gi['foodandagriculture_how_status'] = df_gi[foodandagriculturesystems_how_list].any(axis=1) 
# df_gi['waterandnatural_how_status'] = df_gi[waterandnaturalsystems_how_list].any(axis=1)
# df_gi['humansettlement_how_status'] = df_gi[humansettlementssystems_how_list].any(axis=1)
# df_gi['coastalandoceanic_how_status'] = df_gi[coastalandoceanicsystems_how_list].any(axis=1)
# df_gi['insfraestructure_how_status'] = df_gi[insfraestructuresystems_how_list].any(axis=1)
# df_gi['health_how_status'] = df_gi[healthsystems_how_list].any(axis=1)
# df_gi['planing_cross_how_status'] = df_gi[planing_crosscutting_how_list].any(axis=1)
# df_gi['finance_cross_how_status'] = df_gi[finance_crosscutting_how_list].any(axis=1)

priority_systems_list = ['Food and Agriculture','Health','Human Settlements','Coastal and Oceans','Infrastructure','Water and Nature','Planning and Policy: Cross-cutting','Finance: Cross-cutting']

foodandagriculturesystems_to_subidx_list = ['foodandagriculture_outtarg_status',]
waterandnaturalsystems_to_subidx_list = ['waterandnatural_outtarg_status',]
humansettlementssystems_to_subidx_list = ['humansettlements_outtarg_status',]
coastalandoceanicsystems_to_subidx_list = ['coastalandoceanic_outtarg_status',]
insfraestructuresystems_to_subidx_list = ['insfraestructure_outtarg_status',]
healthsystems_to_subidx_list = ['health_outtarg_status',]
planing_crosscutting_to_subidx_list = ['planing_cross_outtarg_status',]
finance_crosscutting_to_subidx_list = ['finance_cross_outtarg_status',] 

## I took off the "the how" because it is optional
# foodandagriculturesystems_to_subidx_list = ['foodandagriculture_outtarg_status','foodandagriculture_how_status']
# waterandnaturalsystems_to_subidx_list = ['waterandnatural_outtarg_status','waterandnatural_how_status']
# humansettlementssystems_to_subidx_list = ['humansettlements_outtarg_status','humansettlement_how_status']
# coastalandoceanicsystems_to_subidx_list = ['coastalandoceanic_outtarg_status','coastalandoceanic_how_status']
# insfraestructuresystems_to_subidx_list = ['insfraestructure_outtarg_status','insfraestructure_how_status']
# healthsystems_to_subidx_list = ['health_outtarg_status','health_how_status']
# planing_crosscutting_to_subidx_list = ['planing_cross_outtarg_status','planing_cross_how_status']
# finance_crosscutting_to_subidx_list = ['finance_cross_outtarg_status','finance_cross_how_status'] 

df_gi['foodandagriculture_sub_subidx'] = (df_gi[foodandagriculturesystems_to_subidx_list].mean(axis=1) * 100).astype(int)
df_gi['waterandnatural_sub_subidx'] = (df_gi[waterandnaturalsystems_to_subidx_list].mean(axis=1) * 100).astype(int)
df_gi['humansettlements_sub_subidx'] = (df_gi[humansettlementssystems_to_subidx_list].mean(axis=1) * 100).astype(int)
df_gi['coastalandoceanic_sub_subidx'] = (df_gi[coastalandoceanicsystems_to_subidx_list].mean(axis=1) * 100).astype(int)
df_gi['insfraestructure_sub_subidx'] = (df_gi[insfraestructuresystems_to_subidx_list].mean(axis=1) * 100).astype(int)
df_gi['health_sub_subidx'] = (df_gi[healthsystems_to_subidx_list].mean(axis=1) * 100).astype(int)
df_gi['planing_cross_sub_subidx'] = (df_gi[planing_crosscutting_to_subidx_list].mean(axis=1) * 100).astype(int)
df_gi['finance_cross_sub_subidx'] = (df_gi[finance_crosscutting_to_subidx_list].mean(axis=1) * 100).astype(int)


#Sharm-El-Sheikh Adaptation Agenda (SAA) SAA SUB INDEX saa_gi_subidx
saa_gi_to_index = ['foodandagriculture_sub_subidx','waterandnatural_sub_subidx','humansettlements_sub_subidx','coastalandoceanic_sub_subidx',
                   'insfraestructure_sub_subidx','health_sub_subidx','planing_cross_sub_subidx','finance_cross_sub_subidx']

#There are differences between declared y reported. In the first case it might not conicide where there is actually information reported. 
df_gi['count_saa_p_systems'] = df_gi[saa_gi_to_index].apply(lambda x: (x > 0).sum(), axis=1)
df_gi['saa_gi_subidx'] = df_gi[saa_gi_to_index].sum(axis=1) / df_gi['count_saa_p_systems']

## adjustment when there is Zero priority system reported
if df_gi['saa_gi_subidx'].isnull().any():
    df_gi.loc[df_gi['saa_gi_subidx'].isnull(), 'saa_gi_subidx'] = 0


# st.write('asdasdasd saa_gi_subidx', df_gi[['InitName','saa_gi_subidx','count_saa_p_systems']+saa_gi_to_index])

priority_systems_list = ['Food and Agriculture','Health','Human Settlements','Coastal and Oceans','Infrastructure','Water and Nature','Planning and Policy: Cross-cutting','Finance: Cross-cutting']

saa_gi_to_index = ['foodandagriculture_sub_subidx','waterandnatural_sub_subidx','humansettlements_sub_subidx','coastalandoceanic_sub_subidx',
                   'insfraestructure_sub_subidx','health_sub_subidx','planing_cross_sub_subidx','finance_cross_sub_subidx']

relations = {
'Food and Agriculture':'foodandagriculture_sub_subidx',
'Health':'health_sub_subidx',
'Human Settlements':'humansettlements_sub_subidx',
'Coastal and Oceans':'coastalandoceanic_sub_subidx',
'Infrastructure':'insfraestructure_sub_subidx',
'Water and Nature':'waterandnatural_sub_subidx',
'Planning and Policy: Cross-cutting':'planing_cross_sub_subidx',
'Finance: Cross-cutting':'finance_cross_sub_subidx'
}


# Function to identify required SAA GI sub-indices
def identify_req_saa_gi(row):
    pending_items = []
    for key, value in relations.items():
        if pd.notna(row[key]) and row[key] != 0:  # Check if the 'key' column has information
            if row[value] < 90:  # Check the related 'value' column under specific condition
                pending_items.append(value)
    return ";".join(pending_items)

# Apply the function to each row to create the 'saa_gi_req' column
df_gi['saa_gi_req'] = df_gi.apply(identify_req_saa_gi, axis=1)


# Official list of Variables for SAA information in GI
saa_gi_responses_list = ['count_saa_p_systems','saa_p_systems_gi_concat']
saa_gi_results_list  = ['saa_gi_subidx','saa_gi_req']
saa_gi_to_index = saa_gi_to_index
saa_gi_all_list = saa_gi_responses_list + saa_gi_results_list + saa_gi_to_index
  ##
##  ##
 ##
# st.write("SAA Info",df_gi[['InitName']+saa_gi_all_list])

##_______________________
##_______________________
##_______________________
##____ ACTION CLUSTERS___
##_______________________
##_______________________
##_______________________

resilience_actions_cluster_list = [
     'q158', 'q159', 'q160', 'q161', 'q162', 'q163', 'q164',
    'q165', 'q166', 'q167', 'q168', 'q169', 'q170', 'q171', 'q172',
    'q173', 'q174', 'q175', 'q176', 'q177', 'q178', 'q179', 'q180',
    'q181', 'q182', 'q183', 'q184', 'q185','q186',
]

# Dictionary mapping full descriptions to simplified descriptions
simplified_descriptions = {
    'q158': 'Monitoring and mapping of hazards and vulnerabilities',
    'q159': 'Climate services and modelling',
    'q160': 'Generation and processing of data',
    'q161': 'Early warning systems',
    'q162': 'Emergency preparedness',
    'q163': 'Environmental governance and resource management systems',
    'q164': 'Environmental laws and regulatory framework',
    'q165': 'Building regulations and standards for climate resilience',
    'q166': 'Protected areas and property rights definitions',
    'q167': 'Institutional-led climate adaptation planning processes',
    'q168': 'Measures to improve air quality and reduce pollution',
    'q169': 'Green infrastructure and other engineered nature-based solutions',
    'q170': 'Conservation and restoration of terrestrial and aquatic ecosystems',
    'q171': 'Critical Infrastructure and Protective Systems',
    'q172': 'Coastal Infrastructure Protection',
    'q173': 'Energy efficiency and renewable energy technologies',
    'q174': 'Water security and quality',
    'q175': 'Health services',
    'q176': 'Food safety and sustainable services',
    'q177': 'Agricultural, livestock, forestry and aquiacultural practices actions',
    'q178': 'Social protection actions',
    'q179': 'Community-based inclusive and participatory risk reduction',
    'q180': 'Climate hazard communication, information, and technology awareness',
    'q181': 'Knowledge building for resilience',
    'q182': 'Research and collaboration actions',
    'q183': 'Livelihood diversification and social economy',
    'q184': 'Climate insurance and risk transfer',
    'q185': 'Financial and investment tools in case of climate disasters',
    'q186': 'Economic incentives',
}

# Apply the simplified descriptions to the DataFrame
for question_code, simplified_description in simplified_descriptions.items():
    df_gi[question_code] = df_gi[question_code].replace({
        f'{simplified_description} = .*': simplified_description
    }, regex=True)

# df_gi[resilience_actions_cluster_list]
df_gi['action_clusters_gi_status'] = df_gi[resilience_actions_cluster_list].any(axis=1)
df_gi['action_clusters_gi_count'] = df_gi[resilience_actions_cluster_list].apply(lambda x: pd.notna(x).sum(), axis=1)
df_gi['action_clusters_gi_concat']  =  df_gi[resilience_actions_cluster_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)

# Additionally, if 'survey_reviewed' is False, set 'action_clusters_gi_status' to False as well
df_gi.loc[df_gi['survey_reviewed_gi'] == False, 'action_clusters_gi_status'] = False

df_gi['action_clusterss_gi_subidx'] = df_gi['action_clusters_gi_status'].apply(lambda x: 100 if x else 0)
# st.write(df_gi[resilience_actions_cluster_list +['InitName', 'action_clusters_gi_status','action_clusterss_gi_subidx','survey_reviewed_gi']])

ac_gi_list = ['action_clusters_gi_status']
## Indentifying info required
index_list = ac_gi_list
# Apply the function to each row
df_gi['action_clusters_gi_req'] = df_gi.apply(identify_req_status, axis=1)

# ## Confirm results sub index action_clusterss_gi_subidx
# action_clusters_gi_subidx_summary = ['action_clusters_gi_concat','action_clusterss_gi_subidx','action_clusters_gi_req']+ac_gi_list
# # df_gi[action_clusters_gi_subidx_summary]

# Official list of Variables for Action Cluster information in GI
action_clusters_gi_responses_list = ['action_clusters_gi_concat','action_clusters_gi_count']
action_clusters_gi_results_list  = ['action_clusterss_gi_subidx','action_clusters_gi_req']
action_clusters_gi_to_index = ac_gi_list
action_clusters_gi_all_list = action_clusters_gi_responses_list + action_clusters_gi_results_list + action_clusters_gi_to_index
  ##
##  ##
 ##
# st.write("Action Cluster Info",df_gi[['InitName']+action_clusters_gi_all_list])

##________________________________
##________________________________
##________________________________
##______TYPE OF IMPACT____________
##________________________________
##________________________________
##________________________________


# Types of Impact: The final part seeks to understand if your initiative aims to have a clear and measurable effect on different beneficiaries.

rename_gi = {
    'q216':'type_of_impact',
    }
df_gi = df_gi.rename(columns = rename_gi)

direct_impact_list = ['type_of_impact']
df_gi['type_impact_gi_status'] = df_gi[direct_impact_list].notna().all(axis=1)
df_gi.loc[df_gi['survey_reviewed_gi'] == False, 'type_impact_gi_status'] = False
df_gi['type_impact_gi_subidx'] = df_gi['type_impact_gi_status'].apply(lambda x: 100 if x else 0)

## Indentifying info required
index_list = ['type_impact_gi_status']
# Apply the function to each row
df_gi['type_impact_gi_req'] = df_gi.apply(identify_req_status, axis=1)

# Official list of Variables for Type of Impact in GI
type_impact_gi_responses_list = direct_impact_list
type_impact_gi_results_list  = ['type_impact_gi_subidx','type_impact_gi_req']
type_impact_gi_to_index = index_list
type_impact_gi_all_list =  type_impact_gi_responses_list + type_impact_gi_results_list + type_impact_gi_to_index
  ##
##  ##
 ##
# st.write("Type of Impact Info",df_gi[['InitName']+type_impact_gi_all_list])





##______________________________________________________________________________________________________________
##______________________________________________________________________________________________________________
##______________________________________________________________________________________________________________
## Creating GENERAL INFORMATION COMPLETNESS INDEX Index gi_completness_idx
##______________________________________________________________________________________________________________
##______________________________________________________________________________________________________________
##______________________________________________________________________________________________________________

gi_survey_index_list = ['partner_info_gi_subidx',
                             'members_info_gi_subidx',
                             'metrics_gi_subidx',
                             'saa_gi_subidx',
                             'action_clusterss_gi_subidx',
                             'type_impact_gi_subidx']

weights = {
    'partner_info_gi_subidx': 0.083333333,
    'members_info_gi_subidx': 0.25,
    'metrics_gi_subidx': 0.083333333,
    'saa_gi_subidx': 0.25,
    'action_clusterss_gi_subidx': 0.25,
    'type_impact_gi_subidx': 0.083333333
}

# Calculate the weighted gi_completeness_idx
df_gi['gi_completeness_idx'] = sum(df_gi[col] * weight for col, weight in weights.items())

# #ADJUNTING VARIABLE "SURVEY REVIEW_GI"
df_gi.loc[df_gi['gi_completeness_idx'] ==0, 'survey_reviewed_gi'] = False
df_gi.loc[df_gi['gi_completeness_idx'] >0, 'survey_reviewed_gi'] = True




# st.write("## IMportantar GI")
# df_gi[['InitName','gi_completeness_idx']+gi_survey_index_list]


## 


#### GI Completeness Status order by Proirity gi_completeness_status and gi_completeness_req_priority
df_gi['gi_completeness_status'] = np.where(df_gi['gi_completeness_idx'] > 90, "Accepted", "Awaiting Completion")

required_gi_list_prioritized = ['members_info_gi_req',
                                'saa_gi_req',
                                'action_clusters_gi_req',
                                'metrics_gi_req',
                                'partner_info_gi_req',
                                'type_impact_gi_req']

df_gi['gi_completeness_req_priority'] = df_gi.apply(
    lambda row: '; '.join(filter(None, [str(row[col]) for col in required_gi_list_prioritized if pd.notnull(row[col])])), axis=1)

def concatenate_req_values_final_gi(row):
    pending_values = []
    # Check condition and concatenate the appropriate pending value
    if row['members_info_gi_subidx'] <= 90:
        pending_values.append(row['members_info_gi_req'])
    if row['saa_gi_subidx'] <= 90:
        pending_values.append(row['saa_gi_req'])
    if row['action_clusterss_gi_subidx'] <= 90:
        pending_values.append(row['action_clusters_gi_req'])
    if row['metrics_gi_subidx'] <= 90:
        pending_values.append(row['metrics_gi_req'])
    if row['type_impact_gi_subidx'] <= 90:
        pending_values.append(row['type_impact_gi_req'])
    if row['partner_info_gi_subidx'] <= 90:
        pending_values.append(row['partner_info_gi_req'])
    
    # Join the collected pending values with a separator, e.g., ", "
    return ', '.join(filter(None, pending_values))  # filter(None, ...) removes empty strings


df_gi['gi_completeness_req_priority'] = df_gi.apply(concatenate_req_values_final_gi, axis=1)

required_gi_list_to_rename = ['gi_completeness_req_priority']+required_gi_list_prioritized

# Apply the replacement operation to each specified column
    
for col in required_gi_list_to_rename:
    df_gi[col] = df_gi[col].astype(str).apply(lambda x: x.replace('_gu_status', ''))

for col in required_gi_list_to_rename:
    df_gi[col] = df_gi[col].astype(str).apply(lambda x: x.replace('_status', ''))
    
for col in required_gi_list_to_rename:
    df_gi[col] = df_gi[col].astype(str).apply(lambda x: x.replace('_subidx', '_info'))

for col in required_gi_list_to_rename:
    df_gi[col] = df_gi[col].astype(str).apply(lambda x: x.replace('_gi', ''))
    
for col in required_gi_list_to_rename:
    df_gi[col] = df_gi[col].astype(str).apply(lambda x: x.replace(', ;', ';'))
    
for col in required_gi_list_to_rename:
    df_gi[col] = df_gi[col].astype(str).apply(lambda x: x.replace('sub_info', 'saa'))



## Renaming Codes to Real Questions
real_questions_gi_dict = {"type_impact":"Indication of the Type of Impact Expected: 'Does your initiative aim to generate a direct and measurable impact on individuals, companies, cities, regions, countries or natural systems?'",
    "priority_groups":"Identification of Priority Groups: 'Do the actions of your initiative related to RtR target any of these priority groups? (select all that apply)'",
    "insfraestructure_saa":"SAA Infrastructure System Questions",
    "foodandagriculture_saa":"SAA Food and Agriculture System Questions",
    "waterandnatural_saa":"SAA Water and Natural Systems Questions",
    "health_saa":"SAA Health Systems Questions",
    "members_type":"Identification of Member Types: 'Please indicate the types of members your initiative has.'",
    "descrip_n_location":"Partner Description and Location Questions",
    "member_confirmation":"Confirmation of Members Presence: 'In RtR, a member of an RtR Partner is defined as: an implementer, collaborator (partner organization), endorser, or donor - entities that directly contribute to the pledge, plan, and resilience actions reported by your initiative to the campaign, and that have consented to be linked to the RtR through the partner initiative. According to the above, does your initiative has members?'",
    "finance_cross_saa":"SAA Finance Cross Cutting Enabler Questions",
    "action_clusters":"Identification of Action Clusters: 'Please review the descriptions of each Action Cluster. Choose the ones that correspond closely to your organization work related to RtR, considering that a separate plan may be needed for each cluster in future reports'",
    "members_n_reported":"Number of Members Question: 'Among the members that constitute your initiative, how many are explicitly engaged in and actively committed to the RtR campaign?'",
    "coastalandoceanic_saa":"SAA Coastal and Oceanic Systems Questions",
    "members_data_upload":"Upload File with Detailed Member Information: 'We kindly request that you upload a detailed file containing information about your current members. If possible, please clarify the types of members included.'",
    "humansettlements_saa":"SAA Human Settlements Systems Questions",
    "metrics_upload_file":"Upload File with Information about your metrics procedures, data validation and/or tracking progress",
    "metrics_info":"Metrics Procedures, Data Validation and/or Tracking Progress Questions",
    "regions":"Indication of Type of Regions: 'Please indicate all the regions where your initiative's actions related to RtR are being implemented.'",
    "planing_cross_saa":"SAA Planning Cross Cutting Enabler Questions",
    "members_general_info":"General Information About Members Questions",
    }

def replace_values_in_string(s):
    # Splitting the string on both semicolons and commas, and stripping spaces
    parts = [x.strip() for x in re.split(';|,', s)]
    replaced_parts = []
    
    for part in parts:
        # Convert part to lowercase for case-insensitive matching
        lower_part = part.lower()
        # Attempt to find a match in the dictionary keys, converted to lowercase
        match = next((real_questions_gi_dict[key] for key in real_questions_gi_dict if key.lower() == lower_part), None)
        # If a match is found, use it; otherwise, keep the original part
        if match:
            replaced_parts.append(match)
        else:
            replaced_parts.append(part)
    
    # Joining the parts back into a string, separated by "; "
    return "; ".join(replaced_parts)

# Apply the function to each row of the 'gi_completeness_req_priority' column
df_gi['gi_completeness_req_priority_recode'] = df_gi['gi_completeness_req_priority'].apply(replace_values_in_string)
df_gi['gi_overall_status'] = "Completeness: " + df_gi['gi_completeness_status'] + " & Confidence: " + df_gi['confidence_members_overall_gi_status']

##
# df_gi['gi_overall_status']


action_required_gi_list = {
    "Completeness: Accepted & Confidence: High. Members Information Available.":"No Action Required.",
    "Completeness: Accepted & Confidence: High. It Has No Members.":"No Action Required.",
    "Completeness: Awaiting Completion & Confidence: Very Low. No information about Members Received.":"Report General Information. No information Available",
    "Completeness: Awaiting Completion & Confidence: Low. Unsure about having Members (No Data Available).":"Complete Pending Questions and Confirm Information About Members. Currently Unsure.",
    "Completeness: Awaiting Completion & Confidence: Medium. Number of Members Not Available.":"Complete Pending Questions and Report Number of Members",
    "Completeness: Awaiting Completion & Confidence: Medium. Member Data Upload Not Available.":"Complete Pending Questions and Upload Data about Members",}


df_gi['gi_action_required'] = df_gi['gi_overall_status'].map(action_required_gi_list)
df_gi['gi_action_required'] = df_gi['gi_action_required'].str.capitalize()


initial_columns = ['InitName','Org_Type', 'enddate_gi','gi_completeness_idx','gi_overall_status','gi_action_required', 'gi_completeness_status', 'gi_completeness_req_priority','gi_completeness_req_priority_recode','description_general','responder_gi','responder_email_gi']
# initial_columns = ['InitName','Org_Type', 'enddate_gi','gi_completeness_idx','gi_overall_status','gi_action_required', 'gi_completeness_status', 'gi_completeness_req_priority','gi_completeness_req_priority_recode','gi_confidence_members_overall_idx','description_general','responder_gi','responder_email_gi']
confidence_gi_responses_list = confidence_gi_responses_list
completeness_gi_variables_list = partner_info_gi_all_list + members_info_gi_all_list + confidence_gi_responses_list + metrics_info_gi_all_list + saa_gi_all_list + action_clusters_gi_all_list + type_impact_gi_all_list

# Combine the initial columns with the completeness variables list
all_columns_to_display_gi = initial_columns + completeness_gi_variables_list 

#Confirmation
# st.write("# GI over all", df_gi[all_columns_to_display_gi])

### CREATING A SUMMARY TABLE OG GENERAL INFORMATION RESULTS
df_gi_summary = df_gi[all_columns_to_display_gi]
# st.write('# General Information Survey  Summary',df_gi_summary)

# st.write("SUMMARY FIX")
# df_gi_summary







#--ATENTION HERE DO NOT DELETE UNTIL CONFIRMATION ---##
# df = df_gi
# df_len = len(df.index)

#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________________________
# END BLOCK GENERAL INFORMATION
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________

    
    


#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________________________
# BLOCK PLEDGE STATEMENT 2023 
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________

# st.markdown("# PLEDGE STATEMENT SURVEY TREATMENT")
### PLEDGE STATEMENT SURVEY 2023

## CLEANING PART OF THE DATA AND SETTING INDEX

#Renaming and excluding partners not longer part of the race
replacements = {
    "Climate-KIC Accelerator-international Innovation Clusters work (KIC-FRR)": "Climate Knowledge and Innovation Community (Climate-KIC)",
    "BFA Global (BFA)": "BFA Global/ CIFAR Alliance (BFA)",
    "Cities Race to Zero (Resilience) Coalition (CitiesR2R)": "Cities Race to Resilience (CitiesR2R)",
    "Global Fund for Coral Reef (GFCR)": "Global Fund for Coral Reefs (GFCR)",
    "United Nations Office for Disaster Risk Reduction - ARISE (Private Sector Alliance for Disaster Resilient Societies) (UN ARISE)": "ARISE - United Nations Office for Disaster Risk Reduction (UN ARISE)",
    "WBCSDs food & agriculture climate workstream (WBCSD)": "Agriculture 1.5 - WBCSD’s food & agriculture climate workstream (WBCSD)",
    "Sanitation and Water for All  (SWA)": "Sanitation and Water for All (SWA)",
    "Urban Sustainability Directors Network (USDN) Resilience Hubs (USDN)": "Urban Sustainability Directors Network (USDN)",
    "RegionsAdapt (Regions4)": "RegionsAdapt (RegionsAdapt)",
    'Efficiency for Access Coalition':'Efficiency for Access Coalition (EforA)',
    'Efficiency for Access Coalition (EfoA)':'Efficiency for Access Coalition (EforA)',
    'Just Rural Transition (JRT)':'Just Rural Transition',
    'Least Developed Countries Universities Consortium on Climate Change (LUCCC)':'Least Developed Countries Universities Consortium on Climate Change (LUCCC) (ICCCAD)',}
df_pledge['s9'] = df_pledge['s9'].replace(replacements)

#Merging Data with ID MASTER and making sure the data has all members name
df_pledge = df_pledge.rename(columns={'s9':'InitName','s3':'enddate_pledge'})
df_pledge = pd.merge(df_pledge, df_partners_name, on='InitName', how='outer')

# st.markdown("Lista Nombres Pledge")
# st.write(len(df_pledge['InitName']))
# st.write(df_pledge[['InitName','Master ID','Org_Type']])

#Set index
df_pledge.set_index('Master ID', inplace = True)
df_pledge.index.names = ['Master ID']

#CleanNA
df_pledge = df_pledge.dropna(how = 'all')
df_pledge = df_pledge.replace(["Please Complete","Please complete","First Name","Last Name","Please Complete ","email@email.com","Please@complete.com",  "Pleasecomplete@Pleasecomplete.com","please@complete.com", "Would you kindly confirm, please?", "Would you kindly confirm, please? ", ""], np.nan)

#Additional step to ensure all blank spaces are also treated as np.nan
df_pledge = df_pledge.applymap(lambda x: np.nan if isinstance(x, str) and x.strip()=="" else x)
for col in df_pledge.columns:
    df_pledge[col] = df_pledge[col].replace({"": np.nan, " ": np.nan})

#Treatment of "OTHERS" when providing the names
# use numpy where to replace 'Other' in Respondant column with OtherName values
# df['Respondant'] = np.where(df['Respondant'] == 'Other', df['OtherName'], df['Respondant'])

#Making a variable to indentify if the survey has been open or not. 
# Convert the date and time column to datetime data type
df_pledge['enddate_pledge'] = pd.to_datetime(df_pledge['enddate_pledge'], infer_datetime_format=True, errors='coerce')
last_survey_view_list = ['enddate_pledge']
start_date = pd.to_datetime('09/12/2023 08:00:00', format='%m/%d/%Y %H:%M:%S', errors='coerce')
df_pledge['survey2023_reviewed_pledge'] = df_pledge['enddate_pledge'] >= start_date
# st.write(df_pledge[last_survey_view_list+['s9','survey2023_reviewed_pledge']])

#Making a validation colum for thouse that have provide information about the repondant. 
contact_info_list_pledge = ['s11','s12','s16']
df_pledge['respondent_validation_pledge'] = df_pledge[contact_info_list_pledge].notna().all(axis=1)
#st.write(df_pledge[contact_info_list+['respondent_validation_pledge']])


#Merging Data with pledge information 2022 to make reliability analisis of the metrics reported
rename_2022_pledge_data = {'s9':'InitName',
'NumDirectIndiv2022':'individuals_n_total_pledge_2022',
'CompaniesCount_Provision_key_services2022':'companiescount_provision_key_services2022_pledge',
'CompaniesCount_Resilient_occupations2022':'companiescount_resilient_occupations2022_pledge',
'CompaniesTotal2002':'companies_n_comp_pledge_2022',
'RegionsCount_Provision_key_services2022':'regionscount_provision_key_services2022_pledge',
'RegionsCount_Protection_from_harm2022':'regionscount_protection_from_harm2022_pledge',
'RegionsTotal2022':'region_n_reg_pledge_2022',
'CitiesCount_Provision_key_services2022':'citiescount_provision_key_services2022_pledge',
'CitiesCount_Protection_from_harm2022':'citiescount_protection_from_harm2022_pledge',
'CitiesTotal2022':'cities_n_cit_pledge_2022',
'NatSysHectaTotal2022':'natsyst_n_hect_pledge_2022',
}

df_2022_pledge = df_2022_pledge.rename(columns = rename_2022_pledge_data)
df_pledge = pd.merge(df_pledge, df_2022_pledge, on='InitName', how='outer')

##Confirm 2022 data in DataSet Pledge 2023
key_pledge_2022_info_list = ['individuals_n_total_pledge_2022',
'companies_n_comp_pledge_2022',
'region_n_reg_pledge_2022',
'cities_n_cit_pledge_2022',
'natsyst_n_hect_pledge_2022',
]
df_pledge[key_pledge_2022_info_list] = df_pledge[key_pledge_2022_info_list].fillna(0).replace([None], 0)
# st.write("Old Data: Pledge 2022")
# df_pledge[key_pledge_2022_info_list]


## Metrics Pledge Calculation and Reliability
# st.write('## Metrics Comparation in Pledges between 2022 and 2023 for metrics reliability assessment. ')

rename_pledge = {'s16':'responder_email',
          's17':'d_indiv_pledge',
          's2512':'d_indiv_number_pledge_2023',
          's18':'companies_pledge',
          's23':'companies_n_comp_pledge_2023',
          's83':'companies_n_indiv_pledge_2023',
          's19':'region_pledge',
          's650':'region_n_reg_pledge_2023',
          's711':'region_n_indiv_pledge_2023',
          's20':'cities_pledge',
          's1278':'cities_n_cit_pledge_2023',
          's1331':'cities_n_indiv_pledge_2023',
          's21':'natsyst_pledge',
          's1909':'natsyst_n_hect_pledge_2023',
          's1944':'natsyst_n_indiv_pledge_2023',}
df_pledge = df_pledge.rename(columns = rename_pledge)

key_metrics_2023_pledge_list = ['d_indiv_number_pledge_2023',
                                'companies_n_comp_pledge_2023',
                                'companies_n_indiv_pledge_2023',
                                'region_n_reg_pledge_2023',
                                'region_n_indiv_pledge_2023',
                                'cities_n_cit_pledge_2023',
                                'cities_n_indiv_pledge_2023',
                                'natsyst_n_hect_pledge_2023',
                                'natsyst_n_indiv_pledge_2023',]
df_pledge[key_metrics_2023_pledge_list] = df_pledge[key_metrics_2023_pledge_list].fillna(0).astype(int)
# st.write('All variables Data Pledge Metrics',df_pledge[key_metrics_2023_pledge_list + key_pledge_2022_info_list ]) 

# Creating final number of infividuals in pledge 2023 to compare it with its relative in 2022
individuals_beneficiaries_pledge_2023_list = ['d_indiv_number_pledge_2023',
                                              'companies_n_indiv_pledge_2023',
                                              'region_n_indiv_pledge_2023',
                                              'cities_n_indiv_pledge_2023',
                                              'natsyst_n_indiv_pledge_2023',]
# Sum across specified columns for each row and assign to a new column
df_pledge['individuals_n_total_pledge_2023'] = df_pledge[individuals_beneficiaries_pledge_2023_list].sum(axis=1) ## FINAL NUMBER OF INDIVIDUALS DECLARED AS PLEDGE


## FUNCTION TO COMPARE TWO COLUMNS IN PLEDGE
def compare_metrics(df, dimension_name, new_variable_name, value_2022_column, value_2023_column):
    # Correctly combining conditions with parentheses
    conditions = [
        (df[value_2022_column] == df[value_2023_column]) & (df[value_2022_column] != 0) & (df[value_2023_column] != 0),
        df[value_2022_column] > df[value_2023_column],
        df[value_2022_column] < df[value_2023_column],
        df[value_2023_column] == 0
    ]
    choices = [
        f"Metrics Accepted: {dimension_name} Equals compared to 2022",
        f"Metrics Needing Review: {dimension_name} Decrease compared to 2022",
        f"Metrics Accepted: {dimension_name} Increase compared to 2022",
        f"Metrics Needing Review: No Reports on {dimension_name}",
    ]
    df[new_variable_name] = np.select(conditions, choices, default='Need to Review')
    return df

## CREATING RELIABILITY VARIABLES FOR EACH TYPE OF OF BENEFICIARY PLEDGE
# grupo1
df = df_pledge
# dimension_name = 'Individuals, both Direct and Indirect'  ## It relates to the reported number of individuals pledged. As in Pledge 2022 we only considered primary individuals reported as the result. After the metrics enhancement the tool was adjusted. Then in 2023 tool version the final count of individuals pledges is the sum of all questions about the numbers of individuals both from individuals as primary beneficiary and the other types of primary beneficiaries.
dimension_name = 'Individuals (Direct and Indirect)'
new_variable_name = 'n_individuals_pledged_total_confidence'
value_2022_column = 'individuals_n_total_pledge_2022'
value_2023_column = 'individuals_n_total_pledge_2023'
# Apply the function
df_pledge = compare_metrics(df, dimension_name, new_variable_name, value_2022_column, value_2023_column)
# Correct syntax for selecting multiple columns in Streamlit's st.write
columns_to_display = [value_2022_column, value_2023_column, new_variable_name]
# st.write(new_variable_name,df_pledge[columns_to_display])

# grupo2
df = df_pledge
conditional_p_benf = 'companies_pledge'
dimension_name = 'Num Companies'
new_variable_name = 'companies_n_comp_pledge_confidence'
value_2022_column = 'companies_n_comp_pledge_2022'
value_2023_column = 'companies_n_comp_pledge_2023'
# Apply the function
df_pledge = compare_metrics(df, dimension_name, new_variable_name, value_2022_column, value_2023_column)
df_pledge.loc[df_pledge[conditional_p_benf].isna(), new_variable_name] = "No Apply"
# Correct syntax for selecting multiple columns in Streamlit's st.write
columns_to_display = [conditional_p_benf,value_2022_column, value_2023_column, new_variable_name]
# st.write(new_variable_name,df_pledge[columns_to_display])

# grupo3
df = df_pledge
conditional_p_benf = 'cities_pledge'
dimension_name = 'Num Cities'
new_variable_name = 'cities_n_cit_pledge_confidence'
value_2022_column = 'cities_n_cit_pledge_2022'
value_2023_column = 'cities_n_cit_pledge_2023'
# Apply the function
df_pledge = compare_metrics(df, dimension_name, new_variable_name, value_2022_column, value_2023_column)
df_pledge.loc[df_pledge[conditional_p_benf].isna(), new_variable_name] = "No Apply"
# Correct syntax for selecting multiple columns in Streamlit's st.write
columns_to_display = [conditional_p_benf,value_2022_column, value_2023_column, new_variable_name]
# st.write(new_variable_name,df_pledge[columns_to_display])

# grupo4
df = df_pledge
conditional_p_benf = 'region_pledge'
dimension_name = 'Num Regions'
new_variable_name = 'region_n_reg_pledge_confidence'
value_2022_column = 'region_n_reg_pledge_2022'
value_2023_column = 'region_n_reg_pledge_2023'
# Apply the function
df_pledge = compare_metrics(df, dimension_name, new_variable_name, value_2022_column, value_2023_column)
df_pledge.loc[df_pledge[conditional_p_benf].isna(), new_variable_name] = "No Apply"
# Correct syntax for selecting multiple columns in Streamlit's st.write
columns_to_display = [conditional_p_benf,value_2022_column, value_2023_column, new_variable_name]
# st.write(new_variable_name,df_pledge[columns_to_display])

# grupo5
df = df_pledge
conditional_p_benf = 'natsyst_pledge'
dimension_name = 'Hectares of Natural Systems'
new_variable_name = 'natsyst_n_hect_pledge_2023_confidence'
value_2022_column = 'natsyst_n_hect_pledge_2022'
value_2023_column = 'natsyst_n_hect_pledge_2023'
# Apply the function
df_pledge = compare_metrics(df, dimension_name, new_variable_name, value_2022_column, value_2023_column)
df_pledge.loc[df_pledge[conditional_p_benf].isna(), new_variable_name] = "No Apply"
# Correct syntax for selecting multiple columns in Streamlit's st.write
columns_to_display = [conditional_p_benf,value_2022_column, value_2023_column, new_variable_name]
# st.write(new_variable_name,df_pledge[columns_to_display])


#____COUNTRIES TREATMENT PLEDGE
#____COUNTRIES TREATMENT PLEDGE
#____COUNTRIES TREATMENT PLEDGE
#____COUNTRIES TREATMENT PLEDGE

#Treatment of countries
#Replace Names
taiwan_list         = ['s230','s417','s603','s858','s1045','s1231','s1478','s1665','s1851','s2091','s2278','s2465','s2686','s2873','s3059',]
df_pledge[taiwan_list] = df_pledge[taiwan_list].replace("Taiwan","Taiwan, Province of China").fillna('').astype(str)

eeuu_list = ['s267','s454','s640','s895','s1082','s1268','s1515','s1702','s1888','s2128','s2316','s2502','s2723','s2910','s3096',]
df_pledge[eeuu_list] = df_pledge[eeuu_list].replace("United States","United States of America").fillna('').astype(str)

#Identifyng columns
companies_countries_pledge_status_l    =  ['s' + str(i) for i in range(90, 276)]
regions_countries_pledge_status_l      =    ['s' + str(i) for i in range(718, 904)]
cities_countries_pledge_status_l       =     ['s' + str(i) for i in range(1338,1524 )]
natsyst_countries_pledge_status_l      =    ['s' + str(i) for i in range(1951, 2137)]
d_individuals_countries_pledge_status_l =['s' + str(i) for i in range(2546, 2732)]

#Joint Columns of countries
df_pledge['countries_individuals'] = df_pledge[d_individuals_countries_pledge_status_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_pledge['countries_individuals'] = df_pledge['countries_individuals'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_pledge['countries_individuals_pledge_counts'] = df_pledge['countries_individuals'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

df_pledge['countries_companies']   = df_pledge[companies_countries_pledge_status_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_pledge['countries_companies'] = df_pledge['countries_companies'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_pledge['countries_companies_pledge_counts'] = df_pledge['countries_companies'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

df_pledge['countries_regions']     = df_pledge[regions_countries_pledge_status_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_pledge['countries_regions'] = df_pledge['countries_regions'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_pledge['countries_regions_pledge_counts'] = df_pledge['countries_regions'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

df_pledge['countries_cities']      = df_pledge[cities_countries_pledge_status_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_pledge['countries_cities'] = df_pledge['countries_cities'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_pledge['countries_cities_pledge_counts'] = df_pledge['countries_cities'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

df_pledge['countries_nat_sys']     = df_pledge[natsyst_countries_pledge_status_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_pledge['countries_nat_sys'] = df_pledge['countries_nat_sys'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_pledge['countries_nat_sys_pledge_counts'] = df_pledge['countries_nat_sys'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

# Concatenate the country columns into one string per row, separating them with semicolons
df_pledge['all_countries'] = df_pledge[['countries_individuals', 'countries_companies', 'countries_regions', 'countries_cities', 'countries_nat_sys']].apply(lambda x: ';'.join(x.dropna().astype(str)), axis=1)
# Split the concatenated string, remove duplicates and empty strings, then rejoin them
df_pledge['all_countries'] = df_pledge['all_countries'].apply(lambda x: ';'.join(sorted(set(filter(None, [i.strip() for i in x.split(';')])))))
df_pledge['all_countries_pledge_counts'] = df_pledge['all_countries'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

# Total Number of Countries
# #Creating a list of all country names 
# # Split each row by the delimiter and flatten the resulting list
# all_countries_list = [country.strip() for sublist in df_pledge['all_countries'].str.split(';') for country in sublist if country.strip()]
# # Get unique country names using set
# unique_countries = list(set(all_countries_list = [country.strip() for sublist in df_pledge['all_countries'].str.split(';') for country in sublist if country.strip()]
# ))
# # Create a new DataFrame
# df_unique_countries = pd.DataFrame(unique_countries, columns=['Country'])
# # Display the result
# # st.write(df_unique_countries)

#creating a list of countries depending of its continent
Africa = df_country[df_country['continent']== 'Africa']
Asia = df_country[df_country['continent']== 'Asia']
Europe = df_country[df_country['continent']== 'Europe']
Oceania = df_country[df_country['continent']== 'Oceania']
Northern_America = df_country[df_country['continent']== 'North America']
Southern_America = df_country[df_country['continent']== 'South America'] #NEW
Antarctica = df_country[df_country['continent']== 'Antarctica'] #NEW
seven_seas = df_country[df_country['continent']== 'Seven seas (open ocean)'] #NEW
# LATAMC = df_country[df_country['continent']== 'Latin America and the Caribbean'] #OLD

Africa_list = Africa['Country'].tolist()
Asia_list = Asia['Country'].tolist()
Europe_list = Europe['Country'].tolist()
Oceania_list = Oceania['Country'].tolist()
Northern_America_list = Northern_America['Country'].tolist()
Southern_America_list = Southern_America['Country'].tolist()
Antarctica_list = Antarctica['Country'].tolist()
seven_seas_list = seven_seas['Country'].tolist()
# LATAMC_list = LATAMC['Country'].tolist()

df_pledge['Africa'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Africa_list for country in x])), 'Africa', '')
df_pledge['Asia'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Asia_list for country in x])), 'Asia', '')
df_pledge['Europe'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Europe_list for country in x])), 'Europe', '')
df_pledge['Oceania'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Oceania_list for country in x])), 'Oceania', '')
df_pledge['Northern_America'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
df_pledge['Southern_America'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_America_list for country in x])), 'South America', '')
df_pledge['Antarctica'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Antarctica_list for country in x])), 'Antarctica', '')
df_pledge['Seven_seas'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in seven_seas_list for country in x])), 'Seven seas (open ocean)', '')

# df_pledge['LATAMC'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in LATAMC_list for country in x])), 'Latin America and the Caribbean', '')
# continents_pledge_list = ['Africa','Asia','Europe','LATAMC','Northern_America','Oceania']

continents_pledge_list = ['Africa','Asia','Europe','Oceania','Northern_America','Southern_America','Antarctica','Seven_seas']

# st.write('continents_pledge_list',df_pledge[continents_pledge_list])



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

df_pledge['South_Asia'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in South_Asia_list for country in x])), 'South Asia', '')
df_pledge['Europe_Central_Asia'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Europe_Central_Asia_list for country in x])), 'Europe & Central Asia', '')
df_pledge['Middle_East_North_Africa'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Middle_East_North_Africa_list for country in x])), 'Middle East & North Africa', '')
df_pledge['Sub_Saharan_Africa'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Sub_Saharan_Africa_list for country in x])), 'Sub-Saharan Africa', '')
df_pledge['Latin_America_Caribbean'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Latin_America_Caribbean_list for country in x])), 'Latin America & Caribbean', '')
df_pledge['East_Asia_Pacific'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in East_Asia_Pacific_list for country in x])), 'East Asia & Pacific', '')
df_pledge['North_America'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in North_America_list for country in x])), 'North America', '')

regions_pledge_list = ['South_Asia','Europe_Central_Asia','Middle_East_North_Africa','Sub_Saharan_Africa','Latin_America_Caribbean','East_Asia_Pacific','North_America']
# st.write(df_pledge[regions_pledge_list])

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

df_pledge['Southern_Asia'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Asia_list for country in x])), 'Southern Asia', '')
df_pledge['Southern_Europe'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Europe_list for country in x])), 'Southern Europe', '')
df_pledge['Northern_Africa'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_Africa_list for country in x])), 'Northern Africa', '')
df_pledge['Middle_Africa'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Middle_Africa_list for country in x])), 'Middle Africa', '')
df_pledge['Caribbean'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Caribbean_list for country in x])), 'Caribbean', '')
df_pledge['South_America'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in South_America_list for country in x])), 'South America', '')
df_pledge['Western_Asia'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Asia_list for country in x])), 'Western Asia', '')
df_pledge['Australia_and_New_Zealand'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Australia_and_New_Zealand_list for country in x])), 'Australia and New Zealand', '')
df_pledge['Western_Europe'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Europe_list for country in x])), 'Western Europe', '')
df_pledge['Eastern_Europe'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Europe_list for country in x])), 'Eastern Europe', '')
df_pledge['Central_America'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Central_America_list for country in x])), 'Central America', '')
df_pledge['Western_Africa'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Africa_list for country in x])), 'Western Africa', '')
df_pledge['Southern_Africa'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Africa_list for country in x])), 'Southern Africa', '')
df_pledge['Eastern_Africa'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Africa_list for country in x])), 'Eastern Africa', '')
df_pledge['South_Eastern_Asia'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in South_Eastern_Asia_list for country in x])), 'South-Eastern Asia', '')
df_pledge['Northern_America'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
df_pledge['Eastern_Asia'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Asia_list for country in x])), 'Eastern Asia', '')
df_pledge['Northern_Europe'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_Europe_list for country in x])), 'Northern Europe', '')
df_pledge['Central_Asia'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Central_Asia_list for country in x])), 'Central Asia', '')
df_pledge['Melanesia'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Melanesia_list for country in x])), 'Melanesia', '')
df_pledge['Polynesia'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Polynesia_list for country in x])), 'Polynesia', '')
df_pledge['Micronesia'] = np.where(df_pledge['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Micronesia_list for country in x])), 'Micronesia', '')

subregions_pledge_list = ['Southern_Asia','Southern_Europe','Northern_Africa','Middle_Africa','Caribbean','South_America',
                          'Western_Asia','Australia_and_New_Zealand','Western_Europe','Eastern_Europe','Central_America',
                          'Western_Africa','Southern_Africa','Eastern_Africa','South_Eastern_Asia','Northern_America','Eastern_Asia',
                          'Northern_Europe','Central_Asia','Melanesia','Polynesia','Micronesia',]
# st.write(df_pledge[subregions_pledge_list])

# #Concatenating columns
df_pledge['country_continents_all'] = df_pledge[continents_pledge_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_pledge['country_region_all'] = df_pledge[regions_pledge_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_pledge['country_subregion_all'] = df_pledge[subregions_pledge_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
# st.write(df_pledge[['country_continents_all','country_region_all','country_subregion_all']])

#results
all_countries_pledge_responses_list = [
    'countries_individuals','countries_individuals_pledge_counts',
    'countries_companies','countries_companies_pledge_counts',
    'countries_regions','countries_regions_pledge_counts',
    'countries_cities','countries_cities_pledge_counts',
    'countries_nat_sys','countries_nat_sys_pledge_counts',
    'all_countries','all_countries_pledge_counts']







### PLEDGE STATEMENT SURVEY COMPLETENESS INDEX
# title_section_1 = "# Section 1. Introduction [Indentificación of the Pledge based in responses of type of primary beneficiaries]"
# subtitle_section_1_1 = "## 1.1) Number of Pledges"
# st.markdown(title_section_1)
# st.markdown(subtitle_section_1_1)
# st.markdown("Number of Pledges: ") ## It will be considered as a Pledge if they have reported information about direct beneficiaries

primary_beneficiaries_identification_pledge_l = ['d_indiv_pledge','companies_pledge','region_pledge','cities_pledge','natsyst_pledge']
df_pledge['pledge_reported'] = df_pledge[primary_beneficiaries_identification_pledge_l ].notna().any(axis=1)
num_pledges = df_pledge['pledge_reported'].sum()
df_pledge['p_benefic_pledge_concat']  = df_pledge[primary_beneficiaries_identification_pledge_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_pledge['p_benefic_pledge_counts'] = df_pledge['p_benefic_pledge_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
# st.write(df_pledge[['InitName','pledge_reported','p_benefic_pledge_concat','p_benefic_pledge_counts']])


## Making Responder Identification SubIndex responder_id_pledge_subidx
# title_section_2 = "# Section 2: Initiatives and Beneficiaries Identification"
# subtitle_section_2_1 = "## 2.1) Initiative Identification"
# subtitle_section_2_2 = "## 2.2) Responder Identification"

info_partner_id = """2.1) Partner Identification 
Identifying each partner and their representative accurately is crucial to begin the survey process. You will be prompted to select your partner entity from a pre-existing list or to manually input its name. Likewise, you'll need to provide details about the representative completing the survey, including their name and email address. Providing this accurate information upfront is vital for ensuring efficient and precise future interactions throughout the reporting process. 
Questions and guidelines: 
1. Please select the name of your organization from the list of RtR Partners provided. If your organization's name is not listed, kindly type it in the provided space: Always use the same name for your initiative, If it has substantially changed, please kindly inform us via email to nicolleaspee@climatechampions.team. 
2. Survey Responder’s Full Name. This information will be crucial for potential future communications, including seeking clarifications or making further inquiries. 
3. Survey Responder’s Email Address. This information will be crucial for potential future communications, including seeking clarifications or making further inquiries. """


# st.markdown(title_section_2)
# st.markdown(subtitle_section_2_1)
partner_identification_pledge_l = ['InitName','s10']
# st.write(df_pledge[partner_identification_pledge_l])

# st.markdown(subtitle_section_2_2)
responder_name_id_pledge_l = ['s11','s12']
responder_mail_pledge_l =['responder_email']

df_pledge['responder_name_pledge_concat'] = df_pledge[responder_name_id_pledge_l].apply(lambda x: ' '.join(map(str, x)), axis=1)
df_pledge['responder_name_pledge_concat'] = df_pledge['responder_name_pledge_concat'].str.replace('nan', '')
responder_id_pledge_responses_list = ['responder_name_pledge_concat'] + responder_mail_pledge_l 

df_pledge['responder_name_lastname_pledge_status'] = df_pledge[responder_name_id_pledge_l].notna().all(axis=1)
df_pledge['responder_email_pledge_status'] = df_pledge[responder_mail_pledge_l].notna().all(axis=1)
responder_id_pledge_subidx_list =['responder_name_lastname_pledge_status','responder_email_pledge_status']
df_pledge['responder_id_pledge_subidx'] = (df_pledge[responder_id_pledge_subidx_list].mean(axis=1) * 100).astype(int)
# st.write(df_pledge[['responder_id_pledge_subidx']+responder_id_pledge_subidx_list])

## Indentifying info required
index_list = responder_id_pledge_subidx_list
# Apply the function to each row
df_pledge['responder_id_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)

# Summary List responder_id_pledge_all_list
responder_id_pledge_responses_list = responder_id_pledge_responses_list
responder_id_pledge_results_list  = ['responder_id_pledge_subidx','responder_id_pledge_req',]           
responder_id_pledge_subidx_list = responder_id_pledge_subidx_list
responder_id_pledge_all_list = responder_id_pledge_responses_list + responder_id_pledge_results_list + responder_id_pledge_subidx_list
  ##
##  ##
 ##
## Confirm results sub index responder_id_pledge_subidx
# st.write('Responder ID Pledge',df_pledge[['InitName']+responder_id_pledge_all_list])






#Primary Beneficiaries Subidx
# title_section_3 = "# Section 3: Primary Beneficiaries Reporting"
# subtitle_section_3_0 = "## 3.0) Primary Beneficiaries Identification"

# st.markdown(title_section_3)
# st.markdown(subtitle_section_3_0)

## 3.1) Companies
subtitle_section_3_1 = "## 3.1) Companies"
# st.markdown(subtitle_section_3_1)
companies_l = ['companies_pledge']
companies_n_companies_pledge_status_l = ['companies_n_comp_pledge_2023']
# Ensure the data is numeric
df_pledge[companies_n_companies_pledge_status_l] = df_pledge[companies_n_companies_pledge_status_l].apply(pd.to_numeric, errors='coerce')
#Number of Companies
# st.write("Number of Companies (Sum)", df_pledge[companies_n_companies_pledge_status_l[0]].sum())
# st.write("Number of Companies (Adjusted *0.75)", df_pledge[companies_n_companies_pledge_status_l[0]].sum()*0.75)
df_pledge['companies_n_companies_pledge_status'] = df_pledge[companies_n_companies_pledge_status_l].notna().any(axis=1)
df_pledge.loc[df_pledge[companies_n_companies_pledge_status_l[0]] == 0, 'companies_n_companies_pledge_status'] = False
# st.write(df_pledge[companies_l + companies_n_companies_pledge_status_l+['companies_n_companies_pledge_status']])

companies_sector_pledge_status_l = ['s' + str(i) for i in range(24, 46)]
df_pledge['companies_sector_pledge_status'] = df_pledge[companies_sector_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[companies_l + companies_sector_pledge_status_l+['companies_sector_pledge_status']])

hazards_option_l = [
    'Water stress (urban focus)', 'Water stress (rural focus)', 'Extreme heat',
    'Extreme cold', 'Drought (agriculture focus)', 'Drought (other sectors)',
    'Urban flood', 'River flood', 'Coastal flood', 'Tropical Cyclone',
    'Snow, Ice', 'Wildfire', 'Extreme wind', 'Oceanic Events',
    'Other coastal events',
]
companies_hazards_pledge_status_all_types_hazard_l = ['s46']
companies_hazards_pledge_status_l = ['s' + str(i) for i in range(47, 62)]  # Start from the next after "'All types of hazards' to exclude 'All types of hazards' & Others(please specify)
# Replace the value in each column with the corresponding hazard from hazards_option_l if the 's46' column is 'All types of hazards'
for idx, col in enumerate(companies_hazards_pledge_status_l):
    df_pledge[col] = df_pledge.apply(lambda row: hazards_option_l[idx] if row[companies_hazards_pledge_status_all_types_hazard_l[0]] == 'All types of hazards' else row[col], axis=1)
companies_hazards_pledge_status_l = ['s' + str(i) for i in range(47, 63)] #Adding Other to list
df_pledge['companies_hazards_pledge_status'] = df_pledge[companies_hazards_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[companies_hazards_pledge_status_l+['companies_hazards_pledge_status']])

companies_types_of_individuals_pledge_status_l = ['s' + str(i) for i in range(63, 83)]
df_pledge['companies_types_of_individuals_pledge_status'] = df_pledge[companies_types_of_individuals_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[companies_l + companies_types_of_individuals_pledge_status_l+['companies_types_of_individuals_pledge_status']])

companies_n_individuals_pledge_status_l = ['companies_n_indiv_pledge_2023']
# Ensure the data is numeric
df_pledge[companies_n_individuals_pledge_status_l] = df_pledge[companies_n_individuals_pledge_status_l].apply(pd.to_numeric, errors='coerce')
df_pledge['companies_n_individuals_pledge_status'] = df_pledge[companies_n_individuals_pledge_status_l].notna().any(axis=1)
df_pledge.loc[df_pledge[companies_n_individuals_pledge_status_l [0]] == 0, 'companies_n_individuals_pledge_status'] = False
#Number of individuals --> Companies
# st.write("Number of Individuals --> Companies (sum)",df_pledge[companies_n_individuals_pledge_status_l[0]].sum())

companies_continents_pledge_l = ['s' + str(i) for i in range(84, 90)]
df_pledge['companies_continents_pledge'] = df_pledge[companies_continents_pledge_l].notna().any(axis=1)
# st.write(df_pledge[companies_continents_pledge_l+['companies_continents_pledge']])

companies_countries_pledge_status_l =['s' + str(i) for i in range(90, 276)]
df_pledge['companies_countries_pledge_status'] = df_pledge[companies_countries_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[companies_countries_pledge_status_l+['companies_countries_pledge_status']])

companies_capabily_country_level_pledge_l = ['s276',]
df_pledge['companies_capabily_country_level_pledge'] = df_pledge[companies_capabily_country_level_pledge_l].notna().any(axis=1)
# st.write("# Pledge Companies Capability")
# st.write(df_pledge[companies_capabily_country_level_pledge_l+['companies_capabily_country_level_pledge']])
 
companies_distribution_individuals_per_country_pledge_l = ['s' + str(i) for i in range(277, 649)]
df_pledge['companies_distribution_individuals_per_country_pledge'] = df_pledge[companies_distribution_individuals_per_country_pledge_l].notna().any(axis=1)
# st.write(df_pledge[companies_distribution_individuals_per_country_pledge_l+['companies_distribution_individuals_per_country_pledge']])


## COMPANIES PLEDGE SUB INDEX companies_pledge_sub_subidx
companies_index_list_pledge = [
    'companies_n_companies_pledge_status',
    'companies_sector_pledge_status',
    'companies_hazards_pledge_status',
    'companies_types_of_individuals_pledge_status',
    'companies_n_individuals_pledge_status',
    'companies_countries_pledge_status',
]

weights = {
    'companies_n_companies_pledge_status': 0.175,
    'companies_sector_pledge_status': 0.041666667,
    'companies_hazards_pledge_status': 0.041666667,
    'companies_types_of_individuals_pledge_status': 0.041666667,
    'companies_n_individuals_pledge_status': 0.35,
    'companies_countries_pledge_status': 0.35,
}

# Setting specific columns to False where 'companies_pledge' is NaN
df_pledge.loc[df_pledge['companies_pledge'].isna(), companies_index_list_pledge] = False

# Calculate the weighted sum of the components for companies_pledge_sub_subidx
df_pledge['companies_pledge_sub_subidx'] = df_pledge.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_pledge['companies_pledge_sub_subidx'] = (df_pledge['companies_pledge_sub_subidx'] * 100).astype(int)


## Indentifying info required
index_list = companies_index_list_pledge
# Apply the function to each row
df_pledge['companies_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)
df_pledge.loc[df_pledge['companies_pledge'].isna(), 'companies_pledge_req'] = "No Apply"


# Summary List companies_pledge_all_list
companies_n_pledge_confidence_list = ['companies_n_comp_pledge_2022','companies_n_comp_pledge_confidence'] 
companies_pledge_responses_list = companies_l + companies_n_companies_pledge_status_l + companies_n_pledge_confidence_list+ companies_n_individuals_pledge_status_l 
companies_pledge_results_list  = ['companies_pledge_sub_subidx','companies_pledge_req',]           
companies_pledge_sub_subidx_list = companies_index_list_pledge
companies_pledge_all_list = companies_pledge_responses_list + companies_pledge_results_list + companies_pledge_sub_subidx_list
  ##
##  ##
 ##
## Confirm results sub index companies_pledge_sub_subidx
# st.write('Companies Pledge Subidx',df_pledge[['InitName']+companies_pledge_all_list])
 
 
 
subtitle_section_3_2 = "## 3.2) Regions"
#3.2) Regions 
# st.markdown(subtitle_section_3_2)
regions_l = ['region_pledge']
regions_n_regions_pledge_status_l = ['region_n_reg_pledge_2023',]
# Ensure the data is numeric
df_pledge[regions_n_regions_pledge_status_l] = df_pledge[regions_n_regions_pledge_status_l].apply(pd.to_numeric, errors='coerce')
#Number of Regions
# st.write("Number of Regions (sum)", df_pledge[regions_n_regions_pledge_status_l[0]].sum())
# st.write("Number of Regions (Adjusted *0.75)", df_pledge[regions_n_regions_pledge_status_l[0]].sum()*0.75)

df_pledge['regions_n_regions_pledge_status'] = df_pledge[regions_n_regions_pledge_status_l].notna().any(axis=1)
df_pledge.loc[df_pledge[regions_n_regions_pledge_status_l [0]] == 0, 'regions_n_regions_pledge_status'] = False
# st.write(df_pledge[regions_l + regions_n_regions_pledge_status_l+['regions_n_regions_pledge_status']])

regions_p_benefic_all_pledge_status_l = ['s' + str(i) for i in range(651, 678)]
df_pledge['regions_p_benefic_all_pledge_status'] = df_pledge[regions_p_benefic_all_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[regions_l + regions_p_benefic_all_pledge_status_l+['regions_p_benefic_all_pledge_status']])

hazards_option_l = [
    'Water stress (urban focus)', 'Water stress (rural focus)', 'Extreme heat',
    'Extreme cold', 'Drought (agriculture focus)', 'Drought (other sectors)',
    'Urban flood', 'River flood', 'Coastal flood', 'Tropical Cyclone',
    'Snow, Ice', 'Wildfire', 'Extreme wind', 'Oceanic Events',
    'Other coastal events',]
regions_hazards_pledge_status_all_types_hazard_l = ['s678',]
regions_hazards_pledge_status_l = ['s' + str(i) for i in range(679, 694)]  # Start from the next after "'All types of hazards' to exclude 'All types of hazards' & Others(please specify)
# Replace the value in each column with the corresponding hazard from hazards_option_l if the 'all types of hazards' column is 'All types of hazards'
for idx, col in enumerate(regions_hazards_pledge_status_l):
    df_pledge[col] = df_pledge.apply(lambda row: hazards_option_l[idx] if row[regions_hazards_pledge_status_all_types_hazard_l[0]] == 'All types of hazards' else row[col], axis=1)

regions_hazards_pledge_status_l = ['s' + str(i) for i in range(679, 695)] #Adding Other to list
df_pledge['regions_hazards_pledge_status'] = df_pledge[regions_hazards_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[regions_hazards_pledge_status_l+['regions_hazards_pledge_status']])

regions_types_of_individuals_options = [
'Coastal communities: Populations living in areas sensitive to sea-level rise, erosion, and coastal storms.','Communities adhering to building standards for climate resilience: Those living in areas where building codes and standards focus on climate resilience.','Communities in agricultural, livestock, and fisheries zones: Populations residing near or dependent on these types of industries.','Communities near forests and conservation areas: Residents of areas adjacent to forests and wildlife conservation zones.','Communities or regions receiving financial support for climate resilience: Those benefiting from grants, subsidies, or other financial incentives aimed at climate resilience.','Communities relying on major public infrastructures: Populations dependent on large-scale public infrastructure like highways, bridges, and dams.','Communities relying on specific water sources: Those dependent on particular rivers, lakes, or groundwater for their water supply.','Inhabitants of cities with active climate governance: Residents of urban areas where local governments are proactive in climate change mitigation and adaptation.','Populations benefiting from tailored public health services: Communities served by healthcare services adapted to the challenges posed by climate change.','Populations in areas prone to coastal natural disasters: Those living in regions vulnerable to hurricanes, tsunamis, or other coastal hazards.','Populations in energy-efficient planning zones: Residents of areas where sustainable and energy-efficient urban planning is a priority.','Populations near or in park areas: Those living adjacent to or within national, state, or local parks.','Residents of DRM-focused communities: Populations in areas with specialized disaster risk management agencies or services.','Residents of areas with environmental protection measures: Those living in zones with specific policies or programs aimed at environmental conservation.','Urban communities with local gardening and public spaces: Populations in urban areas that benefit from local initiatives like community gardens or improved public spaces.',
]
regions_type_of_individuaks_all_l = ['s710',]
regions_types_of_individuals_pledge_status_l = ['s' + str(i) for i in range(695, 710)]  # Start from the next after "'All types of hazards' to exclude 'All types of hazards' & Others(please specify)
# Replace the value in each column with the corresponding hazard from hazards_option_l if the 'all types of hazards' column is 'All types of hazards'
for idx, col in enumerate(regions_types_of_individuals_pledge_status_l):
    df_pledge[col] = df_pledge.apply(lambda row: regions_types_of_individuals_options[idx] if row[regions_type_of_individuaks_all_l[0]] == 'All' else row[col], axis=1)
regions_types_of_individuals_pledge_status_l = ['s' + str(i) for i in range(695, 711)]
df_pledge['regions_types_of_individuals_pledge_status'] = df_pledge[regions_types_of_individuals_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[regions_l + regions_types_of_individuals_pledge_status_l+['regions_types_of_individuals_pledge_status']])

regions_n_individuals_pledge_status_l = ['region_n_indiv_pledge_2023',]
df_pledge[regions_n_individuals_pledge_status_l] = df_pledge[regions_n_individuals_pledge_status_l].apply(pd.to_numeric, errors='coerce')
df_pledge['regions_n_individuals_pledge_status'] = df_pledge[regions_n_individuals_pledge_status_l].notna().any(axis=1)
df_pledge.loc[df_pledge[regions_n_individuals_pledge_status_l [0]] == 0, 'regions_n_individuals_pledge_status'] = False

#Number of individuals --> Regions
# st.write("Number of Individuals --> Regions (sum)",df_pledge[regions_n_individuals_pledge_status_l[0]].sum())

regions_continents_pledge_l = ['s' + str(i) for i in range(712, 718)]
df_pledge['regions_continents_pledge'] = df_pledge[regions_continents_pledge_l].notna().any(axis=1)
# st.write(df_pledge[regions_continents_pledge_l+['regions_continents_pledge']])

regions_countries_pledge_status_l =['s' + str(i) for i in range(718, 904)]
df_pledge['regions_countries_pledge_status'] = df_pledge[regions_countries_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[regions_countries_pledge_status_l+['regions_countries_pledge_status']])

regions_capabily_country_level_pledge_l = ['s904',]
df_pledge['regions_capabily_country_level_pledge'] = df_pledge[regions_capabily_country_level_pledge_l].notna().any(axis=1)
# st.write("# Regions Capability")
# st.write(df_pledge[regions_capabily_country_level_pledge_l+['regions_capabily_country_level_pledge']])

regions_distribution_individuals_per_country_pledge_l = ['s' + str(i) for i in range(905, 1277)]
df_pledge['regions_distribution_individuals_per_country_pledge'] = df_pledge[regions_distribution_individuals_per_country_pledge_l].notna().any(axis=1)
# st.write(df_pledge[regions_distribution_individuals_per_country_pledge_l+['regions_distribution_individuals_per_country_pledge']])


## REGION Sub Index regions_pledge_sub_subidx
regions_index_list_pledge = ['regions_n_regions_pledge_status','regions_p_benefic_all_pledge_status','regions_hazards_pledge_status','regions_types_of_individuals_pledge_status','regions_n_individuals_pledge_status','regions_countries_pledge_status',]
df_pledge.loc[df_pledge['region_pledge'].isna(), regions_index_list_pledge] = False

weights = {
    'regions_n_regions_pledge_status':0.175,
    'regions_p_benefic_all_pledge_status':0.041666667,
    'regions_hazards_pledge_status':0.041666667,
    'regions_types_of_individuals_pledge_status':0.041666667,
    'regions_n_individuals_pledge_status':0.35,
    'regions_countries_pledge_status':0.35,}

# Calculate the weighted sum of the components for regions_pledge_sub_subidx
df_pledge['regions_pledge_sub_subidx'] = df_pledge.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_pledge['regions_pledge_sub_subidx'] = (df_pledge['regions_pledge_sub_subidx'] * 100).astype(int)

## Indentifying info required
index_list = regions_index_list_pledge
# Apply the function to each row
df_pledge['regions_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)
df_pledge.loc[df_pledge['region_pledge'].isna(), 'regions_pledge_req'] = "No Apply"

# Summary List regions_pledge_all_list
region_n_reg_pledge_confidence_list = ['region_n_reg_pledge_2022','region_n_reg_pledge_confidence'] 
regions_pledge_responses_list = regions_l + regions_n_regions_pledge_status_l + region_n_reg_pledge_confidence_list +regions_n_individuals_pledge_status_l 
regions_pledge_results_list  = ['regions_pledge_sub_subidx','regions_pledge_req',]           
regions_pledge_sub_subidx_list = regions_index_list_pledge
regions_pledge_all_list = regions_pledge_responses_list + regions_pledge_results_list + regions_pledge_sub_subidx_list
  ##
##  ##
 ##
## Confirm results sub index regions_pledge_sub_subidx
# st.write('regions Pledge Subidx',df_pledge[['InitName']+regions_pledge_all_list])



subtitle_section_3_3 = "## 3.3) Cities"
#3.3) Cities
# st.markdown(subtitle_section_3_3)
cities_l = ['cities_pledge',]
cities_n_cities_pledge_status_l = ['cities_n_cit_pledge_2023',]
# Ensure the data is numeric
df_pledge[cities_n_cities_pledge_status_l] = df_pledge[cities_n_cities_pledge_status_l].apply(pd.to_numeric, errors='coerce')
#Number of cities
# st.write("Number of cities (sum)", df_pledge[cities_n_cities_pledge_status_l[0]].sum())
# st.write("Number of cities (adjusted *0.75)", df_pledge[cities_n_cities_pledge_status_l[0]].sum()*0.75)

df_pledge['cities_n_cities_pledge_status'] = df_pledge[cities_n_cities_pledge_status_l].notna().any(axis=1)
df_pledge.loc[df_pledge[cities_n_cities_pledge_status_l [0]] == 0, 'cities_n_cities_pledge_status'] = False
# st.write(df_pledge[cities_l + cities_n_cities_pledge_status_l+['cities_n_cities_pledge_status']])

cities_p_benefic_all_pledge_status_l = ['s' + str(i) for i in range(1279, 1298)]
df_pledge['cities_p_benefic_all_pledge_status'] = df_pledge[cities_p_benefic_all_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[cities_l + cities_p_benefic_all_pledge_status_l+['cities_p_benefic_all_pledge_status']])

hazards_option_l = [
    'Water stress (urban focus)', 'Water stress (rural focus)', 'Extreme heat',
    'Extreme cold', 'Drought (agriculture focus)', 'Drought (other sectors)',
    'Urban flood', 'River flood', 'Coastal flood', 'Tropical Cyclone',
    'Snow, Ice', 'Wildfire', 'Extreme wind', 'Oceanic Events',
    'Other coastal events',]
cities_hazards_pledge_status_all_types_hazard_l = ['s1298',]
cities_hazards_pledge_status_l = ['s' + str(i) for i in range(1299, 1314)]  # Start from the next after "'All types of hazards' to exclude 'All types of hazards' & Others(please specify)
# Replace the value in each column with the corresponding hazard from hazards_option_l if the 'all types of hazards' column is 'All types of hazards'
for idx, col in enumerate(cities_hazards_pledge_status_l):
    df_pledge[col] = df_pledge.apply(lambda row: hazards_option_l[idx] if row[cities_hazards_pledge_status_all_types_hazard_l[0]] == 'All types of hazards' else row[col], axis=1)
cities_hazards_pledge_status_l = ['s' + str(i) for i in range(1299, 1315)] #Adding Other to list
df_pledge['cities_hazards_pledge_status'] = df_pledge[cities_hazards_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[cities_hazards_pledge_status_l+['cities_hazards_pledge_status']])

cities_types_of_individuals_pledge_status_l = ['s' + str(i) for i in range(1315, 1331)]
df_pledge['cities_types_of_individuals_pledge_status'] = df_pledge[cities_types_of_individuals_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[cities_l + cities_types_of_individuals_pledge_status_l+['cities_types_of_individuals_pledge_status']])

cities_n_individuals_pledge_status_l = ['cities_n_indiv_pledge_2023']
df_pledge[cities_n_individuals_pledge_status_l] = df_pledge[cities_n_individuals_pledge_status_l].apply(pd.to_numeric, errors='coerce')
df_pledge['cities_n_individuals_pledge_status'] = df_pledge[cities_n_individuals_pledge_status_l].notna().any(axis=1)
df_pledge.loc[df_pledge[cities_n_individuals_pledge_status_l [0]] == 0, 'cities_n_individuals_pledge_status'] = False

#Number of individuals --> cities
# st.write("Number of individuals --> Cities (sum): ",df_pledge[cities_n_individuals_pledge_status_l[0]].sum())

cities_continents_pledge_l = ['s' + str(i) for i in range(1332, 1338)]
df_pledge['cities_continents_pledge'] = df_pledge[cities_continents_pledge_l].notna().any(axis=1)
# st.write(df_pledge[cities_continents_pledge_l+['cities_continents_pledge']])

cities_countries_pledge_status_l =['s' + str(i) for i in range(1338,1524 )]
df_pledge['cities_countries_pledge_status'] = df_pledge[cities_countries_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[cities_countries_pledge_status_l+['cities_countries_pledge_status']])

cities_capabily_country_level_pledge_l = ['s1524',]
df_pledge['cities_capabily_country_level_pledge'] = df_pledge[cities_capabily_country_level_pledge_l].notna().any(axis=1)
# st.write(df_pledge[['s1524','cities_capabily_country_level_pledge']])

cities_distribution_individuals_per_country_pledge_l = ['s' + str(i) for i in range(1525, 1897)]
df_pledge['cities_distribution_individuals_per_country_pledge'] = df_pledge[cities_distribution_individuals_per_country_pledge_l].notna().any(axis=1)
# st.write(df_pledge[cities_distribution_individuals_per_country_pledge_l+['cities_distribution_individuals_per_country_pledge']])
 
cities_index_list_pledge =['cities_n_cities_pledge_status',
                           'cities_p_benefic_all_pledge_status',
                           'cities_hazards_pledge_status',
                           'cities_types_of_individuals_pledge_status',
                           'cities_n_individuals_pledge_status',
                           'cities_countries_pledge_status',]
df_pledge.loc[df_pledge['cities_pledge'].isna(), cities_index_list_pledge] = False
cities_metrics_list = ['cities_n_cit_pledge_2023','cities_n_indiv_pledge_2023']
df_pledge.loc[df_pledge['cities_pledge'].isna(), cities_metrics_list] = np.nan

## INDEX CITIES
weights = {
    'cities_n_cities_pledge_status':0.175,
    'cities_p_benefic_all_pledge_status':0.041666667,
    'cities_hazards_pledge_status':0.041666667,
    'cities_types_of_individuals_pledge_status':0.041666667,
    'cities_n_individuals_pledge_status':0.35,
    'cities_countries_pledge_status':0.35,}

# Calculate the weighted sum of the components for cities_pledge_sub_subidx
df_pledge['cities_pledge_sub_subidx'] = df_pledge.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_pledge['cities_pledge_sub_subidx'] = (df_pledge['cities_pledge_sub_subidx'] * 100).astype(int)

## Indentifying info required
index_list = cities_index_list_pledge
# Apply the function to each row
df_pledge['cities_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)
df_pledge.loc[df_pledge['cities_pledge'].isna(), 'cities_pledge_req'] = "No Apply"

# Summary List cities_pledge_all_list
cities_n_cit_pledge_confidence_list = ['cities_n_cit_pledge_2022','cities_n_cit_pledge_confidence'] 
cities_pledge_responses_list = cities_l + cities_n_cities_pledge_status_l + cities_n_cit_pledge_confidence_list + cities_n_individuals_pledge_status_l 
cities_pledge_results_list  = ['cities_pledge_sub_subidx','cities_pledge_req',]           
cities_pledge_sub_subidx_list = cities_index_list_pledge
cities_pledge_all_list = cities_pledge_responses_list + cities_pledge_results_list + cities_pledge_sub_subidx_list
  ##
##  ##
 ##
## Confirm results sub index cities_pledge_sub_subidx
# st.write('cities Pledge Subidx',df_pledge[['InitName']+cities_pledge_all_list])



subtitle_section_3_4 = "## 3.4) Natural Systems"
#3.4) Natural Systems
# st.markdown(subtitle_section_3_4)
natsyst_l = ['natsyst_pledge',]
natsyst_type_natsyst_pledge_status_l = ['s' + str(i) for i in range(1897, 1909)]
df_pledge['natsyst_type_pledge_concat'] = df_pledge.apply(lambda row: ';'.join([str(row[col]) for col in natsyst_type_natsyst_pledge_status_l if pd.notnull(row[col]) and row[col] != '']), axis=1)


df_pledge['natsyst_type_natsyst_pledge_status'] = df_pledge[natsyst_type_natsyst_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[natsyst_l + natsyst_type_natsyst_pledge_status_l+['natsyst_type_natsyst_pledge_status']])

natsyst_n_hectares_pledge_status_l = ['natsyst_n_hect_pledge_2023',]
# Ensure the data is numeric
df_pledge[natsyst_n_hectares_pledge_status_l] = df_pledge[natsyst_n_hectares_pledge_status_l].apply(pd.to_numeric, errors='coerce')
#Number of Hectares
# st.write("Number of Hectares (sum)", df_pledge[natsyst_n_hectares_pledge_status_l[0]].sum())
# st.write("Number of Hectares (adjusted *0.75)", df_pledge[natsyst_n_hectares_pledge_status_l[0]].sum()*0.75)

df_pledge['natsyst_n_hectares_pledge_status'] = df_pledge[natsyst_n_hectares_pledge_status_l].notna().any(axis=1)
df_pledge.loc[df_pledge[natsyst_n_hectares_pledge_status_l [0]] == 0, 'natsyst_n_hectares_pledge_status'] = False
# st.write(df_pledge[natsyst_l + natsyst_n_hectares_pledge_status_l+['natsyst_n_hectares_pledge_status']])

#Other number of Natural Systems
# st.write(df_pledge['s1910'])

hazards_option_l = [
    'Water stress (urban focus)', 'Water stress (rural focus)', 'Extreme heat',
    'Extreme cold', 'Drought (agriculture focus)', 'Drought (other sectors)',
    'Urban flood', 'River flood', 'Coastal flood', 'Tropical Cyclone',
    'Snow, Ice', 'Wildfire', 'Extreme wind', 'Oceanic Events',
    'Other coastal events',]
natsyst_hazards_pledge_status_all_types_hazard_l = ['s1911']
natsyst_hazards_pledge_status_l = ['s' + str(i) for i in range(1912, 1927)]  # Start from the next after "'All types of hazards' to exclude 'All types of hazards' & Others(please specify)
# Replace the value in each column with the corresponding hazard from hazards_option_l if the 'all types of hazards' column is 'All types of hazards'
for idx, col in enumerate(natsyst_hazards_pledge_status_l):
    df_pledge[col] = df_pledge.apply(lambda row: hazards_option_l[idx] if row[natsyst_hazards_pledge_status_all_types_hazard_l[0]] == 'All types of hazards' else row[col], axis=1)
natsyst_hazards_pledge_status_l = ['s' + str(i) for i in range(1912, 1928)] #Adding Other to list
df_pledge['natsyst_hazards_pledge_status'] = df_pledge[natsyst_hazards_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[natsyst_hazards_pledge_status_l+['natsyst_hazards_pledge_status']])

natsyst_types_of_individuals_pledge_status_l = ['s' + str(i) for i in range(1928, 1944)]
df_pledge['natsyst_types_of_individuals_pledge_status'] = df_pledge[natsyst_types_of_individuals_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[natsyst_l + natsyst_types_of_individuals_pledge_status_l+['natsyst_types_of_individuals_pledge_status']])

natsyst_n_individuals_pledge_status_l = ['natsyst_n_indiv_pledge_2023',]
df_pledge[natsyst_n_individuals_pledge_status_l] = df_pledge[natsyst_n_individuals_pledge_status_l].apply(pd.to_numeric, errors='coerce')
df_pledge['natsyst_n_individuals_pledge_status'] = df_pledge[natsyst_n_individuals_pledge_status_l].notna().any(axis=1)
df_pledge.loc[df_pledge[natsyst_n_individuals_pledge_status_l [0]] == 0, 'natsyst_n_individuals_pledge_status'] = False
# st.write(df_pledge[natsyst_n_individuals_pledge_status_l])
# #Number of individuals --> natsyst
# st.write("Number Individuals --> Natural Systems (sum)", df_pledge[natsyst_n_individuals_pledge_status_l[0]].sum())
# st.write("Number Individuals --> Natural Systems (adjusted 0*75)", df_pledge[natsyst_n_individuals_pledge_status_l[0]].sum()*0.75)

natsyst_continents_pledge_l = ['s' + str(i) for i in range(1945, 1951)]
df_pledge['natsyst_continents_pledge'] = df_pledge[natsyst_continents_pledge_l].notna().any(axis=1)
# st.write(df_pledge[natsyst_continents_pledge_l+['natsyst_continents_pledge']])

natsyst_countries_pledge_status_l =['s' + str(i) for i in range(1951, 2137)]
df_pledge['natsyst_countries_pledge_status'] = df_pledge[natsyst_countries_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[natsyst_countries_pledge_status_l+['natsyst_countries_pledge_status']])

natsyst_capabily_country_level_pledge_l = ['s2137',]
df_pledge['natsyst_capabily_country_level_pledge'] = df_pledge[natsyst_capabily_country_level_pledge_l].notna().any(axis=1)
# st.write(df_pledge[natsyst_capabily_country_level_pledge_l+['natsyst_capabily_country_level_pledge']])

natsyst_distribution_individuals_per_country_pledge_l = ['s' + str(i) for i in range(2138, 2511)]
df_pledge['natsyst_distribution_individuals_per_country_pledge'] = df_pledge[natsyst_distribution_individuals_per_country_pledge_l].notna().any(axis=1)
# st.write(df_pledge[natsyst_distribution_individuals_per_country_pledge_l+['natsyst_distribution_individuals_per_country_pledge']])

natsyst_index_list_pledge =['natsyst_type_natsyst_pledge_status',
                            'natsyst_n_hectares_pledge_status',
                            'natsyst_hazards_pledge_status',
                            'natsyst_types_of_individuals_pledge_status',
                            'natsyst_n_individuals_pledge_status',
                            'natsyst_countries_pledge_status',]    
df_pledge.loc[df_pledge['natsyst_pledge'].isna(), natsyst_index_list_pledge] = False
natsyst_metrics_list = ['natsyst_n_hect_pledge_2023','natsyst_n_indiv_pledge_2023']
df_pledge.loc[df_pledge['natsyst_pledge'].isna(), natsyst_metrics_list] = np.nan

## SUB INDEX NATURAL SYSTEMS
weights = {
    'natsyst_n_hectares_pledge_status':0.275,
    'natsyst_type_natsyst_pledge_status':0.041666667,
    'natsyst_hazards_pledge_status':0.041666667,
    'natsyst_types_of_individuals_pledge_status':0.041666667,
    'natsyst_n_individuals_pledge_status':0.3,
    'natsyst_countries_pledge_status':0.3,}

# Calculate the weighted sum of the components for natsyst_pledge_sub_subidx
df_pledge['natsyst_pledge_sub_subidx'] = df_pledge.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_pledge['natsyst_pledge_sub_subidx'] = (df_pledge['natsyst_pledge_sub_subidx'] * 100).astype(int)

## Indentifying info required
index_list = natsyst_index_list_pledge
# Apply the function to each row
df_pledge['natsyst_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)
df_pledge.loc[df_pledge['natsyst_pledge'].isna(), 'natsyst_pledge_req'] = "No Apply"

# Summary List natsyst_pledge_all_list

natsyst_n_hect_pledge_confidence_list = ['natsyst_n_hect_pledge_2022','natsyst_n_hect_pledge_2023_confidence'] 
natsyst_pledge_responses_list = ['natsyst_pledge','natsyst_type_pledge_concat','natsyst_n_hect_pledge_2023','natsyst_n_indiv_pledge_2023']
natsyst_pledge_results_list  = ['natsyst_pledge_sub_subidx','natsyst_pledge_req',]           
natsyst_pledge_sub_subidx_list = natsyst_index_list_pledge
natsyst_pledge_all_list = natsyst_pledge_responses_list + natsyst_n_hect_pledge_confidence_list + natsyst_pledge_results_list + natsyst_pledge_sub_subidx_list
  ##
##  ##
 ##
## Confirm results sub index natsyst_pledge_sub_subidx
# st.write('natsyst Pledge Subidx',df_pledge[['InitName']+natsyst_pledge_all_list])

 


subtitle_section_3_5 = "## 3.5) Direct Individuals"
#3.5) Individuals
# st.markdown(subtitle_section_3_5)
d_individuals_l = ['d_indiv_pledge']
d_individuals_n_d_individuals_pledge_status_l = ['d_indiv_number_pledge_2023',]
partner_name = ['InitName']
# Ensure the data is numeric
df_pledge[d_individuals_n_d_individuals_pledge_status_l] = df_pledge[d_individuals_n_d_individuals_pledge_status_l].apply(pd.to_numeric, errors='coerce')
df_pledge['d_individuals_n_d_individuals_pledge_status'] = df_pledge[d_individuals_n_d_individuals_pledge_status_l].notna().any(axis=1)
df_pledge.loc[df_pledge[d_individuals_n_d_individuals_pledge_status_l [0]] == 0, 'd_individuals_n_d_individuals_pledge_status'] = False
# st.write(df_pledge[partner_name + d_individuals_l + d_individuals_n_d_individuals_pledge_status_l+['d_individuals_n_d_individuals_pledge_status']])
#Number of Direct Individuals
# st.write("Number of Direct Individuals (sum)",df_pledge[d_individuals_n_d_individuals_pledge_status_l[0]].sum())
# st.write("Number of Direct Individuals (adjusted *0.75)", df_pledge[d_individuals_n_d_individuals_pledge_status_l[0]].sum()*0.75)

d_individuals_priority_groups_pledge_status_l = ['s' + str(i) for i in range(2513, 2523)]
df_pledge['d_individuals_priority_groups_pledge_status'] = df_pledge[d_individuals_priority_groups_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[d_individuals_l + d_individuals_priority_groups_pledge_status_l+['d_individuals_priority_groups_pledge_status']])

hazards_option_l = [
    'Water stress (urban focus)', 'Water stress (rural focus)', 'Extreme heat',
    'Extreme cold', 'Drought (agriculture focus)', 'Drought (other sectors)',
    'Urban flood', 'River flood', 'Coastal flood', 'Tropical Cyclone',
    'Snow, Ice', 'Wildfire', 'Extreme wind', 'Oceanic Events',
    'Other coastal events',]
d_individuals_hazards_pledge_status_all_types_hazard_l = ['s2523',]
d_individuals_hazards_pledge_status_l = ['s' + str(i) for i in range(2524, 2539)]  # Start from the next after "'All types of hazards' to exclude 'All types of hazards' & Others(please specify)
# Replace the value in each column with the corresponding hazard from hazards_option_l if the 'all types of hazards' column is 'All types of hazards'
for idx, col in enumerate(d_individuals_hazards_pledge_status_l):
    df_pledge[col] = df_pledge.apply(lambda row: hazards_option_l[idx] if row[d_individuals_hazards_pledge_status_all_types_hazard_l[0]] == 'All types of hazards' else row[col], axis=1)
d_individuals_hazards_pledge_status_l = ['s' + str(i) for i in range(2524, 2540)] #Adding Other to list
df_pledge['d_individuals_hazards_pledge_status'] = df_pledge[d_individuals_hazards_pledge_status_l].notna().any(axis=1)
# st.write(df_pledge[d_individuals_hazards_pledge_status_l+['d_individuals_hazards_pledge_status']])

d_individuals_continents_pledge_l = ['s' + str(i) for i in range(2540, 2546)]
df_pledge['d_individuals_continents_pledge'] = df_pledge[d_individuals_continents_pledge_l].notna().any(axis=1)
# st.write(df_pledge[d_individuals_continents_pledge_l+['d_individuals_continents_pledge']])

d_individuals_countries_pledge_status_l =['s' + str(i) for i in range(2546, 2732)]
df_pledge['d_individuals_countries_pledge_status'] = df_pledge[d_individuals_countries_pledge_status_l].notna().any(axis=1)
# st.write("Tabla Paises")
# st.write(df_pledge[d_individuals_countries_pledge_status_l+['d_individuals_countries_pledge_status']])
columns_to_display = ['InitName', 'd_individuals_countries_pledge_status'] + d_individuals_countries_pledge_status_l
df_countries_pledge_individuals = df_pledge[columns_to_display]
# st.write(df_countries_pledge_individuals)

d_individuals_capabily_country_level_pledge_l = ['s2732',]
df_pledge['d_individuals_capabily_country_level_pledge'] = df_pledge[d_individuals_capabily_country_level_pledge_l].notna().any(axis=1)
# st.write(df_pledge[d_individuals_capabily_country_level_pledge_l+['d_individuals_capabily_country_level_pledge']])

d_individuals_distribution_individuals_per_country_pledge_l = ['s' + str(i) for i in range(2733, 3105)]
df_pledge['d_individuals_distribution_individuals_per_country_pledge'] = df_pledge[d_individuals_distribution_individuals_per_country_pledge_l].notna().any(axis=1)
# st.write(df_pledge[d_individuals_distribution_individuals_per_country_pledge_l+['d_individuals_distribution_individuals_per_country_pledge']])
 
d_individuals_index_list_pledge =['d_individuals_n_d_individuals_pledge_status',
                                  'd_individuals_priority_groups_pledge_status',
                                  'd_individuals_hazards_pledge_status',
                                  'd_individuals_countries_pledge_status',]    
df_pledge.loc[df_pledge['d_indiv_pledge'].isna(), d_individuals_index_list_pledge] = False

## SUB INDEX INDIVIDUALS
weights = {
    'd_individuals_priority_groups_pledge_status':0.15,
    'd_individuals_hazards_pledge_status':0.05,
    'd_individuals_n_d_individuals_pledge_status':0.4,
    'd_individuals_countries_pledge_status':0.4,}

# Calculate the weighted sum of the components for d_individuals_pledge_sub_subidx
df_pledge['d_individuals_pledge_sub_subidx'] = df_pledge.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_pledge['d_individuals_pledge_sub_subidx'] = (df_pledge['d_individuals_pledge_sub_subidx'] * 100).astype(int)


## Indentifying info required
index_list = d_individuals_index_list_pledge
# Apply the function to each row
df_pledge['d_individuals_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)
df_pledge.loc[df_pledge['d_indiv_pledge'].isna(), 'd_individuals_pledge_req'] = "No Apply"

# Summary List d_individuals_pledge_all_list
d_individuals_pledge_responses_list = d_individuals_l + d_individuals_n_d_individuals_pledge_status_l
d_individuals_pledge_results_list  = ['d_individuals_pledge_sub_subidx','d_individuals_pledge_req',]           
d_individuals_pledge_sub_subidx_list = d_individuals_index_list_pledge
d_individuals_pledge_all_list = d_individuals_pledge_responses_list + d_individuals_pledge_results_list + d_individuals_pledge_sub_subidx_list
  ##
##  ##
 ##
## Confirm results sub index d_individuals_pledge_sub_subidx
# st.write('d_individuals Pledge Subidx',df_pledge[['InitName']+d_individuals_pledge_all_list])
 
 


## PRIMARY BENEFICIARIES ALL SUB INDEX
## Primary Beneficiaries Identification adjusted by index of responses
df_pledge.loc[df_pledge['d_individuals_pledge_sub_subidx'] == 0, 'd_indiv_pledge'] = np.nan
df_pledge.loc[df_pledge['companies_pledge_sub_subidx'] == 0, 'companies_pledge'] = np.nan
df_pledge.loc[df_pledge['regions_pledge_sub_subidx'] == 0, 'region_pledge'] = np.nan
df_pledge.loc[df_pledge['cities_pledge_sub_subidx'] == 0, 'cities_pledge'] = np.nan
df_pledge.loc[df_pledge['natsyst_pledge_sub_subidx'] == 0, 'natsyst_pledge'] = np.nan

#replacing 0 to nan
index_pledge_list = ['d_individuals_pledge_sub_subidx','companies_pledge_sub_subidx','regions_pledge_sub_subidx','cities_pledge_sub_subidx','natsyst_pledge_sub_subidx',]
for col in index_pledge_list:
    df_pledge.loc[df_pledge[col] == 0, col] = np.nan


## COUNTING NUMBER OF PRIMARY BENEFICIARIES FOR INDEX
pledge_p_beneficiaries_responses_list = ['p_benefic_pledge_concat','p_benefic_pledge_counts']

#PRIMARY BENEFICIARIES  SUB INDEX INDEX
indexes_beneficiaries_list_pledge = ['d_individuals_pledge_sub_subidx', 
                                     'companies_pledge_sub_subidx', 
                                     'regions_pledge_sub_subidx', 
                                     'cities_pledge_sub_subidx', 
                                     'natsyst_pledge_sub_subidx']
df_pledge['p_benefic_all_pledge_subidx'] = df_pledge[indexes_beneficiaries_list_pledge].sum(axis=1) / df_pledge['p_benefic_pledge_counts']
p_beneficiaries_list_pledge = ['p_benefic_pledge_concat','p_benefic_pledge_counts','p_benefic_all_pledge_subidx']

# st.write(df_pledge[['InitName','p_benefic_pledge_concat','p_benefic_pledge_counts'] + indexes_beneficiaries_list_pledge + ['p_benefic_all_pledge_subidx']])


p_benefic_all_pledge_req_list = ['d_individuals_pledge_req',
                                   'companies_pledge_req',
                                   'regions_pledge_req',
                                   'cities_pledge_req',
                                   'natsyst_pledge_req']

def concatenate_req_values_pledge(row):
    pending_values = []
    # Check each pair of conditions and concatenate the appropriate pending value
    if  0 < row['d_individuals_pledge_sub_subidx'] < 90:
        pending_values.append(row['d_individuals_pledge_req'])
    if  0 < row['companies_pledge_sub_subidx'] < 90:
        pending_values.append(row['companies_pledge_req'])
    if  0 < row['regions_pledge_sub_subidx'] < 90:
        pending_values.append(row['regions_pledge_req'])
    if  0 < row['cities_pledge_sub_subidx'] < 90:
        pending_values.append(row['cities_pledge_req'])
    if  0 < row['natsyst_pledge_sub_subidx'] < 90:
        pending_values.append(row['natsyst_pledge_req'])
    
    # Join the collected pending values with a separator, e.g., ", "
    return ', '.join(filter(None, pending_values))  # filter(None, ...) removes empty strings
# Apply the function to each row in the DataFrame to create the new column
df_pledge['p_benefic_all_pledge_req'] = df_pledge.apply(concatenate_req_values_pledge, axis=1)
df_pledge.loc[df_pledge['p_benefic_pledge_counts'] == 0, 'n_individuals_pledged_total_confidence'] = ""



### Pledge Metrics Relibility
# st.write('#Pledge Metrics Relibility')

metrics_individuals_pledge_confidence_list = ['n_individuals_pledged_total_confidence']
metrics_other_p_benific_pledge_confidence_list = ['companies_n_comp_pledge_confidence',
'cities_n_cit_pledge_confidence',
'region_n_reg_pledge_confidence',
'natsyst_n_hect_pledge_2023_confidence']

df_pledge['comp_cit_reg_naysys_pledged_confidence'] = df_pledge[metrics_other_p_benific_pledge_confidence_list].apply(
    lambda x: '; '.join([str(value) for value in x.dropna() if "Accepted" not in str(value)]),
    axis=1
)
required_pledge_list_to_rename = ['comp_cit_reg_naysys_pledged_confidence']
# Apply the replacement operation to each specified column
for col in required_pledge_list_to_rename:
    df_pledge[col] = df_pledge[col].astype(str).apply(lambda x: x.replace('No Apply', ''))
    df_pledge['comp_cit_reg_naysys_pledged_confidence'] = df_pledge['comp_cit_reg_naysys_pledged_confidence'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
# df_pledge[['n_individuals_pledged_total_confidence','comp_cit_reg_naysys_pledged_confidence']] 
comp_cit_reg_naysys_pledged_confidence_list = ['comp_cit_reg_naysys_pledged_confidence']

confidence_metrics_pledge_list = metrics_individuals_pledge_confidence_list + comp_cit_reg_naysys_pledged_confidence_list +  metrics_other_p_benific_pledge_confidence_list

# st.write('reliability metrics pledge')
# df_pledge[['InitName']+ confidence_metrics_pledge_list]

# Summary List p_benefic_all_pledge_all_list
p_benefic_all_individuals_n_total_confidence_list = ['individuals_n_total_pledge_2023','individuals_n_total_pledge_2022','n_individuals_pledged_total_confidence','comp_cit_reg_naysys_pledged_confidence'] 
p_benefic_all_pledge_responses_list = pledge_p_beneficiaries_responses_list
p_benefic_all_pledge_results_list  = ['p_benefic_all_pledge_subidx','p_benefic_all_pledge_req',]           
# p_benefic_all_pledge_subidx_list = indexes_beneficiaries_list_pledge
p_benefic_all_pledge_subidx_list = d_individuals_pledge_all_list + companies_pledge_all_list + regions_pledge_all_list + cities_pledge_all_list + natsyst_pledge_all_list
p_benefic_all_pledge_all_list = p_benefic_all_pledge_results_list + p_benefic_all_individuals_n_total_confidence_list  +p_benefic_all_pledge_responses_list + p_benefic_all_pledge_subidx_list
  ##
##  ##
 ##
## Confirm results sub index p_benefic_all_pledge_subidx
# st.write('p_beneficiaries Pledge Subidx',df_pledge[['InitName']+p_benefic_all_pledge_all_list])
 
 


## Hazards Treatment
## All Types of Hazards already treated before when making the index of completness for each primary beneficiary
#____HAZARDS  #Do not include option other
hazard_list_ind_pledge         = ['s' + str(i) for i in range(2524, 2539)]  # OK
hazard_list_comp_pledge        = ['s' + str(i) for i in range(47, 62)]  #ok
hazard_list_region_pledge      = ['s' + str(i) for i in range(679, 694)]  #ok
hazard_list_cities_pledge      = ['s' + str(i) for i in range(1299, 1314)]  #ok
hazard_list_nat_sys_pledge     = ['s' + str(i) for i in range(1912, 1927)]  #ok

df_pledge['hazards_ind_pledge_concat']           = df_pledge[hazard_list_ind_pledge].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1) #Concatenate
df_pledge['hazards_comp_pledge_concat']          = df_pledge[hazard_list_comp_pledge].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_pledge['hazards_region_pledge_concat']        = df_pledge[hazard_list_region_pledge].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_pledge['hazards_cities_pledge_concat']        = df_pledge[hazard_list_cities_pledge].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_pledge['hazards_nat_sys_pledge_concat']       = df_pledge[hazard_list_nat_sys_pledge].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)


hazards_all_pledge_l = ['hazards_ind_pledge_concat', 'hazards_comp_pledge_concat', 'hazards_region_pledge_concat', 'hazards_cities_pledge_concat', 'hazards_nat_sys_pledge_concat']

# Concatenating columns, removing NaNs, and stripping spaces
df_pledge['hazards_all_pledge_concat'] = df_pledge[hazards_all_pledge_l].apply(lambda x: ';'.join(x.dropna().astype(str)), axis=1)
# Filter out empty strings, remove duplicates, and ensure no leading "; "
df_pledge['hazards_all_pledge_concat'] = df_pledge['hazards_all_pledge_concat'].apply(lambda x: ';'.join(dict.fromkeys(filter(None, (i.strip() for i in x.split(';')))).keys()))
df_pledge['hazards_all_pledge_count'] = df_pledge['hazards_all_pledge_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
hazards_pledge_list = ['hazards_all_pledge_concat','hazards_all_pledge_count']
# st.markdown('Hazards Pledge')
# df_pledge['hazards_all_pledge_concat']



# title_section_4 = "# Principles for Locally Led Adaptation"
# subtitle_section_1 = "## 4.1) Commitment"
# st.markdown(title_section_4)
# st.markdown(subtitle_section_1)

description_locally_led_commitment = """Principles for Locally Led Adaptation 
In the forthcoming section, we delve into a critical aspect of enhancing resilience by endorsing Locally led adaptation principles. These principles aim to fundamentally transform the current top-down approaches into a novel model where local stakeholders are endowed with greater authority and resources to confront the challenges posed by climate change. 
You'll find a series of statements that outline different aspects of locally-led adaptation. We request you to evaluate your initiative's adherence to these principles by selecting from a range of 3 commitment levels. Your honest and thoughtful responses will help us better align our collective strategies and resources, and they're essential for fostering accountability and transparency within the RtR campaign. 
We appreciate your dedication to this pivotal component of resilience-building and thank you in advance for your detailed and honest feedback. 
Please review the Locally Led Adaptation principles here before answering the next question. 
4.1) Commitment 
1. To what extent are your initiative and its member organizations committed to the Principles for Locally Led Adaptation? 
○ Currently Under Review: Evaluation in Progress 
○ No Commitment: Not Aligned with Principles 
○ Mildly Committed: Partially Aligned with Principles 
○ Highly Committed: Fully Aligned and Actively Practicing Principles 
"""


rename = {'s3105':'locally_led_commitment',}
df_pledge = df_pledge.rename(columns = rename)

locally_led_commitment_pledge_l = ['locally_led_commitment',]
df_pledge.loc[df_pledge['survey2023_reviewed_pledge'] == False, locally_led_commitment_pledge_l] = np.nan
df_pledge['locally_led_commitment_pledge_status'] = df_pledge[locally_led_commitment_pledge_l].notna().any(axis=1)
df_pledge.loc[df_pledge[locally_led_commitment_pledge_l[0]] == 'Currently Under Review: Evaluation in Progress', 'locally_led_commitment_pledge_status'] = False
df_pledge['locally_led_commitment_pledge_subidx'] = df_pledge['locally_led_commitment_pledge_status'].apply(lambda x: 100 if x == True else 0)
locally_led_commitment_pledge_list = ['locally_led_commitment_pledge_status']

## Indentifying info required
index_list = locally_led_commitment_pledge_list
# Apply the function to each row
df_pledge['locally_led_commitment_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)

# Summary List locally_led_commitment_pledge_all_list
locally_led_commitment_pledge_responses_list = locally_led_commitment_pledge_l
locally_led_commitment_pledge_results_list  = ['locally_led_commitment_pledge_subidx','locally_led_commitment_pledge_req',]           
locally_led_commitment_pledge_subidx_list = locally_led_commitment_pledge_list
locally_led_commitment_pledge_all_list = locally_led_commitment_pledge_responses_list + locally_led_commitment_pledge_results_list + locally_led_commitment_pledge_subidx_list
##
##  ##
##
## Confirm results sub index locally_led_commitment_pledge_subidx
# st.write('locally_led_commitment Pledge Subidx',df_pledge[['InitName']+locally_led_commitment_pledge_all_list])


# title_section_5 = "# Section 5: Mobilization of Financial Resources"
# subtitle_section_5_1 = "## 5.1) Amount of Financial Resources"
# st.markdown(title_section_5)
# st.markdown(subtitle_section_5_1)
rename = {'s3106':'commit_secure_finance_pledge',}
df_pledge = df_pledge.rename(columns = rename)

# st.markdown("Does the initiative, in relation to its members, commit to secure a specific amount of financial resources by 2030 to fulfill this pledge?")
commit_secure_financial_resources_pledge_l = ['commit_secure_finance_pledge',]
df_pledge.loc[df_pledge['survey2023_reviewed_pledge'] == False, commit_secure_financial_resources_pledge_l] = np.nan
# st.write(df_pledge[commit_secure_financial_resources_pledge_l])
df_pledge['commit_secure_financial_resources_pledge_status'] = df_pledge[commit_secure_financial_resources_pledge_l].notna().any(axis=1)
df_pledge['commit_secure_financial_resources_pledge_subidx'] = df_pledge['commit_secure_financial_resources_pledge_status'].apply(lambda x: 100 if x == True else 0)
# st.write(df_pledge[commit_secure_financial_resources_pledge_l+['commit_secure_financial_resources_pledge_status', 'commit_secure_financial_resources_pledge_subidx']])

# st.markdown("Amount of money anticipated to be mobilized as part of the pledge (in USD)")
rename = {'s3107':'amount_of_finance_anticipated_pledge',}
df_pledge = df_pledge.rename(columns = rename)

amount_of_financial_resources_pledge_l = ['amount_of_finance_anticipated_pledge',]
df_pledge[amount_of_financial_resources_pledge_l] = df_pledge[amount_of_financial_resources_pledge_l].apply(pd.to_numeric, errors='coerce')
df_pledge['amount_of_financial_resources_pledge_status'] = df_pledge[amount_of_financial_resources_pledge_l].notna().any(axis=1)
df_pledge.loc[df_pledge[amount_of_financial_resources_pledge_l[0]] == 0, 'amount_of_financial_resources_pledge_status'] = False
# st.write(df_pledge[amount_of_financial_resources_pledge_l+['amount_of_financial_resources_pledge_status']])

# st.markdown("Please add any comments about the amount of money anticipated to be mobilized as part of the pledge (in USD)")
rename = {'s3108':'amount_of_finance_anticipated_comms_pledge',}
df_pledge = df_pledge.rename(columns = rename)
amount_of_financial_resources_pledge_comments_l = ['amount_of_finance_anticipated_comms_pledge',]
df_pledge['amount_of_financial_resources_pledge_comms_status'] = df_pledge[amount_of_financial_resources_pledge_comments_l].notna().any(axis=1)
# st.write(df_pledge[amount_of_financial_resources_pledge_comments_l+['amount_of_financial_resources_pledge_comms_status']])

df_pledge.loc[df_pledge['commit_secure_finance_pledge'] == 'No', 'amount_of_financial_resources_pledge_status'] = True
df_pledge.loc[df_pledge['commit_secure_finance_pledge'] == 'No', 'amount_of_financial_resources_pledge_comms_status'] = True

finance_pledge_details_list =['commit_secure_financial_resources_pledge_status',
                              'amount_of_financial_resources_pledge_status',
                              'amount_of_financial_resources_pledge_comms_status']

weights = {
    'commit_secure_financial_resources_pledge_status':0.25,
    'amount_of_financial_resources_pledge_status':0.7,
    'amount_of_financial_resources_pledge_comms_status':0.05,}

# Calculate the weighted sum of the components for finance_pledge_subidx
df_pledge['finance_pledge_subidx'] = df_pledge.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_pledge['finance_pledge_subidx'] = (df_pledge['finance_pledge_subidx'] * 100).astype(int)
df_pledge.loc[df_pledge['commit_secure_finance_pledge'] == 'No', 'finance_pledge_subidx'] = 100

## Indentifying info required
index_list = finance_pledge_details_list
# Apply the function to each row
df_pledge['finance_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)

# Summary List finance_pledge_all_list
finance_pledge_responses_list = commit_secure_financial_resources_pledge_l + amount_of_financial_resources_pledge_l + amount_of_financial_resources_pledge_comments_l
finance_pledge_results_list  = ['finance_pledge_subidx','finance_pledge_req',]           
finance_pledge_subidx_list = finance_pledge_details_list
finance_pledge_all_list = finance_pledge_responses_list + finance_pledge_results_list + finance_pledge_subidx_list
## Confirm results sub index finance_pledge_subidx
  ##
##  ##
 ##
# st.write('finance Pledge Subidx',df_pledge[['InitName']+finance_pledge_all_list])
 
 

 

title_section_6 = "# Section 6: Key fundamentals. Understanding Your 2030 Pledge"
# st.markdown(title_section_6)
subtitle_section_6_1 = "## 6.1) Explanation for numbers reported" ## Sub Index metrics_explanation_pledge_subidx
# st.markdown(subtitle_section_6_1)
# st.markdown("Please briefly explain the process you used to calculate or determine the number of individuals who will benefit from your initiative as part of your 2030 pledge?")
rename = {'s3109':'metrics_explanation_pledge',}
df_pledge = df_pledge.rename(columns = rename)
explanation_for_numbers_reported_pledge_l = ['metrics_explanation_pledge',]
df_pledge['metrics_explanation_pledge_status'] = df_pledge[explanation_for_numbers_reported_pledge_l].notna().any(axis=1)
explanation_not_enough_list = ['tbd','will add later']
condition = df_pledge[explanation_for_numbers_reported_pledge_l[0]].isin(explanation_not_enough_list)
df_pledge.loc[condition, 'metrics_explanation_pledge_status'] = False
df_pledge['metrics_explanation_pledge_subidx'] = df_pledge['metrics_explanation_pledge_status'].apply(lambda x: 100 if x else 0)
metrics_explanation_pledge_list = ['metrics_explanation_pledge_subidx']
# st.write(df_pledge[explanation_for_numbers_reported_pledge_l + ['metrics_explanation_pledge_status', 'metrics_explanation_pledge_subidx']])

## Indentifying info required
index_list = ['metrics_explanation_pledge_status']
# Apply the function to each row
df_pledge['metrics_explanation_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)
# df_pledge['metrics_explanation_pledge_req']


# Summary List metrics_explanation_pledge_all_list
metrics_explanation_pledge_responses_list = explanation_for_numbers_reported_pledge_l 
metrics_explanation_pledge_results_list  = ['metrics_explanation_pledge_subidx','metrics_explanation_pledge_req',]           
metrics_explanation_pledge_subidx_list = ['metrics_explanation_pledge_status']
metrics_explanation_pledge_all_list = metrics_explanation_pledge_responses_list + metrics_explanation_pledge_results_list + metrics_explanation_pledge_subidx_list
## Confirm results sub index metrics_explanation_pledge_subidx
  ##
##  ##
 ##
# st.write('metrics_explanation Pledge Subidx',df_pledge[['InitName']+metrics_explanation_pledge_all_list])
 



subtitle_section_6_2 = "## 6.2) Climate risk assessment"  ## Sub Index climate_risk_assessment_pledge_subidx
# st.markdown(subtitle_section_6_2)
# st.markdown("Is your pledge based on a climate risk assessment?"

info_climate_risk_assess = """6.2) Climate risk assessment 
2. Is your pledge based on a climate risk assessment? Please indicate if 
you used any type of risk assessment to elaborate this pledge. This includes evaluating risk components, as outlined in the “Risk Assessment” concept in the Glossary below. 
3. Please upload documentation to support your risk assessment 
6.3) Diagnostics assessment 
4. Is your pledge based on a diagnosis of the need and vulnerability of your target beneficiaries? Please indicate if you used any type of vulnerability diagnosis of your target beneficiaries, apart or instead of a risk assessment, as we understand that this could be included in the previous answer. 
5. If you have any document explaining your diagnostics and/or its results, please upload it. If you have any documentation that provides deeper insight into your diagnosis, please share it with us. """


rename = {'s3110':'climate_risk_assess_explan_pledge',}
df_pledge = df_pledge.rename(columns = rename)
climate_risk_assessment_pledge_l = ['climate_risk_assess_explan_pledge',]
df_pledge.loc[df_pledge['survey2023_reviewed_pledge'] == False, climate_risk_assessment_pledge_l] = np.nan
df_pledge['climate_risk_assess_pledge_status'] = df_pledge[climate_risk_assessment_pledge_l].notna().any(axis=1)
# st.write(df_pledge[climate_risk_assessment_pledge_l + ['climate_risk_assess_pledge_status']])

rename = {'s3111':'climate_risk_assess_explan_other_pledge',}
df_pledge = df_pledge.rename(columns = rename)
climate_risk_assessment_pledge_other_l = ['climate_risk_assess_explan_other_pledge',]
df_pledge['climate_risk_assess_pledge_other_status'] = df_pledge[climate_risk_assessment_pledge_other_l].notna().any(axis=1)
climate_risk_assessment_not_enough_list = ['will add later','Not clear what this question is targeting']
condition = df_pledge[climate_risk_assessment_pledge_other_l[0]].isin(climate_risk_assessment_not_enough_list)
df_pledge.loc[condition, 'climate_risk_assess_pledge_other_status'] = False
# st.write(df_pledge[climate_risk_assessment_pledge_other_l +['climate_risk_assess_pledge_other_status']])

rename = {'s3112':'climate_risk_assess_upload_pledge',}
df_pledge = df_pledge.rename(columns = rename)
climate_risk_assessment_pledge_upload_l = ['climate_risk_assess_upload_pledge',]
df_pledge['climate_risk_assess_upload_pledge_status'] = df_pledge[climate_risk_assessment_pledge_upload_l].notna().any(axis=1)
# st.write(df_pledge[climate_risk_assessment_pledge_upload_l+['climate_risk_assess_upload_pledge_status']])

# Apply conditions and modify 'climate_risk_assess_pledge_status' only if conditions are met, else keep original value
df_pledge['climate_risk_assess_pledge_status'] = np.where(
    (df_pledge['climate_risk_assess_explan_pledge'] == 'None of the listed answers fit (please specify)') &
    (df_pledge['climate_risk_assess_explan_other_pledge'].isna()),
    False,  # Set to False if conditions are met
    df_pledge['climate_risk_assess_pledge_status']  # Keep original value otherwise
)

climate_risk_pledge_list_to_index =['climate_risk_assess_pledge_status', 
                                    'climate_risk_assess_pledge_other_status',
                                    'climate_risk_assess_upload_pledge_status']

weights = {
    'climate_risk_assess_pledge_status':0.91,
    'climate_risk_assess_pledge_other_status':0.06,
    'climate_risk_assess_upload_pledge_status':0.03,}

# Calculate the weighted sum of the components for climate_risk_assess_pledge_subidx
df_pledge['climate_risk_assess_pledge_subidx'] = df_pledge.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_pledge['climate_risk_assess_pledge_subidx'] = (df_pledge['climate_risk_assess_pledge_subidx'] * 100).astype(int)

## Indentifying info required
index_list = climate_risk_pledge_list_to_index
# Apply the function to each row
df_pledge['climate_risk_assess_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)

# Summary List climate_risk_assess_pledge_all_list
climate_risk_assess_pledge_responses_list = climate_risk_assessment_pledge_l + climate_risk_assessment_pledge_other_l
climate_risk_assess_pledge_results_list  = ['climate_risk_assess_pledge_subidx','climate_risk_assess_pledge_req',]           
climate_risk_assess_pledge_subidx_list = climate_risk_pledge_list_to_index
climate_risk_assess_pledge_all_list = climate_risk_assess_pledge_responses_list + climate_risk_assess_pledge_results_list + climate_risk_assess_pledge_subidx_list
## Confirm results sub index climate_risk_assess_pledge_subidx
  ##
##  ##
 ##
# st.write('climate_risk_assess Pledge Subidx',df_pledge[['InitName']+climate_risk_assess_pledge_all_list])
 
 
# options_climate_risk_list = [
#     "Yes, we've done a detailed climate risk assessment for each community/company/territory in our initiative",
#     "We've assessed risks using global data, not specific to our target community/company/territory",
#     "We haven't done our own assessment but we use an external source for risk data",
#     "We plan to assess risks before starting our actions but haven't yet",
#     "We haven't and don't plan to assess climate risks at all" ]

subtitle_section_6_3 = "## 6.3) Diagnostics assessment"  ## Sub Index diagnostic_pledge_subidx
# st.markdown(subtitle_section_6_3)
# st.markdown('Is your pledge based on a diagnostics on the need and vulnerability of your target beneficiaries?')

info_climate_diagnost = """6.3) Diagnostics assessment 
4. Is your pledge based on a diagnosis of the need and vulnerability of your target beneficiaries? Please indicate if you used any type of vulnerability diagnosis of your target beneficiaries, apart or instead of a risk assessment, as we understand that this could be included in the previous answer. 
5. If you have any document explaining your diagnostics and/or its results, please upload it. If you have any documentation that provides deeper insight into your diagnosis, please share it with us. 
"""

rename = {'s3113':'climate_diagnost_explan_pledge',}
df_pledge = df_pledge.rename(columns = rename)
climate_diagnost_pledge_l = ['climate_diagnost_explan_pledge',]
df_pledge['climate_diagnost_pledge_status'] = df_pledge[climate_diagnost_pledge_l].notna().any(axis=1)
# st.write(df_pledge[climate_diagnost_pledge_l+['climate_diagnost_pledge_status']])

rename = {'s3114':'climate_diagnost_explan_other_pledge',}
df_pledge = df_pledge.rename(columns = rename)
climate_diagnost_pledge_other_l = ['climate_diagnost_explan_other_pledge',]
df_pledge['climate_diagnost_pledge_other_status'] = df_pledge[climate_diagnost_pledge_other_l].notna().any(axis=1)
diagnotis_not_enough_list = ['will add later']
condition = df_pledge[climate_diagnost_pledge_other_l[0]].isin(diagnotis_not_enough_list)
df_pledge.loc[condition, 'climate_diagnost_pledge_other_status'] = False
# st.write(df_pledge[climate_diagnost_pledge_other_l+['climate_diagnost_pledge_other_status']])

rename = {'s3115':'climate_diagnost_upload_pledge',}
df_pledge = df_pledge.rename(columns = rename)
climate_diagnost_pledge_upload_l = ['climate_diagnost_upload_pledge',]
df_pledge['climate_diagnost_pledge_upload_status'] = df_pledge[climate_diagnost_pledge_upload_l].notna().any(axis=1)
# st.write(df_pledge[climate_diagnost_pledge_upload_l+['climate_diagnost_pledge_upload_status']])

# Apply conditions and modify 'climate_diagnost_pledge_status' only if conditions are met, else keep original value
df_pledge['climate_diagnost_pledge_status'] = np.where(
    (df_pledge['climate_diagnost_explan_pledge'] == 'None of the above (please specify)') &
    (df_pledge['climate_diagnost_explan_other_pledge'].isna()),
    False,  # Set to False if conditions are met
    df_pledge['climate_diagnost_pledge_status']  # Keep original value otherwise
)

climate_diagnostic_pledge_list_to_index =['climate_diagnost_pledge_status', 
                                  'climate_diagnost_pledge_other_status',
                                  'climate_diagnost_pledge_upload_status']

weights = {
    'climate_diagnost_pledge_status':0.91,
    'climate_diagnost_pledge_other_status':0.06,
    'climate_diagnost_pledge_upload_status':0.03,}

# Calculate the weighted sum of the components for climate_diagnost_pledge_subidx
df_pledge['climate_diagnost_pledge_subidx'] = df_pledge.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_pledge['climate_diagnost_pledge_subidx'] = (df_pledge['climate_diagnost_pledge_subidx'] * 100).astype(int)

## Indentifying info required
index_list = climate_diagnostic_pledge_list_to_index
# Apply the function to each row
df_pledge['climate_diagnost_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)

# Summary List climate_diagnostic_assess_pledge_all_list
climate_diagnostic_assess_pledge_responses_list = climate_diagnost_pledge_l + climate_diagnost_pledge_other_l
climate_diagnostic_assess_pledge_results_list  = ['climate_diagnost_pledge_subidx','climate_diagnost_pledge_req',]           
climate_diagnost_pledge_subidx_list = climate_diagnostic_pledge_list_to_index
climate_diagnostic_assess_pledge_all_list = climate_diagnostic_assess_pledge_responses_list + climate_diagnostic_assess_pledge_results_list + climate_diagnost_pledge_subidx_list
## Confirm results sub index climate_diagnost_pledge_subidx
  ##
##  ##
 ##
# st.write('Climate_diagnostic Pledge Subidx',df_pledge[['InitName']+climate_diagnostic_assess_pledge_all_list])


# options_diagnotic_list = ["Yes, we have performed a full-fledged diagnostics on each community/business/territory we aim to target with our initiative.",
#     "We have performed a diagnostics, but only based on global data, not on the specific needs of each target community/business/territory.",
#     "We have not performed diagnostics yet, but we aim to do that before we start implementing our actions.",
#     "We have not performed nor we aim to perform any diagnostics of need and/or vulnerability.",]



subtitle_section_6_4 = "## 6.4) Consultation of members"  ## SUB Index members_consultation_pledge_subidx
# st.markdown(subtitle_section_6_4)
# st.markdown('Have you consulted your members to prepare this pledge statement?')

rename = {'s3116':'members_consultation_pledge',}
df_pledge = df_pledge.rename(columns = rename)
consultation_of_members_pledge_l = ['members_consultation_pledge',]
# df_pledge = df_pledge.replace(["None of the above (please specify)", ""], np.nan)
df_pledge['consultation_of_members_pledge_status'] = df_pledge[consultation_of_members_pledge_l].notna().any(axis=1)
# st.write(df_pledge[consultation_of_members_pledge_l+['consultation_of_members_pledge_status']])

rename = {'s3117':'members_consultation_other_pledge',}
df_pledge = df_pledge.rename(columns = rename)
consultation_of_members_pledge_other_l = ['members_consultation_other_pledge',]
df_pledge['consultation_of_members_pledge_other_status'] = df_pledge[consultation_of_members_pledge_other_l].notna().any(axis=1)
members_not_enough_list = ['will add later']
condition = df_pledge[consultation_of_members_pledge_other_l[0]].isin(members_not_enough_list)
df_pledge.loc[condition, 'consultation_of_members_pledge_other_status'] = False
# st.write(df_pledge[consultation_of_members_pledge_other_l+['consultation_of_members_pledge_other_status']])

# Apply conditions and modify 'consultation_of_members_pledge_status' only if conditions are met, else keep original value
df_pledge['consultation_of_members_pledge_status'] = np.where(
    (df_pledge['members_consultation_pledge'] == 'None of the above (please specify)') &
    (df_pledge['members_consultation_other_pledge'].isna()),
    False,  # Set to False if conditions are met
    df_pledge['consultation_of_members_pledge_status']  # Keep original value otherwise
)

members_consultation_pledge_list_to_index = ['consultation_of_members_pledge_status',]

weights = {
    'consultation_of_members_pledge_status':1,}

# Calculate the weighted sum of the components for members_consultation_pledge_subidx
df_pledge['members_consultation_pledge_subidx'] = df_pledge.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_pledge['members_consultation_pledge_subidx'] = (df_pledge['members_consultation_pledge_subidx'] * 100).astype(int)


## Indentifying info required
index_list = members_consultation_pledge_list_to_index
# Apply the function to each row
df_pledge['members_consultation_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)




## Reliability of the Pledge Based in if it included Members in the making of the pledge. It is supposed to be a participatory process
# df_pledge['members_consultation_pledge_confidence'] =[]
options_members_consultation = ["Yes, they have been asked to fill in a pledge statement of their own which we used to prepare our aggregate statement.",]
condition = df_pledge['members_consultation_pledge'].isin(options_members_consultation)
df_pledge.loc[condition, 'members_consultation_pledge_confidence'] = "High Reliability: Pledge completed in consultation with members."

options_members_consultation = ["Yes, they have been consulted, but have not yet been asked to fill in a formal pledge statement to us. We understand we may need to update our pledge when we receive more information from our members.",]
condition = df_pledge['members_consultation_pledge'].isin(options_members_consultation)
df_pledge.loc[condition, 'members_consultation_pledge_confidence'] = "Medium Reliability: Pledge partially completed in consultation with members. The Pledge is expected to be updated."

options_members_consultation = ["No, but we will consult them to validate this pledge and update it accordingly.",]
condition = df_pledge['members_consultation_pledge'].isin(options_members_consultation)
df_pledge.loc[condition, 'members_consultation_pledge_confidence'] = "Medium-Low Reliability: Pledge has not been consulted with members. Need to validate with members and update the report."

options_members_consultation = ["None of the above (please specify)",]
condition = df_pledge['members_consultation_pledge'].isin(options_members_consultation)
df_pledge.loc[condition, 'members_consultation_pledge_confidence'] = "Medium-Low Reliability: Pledge has not been consulted with members. Need to confirm the validation with members and update the report."
df_pledge['members_consultation_pledge_confidence'] = df_pledge['members_consultation_pledge_confidence'].fillna("Low Reliability: No information available if pledge was completed in consultation with members.")

# Summary List members_consultation_assess_pledge_all_list
members_consultation_assess_pledge_responses_list = consultation_of_members_pledge_l + consultation_of_members_pledge_other_l
members_consultation_assess_pledge_results_list  = ['members_consultation_pledge_subidx','members_consultation_pledge_confidence','members_consultation_pledge_req',]           
members_consultation_pledge_list_to_index = members_consultation_pledge_list_to_index
members_consultation_assess_pledge_all_list = members_consultation_assess_pledge_responses_list + members_consultation_assess_pledge_results_list + members_consultation_pledge_list_to_index
## Confirm results sub index climate_diagnost_pledge_subidx
  ##
##  ##
 ##
# st.write('members_consultation Pledge Subidx & Confidence',df_pledge[['InitName']+members_consultation_assess_pledge_all_list])


subtitle_section_6_5 = "## 6.5) Confirmation of Future Plan Submission"  ## SUB Index confirmation_future_plans_pledge_subidx
# st.markdown(subtitle_section_6_5)

info_future_plan = """6.5) Confirmation of Future Plan Submission 
The "Plan Submission" dimension assesses and facilitates organizations' readiness to finalize and present their plan statements, The plan should include specific actions, delivery timelines, and expected beneficiaries. It gauges their progress and projected timelines, offers a feedback mechanism, and ensures a more responsive and supportive framework. Because developing comprehensive plans can be a time-intensive process, this dimension serves as a checkpoint to gauge where organizations are in their journey of commitment and preparation. 
Questions and Guidelines: 
1. Are you ready to submit your Plan Statement? This question seeks to understand the status of the different partners for the upcoming stage of reporting so we can provide support and guidance for those who need it. 
2. When do you expect you will be ready to submit your Plan statement? Providing an estimated time frame is relevant for us to understand the status of the partners for the upcoming “Plan Reporting Stage” 
3. Please provide a brief comment on how you are progressing to build a Plan statement This question seeks to understand any advances for the Plan Submission, including progress in specific actions to implement, timelines, and estimation of beneficiaries, among others. 
"""

# st.markdown('Are you ready to submit your Plan Statement?')
rename = {'s3118':'confirmation_of_future_plan_pledge',}
df_pledge = df_pledge.rename(columns = rename)
confirmation_of_future_plan_submission_pledge_l = ['confirmation_of_future_plan_pledge',]
df_pledge['confirmation_of_future_plan_submission_pledge_status'] = df_pledge[confirmation_of_future_plan_submission_pledge_l].notna().any(axis=1)
# st.write(df_pledge[confirmation_of_future_plan_submission_pledge_l+['confirmation_of_future_plan_submission_pledge_status']])

rename = {'s3119':'confirmation_of_future_plan_when_pledge',}
df_pledge = df_pledge.rename(columns = rename)
confirmation_of_future_plan_submission_pledge_when_l = ['confirmation_of_future_plan_when_pledge',]
df_pledge['confirmation_of_future_plan_submission_pledge_when_status'] = df_pledge[confirmation_of_future_plan_submission_pledge_when_l].notna().any(axis=1)
# st.write(df_pledge[confirmation_of_future_plan_submission_pledge_when_l+['confirmation_of_future_plan_submission_pledge_when_status']])

rename = {'s3120':'confirmation_of_future_plan_how_pledge',}
df_pledge = df_pledge.rename(columns = rename)
confirmation_of_future_plan_submission_pledge_how_l = ['confirmation_of_future_plan_how_pledge',]
df_pledge['confirmation_of_future_plan_submission_pledge_how_status'] = df_pledge[confirmation_of_future_plan_submission_pledge_how_l].notna().any(axis=1)
confirmation_plan_not_enough_list = ['will add later','-']
condition = df_pledge[confirmation_of_future_plan_submission_pledge_how_l[0]].isin(confirmation_plan_not_enough_list)
df_pledge.loc[condition, 'confirmation_of_future_plan_submission_pledge_how_status'] = False
# st.write(df_pledge[confirmation_of_future_plan_submission_pledge_how_l+['confirmation_of_future_plan_submission_pledge_how_status']])

confirmation_plan_list_to_index = ['confirmation_of_future_plan_submission_pledge_status','confirmation_of_future_plan_submission_pledge_when_status','confirmation_of_future_plan_submission_pledge_how_status']
df_pledge['confirmation_future_plans_pledge_subidx'] = (df_pledge[confirmation_plan_list_to_index].mean(axis=1) * 100).astype(int)

## Indentifying info required
index_list = confirmation_plan_list_to_index
# Apply the function to each row
df_pledge['confirmation_future_plans_pledge_req'] = df_pledge.apply(identify_req_status, axis=1)

# Summary List confirmation_future_plans_pledge_all_list
confirmation_future_plans_pledge_responses_list = confirmation_of_future_plan_submission_pledge_l + confirmation_of_future_plan_submission_pledge_when_l + confirmation_of_future_plan_submission_pledge_how_l
confirmation_future_plans_pledge_results_list  = ['confirmation_future_plans_pledge_subidx','confirmation_future_plans_pledge_req',]           
confirmation_future_plans_pledge_list_to_index = confirmation_plan_list_to_index
confirmation_future_plans_pledge_all_list = confirmation_future_plans_pledge_responses_list + confirmation_future_plans_pledge_results_list + confirmation_future_plans_pledge_list_to_index
## Confirm results sub index climate_diagnost_pledge_subidx
  ##
##  ##
 ##
# st.write('confirmation_future_plans Pledge Subidx',df_pledge[['InitName']+confirmation_future_plans_pledge_all_list])




# title_section_7 = "## Section 7: Confirmation of Pledge Statement 2023"
# subtitle_section_7_1 = "## 7.1) Confirmation"
# subtitle_section_7_2 = "## 7.2) Last Comments"
# st.markdown(title_section_7)
# st.markdown(subtitle_section_7_1)
# st.markdown("Do you confirm that the statements made in this survey represent the pledges for the initiative, updated for 2023?")
confirmation_of_responses_after_pre_filling_by_ts_pledge_l = ['s3121',]
# st.write(df_pledge[confirmation_of_responses_after_pre_filling_by_ts_pledge_l])

df_pledge['confirmation_responses_2023'] = df_pledge[confirmation_of_responses_after_pre_filling_by_ts_pledge_l].notna().any(axis=1)
# st.write(df_pledge[confirmation_of_responses_after_pre_filling_by_ts_pledge_l+['confirmation_responses_2023']])

# st.markdown(subtitle_section_7_2)
last_comment_pledge_l = ['s3122',]
df_pledge['last_comment_pledge'] = df_pledge[last_comment_pledge_l].notna().any(axis=1)
# st.write(df_pledge[last_comment_pledge_l+['last_comment_pledge']])


#PLEDGE OVERALL INDEX
pledge_overall_index_list = ['responder_id_pledge_subidx',
                             'p_benefic_all_pledge_subidx',
                             'locally_led_commitment_pledge_subidx',
                             'finance_pledge_subidx',
                             'metrics_explanation_pledge_subidx',
                             'climate_risk_assess_pledge_subidx',
                             'climate_diagnost_pledge_subidx',
                             'members_consultation_pledge_subidx',
                             'confirmation_future_plans_pledge_subidx',]

# Replace np.nan values with 0 in the specified columns of df_pledge
df_pledge[pledge_overall_index_list] = df_pledge[pledge_overall_index_list].fillna(0)

weights = {
    'responder_id_pledge_subidx':0.033333333,
    'p_benefic_all_pledge_subidx':0.333333333,
    'locally_led_commitment_pledge_subidx':0.055555556,
    'finance_pledge_subidx':0.111111111,
    'metrics_explanation_pledge_subidx':0.111111111,
    'climate_risk_assess_pledge_subidx':0.111111111,
    'climate_diagnost_pledge_subidx':0.111111111,
    'members_consultation_pledge_subidx':0.111111111,
    'confirmation_future_plans_pledge_subidx':0.022222222,
    }

# Calculate the weighted sum of the components for pledge_completeness_idx
df_pledge['pledge_completeness_idx'] = df_pledge.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)

#Adjustment to avoid % of completeness when "please complete" is present in the reporting tool
df_pledge.loc[df_pledge['pledge_completeness_idx'] < 2, 'pledge_completeness_idx'] = 0


# st.write("IMPORTANT PLEDGE")
# df_pledge[['InitName','pledge_completeness_idx']+pledge_overall_index_list] 



### Pledge Completeness Status order by Proirity pledge_completeness_status and pledge_completeness_req_priority
df_pledge['pledge_completeness_status'] = np.where(df_pledge['pledge_completeness_idx'] > 90, "Accepted", "Awaiting Completion")




required_pledge_list_prioritized = ['p_benefic_all_pledge_req',
                                    'members_consultation_pledge_req',
                                    'metrics_explanation_pledge_req',
                                    'finance_pledge_req',
                                    'climate_risk_assess_pledge_req',
                                    'climate_diagnost_pledge_req',
                                    'locally_led_commitment_pledge_req',
                                    'responder_id_pledge_req',
                                    'confirmation_future_plans_pledge_req']
                                    
                                    
df_pledge['pledge_completeness_req_priority'] = df_pledge.apply(
    lambda row: '; '.join(filter(None, [str(row[col]) for col in required_pledge_list_prioritized if pd.notnull(row[col])])), axis=1)


required_pledge_list_to_rename = ['pledge_completeness_req_priority']+required_pledge_list_prioritized

# Apply the replacement operation to each specified column
for col in required_pledge_list_to_rename:
    df_pledge[col] = df_pledge[col].astype(str).apply(lambda x: x.replace('_pledge  _status', ''))
    
for col in required_pledge_list_to_rename:
    df_pledge[col] = df_pledge[col].astype(str).apply(lambda x: x.replace('_status', ''))
    
for col in required_pledge_list_to_rename:
    df_pledge[col] = df_pledge[col].astype(str).apply(lambda x: x.replace('_subidx', '_info'))

for col in required_pledge_list_to_rename:
    df_pledge[col] = df_pledge[col].astype(str).apply(lambda x: x.replace('_pledge', ''))
    
for col in required_pledge_list_to_rename:
    df_pledge[col] = df_pledge[col].astype(str).apply(lambda x: x.replace(', ;', ';'))


def concatenate_req_values_final_pledge(row):
    pending_values = []
    # Check condition and concatenate the appropriate pending value
    if row['p_benefic_all_pledge_subidx'] <= 90:
        pending_values.append(row['p_benefic_all_pledge_req'])
    if row['members_consultation_pledge_subidx'] <= 90:
        pending_values.append(row['members_consultation_pledge_req'])
    if row['metrics_explanation_pledge_subidx'] <= 90:
        pending_values.append(row['metrics_explanation_pledge_req'])
    if row['finance_pledge_subidx'] <= 90:
        pending_values.append(row['finance_pledge_req'])
    if row['climate_risk_assess_pledge_subidx'] <= 90:
        pending_values.append(row['climate_risk_assess_pledge_req'])
    if row['climate_diagnost_pledge_subidx'] <= 90:
        pending_values.append(row['climate_diagnost_pledge_req'])
    if row['locally_led_commitment_pledge_subidx'] <= 90:
        pending_values.append(row['locally_led_commitment_pledge_req'])
    if row['responder_id_pledge_subidx'] <= 90:
        pending_values.append(row['responder_id_pledge_req'])
    if row['confirmation_future_plans_pledge_subidx'] <= 90:
        pending_values.append(row['confirmation_future_plans_pledge_req'])
    
    # Join the collected pending values with a separator, e.g., ", "
    return ', '.join(filter(None, pending_values))  # filter(None, ...) removes empty strings

df_pledge['pledge_completeness_req_priority'] = df_pledge.apply(concatenate_req_values_final_pledge, axis=1)
# df_pledge['pledge_completeness_req_priority']

## Renaming Codes to Real Questions
real_questions_pledge_dict = {
    "consultation_of_members":"Consultation of Members: 'Have you consulted your members to prepare this pledge statement?'",
    "commit_secure_financial_resources":"Finance: 'Does the initiative, in relation to its members, commit to secure a specific amount of financial resources by 2030 to fulfill this pledge?'",
    "companies_n_individuals":"Number of Individuals Beneficiaries through Companies: 'Taking into consideration the specific individuals you've previously indicated in this section, how many individual beneficiaries through these companies does your initiative pledge to make more resilient against climatic hazards?'",
    "amount_of_financial_resources":"Amount USD mobilized as part of Pledge: 'Amount of money anticipated to be mobilized as part of the pledge (in USD)'",
    "metrics_explanation":"Metrics Explanation: 'Please briefly explain the process you used to calculate or determine the number of individuals who will benefit from your initiative as part of your 2030 pledge?'",
    "natsyst_hazards":"Natural Systems Hazards: 'Against which of these hazards does your initiative aim to provide resilience? Select all that apply'",
    "responder_email":"Email: 'Survey Responder's Email Address'",
    "amount_of_financial_resources_comms":"Amount USD Mobilized as part of Pledge: 'Please add any comments about the amount of money anticipated to be mobilized as part of the pledge (in USD)'",
    "companies_types_of_individuals":"Types of Individuals Beneficiaries through Companies: 'What kind of groups of individuals benefit from making these companies more resilient? Please select all that apply.'",
    "regions_hazards":"Regions Hazards: 'For these regional beneficiaries, which specific climatic hazards does your 2030 pledge aim to provide resilience against? Please select all that apply.'",
    "companies_n_companies":"Number of Companies: 'For analytical clarity and reliability in calculations, please provide the number of companies your initiative aims to make more resilient as a numeric value.'",
    "d_individuals_priority_groups":"Prioritity Groups of Direct Individuals: 'How much is the impact of your action specifically targeted to each of the following priority groups?'",
    "confirmation_of_future_plan_submission_how":"Future Plan Submission: 'Please provide a brief comment on how you are progressing to build a Plan statement.'",
    "natsyst_n_individuals":"Number of Individuals Beneficiaries through Natural Systems: 'Taking into consideration the specific individuals you've previously indicated in this section, how many individual beneficiaries within these Natural Systems does your initiative pledge to make more resilient against climatic hazards by 2030?'",
    "climate_diagnost":"Diagnostic: 'Is your pledge based on a diagnostics on the need and vulnerability of your target beneficiaries?'",
    "locally_led_commitment":"Locally Led Commitment: 'To what extent are your initiative and its member organizations committed to the Principles for Locally Led Adaptation?'",
    "d_individuals_hazards":"Individuals (Directly) Hazards: 'For these individuals, which specific climatic hazards do your 2030 pledge aim to provide resilience against?'",
    "regions_p_benefic_all":"Regions Primary Beneficiriaries: 'Which are the primary beneficiaries in the regions your initiative pledge to make more resilient by 2030? Select all that apply.'",
    "climate_diagnost_upload":"Diagnostics: 'Please upload documentation explaining your diagnostics and/or its results.'",
    "natsyst_n_hectares":"Number of Hectares Natural Systems: 'Considering the types of natural systems your initiative pledges to make more resilient by 2030, please indicate the estimated number of hectares your initiative aims to benefit.If this information is not available, please enter '0.' ",
    "climate_risk_assess_other":"Climate Risk Assessment: 'Is your pledge based on a climate risk assessment? (Other)'",
    "confirmation_of_future_plan_submission_when":"Future Plan Submission: 'When do you expect you will be ready to submit your Plan statement?'",
    "regions_n_individuals":"Number of Individuals Beneficiaries through Regions: 'Taking into consideration the specific individuals you've previously indicated in this section, how many individual beneficiaries within these regions does your initiative pledge to make more resilient against climatic hazards by 2030?'",
    "natsyst_types_of_individuals":"Type of Individuals through Natural Systems: 'What kind of groups of individuals related to these Natural Systems benefit from the resilience measures your 2030 initiative promotes? Please select all that apply.'",
    "confirmation_of_future_plan_submission":"Confirmation Future Plan Submission: 'Are you ready to submit your Plan Statement?'",
    "responder_name_lastname":"Responder: 'Survey Responder's Full Name'",
    "regions_n_regions":"Number of Regions: 'For analytical clarity and reliability in calculations, please provide the number of Regions your initiative aims to make more resilient as a numeric value.'",
    "climate_risk_assess_upload":"Climate Risk Assessment: 'Please upload documentation to support your risk assessment'",
    "regions_types_of_individuals":"Regions Type of Individuals: 'Which are the primary beneficiaries in the regions your initiative pledge to make more resilient by 2030? Select all that apply.'",
    "climate_diagnost_other":"Diagnostic: 'Is your pledge based on a diagnostics on the need and vulnerability of your target beneficiaries? (Other)'",
    "climate_risk_assess":"Climate Risk Assessment: 'Is your pledge based on a climate risk assessment?'",
    "d_individuals_n_d_individuals":"Number of Individuals (Directly): 'To clarify, please specify the exact number of direct individuals your initiative pledges to make more resilient against climate hazards.'",

    }

def replace_values_in_string(s):
    # Splitting the string on both semicolons and commas, and stripping spaces
    parts = [x.strip() for x in re.split(';|,', s)]
    replaced_parts = []
    
    for part in parts:
        # Convert part to lowercase for case-insensitive matching
        lower_part = part.lower()
        # Attempt to find a match in the dictionary keys, converted to lowercase
        match = next((real_questions_pledge_dict[key] for key in real_questions_pledge_dict if key.lower() == lower_part), None)
        # If a match is found, use it; otherwise, keep the original part
        if match:
            replaced_parts.append(match)
        else:
            replaced_parts.append(part)
    
    # Joining the parts back into a string, separated by "; "
    return "; ".join(replaced_parts)

# Apply the function to each row of the 'pledge_completeness_req_priority' column
df_pledge['pledge_completeness_req_priority_recoded'] = df_pledge['pledge_completeness_req_priority'].apply(replace_values_in_string)

# fixing pledge_completeness_status
mask = df_pledge['pledge_completeness_req_priority'].str.contains('_n_')
df_pledge.loc[mask, 'pledge_completeness_status'] = 'Awaiting Completion'


## CONFIDENCE PLEDGE
confidence_metrics_pledge_list = metrics_individuals_pledge_confidence_list + comp_cit_reg_naysys_pledged_confidence_list +  metrics_other_p_benific_pledge_confidence_list
confidence_consultation_members_list = ['members_consultation_pledge_confidence']
confidence_pledge_overall_list = ['n_individuals_pledged_total_confidence','comp_cit_reg_naysys_pledged_confidence','members_consultation_pledge_confidence']
df_pledge['confidence_pledge_overall_status'] = df_pledge[confidence_pledge_overall_list].apply(lambda x: ';'.join(x.astype(str)), axis=1)
df_pledge['confidence_pledge_overall_status'] = df_pledge['confidence_pledge_overall_status'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))




# df_pledge['confidence_pledge_overall_status']
# df_pledge['members_consultation_pledge_confidence']
# df_pledge['pledge_confidence_overall_idx'] 





pledge_confidence_overall_idx_dict = {
    "Medium-Low Reliability: Pledge has not been consulted with members. Need to validate with members and update the report.":1/4,
    "Medium Reliability: Pledge partially completed in consultation with members. The Pledge is expected to be updated.":3/4,
    "Low Reliability: No information available if pledge was completed in consultation with members.":0,
    "Medium-Low Reliability: Pledge has not been consulted with members. Need to confirm the validation with members and update the report.":2/4,
    "High Reliability: Pledge completed in consultation with members.":4/4,}

df_pledge['pledge_confidence_overall_idx'] = df_pledge['members_consultation_pledge_confidence'].map(pledge_confidence_overall_idx_dict)

df_pledge['pledge_overall_status'] = "Completeness: " + df_pledge['pledge_completeness_status'] + " & " + df_pledge['confidence_pledge_overall_status']

mask = df_pledge['pledge_overall_status'].str.contains('Awaiting Completion')
df_pledge.loc[mask, 'pledge_action_required'] = 'Please complete the pending questions in the pledge statement and verify its reliability'

df_pledge['pledge_action_required'] = df_pledge['pledge_action_required'].fillna("Please review the validation of the pledge statement with members to increase reliability.")

pledge_general_responses_list = all_countries_pledge_responses_list + hazards_pledge_list
pledge_completeness_responses_list = responder_id_pledge_all_list + p_benefic_all_pledge_all_list + metrics_explanation_pledge_all_list + finance_pledge_all_list + locally_led_commitment_pledge_all_list + climate_risk_assess_pledge_all_list + climate_diagnostic_assess_pledge_all_list + members_consultation_assess_pledge_all_list + confirmation_future_plans_pledge_all_list
pledge_overall_index_list =  pledge_completeness_responses_list + pledge_general_responses_list



# ## Parche The Climakers (Climakers)

df_pledge.loc[df_pledge['InitName'] == 'The Climakers (Climakers)', 'enddate_pledge'] = '2024-03-13 12:33:31'

# ## End Parche The Climakers (Climakers)





# st.write("# Pledge summary table")
df_pledge_summary = df_pledge[['InitName','Org_Type','enddate_pledge','pledge_action_required','pledge_overall_status','pledge_completeness_idx','pledge_completeness_status','pledge_completeness_req_priority','pledge_completeness_req_priority_recoded','pledge_confidence_overall_idx','confidence_pledge_overall_status',]+pledge_overall_index_list]






# df_pledge_summary
# df_pledge_summary.columns



#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________________________
# END BLOCK PLEDGE STATEMENT
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________






#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________________________
# DATA CLEANING ### PLAN 2023 (The official one after metrics enhancement). All information from PLAN 2022 is included here
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________


# st.markdown("# RESILIENCE-BUILDING PLAN SURVEY 2023")

### RESILIENCE-BUILDING PLAN SURVEY 2023
#Renaming and excluding partners not longer part of the race
replacements = {
    "Climate-KIC Accelerator-international Innovation Clusters work (KIC-FRR)": "Climate Knowledge and Innovation Community (Climate-KIC)",
    "BFA Global (BFA)": "BFA Global/ CIFAR Alliance (BFA)",
    "Cities Race to Zero (Resilience) Coalition (CitiesR2R)": "Cities Race to Resilience (CitiesR2R)",
    "Global Fund for Coral Reef (GFCR)": "Global Fund for Coral Reefs (GFCR)",
    "United Nations Office for Disaster Risk Reduction - ARISE (Private Sector Alliance for Disaster Resilient Societies) (UN ARISE)": "ARISE - United Nations Office for Disaster Risk Reduction (UN ARISE)",
    "WBCSDs food & agriculture climate workstream (WBCSD)": "Agriculture 1.5 - WBCSD’s food & agriculture climate workstream (WBCSD)",
    "Sanitation and Water for All  (SWA)": "Sanitation and Water for All (SWA)",
    "Urban Sustainability Directors Network (USDN) Resilience Hubs (USDN)": "Urban Sustainability Directors Network (USDN)",
    "RegionsAdapt (Regions4)": "RegionsAdapt (RegionsAdapt)",
    'Efficiency for Access Coalition (EfoA)':'Efficiency for Access Coalition (EforA)',
    'Just Rural Transition (JRT)':'Just Rural Transition',
    'Least Developed Countries Universities Consortium on Climate Change (LUCCC)':'Least Developed Countries Universities Consortium on Climate Change (LUCCC) (ICCCAD)',

}
df_2023_plan['r9'] = df_2023_plan['r9'].replace(replacements)

df_2023_plan = df_2023_plan.rename(columns={'r9': 'InitName','r3':'enddate_plan'})








#Merging Data with ID MASTER and making sure the data has all members name
#oldcodebelowrelatedtothetreatment of type of initiative.
# df_partners_name = df_partners_name.rename(columns={'InitName': 'InitName'})  # <--- this should be applyed when it comes after the pledge info
# # df_partners_name = df_partners_name.rename(columns={'InitName': 'r9'})

df_2023_plan = pd.merge(df_2023_plan, df_partners_name, on='InitName', how='outer')

# st.markdown("Lista Nombres Plan")
# st.write(len(df_2023_plan['InitName'].unique()))
# st.write(df_2023_plan['InitName'].unique())
# st.write(df_2023_plan[['InitName','Org_Type']])

#Set index
df_2023_plan.set_index('Master ID', inplace = True)
df_2023_plan.index.names = ['Master ID']

# st.write(df_2023_plan)
df_2023_plan = df_2023_plan.dropna(how = 'all')
df_2023_plan = df_2023_plan.replace(["Please Complete","pleasecomplete@pleasecomplete.com","Please complete","First Name","Last Name","Please Complete ","email@email.com",  "Pleasecomplete@Pleasecomplete.com","please@complete.com", "Would you kindly confirm, please?", "Would you kindly confirm, please? ", ""], np.nan)

#Additional step to ensure all blank spaces are also treated as np.nan
df_2023_plan = df_2023_plan.applymap(lambda x: np.nan if isinstance(x, str) and x.strip()=="" else x)

for col in df_2023_plan.columns:
    df_2023_plan[col] = df_2023_plan[col].replace({"": np.nan, " ": np.nan})

#Treatment of "OTHERS" when providing the names
# use numpy where to replace 'Other' in Respondant column with OtherName values
# df['Respondant'] = np.where(df['Respondant'] == 'Other', df['OtherName'], df['Respondant'])

## Plan Survey reviewed
#Making a variable to indentify if the survey has been open or not.  <<--- This is not enoght. A new filter will be done after creating a plan over all index. Plan bellow a 0% will not be conisiderated.
# Convert the date and time column to datetime data type
df_2023_plan['enddate_plan'] = pd.to_datetime(df_2023_plan['enddate_plan'], infer_datetime_format=True, errors='coerce')
last_survey_view_list = ['r3']
start_date = pd.to_datetime('10/05/2023 16:24:00', format='%m/%d/%Y %H:%M:%S', errors='coerce')
df_2023_plan['survey_reviewed_plan'] = df_2023_plan['enddate_plan'] >= start_date
# st.markdown("## Plan Survey All Data")
# st.write(df_2023_plan[last_survey_view_list+['r9','survey_reviewed_plan']])


#____COUNTRIES
#Treatment of countries
taiwan_list         = ['r352','r539','r725','r962','r1149','r1335','r1564','r1751','r1937','r2160','r2347','r2534','r2727','r2914','r3100',]
df_2023_plan[taiwan_list] = df_2023_plan[taiwan_list].replace("Taiwan","Taiwan, Province of China").fillna('').astype(str)

eeuu_list = ['r576','r762','r999','r1186','r1372','r1601','r1788','r1974','r2197','r2385','r2571','r2764','r2951','r3137',]
df_2023_plan[eeuu_list] = df_2023_plan[eeuu_list].replace("United States","United States of America").fillna('').astype(str)



companies_countries_plan_all_l =['r' + str(i) for i in range(212, 398)]
regions_countries_plan_all_l =['r' + str(i) for i in range(822, 1008)]
cities_countries_plan_all_l =['r' + str(i) for i in range(1424,1610 )]
natsyst_countries_plan_all_l =['r' + str(i) for i in range(2020, 2206)]
d_individuals_countries_plan_all_l =['r' + str(i) for i in range(2587, 2773)]

df_2023_plan['countries_individuals'] = df_2023_plan[d_individuals_countries_plan_all_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['countries_individuals'] = df_2023_plan['countries_individuals'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))

df_2023_plan['countries_individuals_plan_counts'] = df_2023_plan['countries_individuals'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

df_2023_plan['countries_companies']   = df_2023_plan[companies_countries_plan_all_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['countries_companies'] = df_2023_plan['countries_companies'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['countries_companies_plan_counts'] = df_2023_plan['countries_companies'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

df_2023_plan['countries_regions']     = df_2023_plan[regions_countries_plan_all_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['countries_regions'] = df_2023_plan['countries_regions'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['countries_regions_plan_counts'] = df_2023_plan['countries_regions'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

df_2023_plan['countries_cities']      = df_2023_plan[cities_countries_plan_all_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['countries_cities'] = df_2023_plan['countries_cities'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['countries_cities_plan_counts'] = df_2023_plan['countries_cities'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

df_2023_plan['countries_nat_sys']     = df_2023_plan[natsyst_countries_plan_all_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['countries_nat_sys'] = df_2023_plan['countries_nat_sys'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['countries_nat_sys_plan_counts'] = df_2023_plan['countries_nat_sys'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

df_2023_plan['all_countries']  = df_2023_plan[['countries_individuals','countries_companies','countries_regions','countries_cities','countries_nat_sys']].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['all_countries'] = df_2023_plan['all_countries'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))

##Parche EEUU
df_2023_plan['all_countries'] = df_2023_plan['all_countries'].str.replace("United States of America", "United States", regex=False)
df_2023_plan['all_countries'] = df_2023_plan['all_countries'].str.replace("United States", "United States of America", regex=False)


df_2023_plan['all_countries_plan_counts'] = df_2023_plan['all_countries'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

countries_plan_responses_list = [
    'countries_individuals','countries_individuals_plan_counts',
    'countries_companies','countries_companies_plan_counts',
    'countries_regions','countries_regions_plan_counts',
    'countries_cities','countries_cities_plan_counts',
    'countries_nat_sys','countries_nat_sys_plan_counts',
    'all_countries','all_countries_plan_counts']

# st.write("PLAN all countries 2023")
# st.write(df_2023_plan['all_countries'])

# Total Number of Countries
#Creating a list of all country names 
# Split each row by the delimiter and flatten the resulting list
all_countries = [country.strip() for sublist in df_2023_plan['all_countries'].str.split(';') for country in sublist if country.strip()]
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
Oceania = df_country[df_country['continent']== 'Oceania']
Northern_America = df_country[df_country['continent']== 'North America']
Southern_America = df_country[df_country['continent']== 'South America'] #NEW
Antarctica = df_country[df_country['continent']== 'Antarctica'] #NEW
seven_seas = df_country[df_country['continent']== 'Seven seas (open ocean)'] #NEW
# LATAMC = df_country[df_country['continent']== 'Latin America and the Caribbean'] #OLD

Africa_list = Africa['Country'].tolist()
Asia_list = Asia['Country'].tolist()
Europe_list = Europe['Country'].tolist()
Oceania_list = Oceania['Country'].tolist()
Northern_America_list = Northern_America['Country'].tolist()
Southern_America_list = Southern_America['Country'].tolist()
Antarctica_list = Antarctica['Country'].tolist()
seven_seas_list = seven_seas['Country'].tolist()
# LATAMC_list = LATAMC['Country'].tolist()

df_2023_plan['Africa'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Africa_list for country in x])), 'Africa', '')
df_2023_plan['Asia'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Asia_list for country in x])), 'Asia', '')
df_2023_plan['Europe'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Europe_list for country in x])), 'Europe', '')
df_2023_plan['Oceania'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Oceania_list for country in x])), 'Oceania', '')
df_2023_plan['Northern_America'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
df_2023_plan['Southern_America'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_America_list for country in x])), 'South America', '')
df_2023_plan['Antarctica'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Antarctica_list for country in x])), 'Antarctica', '')
df_2023_plan['Seven_seas'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in seven_seas_list for country in x])), 'Seven seas (open ocean)', '')

# df_2023_plan['LATAMC'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in LATAMC_list for country in x])), 'Latin America and the Caribbean', '')
# continents_pledge_list = ['Africa','Asia','Europe','LATAMC','Northern_America','Oceania']

continents_plan_list = ['Africa','Asia','Europe','Oceania','Northern_America','Southern_America','Antarctica','Seven_seas']

# st.write('continents_pledge_list',df_2023_plan[continents_pledge_list])
# st.write(df_2023_plan[continents_plan_list])

#### OLD 
# #creating a list of countries depending of its continent
# Africa = df_country[df_country['continent']== 'Africa']
# Asia = df_country[df_country['continent']== 'Asia']
# Europe = df_country[df_country['continent']== 'Europe']
# LATAMC = df_country[df_country['continent']== 'Latin America and the Caribbean']
# Northern_America = df_country[df_country['continent']== 'Northern America']
# Oceania = df_country[df_country['continent']== 'Oceania']

# Africa_list = Africa['Country'].tolist()
# Asia_list = Asia['Country'].tolist()
# Europe_list = Europe['Country'].tolist()
# LATAMC_list = LATAMC['Country'].tolist()
# Northern_America_list = Northern_America['Country'].tolist()
# Oceania_list = Oceania['Country'].tolist()

# df_2023_plan['Africa'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Africa_list for country in x])), 'Africa', '')
# df_2023_plan['Asia'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Asia_list for country in x])), 'Asia', '')
# df_2023_plan['Europe'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Europe_list for country in x])), 'Europe', '')
# df_2023_plan['LATAMC'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in LATAMC_list for country in x])), 'Latin America and the Caribbean', '')
# df_2023_plan['Northern_America'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
# df_2023_plan['Oceania'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Oceania_list for country in x])), 'Oceania', '')

# continents_plan_list = ['Africa','Asia','Europe','LATAMC','Northern_America','Oceania']
# # st.write(df_2023_plan[continents_plan_list])



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

df_2023_plan['South_Asia'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in South_Asia_list for country in x])), 'South Asia', '')
df_2023_plan['Europe_Central_Asia'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Europe_Central_Asia_list for country in x])), 'Europe & Central Asia', '')
df_2023_plan['Middle_East_North_Africa'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Middle_East_North_Africa_list for country in x])), 'Middle East & North Africa', '')
df_2023_plan['Sub_Saharan_Africa'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Sub_Saharan_Africa_list for country in x])), 'Sub-Saharan Africa', '')
df_2023_plan['Latin_America_Caribbean'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Latin_America_Caribbean_list for country in x])), 'Latin America & Caribbean', '')
df_2023_plan['East_Asia_Pacific'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in East_Asia_Pacific_list for country in x])), 'East Asia & Pacific', '')
df_2023_plan['North_America'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in North_America_list for country in x])), 'North America', '')

regions_plan_list = ['South_Asia','Europe_Central_Asia','Middle_East_North_Africa','Sub_Saharan_Africa','Latin_America_Caribbean','East_Asia_Pacific','North_America']
# st.write(df_2023_plan[regions_plan_list])

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

df_2023_plan['Southern_Asia'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Asia_list for country in x])), 'Southern Asia', '')
df_2023_plan['Southern_Europe'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Europe_list for country in x])), 'Southern Europe', '')
df_2023_plan['Northern_Africa'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_Africa_list for country in x])), 'Northern Africa', '')
df_2023_plan['Middle_Africa'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Middle_Africa_list for country in x])), 'Middle Africa', '')
df_2023_plan['Caribbean'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Caribbean_list for country in x])), 'Caribbean', '')
df_2023_plan['South_America'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in South_America_list for country in x])), 'South America', '')
df_2023_plan['Western_Asia'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Asia_list for country in x])), 'Western Asia', '')
df_2023_plan['Australia_and_New_Zealand'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Australia_and_New_Zealand_list for country in x])), 'Australia and New Zealand', '')
df_2023_plan['Western_Europe'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Europe_list for country in x])), 'Western Europe', '')
df_2023_plan['Eastern_Europe'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Europe_list for country in x])), 'Eastern Europe', '')
df_2023_plan['Central_America'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Central_America_list for country in x])), 'Central America', '')
df_2023_plan['Western_Africa'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Africa_list for country in x])), 'Western Africa', '')
df_2023_plan['Southern_Africa'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Africa_list for country in x])), 'Southern Africa', '')
df_2023_plan['Eastern_Africa'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Africa_list for country in x])), 'Eastern Africa', '')
df_2023_plan['South_Eastern_Asia'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in South_Eastern_Asia_list for country in x])), 'South-Eastern Asia', '')
df_2023_plan['Northern_America'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
df_2023_plan['Eastern_Asia'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Asia_list for country in x])), 'Eastern Asia', '')
df_2023_plan['Northern_Europe'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_Europe_list for country in x])), 'Northern Europe', '')
df_2023_plan['Central_Asia'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Central_Asia_list for country in x])), 'Central Asia', '')
df_2023_plan['Melanesia'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Melanesia_list for country in x])), 'Melanesia', '')
df_2023_plan['Polynesia'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Polynesia_list for country in x])), 'Polynesia', '')
df_2023_plan['Micronesia'] = np.where(df_2023_plan['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Micronesia_list for country in x])), 'Micronesia', '')

subregions_plan_list = ['Southern_Asia','Southern_Europe','Northern_Africa','Middle_Africa','Caribbean','South_America',
                          'Western_Asia','Australia_and_New_Zealand','Western_Europe','Eastern_Europe','Central_America',
                          'Western_Africa','Southern_Africa','Eastern_Africa','South_Eastern_Asia','Northern_America','Eastern_Asia',
                          'Northern_Europe','Central_Asia','Melanesia','Polynesia','Micronesia',]

# st.write(df_2023_plan[subregions_plan_list])

# #Concatenating columns
df_2023_plan['country_continents_all'] = df_2023_plan[continents_plan_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['country_region_all'] = df_2023_plan[regions_plan_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['country_subregion_all'] = df_2023_plan[subregions_plan_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
# st.write(df_2023_plan[['all_countries','country_continents_all','country_region_all','country_subregion_all']])





##### Plan Structure
# st.write('# PLAN TABLES TO EXPLORER')
# st.markdown("## Section 1. Introduction")
#Making a data set with only information where 'survey_reviewed_plan' = True
df_2023_plan = df_2023_plan[df_2023_plan['survey_reviewed_plan'] == True]
# st.markdown("## Plan Survey All Data Filtered by Reviewd")
# st.write(df_2023_plan)
# st.markdown("Numbers Partner Reporting Plan")
# st.write(df_2023_plan['InitName'].nunique())
# st.markdown("Numbers of Plan Reported")
# st.write(df_2023_plan['survey_reviewed_plan'].sum())
# st.markdown("Numbers Plan per Partner")
# st.write(df_2023_plan['InitName'].value_counts())
#Creating PlanYearVariable
df_2023_plan['PlanYear'] = None
df_2023_plan['PlanYear'] = np.where(df_2023_plan['survey_reviewed_plan'] == True, '2023', df_2023_plan['PlanYear'])



# st.markdown("## Section 2: Plan Identification") 
### plan_identif_subidx which contains three dimension: responder_id_plan_status; action_clusters_plan_status; plan_description_status
## Respondant Validation
responder_name_id_plan_l = ['r11','r12']
# st.write(df_2023_plan[responder_name_id_plan_l])
df_2023_plan = df_2023_plan.rename(columns={'r16': 'responder_email_plan'})
responder_mail_plan_l =['responder_email_plan']
df_2023_plan['reponder_id_plan_status'] = df_2023_plan[responder_name_id_plan_l].notna().all(axis=1)
df_2023_plan['reponder_email_plan_status'] = df_2023_plan[responder_mail_plan_l].notna().all(axis=1)
responder_info_plan_list =['reponder_id_plan_status','reponder_email_plan_status']
df_2023_plan['responder_info_plan_status'] = df_2023_plan[responder_info_plan_list].all(axis=1)
df_2023_plan['responder_info_plan_concat'] = df_2023_plan[responder_name_id_plan_l].apply(lambda x: ' '.join(map(str, x)), axis=1)
df_2023_plan['responder_info_plan_concat'] = df_2023_plan['responder_info_plan_concat'].str.replace('nan', '')
# st.write(df_2023_plan['responder_info_plan_concat'])

responder_info_plan_list_summary = ['responder_info_plan_concat'] + responder_mail_plan_l + ['responder_info_plan_status']
# st.write(df_2023_plan[responder_info_plan_list_summary])

df_2023_plan = df_2023_plan.rename(columns={'r17': 'plan_name'})

replacements_plan_names = {"Target 1: By 2025, 50 countries have reviewed and integrated their crisis/disaster risk management, climate adaptation laws, policies and/or plans to ensure that they reduce climate change impacts and exposure on people and the environment.":"Target 1"}
df_2023_plan['plan_name'] = df_2023_plan['plan_name'].replace(replacements_plan_names)

df_2023_plan['plan_short_name'] = df_2023_plan['short_name'] + ": " +df_2023_plan['plan_name' ]
plan_name_list = ['plan_short_name'] 
# st.write(df_2023_plan[plan_name_list])

responder_info_plan_responses = plan_name_list + ['responder_info_plan_concat'] + responder_mail_plan_l  ##DOES NOT INCLUDE STATUS VARIABLES
# st.markdown("## Respondant Validation")

plan_id_n_responder_info_plan_list_summary = plan_name_list + responder_info_plan_list_summary
# st.write('Respondant Validation',df_2023_plan[plan_id_n_responder_info_plan_list_summary])

## This is made to identify types of action 
## Resilience Action Cluster Plan 
# Please select an Resilience Action Cluster or group of Resilience Action Clusters that align with your Resilience-Building Plan.
resilience_actions_cluster_list_plan = ['r18','r19','r20','r21','r22','r23','r24','r25','r26','r27','r28','r29','r30','r31','r32','r33','r34','r35','r36','r37','r38','r39','r40','r41','r42','r43','r44','r45','r46',]

# Identification of Resilience Action Clusters: In this section, we request that you identify and elaborate on the resilience actions taken by your initiative, which are categorized into Action Clusters.
# df_2023_plan[resilience_actions_cluster_list_plan]


simplified_descriptions = {
    'r18': 'Monitoring and mapping of hazards and vulnerabilities',
    'r19': 'Climate services and modelling',
    'r20': 'Generation and processing of data',
    'r21': 'Early warning systems',
    'r22': 'Emergency preparedness',
    'r23': 'Environmental governance and resource management systems',
    'r24': 'Environmental laws and regulatory framework',
    'r25': 'Protected areas and property rights definitions',
    'r26': 'Institutional-led climate adaptation planning processes',
    'r27': 'Building regulations and standards for climate resilience',
    'r28': 'Measures to improve air quality and reduce pollution',
    'r29': 'Green infrastructure and other engineered nature-based solutions',
    'r30': 'Conservation and restoration of terrestrial and aquatic ecosystems',
    'r31': 'Critical Infrastructure and Protective Systems',
    'r32': 'Coastal Infrastructure Protection',
    'r33': 'Energy efficiency and renewable energy technologies',
    'r34': 'Water security and quality',
    'r35': 'Health services',
    'r36': 'Food safety and sustainable services',
    'r37': 'Climate insurance and risk transfer',
    'r38': 'Social protection actions',
    'r39': 'Agricultural, livestock, forestry and aquiacultural practices actions',
    'r40': 'Community-based inclusive and participatory risk reduction',
    'r41': 'Climate hazard communication, information, and technology awareness',
    'r42': 'Knowledge building for resilience',
    'r43': 'Research and collaboration actions',
    'r44': 'Livelihood diversification and social economy',
    'r45': 'Financial and investment tools in case of climate disasters',
    'r46': 'Economic incentives',
}

# Apply the simplified descriptions to the DataFrame
for question_code, simplified_description in simplified_descriptions.items():
    df_2023_plan[question_code] = df_2023_plan[question_code].replace({
        f'{simplified_description}: .*': simplified_description
    }, regex=True)



## ACTION CLUSTER PLAN 2023_ 
x14_list =	['r18','r19','r20']		#OK	1
x15_list =	['r21']						#OK 2
x16_list =	['r22']							#OK 3			
x17_list =	['r23','r24','r25','r26','r27']		#ok 4			
x18_list =	['r28','r29','r30']					#ok 5
x19_list =	['r31','r32','r33','r34','r35','r36']	#ok 6					
x20_list =	['r37','r38']						# ok7		
x21_list =	['r39','r40','r41','r42','r43']		# ok8		
x22_list =	['r44','r45','r46'] #OK 9

# Set each xNN column to True if any corresponding xNN_list column has information
df_2023_plan['x14'] = df_2023_plan[x14_list].any(axis=1) 
df_2023_plan['x15'] = df_2023_plan[x15_list].any(axis=1)
df_2023_plan['x16'] = df_2023_plan[x16_list].any(axis=1)
df_2023_plan['x17'] = df_2023_plan[x17_list].any(axis=1)
df_2023_plan['x18'] = df_2023_plan[x18_list].any(axis=1)
df_2023_plan['x19'] = df_2023_plan[x19_list].any(axis=1)
df_2023_plan['x20'] = df_2023_plan[x20_list].any(axis=1)
df_2023_plan['x21'] = df_2023_plan[x21_list].any(axis=1)
df_2023_plan['x22'] = df_2023_plan[x22_list].any(axis=1)

# list_action_areas = ['x14','x15','x16','x17','x18','x19','x20','x21','x22',]

df_2023_plan['action_clusters_plan_status'] = df_2023_plan[resilience_actions_cluster_list_plan].any(axis=1)
df_2023_plan['action_clusters_plan_concat'] = df_2023_plan[resilience_actions_cluster_list_plan].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['action_clusters_plan_concat'] = df_2023_plan['action_clusters_plan_concat'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['action_clusters_plan_counts'] = df_2023_plan['action_clusters_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
# st.markdown("## Resilience Action Cluster Plan ")

action_clusters_info_plan_responses = ['action_clusters_plan_concat','action_clusters_plan_counts',]
action_clusters_info_plan_list_summary = action_clusters_info_plan_responses + ['action_clusters_plan_status']
# st.write('Action Cluster Plan',df_2023_plan[action_clusters_info_plan_list_summary])


## Plan General Description
#Could you please describe the Resilience-Building Plan you are reporting on, in general terms? When describing your Resilience-Building Plan in general terms, aim to provide an overview that offers context for your chosen Action Cluster(s) and gives a sna	
df_2023_plan = df_2023_plan.rename(columns={'r47': 'plan_description'})
plan_description_l = ['plan_description']
df_2023_plan['plan_description_status'] = df_2023_plan[plan_description_l].notna().all(axis=1)
description_not_enough_list = ['bla']
condition = df_2023_plan[plan_description_l[0]].isin(description_not_enough_list)
df_2023_plan.loc[condition, 'plan_description_status'] = False
# st.markdown("## Plan General Description")
plan_description_responses = plan_description_l
plan_description_list_summary = plan_description_l + ['plan_description_status']
# st.write('Plan General Description',df_2023_plan[plan_description_list_summary])



### PLAN IDENTIFICATION SUB_INDEX plan_identif_subidx

info_plan_identif_subidx = """4. Initiative Information (section 2)

This section asks for details to identify both the initiative and the individual responsible for completing this survey. This ensures efficient and precise future interactions regarding the reporting process.

Please select the name of your organization from the list of RtR Partners below. If your organization's name is not listed, kindly type it in the provided space.
Survey Responder's Full Name
Survey Responder's Email Address

5. Plan Identification

Before completing this section, ensure that you've adequately prepared your plan submission as outlined in the provided guide. This means that before finalizing this submission, you should already know the total number of plans you'll submit to the RtR Campaign. Moreover, you should discern the distinctions between each plan in terms of the represented resilience action clusters, unique individual beneficiaries, and their respective country locations. Crucially, the combined count of all the plans you're submitting should approximate as closely as possible to the total number of individual beneficiaries you pledged in the previous phase of the RtR Campaign.

Once you've structured your plan(s) for submission, answering the subsequent questions will become more intuitive. You'll recognize that the process of naming and categorizing your Resilience-Building Plan is integral to the Race to Resilience (RtR) reporting framework. It's not just about giving it a title; it's about aligning your initiative with one or more specific Resilience Action Clusters that best represent the aspect or dimension you're addressing, especially if you're submitting multiple plans.

What name have you designated for this specific Resilience-Building Plan you are reporting? 

When choosing a name for your Resilience-Building Plan, opt for a unique and easily identifiable title that captures the essence of your initiative, keeping in mind the previously identified number of plans to report. Each plan should have a distinct name. This title will act as the primary identifier within the Race to Resilience (RtR) framework, ensuring effortless tracking and evaluation of your project.


6. Resilience Action Cluster

In the Race to Resilience (RtR) framework, Resilience Action Clusters form the strategic core of your Resilience-Building Plan, guiding coherent actions targeted at specified locations, beneficiary groups, or measurement methodologies. These clusters, developed collaboratively by the Technical Secretariat and validated by the Methodology Advisory Group (MAG), represent 29 rigorously evaluated categories based on inputs from entities like the Marrakech Partnership, the Carbon Disclosure Project (CDP), and the IPCC.

Resilience actions cluster usually include a combination of adaptation and response measures, as well as capacity building and awareness raising actions. They can range from the improvement of basic infrastructure and services, such as water supply systems, renewable energy and food security, to resilience education and training programs, risk management strategies and the development of strategic resource plans.

It’s crucial to align your plan succinctly with a unified set of actions, concentrated on specific geographic areas, beneficiary groups, or impact systems, enhancing the effectiveness of your reporting and clarifying your plan's impact within the RtR framework. 

Important: Your prior identification of resilience action clusters during plan preparation is essential for generating optimal responses. For a comprehensive understanding of each Resilience Action Cluster, please consult the provided documentation:  Actions Cluster for the RtR Campaign.docx

Please select a Resilience Action Cluster or group of Resiliencia Action Clusters that align with your Resilience-Building Plan.
Monitoring and mapping of hazards and vulnerabilities = Collection and analysis of geospatial and socioeconomic information to identify areas and populations that are most exposed to climate risks.
Climate services and modelling = Development and application of climate models that generate projections and future scenarios of climate and its impacts.
Generation and processing of data = Collection of relevant data for climate resilience and its analysis to identify patterns, trends, and relationships that can inform adaptation and mitigation.
Early warning systems = Implementation of systems that constantly monitor environmental and climatic conditions and issue alerts when extreme events are detected.
Emergency preparedness = Development of contingency and preparedness plans to deal with climate disasters.
Environmental governance and resource management systems = Implementation of policies, practices, and sustainable management systems for natural resources.
Environmental laws and regulatory framework = Creation, updating, and application of laws and regulations that protect the environment, promote climate change adaptation, and foster sustainable practices.
Building regulations and standards for climate resilience = Development and implementation of regulations and standards that ensure buildings are climate-resilient.
Protected areas and property rights definitions = Establishment and management of protected areas to conserve biodiversity and maintain ecosystem services.
Institutional-led climate adaptation planning processes = Design and implementation of strategies and plans for climate adaptation at different levels of government.
Measures to improve air quality and reduce pollution = Implementation of policies, technologies, and practices to reduce emissions of air pollutants.
Green infrastructure and other engineered nature-based solutions = Design and implementation of infrastructure that uses natural systems to improve climate resilience and provide environmental benefits.
Conservation and restoration of terrestrial and aquatic ecosystems = Protection and recovery of ecosystems to ensure their ability to provide ecosystem services and contribute to climate resilience.
Critical Infrastructure and Protective Systems = Design, construction, and maintenance of critical infrastructure that is resilient to climate impacts.
Coastal Infrastructure Protection = Implementation of measures to protect coastal infrastructure from extreme climate events and sea level rise.
Energy efficiency and renewable energy technologies = Promotion and implementation of technologies and practices that reduce energy consumption and increase the use of renewable energy sources.
Water security and quality = Implementation of measures to ensure availability, quality, and access to water in the context of climate change.
Health services = Strengthening and adapting healthcare systems to face the challenges and risks associated with climate change.
Food safety and sustainable services = Implementation of practices and technologies that ensure the availability, access, and stability of nutritious and culturally appropriate foods.
Agricultural, livestock, forestry and aquiacultural practices actions = Promotion and implementation of sustainable and resilient practices in these sectors.
Social protection actions = Implementing social protection programs and policies that help vulnerable communities cope with and adapt to the impacts of climate change.
Community-based inclusive and participatory risk reduction = Strengthening the capacity of local communities to identify, evaluate, and address climate risks in an inclusive and participatory manner.
Climate hazard communication, information, and technology awareness = Developing and implementing communication and education strategies and tools that help communities understand and address climate risks.
Knowledge building for resilience = Promoting and implementing research, training, and skill-building activities that strengthen the capacity of communities and other actors to cope with climate change.
Research and collaboration actions = Fostering cooperation and knowledge exchange among institutions, sectors, and countries on climate resilience.
Livelihood diversification and social economy = Supporting the diversification of income sources and the promotion of sustainable and climate-resilient economic activities.
Climate insurance and risk transfer = Developing and implementing financial mechanisms that help vulnerable communities and sectors to recover from the economic impacts of climate change.
Financial and investment tools in case of climate disasters = Developing and implementing financial instruments and investment strategies that mobilize resources for recovery and reconstruction after climate disasters.
Economic incentives = Establishing economic incentives that promote the adoption of climate-resilient practices and the conservation of natural resources.

Could you please describe the Resilience-Building Plan you are reporting on, in general terms? 

When describing your Resilience-Building Plan in general terms, aim to provide an overview that offers context for your chosen Action Cluster(s) and gives a snapshot of your overarching goals and targets. This description will be crucial for anyone reviewing your plan to grasp its scope, potential impact, and alignment with the larger goals of the Race to Resilience (RtR) campaign.
"""


# Plan Identification Section Index: It ask for the respondant information, the Action Cluster and a Description of the Plan
plan_identif_list_to_index = ['responder_info_plan_status','action_clusters_plan_status','plan_description_status']
weights = {
    'responder_info_plan_status':0.05,
    'action_clusters_plan_status':0.55,
    'plan_description_status':0.4,
    }

# Calculate the weighted sum of the components for plan_identif_subidx
df_2023_plan['plan_identif_subidx'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_2023_plan['plan_identif_subidx'] = (df_2023_plan['plan_identif_subidx'] * 100).astype(int)

# st.markdown("## Plan Indentification index")
plan_identifaction_summary_list = ['plan_identif_subidx']+plan_identif_list_to_index

index_list = plan_identif_list_to_index
# Create a new column for pending identification based on a threshold
def identify_req_status(row):
    pending_items = []
    for col in index_list:
        # Assuming a mechanism to evaluate if the column value is below 90
        # This needs to be adjusted based on how you're scoring or evaluating each column
        if row[col] == False:  # Placeholder condition
            pending_items.append(col)
    return ";".join(pending_items)

# Apply the function to each row
df_2023_plan['plan_identif_req'] = df_2023_plan.apply(identify_req_status, axis=1)

plan_identif_responses_list = responder_info_plan_responses + plan_description_responses + action_clusters_info_plan_responses
plan_identif_result_list = ['plan_identif_subidx','plan_identif_req'] 
plan_identif_list_to_index = plan_identif_list_to_index
plan_identif_plan_all_list = plan_identif_responses_list + plan_identif_result_list + plan_identif_list_to_index
 ##
##  ##
 ##
# st.write("plan_identif_plan_all_list",df_2023_plan[plan_identif_plan_all_list])




# st.markdown("## Section 3: Describe the problem")
info_plan_description = """Section 3: Describe the problem

7. Describe the Problem (section 3)

Describing the climate problem is foundational for any resilience initiative. By pinpointing the particular hazards and matching them with the groups that are most vulnerable, you create a targeted lens through which to view the climate crisis. This sharp focus is indispensable for crafting a resilience plan that effectively addresses the real and immediate needs of those most impacted.

Hazard. Identifying the Hazard as a starting point.

Against which of the following hazards is your Resilience-Building Plan designed to provide resilience?
All types of hazards
Water stress (urban focus)
Water stress (rural focus)
Extreme heat
Extreme cold
Drought (agriculture focus)
Drought (other sectors)
Urban flood
River flood
Coastal flood
Tropical Cyclone
Snow, Ice
Wildfire
Extreme wind
Oceanic Events
Other coastal events
Other

Vulnerable Groups. Identifying priority beneficiaries

To what extent is the impact of your Resilience-Building Plan specifically directed towards each of the following priority groups?
Women and girls
LGBTQIA+
Elderly
Children and Youth
Disabled
Indigenous or traditional communities
Racial, ethnic and/or religious minorities
Refugees
Low-Income Communities
Other (please specify)

Problem Statement. Contextualizing the hazard and vulnerable groups

Considering the hazard(s) you've identified and the vulnerable groups you aim to support, please provide a concise narrative describing the specific climate-related risk or problem you're targeting. A high-level summary is sufficient, but you're welcome to share full details via email if interested.
"""


## Hazards Plan
# Hazard. Identifying the Hazard as a starting point.Against which of the following hazards is your Resilience-Building Plan designed to provide resilience?
hazards_option_l = [
    'Water stress (urban focus)', 'Water stress (rural focus)', 'Extreme heat',
    'Extreme cold', 'Drought (agriculture focus)', 'Drought (other sectors)',
    'Urban flood', 'River flood', 'Coastal flood', 'Tropical Cyclone',
    'Snow, Ice', 'Wildfire', 'Extreme wind', 'Oceanic Events',
    'Other coastal events',
]
hazards_plan_all_types_hazard_l = ['r48']
hazards_plan_l = ['r' + str(i) for i in range(49, 64)]  # Start from the next after "'All types of hazards' to exclude 'All types of hazards' & Others(please specify)
# Replace the value in each column with the corresponding hazard from hazards_option_l if the 'r48' column is 'All types of hazards'
for idx, col in enumerate(hazards_plan_l):
    df_2023_plan[col] = df_2023_plan.apply(lambda row: hazards_option_l[idx] if row[hazards_plan_all_types_hazard_l[0]] == 'All types of hazards' else row[col], axis=1)
hazards_plan_l = ['r' + str(i) for i in range(49, 65)] #Adding Other to list
df_2023_plan['hazards_plan_status'] = df_2023_plan[hazards_plan_l].notna().any(axis=1)


# Concatenating columns, removing NaNs, and stripping spaces
df_2023_plan['hazards_plan_concat'] = df_2023_plan[hazards_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
# Filter out empty strings, remove duplicates, and ensure no leading "; "
df_2023_plan['hazards_plan_concat']= df_2023_plan['hazards_plan_concat'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['hazards_plan_counts'] = df_2023_plan['hazards_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
hazards_plan_responses = ['hazards_plan_concat','hazards_plan_counts']
# st.markdown("## Hazards Plan")
# st.write(df_2023_plan[['hazards_plan_status'] + hazards_plan_responses])


## Priority Groups Plan
priority_groups_plan_l = ['r' + str(i) for i in range(65, 75)]
priority_groups_plan_l_with_no_other = ['r' + str(i) for i in range(65, 74)]
priority_group_dictionary = {
'Not targeted.':1,
'Mildly targeted but not exclusively.':3,
'Main or unique target.':5,}

df_2023_plan['priority_groups_plan_status'] = df_2023_plan[priority_groups_plan_l].notna().any(axis=1)


for column in priority_groups_plan_l_with_no_other:
    if column in df_2023_plan.columns:  # Check if the column exists in the DataFrame
        df_2023_plan[column] = df_2023_plan[column].map(priority_group_dictionary).fillna(0).astype(int)
    else:
        pd.nan
        

pritority_groups_to_rename = {'r65':'Women and girls',
'r66':'LGBTQIA+',
'r67':'Elderly',
'r68':'Children and Youth',
'r69':'Disabled',
'r70':'Indigenous or traditional communities',
'r71':'Racial, ethnic and/or religious minorities',
'r72':'Refugees',
'r73':'Low Income Communities',
'r74':'Other',
}
df_2023_plan = df_2023_plan.rename(columns=pritority_groups_to_rename)


priority_groups_renamed_list = ['Women and girls','LGBTQIA+','Elderly','Children and Youth',
                                'Disabled','Indigenous or traditional communities',
                                'Racial, ethnic and/or religious minorities','Refugees',
                                'Low Income Communities','Other']



# Convert columns to numeric (float), errors='coerce' will turn non-convertible values to NaN
for col in priority_groups_renamed_list:
    df_2023_plan[col] = pd.to_numeric(df_2023_plan[col], errors='coerce')

# Now apply the concatenation logic
df_2023_plan['priority_groups_targeted_plan_concat'] = df_2023_plan.apply(
    lambda row: '; '.join(
        [col for col in priority_groups_renamed_list if row[col] > 3] +
        (["Other"] if pd.notna(row['Other']) else [])
    ), 
    axis=1
)
df_2023_plan['priority_groups_targeted_plan_concat'] = df_2023_plan['priority_groups_targeted_plan_concat'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['priority_groups_targeted_plan_counts'] = df_2023_plan['priority_groups_targeted_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
priority_groups_plan_responses = ['priority_groups_targeted_plan_concat','priority_groups_targeted_plan_counts']

# st.markdown("## Priority Groups Plan")
# st.write(df_2023_plan[['priority_groups_plan_status']+priority_groups_plan_responses])


## Problem Statement Plan
# Problem Statement. Contextualizing the hazard and vulnerable groupsConsidering the hazard(s) you've identified and the vulnerable groups you aim to support, could you please provide a focused narrative describing the specific climate-related risk or probl
df_2023_plan = df_2023_plan.rename(columns={'r75': 'problem_statement_plan'})
plan_probl_statement_l = ['problem_statement_plan']
df_2023_plan['plan_probl_statement_status'] = df_2023_plan[plan_probl_statement_l].notna().all(axis=1)
probl_statem_not_enough_list = ['bla','blabla']
condition = df_2023_plan[plan_probl_statement_l[0]].isin(probl_statem_not_enough_list)
df_2023_plan.loc[condition, 'plan_probl_statement_status'] = False
# st.markdown("## Problem Statement Plan")
# st.write(df_2023_plan[['plan_probl_statement_status',]+plan_probl_statement_l])



### PLAN DESCRIPTION SUB INDEX
# Plan description of the problem section index
description_problem_list_to_index = ['hazards_plan_status','priority_groups_plan_status','plan_probl_statement_status']

weights = {
    'hazards_plan_status':0.2,
    'priority_groups_plan_status':0.2,
    'plan_probl_statement_status':0.6,
    }

# Calculate the weighted sum of the components for description_plan_subidx
df_2023_plan['description_plan_subidx'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_2023_plan['description_plan_subidx'] = (df_2023_plan['description_plan_subidx'] * 100).astype(int)

# st.markdown("## Describe the problem index")
plan_problem_descrip_summary_list = ['description_plan_subidx']+description_problem_list_to_index
# st.write(df_2023_plan[plan_problem_descrip_summary_list])

index_list = description_problem_list_to_index
df_2023_plan['description_plan_req'] = df_2023_plan.apply(identify_req_status, axis=1)

description_plan_responses_list = hazards_plan_responses + priority_groups_plan_responses + plan_probl_statement_l
description_plan_result_list = ['description_plan_subidx','description_plan_req'] 
description_plan_list_to_index = description_problem_list_to_index
description_plan_plan_all_list = description_plan_responses_list + description_plan_result_list + description_plan_list_to_index
 ##
##  ##
 ##
# st.write("description_plan_all_list",df_2023_plan[description_plan_plan_all_list])





# st.markdown("## Section 4: Mapping a Pathway of Change through Sharm-El-Sheikh Adaptation Agenda (SAA) Task Forces")
## Sharm-El-Sheikh Adaptation Agenda (SAA) 
# Sharm-El-Sheikh Adaptation Agenda (SAA) Impact Systems & Cross-Cutting Enablers: This part is dedicated to your involvement in the SAA Impact Systems and any associated cross-cutting enablers.


info_saa_plan_idx = """Section 4: Mapping a Pathway of Change through Sharm-El-Sheikh Adaptation Agenda (SAA) Task Forces

8. Mapping a Pathway of Change through Sharm-El-Sheikh Adaptation Agenda (SAA) Task Forces (Section 4)

In the face of the risks posed by climate change, it is crucial to enhance capacities to adapt, increase resilience, and reduce vulnerabilities.

Our goal is to enhance the ability to adapt to the growing impacts and reducing the risk that is constantly increasing by implementing more resilient actions.

In response to this imperative, the Sharm-El-Sheikh Adaptation Agenda (SAA) has emerged as a critical initiative to tackle global climate change issues. This agenda was established by COP27 together with the HLCs in 2022 and sets out Global 2030 Adaptation Outcome Targets.

These targets offer a consolidated set of adaptation and resilience solutions for countries and all stakeholders towards climate-resilient development pathways, and are organized into six different impact systems and two cross-cutting enablers, also known as SAA Task Forces.

When detailing this Resilience-Building Plan, please select the SAA Task Forces you intend to influence from the provided list. For each selected task force, specify the primary outcome target to which this plan relates. If your plan doesn't directly align with them, you can also describe how it proposes to approach them. Even a gradual or partial alignment with the outcome target is valuable, providing essential context about the intentions and direction of your plan.

Which SAA impact systems and/or cross-cutting enablers are your Resilience-Building Plan targeting?

Food and Agriculture Systems
Refer to the entire process of producing, processing, distributing, and consuming food and agricultural products, including the impact on food security, nutrition and health, social equity, and the economy.
Water and Natural Systems
Encompass the interrelated ecological and hydrological systems, including agricultural land, wilderness areas, and rural communities, and their impact on biodiversity, water resources, and the functioning of wastewater systems.
Human Settlements Systems
These are the constructed environments where people live, work and play, including urban, suburban and rural areas. Human settlements are vulnerable to the impacts of climate change, including sea level rise, increased heat, and extreme weather events.
Coastal and Ocean Systems
These are the marine ecosystems along the coast and in the ocean, including coral reefs, mangroves, fishing communities, and coastal urban areas. These systems are highly susceptible to the impacts of climate change, such as sea level rise, ocean acidification, and extreme weather events.
Infrastructure Systems
These are the critical systems that support human activity, such as energy and transportation systems. Climate change can cause disruptions to these systems, such as damage to hydroelectric power or rail assets caused by flooding, or changes in demand caused by heat waves.
Health Systems 
Though solutions are still under development, this system underscores the infrastructure and services ensuring health. Climate change can introduce or exacerbate health issues, from spreading diseases to overwhelming healthcare facilities.
Cross-Cutting Enabler – Planning
Planning is essential to understanding the impacts of climate change across different systems, making informed decisions, and allocating resources to implement and accelerate adaptation.
Cross-Cutting Enabler - Finance
Financial strategies, funding sources, and investment decisions underpin the feasibility and sustainability of resilience-building efforts.

Note: The following questions within this section will only apply to the task forces selected here. 
"""



saa_identification_plan_l = ['r76','r77','r78','r79','r80','r81','r82','r83',]

recode_saa = {
    "Food and Agriculture SystemsRefer to the entire process of producing, processing, distributing, and consuming food and agricultural products, including the impact on food security, nutrition and health, social equity, and the economy.":"Food and Agriculture",
    "Water and Natural SystemsEncompass the interrelated ecological and hydrological systems, including agricultural land, wilderness areas, and rural communities, and their impact on biodiversity, water resources, and the functioning of wastewater systems.":"Water and Nature",
    "Human Settlements SystemsThese are the constructed environments where people live, work and play, including urban, suburban and rural areas. Human settlements are vulnerable to the impacts of climate change, including sea level rise, increased heat, and extreme weather events.":"Human Settlements",
    "Coastal and Ocean SystemsThese are the marine ecosystems along the coast and in the ocean, including coral reefs, mangroves, fishing communities, and coastal urban areas. These systems are highly susceptible to the impacts of climate change, such as sea level rise, ocean acidification, and extreme weather events.":"Coastal and Oceans",
    "Infrastructure SystemsThese are the critical systems that support human activity, such as energy and transportation systems. Climate change can cause disruptions to these systems, such as damage to hydroelectric power or rail assets caused by flooding, or changes in demand caused by heat waves.":"Infrastructure",
    "Health Systems Though solutions are still under development, this system underscores the infrastructure and services ensuring health. Climate change can introduce or exacerbate health issues, from spreading diseases to overwhelming healthcare facilities.":"Health",
    "Cross-Cutting Enabler – PlanningPlanning is essential to understanding the impacts of climate change across different systems, making informed decisions, and allocating resources to implement and accelerate adaptation.":"Planning and Policy: Cross-cutting",
    "Cross-Cutting Enabler - FinanceFinancial strategies, funding sources, and investment decisions underpin the feasibility and sustainability of resilience-building efforts.":'Finance: Cross-cutting'}


for column in saa_identification_plan_l:
    df_2023_plan.loc[:, column] = df_2023_plan[column].replace(recode_saa)
    
df_2023_plan['saa_taskforce_concat_plan'] = df_2023_plan[saa_identification_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['saa_taskforce_concat_plan'] = df_2023_plan['saa_taskforce_concat_plan'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['saa_taskforce_concat_counts'] = df_2023_plan['saa_taskforce_concat_plan'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
saa_taskforce_plan_responses = ['saa_taskforce_concat_plan','saa_taskforce_concat_counts']

# df_2023_plan[saa_taskforce_plan_responses]

foodandagriculturesystems_out_target_list = ['r84','r85','r86','r87',]
waterandnaturalsystems_out_target_list = ['r90','r91','r92','r93','r94','r95',]
humansettlementssystems_out_target_list = ['r98','r99','r100','r101','r102','r103',]
coastalandoceanicsystems_out_target_list = ['r106','r107','r108','r109','r110',]
insfraestructuresystems_out_target_list = ['r113','r114','r115','r116','r117','r118',]
healthsystems_out_target_list = ['r121',]
planing_crosscutting_out_target_list = ['r122','r123','r124','r125','r126','r127','r128',]
finance_crosscutting_out_target_list = ['r129','r130','r131','r132','r133',]    

foodandagriculturesystems_how_list = ['r89',]
waterandnaturalsystems_how_list = ['r97',]
humansettlementssystems_how_list = ['r105',]
coastalandoceanicsystems_how_list = ['r112',]
insfraestructuresystems_how_list = ['r120',]
healthsystems_how_list = ['r121',]
planing_crosscutting_how_list = ['r128',]
finance_crosscutting_how_list = ['r134',]
taskforce_how_saa_list = foodandagriculturesystems_how_list + waterandnaturalsystems_how_list + humansettlementssystems_how_list + coastalandoceanicsystems_how_list + insfraestructuresystems_how_list + healthsystems_how_list + planing_crosscutting_how_list + finance_crosscutting_how_list
#clening not enough responses about the description of how connect to SAA taskforces
df_2023_plan[taskforce_how_saa_list] = df_2023_plan[taskforce_how_saa_list].replace(['bla bla', ""], np.nan)

df_2023_plan['foodandagriculture_outtarg_status'] = df_2023_plan[foodandagriculturesystems_out_target_list].any(axis=1)
df_2023_plan['waterandnatural_outtarg_status'] = df_2023_plan[waterandnaturalsystems_out_target_list].any(axis=1)
df_2023_plan['humansettlements_outtarg_status'] = df_2023_plan[humansettlementssystems_out_target_list].any(axis=1)
df_2023_plan['coastalandoceanic_outtarg_status'] = df_2023_plan[coastalandoceanicsystems_out_target_list].any(axis=1)
df_2023_plan['insfraestructure_outtarg_status'] = df_2023_plan[insfraestructuresystems_out_target_list].any(axis=1)
df_2023_plan['health_outtarg_status'] = df_2023_plan[healthsystems_out_target_list].any(axis=1)
df_2023_plan['planing_cross_outtarg_status'] = df_2023_plan[planing_crosscutting_out_target_list].any(axis=1)
df_2023_plan['finance_cross_outtarg_status']= df_2023_plan[finance_crosscutting_out_target_list].any(axis=1)

df_2023_plan['foodandagriculture_how_status'] = df_2023_plan[foodandagriculturesystems_how_list].any(axis=1) 
df_2023_plan['waterandnatural_how_status'] = df_2023_plan[waterandnaturalsystems_how_list].any(axis=1)
df_2023_plan['humansettlement_how_status'] = df_2023_plan[humansettlementssystems_how_list].any(axis=1)
df_2023_plan['coastalandoceanic_how_status'] = df_2023_plan[coastalandoceanicsystems_how_list].any(axis=1)
df_2023_plan['insfraestructure_how_status'] = df_2023_plan[insfraestructuresystems_how_list].any(axis=1)
df_2023_plan['health_how_status'] = df_2023_plan[healthsystems_how_list].any(axis=1)
df_2023_plan['planing_cross_how_status'] = df_2023_plan[planing_crosscutting_how_list].any(axis=1)
df_2023_plan['finance_cross_how_status'] = df_2023_plan[finance_crosscutting_how_list].any(axis=1)

foodandagriculturesystems_to_subidx_list = ['foodandagriculture_outtarg_status','foodandagriculture_how_status']
waterandnaturalsystems_to_subidx_list = ['waterandnatural_outtarg_status','waterandnatural_how_status']
humansettlementssystems_to_subidx_list = ['humansettlements_outtarg_status','humansettlement_how_status']
coastalandoceanicsystems_to_subidx_list = ['coastalandoceanic_outtarg_status','coastalandoceanic_how_status']
insfraestructuresystems_to_subidx_list = ['insfraestructure_outtarg_status','insfraestructure_how_status']
healthsystems_to_subidx_list = ['health_outtarg_status','health_how_status']
planing_crosscutting_to_subidx_list = ['planing_cross_outtarg_status','planing_cross_how_status']
finance_crosscutting_to_subidx_list = ['finance_cross_outtarg_status','finance_cross_how_status'] 

df_2023_plan['foodandagriculture_sub_subidx'] = (df_2023_plan[foodandagriculturesystems_to_subidx_list].mean(axis=1) * 100).astype(int)
df_2023_plan['waterandnatural_sub_subidx'] = (df_2023_plan[waterandnaturalsystems_to_subidx_list].mean(axis=1) * 100).astype(int)
df_2023_plan['humansettlements_sub_subidx'] = (df_2023_plan[humansettlementssystems_to_subidx_list].mean(axis=1) * 100).astype(int)
df_2023_plan['coastalandoceanic_sub_subidx'] = (df_2023_plan[coastalandoceanicsystems_to_subidx_list].mean(axis=1) * 100).astype(int)
df_2023_plan['insfraestructure_sub_subidx'] = (df_2023_plan[insfraestructuresystems_to_subidx_list].mean(axis=1) * 100).astype(int)
df_2023_plan['health_sub_subidx'] = (df_2023_plan[healthsystems_to_subidx_list].mean(axis=1) * 100).astype(int)
df_2023_plan['planing_cross_sub_subidx'] = (df_2023_plan[planing_crosscutting_to_subidx_list].mean(axis=1) * 100).astype(int)
df_2023_plan['finance_cross_sub_subidx'] = (df_2023_plan[finance_crosscutting_to_subidx_list].mean(axis=1) * 100).astype(int)

#Sharm-El-Sheikh Adaptation Agenda (SAA) SAA SUB INDEX saa_plan_subidx
saa_plan_to_index = ['foodandagriculture_sub_subidx','waterandnatural_sub_subidx','humansettlements_sub_subidx','coastalandoceanic_sub_subidx',
                   'insfraestructure_sub_subidx','health_sub_subidx','planing_cross_sub_subidx','finance_cross_sub_subidx']

df_2023_plan['count_saa_p_systems'] = df_2023_plan[saa_plan_to_index].apply(lambda x: (x != 0).sum(), axis=1)

df_2023_plan['saa_plan_subidx'] = df_2023_plan[saa_plan_to_index].sum(axis=1) / df_2023_plan['count_saa_p_systems']
df_2023_plan['saa_plan_subidx'] = df_2023_plan['saa_plan_subidx'].fillna(0)


# st.write(df_2023_plan[['saa_plan_subidx','count_saa_p_systems']+saa_plan_to_index])

### Sharm-El-Sheikh Adaptation Agenda (SAA) Plan Subidx
saa_plan_summary_list = ['saa_plan_subidx','saa_taskforce_concat_plan','count_saa_taskforce_declared']+saa_plan_to_index
# st.write(df_2023_plan[saa_plan_summary_list])

index_list = saa_plan_to_index
def identify_req_saa_plan(row):
    pending_items = []
    for col in index_list:
        # Check if the value is different from 0 and below 90
        if 0 < row[col] < 90:
            pending_items.append(col)
    return ";".join(pending_items)


# Apply the function to each row to create the 'saa_plan_req' column
df_2023_plan['saa_plan_req'] = df_2023_plan.apply(identify_req_saa_plan, axis=1)
# df_2023_plan[['saa_plan_subidx','saa_plan_req']+saa_plan_to_index]

saa_plan_responses_list = saa_taskforce_plan_responses
saa_plan_result_list = ['saa_plan_subidx','saa_plan_req'] 
saa_plan_list_to_index = saa_plan_to_index
saa_plan_plan_all_list = saa_plan_responses_list + saa_plan_result_list + saa_plan_list_to_index
 ##
##  ##
 ##
# st.write("saa_plan_all_list",df_2023_plan[saa_plan_plan_all_list])





#Section 5.1: Define Interventions_Depth [RA]
# st.markdown("## Section 5.1: Define Interventions Depth (Resilience Attributes)")

info_ra = """18. Depth metrics

Depth Metrics are crucial tools to gauge the enhancement of resilience. They utilize resilience attributes as indicators of resilience-building impacts, given the challenge of directly measuring resilience. These attributes are essential components that amplify a system's adaptive capacities. They also guide the design and assessment of resilience strategies.

Attributes are interrelated, making it imperative to approach resilience-building holistically, recognizing the synergy among them. Each attribute plays a vital role in fortifying resilience, but their significance might differ based on the strategy and action taken. Depth Metrics, thus, provide a framework to assess the alignment and effectiveness of resilience initiatives. For a detailed exploration of resilience attributes, consult the Resilience Attributes_RtR.docx

19. Intentionality of Resilience Attributes 

Intentionality is used to gauge how central resilience attribute subcategories are within the Resilience-Building Plan. Please, classify the level of intentionality for each resilience sub-category in the plan, providing insight into the plan's focus on specific resilience dimensions.

Levels of intentionality range from:
4 - Central to most actions in the plan.
3 - Important in many actions but not always central.
2 - Directly addressed by some actions.
1 - Indirectly considered; not the primary focus.
0 - Not addressed in the current plan.

This categorization ensures targeted resilience-building and allows for strategy adjustments as needs evolve. It's essential that intentionality is supported by a strong narrative, highlighting the intended strategy impact. Starting in 2024, evidence of how intentions translate into impacts will be requested. Guidance on this will be shared in the next Reporting Cycle.

20. Preparedness and Planning

Preparedness and planning are vital in proactively managing change and uncertainty. Anticipating disturbances allows for timely interventions, preventing unexpected impacts (Liao et al., 2018). Moreover, proactive management isn't just about quick action, but a strategic response to maximize opportunities and minimize potential adverse effects (Handayani et al., 2019). This attribute is bifurcated into preparedness and planning.

Preparedness:
It underscores the importance of anticipating and readying for change. Preparedness isn't just about setting up warning systems but also about identifying threats early on (Shah et al., 2018). Recognizing a hazard and knowing how to act can not only reduce its impact but also create chances for growth during adversity.

To what extent do the actions within your Resilience-Building Plan contribute to building or enhancing the capacity to anticipate, prepare for, respond to, and monitor socio-climatic hazards?

Planning:
This emphasizes strategizing for the near and distant future, addressing climate change adaptation. Planning isn't just about long-term views but also about involving various stakeholders and setting clear goals for the conservation and sustainable use of resources (Sellberg et al., 2018). Such planning aids in anticipating and responding to change effectively.

To what extent do the actions within your Resilience-Building Plan contribute to short-, medium-, and long-term planning to mitigate and reduce climate risks and foster adaptation?

21. Learning

Learning is crucial in understanding climate change adaptation and managing uncertainties. It leverages memory to enhance resilience. Social learning mechanisms, including governance, self-organization, and open communication, have been found to contribute to resilience against urban disasters (Zhang et al., 2020). Furthermore, elements like local knowledge and social memory are critical in community resilience-building against shocks (Choudhury, Emdad Haque, et al., 2021). Learning, in this framework, is a continuously evolving skill that promotes introspection on acquired knowledge. This capacity is segmented into two main types: experiential and educational learning.

Experiential Learning:
This refers to the learning drawn from past experiences. It’s about not repeating past mistakes and taking informed steps in the future. Such learning aims to change perspectives, making them more open, inclusive, and aimed at resilience enhancement (Choudhury, Haque, et al., 2021).

To what extent do the actions within your Resilience-Building Plan promote reflective and experiential learning, encouraging the sharing of knowledge, practices, and past experiences?

Educational Learning:
This encompasses the dynamic assimilation of new knowledge related to climate change. Beyond classrooms, it happens via community interactions, research, and fieldwork. Its aim is to foster analytical skills to grasp climate change complexities (Gavilanes Capelo & Tipán Barros, 2021).

To what extent do the actions within your Resilience-Building Plan deliver new knowledge to targeted beneficiaries about understanding and addressing climate-related risks?

22. Agency

Agency emphasizes proactive adaptation and learning in the face of challenges. It's about active decision-making rather than mere reactions, transforming adversities into developmental opportunities. Agency focuses on empowerment, ensuring resilience by taking charge of situations and optimizing outcomes (Thomalla et al., 2018). Agency is categorized into three facets: autonomy, leadership, and decision-making.

Autonomy:
Autonomy grants individuals or systems the power to act independently, aligning actions to specific challenges. It's about having the self-sufficiency to assess situations, set objectives, and make decisions. This independence boosts confidence and ensures successful adaptation (Valencia et al., 2019).

To what extent do the actions within your Resilience-Building Plan foster individual and collective ownership of resources, strengthening the autonomy of targeted beneficiaries?

Leadership:
In resilience terms, leadership is the capacity to rally others toward collective goals during tough times. Effective leadership can harness resources, cultivate cooperation, and spearhead recovery, underpinning resilience (Collins et al., 2018). Leadership is pivotal for resilience as it guides adaptation and post-adversity recovery.

To what extent do the actions within your Resilience-Building Plan support and foster various types of social leadership for climate action?

Decision-making:
Decision-making is about evaluating and acting on available options during challenges. It's essential for quick, effective responses, playing a vital role in resilience enhancement. Apt decision-making skills encompass good judgment, pressure management, and lessons from past mistakes (Lam & Kuipers, 2019).

To what extent do the actions within your Resilience-Building Plan enhance individual and collective decision-making processes, emphasizing well-informed choices?

23. Social Collaboration
Social collaboration is about uniting individuals for combined resilience, emphasizing self-organization and synchronized collective efforts. Solid, interconnected social ties heighten a community's resilience to challenges (Koliou et al., 2020). It encompasses social capital cultivation, relationship building, place attachment, and robust governance (Faulkner et al., 2018). This collaboration is split into three aspects: collective participation, connectivity, and coordination.
Collective Participation:
This enhances resilience by rallying communities toward mutual goals. It emphasizes cohesion and combined efforts, especially against challenges like climate change. Such unity leverages shared resources, know-how, and abilities, improving community readiness, response, and recovery. Additionally, it deepens territorial attachment, solidifying resilience.

To what extent do the actions within your Resilience-Building Plan encourage social relationships (intergenerational, gender-based, among different interest groups), enhancing community identity and belonging?
Connectivity:
Connectivity evaluates the robustness and depth of social links. It's about having potent, dependable communication routes and using them to advance resilience, including resource-sharing and crisis support (Hong et al., 2019). Enhanced connectivity fosters a proactive, informed network that can swiftly share essential data, back each other, and jointly devise crisis strategies.

To what extent do the actions within your Resilience-Building Plan improve communication processes between individuals and social groups?
Coordination:
Coordination ensures alignment of various stakeholders for mutual objectives. By improving crisis response efficiency, unity, and collaboration, coordination underpins resilience (Galappaththi et al., 2019). It encompasses mutual understanding, strategy creation, effort synchronization, and resource management for an optimized, responsive setup. Effective coordination speeds up strategy execution, optimizes resource utilization, and augments overall resilience.

To what extent do the actions within your Resilience-Building Plan promote networks or associations that catalyze and improve social coordination and collaboration?
24. Flexibility

Flexibility is the ability to adapt and alter coping mechanisms in response to ongoing evaluations and emerging information. By allowing for adjustments, flexibility ensures that individuals, communities, and systems can promptly and aptly react to unforeseen changes and challenges, thereby reducing adverse effects and capitalizing on emerging opportunities (Sharifi, 2019). This resilience component can be distilled into two subcategories: diversity and redundancy.

Diversity:
Diversity emphasizes a spectrum of adaptive approaches to cater to varying challenges or climatic events. By embracing diverse strategies, one increases the likelihood of having the right tool or approach at hand for any challenge. Beyond enhancing adaptability, diversity also stimulates innovation and resourcefulness, further empowering adaptability in shifting contexts (O'Neill et al., 2017).

To what extent do the actions within your Resilience-Building Plan enhance the variety of strategies for producing social and ecological services, products, and processes?

Redundancy:
Redundancy ensures the availability of backup strategies, emphasizing continuity even in the face of outages or failures. Think of redundancy as a safety net, ensuring that when one strategy or system falters, there are others ready to step in. While redundancy might seem like over-preparation in regular circumstances, it becomes a lifeline during disruptions, safeguarding functionality and ensuring recovery in the face of adversity (Balaei et al., 2020).

To what extent do the actions within your Resilience-Building Plan promote overlapping functions or services to ensure alternatives during sudden changes or disturbances?

25. Equity

Equity in resilience emphasizes fair access to resources and inclusive decision-making. It becomes vital when considering social vulnerabilities and the disparities in power, knowledge, and resources (Matin et al., 2018). By recognizing these disparities, equity aims to mitigate power imbalances and potential risks associated with resilience efforts, ensuring that there are no unintentional "winners" or "losers" (Meerow et al., 2019). This attribute splits into two subcategories: Distributive equity and Equity of access.

Distributive Equity:
Equity refers to the ability to ensure fair and equitable distribution and access to resources, while recognizing and respecting the rights of all stakeholders. It is a capacity that requires fair and equitable treatment of all actors, avoiding favoritism. In the context of resilience, it is critical to ensure that the benefits and costs of adaptation and recovery strategies are shared fairly and that no one is excluded or left behind (Grove et al., 2020). In this sense, equity highlights the need to address these issues when promoting resilience by supporting the development of systems that respond to change in a socially just manner.

To what extent do the actions within your Resilience-Building Plan ensure equitable distribution of resources and fair sharing of adaptation and recovery strategy benefits?

Equity of Access:
emphasizes the capacity to incorporate and integrate all affected actors and discourses into decision-making processes, with special emphasis on the diversity of actors and social identities, including historically marginalized groups. This capacity ensures that all points of view are considered and valued and that decisions are made in a democratic and consensual manner. Inclusiveness is crucial to ensure that decisions made are representative of the needs and aspirations of all stakeholders, and to foster cooperation, cohesion, and trust, elements that in turn strengthen resilience (Fitzgibbons & Mitchell, 2021).

To what extent do the actions within your Resilience-Building Plan involve all stakeholders, especially marginalized groups, ensuring comprehensive representation in decision-making?

26. Assets

Assets encompass various resources crucial for bolstering resilience against disturbances and adversities. These resources range from financial to technological and play a pivotal role in equipping communities and systems to face challenges (Koliou et al., 2020). Five subcategories define this attribute: finance, infrastructure, natural resources, technology, and services.

Finance:
Finance refers to the capacity to access, manage and effectively use financial resources. This aspect is essential in resilience building, as financial funds enable the implementation of climate change adaptation measures and strategies (Zhang & Managi, 2020). The robustness of internal funding, i.e., funds generated and managed within the community or system, is often more significant than external funding sources. This suggests that strengthening skills and strategies to improve internal funding may result in more effective management of financial resources (Reguero et al., 2020). This optimization in the management of finances enhances resilience to disasters and increases long-term resilience in a more efficient and sustainable manner.

To what extent do the actions within your Resilience-Building Plan introduce or promote financial mechanisms supporting diverse stakeholders in climate change efforts?

Infrastructure:
Infrastructure encompasses the physical and systematic facilities that are essential to the functioning and well-being of a community or society. Ensuring the resilience of infrastructure is critical, as these facilities act as platforms that can absorb and withstand catastrophes, thereby increasing the resilience of society (Andersson et al., 2019). In addition, a well-maintained infrastructure adapted to climate change can provide vital services during disruptions, minimizing negative impacts on the community.

To what extent do the actions within your Resilience-Building Plan contribute to sustainable infrastructure development resilient to climate risks?

Natural Resources:
The effective management and use of natural resources is fundamental to the life and well-being of communities and ecosystems. These resources, also known as nature's services, are assets provided by the environment that can increase the resilience of people and systems (Silver et al., 2019). Sustainable management of natural resources ensures their long-term availability and enables adaptation and recovery in the face of climate shocks.

To what extent do the actions within your Resilience-Building Plan advocate for ecosystem conservation/restoration and the improvement of ecological services accessed by communities?

Technologies:
Access to and use of appropriate technologies can significantly facilitate adaptation to climate change. Technologies can improve the efficiency and effectiveness of processes and, at the same time, act as a backup in case of catastrophes (Min, 2019). From the development of information and communication technologies to the implementation of renewable energy technologies, these tools can contribute to building more resilient and sustainable systems.

To what extent do the actions within your Resilience-Building Plan encourage the introduction or enhancement of technological solutions to address climate change?

Basic services:
Access to a wide range of services is a crucial component of supporting climate change adaptation. These services can include health, education, infrastructure services, and others (Simpson et al., 2019). A resilient system ensures that these services remain accessible and functional during shocks, ensuring the well-being of the community and maintaining its ability to recover and adapt to the challenges of climate change.

To what extent do the actions within your Resilience-Building Plan improve access to essential services fostering community well-being in the context of climate change adaptation?

27. Narrative of Resilience Attributes

The narrative of resilience attributes adds an essential qualitative dimension to the metrics-driven evaluation process, with a particular focus on weaving a story of climate resilience. This narrative provides a systematic method for pinpointing key points in the plan's strategy and facilitates an understanding of the logic and context behind the selection of specific resilience attributes. Through this narrative approach, the ongoing story of how climate resilience is being built is told, delving into the nuanced and strategic considerations involved.

This narrative becomes a vital tool in giving stakeholders a deeper understanding of how individual elements integrate into an overarching strategy to combat the adverse effects of climate change. In this way, it fosters greater stakeholder engagement, optimizes governance, and ensures more efficient implementation in climate resilience.

The narrative complements the questions on the ‘intentionality’ of Resilience Attributes. It shows the ways in which you are aiming to achieve the impact that is intended and declared. Please strive to make your narrative as coherent as possible with the subcategories of resilience attributes that were selected above.

To guide you in drafting it, the narrative is structured around three fundamental questions: "What?", "Who?", and "How long?" is climate resilience being built.

Tangible: What?

This dimension refers to the tangible and explicit presence of the capacity or skill being reinforced to boost the resilience of specific individuals or systems. An attribute is considered tangible when it manifests in specific and detailed actions, processes, or products, thereby providing concrete evidence of its effectiveness.

In relation to the tangible outcomes, could you describe the main product, process, or capacity that your Resilience-Building Plan aims to specifically enhance or develop? How will this concrete outcome strengthen the resilience of specific individuals or systems?

Inclusive: Who?

This dimension focuses on ensuring equitable access and benefits across all involved actors. A resilience attribute is deemed inclusive when it acknowledges and respects the diversity of experiences and needs and proactively seeks to widen the scope of the capacity or skill under enhancement. This attribute aims to cultivate a relational perspective on resilience, fostering collaborative participation between individuals and systems.

How does your Resilience-Building Plan ensure inclusivity, recognizing and respecting the diverse experiences and needs of all involved stakeholders? How does the plan actively strive to extend the benefits and capacities being enhanced for resilience to everyone involved?

Sustainable: How long?

This dimension examines the durability and ongoing impact of the resilience attribute. It is considered "enduring" when it continually extends its positive influence, thereby bolstering the capacity or skill in question. Additionally, this measure emphasizes a sustained commitment to the attribute, safeguarding its long-term contribution to resilience.

In terms of the sustainability and longevity of your Resilience-Building Plan's impact, what strategies and safeguards are in place to ensure that the actions taken will remain relevant and effective over time?

"""


#list
ra_likert_recode = {'0 - Not addressed in the current plan.' : '0',
                        '1 - Indirectly considered; not the primary focus.' : '1',
                        '2 - Directly addressed by some actions.' : '2',
                        '3 - Important in many actions but not always central.':'3',
                        '4 - Central to most actions in the plan.' : '4',}

df_2023_plan.rename(columns = {'r135':'Preparedness',
    'r136':'Planning',
    'r137':'Experiential_learning',
    'r138':'Educational_learning',
    'r139':'Autonomy',
    'r140':'Leadership',
    'r141':'Decision_making',
    'r142':'Collective_participation',
    'r143':'Connectivity',
    'r144':'Coordination', #Networking
    'r145':'Diversity',
    'r146':'Redundancy',
    'r147':'Distributive_Equity',  # EQUITE
    'r148':'Equity_of_Access', # INCLUSIVITY
    'r149':'Finance',
    'r150':'Infrastructure',
    'r151':'Natural_resources',
    'r152':'Technologies',
    'r153':'Basic_services',}, inplace = True) ## New Name

# Old Name: "Equity" --> New Name ---> "Distributive_Equity" 
# Old Name: "Inclusivity" --> New Name --> 'Equity_of_Access'
# Old Name: "Services" ---> New Name --> 'Basic_services'
# Old Name: "Networking" --> New Name  --> 'Coordination'

sub_ra_likert_var_list = ['Preparedness','Planning','Experiential_learning','Educational_learning','Autonomy','Leadership',
'Decision_making','Collective_participation','Connectivity','Coordination','Diversity','Redundancy','Distributive_Equity','Equity_of_Access',
'Finance','Infrastructure','Natural_resources','Technologies','Basic_services',]

#Replacing Values sub RA
df_2023_plan[sub_ra_likert_var_list] = df_2023_plan[sub_ra_likert_var_list].replace(ra_likert_recode)
##To numeric
df_2023_plan[sub_ra_likert_var_list] = df_2023_plan[sub_ra_likert_var_list].apply(pd.to_numeric, errors='coerce')

df_2023_plan['Equity_Inclusivity_mean']         = df_2023_plan[['Distributive_Equity','Equity_of_Access']].apply(lambda x: x.mean(), axis=1)
df_2023_plan['Social_Collaboration_mean']       = df_2023_plan[['Collective_participation','Connectivity','Coordination']].apply(lambda x: x.mean(), axis=1)
df_2023_plan['Preparedness_and_planning_mean']  = df_2023_plan[['Preparedness','Planning']].apply(lambda x: x.mean(), axis=1)
df_2023_plan['Learning_mean']                   = df_2023_plan[['Experiential_learning','Educational_learning']].apply(lambda x: x.mean(), axis=1)
df_2023_plan['Agency_mean']                     = df_2023_plan[['Autonomy','Leadership','Decision_making']].apply(lambda x: x.mean(), axis=1)
df_2023_plan['Flexibility_mean']                = df_2023_plan[['Diversity','Redundancy']].apply(lambda x: x.mean(), axis=1)
df_2023_plan['Assets_mean']                     = df_2023_plan[['Finance','Natural_resources','Technologies','Infrastructure','Basic_services']].apply(lambda x: x.mean(), axis=1)

ra_intentionality_list = sub_ra_likert_var_list

ra_plan_mean_list = ['Equity_Inclusivity_mean','Social_Collaboration_mean',
                     'Preparedness_and_planning_mean','Learning_mean',
                     'Agency_mean','Flexibility_mean','Assets_mean']

ra_variables_to_recode = {
'r154':'Tangible_ra_narrative',
'r155':'Inclusive_ra_narrative',
'r156':'Sustainable_ra_narrative',
}
df_2023_plan = df_2023_plan.rename(columns=ra_variables_to_recode)


ra_narrative_list = ['Tangible_ra_narrative','Inclusive_ra_narrative','Sustainable_ra_narrative',]

df_2023_plan['ra_intentionality_status'] = df_2023_plan[ra_intentionality_list].notna().all(axis=1)  
df_2023_plan['ra_narrative_status'] = df_2023_plan[ra_narrative_list].notna().all(axis=1)  


# Convert columns to numeric (float), errors='coerce' will turn non-convertible values to NaN
for col in ra_intentionality_list:
    df_2023_plan[col] = pd.to_numeric(df_2023_plan[col], errors='coerce')

df_2023_plan['sub_ra_central_targeted_concat'] = df_2023_plan.apply(
    lambda row: '; '.join([col for col in ra_intentionality_list if row[col] == 4]),
    axis=1
)

df_2023_plan['sub_ra_targeted_but_not_central_concat'] = df_2023_plan.apply(
    lambda row: '; '.join([col for col in ra_intentionality_list if (row[col] > 1) & (row[col] != 4)]),
    axis=1
)

df_2023_plan['sub_ra_central_targeted_counts'] = df_2023_plan['sub_ra_central_targeted_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
df_2023_plan['sub_ra_targeted_but_not_central_counts'] = df_2023_plan['sub_ra_targeted_but_not_central_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))

required_ra_list_to_rename = ['sub_ra_central_targeted_concat','sub_ra_targeted_but_not_central_concat']

for col in required_ra_list_to_rename:
    df_2023_plan[col] = df_2023_plan[col].astype(str).apply(lambda x: x.replace('_subra', ''))
    
sub_ra_responses_list = ra_plan_mean_list + ['sub_ra_central_targeted_concat','sub_ra_central_targeted_counts','sub_ra_targeted_but_not_central_concat','sub_ra_targeted_but_not_central_counts'] + ra_narrative_list


#RA Plan SubIndex ra_plan_subidx
ra_list_to_index = ['ra_intentionality_status','ra_narrative_status']
df_2023_plan['ra_plan_subidx'] = (df_2023_plan[ra_list_to_index].mean(axis=1) * 100).astype(int)
ra_plan_summary_list = ['ra_plan_subidx']+ra_list_to_index
# st.write("### RA summary")
# st.write(df_2023_plan[ra_plan_summary_list])

index_list = ra_list_to_index
df_2023_plan['ra_plan_req'] = df_2023_plan.apply(identify_req_status, axis=1)
# df_2023_p lan[['ra_plan_subidx','ra_plan_req']+ra_list_to_index]


ra_plan_responses_list = sub_ra_responses_list
ra_plan_result_list = ['ra_plan_subidx','ra_plan_req'] 
ra_plan_list_to_index = ra_list_to_index
ra_plan_plan_all_list = ra_plan_responses_list + ra_plan_result_list + ra_plan_list_to_index
 ##
##  ##
 ##
# st.write("ra_plan_all_list",df_2023_plan[ra_plan_plan_all_list])



## Section 5.2: Define Interventions Magnitude

info_primary_beneficiaries_magnitude ="""28. Magnitude metrics
Magnitude Metrics focus on quantifying the impact of resilience-building initiatives in numerical terms, specifically the number of people affected. These metrics are essential not only for measuring the scope of the built resilience but also for precisely defining the intervention of the plan by identifying the individual beneficiaries and assessing how many of them become more resilient as a result.

Just as was requested for the Partner’s Pledge Statement, the first step in using Magnitude Metrics is the clear identification of primary beneficiaries. These beneficiaries are categorized into various groups, including Companies, Regions, Cities, Natural Systems, and Direct Individuals. This approach to categorization provides a more detailed and tailored view of the beneficiaries, allowing for better targeting of interventions and resources.

Once the beneficiaries are identified, the next step is to estimate the number of individuals who will become more resilient as a result of the implemented actions. This quantification is carried out by country and by type of beneficiary, providing a comprehensive view of the scale and impact of the interventions.

It is essential to emphasize that even if the focus may be on beneficiaries like Companies, Regions, Cities, or Natural Systems, all partners will be  required to also quantify the impact on individuals (e.g. the indirect impact that can be achieved on people, households and communities as a side-effect of the direct impact sought on the primary beneficiary; more guidance on this in the following pages). This is in line with the primary objective of the campaign to foster resilience at an individual level, ensuring that all initiatives contribute to this overarching goal.

29. Types of Beneficiaries to be Made More Resilient to Climate Change by 2030

Start by identifying the primary type of beneficiary that your Plan aims to make more resilient. This is vital as it will guide the interventions in your Plan. 

Once you've identified your primary beneficiaries, you will be expected to estimate the number of individual beneficiaries within that category who will become more resilient due to the Plan (except, of course, if you selected the category of ‘direct individuals’ as primary beneficiary). Adherence to these guidelines is crucial for accurate reporting and avoiding double-counting.

If you're uncertain which types of beneficiaries best align with the focus of your Resilience-Building Plan, you can refer to the examples provided in the guide. After making your selection, click on it to access customized instructions for completing the Plan's metrics and interventions. You can select as many categories of beneficiaries as you see fit.

Individuals: This is the main target of the Campaign and should be selected by all initiatives that work directly with people, households, and individuals who are members of communities.
Companies: This pertains to actions that make companies and businesses more resilient to the risks of climate change. By doing so, they indirectly safeguard livelihoods and the provision of essential services.
Regions: These are actions aimed at large geographical areas, whether they're administrative, ecological, or otherwise, to boost their resilience against climate change.
Cities: These actions target urban centers to enhance their resilience against climate change.
Natural Systems: These actions aim to protect, conserve, or restore ecosystems, making them more resilient to climate change and thereby safeguarding vital ecosystem services.

You will be prompted to submit a resilience-building plan based solely on the types of primary beneficiaries you identify in this question.

IMPORTANT: As part of the RtR Global Campaign, all RtR Partners are required to estimate the number of individual beneficiaries. However, it's crucial to first identify the main type of beneficiary for each different plan that you might submit. 

Please note that this question focuses on those main types of beneficiaries. For instance, if you collaborate with city administrations to improve their water infrastructure, then the cities are your primary beneficiaries. In such a case, refrain from listing 'individuals' as primary beneficiaries in the relevant section. The benefits to individuals in this context are secondary, as they are derived through the cities. Therefore, please complete only the 'Cities' section as your primary beneficiary and provide the estimated count of individual beneficiaries within that section.
"""


rename_plan = {'r158':'companies_plan',
          'r162':'companies_n_comp_plan_2023',
          'r205':'companies_n_indiv_plan_2023',
          'r159':'region_plan',
          'r771':'region_n_reg_plan_2023',
          'r815':'region_n_indiv_plan_2023',
          'r160':'cities_plan',
          'r1381':'cities_n_cit_plan_2023',
          'r1417':'cities_n_indiv_plan_2023',
          'r161':'natsyst_plan',
          'r1995':'natsyst_n_hect_plan_2023',
          'r2013':'natsyst_n_indiv_plan_2023',
          'r157':'d_indiv_plan',
          'r2580':'d_indiv_number_plan_2023',}
df_2023_plan = df_2023_plan.rename(columns = rename_plan)


key_metrics_2023_plan_list = ['companies_n_comp_plan_2023',
                                'companies_n_indiv_plan_2023',
                                'region_n_reg_plan_2023',
                                'region_n_indiv_plan_2023',
                                'cities_n_cit_plan_2023',
                                'cities_n_indiv_plan_2023',
                                'natsyst_n_hect_plan_2023',
                                'natsyst_n_indiv_plan_2023',
                                'd_indiv_number_plan_2023']
df_2023_plan[key_metrics_2023_plan_list] = df_2023_plan[key_metrics_2023_plan_list].fillna(0).astype(int)
# st.write('All variables Data plan Metrics',df_plan[key_metrics_2023_plan_list + key_plan_2022_info_list ]) 

# Creating final number of infividuals in plan 2023 to compare it with its relative in 2022
individuals_beneficiaries_plan_2023_list = ['companies_n_indiv_plan_2023',
                                              'region_n_indiv_plan_2023',
                                              'cities_n_indiv_plan_2023',
                                              'natsyst_n_indiv_plan_2023',
                                              'd_indiv_number_plan_2023',]
# Sum across specified columns for each row and assign to a new column
df_2023_plan['individuals_n_total_plan_2023'] = df_2023_plan[individuals_beneficiaries_plan_2023_list].sum(axis=1) ## FINAL NUMBER OF INDIVIDUALS DECLARED AS plan
p_beneficiaries_plan_2023_list = ['d_indiv_plan','companies_plan','region_plan','cities_plan','natsyst_plan']



df_2023_plan['p_beneficiaries_plan_concat'] = df_2023_plan[p_beneficiaries_plan_2023_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['p_beneficiaries_plan_concat'] = df_2023_plan['p_beneficiaries_plan_concat'].apply(lambda x: ';'.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['p_beneficiaries_plan_counts'] = df_2023_plan['p_beneficiaries_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
p_beneficiaries_plan_responses = ['p_beneficiaries_plan_concat','p_beneficiaries_plan_counts']
# df_2023_plan[p_beneficiaries_plan_responses]

# st.write("## Section 5.2: Define Interventions Magnitude")
# st.markdown("### 5.2.1) Primary Beneficiaries Identification (Plan)")

### 5.2.2) Companies (Plan)
# st.markdown("### 5.2.2) Companies (Plan)")
companies_l = ['companies_plan']
companies_n_companies_plan_l = ['companies_n_comp_plan_2023',]
# Ensure the data is numeric
df_2023_plan[companies_n_companies_plan_l] = df_2023_plan[companies_n_companies_plan_l].apply(pd.to_numeric, errors='coerce')
#Number of Companies
# st.write("Number of Companies (Sum)", df_2023_plan[companies_n_companies_plan_l[0]].sum())
# st.write("Number of Companies (Adjusted *0.75)", df_2023_plan[companies_n_companies_plan_l[0]].sum()*0.75)
df_2023_plan['companies_n_companies_plan_status'] = df_2023_plan[companies_n_companies_plan_l].notna().any(axis=1)
df_2023_plan.loc[df_2023_plan[companies_n_companies_plan_l[0]] == 0, 'companies_n_companies_plan_status'] = False
# st.write(df_2023_plan[companies_l + companies_n_companies_plan_l+['companies_n_companies_plan_status']])

companies_sector_plan_l = ['r' + str(i) for i in range(163, 185)]
df_2023_plan['companies_sector_plan_status'] = df_2023_plan[companies_sector_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[companies_l + companies_sector_plan_l+['companies_sector_plan_status']])

companies_sector_plan_l = ['r' + str(i) for i in range(185, 205)]
df_2023_plan['companies_sector_plan_status'] = df_2023_plan[companies_sector_plan_l].notna().any(axis=1)
df_2023_plan['companies_sector_plan_concat'] = df_2023_plan[companies_sector_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['companies_sector_plan_concat'] = df_2023_plan['companies_sector_plan_concat'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['companies_sector_plan_counts'] = df_2023_plan['companies_sector_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
companies_sector_plan_responses = ['companies_sector_plan_concat','companies_sector_plan_counts']

companies_types_of_individuals_plan_l = ['r' + str(i) for i in range(185, 205)]
df_2023_plan['companies_types_of_individuals_plan_status'] = df_2023_plan[companies_types_of_individuals_plan_l].notna().any(axis=1)
df_2023_plan['companies_types_of_individuals_plan_concat'] = df_2023_plan[companies_types_of_individuals_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['companies_types_of_individuals_plan_concat'] = df_2023_plan['companies_types_of_individuals_plan_concat'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['companies_types_of_individuals_plan_counts'] = df_2023_plan['companies_types_of_individuals_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
companies_types_of_individuals_plan_responses = ['companies_types_of_individuals_plan_concat','companies_types_of_individuals_plan_counts']

companies_n_individuals_plan_l = ['companies_n_indiv_plan_2023']
# Ensure the data is numeric
df_2023_plan[companies_n_individuals_plan_l] = df_2023_plan[companies_n_individuals_plan_l].apply(pd.to_numeric, errors='coerce')
df_2023_plan['companies_n_individuals_plan_status'] = df_2023_plan[companies_n_individuals_plan_l].notna().any(axis=1)
df_2023_plan.loc[df_2023_plan[companies_n_individuals_plan_l [0]] == 0, 'companies_n_individuals_plan_status'] = False
## Number of individuals --> Companies
# st.write("Number of Individuals --> Companies (sum)",df_2023_plan[companies_n_individuals_plan_l[0]].sum())

companies_continents_plan_l = ['r' + str(i) for i in range(206, 212)]
df_2023_plan['companies_continents_plan'] = df_2023_plan[companies_continents_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[companies_continents_plan_l+['companies_continents_plan']])

companies_countries_plan_all_l =['r' + str(i) for i in range(212, 398)]
df_2023_plan['companies_countries_plan_all_status'] = df_2023_plan[companies_countries_plan_all_l].notna().any(axis=1)
# st.write(df_2023_plan[companies_countries_plan_all_l+['companies_countries_plan_all_status']])

companies_capabily_country_level_plan_l = ['r398',]
df_2023_plan['companies_capabily_country_level_plan'] = df_2023_plan[companies_capabily_country_level_plan_l].notna().any(axis=1)
# st.write("# Pledge Companies Capability")
# st.write(df_2023_plan[companies_capabily_country_level_plan_l+['companies_capabily_country_level_plan']])
 
companies_distribution_individuals_per_country_plan_l = ['r' + str(i) for i in range(399, 771)]
df_2023_plan['companies_distribution_individuals_per_country_plan'] = df_2023_plan[companies_distribution_individuals_per_country_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[companies_distribution_individuals_per_country_plan_l+['companies_distribution_individuals_per_country_plan']])

companies_idx_list_plan = ['companies_n_companies_plan_status','companies_sector_plan_status',
                           'companies_types_of_individuals_plan_status',
                           'companies_n_individuals_plan_status','companies_countries_plan_all_status',]
df_2023_plan.loc[df_2023_plan['companies_plan'].isna(), companies_idx_list_plan] = False


## Companies Plan Sub Index
weights = {
    'companies_n_companies_plan_status':0.12,
    'companies_sector_plan_status':0.03,
    'companies_types_of_individuals_plan_status':0.05,
    'companies_n_individuals_plan_status':0.4,
    'companies_countries_plan_all_status':0.4,
    }

# Calculate the weighted sum of the components for companies_sub_subidx_plan
df_2023_plan['companies_sub_subidx_plan'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_2023_plan['companies_sub_subidx_plan'] = (df_2023_plan['companies_sub_subidx_plan'] * 100).astype(int)

# companies_idx_list_plan_all = companies_l + companies_n_companies_plan_l + companies_n_individuals_plan_l + ['companies_sub_subidx_plan'] + companies_idx_list_plan 

index_list = companies_idx_list_plan
df_2023_plan['companies_sub_subidx_plan_req'] = df_2023_plan.apply(identify_req_status, axis=1)
df_2023_plan.loc[df_2023_plan['companies_plan'].isna(), 'companies_sub_subidx_plan_req'] = "No Apply"

companies_plan_responses_list = companies_l + ['companies_n_comp_plan_2023','companies_n_indiv_plan_2023'] + companies_sector_plan_responses  + companies_types_of_individuals_plan_responses
companies_plan_result_list = ['companies_sub_subidx_plan','companies_sub_subidx_plan_req'] 
companies_plan_list_to_index = companies_idx_list_plan
companies_plan_plan_all_list = companies_plan_responses_list + companies_plan_result_list + companies_plan_list_to_index
 ##
##  ##
 ##
# st.write("companies_plan_all_list",df_2023_plan[companies_plan_plan_all_list])



### 5.2.3) Regions (Plan)
# st.markdown("### 5.2.3) Regions (Plan)")
regions_l = ['region_plan']
regions_n_regions_plan_l = ['region_n_reg_plan_2023',]
# Ensure the data is numeric
df_2023_plan[regions_n_regions_plan_l] = df_2023_plan[regions_n_regions_plan_l].apply(pd.to_numeric, errors='coerce')
#Number of Regions
# st.write("Number of Regions (sum)", df_2023_plan[regions_n_regions_plan_l[0]].sum())
# st.write("Number of Regions (Adjusted *0.75)", df_2023_plan[regions_n_regions_plan_l[0]].sum()*0.75)

df_2023_plan['regions_n_regions_plan_status'] = df_2023_plan[regions_n_regions_plan_l].notna().any(axis=1)
df_2023_plan.loc[df_2023_plan[regions_n_regions_plan_l [0]] == 0, 'regions_n_regions_plan_status'] = False
# st.write(df_2023_plan[regions_l + regions_n_regions_plan_l+['regions_n_regions_plan_status']])

regions_primary_beneficiaries_plan_l = ['r' + str(i) for i in range(772, 799)]
df_2023_plan['regions_primary_beneficiaries_plan_status'] = df_2023_plan[regions_primary_beneficiaries_plan_l].notna().any(axis=1)
df_2023_plan['regions_primary_beneficiaries_plan_concat'] = df_2023_plan[regions_primary_beneficiaries_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['regions_primary_beneficiaries_plan_concat'] = df_2023_plan['regions_primary_beneficiaries_plan_concat'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['regions_primary_beneficiaries_plan_counts'] = df_2023_plan['regions_primary_beneficiaries_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
regions_primary_beneficiaries_plan_responses = ['regions_primary_beneficiaries_plan_concat','regions_primary_beneficiaries_plan_counts']


regions_types_of_individuals_plan_l = ['r' + str(i) for i in range(799, 815)]
df_2023_plan['regions_types_of_individuals_plan_status'] = df_2023_plan[regions_types_of_individuals_plan_l].notna().any(axis=1)
df_2023_plan['regions_types_of_individuals_plan_concat'] = df_2023_plan[regions_types_of_individuals_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['regions_types_of_individuals_plan_concat'] = df_2023_plan['regions_types_of_individuals_plan_concat'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['regions_types_of_individuals_plan_counts'] = df_2023_plan['regions_types_of_individuals_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
regions_types_of_individuals_plan_responses = ['regions_types_of_individuals_plan_concat','regions_types_of_individuals_plan_counts']

regions_n_individuals_plan_l = ['region_n_indiv_plan_2023',]
df_2023_plan[regions_n_individuals_plan_l] = df_2023_plan[regions_n_individuals_plan_l].apply(pd.to_numeric, errors='coerce')
df_2023_plan['regions_n_individuals_plan_status'] = df_2023_plan[regions_n_individuals_plan_l].notna().any(axis=1)
df_2023_plan.loc[df_2023_plan[regions_n_individuals_plan_l [0]] == 0, 'regions_n_individuals_plan_status'] = False

#Number of individuals --> Regions
# st.write("Number of Individuals --> Regions (sum)",df_2023_plan[regions_n_individuals_plan_l[0]].sum())

regions_continents_plan_l = ['r' + str(i) for i in range(816, 822)]
df_2023_plan['regions_continents_plan'] = df_2023_plan[regions_continents_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[regions_continents_plan_l+['regions_continents_plan']])

regions_countries_plan_all_l =['r' + str(i) for i in range(822, 1008)]
df_2023_plan['regions_countries_plan_all_status'] = df_2023_plan[regions_countries_plan_all_l].notna().any(axis=1)
# st.write(df_2023_plan[regions_countries_plan_all_l+['regions_countries_plan_all_status']])

regions_capabily_country_level_plan_l = ['r1008',]
df_2023_plan['regions_capabily_country_level_plan'] = df_2023_plan[regions_capabily_country_level_plan_l].notna().any(axis=1)
# st.write("# Regions Capability")
# st.write(df_2023_plan[regions_capabily_country_level_plan_l+['regions_capabily_country_level_plan']])

regions_distribution_individuals_per_country_plan_l = ['r' + str(i) for i in range(1009, 1381)]
df_2023_plan['regions_distribution_individuals_per_country_plan'] = df_2023_plan[regions_distribution_individuals_per_country_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[regions_distribution_individuals_per_country_plan_l+['regions_distribution_individuals_per_country_plan']])
 
regions_idx_list_plan = ['regions_n_regions_plan_status','regions_primary_beneficiaries_plan_status',
                         'regions_types_of_individuals_plan_status','regions_n_individuals_plan_status',
                         'regions_countries_plan_all_status',]
df_2023_plan.loc[df_2023_plan['region_plan'].isna(), regions_idx_list_plan] = False

## Regions Plan Sub Index
weights = {
    'regions_n_regions_plan_status':0.12,
    'regions_primary_beneficiaries_plan_status':0.03,
    'regions_types_of_individuals_plan_status':0.05,
    'regions_n_individuals_plan_status':0.4,
    'regions_countries_plan_all_status':0.4,
    }

# Calculate the weighted sum of the components for regions_sub_subidx_plan
df_2023_plan['regions_sub_subidx_plan'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_2023_plan['regions_sub_subidx_plan'] = (df_2023_plan['regions_sub_subidx_plan'] * 100).astype(int)

#requested "_req"
index_list = regions_idx_list_plan
df_2023_plan['regions_sub_subidx_plan_req'] = df_2023_plan.apply(identify_req_status, axis=1)
df_2023_plan.loc[df_2023_plan['region_plan'].isna(), 'regions_sub_subidx_plan_req'] = "No Apply"
# df_2023_plan[['regions_sub_subidx_plan','regions_sub_subidx_plan_req']+regions_idx_list_plan]

regions_plan_responses_list = ['region_plan','region_n_reg_plan_2023']+regions_primary_beneficiaries_plan_responses + ['region_n_indiv_plan_2023'] +  regions_types_of_individuals_plan_responses 
regions_plan_result_list = ['regions_sub_subidx_plan','regions_sub_subidx_plan_req'] 
regions_plan_list_to_index = regions_idx_list_plan
regions_plan_plan_all_list = regions_plan_responses_list + regions_plan_result_list + regions_plan_list_to_index
 ##
##  ##
 ##
# st.write("regions_plan_all_list",df_2023_plan[regions_plan_plan_all_list])



 
### 5.2.4) Cities (Plan)

# st.markdown("### 5.2.4) Cities (Plan)")
cities_l = ['cities_plan',]
cities_n_cities_plan_l = ['cities_n_cit_plan_2023',]
# Ensure the data is numeric
df_2023_plan[cities_n_cities_plan_l] = df_2023_plan[cities_n_cities_plan_l].apply(pd.to_numeric, errors='coerce')
#Number of cities
# st.write("Number of cities (sum)", df_2023_plan[cities_n_cities_plan_l[0]].sum())
# st.write("Number of cities (adjusted *0.75)", df_2023_plan[cities_n_cities_plan_l[0]].sum()*0.75)

df_2023_plan['cities_n_cities_plan_status'] = df_2023_plan[cities_n_cities_plan_l].notna().any(axis=1)
df_2023_plan.loc[df_2023_plan[cities_n_cities_plan_l [0]] == 0, 'cities_n_cities_plan_status'] = False
# st.write(df_2023_plan[cities_l + cities_n_cities_plan_l+['cities_n_cities_plan_status']])

cities_primary_beneficiaries_plan_l = ['r' + str(i) for i in range(1382, 1401)]
df_2023_plan['cities_primary_beneficiaries_plan_status'] = df_2023_plan[cities_primary_beneficiaries_plan_l].notna().any(axis=1)
df_2023_plan['cities_primary_beneficiaries_plan_concat'] = df_2023_plan[cities_primary_beneficiaries_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['cities_primary_beneficiaries_plan_concat'] = df_2023_plan['cities_primary_beneficiaries_plan_concat'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['cities_primary_beneficiaries_plan_counts'] = df_2023_plan['cities_primary_beneficiaries_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
cities_primary_beneficiaries_plan_responses = ['cities_primary_beneficiaries_plan_concat','cities_primary_beneficiaries_plan_counts']

cities_types_of_individuals_plan_l = ['r' + str(i) for i in range(1401, 1417)]
df_2023_plan['cities_types_of_individuals_plan_status'] = df_2023_plan[cities_types_of_individuals_plan_l].notna().any(axis=1)
df_2023_plan['cities_type_individuals_plan_concat'] = df_2023_plan[cities_types_of_individuals_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['cities_type_individuals_plan_concat'] = df_2023_plan['cities_type_individuals_plan_concat'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['cities_type_individuals_plan_counts'] = df_2023_plan['cities_type_individuals_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
cities_type_individuals_plan_responses = ['cities_type_individuals_plan_concat','cities_type_individuals_plan_counts']

cities_n_individuals_plan_l = ['cities_n_indiv_plan_2023']
df_2023_plan[cities_n_individuals_plan_l] = df_2023_plan[cities_n_individuals_plan_l].apply(pd.to_numeric, errors='coerce')
df_2023_plan['cities_n_individuals_plan_status'] = df_2023_plan[cities_n_individuals_plan_l].notna().any(axis=1)
df_2023_plan.loc[df_2023_plan[cities_n_individuals_plan_l [0]] == 0, 'cities_n_individuals_plan_status'] = False

#Number of individuals --> cities
# st.write("Number of individuals --> Cities (sum): ",df_2023_plan[cities_n_individuals_plan_l[0]].sum())

cities_continents_plan_l = ['r' + str(i) for i in range(1418, 1424)]
df_2023_plan['cities_continents_plan'] = df_2023_plan[cities_continents_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[cities_continents_plan_l+['cities_continents_plan']])

cities_countries_plan_all_l =['r' + str(i) for i in range(1424,1610 )]
df_2023_plan['cities_countries_plan_all_status'] = df_2023_plan[cities_countries_plan_all_l].notna().any(axis=1)
# st.write(df_2023_plan[cities_countries_plan_all_l+[''cities_countries_plan_all_status']])

cities_capabily_country_level_plan_l = ['r1610',]
df_2023_plan['cities_capabily_country_level_plan'] = df_2023_plan[cities_capabily_country_level_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[['r1524','cities_capabily_country_level_plan']])

cities_distribution_individuals_per_country_plan_l = ['r' + str(i) for i in range(1611, 1983)]
df_2023_plan['cities_distribution_individuals_per_country_plan'] = df_2023_plan[cities_distribution_individuals_per_country_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[cities_distribution_individuals_per_country_plan_l+['cities_distribution_individuals_per_country_plan']])
 
cities_idx_list_plan =['cities_n_cities_plan_status','cities_primary_beneficiaries_plan_status',
                       'cities_types_of_individuals_plan_status','cities_n_individuals_plan_status',
                       'cities_countries_plan_all_status',]
df_2023_plan.loc[df_2023_plan['cities_plan'].isna(), cities_idx_list_plan] = False
cities_metrics_list = ['cities_n_cit_plan_2023','cities_n_indiv_plan_2023']
df_2023_plan.loc[df_2023_plan['cities_plan'].isna(), cities_metrics_list] = np.nan

## Cities Plan Sub Index
weights = {
    'cities_n_cities_plan_status':0.12,
    'cities_primary_beneficiaries_plan_status':0.03,
    'cities_types_of_individuals_plan_status':0.05,
    'cities_n_individuals_plan_status':0.4,
    'cities_countries_plan_all_status':0.4,
    }

# Calculate the weighted sum of the components for cities_sub_subidx_plan
df_2023_plan['cities_sub_subidx_plan'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_2023_plan['cities_sub_subidx_plan'] = (df_2023_plan['cities_sub_subidx_plan'] * 100).astype(int)

#requested "_req" info variable
index_list = cities_idx_list_plan
df_2023_plan['cities_sub_subidx_plan_req'] = df_2023_plan.apply(identify_req_status, axis=1)
df_2023_plan.loc[df_2023_plan['cities_plan'].isna(), 'cities_sub_subidx_plan_req'] = "No Apply"
# df_2023_plan[['cities_sub_subidx_plan','cities_sub_subidx_plan_req']+cities_idx_list_plan]

cities_plan_responses_list = cities_l + cities_n_cities_plan_l + cities_primary_beneficiaries_plan_responses + cities_n_individuals_plan_l + cities_type_individuals_plan_responses
cities_plan_result_list = ['cities_sub_subidx_plan','cities_sub_subidx_plan_req'] 
cities_plan_list_to_index = cities_idx_list_plan
cities_plan_plan_all_list = cities_plan_responses_list + cities_plan_result_list + cities_plan_list_to_index
 ##
##  ##
 ##
# st.write("cities_plan_all_list",df_2023_plan[cities_plan_plan_all_list])




### 5.2.5) Natural Systems (Plan)

# st.markdown("### 5.2.5) Natural Systems (Plan)")
natsyst_l = ['natsyst_plan',]
natsyst_type_natsyst_plan_l = ['r' + str(i) for i in range(1983, 1995)]
df_2023_plan['natsyst_type_natsyst_plan_status'] = df_2023_plan[natsyst_type_natsyst_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[natsyst_l + natsyst_type_natsyst_plan_l+['natsyst_type_natsyst_plan_status']])
df_2023_plan['natsyst_type_natsyst_plan_concat'] = df_2023_plan[natsyst_type_natsyst_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['natsyst_type_natsyst_plan_concat'] = df_2023_plan['natsyst_type_natsyst_plan_concat'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['natsyst_type_natsyst_plan_counts'] = df_2023_plan['natsyst_type_natsyst_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
natsyst_type_natsyst_plan_responses = ['natsyst_type_natsyst_plan_concat','natsyst_type_natsyst_plan_counts']

natsyst_n_hectares_plan_l = ['natsyst_n_hect_plan_2023',]
# Ensure the data is numeric
df_2023_plan[natsyst_n_hectares_plan_l] = df_2023_plan[natsyst_n_hectares_plan_l].apply(pd.to_numeric, errors='coerce')
#Number of Hectares
# st.write("Number of Hectares (sum)", df_2023_plan[natsyst_n_hectares_plan_l[0]].sum())
# st.write("Number of Hectares (adjusted *0.75)", df_2023_plan[natsyst_n_hectares_plan_l[0]].sum()*0.75)

df_2023_plan['natsyst_n_hectares_plan_status'] = df_2023_plan[natsyst_n_hectares_plan_l].notna().any(axis=1)
df_2023_plan.loc[df_2023_plan[natsyst_n_hectares_plan_l [0]] == 0, 'natsyst_n_hectares_plan_status'] = False
# st.write(df_2023_plan[natsyst_l + natsyst_n_hectares_plan_l+['natsyst_n_hectares_plan_status']])
#Other number of Natural Systems
# st.write(df_2023_plan['r1996',])

natsyst_types_of_individuals_plan_l = ['r' + str(i) for i in range(1997, 2013)]
df_2023_plan['natsyst_types_of_individuals_plan_status'] = df_2023_plan[natsyst_types_of_individuals_plan_l].notna().any(axis=1)
df_2023_plan['natsyst_types_of_individuals_plan_concat'] = df_2023_plan[natsyst_types_of_individuals_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['natsyst_types_of_individuals_plan_concat'] = df_2023_plan['natsyst_types_of_individuals_plan_concat'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['natsyst_types_of_individuals_plan_counts'] = df_2023_plan['natsyst_types_of_individuals_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
natsyst_types_of_individuals_plan_responses = ['natsyst_types_of_individuals_plan_concat','natsyst_types_of_individuals_plan_counts']


natsyst_n_individuals_plan_l = ['natsyst_n_indiv_plan_2023',]
df_2023_plan[natsyst_n_individuals_plan_l] = df_2023_plan[natsyst_n_individuals_plan_l].apply(pd.to_numeric, errors='coerce')
df_2023_plan['natsyst_n_individuals_plan_status'] = df_2023_plan[natsyst_n_individuals_plan_l].notna().any(axis=1)
df_2023_plan.loc[df_2023_plan[natsyst_n_individuals_plan_l [0]] == 0, 'natsyst_n_individuals_plan_status'] = False
# st.write(df_2023_plan[natsyst_n_individuals_plan_l])
# #Number of individuals --> natsyst
# st.write("Number Individuals --> Natural Systems (sum)", df_2023_plan[natsyst_n_individuals_plan_l[0]].sum())
# st.write("Number Individuals --> Natural Systems (adjusted 0*75)", df_2023_plan[natsyst_n_individuals_plan_l[0]].sum()*0.75)


natsyst_continents_plan_l = ['r' + str(i) for i in range(2014, 2020)]
df_2023_plan['natsyst_continents_plan'] = df_2023_plan[natsyst_continents_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[natsyst_continents_plan_l+['natsyst_continents_plan']])

natsyst_countries_plan_all_l =['r' + str(i) for i in range(2020, 2206)]
df_2023_plan['natsyst_countries_plan_all_status'] = df_2023_plan[natsyst_countries_plan_all_l].notna().any(axis=1)
# st.write(df_2023_plan[natsyst_countries_plan_all_l+['natsyst_countries_plan_all_status']])

natsyst_capabily_country_level_plan_l = ['r2206',]
df_2023_plan['natsyst_capabily_country_level_plan'] = df_2023_plan[natsyst_capabily_country_level_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[natsyst_capabily_country_level_plan_l+['natsyst_capabily_country_level_plan']])

natsyst_distribution_individuals_per_country_plan_l = ['r' + str(i) for i in range(2207, 2580)]
df_2023_plan['natsyst_distribution_individuals_per_country_plan'] = df_2023_plan[natsyst_distribution_individuals_per_country_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[natsyst_distribution_individuals_per_country_plan_l+['natsyst_distribution_individuals_per_country_plan']])

natsyst_idx_list_plan =['natsyst_type_natsyst_plan_status','natsyst_n_hectares_plan_status',
                        'natsyst_types_of_individuals_plan_status','natsyst_n_individuals_plan_status',
                        'natsyst_countries_plan_all_status',]    
df_2023_plan.loc[df_2023_plan['natsyst_plan'].isna(), natsyst_idx_list_plan] = False
natsyst_metrics_list = ['natsyst_n_hect_plan_2023','natsyst_n_indiv_plan_2023']
df_2023_plan.loc[df_2023_plan['natsyst_plan'].isna(), natsyst_metrics_list] = np.nan

## Natural Systems Plan Sub Index
weights = {
    'natsyst_type_natsyst_plan_status':0.03,
    'natsyst_n_hectares_plan_status':0.12,
    'natsyst_types_of_individuals_plan_status':0.05,
    'natsyst_n_individuals_plan_status':0.4,
    'natsyst_countries_plan_all_status':0.4,
    }

# Calculate the weighted sum of the components for natsyst_sub_subidx_plan
df_2023_plan['natsyst_sub_subidx_plan'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_2023_plan['natsyst_sub_subidx_plan'] = (df_2023_plan['natsyst_sub_subidx_plan'] * 100).astype(int)

#requested "_req" info variable
index_list = natsyst_idx_list_plan
df_2023_plan['natsyst_sub_subidx_plan_req'] = df_2023_plan.apply(identify_req_status, axis=1)
df_2023_plan.loc[df_2023_plan['natsyst_plan'].isna(), 'natsyst_sub_subidx_plan_req'] = "No Apply"
# df_2023_plan[['natsyst_sub_subidx_plan','natsyst_sub_subidx_plan_req']+natsyst_idx_list_plan]

natsyst_plan_responses_list = natsyst_l + natsyst_n_hectares_plan_l + natsyst_type_natsyst_plan_responses + natsyst_n_individuals_plan_l + natsyst_types_of_individuals_plan_responses
natsyst_plan_result_list = ['natsyst_sub_subidx_plan','natsyst_sub_subidx_plan_req'] 
natsyst_plan_list_to_index = natsyst_idx_list_plan
natsyst_plan_plan_all_list = natsyst_plan_responses_list + natsyst_plan_result_list + natsyst_plan_list_to_index
 ##
##  ##
 ##
# st.write("natsyst_plan_all_list",df_2023_plan[natsyst_plan_plan_all_list])



 

### 5.2.6) Direct Individuals (Plan)
# st.markdown("### 5.2.6) Direct Individuals (Plan)")
d_indivdls_l = ['d_indiv_plan']
d_indivdls_num_d_indivdls_plan_l = ['d_indiv_number_plan_2023',]
partner_name = ['r9']
# Ensure the data is numeric
df_2023_plan[d_indivdls_num_d_indivdls_plan_l] = df_2023_plan[d_indivdls_num_d_indivdls_plan_l].apply(pd.to_numeric, errors='coerce')
df_2023_plan['d_indivdls_num_d_indivdls_plan_status'] = df_2023_plan[d_indivdls_num_d_indivdls_plan_l].notna().any(axis=1)
df_2023_plan.loc[df_2023_plan[d_indivdls_num_d_indivdls_plan_l [0]] == 0, 'd_indivdls_num_d_indivdls_plan_status'] = False
# st.write(df_2023_plan[partner_name + d_indivdls_l + d_indivdls_num_d_indivdls_plan_l+['d_indivdls_num_d_indivdls_plan_status']])
#Number of Direct Individuals
# st.write("Number of Direct Individuals (sum)",df_2023_plan[d_indivdls_num_d_indivdls_plan_l[0]].sum())
# st.write("Number of Direct Individuals (adjusted *0.75)", df_2023_plan[d_indivdls_num_d_indivdls_plan_l[0]].sum()*0.75)

d_indivdls_continents_plan_l = ['r' + str(i) for i in range(2581, 2587)]
df_2023_plan['d_indivdls_continents_plan'] = df_2023_plan[d_indivdls_continents_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[d_indivdls_continents_plan_l+['d_indivdls_continents_plan']])

d_indivdls_countries_plan_all_l =['r' + str(i) for i in range(2587, 2773)]
df_2023_plan['d_indivdls_countries_plan_all_status'] = df_2023_plan[d_indivdls_countries_plan_all_l].notna().any(axis=1)
# st.write("Tabla Paises")
# st.write(df_2023_plan[d_indivdls_countries_plan_all_l+['d_indivdls_countries_plan_all_status']])
columns_to_display = ['InitName', 'd_indivdls_countries_plan_all_status'] + d_indivdls_countries_plan_all_l
df_countries_plan_individuals = df_2023_plan[columns_to_display]
# st.write(df_countries_plan_individuals)

d_indivdls_capabily_country_level_plan_l = ['r2773',]
df_2023_plan['d_indivdls_capabily_country_level_plan'] = df_2023_plan[d_indivdls_capabily_country_level_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[d_indivdls_capabily_country_level_plan_l+['d_indivdls_capabily_country_level_plan']])

d_indivdls_distribution_individuals_per_country_plan_l = ['r' + str(i) for i in range(2774, 3146)]
df_2023_plan['d_indivdls_distribution_individuals_per_country_plan'] = df_2023_plan[d_indivdls_distribution_individuals_per_country_plan_l].notna().any(axis=1)
# st.write(df_2023_plan[d_indivdls_distribution_individuals_per_country_plan_l+['d_indivdls_distribution_individuals_per_country_plan']])
 
d_indivdls_idx_list_plan =['d_indivdls_num_d_indivdls_plan_status','d_indivdls_countries_plan_all_status',]    
df_2023_plan.loc[df_2023_plan['d_indiv_plan'].isna(), d_indivdls_idx_list_plan] = False
df_2023_plan['d_indivdls_sub_subidx_plan'] = (df_2023_plan[d_indivdls_idx_list_plan].mean(axis=1) * 100).astype(int)
# d_indivdls_idx_list_plan_all = d_indivdls_l + d_indivdls_num_d_indivdls_plan_l + ['d_indivdls_sub_subidx_plan'] + d_indivdls_idx_list_plan

#requested "_req" info variable
index_list = d_indivdls_idx_list_plan
df_2023_plan['d_indivdls_sub_subidx_plan_req'] = df_2023_plan.apply(identify_req_status, axis=1)
df_2023_plan.loc[df_2023_plan['d_indiv_plan'].isna(), 'd_indivdls_sub_subidx_plan_req'] = "No Apply"


d_indivdls_plan_responses_list = d_indivdls_l + d_indivdls_num_d_indivdls_plan_l
d_indivdls_plan_result_list = ['d_indivdls_sub_subidx_plan','d_indivdls_sub_subidx_plan_req'] 
d_indivdls_plan_list_to_index = d_indivdls_idx_list_plan
d_indivdls_plan_plan_all_list = d_indivdls_plan_responses_list + d_indivdls_plan_result_list + d_indivdls_plan_list_to_index
 ##
##  ##
 ##
# st.write("d_indivdls_plan_all_list",df_2023_plan[d_indivdls_plan_plan_all_list])



rename_plan = {'r158':'companies_plan',
          'r162':'companies_n_comp_plan_2023',
          'r205':'companies_n_indiv_plan_2023',
          'r159':'region_plan',
          'r771':'region_n_reg_plan_2023',
          'r815':'region_n_indiv_plan_2023',
          'r160':'cities_plan',
          'r1381':'cities_n_cit_plan_2023',
          'r1417':'cities_n_indiv_plan_2023',
          'r161':'natsyst_plan',
          'r1995':'natsyst_n_hect_plan_2023',
          'r2013':'natsyst_n_indiv_plan_2023',
          'r157':'d_indiv_plan',
          'r2580':'d_indiv_number_plan_2023',}


#PRIMARY BENEFICIARIES PLAN INDEX
## Primary Beneficiaries Identification adjusted by index of responses
df_2023_plan.loc[df_2023_plan['d_indivdls_sub_subidx_plan'] == 0, 'd_indiv_plan'] = np.nan
df_2023_plan.loc[df_2023_plan['companies_sub_subidx_plan'] == 0, 'companies_plan'] = np.nan
df_2023_plan.loc[df_2023_plan['regions_sub_subidx_plan'] == 0, 'region_plan'] = np.nan
df_2023_plan.loc[df_2023_plan['cities_sub_subidx_plan'] == 0, 'cities_plan'] = np.nan
df_2023_plan.loc[df_2023_plan['natsyst_sub_subidx_plan'] == 0, 'natsyst_plan'] = np.nan

#replacing 0 to nan
index_plan_list = ['d_indivdls_sub_subidx_plan','companies_sub_subidx_plan','regions_sub_subidx_plan','cities_sub_subidx_plan','natsyst_sub_subidx_plan',]
for col in index_plan_list:
    df_2023_plan.loc[df_2023_plan[col] == 0, col] = np.nan

primary_beneficiaries_identification_plan_l = ['d_indiv_plan','companies_plan','region_plan','cities_plan','natsyst_plan']
df_2023_plan['p_benefic_plan'] = df_2023_plan[primary_beneficiaries_identification_plan_l ].notna().any(axis=1)
df_2023_plan['p_benefic_count_plan'] = df_2023_plan[primary_beneficiaries_identification_plan_l].notna().sum(axis=1)
# st.write("# Numero de typos de beneficiarios")
# st.write(df_2023_plan[ primary_beneficiaries_identification_plan_l + ['p_benefic_count_plan']])

df_2023_plan['p_benefic_concat_plan'] = df_2023_plan[primary_beneficiaries_identification_plan_l].apply(lambda x: ';'.join(map(str, x)), axis=1)
df_2023_plan['p_benefic_concat_plan'] = df_2023_plan['p_benefic_concat_plan'].str.replace('nan', '')
df_2023_plan['p_benefic_concat_plan'] = df_2023_plan['p_benefic_concat_plan'].str.replace(';', ' ')
df_2023_plan['p_benefic_concat_plan'] = df_2023_plan['p_benefic_concat_plan'].str.replace('Natural Systems', 'Natural-Systems ')

def trim_spaces(s):
    return re.sub(' +', ' ', s.strip())

df_2023_plan['p_benefic_concat_plan'] = df_2023_plan['p_benefic_concat_plan'].apply(trim_spaces)
df_2023_plan['p_benefic_concat_plan'] = df_2023_plan['p_benefic_concat_plan'].str.replace(' ', '; ')
# st.write(df_2023_plan[primary_beneficiaries_identification_plan_l + ['p_benefic_plan','p_benefic_concat_plan']])

indexes_beneficiaries_list_plan = ['d_indivdls_sub_subidx_plan', 
                                   'companies_sub_subidx_plan',
                                   'regions_sub_subidx_plan', 
                                   'cities_sub_subidx_plan', 
                                   'natsyst_sub_subidx_plan']

df_2023_plan['pri_benef_magnitud_plan_subidx'] = df_2023_plan[indexes_beneficiaries_list_plan].sum(axis=1) / df_2023_plan['p_benefic_count_plan']
df_2023_plan['pri_benef_magnitud_plan_subidx'] = df_2023_plan['pri_benef_magnitud_plan_subidx'].fillna(0)
df_2023_plan['pri_benef_magnitud_plan_subidx'] = df_2023_plan['pri_benef_magnitud_plan_subidx'].apply(pd.to_numeric, errors='coerce')


p_beneficiaries_summary_list = ['p_benefic_concat_plan','p_benefic_count_plan','pri_benef_magnitud_plan_subidx']
# st.write('Primary Beneficiaries Plan', df_2023_plan[p_beneficiaries_summary_list])

pri_benef_magnitud_plan_req_list = ['d_indivdls_sub_subidx_plan_req',
'companies_sub_subidx_plan_req',
'regions_sub_subidx_plan_req',
'cities_sub_subidx_plan_req',
'natsyst_sub_subidx_plan_req',]


def concatenate_req_values(row):
    pending_values = []
    # Check each pair of conditions and concatenate the appropriate pending value
    if  0 < row['d_indivdls_sub_subidx_plan'] < 90:
        pending_values.append(row['d_indivdls_sub_subidx_plan_req'])
    if  0 < row['companies_sub_subidx_plan'] < 90:
        pending_values.append(row['companies_sub_subidx_plan_req'])
    if  0 < row['regions_sub_subidx_plan'] < 90:
        pending_values.append(row['regions_sub_subidx_plan_req'])
    if  0 < row['cities_sub_subidx_plan'] < 90:
        pending_values.append(row['cities_sub_subidx_plan_req'])
    if  0 < row['natsyst_sub_subidx_plan'] < 90:
        pending_values.append(row['natsyst_sub_subidx_plan_req'])
    
    # Join the collected pending values with a separator, e.g., ", "
    return ', '.join(filter(None, pending_values))  # filter(None, ...) removes empty strings

# Apply the function to each row in the DataFrame to create the new column
df_2023_plan['pri_benef_magnitud_plan_req'] = df_2023_plan.apply(concatenate_req_values, axis=1)

pri_benefi_magnitud_plan_response = p_beneficiaries_plan_responses + ['individuals_n_total_plan_2023']
pri_benefi_magnitud_plan_results = ['pri_benef_magnitud_plan_subidx','pri_benef_magnitud_plan_req']
pri_benefi_magnitud_plan_details = d_indivdls_plan_plan_all_list + companies_plan_plan_all_list + regions_plan_plan_all_list + cities_plan_plan_all_list + natsyst_plan_plan_all_list 
pri_benefi_magnitud_plan_all_list = pri_benefi_magnitud_plan_response + pri_benefi_magnitud_plan_results + pri_benefi_magnitud_plan_details





# Section 6: Governance of the Plan

info_governance = """55. Governance of the Plan (Section 6)

This section tackles two fundamental components for the effectiveness of the Resilience-Building Plan: participation and leadership. Here, strategies and guidelines are laid out to ensure that both elements are well-represented in the process of developing and implementing the plan.

56.  Participation

The involvement of members and other stakeholders is crucial for enriching and effectively executing the Resilience-Building Plan. This subsection examines how members are engaged in the development of the plan, emphasizing the importance of diverse perspectives for responsible and effective implementation.

Did you conduct an internal participatory process to develop the Resilience-Building Plan? Please specify if a formal mechanism was used to include the input of members in shaping the plan. For example, workshops or brainstorming sessions conducted.
Yes
No
How is the participation of your members in the development of the Resilience-Building Plan structured? Clarify the extent of member involvement. Options may include: members lead the plan's formulation, members collaborate in its development, or the initiative is solely the responsibility of the leadership with no member involvement.
The members implement the entire plan.
The initiative collaborates with the members to develop the plan.
The members do not participate, and the initiative is solely responsible for developing the plan.
How many members are actively involved in the Resilience-Building Plan? Please provide an estimate or exact number. This information helps in understanding the scale and inclusivity of the participatory process.

57. Leadership

Effective leadership is essential for navigating the inherent challenges in implementing the Resilience-Building Plan. This subsection focuses on the importance of clear and effective leadership in coordinating a wide range of stakeholders, maintaining a balance between inclusivity and operational efficiency to achieve the plan's objectives.

Is there a designated supervisor or team responsible for the implementation of this Resilience-Building Plan?
Yes, there is a designated supervisor.
No, there is a designated team or committee.
There is neither a designated supervisor nor team.
Other (Please specify)
Please specify the name or title of the individual, team, or department responsible for the implementation of the Resilience-Building Plan. Additionally, provide their contact information for further communication.

Within your Resilience-Building Plan, how do you plan to demonstrate leadership and actively involve diverse stakeholders? 
"""

# st.write("## Section 6: Governance of the Plan")
# st.write("### Section 6.1: Participation")
rename_to_plan = {'r3146':'internal_participatory_process',
                  'r3147':'how_participation_members',
                  'r3148':'n_members_involved_original'}
df_2023_plan = df_2023_plan.rename(columns = rename_to_plan)

particip_how_plan_list = ['internal_participatory_process','how_participation_members']

## Adding number 0 when there are not members involved
# Correcting the condition to check for NaN values and "No"
condition = pd.isna(df_2023_plan['n_members_involved_original']) & (df_2023_plan['internal_participatory_process'] == "No")
# Using .loc with the condition to set 'n_members_involved_original' to 0 where the condition is True
df_2023_plan.loc[condition, 'n_members_involved_original'] = 0

recode_members_plan_dic = {
    '~60 contributors': 60,
    'the whole of the LEIA Programme which consists of around 25 members in the UK from Energy saving trust and around 20 from CLASP in USA and Kenya': 55,
    'ORRAA’s Steering Council reviewed and provided input into the development of our 2030 goals. The Steering Council is comprised of 20 members.':20,
    '135 members':135,
    'GRP has 82 partners working across our resilience initiatives.  https://www.globalresiliencepartnership.org/who-we-are/partners/':82,
}

# st.write("N Members Recoded") ## UPDATE THIS EVERYTIME. 
# st.write(df_2023_plan['n_members_involved_original'])


# Function to apply to each value
def map_or_keep(value):
    # Check if the value is in the dictionary's keys
    if value in recode_members_plan_dic:
        # Replace with dictionary value
        return recode_members_plan_dic[value]
    else:
        # Try to convert to integer, if possible. Keep as is if not.
        try:
            return int(value)
        except ValueError:
            return value

# Apply the function to the column
df_2023_plan['n_members_involved_recod'] = df_2023_plan['n_members_involved_original'].apply(map_or_keep)

particip_num_member_plan_list = ['n_members_involved_original','n_members_involved_recod']
participation_responses = particip_how_plan_list + particip_num_member_plan_list


df_2023_plan['particip_how_plan_plan_status'] = df_2023_plan[particip_how_plan_list].notna().all(axis=1)
df_2023_plan['particip_num_member_plan_status'] = df_2023_plan[particip_num_member_plan_list].notna().all(axis=1)

partic_all_plan_list =['particip_how_plan_plan_status','particip_num_member_plan_status']

## Participation Plan Sub Index
weights = {
    'particip_how_plan_plan_status':0.3,
    'particip_num_member_plan_status':0.7,
    }

# Calculate the weighted sum of the components for partic_plan_sub_subidx
df_2023_plan['partic_plan_sub_subidx'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_2023_plan['partic_plan_sub_subidx'] = (df_2023_plan['partic_plan_sub_subidx'] * 100).astype(int)

#requested "_req" info variable
index_list = partic_all_plan_list
df_2023_plan['partic_plan_sub_subidx_req'] = df_2023_plan.apply(identify_req_status, axis=1)
# df_2023_plan[['partic_plan_sub_subidx','partic_plan_sub_subidx_req']+partic_all_plan_list]

participation_plan_responses_list = participation_responses
participation_plan_result_list = ['partic_plan_sub_subidx','partic_plan_sub_subidx_req'] 
participation_plan_list_to_index = partic_all_plan_list
participation_plan_plan_all_list = participation_plan_responses_list + participation_plan_result_list + participation_plan_list_to_index
 ##
##  ##
 ##
# st.write("participation_plan_all_list",df_2023_plan[participation_plan_plan_all_list])




# st.write("### Section 6.2: Leadership")
rename_to_plan = {'r3149':'supervisor_or_team_responsible',
                  'r3150':'supervisor_or_team_responsible_other',
                  'r3152':'leadership_involve_stakeholders'
}
df_2023_plan = df_2023_plan.rename(columns = rename_to_plan)

supervisor_plan_list = ['supervisor_or_team_responsible','supervisor_or_team_responsible_other',]
leadership_how_plan_list = ['leadership_involve_stakeholders',]


df_2023_plan['supervisor_plan_status'] = df_2023_plan[supervisor_plan_list].notna().any(axis=1)
df_2023_plan['leadership_how_plan_status'] = df_2023_plan[leadership_how_plan_list].notna().all(axis=1)
leadership_how_plan_not_enough_list = ['bla']
condition = df_2023_plan[leadership_how_plan_list[0]].isin(leadership_how_plan_not_enough_list)
df_2023_plan.loc[condition, 'leadership_how_plan_status'] = False
leadeship_all_plan_list =['supervisor_plan_status','leadership_how_plan_status']

## Leadership Plan Sub Index
weights = {
    'supervisor_plan_status':0.3,
    'leadership_how_plan_status':0.7,
    }

# Calculate the weighted sum of the components for leadership_plan_sub_subidx
df_2023_plan['leadership_plan_sub_subidx'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_2023_plan['leadership_plan_sub_subidx'] = (df_2023_plan['leadership_plan_sub_subidx'] * 100).astype(int)

#requested "_req" info variable
index_list = leadeship_all_plan_list
df_2023_plan['leadership_plan_sub_subidx_req'] = df_2023_plan.apply(identify_req_status, axis=1)

leadership_plan_responses_list = supervisor_plan_list + leadership_how_plan_list
leadership_plan_result_list = ['leadership_plan_sub_subidx','leadership_plan_sub_subidx_req'] 
leadership_plan_list_to_index = leadeship_all_plan_list
leadership_plan_plan_all_list = leadership_plan_responses_list + leadership_plan_result_list + leadership_plan_list_to_index
 ##
##  ##
 ##
# st.write("leadership_plan_all_list",df_2023_plan[leadership_plan_plan_all_list])


# GOVERNANCE SUBINDEX
governance_to_index_list_plan = ['partic_plan_sub_subidx', 'leadership_plan_sub_subidx']
df_2023_plan['governance_plan_subidx'] = df_2023_plan[governance_to_index_list_plan].mean(axis=1)
df_2023_plan['governance_plan_subidx'] = df_2023_plan['governance_plan_subidx'].astype(int)
governance_summary_plan_list = ['governance_plan_subidx', 'partic_plan_sub_subidx'] + partic_all_plan_list + ['leadership_plan_sub_subidx'] + leadeship_all_plan_list 
# st.write("Governance",df_2023_plan[governance_summary_plan_list] )
df_2023_plan['governance_plan_req'] = df_2023_plan['partic_plan_sub_subidx_req'] + ';' + df_2023_plan['leadership_plan_sub_subidx_req']
df_2023_plan.loc[df_2023_plan['governance_plan_req'] == ';', 'governance_plan_req'] = ""
# st.write("Governance",df_2023_plan[['governance_plan_subidx','governance_plan_req']])

governance_plan_all_results = ['governance_plan_subidx','governance_plan_req']
governance_plan_all_list = participation_plan_plan_all_list + leadership_plan_plan_all_list + governance_plan_all_results




# Section 7: Barriers, Finance and Assumption
# st.write("## Section 7: Barriers and Assumption")

info_barries = """This subsection aims to identify the challenges and barriers that might obstruct the successful execution of your Resilience-Building Plan. Recognizing these potential hurdles in advance can provide valuable insights for risk mitigation strategies.

What challenges or barriers do you anticipate could affect the successful implementation of your Resilience-Building Plan?
If you have other specific challenges or barriers not listed above, please provide details and explain any strategies you're considering to address them. (This section is optional, but sharing your insights would be beneficial.)

59. Assumption (Section 7)

Identifying and monitoring assumptions is key to the success of projects like a Resilience-Building Plan. This vigilance allows for strategy adaptation when circumstances change, as could happen with an economic shock affecting a community. Constant monitoring allows for timely adjustments in the plan, which is essential for tackling unforeseen challenges and ensuring the project's long-term success.
"""


##A)  Dimension Barriers
# st.write("### Barriers")
barriers_plan_l = ['r' + str(i) for i in range(3153, 3163)]
df_2023_plan['barriers_plan_status'] = df_2023_plan[barriers_plan_l].notna().any(axis=1)
df_2023_plan['barriers_plan_concat'] = df_2023_plan[barriers_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
df_2023_plan['barriers_plan_concat'] = df_2023_plan['barriers_plan_concat'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
df_2023_plan['barriers_plan_counts'] = df_2023_plan['barriers_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
barriers_plan_responses = ['barriers_plan_concat','barriers_plan_counts']

barriers_to_index_list_plan = ['barriers_plan_status']
df_2023_plan['barriers_plan_subidx'] = df_2023_plan[barriers_to_index_list_plan].mean(axis=1)
# Scale to 100 and convert to integer
df_2023_plan['barriers_plan_subidx'] = (df_2023_plan['barriers_plan_subidx'] * 100).astype(int)
#requested "_req" info variable
index_list = barriers_to_index_list_plan
df_2023_plan['barriers_plan_req'] = df_2023_plan.apply(identify_req_status, axis=1)
# df_2023_plan[['barriers_plan_subidx','barriers_plan_req']+barriers_to_index_list_plan]

barriers_plan_responses_list = barriers_plan_responses
barriers_plan_result_list = ['barriers_plan_subidx','barriers_plan_req'] 
barriers_plan_list_to_index = barriers_to_index_list_plan
barriers_plan_plan_all_list = barriers_plan_responses_list + barriers_plan_result_list + barriers_plan_list_to_index
 ##
##  ##
 ##
# st.write("barriers_plan_all_list",df_2023_plan[barriers_plan_plan_all_list])





##B)  Dimension Finance

info_finance = """60. Financing Assumptions (Section 7)

This focuses on the financial assumptions underpinning your Resilience-Building Plan. Understanding the funding landscape is crucial for the plan's success, as it impacts its feasibility and long-term sustainability.

Have you made a budget estimate for the total cost of your Resilience-Building Plan?
Yes
No
Partial
Is funding for your Resilience-Building Plan expected to be both available from the start and consistent throughout its duration?
Secured & Continuous
Partial & Risks
Seeking & Risks
In case of funding shortages, has the plan identified alternative or backup funding sources?
Yes
No
Under Consideration
Does the Resilience-Building Plan assume that estimated intervention costs won't significantly increase?
Stable
Variable
Partial
How much money is expected to be mobilized with this Resilience-Building Plan? Specify the amount in U.S. dollars, and consider providing a range if there's uncertainty.

How much additional funding do you anticipate needing to effectively implement the Resilience-Building Plan? Specify the amount in U.S. dollars, and consider providing a range if there's uncertainty.

Please describe how your organization and its members are catalyzing private finance for adaptation.
"""


rename_to_plan = {'r3163':'finance_budget_estimate',
                  'r3164':'finance_funding_expectations',
                  'r3165':'finance_backup_source',
                  'r3166':'finance_cost_increase',
}
df_2023_plan = df_2023_plan.rename(columns = rename_to_plan)


responses_finance_general = ['finance_budget_estimate','finance_funding_expectations','finance_backup_source','finance_cost_increase']

# st.write("### Finance General Info")
# 'finance_budget_estimate_plan_status' = Have you made a budget estimate for the total cost of your Resilience-Building Plan?
# 'finance_funding_expectations_plan_status' = Is funding for your Resilience-Building Plan expected to be both available from the start and consistent throughout its duration?
# 'finance_backup_sources_plan_status' = In case of funding shortages, has the plan identified alternative or backup funding sources?
# 'finance_cost_increase_plan_status' = Does the Resilience-Building Plan assume that estimated intervention costs won't significantly increase?

df_2023_plan['finance_budget_estimate_plan_status'] = df_2023_plan['finance_budget_estimate'].notna()
df_2023_plan['finance_funding_expectations_plan_status'] = df_2023_plan['finance_funding_expectations'].notna()
df_2023_plan['finance_backup_sources_plan_status'] = df_2023_plan['finance_backup_source'].notna()
df_2023_plan['finance_cost_increase_plan_status'] = df_2023_plan['finance_cost_increase'].notna()

finance_general_plan_l = ['finance_budget_estimate_plan_status',
                          'finance_funding_expectations_plan_status',
                          'finance_backup_sources_plan_status',
                          'finance_cost_increase_plan_status',]

## finance_general_info_status
weights = {
    'finance_budget_estimate_plan_status':0.6,
    'finance_funding_expectations_plan_status':0.2,
    'finance_backup_sources_plan_status':0.1,
    'finance_cost_increase_plan_status':0.1,
    }

# Calculate the weighted sum of the components for finance_general_info_status
df_2023_plan['finance_general_info_sub_subidx'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_2023_plan['finance_general_info_sub_subidx'] = (df_2023_plan['finance_general_info_sub_subidx'] * 100).astype(int)

#required "_req" info variable
index_list = finance_general_plan_l
df_2023_plan['finance_general_info_req'] = df_2023_plan.apply(identify_req_status, axis=1)
# df_2023_plan[['finance_general_info_status','finance_general_info_req']+finance_general_plan_l]

finance_general_info_plan_responses_list = responses_finance_general
finance_general_info_plan_result_list = ['finance_general_info_sub_subidx','finance_general_info_req'] 
finance_general_info_plan_list_to_index = finance_general_plan_l
finance_general_info_plan_plan_all_list = finance_general_info_plan_responses_list + finance_general_info_plan_result_list + finance_general_info_plan_list_to_index
 ##
##  ##
 ##
# st.write("finance_general_info_plan_all_list",df_2023_plan[finance_general_info_plan_plan_all_list])



# st.write("### Finance Amount Movilized ")
rename_to_plan = {'r3167':'money_expected_mobilized',
                  'r3168':'additional_funding_anticipate',
}
df_2023_plan = df_2023_plan.rename(columns = rename_to_plan)


finance_amount_mov_responses = ['money_expected_mobilized','additional_funding_anticipate']
# 'money_expected_mobilized' = How much money is expected to be mobilized with this Resilience-Building Plan?Specify the amount in U.S. dollars.
# 'additional_funding_anticipate' = How much additional funding do you anticipate needing to effectively implement the Resilience-Building Plan? Specify the amount in U.S. dollars

# Ensure the column is in a numeric format and coerce errors to NaN
df_2023_plan['money_expected_mobilized'] = pd.to_numeric(df_2023_plan['money_expected_mobilized'], errors='coerce')
df_2023_plan['additional_funding_anticipate'] = pd.to_numeric(df_2023_plan['additional_funding_anticipate'], errors='coerce')

# Replace 0 with np.nan
df_2023_plan['money_expected_mobilized'] = df_2023_plan['money_expected_mobilized'].replace(0, np.nan)
df_2023_plan['additional_funding_anticipate'] = df_2023_plan['additional_funding_anticipate'].replace(0, np.nan)

df_2023_plan['finance_funding_expected_plan_status'] = df_2023_plan['money_expected_mobilized'].notna()
df_2023_plan['finance_additional_funding_plan_status'] = df_2023_plan['additional_funding_anticipate'].notna()


## finance_amount_plan_sub_subidx
finance_amount_plan_sub_subidx_list = ['finance_funding_expected_plan_status','finance_additional_funding_plan_status']

weights = {
    'finance_funding_expected_plan_status':0.9,
    'finance_additional_funding_plan_status':0.1,
    }

# Calculate the weighted sum of the components for finance_amount_plan_sub_subidx
df_2023_plan['finance_amount_plan_sub_subidx'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_2023_plan['finance_amount_plan_sub_subidx'] = (df_2023_plan['finance_amount_plan_sub_subidx'] * 100).astype(int)

#required "_req" info variable
index_list = finance_amount_plan_sub_subidx_list
df_2023_plan['finance_amount_plan_req'] = df_2023_plan.apply(identify_req_status, axis=1)
# df_2023_plan[['finance_amount_plan_sub_subidx','finance_amount_plan_req']+finance_amount_plan_sub_subidx_list]


finance_amount_plan_responses_list = finance_amount_mov_responses
finance_amount_plan_result_list = ['finance_amount_plan_sub_subidx','finance_amount_plan_req'] 
finance_amount_plan_list_to_index = finance_amount_plan_sub_subidx_list
finance_amount_plan_plan_all_list = finance_amount_plan_responses_list + finance_amount_plan_result_list + finance_amount_plan_list_to_index
 ##
##  ##
 ##
# st.write("finance_amount_plan_all_list PLAN",df_2023_plan[['InitName']+finance_amount_plan_plan_all_list])


# st.write("### How Finance is Movilized ")
#Please describe how your organization and its members are catalyzing private finance for adaptation.

rename_to_plan = {'r3169':'finance_how',
}
df_2023_plan = df_2023_plan.rename(columns = rename_to_plan)

finance_how_list = ['finance_how',]
df_2023_plan['finance_how_plan_status'] = df_2023_plan[finance_how_list].notna().all(axis=1)
finance_how_not_enough_list = ['bla','--']
condition = df_2023_plan[finance_how_list[0]].isin(finance_how_not_enough_list)
df_2023_plan.loc[condition, 'finance_how_plan_status'] = False

## finance_how_movilized_subidx
finance_how_movilized_subidx_list = ['finance_how_plan_status']
weights = {
    'finance_how_plan_status':1,
    }

# Calculate the weighted sum of the components for finance_how_movilized_subidx
df_2023_plan['finance_how_plan_sub_subidx'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)
# Scale to 100 and convert to integer
df_2023_plan['finance_how_plan_sub_subidx'] = (df_2023_plan['finance_how_plan_sub_subidx'] * 100).astype(int)
# df_2023_plan[['finance_how_movilized_subidx','r3169']] 

#required "_req" info variable
index_list = finance_how_movilized_subidx_list
df_2023_plan['finance_how_movilized_req'] = df_2023_plan.apply(identify_req_status, axis=1)
# df_2023_plan[['finance_how_movilized_subidx','finance_how_movilized_req']+finance_how_movilized_subidx_list]


finance_how_plan_responses_list = finance_how_list
finance_how_plan_result_list = ['finance_how_plan_sub_subidx','finance_how_movilized_req'] 
finance_how_plan_list_to_index = finance_how_movilized_subidx_list
finance_how_plan_plan_all_list = finance_how_plan_responses_list + finance_how_plan_result_list + finance_how_plan_list_to_index
 ##
##  ##
 ##
# st.write("finance_how_plan_all_list",df_2023_plan[finance_how_plan_plan_all_list])


#### Making finance_plan_subidx
finance_plan_subidx_list = ['finance_general_info_sub_subidx','finance_amount_plan_sub_subidx','finance_how_plan_sub_subidx']

## finance_plan_subidx
weights = {
    'finance_general_info_sub_subidx':0.1,
    'finance_amount_plan_sub_subidx':0.8,
    'finance_how_plan_sub_subidx':0.1,
    }

# Calculate the weighted sum of the components for finance_plan_subidx
df_2023_plan['finance_plan_subidx'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)

finance_plan_subidx_req_list = ['finance_general_info_req','finance_amount_plan_req','finance_how_movilized_req']

def concatenate_req_values(row):
    pending_values = []
    # Check condition and concatenate the appropriate pending value
    if row['finance_general_info_sub_subidx'] <= 90:
        pending_values.append(row['finance_general_info_req'])
    if row['finance_amount_plan_sub_subidx'] <= 90:
        pending_values.append(row['finance_amount_plan_req'])
    if row['finance_how_plan_sub_subidx'] <= 90:
        pending_values.append(row['finance_how_movilized_req'])
    
    # Join the collected pending values with a separator, e.g., ", "
    return ', '.join(filter(None, pending_values))  # filter(None, ...) removes empty strings

# finance_plan_subidx_req_list = ['finance_general_info_req', 'finance_amount_plan_sub_subidx','finance_amount_plan_req', 'finance_how_movilized_req',]

# Apply the function to each row in the DataFrame to create the new column
df_2023_plan['finance_plan_req'] = df_2023_plan.apply(concatenate_req_values, axis=1)

# Display the DataFrame subset with the specified columns
# df_2023_plan[['finance_plan_subidx','finance_plan_req'] + finance_plan_subidx_req_list]

finance_plan_results_list = ['finance_plan_subidx','finance_plan_req']
finance_plan_sub_subidx_info = finance_general_info_plan_plan_all_list + finance_amount_plan_plan_all_list + finance_how_plan_plan_all_list
fianance_plan_plan_all_list = finance_plan_results_list + finance_plan_sub_subidx_info





##Monitoring and Data Collection

info_monitoring_and_data_collection = """61. Measurement Assumptions (Section 7)

This subsection focuses on the assumptions related to monitoring and measuring the progress of your Resilience-Building Plan. It's important to clarify whether the existing tools and processes are adequate for data collection and the accurate estimation of beneficiaries.

Do you have appropriate tools for monitoring and measuring progress in your Resilience-Building Plan?
Yes, we have all the necessary monitoring tools.
We have some tools but might need more or better ones.
We are still exploring the best tools for our monitoring needs.
Other (Please specify)

How would you describe the ease of data collection in measuring your plan's progress?
Data collection processes are clear and easily manageable.
We can collect data, but it requires significant effort or resources.
It's tough to gather the necessary data consistently.
Other (Please specify)

How confident are you in your ability to accurately measure the number of individuals benefiting from your initiative?
We have robust tools and processes in place to accurately count all beneficiaries.
We can estimate the number of beneficiaries, but there might be some margin of error.
It's challenging to ascertain the exact number, and we mostly rely on rough estimates.
Other (Please specify)
"""

## Extra Monitoring Tools of the Plan
# Update 'r3170', 'r3172', and 'r3174' based on corresponding other columns when they are 'Other (please specify)'
df_2023_plan['r3170'] = df_2023_plan.apply(lambda x: x['r3171'] if x['r3170'] == 'Other (please specify)' else x['r3170'], axis=1)
df_2023_plan['r3172'] = df_2023_plan.apply(lambda x: x['r3173'] if x['r3172'] == 'Other (please specify)' else x['r3172'], axis=1)
df_2023_plan['r3174'] = df_2023_plan.apply(lambda x: x['r3175'] if x['r3174'] == 'Other (please specify)' else x['r3174'], axis=1)

rename_to_plan = {'r3170':'measuring_progress_availability_yes_no',
                  'r3172':'measuring_progress_how',
                  'r3174':'measuring_progress_confidence'}
df_2023_plan = df_2023_plan.rename(columns = rename_to_plan)

# Display the columns of interest
# df_2023_plan[['measuring_progress_availability_yes_no','measuring_progress_how','measuring_progress_confidence']]





# st.write("### Monitoring")
monitoring_plan_l = ['measuring_progress_availability_yes_no']
df_2023_plan['monitoring_plan_status'] = df_2023_plan[monitoring_plan_l].notna().any(axis=1)
# df_2023_plan['monitoring_plan_concat'] = df_2023_plan[monitoring_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
# df_2023_plan['monitoring_plan_concat'] = df_2023_plan['monitoring_plan_concat'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
# # df_2023_plan['monitoring_plan_counts'] = df_2023_plan['monitoring_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
# monitoring_plan_responses = ['monitoring_plan_concat','monitoring_plan_counts']
monitoring_plan_responses = ['measuring_progress_availability_yes_no']


# st.write("### Data Collection")
data_collect_plan_l = ['measuring_progress_how']
df_2023_plan['data_collect_plan_status'] = df_2023_plan[data_collect_plan_l].notna().any(axis=1)
# df_2023_plan['data_collect_plan_concat'] = df_2023_plan[data_collect_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
# df_2023_plan['data_collect_plan_concat'] = df_2023_plan['data_collect_plan_concat'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
# # df_2023_plan['data_collect_plan_counts'] = df_2023_plan['data_collect_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
# data_collect_plan_responses = ['data_collect_plan_concat','data_collect_plan_counts']
data_collect_plan_responses = ['measuring_progress_how',]


# st.write("### Confident about data")
confident_plan_l = ['measuring_progress_confidence']
df_2023_plan['confident_plan_status'] = df_2023_plan[confident_plan_l].notna().any(axis=1)
# df_2023_plan['confident_plan_concat'] = df_2023_plan[confident_plan_l].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
# df_2023_plan['confident_plan_concat'] = df_2023_plan['confident_plan_concat'].apply(lambda x: '; '.join(filter(None, [i.strip() for i in x.split(';')])))
# # df_2023_plan['confident_plan_counts'] = df_2023_plan['confident_plan_concat'].str.split(';').apply(lambda x: len([country for country in x if country.strip()]))
# confident_plan_responses = ['confident_plan_concat','confident_plan_counts']
confident_plan_responses = ['measuring_progress_confidence',]

# making monitoring_data_collect_plan_subidx
monitoring_data_collect_plan_subidx_list = ['monitoring_plan_status','data_collect_plan_status','confident_plan_status']

# df_2023_plan[monitoring_data_collect_plan_subidx_list]

weights = {
    'monitoring_plan_status':0.3,
    'data_collect_plan_status':0.3,
    'confident_plan_status':0.4,
    }

# Calculate the weighted sum of the components for monitoring_data_collect_plan_subidx
df_2023_plan['monitoring_data_collect_plan_subidx'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)

# Scale to 100 and convert to integer
df_2023_plan['monitoring_data_collect_plan_subidx'] = (df_2023_plan['monitoring_data_collect_plan_subidx'] * 100).astype(int)
# df_2023_plan[['monitoring_data_collect_plan_subidx']+monitoring_data_collect_plan_subidx_list] 

#required "_req" info variable
index_list = monitoring_data_collect_plan_subidx_list
df_2023_plan['monitoring_data_collect_plan_req'] = df_2023_plan.apply(identify_req_status, axis=1)
# df_2023_plan[['monitoring_data_collect_plan_subidx','monitoring_data_collect_plan_req']+monitoring_data_collect_plan_subidx_list]


monitoring_data_collect_plan_responses_list = monitoring_plan_responses + data_collect_plan_responses + confident_plan_responses
monitoring_data_collect_plan_result_list = ['monitoring_data_collect_plan_subidx','monitoring_data_collect_plan_req'] 
monitoring_data_collect_plan_list_to_index = monitoring_data_collect_plan_subidx_list
monitoring_data_collect_plan_plan_all_list = monitoring_data_collect_plan_responses_list + monitoring_data_collect_plan_result_list + monitoring_data_collect_plan_list_to_index
 ##
##  ##
 ##
# st.write("monitoring_data_collect_plan_all_list",df_2023_plan[monitoring_data_collect_plan_plan_all_list])


all_plan_dimensions_list = plan_identif_plan_all_list + description_plan_plan_all_list + saa_plan_plan_all_list + ra_plan_plan_all_list + pri_benefi_magnitud_plan_all_list + governance_plan_all_list + barriers_plan_plan_all_list + fianance_plan_plan_all_list + monitoring_data_collect_plan_plan_all_list + countries_plan_responses_list 

subidx_plan_all_to_final_idx = ['plan_identif_subidx','description_plan_subidx','saa_plan_subidx','ra_plan_subidx',
                                'pri_benef_magnitud_plan_subidx','governance_plan_subidx','barriers_plan_subidx',
                                'finance_plan_subidx','monitoring_data_collect_plan_subidx']






#### Plan Completeness Index plan_completeness_idx
weights = {
'plan_identif_subidx':0.033333333,
'description_plan_subidx':0.033333333,
'saa_plan_subidx':0.222222222,
'ra_plan_subidx':0.222222222,
'pri_benef_magnitud_plan_subidx':0.222222222,
'governance_plan_subidx':0.022222222,
'barriers_plan_subidx':0.022222222,
'finance_plan_subidx':0.166666667,
'monitoring_data_collect_plan_subidx':0.055555556
}

# Calculate the weighted sum of the components for plan_completeness_idx
df_2023_plan['plan_completeness_idx'] = df_2023_plan.apply(
    lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
    axis=1
)


# df_2023_plan[['InitName','plan_completeness_idx']]


# finance_plan_subidx_list = ['finance_general_info_sub_subidx','finance_amount_plan_sub_subidx','finance_how_plan_sub_subidx']

# ## finance_plan_subidx
# weights = {
#     'finance_general_info_sub_subidx':0.1,
#     'finance_amount_plan_sub_subidx':0.8,
#     'finance_how_plan_sub_subidx':0.1,
#     }

# # Calculate the weighted sum of the components for finance_plan_subidx
# df_2023_plan['finance_plan_subidx'] = df_2023_plan.apply(
#     lambda row: sum(row[col] * weight for col, weight in weights.items() if col in row),
#     axis=1
# )

# st.write('###IMPORTANT PLAN')
# df_2023_plan[['InitName','plan_completeness_idx']+subidx_plan_all_to_final_idx]



#### Plan Completeness Status order by Proirity plan_completeness_status and plan_completeness_req_priority
df_2023_plan['plan_completeness_status'] = np.where(df_2023_plan['plan_completeness_idx'] > 90, "Accepted", "Awaiting Completion")

required_plan_list_prioritized = [
                      'saa_plan_req',
                      'ra_plan_req',
                      'pri_benef_magnitud_plan_req',
                      'finance_plan_req',
                      'monitoring_data_collect_plan_req',
                      'plan_identif_req',
                      'description_plan_req',
                      'governance_plan_req',
                      'barriers_plan_req',
                      ]

df_2023_plan['plan_completeness_req_priority'] = df_2023_plan.apply(lambda row: ', '.join(filter(None, [row[col] for col in required_plan_list_prioritized])), axis=1)

## Renaming Values 

required_plan_list_recode = ['plan_completeness_req_priority','plan_identif_req',
                      'description_plan_req',
                      'saa_plan_req',
                      'ra_plan_req',
                      'pri_benef_magnitud_plan_req',
                      'governance_plan_req',
                      'barriers_plan_req',
                      'finance_plan_req',
                      'monitoring_data_collect_plan_req']

# Apply the replacement operation to each specified column
for col in required_plan_list_recode:
    df_2023_plan[col] = df_2023_plan[col].astype(str).apply(lambda x: x.replace('_plan_status', ''))
    
for col in required_plan_list_recode:
    df_2023_plan[col] = df_2023_plan[col].astype(str).apply(lambda x: x.replace('_status', ''))
    
for col in required_plan_list_recode:
    df_2023_plan[col] = df_2023_plan[col].astype(str).apply(lambda x: x.replace('_subidx', '_info'))

# for col in required_plan_list_recode:
#     df_2023_plan[col] = df_2023_plan[col].astype(str).apply(lambda x: x.replace('finance_', ''))
    
for col in required_plan_list_recode:
    df_2023_plan[col] = df_2023_plan[col].astype(str).apply(lambda x: x.replace(', ;', ';'))



## Renaming Codes to Real Questions
real_questions_plan_dict = {
    "action_clusters":"Indentification of Action Clusters: 'Please select a Resilience Action Cluster or group of Resiliencia Action Clusters that align with your Resilience-Building Plan.'",
    "cities_n_cities":"Number of Cities: 'How many cities are targeted to become more resilient as a result of your Resilience-Building Plan?'",
    "cities_n_individuals":"Number of Individuals Through Cities: 'Taking into consideration the specific individuals you've previously identified in this section, what is the estimated number of individual beneficiaries who are expected to become more resilient through the enhanced resilience of these cities, as per your Resilience-Building Plan? '",
    "cities_primary_beneficiaries":"Cities Primary Beneficiaries: 'Who are the primary beneficiaries in the cities that your Resilience-Building Plan aims to make more resilient? Select all that apply '",
    "cities_types_of_individuals":"Cities Types of Individuals: 'What types of communities and groups of individuals within these cities are expected to benefit from the resilience measures laid out in your Resilience-Building Plan? Select all that apply '",
    "d_indivdls_num_d_indivdls":"Number of Direct Individuals: 'How many direct individuals are expected to become more resilient as a result of your Resilience-Building Plan? '",
    "finance_additional_funding":"Finance Additional Funding: 'How much additional funding do you anticipate needing to effectively implement the Resilience-Building Plan? Specify the amount in U.S. dollars'",
    "finance_backup_sources":"Funding Backup Sources: 'In case of funding shortages, has the plan identified alternative or backup funding sources?'",
    "finance_budget_estimate":"Finance Budget Estimate: 'Have you made a budget estimate for the total cost of your Resilience-Building Plan?'",
    "finance_cost_increase":"Finance Cost Increase: 'Does the Resilience-Building Plan assume that estimated intervention costs won't significantly increase?'",
    "finance_funding_expectations":"Availability of Funding Expectations: 'Is funding for your Resilience-Building Plan expected to be both available from the start and consistent throughout its duration?'",
    "finance_funding_expected":"Funding Expected: 'How much money is expected to be mobilized with this Resilience-Building Plan?Specify the amount in U.S. dollars.'",
    "finance_how":"Finance How : 'Please describe how your organization and its members are catalyzing private finance for adaptation.'",
    "foodandagriculture_sub_info":"SAA Food and Agriculture System Questions",
    "insfraestructure_sub_info":"SAA Infrastructure System Questions",
    "leadership_how":"Leadership Stakeholders: 'Within your Resilience-Building Plan, how do you plan to demonstrate leadership and actively involve diverse stakeholders? '",
    "natsyst_n_hectares":"Natural Systems Number of Hectares: 'Considering the types of natural systems that your Resilience-Building Plan aims to make more resilient, please indicate the estimated number of hectares your plan aims to benefit.'",
    "natsyst_n_individuals":"Natural Systems Number of Individuals: 'Taking into consideration the specific individuals you've previously identified in this section, what is the estimated number of individual beneficiaries who are expected to become more resilient through the enhanced resilience of these natural systems, as per your Resilience-Building Plan? '",
    "natsyst_types_of_individuals":"Natural Systems Types of Individuals: 'What kind of groups of individuals related to these Natural Systems are expected to benefit from the resilience measures laid out in your Resilience-Building Plan? Select all that apply.'",
    "particip_num_member":"Member's Participation: 'How many members are actively involved in the Resilience-Building Plan? Please provide an estimate or exact number. This information helps in understanding the scale and inclusivity of the participatory process.'",
    "plan_description":"Plan Description: 'Could you please describe the Resilience-Building Plan you are reporting on, in general terms? When describing your Resilience-Building Plan in general terms, aim to provide an overview that offers context for your chosen Action Cluster(s) and gives a sna'",
    "plan_probl_statement":"Problem Statement. Contextualizing the hazard and vulnerable groups. Considering the hazard(s) you've identified and the vulnerable groups you aim to support, please provide a concise narrative describing the specific climate-related risk or problem you're targeting.",
    "planing_cross_sub_info":"SAA Planning Cross Cutting Enabler Questions",
    "planing_cross_sub_info":"SAA Planning Cross Cutting  Questions",
    "priority_groups":"Priority Groups: 'To what extent is the impact of your Resilience-Building Plan specifically directed towards each of the following priority groups?'",
    "ra_intentionality":"RA Intentionality: 'Intentionality is used to gauge how central resilience attribute subcategories are within the Resilience-Building Plan. Please, classify the level of intentionality for each resilience sub-category in the plan, providing insight into the plan's focus on specific resilience dimensions.'",
    "ra_narrative":"Provide a description of your resilience attributes in the following dimensions: Tangible, Inclusive & Sustainable",
    "regions_n_regions":"Number of Regions: 'How many regions are targeted to become more resilient as a result of your Resilience-Building Plan? '",
    "regions_primary_beneficiaries":"Regions Primary Beneficiaries: 'Who are the primary beneficiaries in the regions that your Resilience-Building Plan aims to make more resilient? Select all that apply'",
    "regions_types_of_individuals":"Regions Type of Individuals:'Who are the primary beneficiaries in the regions that your Resilience-Building Plan aims to make more resilient? Select all that apply'",
    "responder_info":"Responder: 'Survey Responder's Full Name and/or Email'",
    "supervisor":"Supervisor of the Plan: 'Is there a designated supervisor or team responsible for the implementation of this Resilience-Building Plan?'",
    "waterandnatural_sub_info":"SAA Water and Natural Systems Questions",
    "barriers":"Barriers: 'What challenges or barriers do you anticipate could affect the successful implementation of your Resilience-Building Plan?'",
    "confident":"Confidence of Data: 'How confident are you in your ability to accurately measure the number of individuals benefiting from your initiative?'",
    "data_collect":"Data Collection: 'How would you describe the ease of data collection in measuring your plan's progress?'",
    "monitoring":"Monitoring: 'Do you have appropriate tools for monitoring and measuring progress in your Resilience-Building Plan?'",
    "particip_how_plan":"Internal Participatory Process: 'Did you conduct an internal participatory process to develop the Resilience-Building Plan? Please specify if a formal mechanism was used to include the input of members in shaping the plan. For example, workshops or brainstorming sessions conducted. (HOW)'",
    }

def replace_values_in_string(s):
    # Splitting the string on both semicolons and commas, and stripping spaces
    parts = [x.strip() for x in re.split(';|,', s)]
    replaced_parts = []
    
    for part in parts:
        # Convert part to lowercase for case-insensitive matching
        lower_part = part.lower()
        # Attempt to find a match in the dictionary keys, converted to lowercase
        match = next((real_questions_plan_dict[key] for key in real_questions_plan_dict if key.lower() == lower_part), None)
        # If a match is found, use it; otherwise, keep the original part
        if match:
            replaced_parts.append(match)
        else:
            replaced_parts.append(part)
    
    # Joining the parts back into a string, separated by "; "
    return "; ".join(replaced_parts)

# Apply the function to each row of the 'plan_completeness_req_priority' column
df_2023_plan['plan_completeness_req_priority_recoded'] = df_2023_plan['plan_completeness_req_priority'].apply(replace_values_in_string)


plan_completness_list = ['plan_completeness_idx','plan_completeness_status','plan_completeness_req_priority','plan_completeness_req_priority_recoded']




## PLAN CONFIDENCE INDEX
# 'measuring_progress_availability_yes_no',
# Do you have appropriate tools for monitoring and measuring progress in your Resilience-Building Plan?
# Yes, we have all the necessary monitoring tools.
# We have some tools but might need more or better ones.
# We are still exploring the best tools for our monitoring needs.
# Other (Please specify)

# 'measuring_progress_how',
# How would you describe the ease of data collection in measuring your plan's progress?
# Data collection processes are clear and easily manageable.
# We can collect data, but it requires significant effort or resources.
# It's tough to gather the necessary data consistently.
# Other (Please specify)

# 'measuring_progress_confidence',
# How confident are you in your ability to accurately measure the number of individuals benefiting from your initiative?
# We have robust tools and processes in place to accurately count all beneficiaries.
# We can estimate the number of beneficiaries, but there might be some margin of error.
# It's challenging to ascertain the exact number, and we mostly rely on rough estimates.
# Other (Please specify)

#Governance
df_2023_plan['confidence_governance_internal_participatory'] = np.where(df_2023_plan['internal_participatory_process'] != "Yes", 
                                                        "Plan Needs Validation By Internal Participatory Process", 
                                                        "Accepted")


df_2023_plan['confidence_governance_designated_resposible'] = np.where(df_2023_plan['supervisor_or_team_responsible'] == "Yes, there is a designated supervisor.", 
                                                        "Accepted", 
                                                        "Plan Needs a designated supervisor or team responsible for its implementation")


# df_2023_plan[['supervisor_or_team_responsible','confidence_governance_designated_resposible']]



#Monitor Assumptions
def check_conditions(row):
    # Define the conditions
    Condition1 = row['measuring_progress_availability_yes_no'] == "Yes, we have all the necessary monitoring tools."
    Condition2 = row['measuring_progress_how'] == "Data collection processes are clear and easily manageable."
    Condition3 = row['measuring_progress_confidence'] == "We have robust tools and processes in place to accurately count all beneficiaries."
    
    # Check if all conditions are met
    if Condition1 and Condition2 and Condition3:
        return "Accepted"
    else:
        return "Need to enhance monitoring tools for accurate beneficiary counts."

# Apply the function to each row
df_2023_plan['confidence_measurement_assumption'] = df_2023_plan.apply(check_conditions, axis=1)


### plan_confidence_status
confidence_plan_list_status = ['confidence_governance_internal_participatory','confidence_governance_designated_resposible','confidence_measurement_assumption']

# Count "Accepted" values for each row across specified columns and assign to a new column
df_2023_plan['plan_confidence_idx'] = df_2023_plan.apply(lambda row: sum(1 for col in confidence_plan_list_status if row[col] == "Accepted"), axis=1) 
df_2023_plan['plan_confidence_status_full'] = "Internal Participatory Decision Making: " +df_2023_plan['confidence_governance_internal_participatory']+"; Governance: "+df_2023_plan['confidence_governance_designated_resposible']+"; Measurement Tools: "+df_2023_plan["confidence_measurement_assumption"]

df_2023_plan.loc[df_2023_plan['plan_confidence_idx'] == 0, 'plan_confidence_status_full'] = "No Information to Measure Confidence Index"

# df_2023_plan[['InitName','plan_confidence_idx',]+confidence_plan_list_status+ ['plan_confidence_status_full']] 



# Define conditions
conditions = [
    df_2023_plan['plan_confidence_idx'] == 3,
    df_2023_plan['plan_confidence_idx'] == 2,
    df_2023_plan['plan_confidence_idx'] == 1,
    df_2023_plan['plan_confidence_idx'] == 0,
]
# Define the corresponding categories for each condition
choices = ["High", "Medium","Medium-Low", "Low"]

# Apply the conditions and choices to the dataframe
df_2023_plan['plan_confidence_status'] = np.select(conditions, choices, default="Unknown")


# Define the mapping for recoding
recode_mapping = {
    3: 3 / 3,
    2: 2 / 3,
    1: 1 / 3,
    0: 0 / 3
}

# Apply the recoding using the mapping
df_2023_plan['plan_confidence_idx'] = df_2023_plan['plan_confidence_idx'].map(recode_mapping)


df_2023_plan['plan_overall_status'] = "Plan Name: "+df_2023_plan['plan_name'] + ": Completeness " + df_2023_plan['plan_completeness_status'] + " & Confidence " + df_2023_plan['plan_confidence_status'] + " (" +df_2023_plan['plan_confidence_status_full'] + ")."

# df_2023_plan[['InitName','plan_confidence_idx','plan_confidence_status_full','plan_overall_status']]


##IMPORTANT DROPNA EN LUGAR EXTRAÑO
df_2023_plan = df_2023_plan.dropna(subset=['InitName'])

mask = df_2023_plan['plan_overall_status'].str.contains('Awaiting Completion')
df_2023_plan.loc[mask, 'plan_action_required'] = 'Please complete the pending questions for the resilience building plan submission and ensure its reliability'

mask = df_2023_plan['plan_overall_status'].str.contains('Accepted')
df_2023_plan.loc[mask, 'plan_action_required'] = 'Please check for reliability and consider improvements if possible.'
df_2023_plan['plan_action_required'] = df_2023_plan['plan_action_required'].fillna("Please review the validation of the resilience-building plan sumbission with members to increase reliability.")

confidence_plan_list = ['plan_confidence_idx','plan_confidence_status','confidence_governance_internal_participatory','confidence_governance_designated_resposible','confidence_measurement_assumption']
plan_over_all_status = ['plan_action_required','plan_overall_status',]

plan_index_overall_variables = {
    'plan_identif_subidx': [plan_identif_list_to_index],
    'description_plan_subidx':[description_problem_list_to_index],
    'saa_plan_subidx':[saa_plan_to_index],
    'ra_plan_subidx':[ra_list_to_index],
    'pri_benef_magnitud_plan_subidx':[indexes_beneficiaries_list_plan],
    'governance_plan_subidx':[governance_to_index_list_plan],
    'barriers_plan_subidx':[barriers_to_index_list_plan],
    'finance_plan_subidx':[finance_plan_subidx_list],
    'monitoring_data_collect_plan_subidx':[monitoring_data_collect_plan_subidx_list],
}

plan_index_list = ['plan_identif_subidx',
    'description_plan_subidx',
    'saa_plan_subidx',
    'ra_plan_subidx',
    'pri_benef_magnitud_plan_subidx',
    'governance_plan_subidx',
    'barriers_plan_subidx',
    'finance_plan_subidx',
    'monitoring_data_collect_plan_subidx']


#FINAL PLAN DATA SET plan_completeness_idx
#Filtering Data Set for all Plan > 10 as result of index
df_2023_plan = df_2023_plan[df_2023_plan['plan_completeness_idx'] > 5]




## Parche Cities Race to Resilience (CitiesR2R)


df_2023_plan.loc[df_2023_plan['InitName'] == 'Cities Race to Resilience (CitiesR2R)', 'enddate_plan'] = '2024-03-13 12:32:31'

## End Parche Cities Race to Resilience (CitiesR2R)







# st.write("# Final Data Set Plans")
# df_2023_plan[['InitName','Org_Type','plan_name','enddate_plan'] + plan_over_all_status + plan_completness_list + confidence_plan_list + all_plan_dimensions_list]

df_2023_plan_summary = df_2023_plan[['InitName','Org_Type','plan_name','PlanYear','enddate_plan'] + plan_over_all_status + plan_completness_list + confidence_plan_list + all_plan_dimensions_list]
# st.write(df_2023_plan.columns)
# st.write(df_2023_plan_summary)

# st.write('Plan2023  summary')
# df_2023_plan_summary
# st.write(df_2023_plan_summary)
# st.markdown("Numbers Partner Reporting Plan")
# st.write(df_2023_plan_summary['InitName'].nunique())
# st.markdown("Numbers of Plan Reported")
# st.write(df_2023_plan_summary['survey_reviewed_plan'].sum())
# st.markdown("Numbers Plan per Partner")
# st.write(df_2023_plan_summary['InitName'].value_counts())


def unique_concatenated_values_and_count(series):
    # Ensure all values are strings before splitting
    all_values = series.astype(str).str.split(";").explode()
    # Remove any potential 'nan' values after conversion
    all_values = all_values[all_values != 'nan']
    # Get unique values
    unique_values = all_values.unique()
    # Return unique values joined by ";" and the count of unique values
    return ";".join(unique_values), len(unique_values)


# {'r3170':'measuring_progress_availability_yes_no',
#                   'r3172':'measuring_progress_how',
#                   'r3174':'measuring_progress_confidence'}



# Apply custom aggregation and split the results into two new columns
grouped = df_2023_plan_summary.groupby('InitName').agg(
    Org_Type=('Org_Type', lambda x: unique_concatenated_values_and_count(x)[0]), 
    all_plans_name=('plan_name', lambda x: unique_concatenated_values_and_count(x)[0]),
    number_of_plans=('plan_name', lambda x: unique_concatenated_values_and_count(x)[1]),  
    enddate_all_plans=('enddate_plan', lambda x: unique_concatenated_values_and_count(x)[0]), 
    all_plans_action_required=('plan_action_required', lambda x: unique_concatenated_values_and_count(x)[0]), 
    all_plans_completeness_idx_mean=('plan_completeness_idx','mean'),
    all_plan_overall_status =('plan_overall_status', lambda x: unique_concatenated_values_and_count(x)[0]), 
    all_plans_completeness_req_priority=('plan_completeness_req_priority', lambda x: unique_concatenated_values_and_count(x)[0]), 
    all_plans_completeness_req_priority_recoded=('plan_completeness_req_priority_recoded', lambda x: unique_concatenated_values_and_count(x)[0]), 
    all_plans_confidence_idx_mean=('plan_confidence_idx','mean'),
    # all_plans_confidence_status_full=('plan_confidence_status_full', lambda x: unique_concatenated_values_and_count(x)[0]), 
    all_plans_short_name=('plan_short_name', lambda x: unique_concatenated_values_and_count(x)[0]), 
    responder_info_all_plans_concat=('responder_info_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    responder_email_all_plans=('responder_email_plan', lambda x: unique_concatenated_values_and_count(x)[0]), 
    action_clusters_all_plans_concat=('action_clusters_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    action_clusters_all_plans_counts=('action_clusters_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]), 
    all_plans_identif_subidx_mean=('plan_identif_subidx','mean'),
    all_plans_identif_req=('plan_identif_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    hazards_all_plans_concat=('hazards_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    hazards_all_plans_counts=('hazards_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]), 
    priority_groups_targeted_all_plans_concat=('priority_groups_targeted_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    priority_groups_targeted_all_plans_counts=('priority_groups_targeted_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    description_all_plans_subidx_mean=('description_plan_subidx','mean'),
    description_all_plans_req=('description_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    saa_taskforce_concat_all_plans=('saa_taskforce_concat_plan', lambda x: unique_concatenated_values_and_count(x)[0]), 
    saa_taskforce_concat_counts=('saa_taskforce_concat_plan', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    saa_all_plans_subidx_mean=('saa_plan_subidx','mean'),
    saa_all_plans_req=('saa_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    foodandagriculture_sub_subidx_mean=('foodandagriculture_sub_subidx','mean'),
    waterandnatural_sub_subidx_mean=('waterandnatural_sub_subidx','mean'),
    humansettlements_sub_subidx_mean=('humansettlements_sub_subidx','mean'),
    coastalandoceanic_sub_subidx_mean=('coastalandoceanic_sub_subidx','mean'),
    insfraestructure_sub_subidx_mean=('insfraestructure_sub_subidx','mean'),
    health_sub_subidx_mean=('health_sub_subidx','mean'),
    all_plansing_cross_sub_subidx_mean=('planing_cross_sub_subidx','mean'),
    finance_cross_sub_subidx_mean=('finance_cross_sub_subidx','mean'),
    Equity_Inclusivity_mean=('Equity_Inclusivity_mean','mean'),
    Social_Collaboration_mean=('Social_Collaboration_mean','mean'),
    Preparedness_and_all_plansning_mean=('Preparedness_and_planning_mean','mean'),
    Learning_mean=('Learning_mean','mean'),
    Agency_mean=('Agency_mean','mean'),
    Flexibility_mean=('Flexibility_mean','mean'),
    Assets_mean=('Assets_mean','mean'),
    sub_ra_central_targeted_concat=('sub_ra_central_targeted_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    sub_ra_central_targeted_counts=('sub_ra_central_targeted_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    sub_ra_targeted_but_not_central_concat=('sub_ra_targeted_but_not_central_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    sub_ra_targeted_but_not_central_counts=('sub_ra_targeted_but_not_central_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    ra_all_plans_subidx_mean=('ra_plan_subidx','mean'),
    ra_all_plans_req=('ra_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    p_beneficiaries_all_plans_concat=('p_beneficiaries_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    p_beneficiaries_all_plans_counts=('p_beneficiaries_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    individuals_n_total_all_plans_2023_sum=('individuals_n_total_plan_2023','sum'),
    pri_benef_magnitud_all_plans_subidx_mean=('pri_benef_magnitud_plan_subidx','mean'),
    pri_benef_magnitud_all_plans_req=('pri_benef_magnitud_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    d_indiv_all_plans=('d_indiv_plan',lambda x: unique_concatenated_values_and_count(x)[0]),
    d_indiv_number_all_plans_2023_sum=('d_indiv_number_plan_2023','sum'),
    d_indivdls_sub_subidx_all_plans_mean=('d_indivdls_sub_subidx_plan','mean'),
    d_indivdls_sub_subidx_all_plans_req=('d_indivdls_sub_subidx_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    companies_all_plans=('companies_plan', lambda x: unique_concatenated_values_and_count(x)[0]), 
    companies_n_comp_all_plans_2023_sum=('companies_n_comp_plan_2023','sum'),
    companies_n_indiv_plan_2023_sum=('companies_n_indiv_plan_2023','sum'),
    companies_sector_all_plans_concat=('companies_sector_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    companies_sector_all_plans_counts=('companies_sector_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    companies_sub_subidx_all_plans_mean=('companies_sub_subidx_plan','mean'),
    companies_sub_subidx_all_plans_req=('companies_sub_subidx_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    region_all_plans=('region_plan', lambda x: unique_concatenated_values_and_count(x)[0]), 
    region_n_reg_all_plans_2023_sum=('region_n_reg_plan_2023','sum'),
    region_n_indiv_plan_2023_sum=('region_n_indiv_plan_2023','sum'),
    regions_primary_beneficiaries_all_plans_concat=('regions_primary_beneficiaries_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    regions_primary_beneficiaries_all_plans_counts=('regions_primary_beneficiaries_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    region_n_indiv_all_plans_2023_sum=('region_n_indiv_plan_2023','sum'),
    regions_types_of_individuals_all_plans_concat=('regions_types_of_individuals_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    regions_types_of_individuals_all_plans_counts=('regions_types_of_individuals_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    regions_sub_subidx_all_plans_mean=('regions_sub_subidx_plan','mean'),
    regions_sub_subidx_all_plans_req=('regions_sub_subidx_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    cities_all_plans=('cities_plan', lambda x: unique_concatenated_values_and_count(x)[0]), 
    cities_n_cit_all_plans_2023_sum=('cities_n_cit_plan_2023','sum'),
    cities_n_indiv_plan_2023_sum=('cities_n_indiv_plan_2023','sum'),
    cities_primary_beneficiaries_all_plans_concat=('cities_primary_beneficiaries_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    cities_primary_beneficiaries_all_plans_counts=('cities_primary_beneficiaries_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    cities_n_indiv_all_plans_2023_sum=('cities_n_indiv_plan_2023','sum'),
    cities_type_individuals_all_plans_concat=('cities_type_individuals_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    cities_type_individuals_all_plans_counts=('cities_type_individuals_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    cities_sub_subidx_all_plans_mean_sum=('cities_sub_subidx_plan','mean'),
    cities_sub_subidx_all_plans_req=('cities_sub_subidx_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    natsyst_all_plans=('natsyst_plan', lambda x: unique_concatenated_values_and_count(x)[0]), 
    natsyst_n_hect_all_plans_2023_sum=('natsyst_n_hect_plan_2023','sum'),
    natsyst_n_indiv_plan_2023_sum=('natsyst_n_indiv_plan_2023','sum'),
    natsyst_type_natsyst_all_plans_concat=('natsyst_type_natsyst_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    natsyst_type_natsyst_all_plans_counts=('natsyst_type_natsyst_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    natsyst_n_indiv_all_plans_2023_sum=('natsyst_n_indiv_plan_2023','sum'),
    natsyst_types_of_individuals_all_plans_concat=('natsyst_types_of_individuals_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    natsyst_types_of_individuals_all_plans_counts=('natsyst_types_of_individuals_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    natsyst_sub_subidx_all_plans_mean=('natsyst_sub_subidx_plan','mean'),
    natsyst_sub_subidx_all_plans_req=('natsyst_sub_subidx_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    n_members_involved_recod_mean=('n_members_involved_recod','mean'), ## USUALLY NEED TO BE RECODED IN EVERY UPDATE
    partic_all_plans_sub_subidx_mean=('partic_plan_sub_subidx','mean'),
    partic_all_plans_sub_subidx_req=('partic_plan_sub_subidx_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    leadership_all_plans_sub_subidx_mean=('leadership_plan_sub_subidx','mean'),
    leadership_all_plans_sub_subidx_req=('leadership_plan_sub_subidx_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    barriers_all_plans_concat=('barriers_plan_concat', lambda x: unique_concatenated_values_and_count(x)[0]), 
    barriers_all_plans_counts=('barriers_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    barriers_all_plans_subidx=('barriers_plan_subidx','mean'),
    barriers_all_plans_req=('barriers_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    finance_all_plans_subidx_mean=('finance_plan_subidx','mean'),
    finance_all_plans_req=('finance_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    finance_general_info_sub_subidx_mean=('finance_general_info_sub_subidx','mean'),
    finance_general_info_req=('finance_general_info_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    money_expected_mobilized_sum=('money_expected_mobilized','sum'),
    additional_funding_anticipate_sum=('additional_funding_anticipate','sum'),
    finance_amount_all_plans_sub_subidx_mean=('finance_amount_plan_sub_subidx','mean'),
    finance_amount_all_plans_req=('finance_amount_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    finance_how_all_plans_sub_subidx_mean=('finance_how_plan_sub_subidx','mean'),
    finance_how_movilized_req=('finance_how_movilized_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    monitoring_all_plans_concat=('measuring_progress_availability_yes_no', lambda x: unique_concatenated_values_and_count(x)[0]), 
    # monitoring_all_plans_counts=('monitoring_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    data_collect_all_plans_concat=('measuring_progress_how', lambda x: unique_concatenated_values_and_count(x)[0]), 
    # data_collect_all_plans_counts=('data_collect_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    confident_all_plans_concat=('measuring_progress_confidence', lambda x: unique_concatenated_values_and_count(x)[0]), 
    # confident_all_plans_counts=('confident_plan_concat', lambda x: unique_concatenated_values_and_count(x)[1]) ,
    monitoring_data_collect_all_plans_subidx_mean=('monitoring_data_collect_plan_subidx','mean'),
    monitoring_data_collect_all_plans_req=('monitoring_data_collect_plan_req', lambda x: unique_concatenated_values_and_count(x)[0]), 
    all_countries_all_plans=('all_countries', lambda x: unique_concatenated_values_and_count(x)[0]), 
    all_countries_all_plans_counts=('all_countries', lambda x: unique_concatenated_values_and_count(x)[1]) ,

).reset_index()

# Now you have a DataFrame with the unique 'InitName', count of each 'InitName', and the average 'plan_completeness_idx'
df_2023_plan_summary_by_partner = grouped



# #Editon of action required when no plan are available
# df_2023_plan_summary_by_partner.loc[df_2023_plan_summary_by_partner['number_of_plans'] == 0, 'all_plans_action_required'] = "No information about plan. Check if plan needs to be submitted already"
# df_2023_plan_summary_by_partner[['number_of_plans','all_plans_action_required']] 
# st.write('# Plan Summary by Partner',df_2023_plan_summary_by_partner)


# df_2023_plan_summary_by_partner['all_plans_confidence_idx_mean']

#####_____________________________________________________________________________________________________
#####_____________________________________________________________________________________________________
#####_____________________________________________________________________________________________________
#####______END PLAN 2023__________________________________________________________________________________
#####_____________________________________________________________________________________________________
#####_____________________________________________________________________________________________________
#####_____________________________________________________________________________________________________









#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#_________________________________________________________________________________________________________________________________________________________________
# # GAPS ANALYSIS [new 2024]
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________

# st.write('# GAPS ANALYSIS ')

initial_variables_list = ['InitName'] #add 'Org_Type' at the end
string_pairs = [
    ('df_gi', 'priority_groups_gi_concat', 'df_2023_plan_summary_by_partner', 'priority_groups_targeted_all_plans_concat'),
    ('df_gi', 'saa_p_systems_gi_concat', 'df_2023_plan_summary_by_partner', 'saa_taskforce_concat_all_plans'),
    ('df_gi', 'action_clusters_gi_concat', 'df_2023_plan_summary_by_partner', 'action_clusters_all_plans_concat'),
    ('df_pledge', 'hazards_all_pledge_concat', 'df_2023_plan_summary_by_partner', 'hazards_all_plans_concat'),
    ('df_pledge', 'all_countries', 'df_2023_plan_summary_by_partner', 'all_countries_all_plans'),
    ('df_pledge', 'p_benefic_pledge_concat', 'df_2023_plan_summary_by_partner', 'p_beneficiaries_all_plans_concat'),
]

numeric_pairs = [
    ('df_pledge', 'amount_of_finance_anticipated_pledge', 'df_2023_plan_summary_by_partner', 'money_expected_mobilized_sum'),
    ('df_pledge', 'individuals_n_total_pledge_2023', 'df_2023_plan_summary_by_partner', 'individuals_n_total_all_plans_2023_sum'),
    ('df_pledge', 'companies_n_comp_pledge_2023', 'df_2023_plan_summary_by_partner', 'companies_n_comp_all_plans_2023_sum'),
    ('df_pledge', 'region_n_reg_pledge_2023', 'df_2023_plan_summary_by_partner', 'region_n_reg_all_plans_2023_sum'),
    ('df_pledge', 'cities_n_cit_pledge_2023', 'df_2023_plan_summary_by_partner', 'cities_n_cit_all_plans_2023_sum'),
    ('df_pledge', 'natsyst_n_hect_pledge_2023', 'df_2023_plan_summary_by_partner', 'natsyst_n_hect_all_plans_2023_sum'),
]


#This funktions are for string pairs
def calculate_gap_percentage(row, base_concat_col, comparison_concat_col):
        if pd.isna(row[base_concat_col]) or row[base_concat_col] == "" or pd.isna(row[comparison_concat_col]) or row[comparison_concat_col] == "":
            return None
        # Ensure values are treated as strings, handling NaN values appropriately
        base_values = set(str(row[base_concat_col]).split(';')) if pd.notna(row[base_concat_col]) else set()
        comparison_values = set(str(row[comparison_concat_col]).split(';')) if pd.notna(row[comparison_concat_col]) else set()
        missing_values = base_values - comparison_values
        total_unique_values = len(base_values)
        
        return (len(missing_values) / total_unique_values) * 100 if total_unique_values > 0 else None

def calculate_gap_analysis(df_base, df_comparison, base_columns, comparison_columns, merge_on, base_concat_col, comparison_concat_col, gap_count_col_name, gap_percentage_col_name, action_result_col_name, missing_values_col_name, simple_action_result_col_name, action_required_msg, no_action_required_msg, incomplete_info_msg):
    df_merged = df_base[base_columns + [base_concat_col]].merge(df_comparison[comparison_columns + [comparison_concat_col]], on=merge_on, how="left")
    
    # Adjust the lambda function to handle NaN values and ensure it operates on strings
    df_merged[gap_count_col_name] = df_merged.apply(
        lambda row: len(set(str(row[base_concat_col]).split(';')) - set(str(row[comparison_concat_col]).split(';'))) if pd.notna(row[base_concat_col]) and pd.notna(row[comparison_concat_col]) else 0, axis=1
    )
    
    df_merged[gap_percentage_col_name] = df_merged.apply(
        lambda row: calculate_gap_percentage(row, base_concat_col, comparison_concat_col), axis=1
    )

    def calculate_simple_action_result(row):
        if pd.isna(row[gap_percentage_col_name]):
            return "Not all data available"
        elif row[gap_percentage_col_name] > 0:
            return "Gap"
        else:
            return "Aligned"

    df_merged[simple_action_result_col_name] = df_merged.apply(calculate_simple_action_result, axis=1)

    def calculate_action_result(row):
        if pd.isna(row[gap_percentage_col_name]):
            return incomplete_info_msg
        elif row[gap_percentage_col_name] > 0:
            return action_required_msg
        else:
            return no_action_required_msg

    df_merged[action_result_col_name] = df_merged.apply(calculate_action_result, axis=1)

    # Adjust for missing values handling
    df_merged[missing_values_col_name] = df_merged.apply(
        lambda row: ";".join(set(str(row[base_concat_col]).split(';')) - set(str(row[comparison_concat_col]).split(';'))) if pd.notna(row[base_concat_col]) and pd.notna(row[comparison_concat_col]) else "", axis=1
    )

    return df_merged


# Results String Values

# ('df_gi', 'priority_groups_gi_concat', 'df_2023_plan_summary_by_partner', 'priority_groups_targeted_all_plans_concat'),
dimension_name = 'priority_groups'
dimension_name_formal = "Priority Groups"
base_tool_name = "General Information"
df_gap_priority_group = calculate_gap_analysis(
    df_base=df_gi, 
    df_comparison=df_2023_plan_summary_by_partner, 
    base_columns=initial_variables_list, 
    comparison_columns=initial_variables_list, 
    merge_on="InitName", 
    base_concat_col="priority_groups_gi_concat", 
    comparison_concat_col="priority_groups_targeted_all_plans_concat",
    gap_count_col_name=dimension_name + "_gap_n",
    gap_percentage_col_name=dimension_name + "_gap_%",
    action_result_col_name=dimension_name + "_gap_action_req",
    missing_values_col_name=dimension_name + "_gap_what_is_it_pending",
    simple_action_result_col_name=dimension_name + "_gap_results",
    action_required_msg="Action Required: Not all " + dimension_name_formal + " reported in " + base_tool_name + " are presented in the submitted plan(s). There is an opportunity to review the submitted plan(s) and close the gap.",
    no_action_required_msg="No Action Required.",
    incomplete_info_msg="Not all information is available to identify gaps. Please review and complete pending questions in the RtR Reporting Tools."
)
# st.write(dimension_name_formal + " Gap Analysis Table", df_gap_priority_group)


# ('df_gi', 'saa_p_systems_gi_concat', 'df_2023_plan_summary_by_partner', 'saa_taskforce_concat_all_plans'),
dimension_name = 'saa'
dimension_name_formal = "SAA Priority Systems"
base_tool_name = "General Information"
df_gap_saa = calculate_gap_analysis(
    df_base=df_gi, 
    df_comparison=df_2023_plan_summary_by_partner, 
    base_columns=initial_variables_list, 
    comparison_columns=initial_variables_list, 
    merge_on="InitName", 
    base_concat_col="saa_p_systems_gi_concat", 
    comparison_concat_col="saa_taskforce_concat_all_plans",
    gap_count_col_name= dimension_name+"_gap_n",
    gap_percentage_col_name=dimension_name+"_gap_%",
    action_result_col_name=dimension_name+"_gap_action_req",
    missing_values_col_name=dimension_name+"_gap_what_is_it_pending",
    simple_action_result_col_name=dimension_name+"_gap_results",
    action_required_msg="Action Required: Not all "+dimension_name_formal+" reported in "+base_tool_name+" are presented in the submitted plan(s). There is an opportunity to review the submitted plan(s) and close the gap.",
    no_action_required_msg="No Action Required.",
    incomplete_info_msg="Not all information is available to identify gaps. Please review and complete pending questions in the RtR Reporting Tools."
)
# st.write(dimension_name_formal+"_gap_table", df_gap_saa)




# ('df_gi', 'action_clusters_gi_concat', 'df_2023_plan_summary_by_partner', 'action_clusters_all_plans_concat')
dimension_name = 'action_clusters'
dimension_name_formal = "Action Clusters"
base_tool_name = "General Information"
df_gap_action_clusters = calculate_gap_analysis(
    df_base=df_gi, 
    df_comparison=df_2023_plan_summary_by_partner, 
    base_columns=initial_variables_list, 
    comparison_columns=initial_variables_list, 
    merge_on="InitName", 
    base_concat_col="action_clusters_gi_concat", 
    comparison_concat_col="action_clusters_all_plans_concat",
    gap_count_col_name= dimension_name+"_gap_n",
    gap_percentage_col_name=dimension_name+"_gap_%",
    action_result_col_name=dimension_name+"_gap_action_req",
    missing_values_col_name=dimension_name+"_gap_what_is_it_pending",
    simple_action_result_col_name=dimension_name+"_gap_results",
    action_required_msg="Action Required: Not all "+dimension_name_formal+" reported in "+base_tool_name+" are presented in the submitted plan(s). There is an opportunity to review the submitted plan(s) and close the gap.",
    no_action_required_msg="No Action Required.",
    incomplete_info_msg="Not all information is available to identify gaps. Please review and complete pending questions in the RtR Reporting Tools."
)
# st.write(dimension_name_formal+"_gap_table", df_gap_action_clusters)

# ('df_pledge', 'hazards_all_pledge_concat', 'df_2023_plan_summary_by_partner', 'hazards_all_plans_concat'),
dimension_name = 'hazards'
dimension_name_formal = "Hazards"
base_tool_name = "Pledge Statement"
df_gap_hazards = calculate_gap_analysis(
    df_base=df_pledge, 
    df_comparison=df_2023_plan_summary_by_partner, 
    base_columns=initial_variables_list, 
    comparison_columns=initial_variables_list, 
    merge_on="InitName", 
    base_concat_col="hazards_all_pledge_concat", 
    comparison_concat_col="hazards_all_plans_concat",
    gap_count_col_name= dimension_name+"_gap_n",
    gap_percentage_col_name=dimension_name+"_gap_%",
    action_result_col_name=dimension_name+"_gap_action_req",
    missing_values_col_name=dimension_name+"_gap_what_is_it_pending",
    simple_action_result_col_name=dimension_name+"_gap_results",
    action_required_msg="Action Required: Not all "+dimension_name_formal+" reported in "+base_tool_name+" are presented in the submitted plan(s). There is an opportunity to review the submitted plan(s) and close the gap.",
    no_action_required_msg="No Action Required.",
    incomplete_info_msg="Not all information is available to identify gaps. Please review and complete pending questions in the RtR Reporting Tools."
)
# st.write(dimension_name_formal+"_gap_table", df_gap_hazards)

# ('df_pledge', 'all_countries', 'df_2023_plan_summary_by_partner', 'all_countries_all_plans'),
dimension_name = 'all_countries'
dimension_name_formal = "Countries"
base_tool_name = "Pledge Statement"
df_gap_all_countries = calculate_gap_analysis(
    df_base=df_pledge, 
    df_comparison=df_2023_plan_summary_by_partner, 
    base_columns=initial_variables_list, 
    comparison_columns=initial_variables_list, 
    merge_on="InitName", 
    base_concat_col="all_countries", 
    comparison_concat_col="all_countries_all_plans",
    gap_count_col_name= dimension_name+"_gap_n",
    gap_percentage_col_name=dimension_name+"_gap_%",
    action_result_col_name=dimension_name+"_gap_action_req",
    missing_values_col_name=dimension_name+"_gap_what_is_it_pending",
    simple_action_result_col_name=dimension_name+"_gap_results",
    action_required_msg="Action Required: Not all "+dimension_name_formal+" reported in "+base_tool_name+" are presented in the submitted plan(s). There is an opportunity to review the submitted plan(s) and close the gap.",
    no_action_required_msg="No Action Required.",
    incomplete_info_msg="Not all information is available to identify gaps. Please review and complete pending questions in the RtR Reporting Tools."
)
# st.write(dimension_name_formal+"_gap_table", df_gap_all_countries)   

# ('df_pledge', 'p_benefic_pledge_concat', 'df_2023_plan_summary_by_partner', 'p_beneficiaries_all_plans_concat'),
dimension_name = 'p_beneficiaries'
dimension_name_formal = "Primary Beneficiaries"
base_tool_name = "Pledge Statement"
df_gap_p_beneficiaries = calculate_gap_analysis(
    df_base=df_pledge, 
    df_comparison=df_2023_plan_summary_by_partner, 
    base_columns=initial_variables_list, 
    comparison_columns=initial_variables_list, 
    merge_on="InitName", 
    base_concat_col="p_benefic_pledge_concat", 
    comparison_concat_col="p_beneficiaries_all_plans_concat",
    gap_count_col_name= dimension_name+"_gap_n",
    gap_percentage_col_name=dimension_name+"_gap_%",
    action_result_col_name=dimension_name+"_gap_action_req",
    missing_values_col_name=dimension_name+"_gap_what_is_it_pending",
    simple_action_result_col_name=dimension_name+"_gap_results",
    action_required_msg="Action Required: Not all "+dimension_name_formal+" reported in "+base_tool_name+" are presented in the submitted plan(s). There is an opportunity to review the submitted plan(s) and close the gap.",
    no_action_required_msg="No Action Required.",
    incomplete_info_msg="Not all information is available to identify gaps. Please review and complete pending questions in the RtR Reporting Tools."
)
# st.write(dimension_name_formal+"_gap_table", df_gap_p_beneficiaries)


# Result Numeric Pairs
numeric_pairs = [
    ('df_pledge', 'amount_of_finance_anticipated_pledge', 'df_2023_plan_summary_by_partner', 'money_expected_mobilized_sum'),
    ('df_pledge', 'individuals_n_total_pledge_2023', 'df_2023_plan_summary_by_partner', 'individuals_n_total_all_plans_2023_sum'),
    ('df_pledge', 'companies_n_comp_pledge_2023', 'df_2023_plan_summary_by_partner', 'companies_n_comp_all_plans_2023_sum'),
    ('df_pledge', 'region_n_reg_pledge_2023', 'df_2023_plan_summary_by_partner', 'region_n_reg_all_plans_2023_sum'),
    ('df_pledge', 'cities_n_cit_pledge_2023', 'df_2023_plan_summary_by_partner', 'cities_n_cit_all_plans_2023_sum'),
    ('df_pledge', 'natsyst_n_hect_pledge_2023', 'df_2023_plan_summary_by_partner', 'natsyst_n_hect_all_plans_2023_sum'),
]


def perform_gap_analysis_numeric(df_base, df_comparison, merge_on, 
                                 base_value_col, comparison_value_col, 
                                 gap_col_name, action_req_col_name, gap_percentage_col_name,
                                 attention_msg, check_data_msg):
    """
    Perform gap analysis between two dataframes on specified columns, generate action requirements, 
    and calculate the percentage of the gap.
    """
    
    df_merged = df_base[[merge_on, base_value_col]].merge(
        df_comparison[[merge_on, comparison_value_col]], 
        on=merge_on, 
        how="left"
    )

    def evaluate_gap_results(row):
        if pd.isna(row[base_value_col]) or pd.isna(row[comparison_value_col]):
            return "Not all data available"
        elif row[base_value_col] != row[comparison_value_col] and row[base_value_col] != 0 and row[comparison_value_col] != 0:
            return 'Gap'
        elif row[base_value_col] == 0 and row[comparison_value_col] == 0:
            return "Not all data available" 
        elif row[base_value_col] == row[comparison_value_col]:
            return "Aligned"
        else:
            return "Not all data available"

    df_merged[gap_col_name] = df_merged.apply(evaluate_gap_results, axis=1)
    
    # Calculate the percentage of the gap
    def calculate_gap_percentage(row):
        if row[base_value_col] > 0:
            return abs(row[base_value_col] - row[comparison_value_col]) / row[base_value_col] * 100
        else:
            return None  # Avoid division by zero

    df_merged[gap_percentage_col_name] = df_merged.apply(calculate_gap_percentage, axis=1)

    def evaluate_gap_action_req(row):
        if pd.isna(row[base_value_col]) or pd.isna(row[comparison_value_col]):
            return "Please ensure to review and complete the entries in the RtR Reporting Tools. Currently, not all the necessary information is available to identify this gap."
        elif row[base_value_col] != row[comparison_value_col] and row[base_value_col] != 0 and row[comparison_value_col] != 0:
            return attention_msg
        elif row[base_value_col] == 0 and row[comparison_value_col] == 0:
            return "Check Data. It reports 0 as "+dimension_name_formal+" whether in the pledge statement or the plan(s) submitted."
        elif row[base_value_col] == row[comparison_value_col]:
            return "No Action Required."
        else:
            return check_data_msg

    df_merged[action_req_col_name] = df_merged.apply(evaluate_gap_action_req, axis=1)

    return df_merged


# ('df_pledge', 'amount_of_finance_anticipated_pledge', 'df_2023_plan_summary_by_partner', 'money_expected_mobilized_sum'),
# Example usage
dimension_name = 'finance'
dimension_name_formal = "Finance Mobilized"
base_tool_name = "Pledge Statement"
df_gap_finance = perform_gap_analysis_numeric(
    df_base=df_pledge, 
    df_comparison=df_2023_plan_summary_by_partner, 
    merge_on="InitName", 
    base_value_col="amount_of_finance_anticipated_pledge",  
    comparison_value_col="money_expected_mobilized_sum",  
    action_req_col_name=dimension_name + "_gap_action_req",
    gap_col_name=dimension_name + "_gap_results",
    gap_percentage_col_name=dimension_name + "_gap_percentage",
    attention_msg="Attention. There is a difference between pledge statement and plan(s) submitted regarding " + dimension_name_formal, 
    check_data_msg="Check Data. It reports 0 as " + dimension_name_formal + " whether in the pledge statement or the plan(s) submitted.",
)
# st.write(dimension_name_formal + ' Analysis Function', df_gap_finance)


#  ('df_pledge', 'individuals_n_total_pledge_2023', 'df_2023_plan_summary_by_partner', 'individuals_n_total_all_plans_2023_sum'),
dimension_name = 'individuals_n_total'
dimension_name_formal = "Total Number of Individuals"
base_tool_name = "Pledge Statement"
df_gap_n_total_individuals = perform_gap_analysis_numeric(
    df_base=df_pledge, 
    df_comparison=df_2023_plan_summary_by_partner, 
    merge_on="InitName", 
    base_value_col="individuals_n_total_pledge_2023",  
    comparison_value_col="individuals_n_total_all_plans_2023_sum",  
    action_req_col_name= dimension_name+"_gap_action_req",
    gap_col_name = dimension_name+"_gap_results" ,
    gap_percentage_col_name=dimension_name + "_gap_percentage",
    attention_msg="Attention. There is a difference between pledge statement and plan(s) submitted regarding "+dimension_name_formal, 
    check_data_msg="Check Data. It reports 0 as "+dimension_name_formal+" whether in the pledge statement or the plan(s) submitted.",
)
# st.write(dimension_name_formal+'_funtion',df_gap_n_total_individuals)

# ('df_pledge', 'companies_n_comp_pledge_2023', 'df_2023_plan_summary_by_partner', 'companies_n_comp_all_plans_2023_sum'),
dimension_name = 'companies_n'
dimension_name_formal = "Total Number of Companies"
base_tool_name = "Pledge Statement"
df_gap_n_companies = perform_gap_analysis_numeric(
    df_base=df_pledge, 
    df_comparison=df_2023_plan_summary_by_partner, 
    merge_on="InitName", 
    base_value_col="companies_n_comp_pledge_2023",  
    comparison_value_col="companies_n_comp_all_plans_2023_sum",  
    action_req_col_name= dimension_name+"_gap_action_req",
    gap_col_name = dimension_name+"_gap_results" ,
    gap_percentage_col_name=dimension_name + "_gap_percentage",
    attention_msg="Attention. There is a difference between pledge statement and plan(s) submitted regarding "+dimension_name_formal, 
    check_data_msg="Check Data. It reports 0 as "+dimension_name_formal+" whether in the pledge statement or the plan(s) submitted.",
)
# st.write(dimension_name_formal+'_funtion',df_gap_n_companies)


# ('df_pledge', 'region_n_reg_pledge_2023', 'df_2023_plan_summary_by_partner', 'region_n_reg_all_plans_2023_sum'),
dimension_name = 'region_n'
dimension_name_formal = "Total Number of Regions"
base_tool_name = "Pledge Statement"
df_gap_n_regions = perform_gap_analysis_numeric(
    df_base=df_pledge, 
    df_comparison=df_2023_plan_summary_by_partner, 
    merge_on="InitName", 
    base_value_col="region_n_reg_pledge_2023",  
    comparison_value_col="region_n_reg_all_plans_2023_sum",  
    action_req_col_name= dimension_name+"_gap_action_req",
    gap_col_name = dimension_name+"_gap_results" ,
    gap_percentage_col_name=dimension_name + "_gap_percentage",
    attention_msg="Attention. There is a difference between pledge statement and plan(s) submitted regarding "+dimension_name_formal, 
    check_data_msg="Check Data. It reports 0 as "+dimension_name_formal+" whether in the pledge statement or the plan(s) submitted.",
)
# st.write(dimension_name_formal+'_funtion',df_gap_n_regions)

# ('df_pledge', 'cities_n_cit_pledge_2023', 'df_2023_plan_summary_by_partner', 'cities_n_cit_all_plans_2023_sum'),
dimension_name = 'cities_n'
dimension_name_formal = "Total Number of Cities"
base_tool_name = "Pledge Statement"
df_gap_n_cities = perform_gap_analysis_numeric(
    df_base=df_pledge, 
    df_comparison=df_2023_plan_summary_by_partner, 
    merge_on="InitName", 
    base_value_col="cities_n_cit_pledge_2023",  
    comparison_value_col="cities_n_cit_all_plans_2023_sum",  
    action_req_col_name= dimension_name+"_gap_action_req",
    gap_col_name = dimension_name+"_gap_results" ,
    gap_percentage_col_name=dimension_name + "_gap_percentage",
    attention_msg="Attention. There is a difference between pledge statement and plan(s) submitted regarding "+dimension_name_formal, 
    check_data_msg="Check Data. It reports 0 as "+dimension_name_formal+" whether in the pledge statement or the plan(s) submitted.",
)
# st.write(dimension_name_formal+'_funtion',df_gap_n_cities)

# ('df_pledge', 'natsyst_n_hect_pledge_2023', 'df_2023_plan_summary_by_partner', 'natsyst_n_hect_all_plans_2023_sum'),
dimension_name = 'natsyst_n'
dimension_name_formal = "Total Hectares of Natural Systems"
base_tool_name = "Pledge Statement"
df_gap_hect_natsyst = perform_gap_analysis_numeric(
    df_base=df_pledge, 
    df_comparison=df_2023_plan_summary_by_partner, 
    merge_on="InitName", 
    base_value_col="natsyst_n_hect_pledge_2023",  
    comparison_value_col="natsyst_n_hect_all_plans_2023_sum",  
    action_req_col_name= dimension_name+"_gap_action_req",
    gap_col_name = dimension_name+"_gap_results" ,
    gap_percentage_col_name=dimension_name + "_gap_percentage",
    attention_msg="Attention. There is a difference between pledge statement and plan(s) submitted regarding "+dimension_name_formal, 
    check_data_msg="Check Data. It reports 0 as "+dimension_name_formal+" whether in the pledge statement or the plan(s) submitted.",
)
# st.write(dimension_name_formal+'_funtion',df_gap_hect_natsyst)


## Making final data set of GAPs
# Initial dataset with partner names and types
df_gaps_all = df_partners_name[['InitName', 'Org_Type']]

# List of datasets to merge
datasets_to_merge = [
    df_gap_action_clusters,
    df_gap_saa,
    df_gap_hazards,
    df_gap_priority_group,
    df_gap_all_countries,
    df_gap_p_beneficiaries,
    df_gap_finance,
    df_gap_n_total_individuals,
    df_gap_n_companies,
    df_gap_n_regions,
    df_gap_n_cities,
    df_gap_hect_natsyst
]

# Sequentially merge each dataset using a left join
for dataset in datasets_to_merge:
    df_gaps_all = pd.merge(df_gaps_all, dataset, on="InitName", how="left")



# Edits responses depending primary id identification

#Part1 
# Columns to update based on the condition
columns_to_update = [
    'companies_n_gap_action_req',
    'region_n_gap_action_req',
    'cities_n_gap_action_req',
    'natsyst_n_gap_action_req',
]

Response_no_p_beneficiaries = "Please ensure to review and complete the entries in the RtR Reporting Tools. As the identification of primary beneficiaries remains unreported, we are unable to identify this specific gap."

# Apply the condition and update
df_gaps_all[columns_to_update] = df_gaps_all.apply(
    lambda row: [Response_no_p_beneficiaries if pd.isna(row['p_benefic_pledge_concat']) or row['p_benefic_pledge_concat'] == "" and pd.isna(row['p_beneficiaries_all_plans_concat']) or row['p_beneficiaries_all_plans_concat'] == "" else x for x in row[columns_to_update]],
    axis=1, result_type='expand'
)

# Part2 Companies

def update_row(row):
    # Convert column values to string, handling NaN values to avoid TypeError
    p_benefic_pledge_concat = str(row['p_benefic_pledge_concat']) if pd.notna(row['p_benefic_pledge_concat']) else ""
    p_beneficiaries_all_plans_concat = str(row['p_beneficiaries_all_plans_concat']) if pd.notna(row['p_beneficiaries_all_plans_concat']) else ""

    # Now perform the check with the string-converted values
    if 'Companies' in p_benefic_pledge_concat or 'Companies' in p_beneficiaries_all_plans_concat:
        # If "Companies" is found in either column, do nothing (values remain the same)
        return row
    else:
        # If "Companies" is not found in both columns, update specific columns
        row['companies_n_gap_results'] = 'No apply'
        row['companies_n_gap_percentage'] = None
        row['companies_n_gap_action_req'] = 'No apply'
    return row
# Apply the function to each row
df_gaps_all = df_gaps_all.apply(update_row, axis=1)


#Cites
def update_row(row):
    # Convert column values to string, handling NaN values to avoid TypeError
    p_benefic_pledge_concat = str(row['p_benefic_pledge_concat']) if pd.notna(row['p_benefic_pledge_concat']) else ""
    p_beneficiaries_all_plans_concat = str(row['p_beneficiaries_all_plans_concat']) if pd.notna(row['p_beneficiaries_all_plans_concat']) else ""

    # Now perform the check with the string-converted values
    if 'Cities' in p_benefic_pledge_concat or 'Cities' in p_beneficiaries_all_plans_concat:
        # If "Companies" is found in either column, do nothing (values remain the same)
        return row
    else:
        # If "Companies" is not found in both columns, update specific columns
        row['cities_n_gap_results'] = 'No apply'
        row['cities_n_gap_percentage'] = None
        row['cities_n_gap_action_req'] = 'No apply'
    return row
# Apply the function to each row
df_gaps_all = df_gaps_all.apply(update_row, axis=1)


#Regions
def update_row(row):
    # Convert column values to string, handling NaN values to avoid TypeError
    p_benefic_pledge_concat = str(row['p_benefic_pledge_concat']) if pd.notna(row['p_benefic_pledge_concat']) else ""
    p_beneficiaries_all_plans_concat = str(row['p_beneficiaries_all_plans_concat']) if pd.notna(row['p_beneficiaries_all_plans_concat']) else ""

    # Now perform the check with the string-converted values
    if 'Regions' in p_benefic_pledge_concat or 'Regions' in p_beneficiaries_all_plans_concat:
        # If "Companies" is found in either column, do nothing (values remain the same)
        return row
    else:
        # If "Companies" is not found in both columns, update specific columns
        row['region_n_gap_results'] = 'No apply'
        row['region_n_gap_percentage'] = None
        row['region_n_gap_action_req'] = 'No apply'
    return row
# Apply the function to each row
df_gaps_all = df_gaps_all.apply(update_row, axis=1)


#Natural Systems
def update_row(row):
    # Convert column values to string, handling NaN values to avoid TypeError
    p_benefic_pledge_concat = str(row['p_benefic_pledge_concat']) if pd.notna(row['p_benefic_pledge_concat']) else ""
    p_beneficiaries_all_plans_concat = str(row['p_beneficiaries_all_plans_concat']) if pd.notna(row['p_beneficiaries_all_plans_concat']) else ""

    # Now perform the check with the string-converted values
    if 'Natural Systems' in p_benefic_pledge_concat or 'Natural Systems' in p_beneficiaries_all_plans_concat:
        # If "Companies" is found in either column, do nothing (values remain the same)
        return row
    else:
        # If "Companies" is not found in both columns, update specific columns
        row['natsyst_n_gap_results'] = 'No apply'
        row['natsyst_n_gap_percentage'] = None
        row['natsyst_n_gap_action_req'] = 'No apply'
    return row
# Apply the function to each row
df_gaps_all = df_gaps_all.apply(update_row, axis=1)

df_gaps_all['gaps_summary'] = "df_gaps_all"

variables_to_summary = {
    'action_clusters_gap_results': 'Action clusters do not coincide (GI-PLAN)',
    'saa_gap_results': 'SAA priority groups do not coincide (GI-PLAN)',
    'hazards_gap_results': 'Hazards do not coincide (GI-PLAN)',
    'priority_groups_gap_results': 'Priority vulnerable groups do not coincide (GI-PLAN)',
    'all_countries_gap_results': 'Countries do not coincide (PLEDGE-PLAN)',
    'p_beneficiaries_gap_results': 'Primary beneficiaries do not coincide (PLEDGE-PLAN)',
    'individuals_n_total_gap_results': 'Total number of individuals does not coincide (PLEDGE-PLAN)',
    'companies_n_gap_results': 'Number of companies does not coincide (PLEDGE-PLAN)',
    'region_n_gap_results': 'Number of regions does not coincide (PLEDGE-PLAN)',
    'cities_n_gap_results': 'Number of cities does not coincide (PLEDGE-PLAN)',
    'natsyst_n_gap_results': 'Hectares of natural systems do not coincide (PLEDGE-PLAN)'
}

# Iterate over each row in the dataframe
for index, row in df_gaps_all.iterrows():
    gaps_summary = []  # Initialize an empty list for each row
    # Check each variable in variables_to_summary
    for left_var, right_var in variables_to_summary.items():
        if row[left_var] == 'Gap':  # If the left-side variable equals 'Gap'
            gaps_summary.append(right_var)  # Add the corresponding right-side variable to the list
        
    
    # Join the list with ";" and assign it to the 'gaps_summary' column
    df_gaps_all.at[index, 'gaps_summary'] = ";".join(gaps_summary)


list_gaps = ['action_clusters_gap_results','saa_gap_results','hazards_gap_results','priority_groups_gap_results',
        'all_countries_gap_results','p_beneficiaries_gap_results','individuals_n_total_gap_results','companies_n_gap_results',
        'region_n_gap_results','cities_n_gap_results','natsyst_n_gap_results']


summary_gaps_table = df_gaps_all[['InitName','gaps_summary']+list_gaps]

# Resulting merged dataset
# st.write('All_Gaps Table 2',summary_gaps_table, summary_gaps_table.columns )




## Creating a aggregated excel document to export as excel type. Each data set in a especific row

values_readme = {
    'Report Tracking':'Data set with key information to Partner Tracking. It present key information of RtR Reporting tools',
    'df_gaps_all': 'All possible gaps identifiable among all official RtR Reporting Tools.',
    'df_gi_summary': 'General Information Survey (enhanced version 2023), Key Variables.',
    'df_pledge_summary': 'Pledge Statement Survey (enhanced version 2023), Key Variables.',
    'all_plans_by_partners': "Partners' aggregated information from all their Resilience Building Plan Submissions (enhanced version 2023).",
    'df_2023_plan_summary': 'Plan Submission Key Variables (enhanced version 2023), Key Variables.',
    'df_gi': 'General Information Survey (enhanced version 2023), all data available including results of analysis of gaps, completeness, and confidence of the reporting.',
    'df_pledge': 'Pledge Statement Survey (enhanced version 2023), all data available including results of analysis of gaps, completeness, and confidence of the reporting.',
    'df_2023_plan': 'Resilience Building Plan Submission tool (enhanced version 2023), all data available including results of analysis of gaps, completeness, and confidence of the reporting.',
}

# Creating a DataFrame from the dictionary
readme = pd.DataFrame(list(values_readme.items()), columns=['Name of the Data Sets', 'Description'])


# Edition of costumized request for Partners

# df_gi['gi_completeness_req_priority']
# st.write("Columns GI")
# Concatenated string column
concatenated_column = df_gi['gi_completeness_req_priority']

# Initialize an empty set to collect unique values
unique_values = set()

# Iterating through each row and splitting the concatenated string
for row in concatenated_column:
    # Splitting by both ";" and ","
    parts = row.split(';')
    for part in parts:
        # Split each part by "," and strip spaces from each value
        values = [value.strip() for value in part.split(',')]
        unique_values.update(values)

# Convert set to a list if needed
unique_values_list_gi = list(unique_values)
# st.write(unique_values_list_gi)


# st.write("Columns Pledge")
# Concatenated string column
concatenated_column = df_pledge['pledge_completeness_req_priority']

# Initialize an empty set to collect unique values
unique_values = set()

# Iterating through each row and splitting the concatenated string
for row in concatenated_column:
    # Splitting by both ";" and ","
    parts = row.split(';')
    for part in parts:
        # Split each part by "," and strip spaces from each value
        values = [value.strip() for value in part.split(',')]
        unique_values.update(values)

# Convert set to a list if needed
unique_values_list_pledge = list(unique_values)
# st.write(unique_values_list_pledge)


# st.write("Columns Plan")
# Concatenated string column
concatenated_column = df_2023_plan['plan_completeness_req_priority']

# Initialize an empty set to collect unique values
unique_values = set()

# Iterating through each row and splitting the concatenated string
for row in concatenated_column:
    # Splitting by both ";" and ","
    parts = row.split(';')
    for part in parts:
        # Split each part by "," and strip spaces from each value
        values = [value.strip() for value in part.split(',')]
        unique_values.update(values)

# Convert set to a list if needed
unique_values_list_plan = list(unique_values)
# st.write(unique_values_list_plan)


# st.write("Columns Plan Summary per Partner")
# Concatenated string column
concatenated_column = df_2023_plan_summary_by_partner['all_plans_completeness_req_priority']

# Initialize an empty set to collect unique values
unique_values = set()

# Iterating through each row and splitting the concatenated string
for row in concatenated_column:
    # Splitting by both ";" and ","
    parts = row.split(';')
    for part in parts:
        # Split each part by "," and strip spaces from each value
        values = [value.strip() for value in part.split(',')]
        unique_values.update(values)

# Convert set to a list if needed
unique_values_list_plan_per_partner = list(unique_values)
# st.write(unique_values_list_plan_per_partner)







## HAZARDS

#creating dataframe for hazards only
# df_pledge[['InitName','hazards_all_pledge_concat']]
# df_2022_2023_plan_consolidated_by_partner[['InitName','hazards_pledge_n_plan']]

df_hazards_pledge_plan = df_pledge[['InitName', 'hazards_all_pledge_concat']].merge(
    df_2023_plan_summary_by_partner[['InitName', 'hazards_all_plans_concat']],
    on='InitName',
    how='outer'
)


# Concatenate 'hazards_all_pledge_concat' and 'hazards_pledge_n_plan' with a semicolon
df_hazards_pledge_plan['hazards_pledge_n_plan'] = df_hazards_pledge_plan.apply(
    lambda row: '; '.join(
        [str(item) for item in [row['hazards_all_pledge_concat'], row['hazards_all_plans_concat']] if pd.notna(item)]
    ),
    axis=1
)


# Split the string by ";", create a set of unique values, and then join them back with ";"
df_hazards_pledge_plan['hazards_pledge_n_plan'] = df_hazards_pledge_plan['hazards_pledge_n_plan'].apply(
    lambda x: '; '.join(sorted(set(x.split('; ')))) if pd.notna(x) else x
)



# List of columns to transform
list_to_all_hazards_dataset = ['InitName', 'hazards_pledge_n_plan', 'hazards_all_pledge_concat', 'hazards_all_plans_concat']

# Melting the dataframe
melted = df_hazards_pledge_plan[list_to_all_hazards_dataset].melt(
    id_vars=['InitName'], 
    value_vars=['hazards_pledge_n_plan', 'hazards_all_pledge_concat', 'hazards_all_plans_concat'],
    var_name='source', 
    value_name='hazard'
)



# Split the concatenated values into lists, explode them into separate rows
melted['hazard'] = melted['hazard'].str.split(';')
melted = melted.explode('hazard')

# Assign the source value based on the original column
melted['source'] = melted['source'].map({
    'hazards_pledge_n_plan': 'Pledge_n_Plan',
    'hazards_all_pledge_concat': 'Pledge',
    'hazards_all_plans_concat': 'Plans'
})


# Create the new dataset
df_hazards_pledge_plan_vertical = melted.dropna(subset=['hazard'])
df_hazards_pledge_plan_vertical = df_hazards_pledge_plan_vertical[df_hazards_pledge_plan_vertical['hazard'] != ""]
df_hazards_pledge_plan_vertical['hazard'] = df_hazards_pledge_plan_vertical['hazard'].str.replace(r'\s+', ' ', regex=True).str.strip()


# st.write("df_hazards_pledge_plan_vertical")
# df_hazards_pledge_plan_vertical['hazard'] 


# Define individual dictionaries for each hazard group following IPCC Category

no_hazard_list = {'Water stress (rural focus)':'Not a climate hazard',
                  'Water stress (urban focus)':'Not a climate hazard',
                  'Earthquake':'Not a climate hazard',
                  'Climate Change':'Not a climate hazard'}

coastal_list = {'Oceanic Events': 'Coastal / Ocean', 'Other coastal events': 'Coastal / Ocean'}
cold_list = {'Extreme cold': 'Cold'}
snow_list = {"Snow, Ice": 'Snow and Ice'}
heat_list = {'Extreme heat': 'Heat'}
dry_list = {'Drought (agriculture focus)': 'Dry', 'Drought (other sectors)': 'Dry','Wildfire': 'Dry'}
Wet_list = {'Coastal flood': 'Wet', 'Urban flood': 'Wet', 'River flood': 'Wet'}
wind_list = {'Extreme wind': 'Wind', 'Tropical Cyclone': 'Wind'}

hazard_dictionary = {**no_hazard_list, **coastal_list,**cold_list, **snow_list, **heat_list, **dry_list, **Wet_list, **wind_list}


# Map the 'hazard' column to the new 'hazard_group' column
df_hazards_pledge_plan_vertical['hazard_group'] = df_hazards_pledge_plan_vertical['hazard'].map(hazard_dictionary)



# #ORIGINAL 2023
# # Define individual dictionaries for each hazard group
# flooding_list = {'Coastal flood': 'Flooding', 'Urban flood': 'Flooding', 'River flood': 'Flooding'}
# drought_list = {'Drought (agriculture focus)': 'Drought', 'Drought (other sectors)': 'Drought'}
# water_list = {'Water stress (rural focus)': 'Water', 'Water stress (urban focus)': 'Water'}
# fire_list = {'Wildfire': 'Fire'}
# coastal_list = {'Oceanic Events': 'Coastal / Ocean', 'Other coastal events': 'Coastal / Ocean'}
# cold_list = {'Extreme cold': 'Cold', "Snow, Ice": 'Cold'}
# wind_list = {'Extreme wind': 'Wind', 'Tropical Cyclone': 'Wind'}
# heat_list = {'Extreme heat': 'Heat'}
# other_list = {'Earthquake':'Other','Climate Change':'Other'}

# # Combine all dictionaries into one
# hazard_dictionary = {**flooding_list, **drought_list, **water_list, **fire_list, **coastal_list, **cold_list, **wind_list, **heat_list, **other_list}

# # Map the 'hazard' column to the new 'hazard_group' column
# df_hazards_pledge_plan_vertical['hazard_group'] = df_hazards_pledge_plan_vertical['hazard'].map(hazard_dictionary)


# st.write("Hazards Final")
# df_hazards_pledge_plan_vertical

















# #######____________________________________________
# #######________META TABLE COUNTRIES PLEDGE & PLAN  #USE ALL INFO
def meta_table_countries_all_sources(df_pledge,df_2023_plan,df_2023_plan_summary_by_partner,):
    # GENERAL SOURCES
    # by pledge (all pledges)
    list_variables_pledge = ['InitName','short_name','Org_Type','all_countries']
    df_m_countries_pledge = df_pledge[list_variables_pledge]
    df_m_countries_pledge['source'] = 'Pledge (General)'

    # by Plans
    # list_variables_plan = ['InitName','short_name','Org_Type','plan_short_name','all_countries'] #OLD
    list_variables_plan = ['InitName','Org_Type','plan_short_name','all_countries']
    # df_m_countries_plan = df_2022_2023_plan_consolidated[list_variables_plan] #OLD
    df_m_countries_plan = df_2023_plan[list_variables_plan]
    rename_plans = {'plan_short_name': 'source'}
    df_m_countries_plan = df_m_countries_plan.rename(columns=rename_plans)
    df_m_countries_plan['source'] = df_m_countries_plan['source'] + " (General)"

    #by Partner Submitting Plan(s)
    list_variables_plan_by_partner = ['InitName','all_countries_all_plans']
    # df_m_countries_plan_by_partner = df_2023_plan_summary_by_partner[list_variables_plan_by_partner] #OLD
    df_m_countries_plan_by_partner = df_2023_plan_summary_by_partner[list_variables_plan_by_partner]
    rename_plans_all = {'all_countries_all_plans': 'all_countries'}
    df_m_countries_plan_by_partner = df_m_countries_plan_by_partner.rename(columns=rename_plans_all)
    df_m_countries_plan_by_partner = pd.merge(df_m_countries_plan_by_partner, df_partners_name[['InitName','short_name','Org_Type']], on='InitName', how='inner')
    df_m_countries_plan_by_partner['source'] = 'Plans (All Plans)'

    #By all Tools
    df_m_countries_all_tools = pd.concat([
        df_m_countries_pledge[['InitName', 'all_countries']], 
        df_m_countries_plan_by_partner[['InitName', 'all_countries']]
    ]).reset_index(drop=True)
    # df_m_countries_all_tools
    df_m_countries_all_tools = df_m_countries_all_tools.groupby('InitName').agg(
        all_countries=('all_countries', lambda x: "; ".join(x.unique())),  # concatenate unique country names    
    ).reset_index()
    df_m_countries_all_tools = pd.merge(df_m_countries_all_tools, df_partners_name[['InitName','short_name','Org_Type']], on='InitName', how='inner')
    df_m_countries_all_tools['source'] ='All Tools (Pledge & Plan)'
    # df_m_countries_all_tools.columns



    # SPECIFIC SOURCES
    #By specif pledge
    list_countries_different_pledge = ['countries_individuals','countries_companies','countries_regions','countries_cities','countries_nat_sys',]

    #by Partner Pledges Beneficiaries
    list_variables_ = ['InitName','countries_individuals']
    pledge_country_individuals = df_pledge[list_variables_]
    rename_list = {'countries_individuals': 'all_countries'}
    pledge_country_individuals = pledge_country_individuals.rename(columns=rename_list)
    pledge_country_individuals = pd.merge(pledge_country_individuals, df_partners_name[['InitName','short_name','Org_Type']], on='InitName', how='inner')
    pledge_country_individuals['source'] = 'Pledge: Individuals (Direct)'

    list_variables_ = ['InitName','countries_companies']
    pledge_country_companies = df_pledge[list_variables_]
    rename_list = {'countries_companies': 'all_countries'}
    pledge_country_companies = pledge_country_companies.rename(columns=rename_list)
    pledge_country_companies = pd.merge(pledge_country_companies, df_partners_name[['InitName','short_name','Org_Type']], on='InitName', how='inner')
    pledge_country_companies['source'] = 'Pledge: Individuals through Companies'

    list_variables_ = ['InitName','countries_regions']
    pledge_country_regions = df_pledge[list_variables_]
    rename_list = {'countries_regions': 'all_countries'}
    pledge_country_regions = pledge_country_regions.rename(columns=rename_list)
    pledge_country_regions = pd.merge(pledge_country_regions, df_partners_name[['InitName','short_name','Org_Type']], on='InitName', how='inner')
    pledge_country_regions['source'] = 'Pledge: Individuals through Regions'

    list_variables_ = ['InitName','countries_cities']
    pledge_country_cities = df_pledge[list_variables_]
    rename_list = {'countries_cities': 'all_countries'}
    pledge_country_cities = pledge_country_cities.rename(columns=rename_list)
    pledge_country_cities = pd.merge(pledge_country_cities, df_partners_name[['InitName','short_name','Org_Type']], on='InitName', how='inner')
    pledge_country_cities['source'] = 'Pledge: Individuals through Cities'

    list_variables_ = ['InitName','countries_nat_sys']
    pledge_country_natsys = df_pledge[list_variables_]
    rename_list = {'countries_nat_sys': 'all_countries'}
    pledge_country_natsys = pledge_country_natsys.rename(columns=rename_list)
    pledge_country_natsys = pd.merge(pledge_country_natsys, df_partners_name[['InitName','short_name','Org_Type']], on='InitName', how='inner')
    pledge_country_natsys['source'] = 'Pledge: Individuals through Natural Systems'


    #By specif Plan consolidated
    list_countries_different_plan = ['countries_individuals','countries_companies','countries_regions','countries_cities','countries_nat_sys',]
    # df_2023_plan[list_countries_different_plan]
    df_2023_plan = df_2023_plan.reset_index(drop=True)

    # by Partner Plan Beneficiaries
    # list_variables_ = ['InitName','countries_individuals'] #OLD
    list_variables_ = ['InitName','countries_individuals']
    # df_2023_plan[list_variables_]
    # plan_country_individuals = df_2022_2023_plan_consolidated[list_variables_] #OLD
    plan_country_individuals = df_2023_plan[list_variables_]
    rename_list = {'countries_individuals': 'all_countries'}
    plan_country_individuals = plan_country_individuals.rename(columns=rename_list)
    plan_country_individuals = pd.merge(plan_country_individuals, df_partners_name[['InitName','short_name','Org_Type']], on='InitName', how='inner')
    plan_country_individuals['source'] = df_2023_plan['plan_short_name'] +'- Individuals (Direct)'


    list_variables_ = ['InitName','countries_companies']
    # plan_country_companies = df_2022_2023_plan_consolidated[list_variables_] #OLD
    plan_country_companies = df_2023_plan[list_variables_] 
    rename_list = {'countries_companies': 'all_countries'}
    plan_country_companies = plan_country_companies.rename(columns=rename_list)
    plan_country_companies = pd.merge(plan_country_companies, df_partners_name[['InitName','short_name','Org_Type']], on='InitName', how='inner')
    # plan_country_companies['source'] = df_2022_2023_plan_consolidated['plan_short_name'] +'- Individuals through Companies' #OLD
    plan_country_companies['source'] = df_2023_plan['plan_short_name'] +'- Individuals through Companies'

    list_variables_ = ['InitName','countries_regions']
    # plan_country_regions = df_2022_2023_plan_consolidated[list_variables_] #OLD
    plan_country_regions = df_2023_plan[list_variables_]
    rename_list = {'countries_regions': 'all_countries'}
    plan_country_regions = plan_country_regions.rename(columns=rename_list)
    plan_country_regions = pd.merge(plan_country_regions, df_partners_name[['InitName','short_name','Org_Type']], on='InitName', how='inner')
    plan_country_regions['source'] = df_2023_plan['plan_short_name'] +'- Individuals through Regions'


    list_variables_ = ['InitName','countries_cities']
    # plan_country_cities = df_2022_2023_plan_consolidated[list_variables_] #OLD
    plan_country_cities = df_2023_plan[list_variables_]
    rename_list = {'countries_cities': 'all_countries'}
    plan_country_cities = plan_country_cities.rename(columns=rename_list)
    plan_country_cities = pd.merge(plan_country_cities, df_partners_name[['InitName','short_name','Org_Type']], on='InitName', how='inner')
    # plan_country_cities['source'] = df_2022_2023_plan_consolidated['plan_short_name'] +'- Individuals through Cities' #OLD
    plan_country_cities['source'] = df_2023_plan['plan_short_name'] +'- Individuals through Cities'

    list_variables_ = ['InitName','countries_nat_sys']
    # plan_country_natsyst = df_2022_2023_plan_consolidated[list_variables_] #OLD
    plan_country_natsyst = df_2023_plan[list_variables_]
    rename_list = {'countries_nat_sys': 'all_countries'}
    plan_country_natsyst = plan_country_natsyst.rename(columns=rename_list)
    plan_country_natsyst = pd.merge(plan_country_natsyst, df_partners_name[['InitName','short_name','Org_Type']], on='InitName', how='inner')
    # plan_country_natsyst['source'] = df_2022_2023_plan_consolidated['plan_short_name'] +'- Individuals through Natural Systems' #OLD
    plan_country_natsyst['source'] = df_2023_plan['plan_short_name'] +'- Individuals through Natural Systems'



    #Making one data set horizonatal
    # Concatenate the DataFrames
    df_m_countries = pd.concat([df_m_countries_plan, df_m_countries_pledge,df_m_countries_plan_by_partner,df_m_countries_all_tools,pledge_country_individuals,pledge_country_companies,pledge_country_regions,pledge_country_cities, pledge_country_natsys,plan_country_individuals,plan_country_companies,plan_country_regions,plan_country_cities,plan_country_natsyst])
    # Reset the index if needed, to avoid duplicate indices
    df_m_countries.reset_index(drop=True, inplace=True)

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

    df_m_countries['Africa'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Africa_list for country in x])), 'Africa', '')
    df_m_countries['Asia'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Asia_list for country in x])), 'Asia', '')
    df_m_countries['Europe'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Europe_list for country in x])), 'Europe', '')
    df_m_countries['LATAMC'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in LATAMC_list for country in x])), 'Latin America and the Caribbean', '')
    df_m_countries['Northern_America'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
    df_m_countries['Oceania'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Oceania_list for country in x])), 'Oceania', '')

    continents_pledge_list = ['Africa','Asia','Europe','LATAMC','Northern_America','Oceania']
    # st.write(df_m_countries[continents_pledge_list])

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

    df_m_countries['South_Asia'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in South_Asia_list for country in x])), 'South Asia', '')
    df_m_countries['Europe_Central_Asia'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Europe_Central_Asia_list for country in x])), 'Europe & Central Asia', '')
    df_m_countries['Middle_East_North_Africa'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Middle_East_North_Africa_list for country in x])), 'Middle East & North Africa', '')
    df_m_countries['Sub_Saharan_Africa'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Sub_Saharan_Africa_list for country in x])), 'Sub-Saharan Africa', '')
    df_m_countries['Latin_America_Caribbean'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Latin_America_Caribbean_list for country in x])), 'Latin America & Caribbean', '')
    df_m_countries['East_Asia_Pacific'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in East_Asia_Pacific_list for country in x])), 'East Asia & Pacific', '')
    df_m_countries['North_America'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in North_America_list for country in x])), 'North America', '')

    regions_pledge_list = ['South_Asia','Europe_Central_Asia','Middle_East_North_Africa','Sub_Saharan_Africa','Latin_America_Caribbean','East_Asia_Pacific','North_America']
    # st.write(df_m_countries[regions_pledge_list])

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

    df_m_countries['Southern_Asia'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Asia_list for country in x])), 'Southern Asia', '')
    df_m_countries['Southern_Europe'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Europe_list for country in x])), 'Southern Europe', '')
    df_m_countries['Northern_Africa'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_Africa_list for country in x])), 'Northern Africa', '')
    df_m_countries['Middle_Africa'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Middle_Africa_list for country in x])), 'Middle Africa', '')
    df_m_countries['Caribbean'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Caribbean_list for country in x])), 'Caribbean', '')
    df_m_countries['South_America'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in South_America_list for country in x])), 'South America', '')
    df_m_countries['Western_Asia'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Asia_list for country in x])), 'Western Asia', '')
    df_m_countries['Australia_and_New_Zealand'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Australia_and_New_Zealand_list for country in x])), 'Australia and New Zealand', '')
    df_m_countries['Western_Europe'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Europe_list for country in x])), 'Western Europe', '')
    df_m_countries['Eastern_Europe'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Europe_list for country in x])), 'Eastern Europe', '')
    df_m_countries['Central_America'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Central_America_list for country in x])), 'Central America', '')
    df_m_countries['Western_Africa'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Africa_list for country in x])), 'Western Africa', '')
    df_m_countries['Southern_Africa'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Africa_list for country in x])), 'Southern Africa', '')
    df_m_countries['Eastern_Africa'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Africa_list for country in x])), 'Eastern Africa', '')
    df_m_countries['South_Eastern_Asia'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in South_Eastern_Asia_list for country in x])), 'South-Eastern Asia', '')
    df_m_countries['Northern_America'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
    df_m_countries['Eastern_Asia'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Asia_list for country in x])), 'Eastern Asia', '')
    df_m_countries['Northern_Europe'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_Europe_list for country in x])), 'Northern Europe', '')
    df_m_countries['Central_Asia'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Central_Asia_list for country in x])), 'Central Asia', '')
    df_m_countries['Melanesia'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Melanesia_list for country in x])), 'Melanesia', '')
    df_m_countries['Polynesia'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Polynesia_list for country in x])), 'Polynesia', '')
    df_m_countries['Micronesia'] = np.where(df_m_countries['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Micronesia_list for country in x])), 'Micronesia', '')

    subregions_pledge_list = ['Southern_Asia','Southern_Europe','Northern_Africa','Middle_Africa','Caribbean','South_America',
                            'Western_Asia','Australia_and_New_Zealand','Western_Europe','Eastern_Europe','Central_America',
                            'Western_Africa','Southern_Africa','Eastern_Africa','South_Eastern_Asia','Northern_America','Eastern_Asia',
                            'Northern_Europe','Central_Asia','Melanesia','Polynesia','Micronesia',]

    # st.write(df_m_countries[subregions_pledge_list])
    # #Concatenating columns
    df_m_countries['country_continents_all'] = df_m_countries[continents_pledge_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
    df_m_countries['country_region_all'] = df_m_countries[regions_pledge_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
    df_m_countries['country_subregion_all'] = df_m_countries[subregions_pledge_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)

    # Vertical
    # Split the 'all_countries' string into a list, remove duplicates within each list

    # df_m_countries
    df_m_countries_vertical = df_m_countries[['InitName','short_name','Org_Type','source','all_countries',]]
    df_m_countries_vertical['all_countries'] = df_m_countries_vertical['all_countries'].apply(lambda x: list(set(x.split('; '))))
    # Explode the DataFrame so each country is in its own row, maintaining the other columns

    df_m_countries_vertical = df_m_countries_vertical.explode('all_countries')
    df_m_countries_vertical['all_countries'] = df_m_countries_vertical['all_countries'].str.strip()
    df_m_countries_vertical = df_m_countries_vertical[df_m_countries_vertical['all_countries'] != '']
    df_m_countries_vertical['all_countries'] = df_m_countries_vertical['all_countries'].str.replace('"', '')

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

    df_m_countries_vertical['Africa'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Africa_list for country in x])), 'Africa', '')
    df_m_countries_vertical['Asia'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Asia_list for country in x])), 'Asia', '')
    df_m_countries_vertical['Europe'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Europe_list for country in x])), 'Europe', '')
    df_m_countries_vertical['LATAMC'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in LATAMC_list for country in x])), 'Latin America and the Caribbean', '')
    df_m_countries_vertical['Northern_America'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
    df_m_countries_vertical['Oceania'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Oceania_list for country in x])), 'Oceania', '')

    continents_pledge_list = ['Africa','Asia','Europe','LATAMC','Northern_America','Oceania']
    # st.write(df_m_countries_vertical[continents_pledge_list])

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

    df_m_countries_vertical['South_Asia'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in South_Asia_list for country in x])), 'South Asia', '')
    df_m_countries_vertical['Europe_Central_Asia'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Europe_Central_Asia_list for country in x])), 'Europe & Central Asia', '')
    df_m_countries_vertical['Middle_East_North_Africa'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Middle_East_North_Africa_list for country in x])), 'Middle East & North Africa', '')
    df_m_countries_vertical['Sub_Saharan_Africa'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Sub_Saharan_Africa_list for country in x])), 'Sub-Saharan Africa', '')
    df_m_countries_vertical['Latin_America_Caribbean'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Latin_America_Caribbean_list for country in x])), 'Latin America & Caribbean', '')
    df_m_countries_vertical['East_Asia_Pacific'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in East_Asia_Pacific_list for country in x])), 'East Asia & Pacific', '')
    df_m_countries_vertical['North_America'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in North_America_list for country in x])), 'North America', '')

    regions_pledge_list = ['South_Asia','Europe_Central_Asia','Middle_East_North_Africa','Sub_Saharan_Africa','Latin_America_Caribbean','East_Asia_Pacific','North_America']
    # st.write(df_m_countries_vertical[regions_pledge_list])

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

    df_m_countries_vertical['Southern_Asia'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Asia_list for country in x])), 'Southern Asia', '')
    df_m_countries_vertical['Southern_Europe'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Europe_list for country in x])), 'Southern Europe', '')
    df_m_countries_vertical['Northern_Africa'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_Africa_list for country in x])), 'Northern Africa', '')
    df_m_countries_vertical['Middle_Africa'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Middle_Africa_list for country in x])), 'Middle Africa', '')
    df_m_countries_vertical['Caribbean'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Caribbean_list for country in x])), 'Caribbean', '')
    df_m_countries_vertical['South_America'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in South_America_list for country in x])), 'South America', '')
    df_m_countries_vertical['Western_Asia'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Asia_list for country in x])), 'Western Asia', '')
    df_m_countries_vertical['Australia_and_New_Zealand'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Australia_and_New_Zealand_list for country in x])), 'Australia and New Zealand', '')
    df_m_countries_vertical['Western_Europe'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Europe_list for country in x])), 'Western Europe', '')
    df_m_countries_vertical['Eastern_Europe'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Europe_list for country in x])), 'Eastern Europe', '')
    df_m_countries_vertical['Central_America'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Central_America_list for country in x])), 'Central America', '')
    df_m_countries_vertical['Western_Africa'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Western_Africa_list for country in x])), 'Western Africa', '')
    df_m_countries_vertical['Southern_Africa'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Southern_Africa_list for country in x])), 'Southern Africa', '')
    df_m_countries_vertical['Eastern_Africa'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Africa_list for country in x])), 'Eastern Africa', '')
    df_m_countries_vertical['South_Eastern_Asia'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in South_Eastern_Asia_list for country in x])), 'South-Eastern Asia', '')
    df_m_countries_vertical['Northern_America'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_America_list for country in x])), 'Northern America', '')
    df_m_countries_vertical['Eastern_Asia'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Eastern_Asia_list for country in x])), 'Eastern Asia', '')
    df_m_countries_vertical['Northern_Europe'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Northern_Europe_list for country in x])), 'Northern Europe', '')
    df_m_countries_vertical['Central_Asia'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Central_Asia_list for country in x])), 'Central Asia', '')
    df_m_countries_vertical['Melanesia'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Melanesia_list for country in x])), 'Melanesia', '')
    df_m_countries_vertical['Polynesia'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Polynesia_list for country in x])), 'Polynesia', '')
    df_m_countries_vertical['Micronesia'] = np.where(df_m_countries_vertical['all_countries'].str.split(';').apply(lambda x: any([country.strip() in Micronesia_list for country in x])), 'Micronesia', '')

    subregions_pledge_list = ['Southern_Asia','Southern_Europe','Northern_Africa','Middle_Africa','Caribbean','South_America',
                            'Western_Asia','Australia_and_New_Zealand','Western_Europe','Eastern_Europe','Central_America',
                            'Western_Africa','Southern_Africa','Eastern_Africa','South_Eastern_Asia','Northern_America','Eastern_Asia',
                            'Northern_Europe','Central_Asia','Melanesia','Polynesia','Micronesia',]

    # st.write(df_m_countries_vertical[subregions_pledge_list])
    # #Concatenating columns
    df_m_countries_vertical['country_continents_all'] = df_m_countries_vertical[continents_pledge_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
    df_m_countries_vertical['country_region_all'] = df_m_countries_vertical[regions_pledge_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)
    df_m_countries_vertical['country_subregion_all'] = df_m_countries_vertical[subregions_pledge_list].apply(lambda x:';'.join(x.dropna().astype(str)),axis=1)

    df_country_2 = df_country
    rename = {'Country': 'all_countries'}
    df_country_2 = df_country_2.rename(columns=rename)
    df_m_countries_vertical = pd.merge(df_m_countries_vertical, df_country_2[['all_countries','country_to_plot']], on='all_countries', how='inner')

    list_source = {"Pledge (General)": 'Pledge (All Beneficiaries)', 'All Tools (Pledge & Plan)': 'All Tools Available',
                "Plans (All Plans)":"Plans (All Plans, in case there is more than one)"}
    df_m_countries_vertical['source'] = df_m_countries_vertical['source'].replace(list_source)
    df_m_countries_vertical['source'] = df_m_countries_vertical['source'].apply(lambda x: x.replace("(General)", "(All Beneficiaries)") if "(General)" in x else x)
    df_m_countries_vertical['countries_count'] = df_m_countries_vertical['all_countries'].map(df_m_countries_vertical['all_countries'].value_counts())

    return df_m_countries, df_m_countries_vertical
    
    
    # df_m_countries_vertical

    # st.write(df_m_countries[['InitName','source','all_countries','country_continents_all','country_region_all','country_subregion_all']])
    # df_m_countries
df_m_countries, df_m_countries_vertical = meta_table_countries_all_sources(df_pledge,df_2023_plan,df_2023_plan_summary_by_partner)


#DATA SET FOR PARTNER FINDER
def df_to_partner_finder():
    list_variables = ['InitName','all_countries','country_continents_all','country_region_all','country_subregion_all']
    df_m_countries_filter_partner_finder = df_m_countries[df_m_countries['source'] == 'All Tools (Pledge & Plan)'][list_variables]
    # df_m_countries_filter_partner_finder

    # Making one database to plot in Partner Finder. It has the structere needed for the selection tool. For showing the data, another dataset need to be used. 
    df_to_find_partner = df_gi[['InitName','priority_groups_gi_concat','saa_p_systems_gi_concat','action_clusters_gi_concat']]

    # df_pledge.columns

    df_to_find_pledge = df_pledge[['InitName','hazards_all_pledge_concat','p_benefic_pledge_concat',]]
    df_to_find_countries = df_m_countries_filter_partner_finder
    df_to_find_partner = pd.merge(df_to_find_partner, df_to_find_pledge, on='InitName', how='outer')
    df_to_find_partner = pd.merge(df_to_find_partner,df_to_find_countries, on='InitName', how='outer')
    df_to_find_partner = pd.merge(df_to_find_partner, df_partners_name[['InitName','Org_Type']], on='InitName', how='inner')

    return df_to_find_partner
df_to_find_partner = df_to_partner_finder()
# df_to_find_partner

#DATA SET FOR PARTNER TRACKER 
def df_partner_campaign_tracker():

    #Making dataset summary: df_partner_campaign

    # Set 'enddate_gi' to NaN where 'gi_completeness_idx' equals 0
    df_gi.loc[df_gi['gi_completeness_idx'] == 0, 'enddate_gi'] = pd.NaT
    df_pledge.loc[df_pledge['pledge_completeness_idx'] == 0, 'enddate_pledge'] = pd.NaT
    # df_2023_plan_summary_by_partner.loc[pd.isna(df_2023_plan_summary_by_partner['OverallPlanConsolidated']), 'enddate_plan'] = np.nan


    #Setting Date to String
    df_gi['gi_last_entry_date'] = df_gi['enddate_gi'].dt.strftime('%Y-%m-%d')
    df_pledge['pledge_last_entry_date'] = df_pledge['enddate_pledge'].dt.strftime('%Y-%m-%d')


    gi_list = [
    'InitName',
    'gi_last_entry_date',
    'n_members_official',
    'gi_completeness_idx',
    'gi_confidence_members_overall_idx',
    'gi_overall_status',
    'gi_action_required',
    'confidence_members_overall_gi_status',
    'gi_completeness_status',
    'gi_completeness_req_priority_recode',]

    Pledge_list = [
    'InitName',
    'pledge_last_entry_date',
    'individuals_n_total_pledge_2023',
    'pledge_completeness_idx',
    'pledge_confidence_overall_idx',
    'pledge_overall_status',
    'pledge_action_required',
    'confidence_pledge_overall_status',
    'pledge_completeness_status',
    'pledge_completeness_req_priority_recoded',
    ]

    Plan_list = [
    'InitName',
    'enddate_all_plans',
    'number_of_plans',
    'individuals_n_total_all_plans_2023_sum',
    'all_plans_completeness_idx_mean',
    'all_plans_confidence_idx_mean',
    'all_plan_overall_status',
    'all_plans_action_required',
    'all_plans_completeness_req_priority_recoded',]
    # 'all_countries_all_plans',]
    # 'OverallPlanConsolidated_2',]

    # Merge df_partners_name with df_gi on 'InitName'
    df_partner_campaign = df_partners_name[['InitName','Master ID','Org_Type']].merge(df_gi[gi_list], on='InitName', how='left')

    # Merge the resulting dataframe with df_pledge on 'InitName'
    df_partner_campaign = df_partner_campaign.merge(df_pledge[Pledge_list], on='InitName', how='left')

    # Merge the resulting dataframe with df_2023_plan_summary_by_partner on 'InitName'
    df_partner_campaign = df_partner_campaign.merge(df_2023_plan_summary_by_partner[Plan_list], on='InitName', how='left')

    # List of columns to update
    columns_to_update = ['gi_completeness_idx', 'pledge_completeness_idx', 'number_of_plans', 'all_plans_completeness_idx_mean']

    # Replace NaN or null values with 0 in the specified columns
    df_partner_campaign[columns_to_update] = df_partner_campaign[columns_to_update].fillna(0)

    df_partner_campaign.loc[df_partner_campaign['number_of_plans'] == 0, 'all_plans_action_required'] = "Check if plan needs to be submitted already"
    df_partner_campaign.loc[df_partner_campaign['number_of_plans'] == 0, 'all_plans_confidence_idx_mean'] = 0
    df_partner_campaign.loc[df_partner_campaign['number_of_plans'] == 0, 'all_plan_overall_status'] = "No Plan Submitted"
    df_partner_campaign.loc[df_partner_campaign['number_of_plans'] == 0, 'all_plans_completeness_req_priority_recoded'] = "No Plan Information at All"

    gi_info_partner_campaign_text = "#GI (Completeness: " + df_partner_campaign["gi_completeness_idx"].apply(lambda x: f"{x*1:.1f}%")+" Confidence: "+df_partner_campaign["gi_confidence_members_overall_idx"].apply(lambda x: f"{x*100:.1f}%")+"): "+df_partner_campaign["gi_overall_status"]
    pledge_info_partner_campaign_text = "#Pledge (Completeness: " + df_partner_campaign["pledge_completeness_idx"].apply(lambda x: f"{x*1:.1f}%")+" Confidence: "+df_partner_campaign["pledge_confidence_overall_idx"].apply(lambda x: f"{x*100:.1f}%")+"): "+df_partner_campaign["pledge_overall_status"]
    plan_info_partner_campaign_text = "#Numbers of Plan: "+ df_partner_campaign["number_of_plans"].astype(int).astype(str) + " (Completeness_mean: " + df_partner_campaign["all_plans_completeness_idx_mean"].apply(lambda x: f"{x*1:.1f}%")+" Confidence_mean: "+df_partner_campaign["all_plans_confidence_idx_mean"].apply(lambda x: f"{x*100:.1f}%")+"): "+df_partner_campaign["all_plan_overall_status"]
    df_partner_campaign["reporting_cycle_status"] = gi_info_partner_campaign_text+"; "+pledge_info_partner_campaign_text+"; "+plan_info_partner_campaign_text
    df_partner_campaign["reporting_cycle_status"] = df_partner_campaign["reporting_cycle_status"].str.replace(": Completeness: ", ": ", regex=False)

    # df_partner_campaign["reporting_cycle_status"]

    df_partner_campaign_order_list = [
        "Master ID",
        "InitName",    
        "Org_Type",
        'n_members_official',
        "reporting_cycle_status",
        "gi_last_entry_date",
        "gi_completeness_idx",
        "gi_confidence_members_overall_idx",
        "gi_overall_status",
        "gi_action_required",
        "confidence_members_overall_gi_status",
        "gi_completeness_status",
        "gi_completeness_req_priority_recode",
        "pledge_last_entry_date",
        'individuals_n_total_pledge_2023',
        "pledge_completeness_idx",
        "pledge_confidence_overall_idx",
        "pledge_overall_status",
        "pledge_action_required",
        "confidence_pledge_overall_status",
        "pledge_completeness_status",
        "pledge_completeness_req_priority_recoded",
        "enddate_all_plans",
        "number_of_plans",
        'individuals_n_total_all_plans_2023_sum',
        "all_plans_completeness_idx_mean",
        "all_plans_confidence_idx_mean",
        "all_plan_overall_status",
        "all_plans_action_required",
        "all_plans_completeness_req_priority_recoded",
    ]
    df_partner_campaign = df_partner_campaign[df_partner_campaign_order_list]

    return df_partner_campaign
df_partner_campaign = df_partner_campaign_tracker()

#DATA SET FOR PARTNER FINDER
def df_to_partner_summary_dataexplorer():
    list_variables = ['InitName','country_region_all','country_subregion_all','all_countries']
    df_m_countries_filter_partner_finder = df_m_countries[df_m_countries['source'] == 'All Tools (Pledge & Plan)'][list_variables]

    # Making one database to plot in Partner Finder. It has the structere needed for the selection tool. For showing the data, another dataset need to be used. 
    # df_to_find_gi = df_gi[['InitName','Org_Type','description_general','website','n_members_official','saa_p_systems_gi_concat']]
    df_to_find_gi = df_gi[['InitName','Org_Type','description_general','website','saa_p_systems_gi_concat']]
    df_to_find_pledge_individuals = df_pledge[['InitName','p_benefic_pledge_concat','individuals_n_total_pledge_2023']]
    df_to_find_plan_individuals = df_2023_plan_summary_by_partner[['InitName','individuals_n_total_all_plans_2023_sum','number_of_plans','all_plans_name',]]
    df_to_find_pledge_nat_systems = df_pledge[['InitName','natsyst_n_hect_pledge_2023']]
    df_to_find_plan_nat_systems = df_2023_plan_summary_by_partner[['InitName','natsyst_n_hect_all_plans_2023_sum','money_expected_mobilized_sum']]
    df_to_find_countries = df_m_countries_filter_partner_finder
    
    df_to_find_partner = pd.merge(df_to_find_gi, df_to_find_pledge_individuals, on='InitName', how='outer')
    df_to_find_partner = pd.merge(df_to_find_partner,df_to_find_plan_individuals, on='InitName', how='outer')
    df_to_find_partner = pd.merge(df_to_find_partner,df_to_find_pledge_nat_systems, on='InitName', how='outer')
    df_to_find_partner = pd.merge(df_to_find_partner,df_to_find_plan_nat_systems, on='InitName', how='outer')
    
    df_to_find_partner = pd.merge(df_to_find_partner,df_to_find_countries, on='InitName', how='outer')
    df_all_partners_summary = pd.merge(df_to_find_partner, df_partners_name[['InitName',]], on='InitName', how='inner')
    
    #CLEANING TEXT
    def replace_semicolon_in_dataframe(df):
        for col in df.select_dtypes(include='object'):  # Select string columns
            df[col] = df[col].str.replace(";", "; ")
        return df
    df_all_partners_summary = replace_semicolon_in_dataframe(df_all_partners_summary)
    
    def clean_semicolons_in_dataframe(df):
        for col in df.select_dtypes(include='object'):
            # Remove leading and trailing semicolons and replace multiple consecutive semicolons with a single semicolon
            df[col] = df[col].str.replace(r"(;+\s*)+", "; ", regex=True).str.strip("; ")
            
            # Replace cells containing only semicolons with an empty string
            df[col] = df[col].replace(";", "")
            
        return df
    df_all_partners_summary = clean_semicolons_in_dataframe(df_all_partners_summary)
        
    # def make_links_clickable(df, column_name):     
    #     df[column_name] = df[column_name].apply(lambda x: f'<a href="{x if x.startswith("http") else "http://" + x}" target="_blank">{x}</a>' if pd.notnull(x) else x)
    #     return df  
    # df_all_partners_summary = make_links_clickable(df_all_partners_summary, 'website')


    rename_list = {
    "InitName": "Partner Name",
    "Org_Type": "Reporting Status",
    "description_general": "Description",
    "website": "Website",
    "n_members_official": "Members",
    "saa_p_systems_gi_concat": "SAA Priority Systems",
    "p_benefic_pledge_concat": "Primary Beneficiaries (Pledge)",
    "individuals_n_total_pledge_2023": "Individuals Pledged",
    "individuals_n_total_all_plans_2023_sum": "Individuals Planned",
    "number_of_plans": "Total Plans Submitted",
    "all_plans_name": "Plan Names",
    "natsyst_n_hect_pledge_2023": "Hectares Natural Systems (Pledge)",
    "natsyst_n_hect_all_plans_2023_sum": "Hectares Natural Systems (Plan)",
    "money_expected_mobilized_sum": "USD Finance Planned",
    "country_region_all": "Region",
    "country_subregion_all": "Subregion",
    "all_countries": "Countries",
    }

    df_all_partners_summary = df_all_partners_summary.rename(columns=rename_list)

    return df_all_partners_summary

df_all_partners_summary = df_to_partner_summary_dataexplorer()

st.write(df_all_partners_summary)



# col1, col2, col3 = st.columns(3)

# with col1:
#     st.write("GI")
#     df_gi.columns

# with col2:
#     st.write("PLEDGE")
#     df_pledge_summary.columns

# with col3:
#     st.write("PLAN")
#     df_2023_plan_summary_by_partner.columns

# st.write("SUMMARY")
# st.table(df_all_partners_summary)

# # df_all_partners_summary.columns













# # DOWNLOAD ESPECIFIC DATA SET IN EXCEL BUTTOMS
def download_all_tables_excel():

    def to_excel_multiple_sheets(dataframes, sheet_names):
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            for df, sheet_name in zip(dataframes, sheet_names):
                df.to_excel(writer, index=False, sheet_name=sheet_name)
                workbook = writer.book
                worksheet = writer.sheets[sheet_name]

                cell_format = workbook.add_format({'border': 1})
                header_format = workbook.add_format({'border': 1, 'bg_color': 'DCE3E5', 'bold': True})

                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num, value, header_format)
                    worksheet.set_column(col_num, col_num, max(len(value), 10))

                    for row_num, cell_value in enumerate(df[value], start=1):
                        if pd.isna(cell_value) or cell_value == float('inf') or cell_value == float('-inf'):
                            cell_value = ''
                        worksheet.write(row_num, col_num, cell_value, cell_format)

        return output.getvalue()

    # Prepare your dataframes and sheet names
    dataframes = [readme, df_partner_campaign, df_gaps_all, df_gi_summary, df_pledge_summary, df_2023_plan_summary_by_partner, df_2023_plan_summary, df_gi, df_pledge, df_2023_plan]  # Replace with your actual dataframes
    sheet_names = ['readme', 'Report Tracking','df_gaps_all', 'df_gi_summary', 'df_pledge_summary', 'all_plans_by_partners', 'df_2023_plan_summary', 'df_gi', 'df_pledge', 'df_2023_plan_all_info']  # Match these names with your dataframes

    # Get the current date and time, formatted as a string
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H%M%S")

    # Use the function to create an Excel file with a dynamically generated name
    file_name = f"metrics_rtr_gaps_and_responses_{current_datetime}.xlsx"
    excel_data = to_excel_multiple_sheets(dataframes, sheet_names)

    # Create a download button in Streamlit
    st.download_button(label='Download Excel File',
                    data=excel_data,
                    file_name=file_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
download_all_tables_excel()





