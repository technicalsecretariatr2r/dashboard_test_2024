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
from numerize.numerize import numerize
from datetime import datetime


#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
# PAGE structure
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________


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


#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________
# Export Data & Filtering to only Partners*
#__________________________________________________________________________________________________________________________________________________________________
#__________________________________________________________________________________________________________________________________________________________________


#ADMINISTRATIVE
@st.cache_data
def load_data_df_partners_name():
    from etl_process import df_partners_name
    return df_partners_name

@st.cache_data
def load_data_geo_info():
    from etl_process import df_country 
    return df_country 


#Data Geo Country
@st.cache_resource
def load_countries():
        political_countries_url = "http://geojson.xyz/naturalearth-3.3.0/ne_50m_admin_0_countries.geojson"
        return political_countries_url
political_countries_url = load_countries()


#Countries Individuals Data Pledge Plan
@st.cache_data
def load_data_cleaned_df_ind_countries_pledge_plan():
    from etl_process import df_ind_countries_pledge_plan
    return df_ind_countries_pledge_plan

#GI 
@st.cache_data
def load_data_cleaned_df_gi():
    from etl_process import df_gi
    return df_gi

@st.cache_data
def load_data_cleaned_df_gi_summary():
    from etl_process import df_gi_summary
    return df_gi_summary


@st.cache_data
def load_data_cleaned_formatted_date_gi():
    from etl_process import formatted_date_gi
    return formatted_date_gi


#PLEDGE
@st.cache_data
def load_data_cleaned_df_pledge():
    from etl_process import df_pledge
    return df_pledge

@st.cache_data
def load_data_cleaned_df_pledge_summary():
    from etl_process import df_pledge_summary
    return df_pledge_summary

@st.cache_data
def load_data_cleaned_formatted_date_pledge():
    from etl_process import formatted_date_pledge
    return formatted_date_pledge

@st.cache_data
def load_df_pledge_summary_no_filtered():
    from etl_process import df_pledge_summary
    return df_pledge_summary


#PLAN 
@st.cache_data
def load_data_cleaned_df_2023_plan():
    from etl_process import df_2023_plan
    return df_2023_plan

@st.cache_data
def load_data_cleaned_df_2023_plan_summary():
    from etl_process import df_2023_plan_summary
    return df_2023_plan_summary

@st.cache_data
def load_data_cleaned_formatted_date_plan():
    from etl_process import formatted_date_plan
    return formatted_date_plan


#PLANs BY PARTNERS
@st.cache_data 
def load_data_plan_by_partners():
    from etl_process import df_2023_plan_summary_by_partner
    return df_2023_plan_summary_by_partner

#PLAN 2022
@st.cache_data 
def load_data_plan_2022():
    from etl_process import df_2022_plan
    return df_2022_plan

#GAPS
@st.cache_data 
def load_data_gaps():
    from etl_process import df_gaps_all
    return df_gaps_all

# #HAZARDS_PLEDGE AND PLAN 
@st.cache_data 
def load_data_df_hazards_pledge_plan_vertical():
    from etl_process import df_hazards_pledge_plan_vertical
    return df_hazards_pledge_plan_vertical

@st.cache_data 
def summary_partner_tracking_table():
    from etl_process import df_partner_campaign
    return df_partner_campaign

@st.cache_data 
def data_rtr_partners():
    from etl_process import df_all_partners_summary
    return df_all_partners_summary


## Calling the funcions and creating datasets

df_all_partners_summary = data_rtr_partners()

df_partner_campaign_tracker = summary_partner_tracking_table()

df_hazards_pledge_plan_vertical = load_data_df_hazards_pledge_plan_vertical()
df_ind_countries_pledge_plan = load_data_cleaned_df_ind_countries_pledge_plan()
df_country =        load_data_geo_info()
df_partners_name =  load_data_df_partners_name()

df_gi =             load_data_cleaned_df_gi()
df_gi_summary =     load_data_cleaned_df_gi_summary()
formatted_date_gi = load_data_cleaned_formatted_date_gi()

df_pledge =         load_data_cleaned_df_pledge()
df_pledge_summary = load_data_cleaned_df_pledge_summary()
formatted_date_pledge = load_data_cleaned_formatted_date_pledge()

df_2023_plan =           load_data_cleaned_df_2023_plan()
df_2023_plan_summary =   load_data_cleaned_df_2023_plan_summary()
df_2023_plan_summary_by_partner =   load_data_plan_by_partners()
formatted_date_plan = load_data_cleaned_formatted_date_gi()

df_gaps_all =  load_data_gaps()
df_pledge_summary_no_filtered = load_df_pledge_summary_no_filtered()
df_2022_plan = load_data_plan_2022()



##FIlter Type
df_all_partners_summary = df_all_partners_summary[df_all_partners_summary['Reporting Status'].isin(['Reporting Partner', 'New Partner'])]
df_partner_campaign_tracker = df_partner_campaign_tracker[df_partner_campaign_tracker['Org_Type'].isin(['Reporting Partner', 'New Partner'])]
df_gi = df_gi[df_gi['Org_Type'] == 'Reporting Partner']
df_gi_summary = df_gi_summary[df_gi_summary['Org_Type'] == 'Reporting Partner']
df_pledge = df_pledge[df_pledge['Org_Type'] == 'Reporting Partner']
df_pledge_summary = df_pledge_summary[df_pledge_summary['Org_Type'] == 'Reporting Partner']
df_2023_plan = df_2023_plan[df_2023_plan['Org_Type'] == 'Reporting Partner']
df_2023_plan_summary = df_2023_plan_summary[df_2023_plan_summary['Org_Type'] == 'Reporting Partner']
df_2023_plan_summary_by_partner = df_2023_plan_summary_by_partner[df_2023_plan_summary_by_partner['Org_Type'] == 'Reporting Partner']
df_gaps_all = df_gaps_all[df_gaps_all['Org_Type'] == 'Reporting Partner']


