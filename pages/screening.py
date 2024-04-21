import time

from dotenv import load_dotenv
import pandas as pd
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.stylable_container import stylable_container
from services import authenticator as auth
from services import database as db

# Load dotenv file
load_dotenv(override=True)


# Load cleaned .data from airtable into pandas dataframe
def load_dataframe(record_list):
    df = pd.DataFrame([record['fields'] for record in record_list],
                      index=[record['fields']['Submission ID'] for record in record_list])
    return df.drop(columns=["Index", "Respondant ID", "Submitted at"])


# Render page
def render_page(submission_id, screener_nr, completed, evaluation, application, questions):
    with st.container(border=True):
        # A suitable emoji for a paper application
        st.title(f'{"✅" if completed else "📄"} Application {submission_id}')
        st.markdown("""
            <style>
            .answer {
                font-size: 16px !important;
            }
            </style>
            """, unsafe_allow_html=True)

        for i in range(len(questions)):
            if application[questions[i]]:
                st.markdown(f"***{questions[i].strip()}***")

                with stylable_container(
                        key=f"question_{i}",
                        css_styles="""
                                    {
                                        background-color: #011152;
                                        border-radius: 4px;
                                        padding: 16px;
                                    }
                                """
                ):
                    with st.container():
                        st.markdown(f'<p class="answer">{application[questions[i]]}</p>', unsafe_allow_html=True)

                add_vertical_space(2)

    with st.form("Evaluation Form"):
        st.header("Evaluation")

        qualitative_value = evaluation[f"Evaluation {screener_nr} - Qualitative"]
        quantitative_value = evaluation[f"Evaluation {screener_nr} - Quantitative"]
        quantitative_int = int(quantitative_value) if quantitative_value else None

        interview_options = ["<select>", "Yes 👍", "No 👎"]
        interview_value = evaluation[f"Evaluation {screener_nr} - Interview"]
        interview_index = interview_options.index(interview_value) if interview_value in interview_options else 0

        notes_value = evaluation[f"Evaluation {screener_nr} - Additional Notes"]
        complete_value = evaluation[f"Evaluation {screener_nr} - Complete"]
        complete_bool = complete_value == "TRUE" if complete_value else False

        qualitative = st.text_area(
            "Please give us a qualitative ranking based on the presented information about this candidate.",
            value=qualitative_value)
        quantitative = st.number_input("Rank this candidate from 1 (bad) to 5 (great)", min_value=1, max_value=5,
                                       value=quantitative_int, step=1)
        interview = st.selectbox("Would you like to interview this candidate?", interview_options,
                                 index=interview_index)
        notes = st.text_area("Here you can add any additional notes or comments.", value=notes_value)
        complete = st.checkbox("Mark as complete", value=complete_bool)

        # Check if all prior information is right
        submitted = st.form_submit_button("Submit")
        if submitted:
            if complete and not qualitative:
                st.error("Please provide a qualitative evaluation.")
            elif complete and not quantitative:
                st.error("Please provide a qualitative evaluation.")
            elif complete and not quantitative:
                st.error("Please provide a quantitative evaluation.")
            elif complete and (not interview or interview == "<select>"):
                st.error("Please provide an interview decision.")

            elif db.update_evaluation(screener_nr, submission_id, qualitative, quantitative, interview, notes, complete):
                st.success("Evaluation submitted successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Error submitting evaluation. Please try again.")


# Load css and apply to streamlit
def apply_css():
    css = open("static/css/style.css")
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


def main():

    # Check if user is logged in
    status, user = auth.logged_in()

    if not status:
        st.switch_page("main.py")

    else:
        questions = db.load_question()
        submissions, n_completed = db.load_submission_id_for_user(user)

        apply_css()

        # Sidebar texts
        st.sidebar.title(f"Hey, {user}! 👋")
        st.sidebar.markdown(f"You have {len(submissions) - n_completed} applications left to review. Let's go!")
        st.sidebar.divider()

        # Create submission titles
        submission_titles = [f"{submission_id} - {'✅' if completed else '📄'}" for submission_id, (screener, completed)
                             in submissions.items()]

        # Get preselected submission from st.session_state
        submission_ids = list(submissions.keys())
        preselected_submission_index = submission_ids.index(
            st.session_state["selected_submission"]) if "selected_submission" in st.session_state else 0

        # Select submission
        selected_submission_title = st.sidebar.selectbox("Select an application:", submission_titles,
                                                         index=preselected_submission_index)

        st.sidebar.button("Logout", on_click=auth.logout)

        if not selected_submission_title:
            st.subheader("You weren't assigned any applications yet.")
            st.text("Please try again later.")

        else:
            selected_submission_id = selected_submission_title.split("-")[0].strip()
            st.session_state["selected_submission"] = selected_submission_id

            evaluation_result = db.evaluations.getByQuery({"Submission ID": selected_submission_id})
            application_result = db.applications.getByQuery({"Submission ID": selected_submission_id})

            if evaluation_result and application_result:
                evaluation = evaluation_result[0]
                application = application_result[0]
                render_page(
                    submission_id=selected_submission_id,
                    screener_nr=submissions[selected_submission_id][0],
                    completed=submissions[selected_submission_id][1],
                    evaluation=evaluation,
                    application=application,
                    questions=questions
                )

            else:
                st.error("Error loading application. Please try again.")


if __name__ == '__main__':
    main()
