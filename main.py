from dotenv import load_dotenv
import os
from numpy import isreal
import pandas as pd
from pyairtable import Api
import streamlit as st

# load dotenv file
load_dotenv(override=True)

# constants
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_ID = os.environ['AIRTABLE_BASE_ID']
AIRTABLE_TABLE_ID = os.environ['AIRTABLE_TABLE_ID']
QUESTION_START = 10
QUESTION_NUMBER = 3

# load records from airtable using pyairtable
api = Api(AIRTABLE_API_KEY)
table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)
record_list = table.all()

# load data into pandas dataframe
df = pd.DataFrame([record['fields'] for record in record_list],
                  index=[record['fields']['Submission ID'] for record in record_list])

# drop unnecessary columns
df = df.drop(columns=["Index", "Respondant ID", "Submitted at"])

# load css and apply to streamlit
# css = open('static/css/style.css')
# st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# init questions
questions = df.columns[QUESTION_START:QUESTION_START + QUESTION_NUMBER].tolist()


# basic streamlit app
def render_page(row, completed):
    st.title(f'{completed} {row["First Name"]} {row["Last Name"]}')

    st.header("Questions")
    st.markdown("""---""")

    for question in questions:
        st.write(question)
        st.write(row[question])
        st.markdown("""---""")

    st.header("Ranking")
    st.write("Please give us a qualitative ranking based on the presented information about this candidate.")
    st.text_area("")


ids = df['Submission ID'].tolist()
completed = ["✅" if completed == 1 else "❌" for completed in df['Completed 1'].tolist()]

# title is id and completed as string
titles = [f'{id} {completed}' for id, completed in zip(ids, completed)]

selected_page, completed = st.sidebar.selectbox("Select an application", titles).split(" ")
render_page(df.loc[selected_page], completed)
