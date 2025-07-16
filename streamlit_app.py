import streamlit as st

# Dummy user database (replace with real DB or auth service in production)
USER_DB = {
    "admin": "admin123",
    "user1": "password1",
    "user2": "password2"
}


# --- PAGE SETUP ---
about_page = st.Page(
    "views/QEforAI_Landing.py",
    title="NILA - AI for QE",
    icon=":material/account_circle:",
    default=True,
)
project_1_page = st.Page(
    "views/storywise.py",
    title="StoryWise - User Story Assessor",
    icon=":material/bar_chart:",
)

project_2_page = st.Page(
    "views/storycraft.py",
    title="StoryCraft - User Story Refiner",
    icon=":material/fax:",
)

project_3_page = st.Page(
    "views/testweaver.py",
    title="TestWeaver API - Generate test cases and scripts from specs",
    icon=":material/book:",
)

project_4_page = st.Page("views/testweaver-ui.py",
                title= "TestWeaver UI - Generate test automation scripts from test steps",
                icon=":material/fax:")

project_5_page = st.Page("views/testweaver-ui-bulk.py",
                title= "TestWeaver UI (Bulk) - Generate test automation suite",
                icon=":material/fax:")


project_n_page = st.Page(
    "views/chatbot.py",
    title="QE Chat Bot",
    icon=":material/smart_toy:",
)

# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])
def main_app():
    # --- NAVIGATION SETUP [WITH SECTIONS]---
    pg = st.navigation(
        {
            "Info": [about_page],
            "Projects": [project_1_page, project_2_page, project_3_page, project_4_page, project_5_page],
        }
    )


    # --- SHARED ON ALL PAGES ---
    st.logo("assets/narwal.png")
    #st.sidebar.markdown("Made to demonstrate AI for QE Capabilities")


    # --- RUN NAVIGATION ---
    pg.run()
