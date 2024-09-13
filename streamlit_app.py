import streamlit as st
from time import sleep
from navigation import make_sidebar

make_sidebar()

st.title("Movie Recommendation System")

st.write("Please log in to continue (user id `Enter any number between 1 to 671`, password `test`).")

username = st.text_input("User ID")
password = st.text_input("Password", type="password")

if st.button("Log in", type="primary"):
    if username in map(str, range(1, 672)) and password == "test":
        st.session_state.logged_in = True
        st.session_state['username'] = username
        st.success("Logged in successfully!")
        sleep(0.5)
        st.switch_page("pages/page1.py")
    else:
        st.error("Incorrect username or password")
