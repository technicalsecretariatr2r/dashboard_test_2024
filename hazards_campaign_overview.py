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


def hazards_campaign_overview(df_hazards_pledge_plan_vertical,n_reporting_partners):
    # def hazard_plegde():
    #     st.write()
    #     #__________________________________________________________________________________________________________________________________________________________________
    #     #__________________________________________________________________________________________________________________________________________________________________
    #     #__________________________________________________________________________________________________________________________________________________________________
    #     #__________________________________________________________________________________________________________________________________________________________________
    #     #__________________________________________________________________________________________________________________________________________________________________
    #     #__________________________________________________________________________________________________________________________________________________________________
    #     #  BLOCK HAZARDS PLEDGE
    #     #__________________________________________________________________________________________________________________________________________________________________
    #     #__________________________________________________________________________________________________________________________________________________________________
    #     #__________________________________________________________________________________________________________________________________________________________________
    #     #__________________________________________________________________________________________________________________________________________________________________
    #     #__________________________________________________________________________________________________________________________________________________________________

    #     # st.write("### CLIMATE HAZARDS AWARENESS")
    #     # st.write("A detailed section on the various climate hazards RTR Partners are addressing through their climate actions.")

    #     # # st.subheader("Hazards where RtR Partners aim to provide resilience")

    #     # # st.write("#### Hazards where RtR Partners aim to provide resilience (Pledge)")
    #     # #Sample size hazards from selection.

    #     # # st.write(df_pledge['All_Hazards_pdg'])
    #     # df2_sz_hazards_pledge = df_pledge['All_Hazards_pdg'].replace(['; ; ; ; '], np.nan).dropna()
    #     # sz_hazards_pledge = str(df2_sz_hazards_pledge.count())

    #     # #dataframe to workwith (All data from the selection).
    #     # df2 = df_pledge['All_Hazards_pdg'].str.split(";", expand=True).apply(lambda x: x.str.strip())
    #     # df2 = df2.stack().value_counts()
    #     # df2 = df2.iloc[1:].sort_index().reset_index(name='Frecuency')  #Check what happend whit blank information.

    #     # #creating new columms based in a dictionary
    #     # flooding_list = {'Coastal flood':'Flooding','Urban flood':'Flooding', 'River flood':'Flooding'}
    #     # drought_list = {'Drought (agriculture focus)':'Drought','Drought (other sectors)':'Drought'}
    #     # water_list   = {'Water stress (rural focus)':'Water','Water stress (urban focus)':'Water'}
    #     # fire_list = {'Wildfire':'Fire'}
    #     # coastal_list = {'Oceanic Events':'Coastal / Ocean','Other coastal events':'Coastal / Ocean'}
    #     # cold_list = {'Extreme cold':'Cold',"Snow, Ice":'Cold'}
    #     # wind_list = {'Extreme wind':'Wind','Tropical Cyclone':'Wind'}
    #     # heat_list = {'Extreme heat':'Heat',}
    #     # hazard_dictionary = {**heat_list,**cold_list,**drought_list,**water_list,**fire_list,**flooding_list,**coastal_list,**wind_list}
    #     # df2['group'] = df2['index'].map(hazard_dictionary)
    #     # df2['% hazard']=((df2['Frecuency']/df2['Frecuency'].sum())*100)

    #     # # sum of % country in 'mayor_area' and creating a new df
    #     # df3 = df2.groupby(['group']).agg({'Frecuency': 'sum'})
    #     # df3 = df3.reset_index()
    #     # df3.rename(columns={'Frecuency': 'Sum_frec_group'}, inplace=True)
    #     # df3['% Hazards']=((df3['Sum_frec_group']/df3['Sum_frec_group'].sum())*100)
    #     # # st.write(df3)

    #     # df2 = pd.merge(df2, df3, on='group', how='left')
    #     # df2 = df2.dropna()


    #     # # Chart Hazard Nivel Profundo

    #     # # This line creates the treemap and sets the color. Replace your previous treemap code with this
    #     # fig_hazard_pledge = px.treemap(
    #     #     df2, 
    #     #     path=[px.Constant("Hazards"), 'group', 'index'], 
    #     #     values='Frecuency',  # or 'Sum_frec_group' if you want the grouped sums instead
    #     #     color='% Hazards',
    #     #     color_continuous_scale='RdPu',
    #     #     # This is where we define what text to display in the boxes of the treemap
    #     #     custom_data=['% hazard', '% Hazards']
    #     # )

    #     # # This part sets what text to show on hover
    #     # fig_hazard_pledge.update_traces(
    #     #     hovertemplate="<b>%{label}</b><br>%{customdata[0]:.2f}% (Group)<br>%{customdata[1]:.2f}% (Total)",
    #     #     texttemplate="<b>%{label}</b><br>%{customdata[0]:.2f}%"
    #     # )

    #     # # These are your layout updates
    #     # fig_hazard_pledge.update_layout(
    #     #     title='Climate Hazards Targeted by RtR Initiatives (Pledge Statements)',
    #     #     font=dict(size=16),
    #     #     margin=dict(t=50, l=25, r=25, b=25)
    #     # )
    #     # fig_hazard_pledge.add_annotation(
    #     #     x=1, y=0,
    #     #     text='Out of ' + str(sz) + ' RtR Initiatives - All Pledges. Pledge Statement Survey 2023',
    #     #     showarrow=False,
    #     #     yshift=-20
    #     # )
    #     # fig_hazard_pledge.update_traces(marker_line_color='grey')

    #     # fig_hazard_pledge.update_traces(root_color='#FF37D5')
    #     # fig_hazard_pledge.update_layout(title='Climate Hazards Targeted by RtR Partners (Pledge Statements)', font=dict(size=16))
    #     # fig_hazard_pledge.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    #     # # fig_hazard_pledge.add_annotation(x=1, y=0,
    #     # #                 text = 'Out of ' + str(sz) + ' RtR Initiatives - All Pledges. Pledge Statement Survey 2023',
    #     # #                 showarrow=False,
    #     # #                 yshift=-20)
    #     # fig_hazard_pledge.data[0].hovertemplate = '%{value:.1f}%'
    #     # fig_hazard_pledge.update_traces(marker_line_color='grey')

    #     # fig_hazard_pledge.update_traces(
    #     #     hovertemplate='%{label}<br>%{parent}<br>%{value:.1f}%',
    #     #     marker_line_color='grey',
    #     #     textinfo='label+text+value'
    #     # )
    #     # # st.plotly_chart(fig_hazard_pledge)


    #     # # CHART HAZARD RECODED
    #     # # Adjust the treemap code to show only two levels
    #     # fig_hazard_pledge_recoded = px.treemap(
    #     #     df2, 
    #     #     path=[px.Constant("Hazards"), 'group'], 
    #     #     values='Sum_frec_group',  # Use the aggregated sum for each group
    #     #     color='% Hazards',  # Assuming this is the correct column for group-level percentages
    #     #     color_continuous_scale='RdPu',
    #     #     # Update what text to display in the boxes of the treemap
    #     #     custom_data=['% Hazards']  # Only one percentage level is now needed
    #     # )

    #     # # Update the hovertemplate to reflect only one custom data value
    #     # fig_hazard_pledge_recoded.update_traces(
    #     #     hovertemplate="<b>%{label}</b><br>%{customdata[0]:.2f}% (Group)",
    #     #     texttemplate="<b>%{label}</b><br>%{customdata[0]:.2f}%",
    #     #     textfont_size=16
    #     # )

    #     # # Apply your layout updates
    #     # fig_hazard_pledge_recoded.update_layout(
    #     #     title='Groups of Climate Hazards Targeted by RtR Partners (Pledge Statements)',
    #     #     font=dict(size=16),
    #     #     margin=dict(t=50, l=25, r=25, b=25)
    #     # )

    #     # # fig_hazard_pledge_recoded.add_annotation(x=1, y=0,
    #     # #                 text = 'Out of ' + str(sz) + ' RtR Initiatives - All Pledges. Pledge Statement Survey 2023',
    #     # #                 showarrow=False,
    #     # #                 yshift=-20)
    #     # fig_hazard_pledge_recoded.data[0].hovertemplate = '%{value:.1f}%'
    #     # fig_hazard_pledge_recoded.update_traces(marker_line_color='grey')


    #     # # Display the figure

    #     # tab1, tab2 = st.tabs(["General Categories", "Specific Categories"])

    #     # with tab1:
    #     #     st.plotly_chart(fig_hazard_pledge_recoded)
    #     # with tab2:
    #     #     st.plotly_chart(fig_hazard_pledge)
            
            


    #     # # Note for hazards
    #     # # ____________________

    #     # # ___________________
    #     # # gettin the highst 3 hazards and lowest 2
    #     # # ________________

    #     # s_df2 = df3.sort_values(by='% Hazards', ascending=False)
    #     # s_df2_best3 = s_df2.head(3)
    #     # list_best3 = s_df2_best3['group'].unique()
    #     # list_best3 =  ', '.join(list_best3)
    #     # #making a function to change the last comma with "&"
    #     # def replace_last(string, delimiter, replacement):
    #     #     start, _, end = string.rpartition(delimiter)
    #     #     return start + replacement + end
    #     # #getting a string with the first three hazards
    #     # list_best3_hazards = replace_last(list_best3, ',', ' & ')

    #     # # _________________________
    #     # # #making a list of the two less presnce in hazards
    #     # s_df2 = df3.sort_values(by='% Hazards', ascending=True)
    #     # s_df2_best3 = s_df2.head(2)
    #     # list_best3 = s_df2_best3['group'].unique()
    #     # list_best3 =  ', '.join(list_best3)
    #     # #making a function to change the last comma with "&"
    #     # def replace_last(string, delimiter, replacement):
    #     #     start, _, end = string.rpartition(delimiter)
    #     #     return start + replacement + end
    #     # #getting a string with the hazards
    #     # list_less_2_hazards = replace_last(list_best3, ',', ' & ')


    #     # # st.plotly_chart(fig_hazard_pledge)
    #     # with st.expander("Navigating this treemap: A User's Guide"):
    #     #         st.write("""
    #     #         This chart displays the percentage of hazard mitigation efforts that RtR Partners have pledged to provide*. The chart is structured as a treemap, with the main category of "Hazards" displayed at the top. Underneath that, you can see the different groups of climate hazards, such as heat, flooding, drought, fire, and cold. Finally, each individual hazard is displayed, such as extreme heat or flooding caused by heavy rainfall.
    #     # 	The size of each box in the treemap represents the percentage of hazard mitigation efforts pledged for that particular hazard. The color of the boxes represents the percentage of total hazard mitigation efforts pledged by RtR Partners within that hazard group. The darker the color, the higher the percentage of total mitigation efforts pledged for that group.

    #     # To view more information about each box, simply hover your mouse over it. The tooltip will display the name of the hazard and the percentage of hazard mitigation efforts pledged for that particular hazard. The total number of RtR Partners reporting information related to hazards is displayed in the annotation at the bottom of the chart.

    #     # *Considering all RtR Partner’s pledges, the 100% is the result of the sum of the frequencies of each specific hazard divided by the total number of hazards.

    #     # 	""")
    #     # st.markdown(list_best3_hazards+" are the hazard groups where RtR Partners aim to provide resilience the most. Partners' pledges show less focus on resilience for "+ list_less_2_hazards+ ".")


    #     # #__________________________________________________________________________________________________________________________________________________________________
    #     # #__________________________________________________________________________________________________________________________________________________________________
    #     # #__________________________________________________________________________________________________________________________________________________________________
    #     # #__________________________________________________________________________________________________________________________________________________________________
    #     # #__________________________________________________________________________________________________________________________________________________________________
    #     # #__________________________________________________________________________________________________________________________________________________________________
    #     # # # END BLOCK HAZARDS PLEDGE
    #     # #__________________________________________________________________________________________________________________________________________________________________
    #     # #__________________________________________________________________________________________________________________________________________________________________
    #     # #__________________________________________________________________________________________________________________________________________________________________
    #     # #__________________________________________________________________________________________________________________________________________________________________
    #     # #__________________________________________________________________________________________________________________________________________________________________

    def presentation_hazards():
        st.markdown("### CLIMATE HAZARDS AWARENESS")
        st.caption("A detailed section on the various climate hazards RTR Partners are addressing through their climate actions.")
        st.markdown("Hazards are the potential occurrence of a natural or human-induced physical event or trend that may cause loss of life, injury, or other health impacts, as well as damage and loss to property, infrastructure, livelihoods, service provision, ecosystems, and environmental resources. Hazards events are exacerbated by climate change and may cause adverse consequences for society and ecosystems. ")


        hazards_dict = {
            "Water stress (urban focus)": "A country is water stressed if the available freshwater supply relative to water withdrawals acts as an important constraint on development, with a focus on urban matters or areas.",
            "Water stress (rural focus)": "A country is water stressed if the available freshwater supply relative to water withdrawals acts as an important constraint on development, with a focus on rural matters or areas.",
            "Extreme heat": "The occurrence of a value of a weather or climate variable above a threshold value near the upper ends of the range of observed values of the variable.",
            "Extreme cold": "The occurrence of a value of a weather or climate variable below a threshold value near the lower ends of the range of observed values of the variable.",
            "Drought (agriculture focus)": "A period of abnormally dry weather long enough to cause a serious hydrological imbalance. With a focus on agriculture impacts.",
            "Drought (other sectors)": "A period of abnormally dry weather long enough to cause a serious hydrological imbalance.",
            "Urban flood": "The overflowing of the normal confines of a stream or other body of water, or the accumulation of water over urban areas that are not normally submerged.",
            "River flood": "Also known as fluvial, it refers to the overflowing of the normal confines of a stream or other body of water, or the accumulation of water over areas that are not normally submerged.",
            "Coastal flood": "Higher-than-normal water levels along the coast caused by tidal changes or thunderstorms that result in flooding, which can last from days to weeks.",
            "Tropical Cyclone": "A tropical cyclone originates over tropical or subtropical waters. It is characterized by a warm-core, non-frontal synoptic-scale cyclone with a low-pressure center, spiral rain bands, and strong winds. Depending on their location, tropical cyclones are referred to as hurricanes (Atlantic, Northeast Pacific), typhoons (Northwest Pacific), or cyclones (South Pacific and Indian Ocean).",
            "Snow, Ice": "Precipitation in the form of ice crystals/snowflakes or ice pellets (sleet) formed directly from freezing water vapor in the air. Ice accumulates when rain hits the cold surface and freezes.",
            "Wildfire": "Any uncontrolled and non-prescribed combustion or burning of plants in a natural setting such as a forest, grassland, brushland, or tundra, which consumes the natural fuels and spreads based on environmental conditions. Wildfires can be triggered by lightning or human actions.",
            "Extreme wind": "Occurrence of strong winds than average, strongest near-surface wind speeds that are generally associated with extreme storms, such as TCs, ETCs, and severe convective storms.",
            "Other coastal events": "Other climate hazards that give rise to dangerous events in coastal areas.",
            "Other (specify)": "Other hazards not listed in this guide."
        }

        # Convert dictionary to markdown format
        markdown_text = "### Climate Hazards\n"
        for hazard, description in hazards_dict.items():
                markdown_text += f"- **{hazard}:** {description}\n"

        # Display the markdown in Streamlit
        # with st.expander("Explore the definitions of each climate hazards here"):
        #         st.markdown(markdown_text)

    # def hazard_detailed_plan(df_hazards_pledge_plan_vertical,):
    
    #     df_filtered = df_hazards_pledge_plan_vertical[df_hazards_pledge_plan_vertical['source'] == 'Plans']
        
    #     # st.write('df_hazards_pledge_plan_vertical Post',df_filtered)    
        
    #     # Drop duplicates to ensure each InitName is counted only once per hazard
    #     df_unique = df_filtered.drop_duplicates(subset=['InitName', 'hazard'])

    #     # Count of 'InitName' by 'hazard'
    #     hazard_counts = df_unique['hazard'].value_counts()

    #     # Calculate percentage based on the total number of 'InitName' (assuming 34 is the total)
    #     hazard_percentages = (hazard_counts / n_reporting_partners) * 100

    #     # Sort data from highest to lowest
    #     sorted_hazard_percentages = hazard_percentages.sort_values(ascending=True)

    #     # Define the number of colors and color range for the bar chart
    #     n_colors = len(sorted_hazard_percentages)  # Adjusted to match number of hazards
    #     start = 0.2  # Start from a higher value than 0 to avoid the lightest colors
    #     end = 1
    #     colors = cm.RdPu(np.linspace(start, end, n_colors))

    #     # Create a horizontal bar chart and assign it to plt_all_hazards_pledge_plan
    #     plt_all_hazards_pledge_plan = plt.figure(figsize=(10, 3))
    #     ax = sorted_hazard_percentages.plot(kind='barh', color=colors)

    #     plt.xlabel('Percentage of Partners (%)')
    #     plt.ylabel('Hazards')
    #     plt.title('Percentage of Partners by Hazard (Plan)')
    #     plt.xlim(0, 100)  # Set x-axis limits to show percentages up to 100%

    #     # Adding text labels to the bars
    #     for index, value in enumerate(sorted_hazard_percentages):
    #         label = f"{value:.1f}% ({hazard_counts.reindex(sorted_hazard_percentages.index).iloc[index]} partner/s)"
    #         plt.text(value, index, label, va='center')

    #     ax.spines['right'].set_visible(False)
    #     ax.spines['top'].set_visible(False)
        
    #     df_filtered_hazard = df_filtered

    #     # Display the plot in Streamlit
    #     # st.pyplot(plt_all_hazards_pledge_plan)
        
    #     return df_filtered_hazard, plt_all_hazards_pledge_plan
        
    # df_filtered_hazard, plt_all_hazards_pledge_plan = hazard_detailed_plan(df_hazards_pledge_plan_vertical)
    # st.write(df_filtered_hazard)
    # st.pyplot(plt_all_hazards_pledge_plan)

    def hazard_grouped_plan(df_hazards_pledge_plan_vertical,n_reporting_partners):
        # Filter for 'Plans' only
        df_filtered = df_hazards_pledge_plan_vertical[df_hazards_pledge_plan_vertical['source'] == 'Plans']
        df_filtered = df_filtered[df_filtered['hazard_group'] != 'Not a climate hazard']

        # Drop duplicates to ensure each InitName is counted only once per hazard_group
        df_unique = df_filtered.drop_duplicates(subset=['InitName', 'hazard_group'])
        
        # Count of 'InitName' by 'hazard_group'
        hazard_group_counts = df_unique['hazard_group'].value_counts()

        # Calculate percentage based on the total number of 'InitName'
        # Update the total number of partners if the previous value is outdated
        n_reporting_partners = n_reporting_partners  
        hazard_group_percentages = (hazard_group_counts / n_reporting_partners) * 100

        # Sort data from highest to lowest
        sorted_percentages = hazard_group_percentages.sort_values(ascending=True)
        sorted_counts = hazard_group_counts.reindex(sorted_percentages.index)  # Reindex to match the sorted percentages

        # Define the number of colors and color range for the bar chart
        n_colors = len(sorted_percentages)
        start = 0.2  # Start from a higher value than 0 to avoid the lightest colors
        end = 1
        colors = cm.RdPu(np.linspace(start, end, n_colors))

        # Create a horizontal bar chart
        plt_hazards_group_pledge_plan = plt.figure(figsize=(10, 2))
        ax = sorted_percentages.plot(kind='barh', color=colors, width=0.9) 

        plt.xlabel('Percentage of Partners (%)')
        plt.ylabel('Climate Hazards')
        plt.title('Percentage of Partners by Type of Climate Hazard (Plan)')
        plt.xlim(0, 100)  # Set x-axis limits to show percentages up to 100%

        # Adding text labels to the bars
        for index, value in enumerate(sorted_percentages):
            label = f"{value:.1f}%"
            plt.text(value, index, label, va='center')
            # label = f"{value:.1f}% ({sorted_counts.iloc[index]} partner/s)"
            # plt.text(value, index, label, va='center')

        # Remove right and top spines
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        # Add a text box below the chart
        plt.figtext(0.99, 0.01, f'N = {n_reporting_partners}',
                    horizontalalignment='right', fontsize=10, weight='normal')

        return df_filtered, plt_hazards_group_pledge_plan
    
    df_filtered, plt_hazards_group_pledge_plan = hazard_grouped_plan(df_hazards_pledge_plan_vertical,n_reporting_partners)
    
    # Display the plot in Streamlit
    presentation_hazards()
    col1, col2, col3 = st.columns([0.5,2,0.5])
    with col2: 
        st.pyplot(plt_hazards_group_pledge_plan)
        st.dataframe(df_filtered,hide_index=True)





