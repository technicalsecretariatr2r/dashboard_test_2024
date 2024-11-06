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

def progress_metrics_updated(rtr_goal_individuals,total_numbers_individuals_pledge_oficial_IR,n_individuals_plan_consolidated,
                             NumHectNatSys2023_pledge_adj,n_hectareas_plan_consolidated,n_direct_individuals2022,
                             n_parters_reporting_metrics_pledge,n_partners_reporting_countries_plan,NatSysHectaTotal2022_pledge_adj,
                             n_total_plans_consolidated,n_partners_reportingnumberofnaturalsyst2022_pledge,
                             n_partners_reportingnumberofnaturalsyst2023_pledge,n_partners_reporting_n_hectareas_plan_consolidated,
                             dollars_movilized_all_plans,dollars_mobilized_all_plans_n_plans,dollars_mobilized_all_plans_n_partners,
                             percentage_increase_resilience_individuals_pledge,percentaje_individuals_pledge_vs_plan, percentaje_hectareas_nat_syst_pledge_vs_plan):
##__________________________________________________________________________________________________________________________________________________________________
## SET 2 - PROGRESS METRICS UPDATE
##__________________________________________________________________________________________________________________________________________________________________
    # st.markdown("""---""")
    # st.markdown("## MAGNITUDE OF RESILIENCE")
    # st.markdown("Magnitude of Resilience metrics assess the 'size' of the impact, computed in terms of the number of beneficiaries reached by the initiatives.")

    ## SET 2 - IMPACT
    st.markdown("### PROGRESS METRICS UPDATE")
    st.markdown("Visualizations of the campaign's progress, focusing on the magnitude of partners' pledges and plans. This includes data on the number of individuals and hectares of natural systems becoming more resilient, as well as the amount of financial resources planned to be mobilized to accelerate implementation.")
    #CHART LEVEL ADVANCE CAMPAIGN
    # st.markdown("### INDIVIDUALS")
    # INDIVIDUALS
    # rtr_goal_individuals_numerized = str(numerize(rtr_goal_individuals)) #Original
    rtr_goal_individuals_numerized = str(numerize(rtr_goal_individuals))[:-1]  # Removes the last charcter
    total_numbers_individuals_pledge_oficial_IR_numerized = str(numerize(total_numbers_individuals_pledge_oficial_IR))[:-1]
    n_individuals_plan_consolidated_numerized = str(numerize(n_individuals_plan_consolidated))[:-1]

    # Calculate the percentages relative to the campaign goal
    percent_goal = (rtr_goal_individuals / rtr_goal_individuals) * 100
    percent_pledged = (total_numbers_individuals_pledge_oficial_IR / rtr_goal_individuals) * 100
    percent_planned = (n_individuals_plan_consolidated / rtr_goal_individuals) * 100

    # Set colors from the RdPu palette
    colors = sns.color_palette("RdPu", n_colors=3)

    # Set the size of the figure
    fig_width = 6  # 
    fig_height = 1.5  # 

    # Create the figure and bar chart
    fig_advances_campaign_individuals, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Plotting the bars
    bars = ax.bar(['Goal','Pledge', 'Plan'],
                [rtr_goal_individuals,total_numbers_individuals_pledge_oficial_IR, n_individuals_plan_consolidated],
                color=colors[:3])

    # Adding values to the columns  (absolute numbers)
    for bar, numerized in zip(bars,
                                    [rtr_goal_individuals_numerized, total_numbers_individuals_pledge_oficial_IR_numerized, n_individuals_plan_consolidated_numerized,]):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,  # Slightly above the bar
                f'{numerized}', ha='center', va='bottom')

    # Set labels and title
    ax.set_ylabel('Billions of Individuals')
    ax.set_xlabel('RtR Campaign')
    ax.set_title('Progress Metrics Update', fontsize=11, y=1.3)

    def billions_formatter(x, pos):
        return f'{int(x / 1e9)}'

    # Apply the formatter
    ax.yaxis.set_major_formatter(FuncFormatter(billions_formatter))

    # Adjust the layout to make room for the x-axis label
    plt.subplots_adjust(bottom=0.25)

    # Remove top and right spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # st.pyplot(fig_advances_campaign_individuals)





    # st.markdown("### HECTARES OF NATURAL SYSTEMS")
    ##HECTARES
    
    
    hectares_pledge_numerize =  str(numerize(NumHectNatSys2023_pledge_adj))
    hectares_plan_numerize =  str(numerize(n_hectareas_plan_consolidated))

    # Calculate the percentages relative to the campaign goal
    percent_pledged = (NumHectNatSys2023_pledge_adj / NumHectNatSys2023_pledge_adj) * 100
    percent_planned = (n_hectareas_plan_consolidated / NumHectNatSys2023_pledge_adj) * 100

    # Set colors from the RdPu palette
    colors = sns.color_palette("RdPu", n_colors=2)

    # Set the size of the figure
    fig_width = 6  # 
    fig_height = 1.5  # 

    # Create the figure and bar chart
    fig_advances_campaign_hectares, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Plotting the bars
    bars = ax.bar(['Pledge', 'Plan'],
                [NumHectNatSys2023_pledge_adj, n_hectareas_plan_consolidated],
                color=colors[:2])

    # Adding values to the columns, combining percentages and absolute numbers
    for bar, percent, numerized in zip(bars,
                                    [percent_pledged, percent_planned], 
                                    [hectares_pledge_numerize, hectares_plan_numerize]):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1,  # Slightly above the bar
                f'{numerized}', ha='center', va='bottom')

    # Set labels and title
    ax.set_ylabel('Million of Hectares')
    ax.set_xlabel('RtR Campaign')
    ax.set_title('Million of Hectares of Natural Systems', fontsize=11, y=1.3)
    
    def million_formatter(x, pos):
        return f'{int(x / 1e7)}'

    # Apply the formatter
    ax.yaxis.set_major_formatter(FuncFormatter(million_formatter))

    # Adjust the layout to make room for the x-axis label
    plt.subplots_adjust(bottom=0.25)

    # Remove top and right spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Show the figure in the Streamlit app
    # st.pyplot(fig_advances_campaign_hectares)


    st.markdown("#### RESILIENCE GOALS: PARTNERS' PLEDGES AND PLANS IN NUMBERS")
    # col1, col2, col3 = st.columns([0.25,1.5,0.25])
    # col2.pyplot(fig_advances_campaign_individuals)
    # col2.pyplot(fig_advances_campaign_hectares)

    # long_description = f"""
    # Since its launch in 2021, the campaign has grown and counts now with a total of {n_all_rtrpartners_2023} partner initiatives, an increase of {numerize(percentage_increase_number_partnes_all_campaign)}% in relation to 2022, and with a total of {n_members2023} collaborating members. Furthermore, new subnational governments have joined the Race through their Flagship Initiatives: with a cumulated {n_cities_citiesrtr} cities from Cities Race to Resilience and a cumulated {n_regions_regions4} regions from RegionsAdapt.
    # """
    # st.markdown(long_description)

    st.markdown("##### INDIVIDUALS")
    col1, col2, col3 = st.columns(3)
    col1.metric("N° Individuals Pledged 2022*",numerize(n_direct_individuals2022),"Out of 17 partners")
    col2.metric("N° Individuals Pledged 2023",numerize(total_numbers_individuals_pledge_oficial_IR),"Out of "+str(n_parters_reporting_metrics_pledge)+" partners")
    col3.metric("N° Individuals Plan 2022-2023",numerize(n_individuals_plan_consolidated),"Out of "+str(n_partners_reporting_countries_plan)+" Partners ("+str(n_total_plans_consolidated)+" Plans)")
    col1, col2, col3 = st.columns([0.25,1.5,0.25])
    col2.pyplot(fig_advances_campaign_individuals)


    st.markdown("##### HECTARES OF NATURAL SYSTEMS")
    
    
    st.write("n_hectareas_plan_consolidated_asdasda",n_hectareas_plan_consolidated,n_partners_reporting_n_hectareas_plan_consolidated)
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Hectares Pledged 2022*",numerize(NatSysHectaTotal2022_pledge_adj),"Out of "+str(n_partners_reportingnumberofnaturalsyst2022_pledge)+" partners")
    col2.metric("Hectares Pledged 2023**",numerize(NumHectNatSys2023_pledge_adj),"Out of "+str(n_partners_reportingnumberofnaturalsyst2023_pledge)+" partners")
    col3.metric("Hectares Plan 2022-2023**",numerize(n_hectareas_plan_consolidated),"Out of "+str(n_partners_reporting_n_hectareas_plan_consolidated)+" partners")
    st.caption("*Metric presented in the RtR Data Explorer for COP27.")
    st.caption("**Metrics have been adjusted for double counting based on 2022 criteria.")
    col1, col2, col3 = st.columns([0.25,1.5,0.25])
    col2.pyplot(fig_advances_campaign_hectares)

    st.markdown("##### ADAPTATION FINANCE MOVILIZED")
    col1, col2, col3 = st.columns(3)
    col1.metric("USD Planned to Movilize by Partners",numerize(dollars_movilized_all_plans),"(out of "+str(dollars_mobilized_all_plans_n_plans)+" plans from "+str(dollars_mobilized_all_plans_n_partners)+" Partners)")

    long_description = f"""
    To date, considering only reporting partners from the 2023 process, the RtR Campaign Partners have pledged actions that are expected to enhance the resilience  of {str(numerize(total_numbers_individuals_pledge_oficial_IR))[:-1]} billion people by 2030, marking a {numerize(percentage_increase_resilience_individuals_pledge)}% increase from 2022 ambitions. This commitment is underscored by combined pledges to protect, restore, or manage {str(numerize(NumHectNatSys2023_pledge_adj))[:-1]} million hectares of natural systems by 2030, delivering substantial benefits for both people and the planet. 


    For the first time, the Campaign is proudly demonstrating the conversion of pledges into tangible actions. Current efforts are set to boost the resilience of {str(numerize(n_individuals_plan_consolidated))[:-1]} billion people. And of the {str(numerize(n_hectareas_plan_consolidated))[:-1]} million hectares pledged for protection, restoration and management, actions have already been initiated on {str(numerize(n_hectareas_plan_consolidated))[:-1]} million hectares. 

    To support these ambitious goals, a remarkable mobilization by Partners of US${str(numerize(dollars_movilized_all_plans))[:-1]} billion is underway. This progress not only showcases the gap between pledges and plans but also highlights the extensive effort required to fulfill these commitments. 
    """
    st.markdown("#### EXECUTIVE SUMMARY")
    st.markdown(long_description)


    ##___________________________________________
    ##___________________________________________
    ##___________________________________________
    ## END CHARTS COMPARATION GOAL - PLEDGE - PLAN
    ##___________________________________________
    ##___________________________________________
    ##___________________________________________






