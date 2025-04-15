import streamlit as st


# --- PAGE SETUP ---
about_page = st.Page(
    "views/QEforAI_Landing.py",
    title="QE for AI",
    icon=":material/account_circle:",
    default=True,
)
project_1_page = st.Page(
    "views/storywise.py",
    title="StoryWise",
    icon=":material/bar_chart:",
)
project_2_page = st.Page(
    "views/chatbot.py",
    title="Chat Bot",
    icon=":material/smart_toy:",
)


# --- NAVIGATION SETUP [WITHOUT SECTIONS] ---
# pg = st.navigation(pages=[about_page, project_1_page, project_2_page])

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [about_page],
        "Projects": [project_1_page, project_2_page],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo("assets/narwal.png")
st.sidebar.markdown("Made to demonstrate AI for QE Capabilities")


# --- RUN NAVIGATION ---
pg.run()
