# login.py

import yaml
import streamlit as st
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from streamlit_authenticator.utilities import *
from pathlib import Path
from streamlit_app import main_app

# Load hashed credentials from a YAML file (see below)
def load_credentials():
    credentials_path = Path(__file__).parent / "credentials.yaml"
    with open(credentials_path, "r") as file:
        config = yaml.load(file, Loader=SafeLoader)
        return config

# Create authenticator with cookie-based session
def authenticate_user():
    config = load_credentials()
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']
    )
    
   # Creating a login widget
    try:
        authenticator.login('main')
    except LoginError as e:
        st.error(e)

        # Authenticating user
    if st.session_state['authentication_status']:
        authenticator.logout("logout", "sidebar")
        #st.write(f'Welcome *{st.session_state["name"]}*')
        #st.title('Some content')
        main_app()
    elif st.session_state['authentication_status'] is False:
        st.error('Username/password is incorrect')
    elif st.session_state['authentication_status'] is None:
        st.warning('Please enter your username and password')

    return None
