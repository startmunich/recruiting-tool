from dotenv import load_dotenv
import os
import pandas as pd
from pyairtable import Api
import streamlit as st

# Load dotenv file
load_dotenv(override=True)

# Constants
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_ID = os.environ['AIRTABLE_BASE_ID']
AIRTABLE_TABLE_ID = os.environ['AIRTABLE_TABLE_ID']
QUESTION_START = 10
QUESTION_NUMBER = 7


# Get table from airtable using pyairtable
def get_table():
    api = Api(AIRTABLE_API_KEY)
    return api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)


# Load cleaned data from airtable into pandas dataframe
def load_dataframe(record_list):
    df = pd.DataFrame([record['fields'] for record in record_list],
                      index=[record['fields']['Submission ID'] for record in record_list])
    return df.drop(columns=["Index", "Respondant ID", "Submitted at"])


# Load css and apply to streamlit
# css = open('static/css/style.css')
# st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


# Create page titles from dataframe
def create_page_titles(df):
    ids = df['Submission ID'].tolist()
    completed = ["✅" if completed == 1 else "" for completed in df['Completed 1'].tolist()]

    # title is id and completed as string
    return [f'{id} {completed}' for id, completed in zip(ids, completed)]


# Render page
def render_page(row, title, questions):
    st.title(f'Application: {title}')

    st.header("Questions")
    st.write("\n")

    for question in questions:
        st.markdown(f"**{question}**")
        st.write(row[question])
        st.divider()

    with st.form("Testform"):
        st.header("Ranking")
        st.write("Please give us a qualitative ranking based on the presented information about this candidate.")
        qualitative_1 = st.text_area("")
        col1, col2 = st.columns(2)
        with col1:
            quantitative_1 = st.number_input("Rank this candidate from 1 (bad) to 5 (great)", min_value=1, max_value=5, value=None, step=1)
        with col2:
            interview_1 = st.checkbox("Invite to interview")
        #check if all prior information is right
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.success("Review sucessfully submitted!")



def main():
    # Load data
    table = get_table()
    record_list = table.all()
    df = load_dataframe(record_list)

    # Init page titles
    titles = create_page_titles(df)

    # Init questions
    questions = df.columns[QUESTION_START:QUESTION_START + QUESTION_NUMBER].tolist()

    # Get selected page and render
    selected_page = st.sidebar.selectbox("Select an application", titles)
    _id = selected_page.split(" ")[0]
    render_page(df.loc[_id], selected_page, questions)


if __name__ == '__main__':
    main()
