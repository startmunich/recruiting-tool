import hashlib

from pysondb import db

applications = db.getDb(".data/applications.json")
evaluations = db.getDb(".data/evaluations.json")
users = db.getDb(".data/users.json")
questions = db.getDb(".data/questions.json")


def load_application_data_into_db(application_data):
    applications.addMany(application_data)


def load_recruiting_tool_data_into_db(recruiting_tool_data):
    evaluations.addMany(recruiting_tool_data)


def load_users_into_db(user_data):
    # Hash the password
    salt = "FinOps is awesome!"
    for user in user_data:
        user["Password"] = hashlib.sha512((user["Password"] + salt).encode("utf-8")).hexdigest()
        user["Token"] = None

    users.addMany(user_data)


def load_questions_into_db(question_data, links_data):
    questions.add({"Type": "Questions", "values": question_data})
    questions.add({"Type": "Links", "values": links_data})


def clear():
    applications.deleteAll()
    evaluations.deleteAll()
    users.deleteAll()
    questions.deleteAll()


def update_evaluation(screener_nr, submission_id, qualitative, quantitative, interview, notes, completed):
    try:
        evaluation = {
            "Submission ID": submission_id,
            f"Evaluation {screener_nr} - Qualitative": qualitative,
            f"Evaluation {screener_nr} - Quantitative": quantitative,
            f"Evaluation {screener_nr} - Interview": "" if interview == "<select>" else interview,
            f"Evaluation {screener_nr} - Additional Notes": notes,
            f"Evaluation {screener_nr} - Complete": "TRUE" if completed else "FALSE",
        }
        evaluations.update({"Submission ID": submission_id}, evaluation)
        return True

    except Exception as e:
        print(e)
        return False


def load_submission_id_for_user(user):
    # Load all evaluations for the user
    user_evaluations = [
        evaluations.getByQuery({"Screener 1": user}),
        evaluations.getByQuery({"Screener 2": user}),
        evaluations.getByQuery({"Screener 3": user})
    ]

    submissions = {}
    n_completed = 0

    for i in range(3):
        for evaluation in user_evaluations[i]:

            # Check submission completed
            completed = evaluation[f"Evaluation {i + 1} - Complete"] == "TRUE"
            if completed:
                n_completed += 1

            # Add screener nr and completed status to the submission
            submissions[evaluation["Submission ID"]] = (i + 1, completed)

    return submissions, n_completed


def load_questions():
    return questions.getByQuery({"Type": "Questions"})[0]["values"]


def load_links():
    return questions.getByQuery({"Type": "Links"})[0]["values"]
