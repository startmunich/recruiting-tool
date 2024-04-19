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

# load css and apply to streamlit
# css = open('static/css/style.css')
# st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# basic streamlit app
st.title('Recruiting Tool')

df = df.drop(columns = ["Index", "Respondant ID", "Submitted at"])

questions = df.columns[QUESTION_START:QUESTION_START+QUESTION_NUMBER]
user_index = 5

st.header("Questions")
st.markdown("""---""")

for i in range(0, len(questions)):
    st.write(questions[i])
    st.write(df[(questions[i])][user_index])
    st.markdown("""---""")

st.header("Ranking")
st.write("Please give us a qualitative ranking based on the presented information about this candidate.")
st.text_area("")
