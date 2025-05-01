import streamlit_authenticator as stauth
hashed_pw = stauth.Hasher(['1234']).generate()
print(hashed_pw[0])
