from dotenv import load_dotenv
import os
import pandas as pd
from pyairtable import Api
import streamlit as st

# load dotenv file
load_dotenv(override=True)

# constants
AIRTABLE_API_KEY = os.environ['AIRTABLE_API_KEY']
AIRTABLE_BASE_ID = os.environ['AIRTABLE_BASE_ID']
AIRTABLE_TABLE_ID = os.environ['AIRTABLE_TABLE_ID']

# load records from airtable using pyairtable
api = Api(AIRTABLE_API_KEY)
table = api.table(AIRTABLE_BASE_ID, AIRTABLE_TABLE_ID)
record_list = table.all()

# load data into pandas dataframe
df = pd.DataFrame([record['fields'] for record in record_list], index=[record['fields']['Submission ID'] for record in record_list])

# basic streamlit app
st.title('Recruiting Tool')
st.dataframe(df)
