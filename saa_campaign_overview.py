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
from wordcloud import WordCloud, STOPWORDS
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


def saa_campiagn_overview(df_gi,n_reporting_partners):
    # # ______________________________________________
    # # BLOCK SAA_____________________________________
    # # ______________________________________________

    st.markdown("### PARTNERS ALIGNMENT WITH THE SHARM-EL-SHEIKH ADAPTATION AGENDA (SAA) PRIORITY SYSTEMS")
    # st.markdown("*Comprehensive Partners Alignment with the Sharm-el-Sheikh Adaptation Agenda (SAA) Priority Systems*")
    st.markdown("Addressing the urgency of global changes requires more concerted efforts at a faster pace and larger scale. This tool shows the growing commitment of NPS in accelerating inclusive and equitable climate action to significantly enhance the required speed and scale. The adaptation solutions delivered span across all priority systems included in the Sharm-el-Sheikh Adaptation Agenda.")
    
    def calculations_saa(df_gi):
        impact_systems = {
        'Finance: Cross-cutting': 'q148',
        'Planning and Policy: Cross-cutting': 'q138',
        'Water and Nature': 'q86',
        'Infrastructure': 'q123',
        'Coastal and Oceans': 'q112',
        'Human Settlements': 'q99',
        'Health': 'q136',
        'Food and Agriculture': 'q77'
        }

        saa_to_explanation = {
            'q77': 'q78', 
            'q86': 'q87',
            'q99': 'q100',
            'q112':'q113',
            'q123':'q124',
            'q136':'q137',
            'q138':'q139',
            'q148':'q149'
        }

        impact_system_list = []
        partner_list = []
        relationship_list = []
        explanation_list = []

        for impact_system, column_name in impact_systems.items():
            partners = df_gi['InitName']
            relationships = df_gi[column_name]
            if column_name in saa_to_explanation:
                explanations = df_gi[saa_to_explanation[column_name]]
            else:
                explanations = [pd.NA] * len(partners)
            
            impact_system_list.extend([impact_system] * len(partners))
            partner_list.extend(partners)
            relationship_list.extend(relationships)
            explanation_list.extend(explanations)

        new_df_gi = pd.DataFrame({
            'Partner Name': partner_list,
            'SAA Impact Systems': impact_system_list,
            'Relationship': relationship_list,
            'Explanation (optional)': explanation_list
        })

        new_df_gi['SAA Impact Systems'] = pd.Categorical(new_df_gi['SAA Impact Systems'], categories=impact_systems.keys(), ordered=True)
        new_df_gi['relation_yes'] = new_df_gi['Relationship'].apply(lambda x: 'Yes' if pd.notna(x) and x != 'Unsure' and x != 'Not Related' else pd.NA)

        #Data Set SAA Summary with RtR Partners & Number of SAA Taskforces
        n_partner_with_saa = new_df_gi[new_df_gi['relation_yes'] == 'Yes']
        n_partner_with_saa = n_partner_with_saa['Partner Name'].value_counts().reset_index()
        n_partner_with_saa.rename(columns={'count': 'N° SAA Taskforces'}, inplace=True)
        n_partner_with_saa.rename(columns={'Partner Name': 'RtR PARTNER NAME'}, inplace=True)
        summary_partner_saa = n_partner_with_saa
        new_order_saa = ['RtR PARTNER NAME','N° SAA Taskforces']

        summary_partner_saa = summary_partner_saa[new_order_saa].sort_values('N° SAA Taskforces', ascending=False)
        summary_partner_saa.rename(columns={'SURVEY RESPONSE STATUS': 'Reliability','RtR PARTNER NAME':'Name'}, inplace=True)
        summary_partner_saa['Related to SAA'] = np.where(summary_partner_saa['N° SAA Taskforces'].notna(), "Yes", "Pending Confirmation")
        # st.write(summary_partner_saa)
            
        # Compute counts of unique values
        value_counts = summary_partner_saa['Related to SAA'].value_counts()
        # Compute percentages
        percentages = value_counts / len(summary_partner_saa) * 100
        # Combine the counts and percentages into a DataFrame for display
        stats_SAA_df_gi = pd.DataFrame({
            'Is the Partner related to an SAA Taskforce?': value_counts.index,
            'Count': value_counts.values,
            'Percentage (%)': percentages.values
        })
        stats_SAA_df_gi = stats_SAA_df_gi.reset_index(drop=True)
        
        return  new_df_gi, summary_partner_saa
    new_df_gi, summary_partner_saa = calculations_saa(df_gi)

    #RtR Partners related to each SAA Priority Systems (direct/indirect)
    def chart_types_rtr_partners_saa_p_systems():
        # st.markdown("#### Relationship Types of RtR Partners with SAA Impact Systems")  # SHOWN IN 2023 REPORT
        # Chart % OFICIAL
        # Making DataSet with all SAA Taskforces Details for Chart
        new_df_gi_filtered = new_df_gi[new_df_gi['relation_yes'] == 'Yes']
        grouped_data_all = new_df_gi.groupby(['SAA Impact Systems', 'Relationship'], sort=False).size().unstack().reset_index()
        grouped_data_details = new_df_gi_filtered.groupby(['SAA Impact Systems', 'Relationship'], sort=False).size().unstack()

        # Set the color palette
        sns.set_palette("RdPu")

        # Create the plot
        fig_partners_saa_detail, ax = plt.subplots(figsize=(6, len(grouped_data_details) / 2))

        # Create the horizontal bar chart
        grouped_data_details.plot(kind='barh', stacked=True, ax=ax)

        # Set the plot title and axis labels
        ax.set_xlabel('Number of RtR Partners')
        ax.set_ylabel('SAA Priority Systems')
        ax.set_xlim([0, 34])

        # Add individual and total values on the bars
        for p in ax.patches:
            left, bottom, width, height = p.get_bbox().bounds
            ax.text(left + width/2, bottom + height/2, int(width), ha='center', va='center')

        
        totals = grouped_data_details.sum(axis=1)
        total_base = n_reporting_partners

        for i, total in enumerate(totals):
            percentage = (total / total_base) * 100  # Calculate the percentage
            ax.text(total + 0.2, i, f'{int(total)} ({percentage:.1f}%)', va='center')

        # Adjust legend and spines
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_title('RtR Partners related to each SAA Priority Systems (2024) ', fontsize=12)

        # Show the plot in Streamlit
        # st.write('"Percentage of RtR Partners related to each SAA Impact Systems [Details]"')
        # st.pyplot(fig_partners_saa_detail) 
        
        return grouped_data_all,grouped_data_details,new_df_gi_filtered,fig_partners_saa_detail,
    grouped_data_all,grouped_data_details,new_df_gi_filtered,fig_partners_saa_detail = chart_types_rtr_partners_saa_p_systems()
    
    #Comparative Chart 2023-2024
    def comparative_chart_2023_2024():
        ## Comparative Chart 2023-2024
        ## Making Data Set    
        saa_data_2023 = {
        'SAA Impact Systems': [
            'Food and Agriculture', 
            'Health', 
            'Human Settlements', 
            'Coastal and Oceans', 
            'Infrastructure', 
            'Water and Nature', 
            'Planning and Policy: Cross-cutting', 
            'Finance: Cross-cutting'
        ],
        '2023': [18, 10, 14, 12, 9, 17, 14, 19],
        'Percentage 2023': ['62.1%', '34.5%', '48.3%', '41.4%', '31.0%', '58.6%', '48.3%', '65.5%']
        }
        saa_data_2023 = pd.DataFrame(saa_data_2023)
        n_reporting_partners_2023 = 29
        
        saa_data_2024 = grouped_data_details.copy()  # Make a copy of the original DataFrame
        saa_data_2024['2024'] = saa_data_2024['Directly related'] + saa_data_2024['Indirectly related']  # Calculate '2024'
        saa_data_2024 = saa_data_2024.reset_index()
        # st.write(saa_data_2024)  # Display the DataFrame
        # st.write(saa_data_2024.columns)
        
        saa_2023_2024_comparison_db = pd.merge(
        saa_data_2024[['SAA Impact Systems', '2024']],
        saa_data_2023[['SAA Impact Systems', '2023',]], 
        
        on='SAA Impact Systems', 
        how='inner'  )


        # Calculate percentages for 2023 and 2024
        saa_2023_2024_comparison_db['Percentage 2023'] = (saa_2023_2024_comparison_db['2023'] / n_reporting_partners_2023) * 100
        saa_2023_2024_comparison_db['Percentage 2024'] = (saa_2023_2024_comparison_db['2024'] / n_reporting_partners) * 100

        # Calculate percentage for 2024 but based on N=29 (as in 2023)
        saa_2023_2024_comparison_db['Percentage 2024 (based on N=29)'] = (saa_2023_2024_comparison_db['2024'] / 29) * 100

        # Calculate the percentage difference between 2023 and 2024 based on N=34 for 2024
        saa_2023_2024_comparison_db['% Difference (2024 vs 2023)'] = saa_2023_2024_comparison_db['Percentage 2024'] - saa_2023_2024_comparison_db['Percentage 2023']

        # Calculate the percentage difference between 2023 and 2024 normalized to N=29
        saa_2023_2024_comparison_db['% Difference (2024 vs 2023 N=23)'] = saa_2023_2024_comparison_db['Percentage 2024 (based on N=29)'] - saa_2023_2024_comparison_db['Percentage 2023']

        # st.write(saa_2023_2024_comparison_db)  # Display the DataFrame
        # st.write(saa_2023_2024_comparison_db.columns)
    
        saa_2023_2024_comparison_db = saa_2023_2024_comparison_db.sort_values(by='2024', ascending=True)
        
        ## CHART

        # Set the Seaborn palette
        sns.set_palette("RdPu")

        # Create the figure and axis for plotting
        fig, ax = plt.subplots(figsize=(10, 4))

        # Normalize the 2023 and 2024 values by dividing by 34
        saa_2023_2024_comparison_db['2023_normalized'] = saa_2023_2024_comparison_db['2023'] / n_reporting_partners * 100
        saa_2023_2024_comparison_db['2024_normalized'] = saa_2023_2024_comparison_db['2024'] / n_reporting_partners * 100

        # Define the position of the bars
        bar_width = 0.3
        index = np.arange(len(saa_2023_2024_comparison_db))

        # Set the x-axis limits from 0 to 100%
        ax.set_xlim(0, 100)
    
        # Set the x-axis ticks at intervals of 10 points
        ax.set_xticks(np.arange(0, 101, 10))

        # Plot 2023 and 2024 bars side by side with the normalized values
        bars_2023 = ax.barh(index, saa_2023_2024_comparison_db['2023_normalized'], bar_width, label='2023')
        bars_2024 = ax.barh(index + bar_width, saa_2023_2024_comparison_db['2024_normalized'], bar_width, label='2024')

        # # Add percentage labels at the end of 2024 bars with 1 decimal point
        # for idx, bar in enumerate(bars_2024):
        #     ax.text(bar.get_width() + 1, bar.get_y() + bar.get_height() / 2, f"{saa_2023_2024_comparison_db['Percentage 2024'][idx]:.1f}%", va='center')

        # Set x-axis and y-axis labels for better clarity
        ax.set_xlabel('Percentage of Partners')
        ax.set_ylabel('SAA Priority Systems')

        # Set the y-ticks and labels for the systems
        ax.set_yticks(index + bar_width / 2)
        ax.set_yticklabels(saa_2023_2024_comparison_db['SAA Impact Systems'])

        # Move the legend to the outside
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))

        # Hide the right and top spines for cleaner look
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Set a title for the chart
        ax.set_title('RtR Partners related to each SAA Priority System (2023 & 2024)', fontsize=10)

        # Add the text "N = 34" in the bottom right corner
        ax.text(1, -0.1, "N = 34", transform=ax.transAxes, fontsize=9, verticalalignment='center', horizontalalignment='right')

        # Show the plot in Streamlit
        
        st.pyplot(fig)
    
    ## Number of SAA Priority Systems per RtR Partner
    def chart_saa_n_p_systems(summary_partner_saa):
        #Making a Chart for the Number of SAA Taskforces

        #putting 0 to all NA to display them on the chart
        saa_partner_chart = summary_partner_saa
        saa_partner_chart['N° SAA Taskforces'] = saa_partner_chart['N° SAA Taskforces'].fillna(0)

        # Set the desired height for the chart
        fig_height = len(saa_partner_chart) * 0.2

        # Create the horizontal bar chart
        fig_n_priority_systems_saa, ax = plt.subplots(figsize=(8, fig_height))
        bars = ax.barh(saa_partner_chart['Name'], saa_partner_chart['N° SAA Taskforces'], height=0.6)

        # Set the plot title and axis labels
        ax.set_title("Number of SAA Priority Systems per RtR Partner", fontsize=10)
        ax.set_xlabel('Number of SAA Priority Systems', fontsize=8)
        ax.set_ylabel('RtR Partners', fontsize=8)

        # Set the font size for x-axis labels
        plt.xticks(fontsize=6)
        # Set the font size for partner names
        plt.yticks(fontsize=6)

        # Add values on each bar
        for bar in bars:
            width = bar.get_width()
            label_y_pos = bar.get_y() + bar.get_height() / 2
            if not np.isnan(width):  # Check if width is not NaN
                if width == 0:
                    ax.text(width + 0.1, label_y_pos, "Pending Confirmation", fontsize=6, va='center', ha='left')
                else:
                    ax.text(width + 0.1, label_y_pos, s=f'{int(width)}', fontsize=6, va='center', ha='left')
                
        # Remove top and right spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

        # Set y-limits to remove excess blank space
        ax.set_ylim(-0.5, len(saa_partner_chart['Name']) - 0.5)

        # Invert the y-axis to display partners from top to bottom
        ax.invert_yaxis()

        # Use tight_layout to fit all elements nicely
        plt.tight_layout()  
        
        # Show the plot in Streamlit
        # st.pyplot(fig_n_priority_systems_saa)
    
        return fig_n_priority_systems_saa
    fig_n_priority_systems_saa = chart_saa_n_p_systems(summary_partner_saa)

    #NOT IN USE.
    def treemap_chart_how_saa(new_df_gi_filtered):
        # TREEMAP Chart about how
        # st.markdown("Some Partners have provided descriptions of how they relate to SAA Priority Systems. The following tree map shows this information")

        saa_partners_toplot = new_df_gi_filtered
        saa_partners_toplot['concat'] = saa_partners_toplot['Partner Name'].astype(str) + saa_partners_toplot['SAA Impact Systems'].astype(str)

        # Calculate counts for each unique value
        value_counts = saa_partners_toplot['concat'].value_counts()
        # Calculate percentages
        total = len(saa_partners_toplot)
        value_percentages = (value_counts / total) * 100
        # If you want to add this percentage to your dataframe for each corresponding value
        saa_partners_toplot['% Partner'] = saa_partners_toplot['concat'].map(value_percentages)

        # Calculate occurrence of each SAA Taskforce
        taskforce_counts = saa_partners_toplot['SAA Impact Systems'].value_counts()
        # Calculate the percentage for each SAA Taskforce
        total = len(saa_partners_toplot)
        taskforce_percentage = (taskforce_counts / total) * 100
        # Map the percentage back to the original dataframe
        saa_partners_toplot['%SAA Taskforce'] = saa_partners_toplot['SAA Impact Systems'].map(taskforce_percentage)

        def add_line_breaks(text, char_limit=100):
            if text == "nan":  # if it's a NaN converted to string
                return ""
            words = text.split()
            lines = []
            current_line = ""
            for word in words:
                if len(current_line + word) > char_limit:
                    lines.append(current_line.strip())
                    current_line = ""
                current_line += word + " "
            lines.append(current_line.strip())
            return '<br>'.join(lines)

        # Convert all values in the column to string before applying the function
        saa_partners_toplot['Explanation (formatted)'] = saa_partners_toplot['Explanation (optional)'].astype(str).apply(add_line_breaks)


        fig_treemap = px.treemap(saa_partners_toplot, 
                                path=[px.Constant("Relation to SAA Priority Systems"), 
                                    'SAA Impact Systems', 'Relationship', 'Partner Name', 'Explanation (formatted)'], 
                                values='% Partner', 
                                color='%SAA Taskforce', 
                                color_continuous_scale='RdPu',
                                custom_data=['Explanation (formatted)'])

        fig_treemap.update_traces(root_color="#FF37D5", 
                                marker_line_color='grey', 
                                hovertemplate='%{customdata[0]}<extra></extra>'
                                )

        fig_treemap.data[0].hovertemplate = '%{value:.1f}%'

        fig_treemap.update_layout(title_text="RTR Partner's description of their relation to SAA Priority Systems.",
                                margin=dict(t=50, l=25, r=25, b=25),
                                width=1000)

        
        # st.plotly_chart(fig_treemap)
        
        # with st.expander("Explore Data: RtR Partner's Relationship with SAA Priority Systems"):
        #     st.markdown("##### RtR Partner's Relationship with SAA Priority Systems")
        #     st.write(grouped_data_all)
        # # st.pyplot(fig_n_priority_systems_saa)## <--- This one is oficial
        # st.plotly_chart(fig_treemap)
        
        outcome_to_explanation = {
            #Food and Agriculture Systems
            'q79':'q79',
            'q80': 'q83', 
            'q81': 'q84', 
            'q82': 'q85',
            
            #Water and Natural Systems
            'q88':'q88',
            'q89': 'q94',
            'q90': 'q95',
            'q91': 'q96',
            'q92': 'q97',
            'q93': 'q98',
            #Human Settlements
            'q101': 'q101',
            'q102': 'q107',
            'q103': 'q108',
            'q104': 'q109',
            'q105': 'q110',
            'q106': 'q111',
            #Coastal and Oceanic Systems 
            'q114': 	'q114',
            'q115': 	'q119',
            'q116': 	'q120',
            'q117': 	'q121',
            'q118': 	'q122',
            
            #Infrastructure Systems
            'q125': 	'q125',
            'q126': 	'q131',
            'q127': 	'q132',
            'q128': 	'q133',
            'q129': 	'q134',
            'q130': 	'q135', 
            
            #Cross-Cutting Enabler 'Planning'
            'q139': 	'q139',
            'q140': 	'q144',
            'q141': 	'q145',
            'q142': 	'q146',
            'q143': 	'q147',
            
            #Cross-Cutting Enabler 'Finance'
            'q150': 	'q150',
            'q151': 	'q154',
            'q152': 	'q155',
            'q153': 	'q156',
        }

        task_force_to_outcome = {
            'Food and Agriculture Systems': ['q79', 'q80', 'q81','q82'],
            'Water and Natural Systems': ['q88', 'q89', 'q90', 'q91', 'q92','q93'],
            'Human Settlements Systems': ['q101', 'q102', 'q103', 'q104', 'q105','q106'],
            'Coastal and Oceanic Systems': ['q114', 'q115', 'q116', 'q117','q118'],
            'Infrastructure Systems': ['q125', 'q126', 'q127', 'q128', 'q129','q130'],
            'Planning & Policy: Cross-cutting': ['q139', 'q140', 'q141', 'q142','q143'],
            'Finance: Cross-cutting': ['q150', 'q151', 'q152','q153']
        }

        final_df_gi_outcomes = pd.DataFrame(columns=['RtR Partner Name', 'SAA Impact Systems', 'Outcome Target', 'Explanation'])

        for task_force, outcomes in task_force_to_outcome.items():
            for outcome in outcomes:
                explanation = outcome_to_explanation[outcome]
                temp_df_gi = df_gi[['InitName', outcome, explanation]]
                temp_df_gi.columns = ['RtR Partner Name', 'Outcome Target', 'Explanation']
                temp_df_gi['SAA Impact Systems'] = task_force
                final_df_gi_outcomes = pd.concat([final_df_gi_outcomes, temp_df_gi])

        final_df_gi_outcomes = final_df_gi_outcomes.dropna(how='all')
        final_df_gi_outcomes = final_df_gi_outcomes[~pd.isna(final_df_gi_outcomes['Outcome Target'])]

        # Calculate occurrence of each RtR Partner Name
        partner_counts = final_df_gi_outcomes['RtR Partner Name'].value_counts()
        # Calculate the percentage for each RtR Partner Name
        total = len(final_df_gi_outcomes)
        partner_percentage = (partner_counts / total) * 100
        # Map the percentage back to the original dataframe
        final_df_gi_outcomes['%RtR Partner Name'] = final_df_gi_outcomes['RtR Partner Name'].map(partner_percentage)
            

        # Calculate occurrence of each SAA Taskforce
        taskforce_counts = final_df_gi_outcomes['SAA Impact Systems'].value_counts()
        # Calculate the percentage for each SAA Taskforce
        total = len(final_df_gi_outcomes)
        taskforce_percentage = (taskforce_counts / total) * 100
        # Map the percentage back to the original dataframe
        final_df_gi_outcomes['%SAA Taskforce'] = final_df_gi_outcomes['SAA Impact Systems'].map(taskforce_percentage)

        # Calculate occurrence of each Outcome Target per SAA Taskforce
        outcome_counts = final_df_gi_outcomes.groupby(['SAA Impact Systems', 'Outcome Target']).size().reset_index(name='counts')
        # Calculate total occurrences per SAA Taskforce
        total_counts = final_df_gi_outcomes.groupby(['SAA Impact Systems']).size().reset_index(name='total')
        # Merge the two dataframes to compute the percentage
        merged = outcome_counts.merge(total_counts, on='SAA Impact Systems')
        merged['%OutcomeTarget_by_taskforce'] = (merged['counts'] / merged['total']) * 100
        # Merge back with the original dataframe
        final_df_gi_outcomes = final_df_gi_outcomes.merge(merged[['SAA Impact Systems', 'Outcome Target', '%OutcomeTarget_by_taskforce']], on=['SAA Impact Systems', 'Outcome Target'], how='left')

        # Calculate occurrence of each SAA Taskforce
        taskforce_counts = final_df_gi_outcomes['Outcome Target'].value_counts()
        # Calculate the percentage for each SAA Taskforce
        total = len(final_df_gi_outcomes)
        taskforce_percentage = (taskforce_counts / total) * 100
        # Map the percentage back to the original dataframe
        final_df_gi_outcomes['%OutcomeTarget_all'] = final_df_gi_outcomes['Outcome Target'].map(taskforce_percentage)
        final_df_gi_outcomes = final_df_gi_outcomes[['RtR Partner Name','SAA Impact Systems','Outcome Target','Explanation']]
        
        recode_list = {
            'Food and Agriculture Systems': 'Food and Agriculture',
            'Water and Natural Systems': 'Water and Nature',
            'Human Settlements Systems': 'Human Settlements',
            'Coastal and Oceanic Systems': 'Coastal and Oceans',
            'Infrastructure Systems': 'Infrastructure',
            'Planning & Policy: Cross-cutting': 'Planning and Policy: Cross-cutting',
            'Finance: Cross-cutting': 'Finance: Cross-cutting',
        }
        final_df_gi_outcomes['SAA Impact Systems'] = final_df_gi_outcomes['SAA Impact Systems'].replace(recode_list)

        new_df_gi_filtered = new_df_gi_filtered[['Partner Name','SAA Impact Systems','Relationship','Explanation (optional)',]]
        
        return final_df_gi_outcomes, new_df_gi_filtered,saa_partners_toplot,fig_treemap    
    final_df_gi_outcomes, new_df_gi_filtered,saa_partners_toplot,fig_treemap = treemap_chart_how_saa(new_df_gi_filtered)


    def saa_summary():
        # #Displaying the number of Partners that has a confirmed relationship with SAA Taskforces
        number_partner_saa = summary_partner_saa['N° SAA Taskforces'].notna().sum()
        col1, col2, col3= st.columns(3)
        col1.metric('RtR Partners related to SAA Priority Systems', str(number_partner_saa))
        
        tab1, tab2, tab3 = st.tabs(["2023-2024 Comparison", "2024 Details", "SAA Priority Systems per Partner in 2024"])

        with tab1: 
            comparative_chart_2023_2024()

        with tab2:    
            st.markdown("Some RtR partners are directly related to the core of SAA priority systems. In some cases, partners have an indirect impact on other systems.")
            st.pyplot(fig_partners_saa_detail)
        
        with tab3: 
            st.markdown("There are RtR partners involved in all SAA Priority Systems, while many others are related to nearly all of them. This illustrates the broad scope of action of RtR partners.")
            st.pyplot(fig_n_priority_systems_saa)
        
    
    def saa_all_info_tables():
        st.markdown("##### Explore the types of relationships between RtR partners and SAA Priority Systems.")
        
        tab1, tab2 = st.tabs(["Relation to SAA Priority Systems", "SAA Outcome Targets"])
        with tab1: 
            st.markdown("##### RtR Partners & SAA Priority Systems")
            st.dataframe(new_df_gi_filtered)

        with tab2: 
            st.markdown("##### RtR Partners & SAA Outcome Targets")
            st.dataframe(final_df_gi_outcomes)
       

    def food_agriculture_summary():
        st.markdown("##### FOOD AND AGRICULTURE")
        st.markdown("*How do the Food and Agriculture Systems relate to the work of RtR Partners?*")
        foodandagriculture_saa = df_gi['q77'].count()
        foodandagriculture_saa_direct_related = len(df_gi[df_gi['q77'] == 'Directly related'])
        foodandagriculture_saa_indirect_related = len(df_gi[df_gi['q77'] == 'Indirectly related'])
        foodandagriculture_saa_not_related = len(df_gi[df_gi['q77'] == 'Not Related'])
        foodandagriculture_saa_unsure = len(df_gi[df_gi['q77'] == 'Unsure'])
        st.markdown("Number of Partners:")
        col1, col2, col3, col4,col5 = st.columns(5)
        col1.metric("Directly related",foodandagriculture_saa_direct_related)
        col2.metric("Indirectly related",foodandagriculture_saa_indirect_related)
        col3.metric("Not Related",foodandagriculture_saa_not_related)
        col4.metric("Unsure",foodandagriculture_saa_unsure)
        # st.markdown("**Q25. If applicable, could you provide further detail on the outcomes or activities RtR Partners has in relation to Food and Agriculture Systems? (OPTIONAL)**")
        foodandagriculture_saa_explanation = df_gi['q78'].count()
        col5.metric("Detailed Explanations",foodandagriculture_saa_explanation)

        saa_taskforce = 'Food and Agriculture'
        # with st.expander("Explore More in "+saa_taskforce ):
        grouped_data_all_filtered = grouped_data_all[grouped_data_all['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### Number of RtR Partners related to '+saa_taskforce)
        st.dataframe(grouped_data_all_filtered)
        
        new_df_gi_filtered_2 = new_df_gi_filtered[new_df_gi_filtered['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### RtR Partner relation to '+saa_taskforce)
        st.dataframe(new_df_gi_filtered_2)
        
        st.markdown('##### RtR Partner relation to '+saa_taskforce+ "' Outcomes Targets" )
        final_df_gi_outcome_target = final_df_gi_outcomes[final_df_gi_outcomes['SAA Impact Systems'] == saa_taskforce]
        st.dataframe(final_df_gi_outcome_target)
      
    def water_summary():
        st.markdown("##### WATER AND NATURE")
        st.markdown("*How do the Water and Nature Systems relate to the work of RtR Partners?*")
        water_natsyst_saa = df_gi['q86'].count()
        water_natsyst_saa_direct_related = len(df_gi[df_gi['q86'] == 'Directly related'])
        water_natsyst_saa_indirect_related = len(df_gi[df_gi['q86'] == 'Indirectly related'])
        water_natsyst_saa_not_related = len(df_gi[df_gi['q86'] == 'Not Related'])
        water_natsyst_saa_unsure = len(df_gi[df_gi['q86'] == 'Unsure'])
        st.markdown("Number of Partners:")
        col1, col2, col3, col4,col5 = st.columns(5)
        col1.metric("Directly related ",water_natsyst_saa_direct_related)
        col2.metric("Indirectly related",water_natsyst_saa_indirect_related)
        col3.metric("Not Related",water_natsyst_saa_not_related)
        col4.metric("Unsure",water_natsyst_saa_unsure)
        # st.markdown("**Q29 If applicable, could you provide further detail on the outcomes or activities RtR Partners has in relation to Water and Nature Systems? (OPTIONAL)**")
        water_natsyst_saa_explanation = df_gi['q87'].count()
        col5.metric("Detailed Explanations",water_natsyst_saa_explanation)


        saa_taskforce = 'Water and Nature'
        with st.expander("Explore More in "+saa_taskforce ):
            grouped_data_all_filtered = grouped_data_all[grouped_data_all['SAA Impact Systems'] == saa_taskforce]
            st.markdown('##### Number of RtR Partners related to '+saa_taskforce)
            st.dataframe(grouped_data_all_filtered)
            
            new_df_gi_filtered_2 = new_df_gi_filtered[new_df_gi_filtered['SAA Impact Systems'] == saa_taskforce]
            st.markdown('##### RtR Partner relation to '+saa_taskforce)
            st.dataframe(new_df_gi_filtered_2)
            
            st.markdown('##### RtR Partner relation to '+saa_taskforce+ "' Outcomes Targets" )
            final_df_gi_outcome_target = final_df_gi_outcomes[final_df_gi_outcomes['SAA Impact Systems'] == saa_taskforce]
            st.dataframe(final_df_gi_outcome_target)  
      
    def human_settlements_summary():
        st.markdown("##### HUMAN SETTLEMENTS")
        st.markdown("*How do the Human Settlement Systems relate to the work of RtR Partners?*")
        humansettlement_saa = df_gi['q99'].count()
        humansettlement_saa_direct_related = len(df_gi[df_gi['q99'] == 'Directly related'])
        humansettlement_saa_indirect_related = len(df_gi[df_gi['q99'] == 'Indirectly related'])
        humansettlement_saa_not_related = len(df_gi[df_gi['q99'] == 'Not Related'])
        humansettlement_saa_unsure = len(df_gi[df_gi['q99'] == 'Unsure'])
        st.markdown("Number of Partners:")
        col1, col2, col3, col4,col5 = st.columns(5)
        col1.metric("Directly related ",humansettlement_saa_direct_related)
        col2.metric("Indirectly related': ",humansettlement_saa_indirect_related)
        col3.metric("Not Related ",humansettlement_saa_not_related)
        col4.metric("Unsure",humansettlement_saa_unsure)
        # st.markdown("**If applicable, could you provide further detail on the outcomes or activities RtR Partners has in relation to Human Settlement Systems? (OPTIONAL)**")
        humansettlement_saa_explanation = df_gi['q100'].count()
        col5.metric("Detailed Explanations",humansettlement_saa_explanation)

        saa_taskforce = 'Human Settlements'

        # with st.expander("Explore More in "+saa_taskforce ):
        grouped_data_all_filtered = grouped_data_all[grouped_data_all['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### Number of RtR Partners related to '+saa_taskforce)
        st.dataframe(grouped_data_all_filtered)
        
        new_df_gi_filtered_2 = new_df_gi_filtered[new_df_gi_filtered['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### RtR Partner relation to '+saa_taskforce)
        st.dataframe(new_df_gi_filtered_2)
        
        st.markdown('##### RtR Partner relation to '+saa_taskforce+ "' Outcomes Targets" )
        final_df_gi_outcome_target = final_df_gi_outcomes[final_df_gi_outcomes['SAA Impact Systems'] == saa_taskforce]
        st.dataframe(final_df_gi_outcome_target)

    def coastal_oceans_summary():
        st.markdown("##### COASTAL AND OCEANS")
        st.markdown("*How do the Coastal and Oceanic Systems relate to the work of RtR Partners?*")
        coastal_oceanic_saa = df_gi['q112'].count()
        coastal_oceanic_saa_direct_related = len(df_gi[df_gi['q112'] == 'Directly related'])
        coastal_oceanic_saa_indirect_related = len(df_gi[df_gi['q112'] == 'Indirectly related'])
        coastal_oceanic_saa_not_related = len(df_gi[df_gi['q112'] == 'Not Related'])
        coastal_oceanic_saa_unsure = len(df_gi[df_gi['q112'] == 'Unsure'])
        st.markdown("Number of Partners:")
        col1, col2, col3, col4,col5 = st.columns(5)
        col1.metric("Directly related ",coastal_oceanic_saa_direct_related)
        col2.metric("Indirectly related': ",coastal_oceanic_saa_indirect_related)
        col3.metric("Not Related ",coastal_oceanic_saa_not_related)
        col4.metric("Unsure",coastal_oceanic_saa_unsure)
        # st.markdown("**If applicable, could you provide further detail on the outcomes or activities RtR Partners has in relation to Coastal and Oceanic Systems? (OPTIONAL)**")
        coastal_oceanic_saa_explanation = df_gi['q113'].count()
        col5.metric("Detailed Explanations",coastal_oceanic_saa_explanation)

        saa_taskforce = 'Coastal and Oceans'

        # with st.expander("Explore More in "+saa_taskforce ):
        grouped_data_all_filtered = grouped_data_all[grouped_data_all['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### Number of RtR Partners related to '+saa_taskforce)
        st.dataframe(grouped_data_all_filtered)
        
        new_df_gi_filtered_2 = new_df_gi_filtered[new_df_gi_filtered['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### RtR Partner relation to '+saa_taskforce)
        st.dataframe(new_df_gi_filtered_2)
        
        st.markdown('##### RtR Partner relation to '+saa_taskforce+ "' Outcomes Targets" )
        final_df_gi_outcome_target = final_df_gi_outcomes[final_df_gi_outcomes['SAA Impact Systems'] == saa_taskforce]
        st.dataframe(final_df_gi_outcome_target)

    def infrastructure_summary():
        st.markdown("##### INFRASTRUCTURE")
        st.markdown("*How do the Infrastructure Systems relate to the work of RtR Partners?*")
        infrastructure_saa = df_gi['q123'].count()
        infrastructure_saa_direct_related = len(df_gi[df_gi['q123'] == 'Directly related'])
        infrastructure_saa_indirect_related = len(df_gi[df_gi['q123'] == 'Indirectly related'])
        infrastructure_saa_not_related = len(df_gi[df_gi['q123'] == 'Not Related'])
        infrastructure_saa_unsure = len(df_gi[df_gi['q123'] == 'Unsure'])
        st.markdown("Number of Partners:")
        col1, col2, col3, col4,col5 = st.columns(5)
        col1.metric("Directly related ",infrastructure_saa_direct_related)
        col2.metric("Indirectly related': ",infrastructure_saa_indirect_related)
        col3.metric("Not Related ",infrastructure_saa_not_related)
        col4.metric("Unsure",infrastructure_saa_unsure)
        # st.markdown("**If applicable, could you provide further detail on the outcomes or activities RtR Partners has in relation to Infrastructure Systems? (OPTIONAL)**")
        infrastructure_saa_explanation = df_gi['q124'].count()
        col5.metric("Detailed Explanations",infrastructure_saa_explanation)


        saa_taskforce = 'Infrastructure'

        # with st.expander("Explore More in "+saa_taskforce ):
        grouped_data_all_filtered = grouped_data_all[grouped_data_all['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### Number of RtR Partners related to '+saa_taskforce)
        st.dataframe(grouped_data_all_filtered)
        
        new_df_gi_filtered_2 = new_df_gi_filtered[new_df_gi_filtered['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### RtR Partner relation to '+saa_taskforce)
        st.dataframe(new_df_gi_filtered_2)
        
        st.markdown('##### RtR Partner relation to '+saa_taskforce+ "' Outcomes Targets" )
        final_df_gi_outcome_target = final_df_gi_outcomes[final_df_gi_outcomes['SAA Impact Systems'] == saa_taskforce]
        st.dataframe(final_df_gi_outcome_target)
    
    def health_summary():
        st.markdown("##### HEALTH")
        st.markdown("**Does the work of RtR Partners include any health-related outcomes or activities**")
        # st.write(df_gi['q136'])
        health_saa = df_gi['q136'].count()
        health_saa_yes= len(df_gi[df_gi['q136'] == 'Directly related'])
        health_saa_no= len(df_gi[df_gi['q136'] == 'Not Related'])
        health_saa_not_sure = len(df_gi[df_gi['q136'] == 'Unsure'])
        st.markdown("Number of Partners:")
        col1, col2, col3, col4,col5 = st.columns(5)
        col1.metric('Related',health_saa_yes)
        col2.metric("No Related",health_saa_no)
        col3.metric("Not Sure",health_saa_not_sure)
        # st.markdown("**If applicable, could you provide further detail on the outcomes or activities RtR Partners has in relation to Health Systems? (OPTIONAL)**")
        health_saa_explanation = df_gi['q137'].count()
        col4.metric("Detailed Explanations",health_saa_explanation)

        saa_taskforce = 'Health'

        # with st.expander("Explore More in "+saa_taskforce):
        grouped_data_all_filtered = grouped_data_all[grouped_data_all['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### Number of RtR Partners related to '+saa_taskforce)
        st.dataframe(grouped_data_all_filtered)
        
        new_df_gi_filtered_2 = new_df_gi_filtered[new_df_gi_filtered['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### RtR Partner relation to '+saa_taskforce)
        st.dataframe(new_df_gi_filtered_2)
        st.write(saa_taskforce+ " Outcomes Targets are not yet available")
        
        final_df_gi_outcome_target = final_df_gi_outcomes[final_df_gi_outcomes['SAA Impact Systems'] == saa_taskforce]
        st.write(final_df_gi_outcome_target)
    
    def planning_policy_summary():
        st.markdown("##### PLANNING AND POLICY: CROSS-CUTTING")
        st.markdown("*How do the Cross-Cutting Enabler 'Planning' relate to the work of RtR Partners?*")
        planning_saa = df_gi['q138'].count()
        planning_saa_direct_related = len(df_gi[df_gi['q138'] == 'Directly related'])
        planning_saa_indirect_related = len(df_gi[df_gi['q138'] == 'Indirectly related'])
        planning_saa_not_related = len(df_gi[df_gi['q138'] == 'Not Related'])
        planning_saa_unsure = len(df_gi[df_gi['q138'] == 'Unsure'])
        st.markdown("Number of Partners:")
        col1, col2, col3, col4,col5 = st.columns(5)
        col1.metric("Directly related",planning_saa_direct_related)
        col2.metric("Indirectly related",planning_saa_indirect_related)
        col3.metric("Not Related",planning_saa_not_related)
        col4.metric("Unsure",planning_saa_unsure)
        # st.markdown("**If applicable, could you provide further detail on the outcomes or activities RtR Partners has in relation to Cross-Cutting Enabler 'Planning'? (OPTIONAL)**")
        planning_saa_explanation = df_gi['q139'].count()
        col5.metric("Detailed Explanations",planning_saa_explanation)

        #  'Planning & Policy: Cross-cutting'
        saa_taskforce = 'Planning and Policy: Cross-cutting'

        # with st.expander("Explore More in "+saa_taskforce ):
        grouped_data_all_filtered = grouped_data_all[grouped_data_all['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### Number of RtR Partners related to '+saa_taskforce)
        st.dataframe(grouped_data_all_filtered)
        
        new_df_gi_filtered_2 = new_df_gi_filtered[new_df_gi_filtered['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### RtR Partner relation to '+saa_taskforce)
        st.dataframe(new_df_gi_filtered_2)
        
        st.markdown('##### RtR Partner relation to '+saa_taskforce+ "' Outcomes Targets" )
        final_df_gi_outcome_target = final_df_gi_outcomes[final_df_gi_outcomes['SAA Impact Systems'] == saa_taskforce]
        st.dataframe(final_df_gi_outcome_target)
            
    def finance_summary():
        st.markdown("##### FINANCE: CROSS-CUTTING")
        st.markdown("*How do the Cross-Cutting Enabler 'Finance' relate to the work of RtR Partners?*")
        finance_saa = df_gi['q148'].count()
        finance_saa_direct_related = len(df_gi[df_gi['q148'] == 'Directly related'])
        finance_saa_indirect_related = len(df_gi[df_gi['q148'] == 'Indirectly related'])
        finance_saa_not_related = len(df_gi[df_gi['q148'] == 'Not Related'])
        finance_saa_unsure = len(df_gi[df_gi['q148'] == 'Unsure'])
        st.markdown("Number of Partners:")
        col1, col2, col3, col4,col5 = st.columns(5)
        col1.metric("Directly related",finance_saa_direct_related)
        col2.metric("Indirectly related",finance_saa_indirect_related)
        col3.metric("Not Related",finance_saa_not_related)
        col4.metric("Unsure",finance_saa_unsure)
        # st.markdown("**If applicable, could you provide further detail on the outcomes or activities RtR Partners has in relation to Cross-Cutting Enabler 'Finance'? (OPTIONAL)**")
        finance_saa_explanation = df_gi['q149'].count()
        col5.metric("Detailed Explanations",finance_saa_explanation)

        saa_taskforce = 'Finance: Cross-cutting'

        # with st.expander("Explore More in "+saa_taskforce ):
        grouped_data_all_filtered = grouped_data_all[grouped_data_all['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### Number of RtR Partners related to '+saa_taskforce)
        st.dataframe(grouped_data_all_filtered)
        
        new_df_gi_filtered_2 = new_df_gi_filtered[new_df_gi_filtered['SAA Impact Systems'] == saa_taskforce]
        st.markdown('##### RtR Partner relation to '+saa_taskforce)
        st.dataframe(new_df_gi_filtered_2)
        
        st.markdown('##### RtR Partner relation to '+saa_taskforce+ "' Outcomes Targets" )
        final_df_gi_outcome_target = final_df_gi_outcomes[final_df_gi_outcomes['SAA Impact Systems'] == saa_taskforce]
        st.dataframe(final_df_gi_outcome_target)

    
    saa_priority_systems_option_list = [
        'All SAA Priority Systems',
        'Food and Agriculture', 
        'Water and Nature', 
        'Human Settlements', 
        'Coastal and Oceans', 
        'Infrastructure', 
        'Health', 
        'Planning and Policy: Cross-cutting', 
        'Finance: Cross-cutting'
    ]

    ## DISPLAY
    saa_summary()

    # Create a selection box
    selected_option = st.selectbox("#### Select an SAA Priority System", saa_priority_systems_option_list)

    # Display the corresponding function based on selection
    if selected_option == 'Food and Agriculture':
        food_agriculture_summary()
    elif selected_option == 'Water and Nature':
        water_summary()
    elif selected_option == 'Human Settlements':
        human_settlements_summary()
    elif selected_option == 'Coastal and Oceans':
        coastal_oceans_summary()
    elif selected_option == 'Infrastructure':
        infrastructure_summary()
    elif selected_option == 'Health':
        health_summary()
    elif selected_option == 'Planning and Policy: Cross-cutting':
        planning_policy_summary()
    elif selected_option == 'Finance: Cross-cutting':
        finance_summary()
    elif selected_option == 'All SAA Priority Systems':
        saa_all_info_tables()

