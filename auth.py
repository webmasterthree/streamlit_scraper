import os
import streamlit as st
from pymongo import MongoClient
from database import db



# Initialize st.session_state.role to None
if "auth" not in st.session_state:
    st.session_state.auth = None

# Retrieve the role from Session State to initialize the widget
st.session_state.auth = st.session_state.auth


def authenticate(username, password):
    user_collection = db.get_collection("user_collection")
    user = user_collection.find_one({"username": username, "password": password})
    if user is not None:
        st.session_state.auth = True
        st.session_state.user = user
        return True
    return False


# Selectbox to choose role
def login():
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            return True
        else:
            st.error("Invalid username or password")
            return False


if not st.session_state.auth:
    if login():
        st.switch_page("pages/main.py")

else:
    st.switch_page("pages/main.py")
