import json
import time

import gspread

from services import database as db


# Constants
INDEX_SCREENER = 2
INDEX_QUALITATIVE = 3
INDEX_QUANTITATIVE = 4
INDEX_INTERVIEW = 5
INDEX_NOTES = 6
INDEX_COMPLETED = 7

# Constant for the amount of questions
N_QUESTIONS = 6

QUESTION_COLS = [
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "AA",
    "AB",
]

# Initialize variables
gc = None
sh = None
application_data = None
evaluations = None
user_data = None
row_numbers = None
questions = None


# Initialize the google sheet
def init():
    print("Initializing google sheet")
    global gc, sh, application_data, evaluations, user_data, row_numbers, questions

    with open("service_account.json", "r") as credentials_file:
        gc_credentials = json.load(credentials_file)
        gc = gspread.service_account_from_dict(gc_credentials)
        sh = gc.open("Application Batch Summer 24 🚀")
        application_data = sh.get_worksheet(0)
        evaluations = sh.get_worksheet(1)
        user_data = sh.get_worksheet(2)
        row_numbers = {submission_id: i + 2 for i, submission_id in enumerate(application_data.col_values(1)[1:])}
        questions = [application_data.acell(f'{c}1').value for c in QUESTION_COLS]


# Upload evaluation .data to the google sheet
def db_to_gsheet():
    print("Loading .data from db into google sheet")
    result = {}

    for evaluation in db.evaluations.getAll():
        row = row_numbers[evaluation["Submission ID"]]

        result_list = []
        for screener_nr in [1, 2, 3]:
            key_screener = f"Screener {screener_nr}"
            key_qualitative = f"Evaluation {screener_nr} - Qualitative"
            key_quantitative = f"Evaluation {screener_nr} - Quantitative"
            key_interview = f"Evaluation {screener_nr} - Interview"
            key_notes = f"Evaluation {screener_nr} - Additional Notes"
            key_completed = f"Evaluation {screener_nr} - Complete"

            result_list += [
                evaluation[key_screener],
                evaluation[key_qualitative],
                evaluation[key_quantitative],
                evaluation[key_interview],
                evaluation[key_notes],
                evaluation[key_completed],
            ]

        result[row] = result_list

    try:
        evaluations.update(f"B2:S{len(result) + 1}", [result[i] for i in range(2, len(result) + 2)])
        return True
    except gspread.exceptions.APIError as e:
        print(e)
        return False


def gsheet_to_db():
    print("Loading .data from google sheet into db")
    # Clear json db
    db.clear()

    # Load .data from google sheet into json db
    db.load_application_data_into_db(application_data.get_all_records(expected_headers=questions))
    db.load_recruiting_tool_data_into_db(evaluations.get_all_records())
    db.load_users_into_db(user_data.get_all_records())
    db.load_questions_into_db(questions)


# Function to calculate the right column index for each screener and desired value
def get_column_for_screener_nr(column_index, screener_nr):
    return column_index + (screener_nr - 1) * N_QUESTIONS


# Get the screener number for a user given the evaluation
def get_screener_nr_for_user(user, evaluation):
    screener_str = list(evaluation.keys())[list(evaluation.values()).index(user)]
    return 1 if screener_str == "Screener 1" else 2 if screener_str == "Screener 2" else 3
