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
st.markdown("# ABOUT THE RtR DATA EXPLORER")

st.markdown("""As a web application developed specifically for the RtR Campaign, the RtR Data Explorer aims to provide information on increased resilience across the Campaign. 
It achieves this objective by utilizing two complementary approaches for human-centered resilience-building: Magnitude and Depth of Resilience. 
- The Magnitude approach helps estimate the size of the impact of resilience-building initiatives, primarily by looking at the number of beneficiaries reached. The RtR Data Explorer provides information on the number of people in vulnerable communities who have benefited from the resilience initiatives across the Campaign. 
- The Depth approach, on the other hand, provides an understanding of how partners and their members are contributing to increasing resilience by observing which conditions (Resilience Attributes) they are impacting. The RtR Data Explorer provides information on the specific resilience attributes that have been impacted by the initiatives, helping to showcase the depth of impact. 

**The RtR Data Explorer aims to provide a comprehensive view of the increased resilience across the RtR Campaign, utilizing both Magnitude and Depth approaches to provide a detailed understanding of the impact of resilience-building initiatives**.
It is made by the Technical Secretariat of the Race to Resilience Campaign, with the support of the Center for Climate and Resilience Research at the Universidad de Chile.
""")


st.header('FREQUENTLY ASKED QUESTIONS')
st.subheader("WHAT IS THE RtR DATA EXPLORER?")
st.markdown("""
The RtR Data Explorer is a web application designed to support the Race to Resilience Campaign. It aims to provide a comprehensive view of the increased resilience across the RtR Campaign, utilizing both Magnitude and Depth approaches to provide a detailed understanding of the impact of resilience-building initiatives. 
""")



st.subheader('WHO ARE ITS USERS?')
st.markdown("""
**User Base of the RtR Data Explorer**
The RtR Data Explorer is primarily designed for non-State actors collaborating with the Race to Resilience Campaign. These partners utilize the platform to report their climate resilience actions and to quantify and validate their impact within a unified framework. Additionally, the platform serves as a valuable resource for anyone interested in understanding the progress and impact of the Campaign's efforts in augmenting global resilience.
""")

st.subheader('HOW IS IT MADE?')
st.markdown("""
**Development of the RtR Data Explorer**
Developed by the Technical Secretariat at the Center for Climate and Resilience Research, Universidad de Chile, the RtR Data Explorer is a product of modern web technologies. It integrates HTML, CSS, JavaScript, and Python, creating an accessible platform via any contemporary web browser. The data, sourced from our partners' resilience initiatives reports, is meticulously aggregated and presented through an intuitive user interface on this platform.
""")


#data updated

@st.cache_data
def load_data_cleaned_formatted_date_gi():
    from etl_process import formatted_date_gi
    return formatted_date_gi
formatted_date_gi = load_data_cleaned_formatted_date_gi()

@st.cache_data
def load_data_cleaned_formatted_date_pledge():
    from etl_process import formatted_date_pledge
    return formatted_date_pledge
formatted_date_pledge = load_data_cleaned_formatted_date_pledge()

@st.cache_data
def load_data_cleaned_formatted_date_plan():
    from etl_process import formatted_date_plan
    return formatted_date_plan
formatted_date_plan =  load_data_cleaned_formatted_date_plan()


