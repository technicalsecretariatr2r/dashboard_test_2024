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


def saa_partner_finder(df_gi,n_reporting_partners,p_short_name):
    # # ______________________________________________
    # # ______________________________________________
    # # BLOCK SAA_______________________________
    # # ______________________________________________
    # # ______________________________________________
    ##_____________________________________________________________________________________________________________
    
    if p_short_name == "No Info":
        pass
    else:
        st.markdown(f"#### THE SHARM-EL-SHEIKH ADAPTATION AGENDA (SAA) PRIORITY SYSTEMS")
        st.markdown(f"Comprehensive Partners Alignment of {p_short_name} with the Sharm-el-Sheikh Adaptation Agenda (SAA) Priority Systems")
        
    try:
        # Data set to plot making: 
        impact_systems = {
        'Finance: Cross-cutting': 'q147',
        'Planning and Policy: Cross-cutting': 'q137',
        'Water and Nature': 'q85',
        'Infrastructure': 'q122',
        'Coastal and Oceans': 'q111',
        'Human Settlements': 'q98',
        'Health': 'q135',
        'Food and Agriculture': 'q76'
        }

        saa_to_explanation = {
            'q76': 'q77', 
            'q85': 'q86',
            'q98': 'q99',
            'q111':'q112',
            'q122':'q123',
            'q135':'q136',
            'q137':'q138',
            'q147':'q148'
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
        

        #Displaying the number of Partners that has a confirmed relationship with SAA Taskforces
        number_partner_saa = summary_partner_saa['N° SAA Taskforces'].notna().sum()
        # col1, col2, col3= st.columns(3)
        # col1.metric('RtR Partners related to SAA Priority Systems', str(number_partner_saa))




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



        # st.markdown("#### Relationship Types of RtR Partners with SAA Impact Systems")  # SHOWN IN 2023 REPORT
        # Chart % OFICIAL
        # Making DataSet with all SAA Taskforces Details for Chart
        new_df_gi_filtered = new_df_gi[new_df_gi['relation_yes'] == 'Yes']
        grouped_data_all = new_df_gi.groupby(['SAA Impact Systems', 'Relationship'], sort=False).size().unstack().reset_index()
        grouped_data_details = new_df_gi_filtered.groupby(['SAA Impact Systems', 'Relationship'], sort=False).size().unstack()

        # st.write(grouped_data_details)

        # Set the color palette
        sns.set_palette("RdPu")

        # Define the custom color palette
        color_palette = {'Directly related': '#FF37D5', 'Indirectly related': '#112E4D'}

        # Create the plot
        fig_details, ax = plt.subplots(figsize=(6, len(grouped_data_details) / 2))

        # Create the horizontal bar chart with custom colors
        grouped_data_details.plot(kind='barh', stacked=True, ax=ax, color=color_palette)

        # Set the plot title and axis labels
        ax.set_xlabel(p_short_name)
        ax.set_ylabel('SAA Priority Systems')

        # Set x-axis limits and ticks
        ax.set_xlim([0, 1])
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))

        # Adjust legend and spines
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.set_title(f'{p_short_name} related to each SAA Priority Systems', fontsize=12)


        # Show the plot in Streamlit
        # st.pyplot(fig_n_priority_systems_saa) # This line is for displaying the plot in Streamlit





        #Chart about how
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
                                path=[px.Constant(f"{p_short_name} & SAA Priority Systems"), 
                                    'SAA Impact Systems', 'Relationship', 'Partner Name', 'Explanation (formatted)'], 
                                values='% Partner', 
                                # color='%SAA Taskforce', 
                                color_continuous_scale='RdPu',
                                custom_data=['Explanation (formatted)'])

        fig_treemap.update_traces(
            # root_color="#FF37D5", 
                                marker_line_color='grey', 
                                hovertemplate='%{customdata[0]}<extra></extra>'
                                )

        fig_treemap.data[0].hovertemplate = '%{value:.1f}%'

        fig_treemap.update_layout(
            showlegend=False,
            title_text=f" {p_short_name}'s relation to each SAA Priority System",
            margin=dict(t=50, l=25, r=25, b=25),
            width=1000)

        # st.plotly_chart(fig_treemap)
        
        st.pyplot(fig_details)
        # with st.expander("Explore Data: RtR Partner's Relationship with SAA Priority Systems"):
        #     st.markdown("##### RtR Partner's Relationship with SAA Priority Systems")
        #     st.write(grouped_data_all)
        # st.pyplot(fig_n_priority_systems_saa)## <--- This one is oficial
        st.plotly_chart(fig_treemap)
        
        ### ok 
        
        
        outcome_to_explanation = {
            #Food and Agriculture Systems
            'q78':'q78',
            'q79': 'q82', 
            'q80': 'q83', 
            'q81': 'q84',
            #Water and Natural Systems
            'q87':'q87',
            'q88': 'q93',
            'q89': 'q94',
            'q90': 'q95',
            'q91': 'q96',
            'q92': 'q97',
            #Human Settlements
            'q100': 'q100',
            'q101': 'q106',
            'q102': 'q107',
            'q103': 'q108',
            'q104': 'q109',
            'q105': 'q110',
            #Coastal and Oceanic Systems 
            'q113': 	'q113',
            'q114': 	'q118',
            'q115': 	'q119',
            'q116': 	'q120',
            'q117': 	'q121',
            #Infrastructure Systems
            'q124': 	'q124',
            'q125': 	'q130',
            'q126': 	'q131',
            'q127': 	'q132',
            'q128': 	'q133',
            'q129': 	'q134', 
            #Cross-Cutting Enabler 'Planning'
            'q138': 	'q138',
            'q139': 	'q143',
            'q140': 	'q144',
            'q141': 	'q145',
            'q142': 	'q146',
            #Cross-Cutting Enabler 'Finance'
            'q149': 	'q149',
            'q150': 	'q153',
            'q151': 	'q154',
            'q152': 	'q155',
        }

        task_force_to_outcome = {
            'Food and Agriculture Systems': ['q78','q79', 'q80', 'q81'],
            'Water and Natural Systems': ['q87','q88', 'q89', 'q90', 'q91', 'q92'],
            'Human Settlements Systems': ['q100','q101', 'q102', 'q103', 'q104', 'q105'],
            'Coastal and Oceanic Systems': ['q113','q114', 'q115', 'q116', 'q117'],
            'Infrastructure Systems': ['q124','q125', 'q126', 'q127', 'q128', 'q129'],
            'Planning & Policy: Cross-cutting': ['q138','q139', 'q140', 'q141', 'q142'],
            'Finance: Cross-cutting': ['q149','q150', 'q151', 'q152']
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

        # st.write(final_df_gi_outcomes)

        # Define custom color mapping for each SAA Impact System
        custom_colors = {
            'Food and Agriculture': '#FFA07A',  # Light Salmon
            'Water and Nature': '#20B2AA',      # Light Sea Green
            'Human Settlements': '#778899',     # Light Slate Gray
            'Coastal and Oceans': '#1E90FF',    # Dodger Blue
            'Infrastructure': '#3CB371',        # Medium Sea Green
            'Planning and Policy: Cross-cutting': '#BA55D3',  # Medium Orchid
            'Finance: Cross-cutting': '#FFD700', # Gold
        }

        #MAKING THE TREE MAP
        final_df_gi_to_treemap = final_df_gi_outcomes[['SAA Impact Systems', 'Outcome Target','%SAA Taskforce', '%OutcomeTarget_all']]
        final_df_gi_to_treemap = final_df_gi_to_treemap.drop_duplicates()
        # Apply the custom color mapping to create a new column for colors
        # final_df_gi_to_treemap['CustomColor'] = final_df_gi_to_treemap['SAA Impact Systems'].map(custom_colors)

        note = "NOTE: (1) Health Systems aren't in the SAA percentages due to no outcome targets. (2) RtR Partners' multiple Task Force ties can shift the percentages."

        fig_treemap = px.treemap(final_df_gi_to_treemap, 
                                path=[px.Constant(f"{p_short_name} Relation to SAA Priority Systems' Outcome Targets"), 'SAA Impact Systems', 'Outcome Target',], 
                                # values='%OutcomeTarget_all', 
                                # color='CustomColor', 
                                # color_continuous_scale='RdPu'
                                )

        # fig_treemap.update_traces(root_color="#FF37D5")
        fig_treemap.update_layout(showlegend=False,
                                title_text=f"{p_short_name} & SAA Priority Systems' Outcome Targets",
                                margin=dict(t=50, l=25, r=25, b=25),
                                width=1000)
        fig_treemap.add_annotation(x=1, y=0,
                    text=note,showarrow=False,
                    yshift=-20)

        # It looks like you want to show the values as percentages with one decimal place.
        fig_treemap.data[0].hovertemplate = '%{value:.1f}%'
        fig_treemap.update_traces(marker_line_color='grey')
        st.plotly_chart(fig_treemap)


        final_df_gi_outcomes = final_df_gi_outcomes[['RtR Partner Name','SAA Impact Systems','Outcome Target','Explanation']]
        
        new_df_gi_filtered = new_df_gi_filtered[['Partner Name','SAA Impact Systems','Relationship','Explanation (optional)',]]
        
        with st.expander("Explore Data: Partner's Explanations of the relationship with SAA Priority Systems & Outcome Targets"):
            st.markdown("##### RtR Partner's Explanations of the relationship with SAA Priority Systems")
            st.dataframe(new_df_gi_filtered)
            st.markdown("##### RtR Partner relation to SAA Priority Systems' Outcomes Targets")
            st.dataframe(final_df_gi_outcomes)
    except Exception as e:
        st.markdown("#### SHARM-EL-SHEIKH ADAPTATION AGENDA (SAA) PRIORITY SYSTEMS")
        st.markdown("No Information Available Yet")
        pass