#### Magnitud Metrics Calculations
def calculate_campaign_metrics(df_partners_name, df_gi_summary, df_pledge_summary, df_pledge_summary_no_filtered, df_2023_plan):
    ## caculating diferences between two years and two years 
    def calculate_percentage_change(old_value, new_value):
        if old_value == 0:
            raise ValueError("The old value cannot be zero for percentage calculation")
        percentage_change = ((new_value - old_value) / old_value) * 100
        return percentage_change
      
    
    ############################
    ############################
    rtr_goal_individuals = 4000000000 

    ############################
    ############################
    ## REPORTING DATA
    #2022
    n_all_rtrpartners_2022_cop27 = 34 
    reporting_partners_in_2022_cop27 = n_all_rtrpartners_2022_cop27 ## ALL Partners were Reporting Parters in 2022. Not all of them reported the tools
    no_reporting_partners_in_2022_cop27 = 0  #New Parters
    n_rtrmember_exp_in_2022_cop27 = 0
    

    #2023
    n_all_rtrpartners_cop28 = 34 
    reporting_partners_in_2023_cop28 = 29
    no_reporting_partner_2023_cop28 = 5 #New Parters
    n_rtrmember_exp_in_2023_cop28 = 1

    #2024  #This Updates every new year that is why these variables are do not longer have a year in their name.
    n_all_rtrpartners = ((df_partners_name["Org_Type"] == "Reporting Partner") | (df_partners_name["Org_Type"] == "New Partner ")).sum()  
    n_reporting_partners = (df_partners_name["Org_Type"] == "Reporting Partner").sum()  ## THIS VARIABLE IS USED AS 100%. OTHERS PARTNERS HAVE NOT STARTED REPORTING PROCESS
    n_newpartners = n_all_rtrpartners - n_reporting_partners
    n_rtrmember_exp = (df_partners_name["Org_Type"] == "Member").sum()
    n_rtrnotpartner = (df_partners_name["Org_Type"] == "No Apply").sum()
    n_reporting_partners_2024 = n_reporting_partners
 

    # Interyears differences - #Change N Parnters through years. 
    percentage_increase_number_partnes_all_campaign_22_23 = round(calculate_percentage_change(n_all_rtrpartners_2022_cop27, n_all_rtrpartners_cop28))
    percentage_increase_number_partnes_all_campaign_23_24 = round(calculate_percentage_change(n_all_rtrpartners_cop28, n_all_rtrpartners))
    percentage_increase_number_partnes_all_campaign_22_24 = round(calculate_percentage_change(n_all_rtrpartners_2022_cop27, n_all_rtrpartners))
    # percentage_increase_number_partnes_all_campaign_22_23
    # percentage_increase_number_partnes_all_campaign_23_24
    # percentage_increase_number_partnes_all_campaign_22_24


    ####
    ####
    #### APPLY: GENERAL INFORMATION LEVEL OF CAMPAIGN (GI)
    ####
    ####

    #2022
    #Partner Level
    n_partner_gi_in_2022 = 26
    n_member_gi_in_2022  = 0
    n_initiatives_gi_pending_2022 = n_all_rtrpartners_2022_cop27 -  n_partner_gi_in_2022
    #Partner' Member level 
    Members_organizations_22 = 2085 ##Info Data Explorer 2022
    Members_organizations_22_n_partners = 23 ##Info Data Explorer 2022
    reporting_partners_in_2022 = n_partner_gi_in_2022

    #2023
    #Partner Level
    n_partner_gi_in_2023 = 28
    n_member_gi_in_2023  = 1
    n_initiatives_gi_pending_2023 = reporting_partners_in_2023_cop28 -  n_partner_gi_in_2023
    #Partner' Member level 
    Members_organizations_23 = 687 
    Members_organizations_23_n_partners = 17
    
    reporting_partners_in_2023 = n_partner_gi_in_2023
    

    #2024
    #Partner Level
    n_partner_gi = df_gi_summary[(df_gi_summary["Org_Type"] == "Reporting Partner") & (df_gi_summary["gi_completeness_idx"] > 0)].shape[0]
    n_member_gi = df_gi_summary[(df_gi_summary["Org_Type"] == "Member") & (df_gi_summary["gi_completeness_idx"] > 0)].shape[0]
    n_initiatives_gi_pending = df_gi_summary[((df_gi_summary["Org_Type"] == "Reporting Partner") | (df_gi_summary["Org_Type"] == "Member")) & (df_gi_summary["gi_completeness_idx"] == 0)].shape[0]
    #Partner' Member level 
    Members_organizations_24 = (df_gi_summary["n_members_official"]).sum()
    Members_organizations_24_n_partners = df_gi_summary[df_gi_summary["n_members_official"] > 0].shape[0]

    n_member_gi_2024 = Members_organizations_24
    n_partner_gi_2024 = n_partner_gi
    n_initiatives_gi_pending_2024 = n_initiatives_gi_pending
    
   
    
    ####
    #### PLEDGE STATEMENT: GENERAL INFORMATION LEVEL OF CAMPAIGN
    ####

    #2022
    n_partner_pledge_in_2022 = 23
    n_member_pledge_in_2022  = 0
    n_initiatives_pledge_pending_in_2022 = reporting_partners_in_2022_cop27 -  n_partner_pledge_in_2022

    n_individuals_pledge_in_2022 =   3077665668 
    n_individuals_pledge_in_2022_n_partners = 17

    n_hectares_pledge_in_2022 = 59835000
    n_hectares_pledge_in_2022_n_partners = 3
    

    #2023
    n_partner_pledge_in_2023 = 28
    n_member_pledge_in_2023  = 1
    n_initiatives_pledge_pending_in_2023 = reporting_partners_in_2023_cop28 -  n_partner_pledge_in_2023

    n_individuals_pledge_in_2023 = 3166185040  #Calculated
    n_individuals_pledge_in_2023_n_partners = 20

    n_hectares_pledge_in_2023 = 59835000
    n_hectares_pledge_in_2023_n_partners = 3

    # #Pendings
    # partners_report_pledge_d_individuals_in_2023 =0
    # partners_repor_pledge_companies_in_2023 = 0
    # partners_repor_pledge_regions_in_2023 = 0
    # partners_repor_pledge_cities_in_2023 = 0
    # partners_repor_pledge_nat_syst_in_2023 = 0


    #2024
    n_partner_pledge    = df_pledge_summary[(df_pledge_summary["Org_Type"] == "Reporting Partner") & (df_pledge_summary["pledge_completeness_idx"] > 0)].shape[0]
    n_member_pledge     = df_pledge_summary[(df_pledge_summary["Org_Type"] == "Member") & (df_pledge_summary["pledge_completeness_idx"] > 0)].shape[0]
    n_initiatives_pledge_pending = n_reporting_partners - n_partner_pledge
    percentaje_reporting_partner_pledge = round((n_partner_pledge / n_reporting_partners)*100)

    n_individuals_pledge_in_2024 =   3261469152
    n_individuals_pledge_in_2024_n_partners = 23
    

    n_hectareas_pledge = df_pledge_summary['natsyst_n_hect_pledge_2023'].sum()
    n_hectareas_pledge_adj = round(df_pledge_summary['natsyst_n_hect_pledge_2023'].sum() * 0.75)
    n_hectareas_pledge_n_partners = df_pledge_summary[df_pledge_summary['natsyst_n_hect_pledge_2023'].notna() & (df_pledge_summary['natsyst_n_hect_pledge_2023'] != 0)]['natsyst_n_hect_pledge_2023'].shape[0]

    partners_report_pledge_d_individuals = df_pledge_summary['d_indiv_pledge'].notna().sum()
    partners_repor_pledge_companies = df_pledge_summary['companies_pledge'].notna().sum()
    partners_repor_pledge_regions = df_pledge_summary['region_pledge'].notna().sum()
    partners_repor_pledge_cities = df_pledge_summary['cities_pledge'].notna().sum()
    partners_repor_pledge_nat_syst = df_pledge_summary['natsyst_pledge'].notna().sum()

    n_direct_individuals_pledge = df_pledge_summary['d_indiv_number_pledge_2023'].sum()*0.75
    n_partners_reportingnumberof_direct_individuals_pledge = df_pledge_summary[df_pledge_summary['d_indiv_number_pledge_2023'].notna() & (df_pledge_summary['d_indiv_number_pledge_2023'] != 0)]['d_indiv_number_pledge_2023'].shape[0]

    n_indiv_companies_pledge = df_pledge_summary['companies_n_indiv_pledge_2023'].sum()*0.75
    n_partners_reportingnumberofindiv_companies_pledge = df_pledge_summary[df_pledge_summary['companies_n_indiv_pledge_2023'].notna() & (df_pledge_summary['companies_n_indiv_pledge_2023'] != 0)]['companies_n_indiv_pledge_2023'].shape[0]

    n_indiv_regions_pledge = df_pledge_summary['region_n_indiv_pledge_2023'].sum()*0.75
    n_partners_reportingnumberofindiv_regions_pledge = df_pledge_summary[df_pledge_summary['region_n_indiv_pledge_2023'].notna() & (df_pledge_summary['region_n_indiv_pledge_2023'] != 0)]['region_n_indiv_pledge_2023'].shape[0]

    n_indiv_cities_pledge = df_pledge_summary['cities_n_indiv_pledge_2023'].sum()*0.75
    n_partners_reportingnumberofindiv_cities_pledge = df_pledge_summary[df_pledge_summary['cities_n_indiv_pledge_2023'].notna() & (df_pledge_summary['cities_n_indiv_pledge_2023'] != 0)]['cities_n_indiv_pledge_2023'].shape[0]

    n_indiv_natsyt_pledge = df_pledge_summary_no_filtered['natsyst_n_individuals_pledge_status'].sum()*0.75
    n_partners_reportingnumberofindiv_natsyst2023 = df_pledge_summary[df_pledge_summary_no_filtered['natsyst_n_individuals_pledge_status'].notna() & (df_pledge_summary_no_filtered['natsyst_n_individuals_pledge_status'] != 0)]['natsyst_n_individuals_pledge_status'].shape[0]

    # oficial number of individuals here
    # total_numbers_individuals_2023 = n_direct_individuals_pledge + n_indiv_companies_pledge + n_indiv_regions_pledge + n_indiv_cities_pledge + n_indiv_natsyt_pledge

    # counting numbers of beneficiaries (pledge)
    Comps2022Num_pledge = df_pledge_summary_no_filtered['companies_n_comp_pledge_2022'].sum()
    Comps2022Num_pledge_adj = df_pledge_summary_no_filtered['companies_n_comp_pledge_2022'].sum()*0.75
    n_partners_reportingnumberofcompanies2022_pledge = df_pledge_summary_no_filtered[df_pledge_summary_no_filtered['companies_n_comp_pledge_2022'].notna() & (df_pledge_summary_no_filtered['companies_n_comp_pledge_2022'] != 0)]['companies_n_comp_pledge_2022'].shape[0]
    Comps2023Num_pledge = df_pledge_summary['companies_n_comp_pledge_2023'].sum()
    Comps2023Num_pledge_adj = round(df_pledge_summary['companies_n_comp_pledge_2023'].sum() * 0.75)
    n_partners_reportingnumberofcompanies2023_pledge = df_pledge_summary[df_pledge_summary['companies_n_comp_pledge_2023'].notna() & (df_pledge_summary['companies_n_comp_pledge_2023'] != 0)]['companies_n_comp_pledge_2023'].shape[0]
    # ## Confirmation
    # st.write('Companies 2024',Comps2023Num_pledge_adj,n_partners_reportingnumberofcompanies2023_pledge)
    # df_pledge_summary[['InitName','companies_n_comp_pledge_2023']]

    Regs2022Nums_pledge = df_pledge_summary_no_filtered['region_n_reg_pledge_2022'].sum()
    Regs2022Nums_pledge_adj = df_pledge_summary_no_filtered['region_n_reg_pledge_2022'].sum()*0.75
    n_partners_reportingnumberofregions2022_pledge = df_pledge_summary_no_filtered[df_pledge_summary_no_filtered['region_n_reg_pledge_2022'].notna() & (df_pledge_summary_no_filtered['region_n_reg_pledge_2022'] != 0)]['region_n_reg_pledge_2022'].shape[0]
    Regs2023Nums_pledge = df_pledge_summary['region_n_reg_pledge_2023'].sum()
    # Regs2023Nums_pledge_adj = df_pledge_summary['region_n_reg_pledge_2023'].sum()*0.75
    Regs2023Nums_pledge_adj = round(df_pledge_summary['region_n_reg_pledge_2023'].sum() * 0.75)
    n_regions_regions4 = 100   #Adjusted 
    n_partners_reportingnumberofregions2023_pledge = df_pledge_summary[df_pledge_summary['region_n_reg_pledge_2023'].notna() & (df_pledge_summary['region_n_reg_pledge_2023'] != 0)]['region_n_reg_pledge_2023'].shape[0]
    # ## Confirmation
    # st.write("n regions pledge 2024")
    # df_pledge_summary[['InitName','region_n_reg_pledge_2023','Org_Type']]

    Cities2022Num_pledge = df_pledge_summary_no_filtered['cities_n_cit_pledge_2022'].sum()
    Cities2022Num_pledge_adj = df_pledge_summary_no_filtered['cities_n_cit_pledge_2022'].sum()*0.75
    n_partners_reportingnumberofcities2022_pledge = df_pledge_summary_no_filtered[df_pledge_summary_no_filtered['cities_n_cit_pledge_2022'].notna() & (df_pledge_summary_no_filtered['cities_n_cit_pledge_2022'] != 0)]['cities_n_cit_pledge_2022'].shape[0]
    Cities2023Num_pledge = df_pledge_summary['cities_n_cit_pledge_2023'].sum()
    # Cities2023Num_pledge_adj = df_pledge_summary['cities_n_cit_pledge_2023'].sum()*0.75
    Cities2023Num_pledge_adj = round(df_pledge_summary['cities_n_cit_pledge_2023'].sum() * 0.75)
    n_cities_citiesrtr = 86 #Adjusted 
    n_partners_reportingnumberofcities2023_pledge = df_pledge_summary[df_pledge_summary['cities_n_cit_pledge_2023'].notna() & (df_pledge_summary['cities_n_cit_pledge_2023'] != 0)]['cities_n_cit_pledge_2023'].shape[0]
    # ##Confirmation
    # st.write("n Cities 2024")
    # df_pledge_summary[['InitName','cities_n_cit_pledge_2023']]

    NatSysHectaTotal2022_pledge = df_pledge_summary_no_filtered['natsyst_n_hect_pledge_2022'].sum()
    NatSysHectaTotal2022_pledge_adj = df_pledge_summary_no_filtered['natsyst_n_hect_pledge_2022'].sum()*0.75
    n_partners_reportingnumberofnaturalsyst2022_pledge = df_pledge_summary_no_filtered[df_pledge_summary_no_filtered['natsyst_n_hect_pledge_2022'].notna() & (df_pledge_summary_no_filtered['natsyst_n_hect_pledge_2022'] != 0)]['natsyst_n_hect_pledge_2022'].shape[0]

    # n_hectareas_pledge = df_pledge_summary['natsyst_n_hect_pledge_2023'].sum()
    # # n_hectareas_pledge_adj = df_pledge_summary['natsyst_n_hect_pledge_2023'].sum()*0.75

    # n_hectareas_pledge_adj = round(df_pledge_summary['natsyst_n_hect_pledge_2023'].sum() * 0.75)
    # n_hectareas_pledge_n_partners = df_pledge_summary[df_pledge_summary['natsyst_n_hect_pledge_2023'].notna() & (df_pledge_summary['natsyst_n_hect_pledge_2023'] != 0)]['natsyst_n_hect_pledge_2023'].shape[0]

    # ##Confirmation
    # st.write("n NAtu Systes 2024")
    # df_pledge_summary[['InitName','natsyst_n_hect_pledge_2023']]
    # st.write('n_hectareas_pledge_adj',n_hectareas_pledge_adj,n_hectareas_pledge_n_partners)

    # percentage_increase_resilience_hectares_pledge = round(calculate_percentage_change(NatSysHectaTotal2022_pledge_adj, n_hectareas_pledge_adj))
    # percentage_increase_resilience_individuals_pledge_22_23 = round(calculate_percentage_change(n_individuals_pledge_in_2022, n_individuals_pledge_in_2023))
    percentage_increase_resilience_individuals_pledge_23_24 =  round(calculate_percentage_change(n_individuals_pledge_in_2023,n_individuals_pledge_in_2024))

    # st.write('percentage_increase_resilience_individuals_pledge_23_24',percentage_increase_resilience_individuals_pledge_23_24)

    # percentage_increase_n_plan2022vs2023 = round(calculate_percentage_change(n_plans_in_2022, n_total_plans_consolidated ))
    # percentage_increase_n_partners_with_plan2022vs2023 = round(calculate_percentage_change(n_partners_reporting_plan_in_2022, n_partners_plan))

    # ## Comparation Pledge vs Plan
    # percentaje_individuals_pledge_vs_plan = round((n_individuals_plan_consolidated/n_individuals_pledge_in_2023 )*100)
    # percentaje_hectareas_nat_syst_pledge_vs_plan = round((n_hectareas_plan_consolidated/n_hectareas_pledge_adj )*100)
    # percentaje_countries_pledge_vs_plan = round((n_countries_plan_consolidated/df_pledge_unique_countries.shape[0])*100)

    
    ####
    ####
    ####
    #### PLAN SUBMISION: PLAN SUBMISION:
    ####
    ####
    ####

    #PLAN 2022  #NO INFO REPORTED ABOUT PLAN IN 2022
    #General Info Reporting Partners
    n_partners_plan_in_2022 = 0
    n_members_plan_in_2022 = 0
    n_total_plans_consolidated_in_2022 = 0

    #Individuals
    n_individuals_plan_consolidated_in_2022 = 0
    n_individuals_plan_consolidated_in_2022_n_partners = 0

    #Fundings
    dollars_movilized_all_plans_in_2022 = 0
    dollars_mobilized_all_plans_n_plans_in_2022 = 0
    dollars_mobilized_all_plans_n_partners_in_2022 = 0

    #Hectares
    n_hectares_plan_in_2022 = 0
    n_hectares_plan_in_2022_n_partners = 0 

    #PLAN 2023
    #General Info Reporting Partners
    n_partners_plan_in_2023 =  21
    n_members_plan_in_2023 = 0
    n_total_plans_consolidated_in_2023 = 25

    #Individuals
    n_individuals_plan_consolidated_in_2023 = 1869492849 
    n_individuals_plan_consolidated_in_2023_n_partners = 17

    #Fundings
    dollars_movilized_all_plans_in_2023 =  39436683725 
    dollars_mobilized_all_plans_n_plans_in_2023 = 17
    dollars_mobilized_all_plans_n_partners_in_2023 = 15

    # n_hectares
    n_hectares_plan_in_2023 = 5482500
    n_hectares_plan_in_2023_n_partners = 2
    
    
    #PLAN 2024
    #General Info Reporting Partners
    n_partners_plan = df_2023_plan[(df_2023_plan["Org_Type"] == "Reporting Partner")]["InitName"].nunique()
    n_members_plan = df_2023_plan[(df_2023_plan["Org_Type"] == "Member")]["InitName"].nunique()
    n_total_plans_consolidated = df_2023_plan.shape[0]
    percentaje_reporting_partner_plan_consolidated = round((n_partners_plan / n_reporting_partners)*100)
    

    #Individuals Plan
    n_individuals_plan_consolidated = 2023647280 #Given by JC Sept 2023
    # n_individuals_plan_consolidated_n_partners = 19

    n_individuals_all_plans_n_plans = df_2023_plan[df_2023_plan['individuals_n_total_plan_2023'] > 0]['InitName'].count()
    n_individuals_all_plans_n_partners = df_2023_plan[df_2023_plan['individuals_n_total_plan_2023'] > 0]['InitName'].nunique()


    #Fundings
    # df_2023_plan['money_expected_mobilized']
    dollars_movilized_all_plans = df_2023_plan['money_expected_mobilized'].sum()
    dollars_mobilized_all_plans_n_plans = df_2023_plan[df_2023_plan['money_expected_mobilized'] > 0]['InitName'].count()
    dollars_mobilized_all_plans_n_partners = df_2023_plan[df_2023_plan['money_expected_mobilized'] > 0]['InitName'].nunique()
    percentaje_partner_reporting_adaptation_finance_consolidated = round((dollars_mobilized_all_plans_n_partners / n_reporting_partners)*100)

    dollars_in_2023 = dollars_movilized_all_plans_in_2023
    dollars_in_2024 = dollars_movilized_all_plans

    percentage_increase_dollars_plan_2023_2024 = round(calculate_percentage_change(dollars_in_2023, dollars_in_2024), 1)
    # st.write('percentage_increase_dollars_plan_2023_2024',percentage_increase_dollars_plan_2023_2024)
    # st.write('dollars_in_2023',dollars_in_2023)
    # st.write('dollars_in_2024',dollars_in_2024)

    #Number of hectares plan
    n_hectareas_plan_consolidated = round(df_2023_plan['natsyst_n_hect_plan_2023'].sum()*0.75)  ## Same metodology as in pledge number of hectareas
    filtered_df = df_2023_plan[df_2023_plan['natsyst_n_hect_plan_2023'] > 0]
    # filtered_df[['InitName','natsyst_n_hect_plan_2023']]
    n_partners_reporting_n_hectareas_plan_consolidated = filtered_df['InitName'].nunique()
    ## Confirmation
    # n_partners_reporting_n_hectareas_plan_consolidated

    #OTHER VALUES
    ## Getting the numbers of Partners plans in each primary beneficiary (CONSOLIDATED)
    plan_n_individuals_direct = df_2023_plan['d_indiv_plan'].notna().sum()
    plan_n_companies = df_2023_plan['companies_plan'].notna().sum()
    plan_n_regions = df_2023_plan['region_plan'].notna().sum()
    plan_n_cities = df_2023_plan['cities_plan'].notna().sum()
    plan_h_natsyst = df_2023_plan['natsyst_plan'].notna().sum()

    #Number of plans (CONSOLIDATED)
    #GettinG the total number of partners that have any reported metrics in all data_consolidated. PLan 2023 referst to the tool created in that year and is still valid in 2024
    numbers_provid_list = ['d_indiv_number_plan_2023','companies_n_indiv_plan_2023','region_n_indiv_plan_2023','cities_n_indiv_plan_2023','natsyst_n_indiv_plan_2023']
    # Create a condition for non-NA values and non-zero values
    condition = (df_2023_plan[numbers_provid_list].notna()) & (df_2023_plan[numbers_provid_list] != 0)
    # Check if any columns in the row meet the condition and assign the result to 'reportmetrics'
    df_2023_plan['reportmetrics'] = condition.any(axis=1)
    n_individuals_plan_consolidated_n_partners = df_2023_plan[df_2023_plan['reportmetrics'] == True].shape[0]


    ## Plan 2023 only
    # n_partner_plan_only2023 = df_2023_plan_summary[(df_2023_plan_summary["Org_Type"] == "Reporting Partner") & (df_2023_plan_summary["plan_completeness_idx"] > 0)]["InitName"].nunique()
    # n_member_plan_only2023 = df_2023_plan_summary[(df_2023_plan_summary["Org_Type"] == "Member") & (df_2023_plan_summary["plan_completeness_idx"] > 0)]["InitName"].nunique()
    # # n_initiatives_plan2023_pending = (n_reporting_partners + n_rtrmember_exp)-(n_partner_plan_only2023 + n_member_plan_only2023)
    # partner_n_plan_only2023    = df_2023_plan_summary[(df_2023_plan_summary["Org_Type"] == "Reporting Partner") & (df_2023_plan_summary["plan_completeness_idx"] > 0)].shape[0]
    # member_n_plan_only2023     = df_2023_plan_summary[(df_2023_plan_summary["Org_Type"] == "Member") & (df_2023_plan_summary["plan_completeness_idx"] > 0)].shape[0]



     # Return all metrics in a dictionary
    return {
        "rtr_goal_individuals": rtr_goal_individuals,
        "n_all_rtrpartners_2022_cop27": n_all_rtrpartners_2022_cop27,
        "reporting_partners_in_2022_cop27": reporting_partners_in_2022_cop27,
        "no_reporting_partners_in_2022_cop27": no_reporting_partners_in_2022_cop27,
        "n_rtrmember_exp_in_2022_cop27": n_rtrmember_exp_in_2022_cop27,
        "n_all_rtrpartners_cop28": n_all_rtrpartners_cop28,
        "reporting_partners_in_2023_cop28": reporting_partners_in_2023_cop28,
        "n_all_rtrpartners": n_all_rtrpartners,
        "n_reporting_partners": n_reporting_partners,
        "n_newpartners": n_newpartners,
        "n_rtrmember_exp": n_rtrmember_exp,
        "n_rtrnotpartner": n_rtrnotpartner,
        "percentage_increase_number_partnes_all_campaign_22_23": percentage_increase_number_partnes_all_campaign_22_23,
        "percentage_increase_number_partnes_all_campaign_23_24": percentage_increase_number_partnes_all_campaign_23_24,
        "percentage_increase_number_partnes_all_campaign_22_24": percentage_increase_number_partnes_all_campaign_22_24,
        "n_partner_gi": n_partner_gi,
        "n_member_gi": n_member_gi,
        "n_initiatives_gi_pending": n_initiatives_gi_pending,
        "Members_organizations_24": Members_organizations_24,
        "n_partner_pledge": n_partner_pledge,
        "n_member_pledge": n_member_pledge,
        "n_initiatives_pledge_pending": n_initiatives_pledge_pending,
        "n_individuals_pledge_in_2024": n_individuals_pledge_in_2024,
        "percentage_increase_resilience_individuals_pledge_23_24": percentage_increase_resilience_individuals_pledge_23_24,
        "n_hectareas_pledge": n_hectareas_pledge,
        "n_hectareas_pledge_adj": n_hectareas_pledge_adj,
        "n_partners_reporting_n_hectareas_plan_consolidated": n_partners_reporting_n_hectareas_plan_consolidated,
        "n_individuals_plan_consolidated": n_individuals_plan_consolidated,
        "dollars_movilized_all_plans_2024": dollars_movilized_all_plans,
        "percentage_increase_dollars_plan_2023_2024": percentage_increase_dollars_plan_2023_2024,
        "n_individuals_pledge_in_2022": n_individuals_pledge_in_2022,
        'n_individuals_plan_consolidated_in_2022':n_individuals_plan_consolidated_in_2022,
        'n_individuals_pledge_in_2023':n_individuals_pledge_in_2023,
        'n_individuals_plan_consolidated_in_2023':n_individuals_plan_consolidated_in_2023,
        'no_reporting_partner_2023_cop28':no_reporting_partner_2023_cop28,
        'n_rtrmember_exp_in_2023_cop28':n_rtrmember_exp_in_2023_cop28,
        'n_partner_gi_in_2022':n_partner_gi_in_2022,
        'n_member_gi_in_2022':n_member_gi_in_2022,
        'n_member_gi_in_2023':n_member_gi_in_2023,
        'n_partner_gi_in_2023':n_partner_gi_in_2023,
        'n_initiatives_gi_pending_2022':n_initiatives_gi_pending_2022,
        'Members_organizations_22':Members_organizations_22,
        'Members_organizations_22_n_partners':Members_organizations_22_n_partners,
        'n_initiatives_gi_pending_2023':n_initiatives_gi_pending_2023,
        'Members_organizations_23':Members_organizations_23,
        'Members_organizations_23_n_partners':Members_organizations_23_n_partners,
        'Members_organizations_24_n_partners':Members_organizations_24_n_partners,
        'n_reporting_partners_2024':n_reporting_partners_2024,
        'n_member_gi_2024':n_member_gi_2024,
        'n_partner_gi_2024':n_partner_gi_2024,
        'n_initiatives_gi_pending_2024':n_initiatives_gi_pending_2024,
        'reporting_partners_in_2023':reporting_partners_in_2023,
        'reporting_partners_in_2022':reporting_partners_in_2022,
        
        'n_hectares_pledge_in_2022':n_hectares_pledge_in_2022,
        'n_hectares_pledge_in_2022_n_partners':n_hectares_pledge_in_2022_n_partners,
        'n_hectares_pledge_in_2023':n_hectares_pledge_in_2023,
        'n_hectares_pledge_in_2023_n_partners':n_hectares_pledge_in_2023_n_partners,
        'n_hectares_plan_in_2023':n_hectares_plan_in_2023,
        'n_hectares_plan_in_2023_n_partners':n_hectares_plan_in_2023_n_partners,
        'n_hectareas_pledge_n_partners':n_hectareas_pledge_n_partners,
        
        'dollars_movilized_all_plans_in_2023':dollars_movilized_all_plans_in_2023,
        'dollars_movilized_all_plans':dollars_movilized_all_plans,
        'dollars_mobilized_all_plans_n_plans_in_2023':dollars_mobilized_all_plans_n_plans_in_2023,
        'dollars_mobilized_all_plans_n_plans':dollars_mobilized_all_plans_n_plans,
        'dollars_mobilized_all_plans_n_partners_in_2023':dollars_mobilized_all_plans_n_partners_in_2023,
        'dollars_mobilized_all_plans_n_partners':dollars_mobilized_all_plans_n_partners,
        
        'n_hectares_plan_in_2022':n_hectares_plan_in_2022,
        'n_hectareas_plan_consolidated':n_hectareas_plan_consolidated,
        'n_hectares_plan_in_2022_n_partners':n_hectares_plan_in_2022_n_partners,
        
        'n_individuals_pledge_in_2024_n_partners':n_individuals_pledge_in_2024_n_partners,
        'n_total_plans_consolidated':n_total_plans_consolidated,
        'n_individuals_all_plans_n_plans':n_individuals_all_plans_n_plans,
        'n_individuals_all_plans_n_partners':n_individuals_all_plans_n_partners,
        
        'n_partners_plan':n_partners_plan,
    }
    
metrics = calculate_campaign_metrics(df_partners_name, df_gi_summary, df_pledge_summary, df_pledge_summary_no_filtered, df_2023_plan)

#GOAL
rtr_goal_individuals = metrics["rtr_goal_individuals"]
#2022
n_all_rtrpartners_2022_cop27 = metrics["n_all_rtrpartners_2022_cop27"]
reporting_partners_in_2022_cop27 = metrics["reporting_partners_in_2022_cop27"]
no_reporting_partners_in_2022_cop27 = metrics["no_reporting_partners_in_2022_cop27"]
n_rtrmember_exp_in_2022_cop27 = metrics["n_rtrmember_exp_in_2022_cop27"]
n_individuals_pledge_in_2022 = metrics["n_individuals_pledge_in_2022"]
n_individuals_plan_consolidated_in_2022 = metrics["n_individuals_plan_consolidated_in_2022"]
n_member_gi_in_2022 = metrics["n_member_gi_in_2022"]
n_partner_gi_in_2022 = metrics["n_partner_gi_in_2022"]
#2023
n_all_rtrpartners_cop28 = metrics["n_all_rtrpartners_cop28"]
reporting_partners_in_2023_cop28 = metrics["reporting_partners_in_2023_cop28"]
percentage_increase_number_partnes_all_campaign_22_23 = metrics["percentage_increase_number_partnes_all_campaign_22_23"]
percentage_increase_number_partnes_all_campaign_23_24 = metrics["percentage_increase_number_partnes_all_campaign_23_24"]
percentage_increase_number_partnes_all_campaign_22_24 = metrics["percentage_increase_number_partnes_all_campaign_22_24"]
n_individuals_pledge_in_2023 = metrics["n_individuals_pledge_in_2023"]
n_individuals_plan_consolidated_in_2023  = metrics["n_individuals_plan_consolidated_in_2023"]
no_reporting_partner_2023_cop28 = metrics["no_reporting_partner_2023_cop28"]
n_rtrmember_exp_in_2023_cop28 = metrics["n_rtrmember_exp_in_2023_cop28"]
n_member_gi_in_2023 = metrics["n_member_gi_in_2023"]
n_partner_gi_in_2023 = metrics["n_partner_gi_in_2023"]

#2024
n_all_rtrpartners = metrics["n_all_rtrpartners"]
n_reporting_partners = metrics["n_reporting_partners"]
n_newpartners = metrics["n_newpartners"]
n_rtrmember_exp = metrics["n_rtrmember_exp"]
n_rtrnotpartner = metrics["n_rtrnotpartner"]
n_partner_gi = metrics["n_partner_gi"]

n_member_gi = metrics["n_member_gi"]
n_initiatives_gi_pending = metrics["n_initiatives_gi_pending"]
Members_organizations_24 = metrics["Members_organizations_24"]

n_partner_pledge = metrics["n_partner_pledge"]
n_member_pledge = metrics["n_member_pledge"]

n_initiatives_pledge_pending = metrics["n_initiatives_pledge_pending"]
n_individuals_pledge_in_2024 = metrics["n_individuals_pledge_in_2024"]
percentage_increase_resilience_individuals_pledge_23_24 = metrics["percentage_increase_resilience_individuals_pledge_23_24"]

n_hectareas_pledge = metrics["n_hectareas_pledge"]
n_hectareas_pledge_adj = metrics["n_hectareas_pledge_adj"]
n_partners_reporting_n_hectareas_plan_consolidated = metrics["n_partners_reporting_n_hectareas_plan_consolidated"]
n_individuals_plan_consolidated = metrics["n_individuals_plan_consolidated"]
dollars_movilized_all_plans_2024 = metrics["dollars_movilized_all_plans_2024"]
percentage_increase_dollars_plan_2023_2024 = metrics["percentage_increase_dollars_plan_2023_2024"]

n_partners_plan = metrics["n_partners_plan"]

#Other
n_initiatives_gi_pending_2022 = metrics['n_initiatives_gi_pending_2022']
Members_organizations_22 = metrics['Members_organizations_22']
Members_organizations_22_n_partners = metrics['Members_organizations_22_n_partners']
n_initiatives_gi_pending_2023 = metrics['n_initiatives_gi_pending_2023']
Members_organizations_23 = metrics['Members_organizations_23']
Members_organizations_23_n_partners = metrics['Members_organizations_23_n_partners']
Members_organizations_24_n_partners = metrics['Members_organizations_24_n_partners']

n_reporting_partners_2024 = metrics['n_reporting_partners_2024']
n_partner_gi_2024 = metrics['n_partner_gi_2024']
n_member_gi_2024 = metrics['n_member_gi_2024']
n_initiatives_gi_pending_2024 = metrics['n_initiatives_gi_pending_2024']
reporting_partners_in_2023 = metrics['reporting_partners_in_2023']
reporting_partners_in_2022 = metrics['reporting_partners_in_2022']


