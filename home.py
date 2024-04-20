import streamlit as st
from streamlit.elements import progress

#dummy variables
user = "Niko"
applications_left = 8
applications_reviewed = 4
progress = applications_reviewed/(applications_left + applications_reviewed)

st.title(f"Hello {user}!")

col1, col2 = st.columns([3, 2])
with col1:
    st.write("This is a new tool with which will help you slice through the application reviewing process easily. Choose from the applications on the left and START the journey!")
    st.write("\n")
    st.markdown(f"**You have {applications_left} applications left to review. Let's go 💪🏻!**")
    if applications_reviewed != 0:
        st.markdown(f"**You have already reviewed {applications_reviewed} 🥳**")

with col2:
    st.image("start_polygon.png", width=250)

st.progress(progress)
