from PIL import Image
import streamlit as st



def structure_and_format():
    im = Image.open("images/R2R_RGB_PINK_BLUE.png")
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


##MAIN SIDE
st.markdown("# Publications")


# Define links for the available reports
reports = {
    "2022": "https://climatechampions.unfccc.int/wp-content/uploads/2022/09/Race-to-Zero-Race-to-Resilience-Progress-Report.pdf",
    "2023": "https://climatechampions.unfccc.int/wp-content/uploads/2024/01/Race-to-Resilience-2023-Campaign-Progress-Report.pdf",
    "2024": None  # Report not yet launched
}

col1, col2, col3 = st.columns(3)
with col1:
    st.button("2024 Report (Coming Soon)", disabled=True)
with col2:
    st.write("")
with col3:
    if st.button("Download 2023 RtR Report"):
        st.markdown(f"[Click here to download]( {reports['2023']} )", unsafe_allow_html=True) 
    
    if st.button("Download 2022 RtR Report"):
        st.markdown(f"[Click here to download]( {reports['2022']} )", unsafe_allow_html=True)
    
    
    