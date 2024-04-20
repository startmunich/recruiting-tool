import streamlit as st
from st_pages import Page, show_pages, add_page_title, hide_pages

if st.session_state["authentication_status"]:
    name = st.session_state["name"]

    show_pages(
        [
            Page("main.py", f"Welcome {name}", "👋"),
            Page("screening.py", "Application Screening", "🖋️"),
        ]
    )

    st.write(f"Welcome {name}")