st.subheader('WHERE DOES ITS DATA COME FROM?')
st.markdown(f"""
**Data Sources of the RtR Data Explorer**
The core data of the RtR Data Explorer stems from the Race to Resilience Campaign's Reporting Tools. These tools are instrumental in enabling our partners to methodically document their contributions towards building resilience against climate change. We offer a succinct overview of the three primary Campaign stages - Apply, Pledge, and Plan - along with the bespoke reporting tools tailored for each stage.

- **Stage 1: Apply - General Information Survey**
  - *Objective:* To amass comprehensive data about RtR partners and their members.
  - *Key Areas:* Information on initiatives, member details, metric strategies, involvement in the Sharm-El-Sheikh Adaptation Agenda, resilience action clusters, and types of impact.
  - *Purpose:* To establish a foundational understanding of each partner’s scope, methodologies, and potential impact within the RtR framework.
  - *Last Data Update:* {formatted_date_gi}

- **Stage 2: Pledge - Pledge Statement Survey**
  - *Objective:* To collect, standardize, and present partners’ resilience commitments for 2030.
  - *Key Areas:* Introduction, identification of partners and beneficiaries, principles of locally led adaptation, mobilization of financial resources, fundamentals of the 2030 pledge, and explanation for reported numbers.
  - *Purpose:* This survey ensures transparency, accountability, and alignment of partners’ pledges with the Campaign's overarching goals.
  - *Last Data Update:* {formatted_date_pledge}

- **Stage 3: Plan - Resilience-Building Plan Survey**
  - *Objective:* To guide partners in developing detailed action plans aligned with their 2030 pledges.
  - *Key Areas:* Plan identification, problem description, mapping change pathways in relation to the Sharm-El-Sheikh Adaptation Agenda, defining interventions (action clusters), assessment of resilience attributes, plan governance, and final confirmation of the statement.
  - *Purpose:* This stage focuses on strategic planning and governance of action plans, emphasizing the depth and magnitude of interventions to achieve the 2030 resilience goals.
  - *Last Data Update:* {formatted_date_plan}

These tools are essential components of the RtR Campaign, designed to capture a diverse range of aspects in our partners' resilience-building efforts. Through these tools, partners can effectively monitor their progress, align with Campaign objectives, and significantly contribute to our shared goal of global resilience by 2030.
""")



st.subheader('HOW CAN I BECOME A MEMBER OF THE RACE TO RESILIENCE CAMPAIGN?')
st.markdown("""To become a member of the Race to Resilience Campaign, initiatives or partners must first submit an Expression of Interest (EoI) form that explains why they are a good candidate for the Campaign and commit to following RtR's membership rules and criteria. After being accepted into the Campaign, partners must set a target for resilience action for themselves and their members and draft an evidence-based plan to take action towards their pledge. Finally, partners should take immediate and effective action towards achieving the actions they have planned and report against this progress. 

Read more """+"[here](https://racetozero.unfccc.int/system/racetoresilience/)")

# st.sidebar.caption('NAVEGATION MENU')
st.sidebar.markdown('')
st.sidebar.caption("[INTRODUCTION](#about-the-rtr-data-explorer)")
st.sidebar.markdown('')
st.sidebar.caption("[FREQUENTLY ASKED QUESTIONS](#frequently-asked-questions)")
st.sidebar.caption("- [What is the RtR Data Explorer?](#what-is-the-rtr-data-explorer)")
st.sidebar.caption("- [Who are its users?](#who-are-its-users)")
st.sidebar.caption("- [How is it made?](#how-is-it-made)")
st.sidebar.caption("- [Where the data come from?](#where-does-its-data-come-from)")
# st.sidebar.caption("- [How to become a RtR Partner](#how-can-i-become-a-member-of-the-race-to-resilience-campaign)")
st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.markdown('')
st.sidebar.caption("**RtR’s WEB PAGE [HERE](https://racetozero.unfccc.int/system/racetoresilience/)**")
st.sidebar.markdown("")
# st.sidebar.caption('**RtR’s METRICS FRAMEWORK [HERE](https://climatechampions.unfccc.int/wp-content/uploads/2022/11/Working-Paper-No-1_R2R%C2%B4s-Metrics-Framework_Oct2022-FOR_SLT.docx.pdf)**')
# st.sidebar.markdown("")
# st.sidebar.caption('**RtR’s METRICS FRAMEWORK VIDEO [HERE](https://www.youtube.com/watch?v=TZFp9_LL8qs)**')


st.markdown("___")

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
        <li>To search for the contribution of specific partners, <a href="/PARTNER_FINDER" target="_self"><strong>click here</strong></a></li>
        <li>To explore our Metrics Framework, <a href="/METRICS_FRAMEWORK" target="_self"><strong>click here</strong></a></li>
    </ul>
</div>
""", unsafe_allow_html=True)

