import streamlit as st
from st_pages import Page, show_pages, add_page_title, hide_pages

if st.session_state["authentication_status"]:
    name = st.session_state["name"]

    show_pages(
        [
            Page("pages/welcome.py", f"Welcome {name}", "👋"),
            Page("pages/screening.py", "Application Screening", "🖋️"),
        ]
    )

    applications_left = 8
    applications_reviewed = 4
    progress = applications_reviewed / (applications_left + applications_reviewed)

    st.title(f"Hello {name}!")

    col1, col2 = st.columns([3, 2])
    with col1:
        st.write(
            "This is a new tool which will help you slice through the application reviewing process easily. Choose from the applications on the left and may the onbaording START!")
        st.subheader(f"You have {applications_left} applications left to review. Let's go 💪🏻!")
        if applications_reviewed != 0:
            st.subheader(f"You have already reviewed {applications_reviewed} 🥳")

    with col2:
        st.image("start_polygon.png", width=250)

    st.progress(progress)

else:
    st.stop()

