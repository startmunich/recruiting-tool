import streamlit as st
import streamlit_authenticator as stauth
from st_pages import Page, show_pages, add_page_title, hide_pages
import yaml

st.set_page_config(
    page_title="Welcome",
    page_icon="👋",
)

with open('./static/config/auth.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['pre-authorized']
)

status = False
hide_pages(
        [
            Page("pages/welcome.py", "Welcome", "👋"),
            Page("pages/screening.py", "Application Screening", "🖋️"),
        ]
)

if not status:
    name, status, username = authenticator.login(location="main", clear_on_submit=True)

    st.session_state["name"] = name
    st.session_state["authentication_status"] = status
    st.session_state["username"] = username

    if status:
        st.switch_page("pages/welcome.py")
