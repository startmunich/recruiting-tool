# streamlit_app.py


import streamlit as st
from services import authenticator as auth
from services import gsheet as gs
from timeloop import Timeloop
from datetime import timedelta

with open("static/css/style.css") as css:
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

tl = Timeloop()


@st.cache_resource()
def init():
    gs.init()
    gs.gsheet_to_db()
    tl.start()


@tl.job(interval=timedelta(seconds=10))
def sync():
    gs.db_to_gsheet()


def password_entered():
    if auth.login(st.session_state["username"], st.session_state["password"])[0]:
        del st.session_state["password"]  # Don't store the username or password.
        del st.session_state["username"]
    else:
        st.error("😕 STARTie not known or password incorrect")


if auth.logged_in()[0]:
    st.switch_page("pages/screening.py")
else:
    init()
    # st.markdown("<h1 style='text-align: center; font-weight: bold; margin: 32px;'>Recruiting SoSe2024</h1>", unsafe_allow_html=True)

    st.set_page_config(page_title="Recruiting SoSe2024", page_icon=":rocket:")

    with st.form("Credentials"):
        st.text_input("Username", key="username")
        st.text_input("Password", type="password", key="password")
        st.form_submit_button("Log in", on_click=password_entered)