n_hectares_pledge_in_2022 = metrics['n_hectares_pledge_in_2022'],
n_hectares_pledge_in_2022_n_partners = metrics['n_hectares_pledge_in_2022_n_partners'],
n_hectares_pledge_in_2023 = metrics['n_hectares_pledge_in_2023'],
n_hectares_pledge_in_2023_n_partners = metrics['n_hectares_pledge_in_2023_n_partners'],
n_hectares_plan_in_2023 = metrics['n_hectares_plan_in_2023'],
n_hectares_plan_in_2023_n_partners = metrics['n_hectares_plan_in_2023_n_partners'],
n_hectareas_pledge_n_partners = metrics['n_hectareas_pledge_n_partners'],

dollars_movilized_all_plans_in_2023 = metrics['dollars_movilized_all_plans_in_2023'],
dollars_movilized_all_plans = metrics['dollars_movilized_all_plans'],
dollars_mobilized_all_plans_n_plans_in_2023 = metrics['dollars_mobilized_all_plans_n_plans_in_2023'],
dollars_mobilized_all_plans_n_plans = metrics['dollars_mobilized_all_plans_n_plans'],
dollars_mobilized_all_plans_n_partners_in_2023 = metrics['dollars_mobilized_all_plans_n_partners_in_2023'],
dollars_mobilized_all_plans_n_partners = metrics['dollars_mobilized_all_plans_n_partners'],

n_hectares_plan_in_2022 = metrics['n_hectares_plan_in_2022'],
n_hectareas_plan_consolidated  = metrics['n_hectareas_plan_consolidated'],
n_hectares_plan_in_2022_n_partners  = metrics['n_hectares_plan_in_2022_n_partners'],


n_individuals_pledge_in_2024_n_partners = metrics['n_individuals_pledge_in_2024_n_partners'],
n_total_plans_consolidated = metrics['n_total_plans_consolidated'],
n_individuals_all_plans_n_plans = metrics['n_individuals_all_plans_n_plans'],
n_individuals_all_plans_n_partners = metrics['n_individuals_all_plans_n_partners'],

##____________________________________________________________
##____________________________________________________________
##____________________________________________________________
## FUNCTIONS: 
##____________________________________________________________
##____________________________________________________________
##____________________________________________________________

## FORMAT DATA EXPLORER 
# def rtr_data_explorer_setup():
#     # Load the logo and configure the page
#     # im = Image.open("logo_web.png")
#     # st.set_page_config(page_title="RtR DATA EXPLORER", page_icon=im, layout="wide", initial_sidebar_state="expanded")
    
#     # Apply custom CSS styling
#     with open("style.css") as css:
#         st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)
    
#     # Hide Streamlit's default footer and menu
#     hide_streamlit_style = """
#                 <style>
#                 #MainMenu {visibility: hidden;}
#                 footer {visibility: hidden;}
#                 </style>
#                 """
#     st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    
#     ## Formating metricas table
#     st.write(
#         """
#         <style>
#         [data-testid="stMetricDelta"] svg {
#             display: none;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,) 
# rtr_data_explorer_setup()

## Welcome
def render_main_page(): 
    logo_path = "logo_web.png"  # Adjust path if needed

    col1, col2 = st.columns([0.6, 5.4])  # Adjust the proportions as needed

    with col1:
        st.image(logo_path, width=100)  # Adjust width if necessary

    with col2:
        st.markdown("## DATA EXPLORER")  # Adjust text size with markdown headers if needed
        
    
    
    def welcome():
        st.markdown("""
                    **Welcome to the RtR Data Explorer**. A data exploration app for the <a style="font-weight:bold" href="https://racetozero.unfccc.int/system/racetoresilience/">Race to Resilience Campaign (RtR)</a>. 
             
                """, unsafe_allow_html=True)
        
        # st.markdown("""
        #             **Welcome to the RtR Data Explorer**. A web application designed to support the <a style="font-weight:bold" href="https://racetozero.unfccc.int/system/racetoresilience/">Race to Resilience Campaign (RtR)</a>. 
        #         """, unsafe_allow_html=True)
    welcome()
   

    def instructions():
        st.markdown("##### HOW TO USE")
        st.markdown("""
                    Begin by accessing the sidebar to choose from the RtR Data Explorer Features. The main page will then refresh to display content tailored to your settings, including interactive charts and maps. Delve into datasets, gain insights from the 'Metrics Framework', and read 'Solution Stories' for an overview of partners' experiences within the Race to Resilience Campaign.
                    """)
        
        with st.expander("Read detailed instructions here"):
            st.markdown("""
                ###### HOW TO USE THE RtR DATA EXPLORER

                **1. Navigation:** Use the sidebar to navigate the app. It is your primary tool for setting your exploration parameters.

                **2. Selecting Options:** Adjust the filters to tailor the data displayed on the main page.

                **3. Interacting with Main Page Content:** Charts and maps will update based on your selections. Hover or click on visualizations for detailed information.

                **4. Exploring Datasets:** Some elements of the main page allow interactive data exploration.

                **5. Understanding Key Concepts:** Visit the 'Metrics Framework' section for key concepts and methodologies.

                **6. Read Solution Stories:** Access case studies of partners working on resilience-building efforts.
                """)
    # instructions()
    
    def governance():
        st.markdown("##### GOVERNANCE SETUP")
        st.markdown("""
                    The governance setup of the Campaign includes three advisory bodies: the Technical Secretariat (TS), the Expert Review Group (ERG), and the Methodological Advisory Group (MAG).
                    The TS is hosted by the <a style="font-weight:bold" href="https://www.cr2.cl/">Center for Climate and Resilience Research (CR)2</a> at the University of Chile, and the other advisory bodies include experts and scientists involved in peer-reviewing applications and improving the RtR framework.
                    """, unsafe_allow_html=True)
    # governance()
# render_main_page()



