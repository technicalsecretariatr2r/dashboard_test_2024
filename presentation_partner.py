import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
from streamlit_folium import st_folium
import folium
from PIL import Image
from numerize.numerize import numerize


def presentation_parter(df_partner_campaign,df_gi_select):
    #PRESENTATION LEVEL
    # Function to safely get the first value from a DataFrame column
    def get_first_value(df, column):
        try:
            # Check if the value is not NaN and not empty
            if pd.notna(df[column].values[0]) and df[column].values[0] != '':
                return df[column].values[0]
            else:
                return "No information Available Yet"
        except (IndexError, KeyError):
            # IndexError if the DataFrame is empty, KeyError if the column doesn't exist
            return "No information Available Yet"

    try:
        p_short_name = df_partner_campaign['short_name'].iloc[0]
        p_full_name = df_partner_campaign['name_only'].iloc[0]

        # try:
        #     logo = df_partner_campaign['logo'].iloc[0]
        #     image = Image.open(logo+'.png')
        #     col1, col2 = st.columns([0.3,1.7])
        #     col1.image(image, width=100)
        #     col2.header((p_full_name + " - " + p_short_name).upper())

        # except Exception as e:
        #     st.header((p_full_name + " - " + p_short_name).upper())

        # Get values safely
        # p_short_name = get_first_value(df_gi_select, 'short_name')
        # p_full_name = get_first_value(df_gi_select, 'name_only')
        p_description = get_first_value(df_gi_select, 'q21')
        p_office_city = get_first_value(df_gi_select, 'q26')
        p_office_country = get_first_value(df_gi_select, 'q29')
        p_web = get_first_value(df_gi_select, 'q32')

        # Display the information if available
        if "No information Available Yet" not in [p_short_name, p_full_name, p_description]:
            st.markdown("**Presentation:**")
            st.markdown(p_description)
        else:
            st.markdown("**Presentation:** No available yet")

        # Display the information if available
        if "No information Available Yet" not in [p_office_city, p_office_country]:
            st.markdown("**Location of the headquarters:** " + p_office_city + ", " + p_office_country)
        else:
            st.markdown("**Location of the headquarters:** No available yet")

        # Display the information if available
        if "No information Available Yet" not in [p_web]:
            st.markdown("**Initiative's website:** " + p_web)
        else:
            st.markdown("**Initiative's website:** No available yet")

        try:
            numbermemberpledge = df_gi_select['q62'].iloc[0]
            col1, col2, col3, col4 = st.columns(4)

            # Check if numbermemberpledge is NaN
            if pd.isna(numbermemberpledge):
                col1.markdown("**Members:** No available yet")
            else:
                col1.metric("**Members**", numbermemberpledge)
        except Exception as e:
            col1.markdown("**Members:** No available yet")
    except Exception as e:
        tile_partner_reporting_status =f"""#### PRESENTATION"""
        # st.markdown(tile_partner_reporting_status)
        # st.write("No Information Available")
        pass
# END PRESENTATION LEVEL

