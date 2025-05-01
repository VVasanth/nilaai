# main.py

import streamlit as st
from login import authenticate_user

authenticator = authenticate_user()

if authenticator:
    # Authenticated app goes here
    st.write("Secret dashboard 📊")
    st.sidebar.title("Navigation")
    authenticator.logout("Logout", "sidebar")