## Campaign Overview
def campaign_overview_cop29():
    
    ## TEXT

    def intro_campaign_text_p0():
        col1, col2,col3 = st.columns([1.45,0.05,0.5])
        long_description = f"""
        Led by the UN Climate Change High-Level Champions under the UNFCCC Marrakesh Partnership for Global Climate Action, 
        the Race to Resilience (RtR) campaign aims to mobilize Non-Party Stakeholders with the ambitious goal of increasing 
        the resilience of 4 billion people by 2030. 
        """
        
        # Define links for the available reports
        reports = {
            "2022": "https://climatechampions.unfccc.int/wp-content/uploads/2022/09/Race-to-Zero-Race-to-Resilience-Progress-Report.pdf",
            "2023": "https://climatechampions.unfccc.int/wp-content/uploads/2024/01/Race-to-Resilience-2023-Campaign-Progress-Report.pdf",
            "2024": None  # Report not yet launched
        }

        
        with col1:
            st.markdown(long_description)
        with col2:
            st.write("")
        with col3:
            if st.button("Download 2023 RtR Report"):
                st.markdown(f"[Click here to download]( {reports['2023']} )", unsafe_allow_html=True) 
            # st.button("2024 Report (Coming Soon)", disabled=True)
            if st.button("Download 2022 RtR Report"):
                st.markdown(f"[Click here to download]( {reports['2022']} )", unsafe_allow_html=True)
            
            
    
            
        
  

    def intro_campaign_text_p1():
        long_description = f"""
        Led by the UN Climate Change High-Level Champions under the UNFCCC Marrakesh Partnership for Global Climate Action, 
        the Race to Resilience (RtR) campaign aims to mobilize Non-Party Stakeholders with the ambitious goal of increasing 
        the resilience of 4 billion people by 2030. Central to the campaign is the commitment to keeping adaptation and people 
        at the forefront of the global climate action agenda.
        """
        st.markdown(long_description)
        
    def figure_metrics_framework_p1():
        image_path = "increasingly_resilient_individuals.png" 

        # Display the image
        st.image(image_path, caption="Source: RtR Metrics Framework", use_column_width=True)
          
    def intro_campaign_text_p2():
        long_description = """
            Through the 4Ps Framework—Pledge, Plan, Proceed, and Publish—RtR partners systematically plan and report on their progress 
            in enhancing the resilience of people in vulnerable communities and natural systems. This structured approach not only 
            tracks the campaign's impact but also supports the goals of the <a style="font-weight:bold" href="https://climatechampions.unfccc.int/system/sharm-el-sheikh-adaptation-agenda/">Sharm el-Sheikh Adaptation Agenda (SAA)</a>. By participating as co-leads and members in the SAA Task Forces, RtR partners are instrumental in driving systems transformations toward 
            a more resilient future.
        """
        st.markdown(long_description, unsafe_allow_html=True)
    
    def figure_metrics_framework_p2():
            image_path = "rtr_stages.png" 
            st.image(image_path, caption="Source: RtR Metrics Framework", use_column_width=True)
        
    def generate_long_description_p2_a(n_all_rtrpartners):
        
        long_description = f"""
        Finalising its 3rd year, the RtR is making steady progress, with {n_all_rtrpartners} partners and over 700 members, present 
        across 164 countries, working to fulfil their commitments.
        """
        # st.markdown("### Campaign Overall")
        st.markdown(long_description)

        # return long_description

    def generate_long_description_p2_b(n_individuals_plan_consolidated, n_individuals_pledge_in_2024):
        # Create the description using the input parameters
        long_description = f"""
        Collectively, RtR Partners have achieved a significant milestone, designing and implementing action plans that now target the protection of lives and livelihoods of over {str(numerize(n_individuals_plan_consolidated))} 
        people most vulnerable to the climate crisis. Driven by a shared vision of a more resilient future, these partners are 
        committed to scaling up their efforts, with ambitious pledges of increasing the resilience of {str(numerize(n_individuals_pledge_in_2024))} 
        people by 2030.
        """
        # st.markdown("### Campaign Overall")
        st.markdown(long_description)

        # return long_description

    def generate_natural_systems_description(n_hectareas_pledge_adj, n_hectareas_plan_consolidated):
        # Create the description using the input parameters
        long_description = f"""
        RtR partners also have committed to increasing the resilience of  {str(numerize(n_hectareas_pledge_adj))} hectares of natural systems by 2030, with  {str(numerize(n_hectareas_plan_consolidated))} hectares already under active planning. This commitment highlights the importance of safeguarding natural ecosystems alongside human communities.
        """
        # st.markdown("### Campaign Overall")
        st.markdown(long_description)
        
    def generate_finance_description(dollars_movilized_all_plans):
        dollars_movilized_all_plans = get_integer(dollars_movilized_all_plans)
        # Create the description using the input parameters
        long_description = f"""
        To support these ambitious objectives, partners’ plans project a mobilization of USD {str(numerize(dollars_movilized_all_plans))}. This significant financial commitment underscores the scale of resources needed to build resilience across diverse communities and ecosystems worldwide.
        """
        # st.markdown("### Campaign Overall")
        st.markdown(long_description)

    def generate_long_description_p3():
        """
        Generates a long description for the Race to Resilience campaign.
        
        Parameters:
        - n_all_rtrpartners (int): The number of partners involved in the campaign.
        - n_individuals_plan_consolidated (int): The number of individuals targeted by the implemented plans.
        - n_individuals_pledge_in_2024 (int): The number of individuals targeted by the pledge for 2024.
        
        Returns:
        - long_description (str): The dynamically generated long description for the campaign.
        """
        
        # Import numerize for formatting large numbers
        # from numerize import numerize

        # Create the description using the input parameters
        long_description = f"""
        The Race to Resilience campaign underscores the power of collaboration, the strength of diversity, and the leadership of 
        Non-Party Stakeholders in keeping adaptation and resilience at the core of the Global Climate Action Agenda. By uniting 
        a wide array of stakeholders, the campaign demonstrates that collective action is essential to drive meaningful progress 
        in building a climate-resilient world.
        """
        # st.markdown("### Campaign Overall")
        st.markdown(long_description)

        # return long_description

    def disclaimer():
        disclaimer = (
        f"<strong>IMPORTANT:</strong> Out of the {n_all_rtrpartners} RtR Partners, "
        f"{n_reporting_partners} participated in the reporting process 2024. Consequently, "
        "this Data Explorer provides an overview of the progress achieved so far by these reporting partners. ")
        
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


    #CHARTS
    ## CHART NUMBER OF PEOPLE [METRICS]
    def plot_num_people_chart(n_individuals_pledge_in_2022, n_individuals_pledge_in_2023, n_individuals_pledge_in_2024,
                            n_individuals_plan_consolidated_in_2022, n_individuals_plan_consolidated_in_2023, n_individuals_plan_consolidated):
        """
        Function to generate a stacked bar chart for the number of individuals pledged and included in plans 
        for the RtR Campaign over the years 2022 to 2024.

        Parameters:
        - n_individuals_pledge_in_2022 (int): Pledged individuals for 2022.
        - n_individuals_pledge_in_2023 (int): Pledged individuals for 2023.
        - n_individuals_pledge_in_2024 (int): Pledged individuals for 2024.
        - n_individuals_plan_consolidated_in_2022 (int): Individuals in plans for 2022.
        - n_individuals_plan_consolidated_in_2023 (int): Individuals in plans for 2023.
        - n_individuals_plan_consolidated (int): Individuals in plans for 2024.

        Returns:
        None: Displays the chart in Streamlit.
        """

        # st.write("### GRAFICO NUMERO DE PERSONAS")

        # Data preparation
        years = ['2022', '2023', '2024']
        n_individuals_pledge_tochart_list = [n_individuals_pledge_in_2022, n_individuals_pledge_in_2023, n_individuals_pledge_in_2024]
        n_individuals_plan_tochart_list = [n_individuals_plan_consolidated_in_2022, n_individuals_plan_consolidated_in_2023, n_individuals_plan_consolidated]

        colors = sns.color_palette("RdPu", n_colors=2)

        # Create a stacked bar chart
        fig, ax = plt.subplots(figsize=(10, 2))
        index = range(len(years))

        # Plotting the stacked bars
        bars_pledge = ax.bar(index, n_individuals_pledge_tochart_list, label='N° Individuals Pledged', color=colors[0])
        bars_plan = ax.bar(index, n_individuals_plan_tochart_list, bottom=[0]*len(n_individuals_pledge_tochart_list), label='N° Individuals In Plans', color=colors[1])

        # Adding labels and title
        ax.set_xlabel('Year')
        ax.set_ylabel('Billions of Individuals')
        ax.set_title("Number of Individuals Pledged and Planned for the RtR Campaign Over the Years (2022 to 2024)", pad=20)

        # Adjust the tick positions to center the labels
        ax.set_xticks(index)
        ax.set_xticklabels(years)
        # ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), fancybox=True, shadow=False, ncol=2)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), fancybox=True, shadow=False, ncol=2)

        # Set y-axis limits to 4.0 billion
        ax.set_ylim(0, 4.0e9)

        # Format the y-axis ticks to show numbers in billions without scientific notation
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x/1e9:.1f}B'))

        # Adding the number above each bar segment with the additional text
        def add_value_labels(bars_pledge, bars_plan, pledge_data, plan_data):
            for bar_pledge, bar_plan, pledge_value, plan_value in zip(bars_pledge, bars_plan, pledge_data, plan_data):
                # Add label for the Pledged value
                ax.text(
                    bar_pledge.get_x() + bar_pledge.get_width() / 2,
                    bar_pledge.get_height() + 0.05 * max(pledge_data),  # Slightly above the bar
                    f'{numerize(int(pledge_value))}',  # Numerize the integer value
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    color='black'
                )
                # Add label for the Plan value within the bar
                ax.text(
                    bar_plan.get_x() + bar_plan.get_width() / 2,
                    bar_plan.get_y() + bar_plan.get_height() / 2,  # Centered within the plan segment
                    # f'{numerize(int(plan_value))} ({plan_value/pledge_value:.0%})',  # Numerize and show percentage
                    f'{numerize(int(plan_value))}',  # Numerize and show percentage
                    ha='center',
                    va='center',
                    fontsize=10,
                    color='white'
                )

        # Remove top and right spines (borders)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Apply the function to all bars with the corresponding values
        add_value_labels(bars_pledge, bars_plan, n_individuals_pledge_tochart_list, n_individuals_plan_tochart_list)

        # Display the chart in Streamlit
        # st.write("GRAFICO DE NUMERO DE PERSONAS STAKED. 2022-2024")
        st.pyplot(fig)

    # CHART NATURAL SYSTEMS
    def hectares_nat_systems_historical(n_hectares_pledge_in_2022,n_hectares_pledge_in_2023,n_hectareas_pledge_adj,
    n_hectares_plan_in_2022,n_hectares_plan_in_2023,n_hectareas_plan_consolidated,
    n_hectares_pledge_in_2022_n_partners, n_hectares_pledge_in_2023_n_partners,n_hectareas_pledge_n_partners,
    n_hectares_plan_in_2022_n_partners,n_hectares_plan_in_2023_n_partners,n_partners_reporting_n_hectareas_plan_consolidated):
        
        years = ['2022', '2023', '2024']
        n_hectareas_pledge_tochart_list = [n_hectares_pledge_in_2022, n_hectares_pledge_in_2023, n_hectareas_pledge_adj]
        n_hectareas_plan_tochart_list = [n_hectares_plan_in_2022, n_hectares_plan_in_2023, n_hectareas_plan_consolidated]
        n_hectareas_pledge_tochart_list_n_partners = [n_hectares_pledge_in_2022_n_partners, n_hectares_pledge_in_2023_n_partners, n_hectareas_pledge_n_partners]
        n_hectareas_plan_tochart_list_n_partners = [n_hectares_plan_in_2022_n_partners, n_hectares_plan_in_2023_n_partners, n_partners_reporting_n_hectareas_plan_consolidated]

        # Ensure lists contain only numbers
        n_hectareas_pledge_tochart_list = [float(x) if isinstance(x, (int, float)) else float(x[0]) for x in n_hectareas_pledge_tochart_list]
        n_hectareas_plan_tochart_list = [float(x) if isinstance(x, (int, float)) else float(x[0]) for x in n_hectareas_plan_tochart_list]


        # Parameters
        bar_width = 0.35
        index = np.arange(len(years))

        # Colors
        colors_pledge = sns.color_palette("RdPu", n_colors=3)[0]
        colors_plan = sns.color_palette("RdPu", n_colors=3)[1]

        # Create a bar chart
        fig, ax = plt.subplots(figsize=(10, 2))

        # Plotting the bars
        bars_pledge = ax.bar(index, n_hectareas_pledge_tochart_list, width=bar_width, label='Pledge', color=colors_pledge)
        bars_plan = ax.bar(index + bar_width, n_hectareas_plan_tochart_list, width=bar_width, label='Plans', color=colors_plan)

        # Adding labels and title
        ax.set_xlabel('Year')
        ax.set_ylabel('Million of Hectares')
        ax.set_title("Hectares of Natural Systems Pledged and Planned from 2022 to 2024", pad=30)

        # Adjust the tick positions to center the labels
        ax.set_xticks(index + bar_width / 2)
        ax.set_xticklabels(years)

        # Format y-axis ticks to show numbers in millions
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f'{x/1e6:.1f}M'))

        # Adding the number above each bar with the additional text
        def add_value_labels(bars, values, partners):
            for i, bar in enumerate(bars):
                yval = bar.get_height()
                partner_value = partners[i]
                
                # Check if partner_value is a tuple, if so, take the first element, else use the value directly
                if isinstance(partner_value, tuple):
                    partner_value = partner_value[0]
                
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    yval + 0.1,
                    f'{numerize(yval)}\n(Out of {int(partner_value)} Partners)',
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    color='black'
                )


        # Apply the function to both sets of bars
        add_value_labels(bars_pledge, n_hectareas_pledge_tochart_list, n_hectareas_pledge_tochart_list_n_partners)
        add_value_labels(bars_plan, n_hectareas_plan_tochart_list, n_hectareas_plan_tochart_list_n_partners)

        # Add legend
        ax.legend()

        # Remove top and right spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Display the chart in Streamlit
        # st.write("Grafico Hectareas todos los años no staked")
        st.pyplot(fig)

    # CHART FINANCE
    def finance_chart_2023_2024(dollars_movilized_all_plans_in_2023,dollars_movilized_all_plans,
                                dollars_mobilized_all_plans_n_plans_in_2023,dollars_mobilized_all_plans_n_plans,
                                dollars_mobilized_all_plans_n_partners_in_2023,dollars_mobilized_all_plans_n_partners):

        years = ['2023', '2024']
        dolars_mob_list_all = [dollars_movilized_all_plans_in_2023, dollars_movilized_all_plans]
        dolars_mob_n_plans_list = [dollars_mobilized_all_plans_n_plans_in_2023, dollars_mobilized_all_plans_n_plans]
        dolars_mob_n_partners_list = [dollars_mobilized_all_plans_n_partners_in_2023, dollars_mobilized_all_plans_n_partners]

        # Define colors
        colors = sns.color_palette("RdPu", n_colors=2)

        # Scale the data to billions with tuple and numeric checks
        dolars_mob_list_all_billions = []
        for x in dolars_mob_list_all:
            # Extract the first element if x is a tuple
            if isinstance(x, tuple):
                x = x[0]
            # Only proceed if x is numeric
            if isinstance(x, (int, float)):
                dolars_mob_list_all_billions.append(x / 1e9)
            else:
                st.write("Non-numeric or unexpected data type in dolars_mob_list_all:", x)

        # Create a bar chart
        fig, ax = plt.subplots(figsize=(10, 1.5))
        bar_width = 0.5
        index = range(len(years))

        # Plotting the bars
        bars_all = ax.bar(index, dolars_mob_list_all_billions, width=bar_width, label='US Dollars', color=colors)

        # Adding labels and title
        ax.set_xlabel('Year')
        ax.set_ylabel('Billions of Dollars')  # Updated label to indicate billions
        ax.set_title("Finance to be Mobilized in RtR Partner's Plans Over the Years (2023 to 2024)", pad=30)

        # Adjust the tick positions to center the labels
        ax.set_xticks([i for i in index])
        ax.set_xticklabels(years)

        # Formatter to show the y-axis values in plain numbers
        ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{int(x):,} B'))
        

        # Adding the number above each bar with additional text
        def add_value_labels(bars, dolars_mob_n_plans_list, dolars_mob_n_partners_list):
            for i, bar in enumerate(bars):
                yval = bar.get_height()
                yval_int = int(yval * 1e9)  # Convert back to the original value for the label

                # Check if elements in dolars_mob_n_plans_list and dolars_mob_n_partners_list are tuples
                # and extract the first element if they are
                n_plans = dolars_mob_n_plans_list[i]
                n_partners = dolars_mob_n_partners_list[i]
                
                if isinstance(n_plans, tuple):
                    n_plans = n_plans[0]
                if isinstance(n_partners, tuple):
                    n_partners = n_partners[0]
                
                # Ensure n_plans and n_partners are integers or can be converted to integers
                try:
                    n_plans = int(n_plans)
                    n_partners = int(n_partners)
                except (TypeError, ValueError):
                    st.write(f"Unexpected value in lists: n_plans={n_plans}, n_partners={n_partners}")
                    continue  # Skip this bar if values are invalid

                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    yval + 0.1,
                    f'{numerize(yval_int)}\n(Out of {n_plans} Plans from {n_partners} Partners)',
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    color='black'
                )

        # Remove top and right spines (borders)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Apply the function to all bars
        add_value_labels(bars_all, dolars_mob_n_plans_list, dolars_mob_n_partners_list)

        # Display the chart in Streamlit
        # st.write("Grafico de Finance 2023-2024 PLAN")
        st.pyplot(fig)

    # ## TOTAL NUMBER OF PARTNERS [REPORTING PARTNERS]
    def plot_reporting_status_cop29(n_all_rtrpartners, n_reporting_partners, n_newpartners):
        """
        Function to create a horizontal bar chart showing the reporting status of partners for COP29 (2024).

        Parameters:
        - n_all_rtrpartners (int): Total number of partners.
        - n_reporting_partners (int): Number of partners reporting for COP29 (2024).
        - n_newpartners (int): Number of new partners not yet reporting.

        Returns:
        None: Displays the bar chart in Streamlit.
        """

        ## CHART REPORTING STATUS COP 29 (2024)
        # Calculate the percentages relative to the total number of partners
        percent_reporting = (n_reporting_partners / n_all_rtrpartners) * 100
        percent_new = (n_newpartners / n_all_rtrpartners) * 100

        colors = sns.color_palette("RdPu", n_colors=2)
        fig_width = 8  # Width of the figure
        fig_height = 2  # Height of the figure

        # Create the figure and horizontal bar chart with defined size
        fig_all_partners, ax = plt.subplots(figsize=(fig_width, fig_height))

        # Plotting the horizontal bars for reporting and new partners on the same bar
        bars = ax.barh(['Partners'], [n_reporting_partners], color=colors[0], label='Reporting Partners')
        ax.barh(['Partners'], [n_newpartners], left=[n_reporting_partners], color=colors[1], label='New Partners')

        # Adding labels inside each section of the bar with absolute number and percentage
        # For Reporting Partners
        midpoint_reporting = n_reporting_partners / 2
        ax.text(midpoint_reporting, 0, f'{n_reporting_partners} Reporting Partners \n - Partners Participating in the 2024 Reporting Process for COP29 -  \n({percent_reporting:.1f}%)',
                va='center', ha='center', color='black')

        # For New Partners
        midpoint_new = n_reporting_partners + (n_newpartners / 2)
        ax.text(midpoint_new, 0, f'{n_newpartners} \nNew Partners\n-No yet reporting-\n({percent_new:.1f}%)',
                va='center', ha='center', color='black')

        # Set labels
        ax.set_xlabel('Number of Partners')
        ax.set_yticklabels([])  # Hide the y-axis labels
        ax.set_title('Total Number of RtR Partner by COP29', fontsize=11)

        # Remove top and right spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Add annotation text
        annotation_text = f"N = {n_all_rtrpartners} Partners"
        fig_all_partners.text(0.95, 0.0, annotation_text, ha='right', va='bottom', fontsize=10, color='black')  # Adjust coordinates and alignment

        # Adjust layout to fit and show the bar chart properly
        plt.tight_layout()
        st.pyplot(fig_all_partners)
    # plot_reporting_status_cop29(n_all_rtrpartners, n_reporting_partners, n_newpartners)

    def display_reporting_status(n_all_rtrpartners, n_reporting_partners, n_newpartners, n_rtrmember_exp,
                                n_all_rtrpartners_cop28, reporting_partners_in_2023_cop28, no_reporting_partner_2023_cop28, n_rtrmember_exp_in_2023_cop28,
                                n_all_rtrpartners_2022_cop27, reporting_partners_in_2022_cop27, no_reporting_partners_in_2022_cop27, n_rtrmember_exp_in_2022_cop27):


        # st.write('### REPORTING PARTNERS THROUGH THE YEARS OF THE RtR CAMPAIGN')
        # col1, col2, col3 = st.columns(3)

        # with col1:
        #     st.write('### 2024 -COP29')
        #     st.metric(label="n_all_rtrpartners_in_2024_cop29", value= n_all_rtrpartners )
        #     # st.write('n_all_rtrpartners_in_2024_cop29')
        #     # n_all_rtrpartners
        #     st.write('n_reporting_partners_in_2024')
        #     n_reporting_partners
        #     st.write('n_newpartners No reporta_in_2024')
        #     n_newpartners
        #     st.write('n_rtrmember_exp_in 2024')
        #     n_rtrmember_exp

        # with col2:
        #     st.write('### 2023 - COP28')
        #     st.metric(label="n_all_rtrpartners_cop28", value= n_all_rtrpartners_cop28 )
        #     # st.write('n_all_rtrpartners_cop28')
        #     # n_all_rtrpartners_cop28
        #     st.write('reporting_partners_in_2023_cop28')
        #     reporting_partners_in_2023_cop28
        #     st.write('no_reporting_partner_2023_cop28')
        #     no_reporting_partner_2023_cop28
        #     st.write('n_rtrmember_exp_in_2023_cop28')
        #     n_rtrmember_exp_in_2023_cop28
            
        # with col3:
        #     st.write('### 2022 - COP27')
        #     st.metric(label="n_all_rtrpartners_2022_cop27", value= n_all_rtrpartners_2022_cop27 )
        #     # st.write('n_all_rtrpartners_2022_cop27')
        #     # n_all_rtrpartners_2022_cop27
        #     st.write('reporting_partners_in_2022_cop27')
        #     reporting_partners_in_2022_cop27
        #     st.write('no_reporting_partners_in_2022_cop27')
        #     no_reporting_partners_in_2022_cop27
        #     st.write('n_rtrmember_exp_in_2022_cop27')
        #     n_rtrmember_exp_in_2022_cop27


        ## Reporting Status of RtR Partners Over Years

        ## CHART 2024 HISTORICAL REPORTING STATUS PARTNERS
        years = ['2022', '2023', '2024']
        all_partners = [n_all_rtrpartners_2022_cop27, n_all_rtrpartners_cop28, n_all_rtrpartners]
        reporting_partners = [reporting_partners_in_2022_cop27, reporting_partners_in_2023_cop28, n_reporting_partners]
        new_partners = [no_reporting_partners_in_2022_cop27, no_reporting_partner_2023_cop28, n_newpartners]
        colors = sns.color_palette("RdPu", n_colors=3)

        # Create a bar chart
        fig, ax = plt.subplots(figsize=(10, 2))
        bar_width = 0.2
        index = range(len(years))
        bars_all = ax.bar(index, all_partners, width=bar_width, label='All Partners', color=colors[0])
        bars_reporting = ax.bar([i + bar_width for i in index], reporting_partners, width=bar_width, label='Reporting Partners', color=colors[1])
        bars_new = ax.bar([i + 2 * bar_width for i in index], new_partners, width=bar_width, label='New Partners (Not Yet Reporting)', color=colors[2])
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Partners')
        ax.set_title('Reporting Status of RtR Partners Over Years', pad=20) 
        ax.set_xticks([i + bar_width for i in index])
        ax.set_xticklabels(years)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), fancybox=True, shadow=False, ncol=3)

        # Adding the number above each bar
        def add_value_labels(bars):
            for bar in bars:
                yval = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    yval + 0.1,
                    int(yval),
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    color='black'
                )
        # Apply the function to all bars
        add_value_labels(bars_all)
        add_value_labels(bars_reporting)
        add_value_labels(bars_new)

        # Remove top and right spines (borders)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # Display the chart in Streamlit
        st.pyplot(fig)


    #METRICS
    def get_integer(value):
                # If the value is a tuple, take the first element
                if isinstance(value, tuple):
                    value = value[0]
                # Convert to integer if possible
                return int(value)
    
    def metrics_pledge(n_individuals_pledge_in_2024,n_individuals_pledge_in_2024_n_partners):
        n_individuals_pledge_in_2024 = get_integer(n_individuals_pledge_in_2024)
        n_individuals_pledge_in_2024_n_partners = get_integer(n_individuals_pledge_in_2024_n_partners)
        
        st.metric(
        label = "N° Individuals Pledged",
        value = numerize(int(n_individuals_pledge_in_2024)),
        help = "Out of "+str(numerize(int(n_individuals_pledge_in_2024_n_partners)))+" partners")

    def metrics_plan(n_individuals_plan_consolidated,n_individuals_all_plans_n_partners,n_total_plans_consolidated):
        n_individuals_plan_consolidated = get_integer(n_individuals_plan_consolidated)
        n_individuals_all_plans_n_partners = get_integer(n_individuals_all_plans_n_partners)
        n_total_plans_consolidated = get_integer(n_total_plans_consolidated) 
        
        
        st.metric(
        label="N° Individuals Plan",
        value=numerize(int(n_individuals_plan_consolidated)),
        help="Out of " + str(numerize(int(n_individuals_all_plans_n_partners))) + 
            " Partners (" + str(numerize(int(n_total_plans_consolidated))) + " Plans)")
        # st.metric("N° Individuals Plan",numerize(int(n_individuals_plan_consolidated)),"Out of "+str(numerize(int(n_individuals_all_plans_n_partners)))+" Partners ("+str(numerize(int(n_total_plans_consolidated))+" Plans)"))

    def metrics_partners(n_all_rtrpartners):  
            st.metric("N° Partners",numerize(int(n_all_rtrpartners)),
            help = f"Out of the {n_all_rtrpartners} RtR Partners, "
            f"{n_reporting_partners} participated in the reporting process 2024. Consequently, "
            "this Data Explorer provides an overview of the progress achieved so far by these reporting partners. ")

    def metrics_members(n_member_gi_2024):  
            # st.metric("N° Members",numerize(int(n_member_gi_2024)))
            st.metric("N° Members",689,help = "This number is underreview")
    
    def metrics_goal(rtr_goal_individuals):  
            st.metric("Campaign Goal",numerize(int(rtr_goal_individuals)))
    
    def metrics_hectares_natsyst_pledge(n_hectareas_pledge_adj,n_hectareas_pledge_n_partners):  
            st.metric("Hectares Pledged",numerize(int(n_hectareas_pledge_adj)), help = f"Out of "+str(numerize(int(n_hectareas_pledge_n_partners)))+" partners")
    
    def metrics_hectares_natsyst_plan(n_hectareas_plan_consolidated,n_partners_reporting_n_hectareas_plan_consolidated):  
            st.metric("Hectares Planned",numerize(int(n_hectareas_plan_consolidated)), help = f"Out of "+str(numerize(int(n_partners_reporting_n_hectareas_plan_consolidated)))+" Partners.")
    
    def metrics_finance(dollars_movilized_all_plans,dollars_mobilized_all_plans_n_plans,dollars_mobilized_all_plans_n_partners):
        dollars_movilized_all_plans = get_integer(dollars_movilized_all_plans)
        dollars_mobilized_all_plans_n_plans = get_integer(dollars_mobilized_all_plans_n_plans)
        dollars_mobilized_all_plans_n_partners = get_integer(dollars_mobilized_all_plans_n_partners)   
        st.metric("USD Planned",numerize(int(dollars_movilized_all_plans)),help = "Out of "+str(numerize(int(dollars_mobilized_all_plans_n_partners)))+" Partners ("+str(numerize(int(dollars_mobilized_all_plans_n_plans))+" plans)"))

    ## DISPLAY
    intro_campaign_text_p0()
    
    
    # n_gi_2024 = n_partner_gi  
    # n_pledge_2024 = n_partner_pledge 
    # n_plans_2024 = n_partners_plan
    # n_finance_plans_2024= dollars_mobilized_all_plans_n_partners 
    
    




    
    
    
    
    
    with st.expander("Discover more about our approach to achieving this goal"):
        col1, col2 = st.columns([1.05,0.95])

        with col1:
            intro_campaign_text_p1()
            intro_campaign_text_p2()
            figure_metrics_framework_p2()

        with col2:
            figure_metrics_framework_p1()
        
        file_path_full_doc = "rtrmetricsframework2023_full.pdf"

        # Adding a download button for the PDF in the second column
    with open(file_path_full_doc, "rb") as file:
            col1.download_button(
                label="Download RtR Metrics Framework here",
                data=file,
                file_name=os.path.basename(file_path_full_doc),
                mime="application/octet-stream",
                key='download_metric_framework_pdf'  # Unique key for this button
            )

    

    #PARTNERS INTRODUCTION
    def description_metric(df_all_partners_summary, n_all_rtrpartners, n_reporting_partners, n_newpartners, n_rtrmember_exp,
                                n_all_rtrpartners_cop28, reporting_partners_in_2023_cop28, no_reporting_partner_2023_cop28, n_rtrmember_exp_in_2023_cop28,
                                n_all_rtrpartners_2022_cop27, reporting_partners_in_2022_cop27, no_reporting_partners_in_2022_cop27, n_rtrmember_exp_in_2022_cop27):
        st.markdown("#### Current Partners & Reporting Status")
        generate_long_description_p2_a(n_all_rtrpartners)
        
        # col1, col2,col3,col4, col5, col6, col7  = st.columns(7)
        # with col1:
        #     st.markdown("#### Current Partners")
        
        # with col4:
        #     st.markdown("#### Reporting Status")
        
        col1, col2,col3,col4, col5, col6, col7  = st.columns([1,1,0.5,1.5,1,1,1])
        with col1:
            metrics_partners(n_all_rtrpartners)
        
        with col2:
            metrics_members(n_member_gi_2024)
        
        with col3:
            st.write("")
            
        with col4:
            st.metric("N° Partners General Information",numerize(int(n_partner_gi)))
            
        with col5:
            st.metric("N° Partners Pledge",numerize(int(n_partner_pledge)))
            
        with col6:
            st.metric("N° Partners Plan",numerize(int(n_partners_plan)))
            
        with col7:
            st.metric("N° Partners Proceed (Pilot)",6)
            
            
        
    
    
    
            
        tab1, tab2 = st.tabs(["List of RtR Partners", "RtR Partners (2022-2024)"])

        with tab1:
            st.dataframe(
                df_all_partners_summary,
                column_config={
                    "Website": st.column_config.LinkColumn("Website"),
                },
                hide_index=True
            )
            st.markdown("<h6 style='color:#FF37D5;'>Use the Partner Finder to explore RtR partners' pledges and plans in greater detail</h4>", unsafe_allow_html=True)


        with tab2:
            col1, col2, col3 = st.columns([0.5,2,0.5])
            
            with col2: 
                st.markdown("The number of RtR partners has increased each year.")
                display_reporting_status(
                    n_all_rtrpartners, n_reporting_partners, n_newpartners, n_rtrmember_exp,
                    n_all_rtrpartners_cop28, reporting_partners_in_2023_cop28, no_reporting_partner_2023_cop28, n_rtrmember_exp_in_2023_cop28,
                    n_all_rtrpartners_2022_cop27, reporting_partners_in_2022_cop27, no_reporting_partners_in_2022_cop27, n_rtrmember_exp_in_2022_cop27
                )        
    description_metric(df_all_partners_summary,n_all_rtrpartners, n_reporting_partners, n_newpartners, n_rtrmember_exp,
                                n_all_rtrpartners_cop28, reporting_partners_in_2023_cop28, no_reporting_partner_2023_cop28, n_rtrmember_exp_in_2023_cop28,
                                n_all_rtrpartners_2022_cop27, reporting_partners_in_2022_cop27, no_reporting_partners_in_2022_cop27, n_rtrmember_exp_in_2022_cop27)
          
    # INDIVIDUALS
    def presentation_metrics_individuals(n_individuals_pledge_in_2022, n_individuals_pledge_in_2023, n_individuals_pledge_in_2024,n_individuals_pledge_in_2024_n_partners,
                                n_individuals_plan_consolidated_in_2022, n_individuals_plan_consolidated_in_2023, n_individuals_plan_consolidated,n_individuals_all_plans_n_partners):
        # st.write("### Progress")
        st.write("#### Increasing resilience on Individuals")
        generate_long_description_p2_b(n_individuals_plan_consolidated, n_individuals_pledge_in_2024) 
        col1, col2,col3,col4, col5 = st.columns([1,1,1.4,0.1,3.5])
        with col1:
            metrics_goal(rtr_goal_individuals)
        
        with col2:
            metrics_pledge(n_individuals_pledge_in_2024,n_individuals_pledge_in_2024_n_partners)
        
        with col3:
            metrics_plan(n_individuals_plan_consolidated,n_individuals_all_plans_n_partners,n_total_plans_consolidated)    
        
        with col4:
            st.write("")
        
        with col5:
            plot_num_people_chart(n_individuals_pledge_in_2022, n_individuals_pledge_in_2023, n_individuals_pledge_in_2024,
                                n_individuals_plan_consolidated_in_2022, n_individuals_plan_consolidated_in_2023, n_individuals_plan_consolidated)       
    presentation_metrics_individuals(n_individuals_pledge_in_2022, n_individuals_pledge_in_2023, n_individuals_pledge_in_2024,n_individuals_pledge_in_2024_n_partners,
                                n_individuals_plan_consolidated_in_2022, n_individuals_plan_consolidated_in_2023, n_individuals_plan_consolidated,n_individuals_all_plans_n_partners)
    
    ## NATURAL SYSTEMS
    def presentation_metrics_natural_systems(n_hectares_pledge_in_2022,n_hectares_pledge_in_2023,n_hectareas_pledge_adj,
            n_hectares_plan_in_2022,n_hectares_plan_in_2023,n_hectareas_plan_consolidated,
            n_hectares_pledge_in_2022_n_partners, n_hectares_pledge_in_2023_n_partners,n_hectareas_pledge_n_partners,
            n_hectares_plan_in_2022_n_partners,n_hectares_plan_in_2023_n_partners,n_partners_reporting_n_hectareas_plan_consolidated):
        
        st.write("#### Increasing resilience on Natural Systems")
        n_hectareas_pledge_adj = get_integer(n_hectareas_pledge_adj)
        n_hectareas_plan_consolidated = get_integer(n_hectareas_plan_consolidated)
        n_partners_reporting_n_hectareas_plan_consolidated = get_integer(n_partners_reporting_n_hectareas_plan_consolidated)
        n_hectareas_pledge_n_partners = get_integer(n_hectareas_pledge_n_partners)
        
        generate_natural_systems_description(n_hectareas_pledge_adj, n_hectareas_plan_consolidated)
        col1, col2,col3,col4, col5 = st.columns([1,1,1.4,0.1,3.5])
        with col1:
            metrics_hectares_natsyst_pledge(n_hectareas_pledge_adj,n_hectareas_pledge_n_partners)
        
        with col2:
            metrics_hectares_natsyst_plan(n_hectareas_plan_consolidated,n_partners_reporting_n_hectareas_plan_consolidated)
    
        with col3:
            st.write("")
        
        with col4:
            st.write("")
        
        with col5:
            hectares_nat_systems_historical(n_hectares_pledge_in_2022,n_hectares_pledge_in_2023,n_hectareas_pledge_adj,
            n_hectares_plan_in_2022,n_hectares_plan_in_2023,n_hectareas_plan_consolidated,
            n_hectares_pledge_in_2022_n_partners, n_hectares_pledge_in_2023_n_partners,n_hectareas_pledge_n_partners,
            n_hectares_plan_in_2022_n_partners,n_hectares_plan_in_2023_n_partners,n_partners_reporting_n_hectareas_plan_consolidated)      
    presentation_metrics_natural_systems(n_hectares_pledge_in_2022,n_hectares_pledge_in_2023,n_hectareas_pledge_adj,
            n_hectares_plan_in_2022,n_hectares_plan_in_2023,n_hectareas_plan_consolidated,
            n_hectares_pledge_in_2022_n_partners, n_hectares_pledge_in_2023_n_partners,n_hectareas_pledge_n_partners,
            n_hectares_plan_in_2022_n_partners,n_hectares_plan_in_2023_n_partners,n_partners_reporting_n_hectareas_plan_consolidated)
    
    ## FINANCE
    def presentation_metrics_finance(dollars_movilized_all_plans_in_2023,dollars_movilized_all_plans,
                                        dollars_mobilized_all_plans_n_plans_in_2023,dollars_mobilized_all_plans_n_plans,
                                        dollars_mobilized_all_plans_n_partners_in_2023,dollars_mobilized_all_plans_n_partners):
        
        st.write("#### Finance planned to be movilized")
        generate_finance_description(dollars_movilized_all_plans)
        col1, col2 = st.columns(2)
        with col1:
            metrics_finance(dollars_movilized_all_plans,dollars_mobilized_all_plans_n_plans,dollars_mobilized_all_plans_n_partners)
            
        with col2:
            finance_chart_2023_2024(dollars_movilized_all_plans_in_2023,dollars_movilized_all_plans,
                                        dollars_mobilized_all_plans_n_plans_in_2023,dollars_mobilized_all_plans_n_plans,
                                        dollars_mobilized_all_plans_n_partners_in_2023,dollars_mobilized_all_plans_n_partners)        
    presentation_metrics_finance(dollars_movilized_all_plans_in_2023,dollars_movilized_all_plans,
                                        dollars_mobilized_all_plans_n_plans_in_2023,dollars_mobilized_all_plans_n_plans,
                                        dollars_mobilized_all_plans_n_partners_in_2023,dollars_mobilized_all_plans_n_partners)
      
