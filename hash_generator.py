import streamlit_authenticator as stauth
hashed_pw = stauth.Hasher().hash('nila@2025')
print(hashed_pw)
