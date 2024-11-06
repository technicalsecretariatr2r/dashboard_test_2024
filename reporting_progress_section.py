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



def reporting_progress_section(n_partner_gi,n_reporting_partners,n_partner_pledge_2023,n_partner2022_2023_plan,
                               percentaje_partner_reporting_adaptation_finance_consolidated,dollars_mobilized_all_plans_n_partners,
                               df_gi_summary,df_pledge_summary,partners_report_pledge_d_individuals2023, partners_repor_pledge_companies2023, partners_repor_pledge_regions2023, partners_repor_pledge_cities2023, partners_repor_pledge_nat_syst2023,n_partners_reportingnumberof_direct_individuals2023, n_partners_reportingnumberofcompanies2023_pledge, n_partners_reportingnumberofregions2023_pledge, n_partners_reportingnumberofcities2023_pledge, n_partners_reportingnumberofnaturalsyst2023_pledge,
                               n_partners_reportingnumberofindiv_companies2023, n_partners_reportingnumberofindiv_regions2023, n_partners_reportingnumberofindiv_cities2023, n_partners_reportingnumberofindiv_natsyst2023,
                               df_2023_plan_summary,n_2022_2023_plans_individuals, n_2022_2023_plans_companies, n_2022_2023_plans_regions, n_2022_2023_plans_cities, n_2022_2023_plans_natsyst,df_2023_plan,
                               n_partner_plan_only2023,percentaje_reporting_partner_pledge_2023,percentaje_reporting_partner_plan_consolidated):



      ## SET 5 - REPORTING PROCESS
    
    # list_to_plan_chart_all_index = ['plan_short_name',
    #                                 'plan_identif_subidx',
    #                                 'description_plan_subidx',
    #                                 'saa_plan_subidx',
    #                                 'ra_plan_subidx',
    #                                 'pri_benef_magnitud_plan_subidx',
    #                                 'governance_plan_subidx', # REVISAR PORQUË NO LO LEE
    #                                 'barriers_plan_subidx',
    #                                 'finance_plan_subidx',
    #                                 'monitoring_data_collect_plan_subidx'
    #                                 ]

    
    # st.write("PLAN",df_2023_plan.columns )
      
    st.markdown("### TRANSPARENCY AND REPORTING")
    st.caption("A dedicated space for reporting the statuses of partners, including the latest tools and reports for 2023.")

    # Calculate the percentages
    percent_partner_gi = round((n_partner_gi / n_reporting_partners) * 100)
    percent_partner_pledge_2023 = (n_partner_pledge_2023 / n_reporting_partners) * 100
    percent_partner2022_2023_plan = (n_partner2022_2023_plan / n_reporting_partners) * 100
    # dollars_mobilized_all_plans_n_partners
    # percentaje_partner_reporting_adaptation_finance_consolidated


    long_description = f"""
    Transparent reporting is crucial for demonstrating climate adaptation progress - to build trust, strengthen accountability, and inform evidence-based policies. While speed of progress varies based on each partner's capacity and the year in which they joined, to date {numerize(percent_partner_gi)}% of reporting partners have responded General Information Tool, {numerize(percentaje_reporting_partner_pledge_2023)}% have submitted a pledge, {numerize(percentaje_reporting_partner_plan_consolidated)}% of partners submitted an action plan and almost {numerize(percentaje_partner_reporting_adaptation_finance_consolidated)}% of partners reported the adaptation finance mobilised.
    """
    st.markdown(long_description)

    tab1, tab2, tab3, tab4 = st.tabs(["All Stages", "General Information", "Pledge Statements","Plans"])

    # LEVEL 1
    
   
    n_gi_2022 = 26  #Source Data Explorer 2023
    n_pledge_2022 = 23 #Source Data Explorer 2023
    n_plans_2022 = 0 #Source Data Explorer 2023
    n_finance_plans_2022 = 0 #Source Data Explorer 2023
    
    n_gi_2023 = 28
    n_pledge_2023 = 25
    n_plans_2023 = 21
    n_finance_plans_2023= 15
 
    n_gi_2024 = n_partner_gi  #Need to update names
    n_pledge_2024 = n_partner_pledge_2023 #Need to update names
    n_plans_2024 = n_partner2022_2023_plan #Need to update names
    n_finance_plans_2024= dollars_mobilized_all_plans_n_partners #Need to update names

    Total = n_reporting_partners 
    

    # Normalize data for percentages
    
    percent_gi_2022 = round((n_gi_2022 / Total) * 100, 0)
    percent_pledge_2022 = round((n_pledge_2022 / Total) * 100, 0)
    percent_plans_2022 = round((n_plans_2022 / Total) * 100, 1)
    percent_finance_plans_2022 = round((n_finance_plans_2022 / Total) * 100, 0)

    percent_gi_2023 = round((n_gi_2023 / Total) * 100, 0)
    percent_pledge_2023 = round((n_pledge_2023 / Total) * 100, 0)
    percent_plans_2023 = round((n_plans_2023 / Total) * 100, 0)
    percent_finance_plans_2023 = round((n_finance_plans_2023 / Total) * 100, 0)

    percent_gi_2024 = round((n_gi_2024 / Total) * 100, 0)
    percent_pledge_2024 = round((n_pledge_2024 / Total) * 100, 0)
    percent_plans_2024 = round((n_plans_2024 / Total) * 100, 0)
    percent_finance_plans_2024 = round((n_finance_plans_2024 / Total) * 100, 0)

    # Data for the plot
    categories = ['Adaptation Finance Mobilization (Planned)', 'Resilience-Building Plan','Pledge Statement','General Information', ]
    percent_2022 = [percent_finance_plans_2022, percent_plans_2022,percent_pledge_2022, percent_gi_2022]
    percent_2023 = [percent_finance_plans_2023, percent_plans_2023,percent_pledge_2023, percent_gi_2023]
    percent_2024 = [percent_finance_plans_2024, percent_plans_2024,percent_pledge_2024, percent_gi_2024]

    # Set the Seaborn palette
    sns.set_palette("RdPu")

    # Create the figure and axis for plotting
    fig, ax = plt.subplots(figsize=(10, 4))

    # Define the position of the bars
    bar_width = 0.3
    index = np.arange(len(categories))

    # Set the x-axis limits from 0 to 100%
    ax.set_xlim(0, 100)

    # Set the x-axis ticks at intervals of 10 points
    ax.set_xticks(np.arange(0, 101, 10))

    # Plot 2022, 2023, and 2024 bars side by side with the normalized values
    bars_2022 = ax.barh(index - bar_width, percent_2022, bar_width, label='2022')
    bars_2023 = ax.barh(index, percent_2023, bar_width, label='2023')
    bars_2024 = ax.barh(index + bar_width, percent_2024, bar_width, label='2024')

    # # Add percentage labels at the end of 2024 bars with 1 decimal point
    # for idx, bar in enumerate(bars_2024):
    #     ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2, f"{percent_2024[idx]:.0f}%", va='center')

    # Set x-axis and y-axis labels for better clarity
    ax.set_xlabel('Percentage of Partners')
    ax.set_ylabel('Reporting Categories')

    # Set the y-ticks and labels for the categories
    ax.set_yticks(index)
    ax.set_yticklabels(categories)

    # Move the legend to the outside
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

    # Hide the right and top spines for cleaner look
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Set a title for the chart
    ax.set_title('Partner Reporting Status (2022 to 2024)', fontsize=10)
    
     # Add a text box below the chart
    plt.figtext(0.99, 0.01, f'N = {n_reporting_partners}',
                horizontalalignment='right', fontsize=10, weight='normal')

    # Show the plot in Streamlit
    st.pyplot(fig)



    # # Set darker colors from the RdPu palette
    # colors = sns.color_palette("RdPu", n_colors=4)

    # # Set the size of the figure
    # fig_width = 8  # 
    # fig_height = 2  # 

    # # Create the figure and bar chart
    # fig_partners_reporting_tools, ax = plt.subplots(figsize=(fig_width, fig_height))

    # # Plotting the bars
    # bars = ax.bar(['General\nInformation', 'Pledge\nStatement', 'Resilience-Building\nPlan','Adaptation Finance\n Mobilization (Planned)'],
    #             [percent_partner_gi, percent_partner_pledge_2023, percent_partner2022_2023_plan,percentaje_partner_reporting_adaptation_finance_consolidated],
    #             color=colors)

    # # Adding percentage and absolute number labels on top of each bar
    # for bar, absolute in zip(bars, [n_partner_gi, n_partner_pledge_2023, n_partner2022_2023_plan, dollars_mobilized_all_plans_n_partners]):
    #     yval = bar.get_height()
    #     plt.text(bar.get_x() + bar.get_width()/2, yval + 1, f'{yval:.1f}% ({absolute})', ha='center', va='bottom')

    # # Set labels and title
    # ax.set_ylabel('Percentage (%) Partners')
    # ax.set_xlabel('RtR Reporting Tools', labelpad=15)

    # # Remove top and right spines
    # ax.spines['right'].set_visible(False)
    # ax.spines['top'].set_visible(False)
    # # st.pyplot(fig_partners_reporting_tools)
    
    
    
    

    with tab1:
        st.markdown("Number of Partners responding each of the RtR Reporting Tool")
        st.pyplot(fig_partners_reporting_tools)
        st.markdown("Partners are required to submit a pledge statement after providing their general information and member details. Following the submission of a pledge statement, partners are then asked to submit a plan. Future steps in the campaign will involve highlighting the progress of these plans (proceed) and ultimately publishing their impacts. These last two stages of the Race will commence in 2024.")

    # LEVEL 2: GENERAL INFORMATION
    # LEVEL 2: GENERAL INFORMATION
    # LEVEL 2: GENERAL INFORMATION
    # LEVEL 2: GENERAL INFORMATION
    # LEVEL 2: GENERAL INFORMATION
    
    # #RANKING CHART #1 GENERAL INFORMATION
    def create_fig1_gi():
        data = df_gi_summary
        data = data.sort_values(by='gi_completeness_idx', ascending=True)

        # Set a base figure height and an increment per partner
        base_height = 2
        height_per_partner = 0.1
        fig_height = base_height + height_per_partner * len(data['InitName'])

        fig1_gi, ax = plt.subplots(figsize=(10, fig_height))
        left = np.zeros(len(data['InitName']))

        # Use colormap
        cmap = cm.get_cmap('RdPu')  # Use RdPu colormap
        colors = cmap(data['gi_completeness_idx'].values / data['gi_completeness_idx'].values.max())

        # Adjust the bar height here
        bars = ax.barh(data['InitName'], data['gi_completeness_idx'], color=colors, height=0.5)  
        # ax.set_xlabel('2023 GIS Completeness Index (%)')  # Indicate percentage in the label
        # ax.set_ylabel('Partner Names')
        ax.set_title('GI Completeness Index (%) per Partner')
        ax.tick_params(axis='y', labelsize=8)  # Adjust the size of the y-axis labels (partner names)
            
        # Formatting x-tick labels to display as percentages
        vals = ax.get_xticks()
        ax.set_xticklabels(['{:.0f}%'.format(x) for x in vals])

        # Loop over the bars and add the value as text
        for bar in bars:
            width = bar.get_width()
            ax.text(width,  # Set the x position of the text
                    bar.get_y() + bar.get_height() / 2,  # Set the y position of the text
                    f'{width:.1f}%',  # Set the text to be displayed
                    ha='left',  # horizontal alignment
                    va='center',
                    fontsize=8)  # vertical alignment

        # Remove top and right spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Set y-limits to remove excess blank space
        ax.set_ylim(-0.5, len(data['InitName']) - 0.5)
        ax.set_xlim(0, 100)
        ax.set_xticklabels([])
        ax.tick_params(axis='x', length=0)
            
        # Use tight_layout to fit all elements nicely
        plt.tight_layout()
        
        return fig1_gi
    fig1_gi = create_fig1_gi()


    #Chart2
    #Horizontal Chart 2_Multi Index_General Information
    general_survey_index_chart_list = ['InitName','partner_info_gi_subidx',
                                    'members_info_gi_subidx','metrics_gi_subidx',
                                    'saa_gi_subidx','action_clusterss_gi_subidx',
                                    'type_impact_gi_subidx',]

    # Define your data
    data = df_gi_summary.sort_values(by='gi_completeness_idx', ascending=True)
    data = data[general_survey_index_chart_list]

    # Make colormap
    cmap = plt.get_cmap('RdPu', len(general_survey_index_chart_list)-1)  # minus 1 because 'q9' is not an index

    # Set the figure size
    fig2_gi, ax = plt.subplots(figsize=(10, len(data['InitName'])/2))  # Adjust the vertical size according to number of partners

    # Initial left position is zero
    left = np.zeros(len(data['InitName']))

    # Loop over all columns except for 'q9' and create a bar for each
    for i, column in enumerate(general_survey_index_chart_list[1:]):
            bars = ax.barh(data['InitName'], data[column], left=left, color=cmap(i), label=column)
            left += data[column]

    # Add legend and labels
    leg = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Moves the legend outside the plot
    ax.set_xlabel('Index Value')
    ax.set_ylabel('Partner Names')
    ax.set_title('Distribution of Different Indexes for Each Partner')

    # Set y-limits to remove excess blank space
    ax.set_ylim(-0.5, len(data['InitName']) - 0.5)

    # Show the plot in Streamlit
    # st.pyplot(fig2_gi)

    with tab2:
        st.markdown("The following charts display the percentage of completeness for each reporting partner in relation to their general information and member details. The first chart shows the overall completeness index of the General Information Survey, and the second chart identifies specific dimensions that need to be addressed to fully complete this reporting tool.")
        st.pyplot(fig1_gi)
        st.pyplot(fig2_gi)


    ## LEVEL 3: PLEDGE STATEMENTS
    ## LEVEL 3: PLEDGE STATEMENTS
    ## LEVEL 3: PLEDGE STATEMENTS
    ## LEVEL 3: PLEDGE STATEMENTS
    
    # #RANKING CHART #3.1 PLEDGE STATEMENT: % OF COMPLETNESS PLEDGE
    data = df_pledge_summary
    data = df_pledge_summary.sort_values(by='pledge_completeness_idx', ascending=True)
    

    # Set a base figure height and an increment per partner
    base_height = 2
    height_per_partner = 0.1
    fig_height = base_height + height_per_partner * len(data['InitName'])

    fig1_pledge, ax = plt.subplots(figsize=(10, fig_height))
    left = np.zeros(len(data['InitName']))

    # Use colormap
    cmap = cm.get_cmap('RdPu')  # Use RdPu colormap
    colors = cmap(data['pledge_completeness_idx'].values / data['pledge_completeness_idx'].values.max())

    # Adjust the bar height here
    bars = ax.barh(data['InitName'], data['pledge_completeness_idx'], color=colors, height=0.5)  
    # ax.set_xlabel('2023  Pledge completeness Index (%)')  # Indicate percentage in the label
    # ax.set_ylabel('Partner Names')
    ax.set_title('PLEDGE Completeness Index (%) per Partner')
    ax.tick_params(axis='y', labelsize=8)  # Adjust the size of the y-axis labels (partner names)
        
    # Formatting x-tick labels to display as percentages
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:.0f}%'.format(x) for x in vals])

    # Loop over the bars and add the value as text
    for bar in bars:
        width = bar.get_width()
        ax.text(width,  # Set the x position of the text
                bar.get_y() + bar.get_height() / 2,  # Set the y position of the text
                f'{width:.1f}%',  # Set the text to be displayed
                ha='left',  # horizontal alignment
                va='center',
                fontsize=8)  # vertical alignment

    # Remove top and right spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Set y-limits to remove excess blank space
    ax.set_ylim(-0.5, len(data['InitName']) - 0.5)
    ax.set_xlim(0, 100)
    ax.set_xticklabels([])
    ax.tick_params(axis='x', length=0)
        
    # Use tight_layout to fit all elements nicely
    plt.tight_layout()
    # st.pyplot(fig1_pledge)


    # #CHART 3.2: DETAILS OF COMPLETENESS BY DIFFERENT DIMENSIONS (PLEDGE)
    pledge_overall_index_list = ['InitName',
                                'responder_id_pledge_subidx',
                                'p_benefic_all_pledge_subidx',
                                'locally_led_commitment_pledge_subidx',
                                'finance_pledge_subidx',
                                'metrics_explanation_pledge_subidx',
                                'climate_risk_assess_pledge_subidx',
                                'climate_diagnost_pledge_subidx',
                                'members_consultation_pledge_subidx',
                                'confirmation_future_plans_pledge_subidx',]

    # Define your data
    data = df_pledge_summary.sort_values(by='pledge_completeness_idx', ascending=True)
    data = data[pledge_overall_index_list]
    
        
    # Make colormap
    cmap = plt.get_cmap('RdPu', len(pledge_overall_index_list)-1)  # minus 1 because 'q9' is not an index

    # Set the figure size
    fig2_pledge, ax = plt.subplots(figsize=(10, len(data['InitName'])/2))  # Adjust the vertical size according to number of partners

    # Initial left position is zero
    left = np.zeros(len(data['InitName']))

    # Loop over all columns except for 'q9' and create a bar for each
    for i, column in enumerate(pledge_overall_index_list[1:]):
            bars = ax.barh(data['InitName'], data[column], left=left, color=cmap(i), label=column)
            left += data[column]

    # Add legend and labels
    leg = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Moves the legend outside the plot
    ax.set_xlabel('Index Value')
    ax.set_ylabel('Partner Names')
    ax.set_title('Pledge Statement Distribution of Different Indexes for Each Partner')

    # Set y-limits to remove excess blank space
    ax.set_ylim(-0.5, len(data['InitName']) - 0.5)

    # Show the plot in Streamlit
    # st.pyplot(fig2_pledge)


    # CHART #3.3 DISTRIBUTION OF PLEDGES AMONG DIFFERENT BENEFICIARIES [ABSOLUTE NUMBERS - FULL DETAILS]
    def gradient(start_hex, end_hex, n):
        """Generate a gradient of colors between two hex colors."""
        s = np.array([int(start_hex[i:i+2], 16) for i in (1, 3, 5)])
        e = np.array([int(end_hex[i:i+2], 16) for i in (1, 3, 5)])
        return [f"#{int(i[0]):02x}{int(i[1]):02x}{int(i[2]):02x}" for i in np.array([tuple(j) for j in np.linspace(s, e, n)])]

    def plot_chart():
        data = {
            'Primary Beneficiaries': ['Individuals', 'Companies', 'Regions', 'Cities', 'Natural Systems'],
            'Pledge Reported': [partners_report_pledge_d_individuals2023, partners_repor_pledge_companies2023, partners_repor_pledge_regions2023, partners_repor_pledge_cities2023, partners_repor_pledge_nat_syst2023],
            'Numbers Reported': [n_partners_reportingnumberof_direct_individuals2023, n_partners_reportingnumberofcompanies2023_pledge, n_partners_reportingnumberofregions2023_pledge, n_partners_reportingnumberofcities2023_pledge, n_partners_reportingnumberofnaturalsyst2023_pledge],
            'Individuals Benefited': [0, n_partners_reportingnumberofindiv_companies2023, n_partners_reportingnumberofindiv_regions2023, n_partners_reportingnumberofindiv_cities2023, n_partners_reportingnumberofindiv_natsyst2023]
        }

        labels = data['Primary Beneficiaries']
        barWidth = 0.25
        r1 = np.arange(len(data['Pledge Reported']))
        r2 = [x + barWidth for x in r1]
        r3 = [x + barWidth for x in r2]

        colors = gradient("#FF37D5", "#112E4D", 3)

        fig_pledge_full_detail, ax = plt.subplots(figsize=(12, 8))

        # Create bars  ##REVIEW THE NAMES OF THE LABELS
        bars1 = ax.barh(r1, data['Pledge Reported'], color=colors[0], height=barWidth, label='Pledge on Primary Beneficiary') 
        bars2 = ax.barh(r2, data['Numbers Reported'], color=colors[1], height=barWidth, label='Numbers of Primary Beneficiary Reported')
        bars3 = ax.barh(r3, data['Individuals Benefited'], color=colors[2], height=barWidth, label='Individuals Benefited Reported')

        # Display the absolute numbers next to the bars
        for idx, bars in enumerate([bars1, bars2, bars3]):
            for bar, label in zip(bars, labels):
                width = bar.get_width()
                # Avoid placing '0' for Individuals group in the Individuals Benefited bar set
                if not (width == 0 and label == "Individuals" and idx == 2):
                    ax.text(width + 0.5, bar.get_y() + bar.get_height()/2, '%d' % int(width), ha='center', va='bottom')

        # Title & Subtitle
        # plt.title('2023 RtR Pledges Overview')
        # plt.xlabel("Number of RtR Initiatives Reporting Pledges for Each Primary Beneficiary")

        # Y axis
        plt.yticks([r + barWidth for r in range(len(data['Pledge Reported']))], labels)

        plt.tight_layout()
        plt.legend()
        # st.pyplot(fig)
        return fig_pledge_full_detail 
    fig_pledge_full_detail = plot_chart()

    # CHART #3.4 Pledge Overview Simple  [ABSOLUTE NUMBERS]
    def gradient(start_hex, end_hex, n):
        """Generate a gradient of colors between two hex colors."""
        s = np.array([int(start_hex[i:i+2], 16) for i in (1, 3, 5)])
        e = np.array([int(end_hex[i:i+2], 16) for i in (1, 3, 5)])
        return [f"#{int(i[0]):02x}{int(i[1]):02x}{int(i[2]):02x}" for i in np.array([tuple(j) for j in np.linspace(s, e, n)])]

    def plot_chart_single():
        data = {
            'Primary Beneficiaries': ['Individuals', 'Companies', 'Regions', 'Cities', 'Natural Systems'],
            'Pledge Reported': [partners_report_pledge_d_individuals2023, partners_repor_pledge_companies2023, partners_repor_pledge_regions2023, partners_repor_pledge_cities2023, partners_repor_pledge_nat_syst2023],
        }

        # Sort data alphabetically by 'Primary Beneficiaries'
        sorted_indices = np.argsort(data['Primary Beneficiaries'])
        sorted_labels = np.array(data['Primary Beneficiaries'])[sorted_indices]
        sorted_values = np.array(data['Pledge Reported'])[sorted_indices]

        barWidth = 0.6
        r1 = np.arange(len(sorted_labels))

        # Choose your color gradient here or set a single color
        colors = gradient("#FF37D5", "#112E4D", len(sorted_labels))

        fig_pledges_primary_beneficiary, ax = plt.subplots(figsize=(11, 5))
    
        # Create vertical bars
        bars1 = ax.bar(r1, sorted_values, color=colors, width=barWidth)
        
        # Display the absolute numbers above the bars
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.5, '%d' % int(height), ha='center', va='bottom', fontsize=14)

        plt.ylabel("Number of Partners", fontsize=16)
        plt.xlabel("Beneficiary Categories (Pledge)", fontsize=16)
        
        # plt.gcf().subplots_adjust(bottom=0.6) 
        # annotation_text = f"Out of {n_partner_pledge_2023} Partners reporting Pledge Statements"
        # fig_pledges_primary_beneficiary.text(0.95, -0.08, annotation_text, ha='right', va='bottom', fontsize=12, color='black', transform=fig_pledges_primary_beneficiary.transFigure)  # Adjust Y coordinate slightly above the bottom

        # X axis
        plt.xticks(r1, sorted_labels, fontsize=14, rotation=0)  # Rotate labels for better visibility
        ax.tick_params(axis='y', labelsize=14)
        ax.tick_params(axis='x', length=5)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # X axis: Setting integer ticks
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True)) 
        ax.set_ylim(0, 29)
        
        plt.tight_layout()
        plt.legend(fontsize=12)
        return fig_pledges_primary_beneficiary 

    # # Usage
    fig_pledges_primary_beneficiary = plot_chart_single()
    # st.write('Pledge Overview Correcto Numeros Obsolutos')
    # st.pyplot(fig_pledges_primary_beneficiary)


    ## CHART 3.5 PLEDGE IN PORCENTAJE

    def gradient(start_hex, end_hex, n):
        """Generate a gradient of colors between two hex colors."""
        s = np.array([int(start_hex[i:i+2], 16) for i in (1, 3, 5)])
        e = np.array([int(end_hex[i:i+2], 16) for i in (1, 3, 5)])
        return [f"#{int(i[0]):02x}{int(i[1]):02x}{int(i[2]):02x}" for i in np.array([tuple(j) for j in np.linspace(s, e, n)])]


    n_total = n_reporting_partners
    def plot_chart_single():
        # Your data goes here:
        data = {
            'Primary Beneficiaries': ['Individuals', 'Regions', 'Cities', 'Natural Systems'],
            'Pledge Reported': [partners_report_pledge_d_individuals2023, partners_repor_pledge_regions2023, partners_repor_pledge_cities2023, partners_repor_pledge_nat_syst2023],
            }

        # Convert absolute values to percentages
        data['Pledge Reported'] = [(value / n_total) * 100 for value in data['Pledge Reported']]
        
        
        st.write(data)

        # Sort data alphabetically by 'Pledge Reported'
        sorted_indices = np.argsort(data['Pledge Reported'])[::-1] 
        sorted_labels = np.array(data['Primary Beneficiaries'])[sorted_indices]
        sorted_values = np.array(data['Pledge Reported'])[sorted_indices]

        barWidth = 0.6
        r1 = np.arange(len(sorted_labels))

        fig_pledges_beneficiaries_percentg, ax = plt.subplots(figsize=(11, 3))
        
        colors = gradient("#FF37D5", "#112E4D", 5)

        # Create vertical bars
        bars1 = ax.bar(r1, sorted_values, color=colors, width=barWidth)  # Choose a color or use your gradient function

        # Display the percentages above the bars
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.5, '%.1f%%' % height, ha='center', va='bottom', fontsize=14)

        plt.ylabel("% Partners", fontsize=16)
        plt.xlabel("Beneficiary Categories (Pledge)", fontsize=16)

        # X axis
        plt.xticks(r1, sorted_labels, fontsize=14, rotation=0)  # Rotate labels for better visibility
        ax.tick_params(axis='y', labelsize=14)
        ax.tick_params(axis='x', length=5)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # Remove Y-axis ticks and labels
        ax.set_yticks([])  # Removes the Y-axis ticks
        ax.set_yticklabels([])  # Removes the Y-axis labels

        # Adjust the y-axis limits and ticks to accommodate percentages
        ax.set_ylim(0, 100)
        ax.yaxis.set_major_formatter(ticker.PercentFormatter())

        plt.tight_layout()
        plt.legend(fontsize=12)
        return fig_pledges_beneficiaries_percentg 
        

    fig_pledges_beneficiaries_percentg = plot_chart_single()
    # st.write('Pledge Overview Percentage ')
    
    # st.pyplot(fig_pledges_beneficiaries_percentg)


    with tab3:
        st.markdown("Percentage of Completness of Partners Pledge Statements")
        st.pyplot(fig1_pledge)
        st.pyplot(fig2_pledge)
        st.markdown("Distribition of Partners Pledge Statement by Beneficiary ")
        st.pyplot(fig_pledges_beneficiaries_percentg)
        # st.pyplot(fig_pledges_primary_beneficiary)
        st.pyplot(fig_pledge_full_detail)
        




    # LEVEL 4) PLAN (ALL: CONSOLIDATED & ONLY 2023 INFO)
    # LEVEL 4) PLAN (ALL: CONSOLIDATED & ONLY 2023 INFO)
    # LEVEL 4) PLAN (ALL: CONSOLIDATED & ONLY 2023 INFO)

    ## CHART 4.1 PLAN CONSOLIDATED (2022 AND 2023) FULL
    ### Chart Number of Plan Consolidated: After the dataset of 2023 and 2022 are united based on 2023 as primary information
    # Chart of different 2022 and 2023 number of charts
    # Grouping and plotting data
    grouped = df_2023_plan.groupby(['InitName', 'PlanYear']).size().unstack().fillna(0)

    fig_plan2022_2023_full, ax = plt.subplots(figsize=(10, 7))
    width = 0.4
    ind = np.arange(len(grouped))

    ax.barh(ind - width/2, grouped.get('2022', 0), width, color='#112E4D', label='2022')
    ax.barh(ind + width/2, grouped.get('2023', 0), width, color='#FF37D5', label='2023')

    ax.set_xlabel('Number of Resilience-Building Plans')
    ax.set_title('Resilience-Building Plans by RtR Initiatives for 2022 and 2023')
    ax.set_yticks(ind)
    ax.set_yticklabels(grouped.index)
    ax.legend()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_axisbelow(True)
    ax.xaxis.grid(color='gray', linestyle='dashed', which='both', linewidth=0.5)
    plt.tight_layout()
    # st.pyplot(fig_plan2022_2023_full)


    # ## CHART 4.2 PLAN CONSOLIDATED (UPDATED)
    # ## Chart of only one colums with the number of plan per partner in 2023
    # # Chart of different 2022 and 2023 number of charts
    # # Grouping and plotting data
    # grouped = df_2023_plan.groupby(['InitName', 'PlanYear']).size().unstack().fillna(0)

    # fig_plan2022_2023_simple_consolidated, ax = plt.subplots(figsize=(10, 7))
    # width = 0.4
    # ind = np.arange(len(grouped))

    # ax.barh(ind - width/2, grouped.get('2022', 0), width, color='#112E4D', label='Submitted in 2022')
    # ax.barh(ind + width/2, grouped.get('2023', 0), width, color='#FF37D5', label='Updated in 2023')

    # ax.set_xlabel('Number of Resilience-Building Plans')
    # ax.set_title('Resilience-Building Plans by RtR Initiatives')
    # ax.set_yticks(ind)
    # ax.set_yticklabels(grouped.index)
    # ax.legend()
    # ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # ax.set_axisbelow(True)
    # ax.xaxis.grid(color='gray', linestyle='dashed', which='both', linewidth=0.5)
    # plt.tight_layout()
    # # st.pyplot(fig_plan2022_2023_simple_consolidated)


    # n_plans_reporting_metrics_plan_consolidated  # Numbers of plans whit information in metrics about individuals
    # n_2022_2023_plans_individuals # Number of plans per primary beneficiay
    # n_2022_2023_plans_companies # Number of plans per primary beneficiay
    # n_2022_2023_plans_regions # Number of plans per primary beneficiay
    # n_2022_2023_plans_cities # Number of plans per primary beneficiay
    # n_2022_2023_plans_natsyst # Number of plans per primary beneficiay


    # Chart #4.3 Plan Overview Simple   
    def gradient(start_hex, end_hex, n):
        """Generate a gradient of colors between two hex colors."""
        s = np.array([int(start_hex[i:i+2], 16) for i in (1, 3, 5)])
        e = np.array([int(end_hex[i:i+2], 16) for i in (1, 3, 5)])
        return [f"#{int(i[0]):02x}{int(i[1]):02x}{int(i[2]):02x}" for i in np.array([tuple(j) for j in np.linspace(s, e, n)])]


    def plot_chart_single_plan():
        # Your data goes here:
        data = {
            'Primary Beneficiaries': ['Individuals', 'Companies', 'Regions', 'Cities', 'Natural Systems'],
            'Plan Reported': [n_2022_2023_plans_individuals, n_2022_2023_plans_companies, n_2022_2023_plans_regions, n_2022_2023_plans_cities, n_2022_2023_plans_natsyst],
        }

        # Sort data alphabetically by 'Primary Beneficiaries'
        sorted_indices = np.argsort(data['Primary Beneficiaries'])
        sorted_labels = np.array(data['Primary Beneficiaries'])[sorted_indices]
        sorted_values = np.array(data['Plan Reported'])[sorted_indices]

        barWidth = 0.6
        r1 = np.arange(len(sorted_labels))

        # Choose your color gradient here or set a single color
        colors = gradient("#FF37D5", "#112E4D", len(sorted_labels))

        fig_plans_primary_beneficiary, ax = plt.subplots(figsize=(11, 2))

        # Create bars
        bars1 = ax.bar(r1, sorted_values, color=colors, width=barWidth)

        # Display the absolute numbers above the bars
        for bar in bars1:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height + 0.5, '%d' % int(height), ha='center', va='bottom', fontsize=14)

        plt.xlabel("Type of Beneficiary", fontsize=12)
        plt.ylabel("N° Plans", fontsize=12)

        # plt.gcf().subplots_adjust(bottom=0.6)
        # annotation_text = f"Out of {n_total_plans_consolidated} plans from {n_partner2022_2023_plan} Partners (Source: Plan Survey 2022 and 2023)"
        # fig_plans_primary_beneficiary.text(0.95, -0.08, annotation_text, ha='right', va='bottom', fontsize=12, color='black', transform=fig_plans_primary_beneficiary.transFigure)

        # X axis
        plt.xticks(r1, sorted_labels, fontsize=10, rotation=0)
        ax.tick_params(axis='y', labelsize=10)
        ax.tick_params(axis='x', length=5)
        ax.spines['right'].set_visible(False)   
        ax.spines['top'].set_visible(False)

        # Y axis: Setting integer ticks
        ax.yaxis.set_major_locator(ticker.MaxNLocator(integer=True))
        # ax.set_ylim(0, 29)

        plt.tight_layout()
        plt.legend(fontsize=12)
        return fig_plans_primary_beneficiary 

    # Usage
    fig_plans_primary_beneficiary = plot_chart_single_plan()
    # st.write('RtR Plans on Primary Beneficiary - Overview (simple)')
    # st.pyplot(fig_plans_primary_beneficiary)









    ## #RANKING CHART #4.4 PLAN (ONLY 2023)
    data = df_2023_plan.sort_values(by='plan_completeness_idx', ascending=True)
   
    base_height = 2
    height_per_partner = 0.1
    fig_height = base_height + height_per_partner * len(data['plan_short_name'])

    fig1_plan, ax = plt.subplots(figsize=(10, fig_height))
    left = np.zeros(len(data['plan_short_name']))

    # Use colormap
    cmap = cm.get_cmap('RdPu')  # Use RdPu colormap
    colors = cmap(data['plan_completeness_idx'].values / data['plan_completeness_idx'].values.max())


    # Adjust the bar height here
    bars = ax.barh(data['plan_short_name'], data['plan_completeness_idx'], color=colors, height=0.5)  
    # ax.set_xlabel('2023 GIS Completeness Index (%)')  # Indicate percentage in the label
    # ax.set_ylabel('Partner Names')
    ax.set_title('2023 PLAN Completeness Index (%) per Partner')
    ax.tick_params(axis='y', labelsize=8)  # Adjust the size of the y-axis labels (partner names)
        
    # Formatting x-tick labels to display as percentages
    vals = ax.get_xticks()
    ax.set_xticklabels(['{:.0f}%'.format(x) for x in vals])

    # Loop over the bars and add the value as text
    for bar in bars:
        width = bar.get_width()
        ax.text(width,  # Set the x position of the text
                bar.get_y() + bar.get_height() / 2,  # Set the y position of the text
                f'{width:.1f}%',  # Set the text to be displayed
                ha='left',  # horizontal alignment
                va='center',
                fontsize=8)  # vertical alignment

    # Remove top and right spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Set y-limits to remove excess blank space
    ax.set_ylim(-0.5, len(data['plan_short_name']) - 0.5)
    ax.set_xlim(0, 100)
    ax.set_xticklabels([])
    ax.tick_params(axis='x', length=0)
        
    # Use tight_layout to fit all elements nicely
    plt.tight_layout()
    # st.pyplot(fig1_plan)



    # #Horizontal Chart 4.5_Multi Index (ONLY 2023)

    list_to_plan_chart_all_index = ['plan_short_name',
                                    'plan_identif_subidx',
                                    'description_plan_subidx',
                                    'saa_plan_subidx',
                                    'ra_plan_subidx',
                                    'pri_benef_magnitud_plan_subidx',
                                    'governance_plan_subidx', # REVISAR PORQUË NO LO LEE
                                    'barriers_plan_subidx',
                                    'finance_plan_subidx',
                                    'monitoring_data_collect_plan_subidx'
                                    ]

    # Define your data
    data = df_2023_plan.sort_values(by='plan_completeness_idx', ascending=True)
    data = data[list_to_plan_chart_all_index]
        
    # Make colormap
    cmap = plt.get_cmap('RdPu', len(list_to_plan_chart_all_index)-1)  # minus 1 because 'q9' is not an index

    # Set the figure size
    fig2_plan, ax = plt.subplots(figsize=(10, len(data['plan_short_name'])/2))  # Adjust the vertical size according to number of partners

    # Initial left position is zero
    left = np.zeros(len(data['plan_short_name']))

    # Loop over all columns except for 'q9' and create a bar for each
    for i, column in enumerate(list_to_plan_chart_all_index[1:]):
            bars = ax.barh(data['plan_short_name'], data[column], left=left, color=cmap(i), label=column)
            left += data[column]

    # Add legend and labels
    leg = ax.legend(loc='upper left', bbox_to_anchor=(1, 1))  # Moves the legend outside the plot
    ax.set_xlabel('Index Value')
    ax.set_ylabel('Partner Names')
    ax.set_title('PLAN Distribution of Different Indexes for Each Partner')

    # Set y-limits to remove excess blank space
    ax.set_ylim(-0.5, len(data['plan_short_name']) - 0.5)

    # Show the plot in Streamlit
    # st.pyplot(fig2_plan)



    ## CHART % PLANES GENERAL 
    # name of the chart: fig_plans_percentaje_submissions

    # Variables
    # n_reporting_partners  #total reporting partners (all)
    # n_partner2022_2023_plan #total partners reporting plan (all)
    n_no_plan_reporting_partners = n_reporting_partners - n_partner2022_2023_plan
    # n_partner_plan_only2023 #Partners reporting and updating plans in 2023 
    n_partner_plan_only2022 = n_partner2022_2023_plan - n_partner_plan_only2023

    # # Variables needed
    # n_reporting_partners
    # n_no_plan_reporting_partners
    # n_partner2022_2023_plan
    # n_partner_plan_only2023
    # n_partner_plan_only2022

    # n_no_plan_reporting_partners
    # n_partner_plan_only2023
    # n_partner_plan_only2022


    # n_no_plan_reporting_partners
    # n_partner2022_2023_plan


    ## CHART % PARTNERS REPORTING PLAN (SIMPLE)

    # Calculate the percentages
    percent_no_plan = (n_no_plan_reporting_partners / n_reporting_partners) * 100
    percent_plan = (n_partner2022_2023_plan / n_reporting_partners) * 100

    # Set darker colors from the RdPu palette
    bar_colors = sns.color_palette("RdPu", n_colors=3)
    bar_height = 1  # The height of the bar to make it narrow

    # Set the size of the figure
    fig_width = 10  # You can adjust this as needed
    fig_height = 1.8  # You can adjust this as needed

    # Create the figure with a defined size
    fig_plans_percentaje_submissions_simple, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Plotting the stacked horizontal bar with the 'height' parameter
    bars = ax.barh(['Partners'], [percent_plan], color=bar_colors[2], label='Plan(s) Submitted', height=bar_height)
    ax.barh(['Partners'], [percent_no_plan], left=[percent_plan], color=bar_colors[0], label='No Plan Submitted', height=bar_height)

    # Position the legend in the upper right corner
    ax.legend(loc='upper right')    

    text_position = bar_height / 50

    ax.text(percent_plan / 2, text_position, f'{percent_plan:.1f}% ({n_partner2022_2023_plan})', va='center', ha='center', color='white')
    ax.text(percent_plan + percent_no_plan / 2, text_position, f'{percent_no_plan:.1f}% ({n_no_plan_reporting_partners})', va='center', ha='center', color='black')

    # Set labels and title
    ax.set_xlabel('Percentage (%)')

    # Remove top and right spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    ax.set_title('Plan Submission Percentages')

    # Show the figure in the Streamlit app
    # st.pyplot(fig_plans_percentaje_submissions_simple)






    ## CHART % PARTNERS REPORTING PLAN (DETAILED)
    # Calculate the percentages
    percent_no_plan = (n_no_plan_reporting_partners / n_reporting_partners) * 100  # No plan submitted
    percent_plan2022 = (n_partner_plan_only2022 / n_reporting_partners) * 100     # Plan submitted in 2022
    percent_plan_updated2023 = (n_partner_plan_only2023 / n_reporting_partners) * 100 # Plans submitted in 2023

    # Set darker colors from the RdPu palette
    bar_colors = sns.color_palette("RdPu", n_colors=3)
    bar_height = 0.1  # The height of the bar to make it narrow

    # Create the figure with a defined size
    fig_width = 9
    fig_height = 2
    fig_plans_percentaje_submissions_detailed, ax = plt.subplots(figsize=(fig_width, fig_height))

    # Plotting the stacked horizontal bar
    bars = ax.barh(['Partners'], [percent_plan2022], color=bar_colors[2], label='Submitting Plans in 2022', height=bar_height)
    ax.barh(['Partners'], [percent_plan_updated2023], left=[percent_plan2022], color=bar_colors[1], label='Plans Updated/Submitted in 2023', height=bar_height)
    ax.barh(['Partners'], [percent_no_plan], left=[percent_plan2022 + percent_plan_updated2023], color=bar_colors[0], label='No Plans Submitted', height=bar_height)

    # Adjust layout to make space for the legend below the chart
    plt.subplots_adjust(bottom=0.25)  # Adjust this value as needed

    # Position the legend below the plot area
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.35), fancybox=True, shadow=False, ncol=3)


    # Adding value labels with both percentage and absolute number
    text_position = bar_height / 50
    ax.text(percent_plan2022 / 2, text_position, f'{percent_plan2022:.1f}% ({n_partner_plan_only2022})', va='center', ha='center', color='black')
    ax.text(percent_plan2022 + percent_plan_updated2023 / 2, text_position, f'{percent_plan_updated2023:.1f}% ({n_partner_plan_only2023})', va='center', ha='center', color='black')
    ax.text(percent_plan2022 + percent_plan_updated2023 + percent_no_plan / 2, text_position, f'{percent_no_plan:.1f}% ({n_no_plan_reporting_partners})', va='center', ha='center', color='black')

    # Set labels
    ax.set_xlabel('Percentage (%)')

    # Remove top and right spines
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    # Show the figure in the Streamlit app
    # st.pyplot(fig_plans_percentaje_submissions_detailed)



    with tab4:
        st.write('CONSOLIDATION OF PLANS 2022 AND 2023')
        st.pyplot(fig_plans_percentaje_submissions_simple)
        # st.pyplot(fig_plans_percentaje_submissions_detailed)
        # st.pyplot(fig_plan2022_2023_full)
        # st.pyplot(fig_plan2022_2023_simple_consolidated)
        st.pyplot(fig_plans_primary_beneficiary)

        st.write('DETAILS ONLY ON UPDATED 2023 PLANS')
        st.pyplot(fig1_plan)
        st.pyplot(fig2_plan)

    # # # ______________________________________________
    # # # ______________________________________________
    # # # END BLOCK GI PLEDGE PLAN DESCRIPTION
    # # # ______________________________________________
    # # # ______________________________________________