# def current_partners():

#     def presentation_partners(): 
#         long_description = f"""
#         ## CURRENT PARTNERS
#         Race to Resilience partners are at the heart of the campaign. Together, they are driving a step-change in global ambition and action on resilience — mobilizing businesses, financial institutions, cities, regions, states and civil society organisations to come together and help achieve our goal of making 4 billion people more resilient to the impacts of climate change by 2030.
#         """
#         st.markdown(long_description)
#     # presentation_partners()

#     st.markdown("### RtR Current Partners")
#     col1, col2, col3,col4 = st.columns([0.15,0.15,0.15,0.55])
    
#     with col1:
#         st.metric("All RtR Partners",n_all_rtrpartners)
#         st.write("")
#         st.markdown('''<a style="font-weight:bold" href="https://racetozero.unfccc.int/meet-the-partners/">Meet the Partners Here</a>
#                     ''', unsafe_allow_html=True)
    
#     with col2:
#         st.metric("Reporting Partners",n_reporting_partners)
    
#     with col3:
#         st.metric("New Partners",n_newpartners)
   
    
#     # Chart historical reporting partners [REPORTING PARTNERS]
   
#     with col4:
#         display_reporting_status(n_all_rtrpartners, n_reporting_partners, n_newpartners, n_rtrmember_exp,
#                                  n_all_rtrpartners_cop28, reporting_partners_in_2023_cop28, no_reporting_partner_2023_cop28, n_rtrmember_exp_in_2023_cop28,
#                                  n_all_rtrpartners_2022_cop27, reporting_partners_in_2022_cop27, no_reporting_partners_in_2022_cop27, n_rtrmember_exp_in_2022_cop27)
# # current_partners()

