import streamlit as st


def authenticated_menu():
    # Show a navigation menu for authenticated users
    st.sidebar.page_link("pages/main.py")
    # st.sidebar.page_link("pages/user.py", label="Your profile")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.page_link("auth.py", label="Log in")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if (
        "auth" not in st.session_state
        or st.session_state.auth is None
        or not st.session_state.auth
    ):
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if (
        "auth" not in st.session_state
        or st.session_state.auth is None
        or not st.session_state.auth
    ):
        st.switch_page("auth.py")
    menu()