## Global Outreach
def global_outreach():
    ##GEOGRAPHICAL DIMENSION
    def process_country_data(df_pledge, df_2023_plan, df_country, n_reporting_partners):

        def countries_to_plot(df, source, variable_country, type_country_info, df_country):
            # Create a list of unique country types (such as country names)
            country_type = df[variable_country].str.split(';').explode().str.strip().unique()

            # Initialize a dictionary to store the results
            result_dict = {type_country_info: [], 'N_Partners': [], 'Short name': []}

            # For each country, count the frequency of partners and concatenate the short names
            for country in country_type:
                # Count the frequency of users, using regex=False to avoid manually escaping special characters
                frequency = df[variable_country].str.contains(country, regex=False).sum()
                # Concatenate the short names separated by semicolons
                partner = '; '.join(df.loc[df[variable_country].str.contains(country, regex=False), 'short_name'].unique())
                # Add the results to the dictionary
                result_dict[type_country_info].append(country)
                result_dict['N_Partners'].append(frequency)
                result_dict['Short name'].append(partner)

            # Create a new DataFrame with the results
            df_expected_country = pd.DataFrame(result_dict)
            df_expected_country = df_expected_country[df_expected_country[type_country_info].notna() & (df_expected_country[type_country_info] != "")]
            df_expected_country = df_expected_country.sort_values(by=['N_Partners'], ascending=True)
            
            # Rename the 'Country' column in df_country to match variable_country
            df_country = df_country.rename(columns={'Country': variable_country})
        
            # # df_country['all_countries'] = df_country['all_countries'].replace("United States","United States of America").fillna('').astype(str)
            
            # df_expected_country['Country'] = df_expected_country['Country'].replace("United States","United States of America").fillna('').astype(str)


            # Merge the expected DataFrame with the country DataFrame on type_country_info
            df_expected_country = pd.merge(df_expected_country, df_country, left_on=type_country_info, right_on=variable_country, how='outer')
            df_expected_country['ND_GAIN Index Country'] = df_expected_country['ND_GAIN Index Country'].replace({0: np.nan})
            df_expected_country['ND_GAIN Index Country'] = df_expected_country['ND_GAIN Index Country'].replace({np.nan: 'No info'})
            
            
            df_expected_country = df_expected_country[df_expected_country['country'].notna()]
            
            # Group by continent, summing the number of partners and concatenating short names
            df_expected_country['Short name'] = df_expected_country['Short name'].astype(str)
            df_expected_country['Source'] = source
            df_expected_country = df_expected_country.sort_values(by='N_Partners', ascending=False)
            
            
            #  Group by continent, summing the number of partners and concatenating unique short names (with duplicates removed)
            continent_summary = df_expected_country.groupby('continent').agg(
                Partners_List=pd.NamedAgg(column='Short name', aggfunc=lambda x: '; '.join(
                    sorted(
                        set([item.strip() for sublist in x for item in sublist.split(';') 
                            if pd.notnull(item) and item.strip().lower() != 'nan'])  # Filter out 'nan'
                    )
                )),
                N_Partners=pd.NamedAgg(column='Short name', aggfunc=lambda x: len(set([item.strip() for sublist in x for item in sublist.split(';') 
                                                                if pd.notnull(item) and item.strip().lower() != 'nan']))),  # Count unique partners
            ).reset_index()
            continent_summary['Category'] = 'continent'
            continent_summary['Source'] = source
            continent_summary = continent_summary.sort_values(by='N_Partners', ascending=False)
            continent_summary['continent'] = continent_summary['continent'].replace('Northern America', 'North America')
            continent_summary['continent'] = continent_summary['continent'].replace('Latin America and the Caribbean', 'North America')


            # Group by region_wb
            region_wb_summary = df_expected_country.groupby('region_wb').agg(
                Partners_List=pd.NamedAgg(column='Short name', aggfunc=lambda x: '; '.join(
                    sorted(
                        set([item.strip() for sublist in x for item in sublist.split(';') 
                            if pd.notnull(item) and item.strip().lower() != 'nan'])  # Filter out 'nan'
                    )
                )),
                N_Partners=pd.NamedAgg(column='Short name', aggfunc=lambda x: len(set([item.strip() for sublist in x for item in sublist.split(';') 
                                                                if pd.notnull(item) and item.strip().lower() != 'nan']))),  # Count unique partners
            ).reset_index()
            region_wb_summary['Category'] = 'region_wb'
            region_wb_summary['Source'] = source
            region_wb_summary = region_wb_summary.sort_values(by='N_Partners', ascending=False)
            
            # Group by subregion
            subregion_summary = df_expected_country.groupby('subregion').agg(
                Partners_List=pd.NamedAgg(column='Short name', aggfunc=lambda x: '; '.join(
                    sorted(
                        set([item.strip() for sublist in x for item in sublist.split(';') 
                            if pd.notnull(item) and item.strip().lower() != 'nan'])  # Filter out 'nan'
                    )
                )),
                N_Partners=pd.NamedAgg(column='Short name', aggfunc=lambda x: len(set([item.strip() for sublist in x for item in sublist.split(';') 
                                                                if pd.notnull(item) and item.strip().lower() != 'nan']))),  # Count unique partners
            ).reset_index()
            subregion_summary['Category'] = 'subregion'
            subregion_summary['Source'] = source
            subregion_summary = subregion_summary.sort_values(by='N_Partners', ascending=False)
            
            # Return the dataframes
            return df_expected_country, continent_summary, region_wb_summary, subregion_summary

        # Data_Pledge
        df = df_pledge
        source = "pledge"
        variable_country = "all_countries"
        type_country_info = "country"
        df_pledge_all_countries, continent_summary_pledge, region_wb_summary_pledge,subregion_summary_pledge = countries_to_plot(df,source, variable_country, type_country_info, df_country)
        # st.write('continent_summary_pledge',continent_summary_pledge)

        # # Data_Plan
        df = df_2023_plan
        source = "plan"
        variable_country = "all_countries"
        type_country_info = "country"
        df_plan_all_countries, continent_summary_plan, region_wb_summary_plan,subregion_summary_plan = countries_to_plot(df,source, variable_country, type_country_info, df_country)
        # st.write('df_plan_all_countries',df_plan_all_countries)


        ## Combine Two Data Frames
        ### Combine the two DataFrames
        df_countries_pledge_and_plan = pd.concat([df_pledge_all_countries[['country', 'Short name', 'Source']],
                                                df_plan_all_countries[['country', 'Short name', 'Source']]], 
                                                ignore_index=True)

        # Group by 'country' and concatenate 'Short name' and 'Source' values using ";"
        df_countries_pledge_and_plan = df_countries_pledge_and_plan.groupby('country').agg({
            'Short name': lambda x: '; '.join(x.dropna().unique()),  # Concatenate unique 'Short name' with ";"
            'Source': lambda x: '; '.join(x.dropna().unique())       # Concatenate unique 'Source' with ";"
        }).reset_index()

        # Correct the country name for 'United States' to 'United States of America'
        df_countries_pledge_and_plan.loc[df_countries_pledge_and_plan['country'] == 'United States', 'country'] = 'United States of America'

        # Concatenate 'Short name' and 'Source' for 'United States of America' and create a new row 'USA_Parche'
        usa_info = df_countries_pledge_and_plan[df_countries_pledge_and_plan['country'] == 'United States of America']

        # Create a DataFrame for the new row
        usa_parche_row = pd.DataFrame({
            'country': ['USA_Parche'],
            'Short name': ['; '.join(usa_info['Short name'])],
            'Source': ['; '.join(usa_info['Source'])]
        })

        # Concatenate the new row to the original DataFrame
        df_countries_pledge_and_plan = pd.concat([df_countries_pledge_and_plan, usa_parche_row], ignore_index=True)
        df_countries_pledge_and_plan = df_countries_pledge_and_plan[df_countries_pledge_and_plan['country'] != 'United States of America']
        df_countries_pledge_and_plan.loc[df_countries_pledge_and_plan['country'] == 'USA_Parche', 'country'] = 'United States of America'

        # Function to remove duplicates in a string separated by ";"
        def remove_duplicates(text):
            items = text.split('; ')
            unique_items = "; ".join(sorted(set(items), key=items.index))
            return unique_items

        # Apply the function only to rows where the 'country' is 'United States of America'
        df_countries_pledge_and_plan['Short name'] = df_countries_pledge_and_plan['Short name'].apply(remove_duplicates)
        df_countries_pledge_and_plan['Source'] = df_countries_pledge_and_plan['Source'].apply(remove_duplicates)

        # Function to count the number of values separated by ";"
        def count_separated_values(text):
            if pd.isna(text) or text.strip() == "":  # Handle NaN or empty strings
                return 0
            return len(text.split(';'))

        # Create a new column 'N_Partners' that counts the values separated by ";"
        df_countries_pledge_and_plan['N_Partners'] = df_countries_pledge_and_plan['Short name'].apply(count_separated_values)

        df_country = df_country.rename(columns={'Country': 'country'})

        # Merge the expected DataFrame with the country DataFrame on type_country_info
        df_countries_pledge_and_plan = pd.merge(df_countries_pledge_and_plan, df_country, how='outer')
        df_countries_pledge_and_plan['ND_GAIN Index Country'] = df_countries_pledge_and_plan['ND_GAIN Index Country'].replace({0: np.nan})
        df_countries_pledge_and_plan['ND_GAIN Index Country'] = df_countries_pledge_and_plan['ND_GAIN Index Country'].replace({np.nan: 'No info'})
            
        # Group by continent, summing the number of partners and concatenating short names
        df_countries_pledge_and_plan['Short name'] = df_countries_pledge_and_plan['Short name'].astype(str)
        # df_expected_country['Source'] = "Pledge & Plan"
        df_countries_pledge_and_plan = df_countries_pledge_and_plan[df_countries_pledge_and_plan['Short name'].notna() & (df_countries_pledge_and_plan['Short name'] != "") & (df_countries_pledge_and_plan['Short name'] != "nan")]
        df_countries_pledge_and_plan = df_countries_pledge_and_plan.sort_values(by='N_Partners', ascending=False)

        # st.write('df_countries_pledge_and_plan',df_countries_pledge_and_plan)


        source = "pledge; plan"   ##This because in the pledge;plan data set, the construction of the table does not follow the above funktion. 

        #  Group by continent, summing the number of partners and concatenating unique short names (with duplicates removed)
        continent_summary_pp = df_countries_pledge_and_plan.groupby('continent').agg(
            Partners_List=pd.NamedAgg(column='Short name', aggfunc=lambda x: '; '.join(
                sorted(
                    set([item.strip() for sublist in x for item in sublist.split(';') 
                        if pd.notnull(item) and item.strip().lower() != 'nan'])  # Filter out 'nan'
                )
            )),
            N_Partners=pd.NamedAgg(column='Short name', aggfunc=lambda x: len(set([item.strip() for sublist in x for item in sublist.split(';') 
                                                            if pd.notnull(item) and item.strip().lower() != 'nan']))),  # Count unique partners
        ).reset_index()
        continent_summary_pp['% Partners'] = round((continent_summary_pp['N_Partners'] / n_reporting_partners)*100,1)
        continent_summary_pp['Category'] = 'continent'
        continent_summary_pp['Source'] = source
        continent_summary_pp = continent_summary_pp.sort_values(by='N_Partners', ascending=False)

        # st.write('contenintes pledge and plan',continent_summary_pp)



        # Group by region_wb
        region_wb_summary_pp = df_countries_pledge_and_plan.groupby('region_wb').agg(
            Partners_List=pd.NamedAgg(column='Short name', aggfunc=lambda x: '; '.join(
                sorted(
                    set([item.strip() for sublist in x for item in sublist.split(';') 
                        if pd.notnull(item) and item.strip().lower() != 'nan'])  # Filter out 'nan'
                )
            )),
            N_Partners=pd.NamedAgg(column='Short name', aggfunc=lambda x: len(set([item.strip() for sublist in x for item in sublist.split(';') 
                                                            if pd.notnull(item) and item.strip().lower() != 'nan']))),  # Count unique partners
        ).reset_index()
        region_wb_summary_pp['% Partners'] = round((region_wb_summary_pp['N_Partners'] / n_reporting_partners)*100,1)
        region_wb_summary_pp['Category'] = 'region_wb'
        region_wb_summary_pp['Source'] = source
        region_wb_summary_pp = region_wb_summary_pp.sort_values(by='N_Partners', ascending=False)

        # Group by subregion
        subregion_summary_pp = df_countries_pledge_and_plan.groupby('subregion').agg(
            Partners_List=pd.NamedAgg(column='Short name', aggfunc=lambda x: '; '.join(
                sorted(
                    set([item.strip() for sublist in x for item in sublist.split(';') 
                        if pd.notnull(item) and item.strip().lower() != 'nan'])  # Filter out 'nan'
                )
            )),
            N_Partners=pd.NamedAgg(column='Short name', aggfunc=lambda x: len(set([item.strip() for sublist in x for item in sublist.split(';') 
                                                            if pd.notnull(item) and item.strip().lower() != 'nan']))),  # Count unique partners
        ).reset_index()
        subregion_summary_pp['% Partners'] = round((subregion_summary_pp['N_Partners'] / n_reporting_partners)*100,1)
        subregion_summary_pp['Category'] = 'subregion'
        subregion_summary_pp['Source'] = source
        subregion_summary_pp = subregion_summary_pp.sort_values(by='N_Partners', ascending=False)

        ## countries calcultation end


    # Return processed dataframes
        return df_plan_all_countries, df_countries_pledge_and_plan, region_wb_summary_pp, subregion_summary_pp,df_pledge_all_countries, region_wb_summary_pledge, subregion_summary_pledge, continent_summary_plan, region_wb_summary_plan, subregion_summary_plan
    df_plan_all_countries, df_countries_pledge_and_plan, region_wb_summary_pp, subregion_summary_pp,df_pledge_all_countries, region_wb_summary_pledge, subregion_summary_pledge, continent_summary_plan, region_wb_summary_plan, subregion_summary_plan = process_country_data(df_pledge, df_2023_plan, df_country, n_reporting_partners)

    def download_excel(data_to_display, file_name='name', title='Data Table', sheet_name='SheetName'):
        """
        Function to enable the download of a DataFrame as an Excel file in Streamlit
        with custom formatting (column width, borders, and colors), and adds a filter to all columns.
        
        Parameters:
        - data_to_display (DataFrame): The DataFrame to be downloaded.
        - file_name (str): The base name of the Excel file to download (without extension).
        - title (str): Title to add to the Excel file.
        - sheet_name (str): The name of the sheet in the Excel file.
        """
    
        # Create an in-memory buffer to store the Excel file
        buffer = io.BytesIO()

        # Get the current date and time to add to the file name and title
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        display_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Append date and time to the file name
        file_name_with_time = f"{file_name}_{current_time}.xlsx"

        # Save the sorted DataFrame to the buffer as an Excel file with custom formatting
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            # Write the sorted DataFrame to the Excel sheet
            data_to_display.to_excel(writer, index=False, sheet_name=sheet_name, startrow=2)

            # Access the workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets[sheet_name]

            # Add a title with the current date and time
            title_format = workbook.add_format({
                'bold': True,
                'font_size': 16,
                'align': 'center',
                'valign': 'vcenter'
            })
            worksheet.merge_range('A1:F1', f"{title} (Downloaded on: {display_time})", title_format)

            # Set the column width based on the length of the content in each column
            for i, col in enumerate(data_to_display.columns):
                max_len = max(data_to_display[col].astype(str).map(len).max(), len(col)) + 2  # Adjust column width
                worksheet.set_column(i, i, max_len)

            # Define a format for the header row (first row)
            header_format = workbook.add_format({
                'bold': True,
                'bg_color': '#FF37D5',
                'font_color': 'white',
                'border': 1
            })

            # Define a format for the rest of the cells (with borders)
            cell_format = workbook.add_format({
                'border': 1
            })

            # Apply header format to the first row (row 2 in this case, since data starts at row 2)
            for col_num, value in enumerate(data_to_display.columns):
                worksheet.write(2, col_num, value, header_format)

            # Apply formatting to all the data in the table
            for row_num, row_data in data_to_display.iterrows():
                for col_num, value in enumerate(row_data):
                    worksheet.write(row_num + 3, col_num, value, cell_format)  # Apply general cell format

            # Add an autofilter to all columns starting from the header row
            worksheet.autofilter(2, 0, len(data_to_display) + 2, len(data_to_display.columns) - 1)

        # Set the buffer's position back to the start
        buffer.seek(0)

        # Create the download button in Streamlit with the new file name
        st.download_button(
            label="Download data as Excel",
            data=buffer,
            file_name=file_name_with_time,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    def safe_numerize(value):
        """
        Safely convert a value to a numerized string, handling numpy types.
        """
        if isinstance(value, (np.int64, np.int32, np.float64, np.float32)):
            value = int(value)
        return numerize(value)
    def display_top_results(data, variable, selected_dataset, variable_name, top_n):
        """
        Function to display the top results for a given dataset.

        Parameters:
        - data (DataFrame): The DataFrame containing the data.
        - variable (str): The column to rank.
        - selected_dataset (str): Dataset name to be included in the description.
        - variable_name (str): The name of the variable to describe in the output.
        - top_n (int): Number of top items to display. Default is 7.
        """
        # st.write("### Results")
        
        # Create variables for the top results
        for i in range(top_n):
            globals()[f"top_{i+1}"] = data[variable].iloc[i]
            globals()[f"top_{i+1}_n_partner"] = data['N_Partners'].iloc[i]
            # st.write(f"{globals()[f'top_{i+1}']} with {globals()[f'top_{i+1}_n_partner']} partners")
        
        # Generate the description for the top results
        description_parts = []
        for i in range(top_n):
            top_variable = data[variable].iloc[i]
            top_n_partner = data['N_Partners'].iloc[i]
            description_parts.append(f"{top_variable} ({safe_numerize(top_n_partner)})")

        # Handling the "and" for the last item in the list
        if len(description_parts) > 1:
            description_str = ", ".join(description_parts[:-1]) + f", and {description_parts[-1]}"
        else:
            description_str = description_parts[0]  # In case there's only one item

        # Create the final description
        description_top_results = (
            f"In the  {selected_dataset}, the top {top_n} {variable_name} by number of partners are "
            + description_str
        )
        # Display the description
        # st.markdown(description_top_results)
        st.markdown(f"""
                        <blockquote style="background-color: #f9f9f9; border-left: 10px solid #ccc; margin: 1.5em 10px; padding: 0.5em 10px;">
                        {description_top_results.strip()}
                        </blockquote>
                        """, unsafe_allow_html=True)
    
        
    def create_world_map(data, columns, political_countries_url, key_on, label_to_chart):
        """
        Function to create and display a world map with choropleth and a custom legend.
        
        Parameters:
        - data (DataFrame or dict): The dataset to visualize on the map.
        - columns (list): Two columns: geographical identifiers and the values.
        - political_countries_url (str): The URL to the GeoJSON file defining country borders.
        - key_on (str): The GeoJSON feature key for linking data to the map.
        - label_to_chart (str): The label to display in the legend and map name.
        """
        if data is not None and columns is not None:
            # Create the map
            world_map_full = folium.Map(location=(0, 0), zoom_start=1.4, tiles="cartodb positron")

            # Add choropleth to the map
            folium.Choropleth(
                geo_data=political_countries_url,
                data=data,
                columns=columns,
                key_on=key_on,
                fill_color="RdPu",
                nan_fill_color="white",
                nan_fill_opacity=0.5,
                fill_opacity=0.7,
                line_opacity=0.2,
                highlight=True,
                name=label_to_chart,
                legend_name=f"{label_to_chart}"  # Legend label
            ).add_to(world_map_full)

            # Display the map
            st_folium(world_map_full, width=925, key="map1")

    def display_geographic_outreach(df_countries_pledge_and_plan, region_wb_summary_pp, subregion_summary_pp,
                                    df_pledge_all_countries, region_wb_summary_pledge, subregion_summary_pledge,
                                    df_plan_all_countries, region_wb_summary_plan, subregion_summary_plan,
                                    political_countries_url, n_all_rtrpartners, n_reporting_partners, n_newpartners):
        

        st.write("### RtR Partners' Global Outreach")
    
        selected_dataset = st.radio(
                "Select a source of information to display the geographic outreach of RtR Partners",
                ["RtR Partners' Pledges", "RtR Partners' Resilience Building Plans","RtR Partners' pledges and plans (all sources)" ]
            )
            
        
        if selected_dataset == "RtR Partners' pledges and plans (all sources)":
            col1, col2 = st.columns(2)
            df_countries_filter_result = df_countries_pledge_and_plan
            source = "Pledge and Plan"
            n_countries_pledge_and_plan = df_countries_pledge_and_plan['country'].count()
            col2.metric(label="Countries with RtR Partners' pledges and plans", value=n_countries_pledge_and_plan)
            
            
            selected_section = col1.radio(
            "Select the type of aggregation level: by country, by region, or by subregion.",
            ['Country Level', 'Region Level', 'Subregion Level']
            )


            if selected_section == 'Country Level':
                # st.write('df_countries_pledge_and_plan', df_countries_pledge_and_plan)
                columns = ["country_to_plot", 'N_Partners']  # Two columns: geographical and data
                data = df_countries_filter_result  # Data to visualize
                key_on = "feature.properties.name"
                label_to_chart = "Countries with RtR Partners' pledges and plans (partners per country)."
                variable = 'country_to_plot'
                variable_name ="countries"
                sheet_name = f"{selected_section}_{source}"
                top_n = 10
                display_top_results(data, variable, selected_dataset, variable_name, top_n)
                create_world_map(data, columns, political_countries_url, key_on, label_to_chart)
                
                ##Data to display countries
                data_country_list = ['country','N_Partners','Short name','region_wb','subregion','Source']
                data_to_display = data[data_country_list]
                data_to_display = data_to_display.rename(columns={
                    'country': 'Country',
                    'N_Partners': 'N° Partners', 
                    'Short name': "RtR Partners' Short Name",
                    'region_wb': 'Region',
                    'subregion': 'Subregion',
                    'Source': 'Data Source'
                })
                data_to_display = data_to_display.sort_values(by=data_to_display.columns[1], ascending=False)
                
                with st.expander(f"Explore and download data on {selected_dataset} from {variable_name}"):
                    st.write(f"#### {label_to_chart} Source: {source}")
                    st.dataframe(data_to_display.reset_index(drop=True))
                    download_excel(data_to_display, file_name=label_to_chart, title=label_to_chart,sheet_name = sheet_name )
            

            elif selected_section == 'Region Level':
                # st.write('region_wb_summary_pp', region_wb_summary_pp)
                columns = ["region_wb", 'N_Partners']
                data = region_wb_summary_pp
                key_on = "feature.properties.region_wb"
                label_to_chart = "Regions with RtR Partners' pledges and plans (partners per region)."
                dataset = region_wb_summary_pp
                variable = 'region_wb'
                variable_name ="regions"
                sheet_name = f"{selected_section}_{source}"
                top_n = 5
                display_top_results(data, variable, selected_dataset, variable_name, top_n)
                create_world_map(data, columns, political_countries_url, key_on, label_to_chart)
                
                ##Data to display regions
                data_to_display = data[['region_wb','N_Partners','Partners_List','Source']]
                data_to_display = data_to_display.rename(columns={
                    'region_wb': 'Regions',
                    'N_Partners': 'N° Partners', 
                    'Partners_List':"RtR Partners' Short Name",
                    'Source': 'Data Source'
                })
                data_to_display = data_to_display.sort_values(by=data_to_display.columns[1], ascending=False)
                with st.expander(f"Explore and download data on {selected_dataset} from {variable_name}"):
                    st.write(f"#### {label_to_chart} Source: {source}")
                    st.dataframe(data_to_display.reset_index(drop=True))
                    
                    download_excel(data_to_display, file_name=label_to_chart, title=label_to_chart,sheet_name = sheet_name )
                

            elif selected_section == 'Subregion Level':
                # st.write('subregion_summary_pp', subregion_summary_pp)
                columns = ["subregion", 'N_Partners']
                data = subregion_summary_pp
                key_on = "feature.properties.subregion"
                label_to_chart = "Subregions with RtR Partners' pledges and plans (partners per subregion)."
                variable = 'subregion'
                variable_name ="subregions"
                sheet_name = f"{selected_section}_{source}"
                top_n = 5
                display_top_results(data, variable, selected_dataset, variable_name, top_n)
                create_world_map(data, columns, political_countries_url, key_on, label_to_chart)
            
                ##Data to display subregions
                data_to_display = data[['subregion','N_Partners','Partners_List','Source']]
                data_to_display = data_to_display.rename(columns={
                    'subregion': 'Subregions',
                    'N_Partners': 'N° Partners', 
                    'Partners_List':"RtR Partners' Short Name",
                    'Source': 'Data Source'
                })
                data_to_display = data_to_display.sort_values(by=data_to_display.columns[1], ascending=False)
                with st.expander(f"Explore and download data on {selected_dataset} from {variable_name}"):
                    st.write(f"#### {label_to_chart} Source: {source}")
                    st.dataframe(data_to_display.reset_index(drop=True))
                    
                    download_excel(data_to_display, file_name=label_to_chart, title=label_to_chart,sheet_name = sheet_name )
                    
        elif selected_dataset == "RtR Partners' Pledges":
            col1, col2 = st.columns(2)
            df_countries_filter_result = df_pledge_all_countries
            source = "Pledge"
            n_countries_pledge = df_countries_filter_result['country'].count()
            col2.metric(label="Countries with RtR Partners' pledges", value=n_countries_pledge)
            
            
            selected_section = col1.radio(
            "Select the type of aggregation level: by country, by region, or by subregion.",
            ['Country Level', 'Region Level', 'Subregion Level']
        )

            if selected_section == 'Country Level':
                # st.write('df_pledge_all_countries', df_pledge_all_countries)
                columns = ["country_to_plot", 'N_Partners']  # Two columns: geographical and data
                data = df_pledge_all_countries  # Data to visualize
                key_on = "feature.properties.name"
                label_to_chart = "Countries with RtR Partners' pledges (partners per country)."
                variable = 'country_to_plot'
                variable_name ="countries"
                sheet_name = f"{selected_section}_{source}"
                top_n = 10
                display_top_results(data, variable, selected_dataset, variable_name, top_n)
                create_world_map(data, columns, political_countries_url, key_on, label_to_chart)
                
                
                ##Data to display countries
                data_country_list = ['country','N_Partners','Short name','region_wb','subregion','Source']
                data_to_display = data[data_country_list]
                data_to_display = data_to_display.rename(columns={
                    'country': 'Country',
                    'N_Partners': 'N° Partners',  # Corrected 'Partenrs' to 'Partners'
                    'Short name': "RtR Partners' Short Name",
                    'region_wb': 'Region',
                    'subregion': 'Subregion',
                    'Source': 'Data Source'
                })
                data_to_display = data_to_display.sort_values(by=data_to_display.columns[1], ascending=False)
                
                with st.expander(f"Explore and download data on {selected_dataset} from {variable_name}"):
                    st.write(f"#### {label_to_chart} Source: {source}")
                    st.dataframe(data_to_display.reset_index(drop=True))
                    
                    download_excel(data_to_display, file_name=label_to_chart, title=label_to_chart,sheet_name = sheet_name )
                



            elif selected_section == 'Region Level':
                # st.write('region_wb_summary_pledge', region_wb_summary_pledge)
                columns = ["region_wb", 'N_Partners']
                data = region_wb_summary_pledge
                key_on = "feature.properties.region_wb"
                label_to_chart = "Regions with RtR Partners' pledges (partners per region)."
                variable = 'region_wb'
                variable_name ="regions"
                sheet_name = f"{selected_section}_{source}"
                top_n = 5
                display_top_results(data, variable, selected_dataset, variable_name, top_n)
                create_world_map(data, columns, political_countries_url, key_on, label_to_chart)
                
                ##Data to display regions
                data_to_display = data[['region_wb','N_Partners','Partners_List','Source']]
                data_to_display = data_to_display.rename(columns={
                    'region_wb': 'Regions',
                    'N_Partners': 'N° Partners', 
                    'Partners_List':"RtR Partners' Short Name",
                    'Source': 'Data Source'
                })
                data_to_display = data_to_display.sort_values(by=data_to_display.columns[1], ascending=False)
                
                
                with st.expander(f"Explore and download data on {selected_dataset} from {variable_name}"):
                    st.write(f"#### {label_to_chart} Source: {source}")
                    st.dataframe(data_to_display.reset_index(drop=True))
                    
                    download_excel(data_to_display, file_name=label_to_chart, title=label_to_chart,sheet_name = sheet_name )
                

            elif selected_section == 'Subregion Level':
                # st.write('subregion_summary_pledge', subregion_summary_pledge)
                columns = ["subregion", 'N_Partners']
                data = subregion_summary_pledge
                key_on = "feature.properties.subregion"
                label_to_chart = "Regions with RtR Partners' pledges (partners per region)."
                variable = 'subregion'
                variable_name ="subregions"
                sheet_name = f"{selected_section}_{source}"
                top_n = 5
                display_top_results(data, variable, selected_dataset, variable_name, top_n)
                create_world_map(data, columns, political_countries_url, key_on, label_to_chart)
                
                ##Data to display subregions
                data_to_display = data[['subregion','N_Partners','Partners_List','Source']]
                data_to_display = data_to_display.rename(columns={
                    'subregion': 'Subregions',
                    'N_Partners': 'N° Partners', 
                    'Partners_List':"RtR Partners' Short Name",
                    'Source': 'Data Source'
                })
                data_to_display = data_to_display.sort_values(by=data_to_display.columns[1], ascending=False)
                
                
                with st.expander(f"Explore and download data on {selected_dataset} from {variable_name}"):
                    st.write(f"#### {label_to_chart} Source: {source}")
                    st.dataframe(data_to_display.reset_index(drop=True))
                    
                    download_excel(data_to_display, file_name=label_to_chart, title=label_to_chart,sheet_name = sheet_name )
        elif selected_dataset == "RtR Partners' Resilience Building Plans":
            col1, col2 = st.columns(2)
            df_countries_filter_result = df_plan_all_countries
            source = "Plan"
            n_countries_plan = df_countries_filter_result['country'].count()
            col2.metric(label="Countries with RtR Partners' Plans", value=n_countries_plan)
            
            selected_section = col1.radio(
            "Select the type of aggregation level: by country, by region, or by subregion.",
            ['Country Level', 'Region Level', 'Subregion Level']
        )

            if selected_section == 'Country Level':
                # st.write('df_plan_all_countries', df_plan_all_countries)
                columns = ["country_to_plot", 'N_Partners']  # Two columns: geographical and data
                data = df_plan_all_countries  # Data to visualize
                key_on = "feature.properties.name"
                label_to_chart = "Countries with RtR Partners' plans (partners per country)."
                variable = 'country_to_plot'
                variable_name ="countries"
                sheet_name = f"{selected_section}_{source}"
                top_n = 10
                display_top_results(data, variable, selected_dataset, variable_name, top_n)
                create_world_map(data, columns, political_countries_url, key_on, label_to_chart)
                
                ##Data to display countries
                data_country_list = ['country','N_Partners','Short name','region_wb','subregion','Source']
                data_to_display = data[data_country_list]
                data_to_display = data_to_display.rename(columns={
                    'country': 'Country',
                    'N_Partners': 'N° Partners',  # Corrected 'Partenrs' to 'Partners'
                    'Short name': "RtR Partners' Short Name",
                    'region_wb': 'Region',
                    'subregion': 'Subregion',
                    'Source': 'Data Source'
                })
                data_to_display = data_to_display.sort_values(by=data_to_display.columns[1], ascending=False)
                
                st.write(data_to_display)
                
                
                with st.expander(f"Explore and download data on {selected_dataset} from {variable_name}"):
                    st.write(f"#### {label_to_chart} Source: {source}")
                    st.dataframe(data_to_display.reset_index(drop=True))
                    
                    download_excel(data_to_display, file_name=label_to_chart, title=label_to_chart,sheet_name = sheet_name )
                


            elif selected_section == 'Region Level':
                # st.write('region_wb_summary_plan', region_wb_summary_plan)
                columns = ["region_wb", 'N_Partners']
                data = region_wb_summary_plan
                key_on = "feature.properties.region_wb"
                label_to_chart = "Regions with RtR Partners' plans (partners per region)."
                dataset = region_wb_summary_plan
                variable = 'region_wb'
                variable_name ="regions"
                sheet_name = f"{selected_section}_{source}"  
                top_n = 5
                display_top_results(data, variable, selected_dataset, variable_name, top_n)
                create_world_map(data, columns, political_countries_url, key_on, label_to_chart)
                
                ##Data to display regions
                data_to_display = data[['region_wb','N_Partners','Partners_List','Source']]
                data_to_display = data_to_display.rename(columns={
                    'region_wb': 'Regions',
                    'N_Partners': 'N° Partners', 
                    'Partners_List':"RtR Partners' Short Name",
                    'Source': 'Data Source'
                })
                data_to_display = data_to_display.sort_values(by=data_to_display.columns[1], ascending=False)
                
                
                with st.expander(f"Explore and download data on {selected_dataset} from {variable_name}"):
                    st.write(f"#### {label_to_chart} Source: {source}")
                    st.dataframe(data_to_display.reset_index(drop=True))
                    
                    download_excel(data_to_display, file_name=label_to_chart, title=label_to_chart,sheet_name = sheet_name )
                

            elif selected_section == 'Subregion Level':
                # st.write('subregion_summary_plan', subregion_summary_plan)
                columns = ["subregion", 'N_Partners']
                data = subregion_summary_plan
                key_on = "feature.properties.subregion"
                label_to_chart = "Subregions with RtR Partners' plans (partners per subregion)."
                variable = 'subregion'
                variable_name ="subregions"  
                sheet_name = f"{selected_section}_{source}"
                top_n = 5
                display_top_results(data, variable, selected_dataset, variable_name, top_n)
                create_world_map(data, columns, political_countries_url, key_on, label_to_chart)
                
                ##Data to display subregions
                data_to_display = data[['subregion','N_Partners','Partners_List','Source']]
                data_to_display = data_to_display.rename(columns={
                    'subregion': 'Subregions',
                    'N_Partners': 'N° Partners', 
                    'Partners_List':"RtR Partners' Short Name",
                    'Source': 'Data Source'
                })
                data_to_display = data_to_display.sort_values(by=data_to_display.columns[1], ascending=False)
                
                
                with st.expander(f"Explore and download data on {selected_dataset} from {variable_name}"):
                    st.write(f"#### {label_to_chart} Source: {source}")
                    st.dataframe(data_to_display.reset_index(drop=True))
                    
                    download_excel(data_to_display, file_name=label_to_chart, title=label_to_chart,sheet_name = sheet_name )


    display_geographic_outreach(df_countries_pledge_and_plan, region_wb_summary_pp, subregion_summary_pp,
                                    df_pledge_all_countries, region_wb_summary_pledge, subregion_summary_pledge,
                                    df_plan_all_countries, region_wb_summary_plan, subregion_summary_plan,
                                    political_countries_url, n_all_rtrpartners, n_reporting_partners, n_newpartners)
# global_outreach()


def transparency_reporting(df_partner_campaign_tracker,df_pledge,df_2023_plan,reporting_partners_in_2022_cop27, reporting_partners_in_2023_cop28, n_reporting_partners,
                                n_partner_gi_in_2022, n_partner_gi_in_2023, n_partner_gi,
                                n_initiatives_gi_pending_2022, n_initiatives_gi_pending_2023, n_initiatives_gi_pending):
    
    #Reporting GI Partners historical
    def plot_gi_historical_chart(reporting_partners_in_2022_cop27, reporting_partners_in_2023_cop28, n_reporting_partners,
                                n_partner_gi_in_2022, n_partner_gi_in_2023, n_partner_gi,
                                n_initiatives_gi_pending_2022, n_initiatives_gi_pending_2023, n_initiatives_gi_pending):


        ## CHART 2024 GI HISTORICAL
        years = ['2022', '2023', '2024']
        all_partners = [reporting_partners_in_2022_cop27, reporting_partners_in_2023_cop28, n_reporting_partners]
        reporting_partners_gi = [n_partner_gi_in_2022, n_partner_gi_in_2023, n_partner_gi]
        pending_reporting_partners_gi = [n_initiatives_gi_pending_2022, n_initiatives_gi_pending_2023, n_initiatives_gi_pending]
        colors = sns.color_palette("RdPu", n_colors=3)

        # Create a bar chart
        fig, ax = plt.subplots(figsize=(10, 4))
        bar_width = 0.3
        index = range(len(years))

        # Plotting the bars
        bars_all = ax.bar(index, all_partners, width=bar_width, label='Reporting Partners', color=colors[0])
        bars_reporting_gi = ax.bar([i + bar_width for i in index], reporting_partners_gi, width=bar_width, label='Partners Reporting GI', color=colors[1])
        bars_pending = ax.bar([i + 2 * bar_width for i in index], pending_reporting_partners_gi, width=bar_width, label='Partners Pending GI', color=colors[2])

        # Adding labels and title
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Reporting Partners')
        ax.set_title('Partners Reporting General Information Survey Over Years')
        ax.set_xticks([i + bar_width for i in index])  # Adjust the tick positions
        ax.set_xticklabels(years)
        ax.legend()

        # Adding the number above each bar
        def add_value_labels(bars):
            for bar in bars:
                yval = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    yval + 0.1,
                    int(yval),
                    ha='center',
                    va='bottom',
                    fontsize=10,
                    color='black'
                )
        # Remove top and right spines (borders)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        # Apply the function to all bars
        add_value_labels(bars_all)
        add_value_labels(bars_reporting_gi)
        add_value_labels(bars_pending)

        # Display the chart in Streamlit
        st.pyplot(fig)
    # plot_gi_historical_chart(reporting_partners_in_2022_cop27, reporting_partners_in_2023_cop28, n_reporting_partners,n_partner_gi_in_2022, n_partner_gi_in_2023, n_partner_gi,n_initiatives_gi_pending_2022, n_initiatives_gi_pending_2023, n_initiatives_gi_pending)
        
    ## COMPLETENESS INDEX
    def pledge_completeness_index(df_pledge):

        # Define the PLEDGE OVERALL INDEX
        pledge_overall_index_list = ['responder_id_pledge_subidx',
                                    'p_benefic_all_pledge_subidx',
                                    'locally_led_commitment_pledge_subidx',
                                    'finance_pledge_subidx',
                                    'metrics_explanation_pledge_subidx',
                                    'climate_risk_assess_pledge_subidx',
                                    'climate_diagnost_pledge_subidx',
                                    'members_consultation_pledge_subidx',
                                    'confirmation_future_plans_pledge_subidx']

        # Replace np.nan values with 0 in the specified columns of df_pledge
        df_pledge[pledge_overall_index_list] = df_pledge[pledge_overall_index_list].fillna(0)

        # Filter the dataset to only include rows where pledge_completeness_idx > 0
        df_filtered = df_pledge[df_pledge['pledge_completeness_idx'] > 0]

        # Mapping technical names to readable labels
        label_mapping = {
            'responder_id_pledge_subidx': 'Responder Identification',
            'p_benefic_all_pledge_subidx': 'Pledge Beneficiaries',
            'locally_led_commitment_pledge_subidx': 'Locally Led Commitment',
            'finance_pledge_subidx': 'Finance Information',
            'metrics_explanation_pledge_subidx': 'Metrics Explanation',
            'climate_risk_assess_pledge_subidx': 'Climate Risk Assessment',
            'climate_diagnost_pledge_subidx': 'Climate Diagnostics',
            'members_consultation_pledge_subidx': 'Members Consultation',
            'confirmation_future_plans_pledge_subidx': 'Confirmation of Future Plans'
        }

        # Calculate the mean of each index dimension (simple mean)
        mean_values = df_filtered[pledge_overall_index_list].mean()
        mean_values.index = mean_values.index.map(label_mapping)

        # Sort the mean values for better presentation
        mean_values = mean_values.sort_values(ascending=True)

        # Calculate the total number of partners (100%) after filtering
        total_partners = df_filtered.shape[0]

        # Create a bar chart with mean values and total partners text
        def plot_mean_dimension_chart(mean_values, total_partners):
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.barh(mean_values.index, mean_values.values, color='#FF37D5')
            
            # Add labels to bars
            for i in range(len(mean_values)):
                ax.text(mean_values.values[i] + 0.01, i, f'{mean_values.values[i]:.2f} %', va='center')
            
            # Add total partners text below the chart
            plt.figtext(0.99, 0.01, f'N Partners = {total_partners}',
                        horizontalalignment='right', fontsize=10, weight='bold')
            
            ax.set_xlabel('Mean Value (%)')
            ax.set_title('Mean of Each Dimension of the Pledge Completeness Index')
            
            # Remove top and right spines (borders)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.tight_layout()
            st.pyplot(fig)

        # Display the chart in Streamlit
        st.title('Pledge Index Dimensions Overview')
        st.write("This chart shows the mean value of each dimension of the pledge index.")
        plot_mean_dimension_chart(mean_values, total_partners)
    # pledge_completeness_index(df_pledge)

    def plan_completeness_index(df_2023_plan):
        # Define the PLAN COMPLETENESS INDEX
        plan_completeness_index_list = ['plan_identif_subidx',
                                        'description_plan_subidx',
                                        'saa_plan_subidx',
                                        'ra_plan_subidx',
                                        'pri_benef_magnitud_plan_subidx',
                                        'governance_plan_subidx',
                                        'barriers_plan_subidx',
                                        'finance_plan_subidx',
                                        'monitoring_data_collect_plan_subidx']

        # Replace np.nan values with 0 in the specified columns of df_2023_plan
        df_2023_plan[plan_completeness_index_list] = df_2023_plan[plan_completeness_index_list].fillna(0)

        # Mapping technical names to readable labels
        label_mapping = {
            'plan_identif_subidx': 'Plan Identification',
            'description_plan_subidx': 'Description of the Plan',
            'saa_plan_subidx': 'SAA Priority Systems Allignment',
            'ra_plan_subidx': 'Resilience Attributes Information',
            'pri_benef_magnitud_plan_subidx': 'Priority Beneficiaries Magnitude',
            'governance_plan_subidx': 'Governance Information',
            'barriers_plan_subidx': 'Barriers Identification',
            'finance_plan_subidx': 'Planned Finance Mobilization',
            'monitoring_data_collect_plan_subidx': 'Monitoring & Data Collection'
        }

        # Calculate the plan completeness index 
        df_2023_plan['plan_completeness_idx'] = df_2023_plan.apply(
            lambda row: sum(row[col] for col in plan_completeness_index_list if col in row),
            axis=1
        )

        # Filter the dataset to only include rows where plan_completeness_idx > 0
        df_filtered = df_2023_plan[df_2023_plan['plan_completeness_idx'] > 0]

        # Calculate the mean of each index dimension (simple mean)
        mean_values = df_filtered[plan_completeness_index_list].mean()
        mean_values.index = mean_values.index.map(label_mapping)

        # Sort the mean values for better presentation
        mean_values = mean_values.sort_values(ascending=True)

        # Calculate the total number of plans (100%) after filtering
        total_plans = df_filtered.shape[0]

        # Create a bar chart with mean values and total plans text
        def plot_mean_dimension_chart(mean_values, total_plans):
            fig, ax = plt.subplots(figsize=(10, 4))
            ax.barh(mean_values.index, mean_values.values, color='#FF37D5')
            
            # Add labels to bars
            for i in range(len(mean_values)):
                ax.text(mean_values.values[i] + 0.01, i, f'{mean_values.values[i]:.2f} %', va='center')
            
            # Add total plans text below the chart
            plt.figtext(0.99, 0.01, f'N Plans = {total_plans}',
                        horizontalalignment='right', fontsize=10, weight='bold')
            
            ax.set_xlabel('Mean Value (%)')
            ax.set_title('Mean of Each Dimension of the Plan Completeness Index')
            
            # Remove top and right spines (borders)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            
            plt.tight_layout()
            st.pyplot(fig)

        # Display the chart in Streamlit
        st.title('Plan Index Dimensions Overview')
        st.write("This chart shows the mean value of each dimension of the plan completeness index.")
        plot_mean_dimension_chart(mean_values, total_plans)
    # plan_completeness_index(df_2023_plan)
        
    

    st.markdown("### TRANSPARENCY AND REPORTING")
    st.markdown("##### Content for this section is under development")
    st.caption("A dedicated space for reporting the statuses of partners, including the latest tools and reports for 2023.")
    # long_description = f"""
    #     Transparent reporting is crucial for demonstrating climate adaptation progress - to build trust, strengthen accountability, and inform evidence-based policies. While speed of progress varies based on each partner's capacity and the year in which they joined, to date {numerize(percent_partner_gi)}% of reporting partners have responded General Information Tool, {numerize(percentaje_reporting_partner_pledge_2023)}% have submitted a pledge, {numerize(percentaje_reporting_partner_plan_consolidated)}% of partners submitted an action plan and almost {numerize(percentaje_partner_reporting_adaptation_finance_consolidated)}% of partners reported the adaptation finance mobilised.
    #     """
    # st.markdown(long_description)

    list_transparency = [
    'InitName',
    'Org_Type',
    'reporting_cycle_status',
    'gi_completeness_idx',
    'gi_confidence_members_overall_idx',
    'gi_overall_status',
    'pledge_completeness_idx',
    'pledge_confidence_overall_idx',
    'pledge_overall_status',
    'number_of_plans',
    'all_plans_completeness_idx_mean',
    'all_plans_confidence_idx_mean',
    'all_plan_overall_status',
    ]

    df_partner_campaign_tracker = df_partner_campaign_tracker[list_transparency]

    def add_newline_skip_first(text):
        if isinstance(text, str):  # Ensure the input is a string
            parts = text.split('#', 1)  # Split only at the first '#'
            if len(parts) > 1:
                # Add newline after each subsequent '#'
                parts[1] = parts[1].replace('#', '\n\n')
            return '#'.join(parts)
        return text

    # Apply the function to the 'reporting_cycle_status' column
    df_partner_campaign_tracker["reporting_cycle_status"] = df_partner_campaign_tracker["reporting_cycle_status"].apply(add_newline_skip_first)

    # n_gi_2022 = 26  #Source Data Explorer 2023
    # n_pledge_2022 = 23 #Source Data Explorer 2023
    # n_plans_2022 = 0 #Source Data Explorer 2023
    # n_finance_plans_2022 = 0 #Source Data Explorer 2023

    # n_gi_2023 = 28
    # n_pledge_2023 = 25
    # n_plans_2023 = 21
    # n_finance_plans_2023= 15

    # n_gi_2024 = n_partner_gi  
    # n_pledge_2024 = n_partner_pledge 
    # n_plans_2024 = n_partners_plan
    # n_finance_plans_2024= dollars_mobilized_all_plans_n_partners 

    # Total = n_reporting_partners 


    tab1, tab2, tab3, tab4, tab5 = st.tabs(["All Stages", "General Information", "Pledge Statements","Plans","Proceed (Pilot)"])

    with tab1:
        list_filter_summary = [
        'InitName',
        'Org_Type',
        'reporting_cycle_status']
        st.dataframe(df_partner_campaign_tracker[list_filter_summary],hide_index=True)

    with tab2:
        plot_gi_historical_chart(reporting_partners_in_2022_cop27, reporting_partners_in_2023_cop28, n_reporting_partners,n_partner_gi_in_2022, n_partner_gi_in_2023, n_partner_gi,n_initiatives_gi_pending_2022, n_initiatives_gi_pending_2023, n_initiatives_gi_pending)
        list_filter_summary_gi = ['InitName',
        'Org_Type',
        'gi_completeness_idx',
        'gi_confidence_members_overall_idx',
        'gi_overall_status']
        st.dataframe(df_partner_campaign_tracker[list_filter_summary_gi],hide_index=True)

    with tab3: 
        pledge_completeness_index(df_pledge)
        list_filter_summary_pledge = ['InitName',
        'Org_Type',
        'pledge_completeness_idx',
        'pledge_confidence_overall_idx',
        'pledge_overall_status',]
        st.dataframe(df_partner_campaign_tracker[list_filter_summary_pledge],hide_index=True)
        
    with tab4: 
        plan_completeness_index(df_2023_plan) 
        list_filter_summary_plan = ['InitName',
        'Org_Type',
        'number_of_plans',
        'all_plans_completeness_idx_mean',
        'all_plans_confidence_idx_mean',
        'all_plan_overall_status',]
        st.dataframe(df_partner_campaign_tracker[list_filter_summary_plan],hide_index=True)
        
    with tab5:  
        st.write("List of Partners in Proceed. Pending")





## OTHERS
# SUMARY OF REPORTING PARTNERS [REPORTING PARTNERS]
def generate_partner_overview(n_all_rtrpartners, n_reporting_partners, n_newpartners):
    """
    Generates a description for the campaign partner overview.

    Parameters:
    - n_all_rtrpartners (int): The total number of campaign partners in 2024.
    - n_reporting_partners (int): The number of partners who have submitted their reports for 2024.
    - n_newpartners (int): The number of new partners starting in 2025.

    Returns:
    - long_description (str): The dynamically generated description for the campaign partner overview.
    """
    
    # Generate the description text
    long_description = f"""
    In 2024, the campaign reached {n_all_rtrpartners} campaign partners. Of these, {n_reporting_partners} partners have 
    submitted their reports for the 2024 reporting cycle, while {n_newpartners} new partners will start their journey in 2025.
    """
    
    # Display the description using markdown
    st.markdown(f"""
                    <blockquote style="background-color: #f9f9f9; border-left: 10px solid #ccc; margin: 1.5em 10px; padding: 0.5em 10px;">
                    {long_description.strip()}
                    </blockquote>
                    """, unsafe_allow_html=True)
# generate_partner_overview(n_all_rtrpartners, n_reporting_partners, n_newpartners)
    
#Member Information
def members_historical_2022_2024(Members_organizations_22,Members_organizations_23,Members_organizations_24,
                                 Members_organizations_22_n_partners,Members_organizations_23_n_partners,Members_organizations_24_n_partners):
    ## Partners' Members related to RtR Campaign Over the Years (2022 al 2024)
    ## CHART MEMBERS HISTORICAL 2022-2024
    years = ['2022', '2023', '2024']
    n_members_total_list = [Members_organizations_22, Members_organizations_23, Members_organizations_24]
    reporting_partners_members = [Members_organizations_22_n_partners, Members_organizations_23_n_partners, Members_organizations_24_n_partners]

    colors = sns.color_palette("RdPu", n_colors=3)

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 4))
    bar_width = 0.6
    index = range(len(years))

    # Plotting the bars
    bars_all = ax.bar(index, n_members_total_list, width=bar_width, label='Members', color=colors[0])

    # Adding labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Members')
    ax.set_title("Partners' Members related to RtR Campaign Over the Years (2022 al 2024)", pad=20) 

    # Adjust the tick positions to center the labels
    ax.set_xticks([i for i in index])
    ax.set_xticklabels(years)
    ax.legend()

    # Adding the number above each bar with the additional text
    def add_value_labels(bars, partners_values):
        for i, bar in enumerate(bars):
            yval = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                yval + 0.1,
                f'{int(yval)}\n(Out of {int(partners_values[i])} Partners)',
                ha='center',
                va='bottom',
                fontsize=10,
                color='black'
            )

    # Remove top and right spines (borders)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Apply the function to all bars with the corresponding reporting partners values
    add_value_labels(bars_all, reporting_partners_members)

    # Display the chart in Streamlit
    st.pyplot(fig)
# members_historical_2022_2024(Members_organizations_22,Members_organizations_23,Members_organizations_24,Members_organizations_22_n_partners,Members_organizations_23_n_partners,Members_organizations_24_n_partners)

def members_historical_2023_2024(Members_organizations_23,Members_organizations_24,
                                 Members_organizations_23_n_partners,Members_organizations_24_n_partners):
    ## Partners' Members related to RtR Campaign (2023 to 2024)
    ## CHART MEMBERS HISTORICAL 2023-2024
    years = ['2023', '2024']
    n_members_total_list = [Members_organizations_23, Members_organizations_24]
    reporting_partners_members = [Members_organizations_23_n_partners, Members_organizations_24_n_partners]

    colors = sns.color_palette("RdPu", n_colors=3)

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 2))
    bar_width = 0.4
    index = range(len(years))

    # Plotting the bars
    bars_all = ax.bar(index, n_members_total_list, width=bar_width, label='Members', color=colors[0])

    # Adding labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Number of Members')
    ax.set_title("Partners' Members related to RtR Campaign (2023 to 2024)", pad=30) 

    # Adjust the tick positions to center the labels
    ax.set_xticks([i for i in index])
    ax.set_xticklabels(years)
    # ax.legend()

    # Adding the number above each bar with the additional text
    def add_value_labels(bars, partners_values):
        for i, bar in enumerate(bars):
            yval = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                yval + 0.1,
                f'{int(yval)} Members\n(Out of {int(partners_values[i])} Partners)',
                ha='center',
                va='bottom',
                fontsize=10,
                color='black'
            )

    # Remove top and right spines (borders)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Apply the function to all bars with the corresponding reporting partners values
    add_value_labels(bars_all, reporting_partners_members)

    # Display the chart in Streamlit
    st.pyplot(fig)
# members_historical_2023_2024(Members_organizations_23,Members_organizations_24,Members_organizations_23_n_partners,Members_organizations_24_n_partners)

# INDIVIDUALS [METRICS]
## METRICAS INDIVIDUALS ONLY PLEDGE
def individuals_pledge_2022_2024(n_individuals_pledge_in_2022, n_individuals_pledge_in_2023, n_individuals_pledge_in_2024):

    ## CHART N Individuals Pledge Historical
    years = ['2022 COP27', '2023 COP28', '2024 COP29']
    n_hectareas_plan_tochart_list = [n_individuals_pledge_in_2022, n_individuals_pledge_in_2023, n_individuals_pledge_in_2024]

    colors = sns.color_palette("RdPu", n_colors=4)

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 2))
    bar_width = 0.6
    index = range(len(years))

    # Plotting the bars
    bars_all = ax.bar(index, n_hectareas_plan_tochart_list, width=bar_width, label='N° Individuals ', color=colors)

    # Adding labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('N° Individuals Pledged')
    ax.set_title("N° Individuals Pledged to RtR Campaign Over the Years (2022 to 2024)", pad=20)

    # Adjust the tick positions to center the labels
    ax.set_xticks([i for i in index])
    ax.set_xticklabels(years)
    # ax.legend()

    # Adding the number above each bar with the additional text
    def add_value_labels(bars):
        for i, bar in enumerate(bars):
            yval = bar.get_height()
            yval_int = int(yval)  # Convert to int before numerizing
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                yval + 0.1,
                f'{numerize(yval_int)}',  # Numerize the integer value
                ha='center',
                va='bottom',
                fontsize=10,
                color='black'
            )

    # Remove top and right spines (borders)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Apply the function to all bars
    add_value_labels(bars_all)

    # Display the chart in Streamlit

    st.write("N° Individuals Pledged to RtR Campaign Over the Years (2022 to 2024)")
    st.pyplot(fig)
# individuals_pledge_2022_2024(n_individuals_pledge_in_2022, n_individuals_pledge_in_2023, n_individuals_pledge_in_2024)

## METRICAS INDIVIDUALS ONLY PLAN
def individuals_plan_chart_historical_2022_2024(n_individuals_plan_consolidated_in_2022, n_individuals_plan_consolidated_in_2023, n_individuals_plan_consolidated):

    ## Individuals PLAN Historical
    years = ['2022', '2023', '2024']
    n_individuals_plan_tochart_list = [n_individuals_plan_consolidated_in_2022, n_individuals_plan_consolidated_in_2023, n_individuals_plan_consolidated, ]

    colors = sns.color_palette("RdPu", n_colors=4)

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 2))
    bar_width = 0.6
    index = range(len(years))

    # Plotting the bars
    bars_all = ax.bar(index, n_individuals_plan_tochart_list, width=bar_width, label='N° Individuals ', color=colors)

    # Adding labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('N° Individuals')
    ax.set_title("N° Individuals In Plans to RtR Campaign Over the Years (2022 to 2024)", pad=20)

    # Adjust the tick positions to center the labels
    ax.set_xticks([i for i in index])
    ax.set_xticklabels(years)
    # ax.legend()

    # Adding the number above each bar with the additional text
    def add_value_labels(bars):
        for i, bar in enumerate(bars):
            yval = bar.get_height()
            yval_int = int(yval)  # Convert to int before numerizing
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                yval + 0.1,
                f'{numerize(yval_int)}',  # Numerize the integer value
                ha='center',
                va='bottom',
                fontsize=10,
                color='black'
            )

    # Remove top and right spines (borders)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Apply the function to all bars
    add_value_labels(bars_all)

    # Display the chart in Streamlit
    st.write('Individuals Plan over the years')
    st.pyplot(fig)
# individuals_plan_chart_historical_2022_2024(n_individuals_plan_consolidated_in_2022, n_individuals_plan_consolidated_in_2023, n_individuals_plan_consolidated)

## METRICAS INDIVIDUALS BOTH NON STAKED - NON OFFICIAL
def individual_pledge_plan_chart_not_staked_historical_2022_2024(n_individuals_pledge_in_2022, n_individuals_pledge_in_2023, n_individuals_pledge_in_2024,
n_individuals_plan_consolidated_in_2022, n_individuals_plan_consolidated_in_2023, n_individuals_plan_consolidated):

    ## Combined CHART N Individuals Pledge and Plan Historical
    years = ['2022', '2023', '2024']
    n_hectareas_plan_tochart_list = [n_individuals_pledge_in_2022, n_individuals_pledge_in_2023, n_individuals_pledge_in_2024]
    n_individuals_plan_tochart_list = [n_individuals_plan_consolidated_in_2022, n_individuals_plan_consolidated_in_2023, n_individuals_plan_consolidated]

    colors = sns.color_palette("RdPu", n_colors=2)

    # Create a bar chart
    fig, ax = plt.subplots(figsize=(10, 2))
    bar_width = 0.35
    index = range(len(years))

    # Plotting the bars
    bars_pledge = ax.bar([i - bar_width/2 for i in index], n_hectareas_plan_tochart_list, width=bar_width, label='N° Individuals Pledged', color=colors[0])
    bars_plan = ax.bar([i + bar_width/2 for i in index], n_individuals_plan_tochart_list, width=bar_width, label='N° Individuals In Plans', color=colors[1])

    # Adding labels and title
    ax.set_xlabel('Year')
    ax.set_ylabel('Billions of Individuals')
    ax.set_title("N° Individuals Pledged and In Plans to RtR Campaign Over the Years (2022 to 2024)", pad=20)

    # Adjust the tick positions to center the labels
    ax.set_xticks([i for i in index])
    ax.set_xticklabels(years)
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.3), fancybox=True, shadow=False, ncol=3)


    # Adding the number above each bar with the additional text
    def add_value_labels(bars):
        for bar in bars:
            yval = bar.get_height()
            yval_int = int(yval)  # Convert to int before numerizing
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                yval + 0.1,
                f'{numerize(yval_int)}',  # Numerize the integer value
                ha='center',
                va='bottom',
                fontsize=10,
                color='black'
            )

    # Remove top and right spines (borders)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Apply the function to all bars with the corresponding reporting partners values
    add_value_labels(bars_pledge)
    add_value_labels(bars_plan)

    # Display the chart in Streamlit
    st.write("GRAFICO DE NUMERO DE PERSONAS NON STAKED PLEDGE + PLAN. 2022-2024")
    st.pyplot(fig)
# individual_pledge_plan_chart_not_staked_historical_2022_2024(n_individuals_pledge_in_2022, n_individuals_pledge_in_2023, n_individuals_pledge_in_2024,n_individuals_plan_consolidated_in_2022, n_individuals_plan_consolidated_in_2023, n_individuals_plan_consolidated)

def display_general_info_survey():
    st.write("")
    #     n_reporting_partners_2024, n_partner_gi_2024, n_member_gi_2024, n_initiatives_gi_pending_2024, Members_organizations_24, Members_organizations_24_n_partners,
    #     reporting_partners_in_2023, n_partner_gi_in_2023, n_member_gi_in_2023, n_initiatives_gi_pending_2023, Members_organizations_23, Members_organizations_23_n_partners,
    #     reporting_partners_in_2022, n_partner_gi_in_2022, n_member_gi_in_2022, n_initiatives_gi_pending_2022, Members_organizations_22, Members_organizations_22_n_partners
    # ):
    #     """
    #     Displays general information survey data for the years 2022, 2023, and 2024 in columns.

    #     Parameters:
    #     - Data for 2024: n_reporting_partners_2024, n_partner_gi_2024, n_member_gi_2024, n_initiatives_gi_pending_2024, Members_organizations_24, Members_organizations_24_n_partners
    #     - Data for 2023: reporting_partners_in_2023, n_partner_gi_in_2023, n_member_gi_in_2023, n_initiatives_gi_pending_2023, Members_organizations_23, Members_organizations_23_n_partners
    #     - Data for 2022: reporting_partners_in_2022, n_partner_gi_in_2022, n_member_gi_in_2022, n_initiatives_gi_pending_2022, Members_organizations_22, Members_organizations_22_n_partners
    #     """
        
    #     st.write('# APPLY: GENERAL INFORMATION SURVEY')
    #     col1, col2, col3 = st.columns(3)

    #     # 2024 COP29 Data
    #     with col1:
    #         st.write('### 2024 COP29')
    #         # st.write(f'n_reporting_partners_in_2024: {n_reporting_partners_2024}')
    #         st.write(f'n_partner_gi_2024: {n_partner_gi_2024}')
    #         st.write(f'n_member_gi_2024: {n_member_gi_2024}')
    #         st.write(f'n_initiatives_gi_pending_2024: {n_initiatives_gi_pending_2024}')
    #         st.write(f'Members_organizations_24: {Members_organizations_24}')
    #         st.write(f'Members_organizations_24_n_partners: {Members_organizations_24_n_partners}')

    #     # 2023 COP28 Data
    #     with col2:
    #         st.write('### 2023 COP28')
    #         st.write(f'reporting_partners_in_2023: {reporting_partners_in_2023}')
    #         st.write(f'n_partner_gi_in_2023: {n_partner_gi_in_2023}')
    #         st.write(f'n_member_gi_in_2023: {n_member_gi_in_2023}')
    #         st.write(f'n_initiatives_gi_pending_2023: {n_initiatives_gi_pending_2023}')
    #         st.write(f'Members_organizations_23: {Members_organizations_23}')
    #         st.write(f'Members_organizations_23_n_partners: {Members_organizations_23_n_partners}')

    #     # 2022 COP27 Data
    #     with col3:
    #         st.write('### 2022 COP27')
    #         st.write(f'reporting_partners_in_2022: {reporting_partners_in_2022}')
    #         st.write(f'n_partner_gi_in_2022: {n_partner_gi_in_2022}')
    #         st.write(f'n_member_gi_in_2022: {n_member_gi_in_2022}')
    #         st.write(f'n_initiatives_gi_pending_2022: {n_initiatives_gi_pending_2022}')
    #         st.write(f'Members_organizations_22: {Members_organizations_22}')
    #         st.write(f'Members_organizations_22_n_partners: {Members_organizations_22_n_partners}')

    # display_general_info_survey(
    #     n_reporting_partners_2024, n_partner_gi_2024, n_member_gi_2024, n_initiatives_gi_pending_2024, Members_organizations_24, Members_organizations_24_n_partners,
    #     reporting_partners_in_2023, n_partner_gi_in_2023, n_member_gi_in_2023, n_initiatives_gi_pending_2023, Members_organizations_23, Members_organizations_23_n_partners,
    #     reporting_partners_in_2022, n_partner_gi_in_2022, n_member_gi_in_2022, n_initiatives_gi_pending_2022, Members_organizations_22, Members_organizations_22_n_partners
    # )




    # n_reporting_partners_in_2024,
    # n_partner_pledge,
    # n_member_pledge,
    # n_initiatives_pledge_pending,
    # n_individuals_pledge_in_2024
    # n_individuals_pledge_in_2024_n_partners,
    # reporting_partners_in_2023_cop28,
    # n_partner_pledge_in_2023,
    # n_member_pledge_in_2023,
    # n_initiatives_pledge_pending_in_2023,
    # n_individuals_pledge_in_2023,
    # n_individuals_pledge_in_2023_n_partners,,
    # reporting_partners_in_2022_cop27,
    # n_partner_pledge_in_2022,
    # n_member_pledge_in_2022,
    # n_initiatives_pledge_pending_in_2022,
    # n_individuals_pledge_in_2022,
    # n_individuals_pledge_in_2022_n_partners,
    # n_hectares_pledge_in_2022,
    # n_hectares_pledge_in_2022_n_partners,


    # st.write('# PLEDGE: PLEDGE STATEMENT')
    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     st.write('### 2024 COP29')
    #     st.write('n_reporting_partners_in_2024')
    #     n_reporting_partners
    #     st.write('n_partner_pledge')
    #     n_partner_pledge
    #     st.write('n_member_pledge')
    #     n_member_pledge
    #     st.write('n_initiatives_pledge_pending')
    #     n_initiatives_pledge_pending
    #     st.write('n_individuals_pledge_in_2024')
    #     n_individuals_pledge_in_2024
    #     st.write('n_individuals_pledge_in_2024_n_partners')
    #     

    # with col2:
    #     st.write('### 2023 COP28')
    #     st.write('reporting_partners_in_2023_cop28')
    #     reporting_partners_in_2023_cop28
    #     st.write('n_partner_pledge_in_2023')
    #     n_partner_pledge_in_2023
    #     st.write('n_member_pledge_in_2023')
    #     n_member_pledge_in_2023
    #     st.write('n_initiatives_pledge_pending_in_2023')
    #     n_initiatives_pledge_pending_in_2023
    #     st.write('n_individuals_pledge_in_2023')
    #     n_individuals_pledge_in_2023
    #     st.write('n_individuals_pledge_in_2023_n_partners')
    #     n_individuals_pledge_in_2023_n_partners

    # with col3:
    #     st.write('### 2022 COP27')
    #     st.write('reporting_partners_in_2022_cop27')
    #     reporting_partners_in_2022_cop27
    #     st.write('n_partner_pledge_in_2022')
    #     n_partner_pledge_in_2022
    #     st.write('n_member_pledge_in_2022')
    #     n_member_pledge_in_2022
    #     st.write('n_initiatives_pledge_pending_in_2022')
    #     n_initiatives_pledge_pending_in_2022
    #     st.write('n_individuals_pledge_in_2022')
    #     n_individuals_pledge_in_2022
    #     st.write('n_individuals_pledge_in_2022_n_partners')
    #     n_individuals_pledge_in_2022_n_partners
    #     st.write('n_hectares_pledge_in_2022')
    #     n_hectares_pledge_in_2022 
    #     st.write('n_hectares_pledge_in_2022_n_partners')
    #     n_hectares_pledge_in_2022_n_partners




    # # # # ## WORKING FINE. DATOS DESCRIPTIVOS PLAN
    # ## Confirmation
    # st.write('# PLAN SUBMISSION: RESILIENCE BUILDING PLANS')
    # col1, col2, col3 = st.columns(3)

    # with col1:
    #     st.write('### 2024 COP29')
    #     st.write('n_reporting_partners_in_2024')
    #     n_reporting_partners
    #     st.write('n_partners_plan')
    #     n_partners_plan
    #     st.write('n_members_plan')
    #     n_members_plan
    #     st.write('n_total_plans_consolidated')
    #     n_total_plans_consolidated
        
    #     st.write('Total de Individuos Plan')
    #     n_individuals_plan_consolidated
    #     st.write('N de planes que repornta indiv')
    #     n_individuals_all_plans_n_plans
    #     st.write('N Partners que reportan individuos en Plan')
    #     n_individuals_all_plans_n_partners
        
        
    #     st.write('dollars_movilized_all_plans')
    #     dollars_movilized_all_plans
    #     st.write('dollars_mobilized_all_plans_n_plans')
    #     dollars_mobilized_all_plans_n_plans
    #     st.write('dollars_mobilized_all_plans_n_partners')
    #     dollars_mobilized_all_plans_n_partners
        
    
    # with col2:
    #     st.write('### 2023 COP28')
    #     st.write('reporting_partners_in_2023_cop28')
    #     reporting_partners_in_2023_cop28
    #     st.write('n_partners_plan_in_2023')
    #     n_partners_plan_in_2023
    #     st.write('n_members_plan_in_2023')
    #     n_members_plan_in_2023
    #     st.write('n_total_plans_consolidated_in_2023')
    #     n_total_plans_consolidated_in_2023 
        
        
    #     st.write('dollars_movilized_all_plans_in_2023')    
    #     dollars_movilized_all_plans_in_2023
    #     st.write('dollars_mobilized_all_plans_n_plans_in_2023')    
    #     dollars_mobilized_all_plans_n_plans_in_2023
    #     st.write('dollars_mobilized_all_plans_n_partners_in_2023')    
    #     dollars_mobilized_all_plans_n_partners_in_2023


    # with col3:
    #     st.write('### 2022 COP27')
    #     st.write('reporting_partners_in_2022_cop27')
    #     reporting_partners_in_2022_cop27
    #     st.write('n_partners_plan_in_2022')
    #     n_partners_plan_in_2022
    #     st.write('n_members_plan_in_2022')
    #     n_members_plan_in_2022
    #     st.write('n_total_plans_consolidated_in_2022')
    #     n_total_plans_consolidated_in_2022
        
        
    #     st.write('n_individuals_plan_consolidated_in_2022')
    #     n_individuals_plan_consolidated_in_2022
    #     st.write('n_individuals_plan_consolidated_in_2023_n_partners')
    #     n_individuals_plan_consolidated_in_2023_n_partners
        
        
    #     st.write('dollars_movilized_all_plans_in_2022')
    #     dollars_movilized_all_plans_in_2022
    #     st.write('dollars_mobilized_all_plans_n_plans_in_2022')
    #     dollars_mobilized_all_plans_n_plans_in_2022
    #     st.write('dollars_mobilized_all_plans_n_partners_in_2022')
    #     dollars_mobilized_all_plans_n_partners_in_2022


# from campaign_overview_general_metrics import campaign_overview_general_metrics
# from progress_metrics_update import progress_metrics_updated
# # from global_reach_campaign_overview import global_outreach_campaign_overview
# from reporting_progress_section import reporting_progress_section
# from Introduction_to_dataexplorer import intro_summary
# from self_description_campaign_overview import selfdescription_partner

from headquarters_rtr import headquarters
from target_beneficiaries_campaign_overview import priority_groups_campaign_overview_bar_chart
from hazards_campaign_overview import hazards_campaign_overview
from actiontypes_partners_plan_overview import action_types_consolidated
from ra_campaign_overview import ra_campaign
from saa_campaign_overview import saa_campiagn_overview



## MULTISELECTOR


selected_section = st.sidebar.radio(
    'Select a Section to Display',['Campaign Overview','SAA Priority Systems','Climate Hazards','Target Beneficiaries','Resilience Attributes','Resilience Actions',"Partners' Headquarters",'Transparency and Reporting',]
)


if 'Campaign Overview' in selected_section:
    render_main_page()
    campaign_overview_cop29()
    # current_partners()
    # selfdescription_partner(df_gi)
    global_outreach()
    st.write("___")
    st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

if 'SAA Priority Systems' in selected_section:
    saa_campiagn_overview(df_gi,n_reporting_partners)
    st.write("___")
    st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

if 'Climate Hazards' in selected_section:
    hazards_campaign_overview(df_hazards_pledge_plan_vertical,n_reporting_partners)
    st.write("___")
    st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")
    
if 'Target Beneficiaries' in selected_section:
    priority_groups_campaign_overview_bar_chart(df_gi, n_reporting_partners)
    
    st.write("___")
    st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

if 'Resilience Attributes' in selected_section:
    ra_campaign(df_2023_plan)
    st.write("___")
    st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")


if 'Resilience Actions' in selected_section:
    action_types_consolidated(df_2023_plan, n_total_plans_consolidated, n_partners_plan,df_2023_plan_summary)
    st.write("___")
    st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")

if 'Transparency and Reporting' in selected_section:
    transparency_reporting(df_partner_campaign_tracker,df_pledge,df_2023_plan,reporting_partners_in_2022_cop27, reporting_partners_in_2023_cop28, n_reporting_partners,
                                n_partner_gi_in_2022, n_partner_gi_in_2023, n_partner_gi,
                                n_initiatives_gi_pending_2022, n_initiatives_gi_pending_2023, n_initiatives_gi_pending)
    st.write("___")
    st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")


if "Partners' Headquarters" in selected_section:
    headquarters(df_gi,df_country,political_countries_url)
    st.write("___")
    st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")



















# if 'Progress Metrics Update' in selected_section:
#     progress_metrics_updated(rtr_goal_individuals,n_individuals_pledge_in_2023,n_individuals_plan_consolidated,
#                              n_hectareas_pledge_adj,n_hectareas_plan_consolidated,n_individuals_pledge_in_2022,
#                              n_parters_reporting_metrics_pledge,n_partners_reporting_countries_plan,NatSysHectaTotal2022_pledge_adj,
#                              n_total_plans_consolidated,n_partners_reportingnumberofnaturalsyst2022_pledge,
#                              n_hectareas_pledge_n_partners,n_partners_reporting_n_hectareas_plan_consolidated,
#                              dollars_movilized_all_plans,dollars_mobilized_all_plans_n_plans,dollars_mobilized_all_plans_n_partners,
#                              percentage_increase_resilience_individuals_pledge,percentaje_individuals_pledge_vs_plan, percentaje_hectareas_nat_syst_pledge_vs_plan)
#     st.write("___")
#     st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")








# if 'Transparency and Reporting' in selected_section:
#     reporting_progress_section(n_partner_gi,n_reporting_partners,n_partner_pledge,n_partners_plan,
#                                percentaje_partner_reporting_adaptation_finance_consolidated,dollars_mobilized_all_plans_n_partners,
#                                df_gi_summary,df_pledge_summary,partners_report_pledge_d_individuals, partners_repor_pledge_companies, partners_repor_pledge_regions, partners_repor_pledge_cities, partners_repor_pledge_nat_syst,n_partners_reportingnumberof_direct_individuals_pledge, n_partners_reportingnumberofcompanies2023_pledge, n_partners_reportingnumberofregions2023_pledge, n_partners_reportingnumberofcities2023_pledge, n_hectareas_pledge_n_partners,
#                                n_partners_reportingnumberofindiv_companies_pledge, n_partners_reportingnumberofindiv_regions_pledge, n_partners_reportingnumberofindiv_cities_pledge, n_partners_reportingnumberofindiv_natsyst2023,
#                                df_2023_plan,plan_n_individuals_direct, plan_n_companies, plan_n_regions, plan_n_cities, plan_h_natsyst,df_2023_plan_summary,
#                                n_partner_plan_only2023,percentaje_reporting_partner_pledge,percentaje_reporting_partner_plan_consolidated)
#     st.write("___")
#     st.markdown("👈 Explore More: Navigate through different sections using the sidebar to discover in-depth insights and information.")












# st.write("____")
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
        <li>To search for partners solution stories, <a href="/SOLUTION_STORIES" target="_self"><strong>click here</strong></a></li>
        <li>To search for the contribution of specific partners, <a href="/PARTNER_FINDER" target="_self"><strong>click here</strong></a></li>
        <li>To explore our Metrics Framework, <a href="/METRICS_FRAMEWORK" target="_self"><strong>click here</strong></a></li>
        <li>To get more information on this data explorer, <a href="/ABOUT_THE_DATA_EXPLORER" target="_self"><strong>click here</strong></a></li>
    </ul>
</div>
""", unsafe_allow_html=True)


