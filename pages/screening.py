import time

from dotenv import load_dotenv
import pandas as pd
from PIL import Image
import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_extras.stylable_container import stylable_container
from services import authenticator as auth
from services import database as db

# Load dotenv file
load_dotenv(override=True)

# Set page title and icon
st.set_page_config(page_title="Recruiting Tool", page_icon=Image.open("static/img/favicon.png"))


# Load cleaned .data from airtable into pandas dataframe
def load_dataframe(record_list):
    df = pd.DataFrame([record['fields'] for record in record_list],
                      index=[record['fields']['Submission ID'] for record in record_list])
    return df.drop(columns=["Index", "Respondant ID", "Submitted at"])


# Render page
def render_page(submission_id, screener_nr, completed, evaluation, application, questions, links):
    with st.container(border=True):
        st.header(f'{"✅" if completed else "📄"} Application {submission_id}')

        for i in range(len(questions)):
            if application[questions[i]]:
                st.markdown(f"***{questions[i].strip()}***")

                with stylable_container(
                        key=f"question_{i}",
                        css_styles="""
                                    {
                                        opacity: 0.78;
                                        transform: scale(0.98, 0.98);
                                        -ms-transform: scale(0.98, 0.98); /* IE 9 */
                                        -webkit-transform: scale(0.98, 0.98); /* Safari and Chrome */
                                        -o-transform: scale(0.98, 0.98); /* Opera */
                                        -moz-transform: scale(0.98, 0.98); /* Firefox */
                                    }
                                """
                ):
                    with st.container():
                        st.markdown(f'<p class="answer">{application[questions[i]]}</p>', unsafe_allow_html=True)

                add_vertical_space(2)

    with st.form("Evaluation Form"):
        st.subheader("Evaluation")

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
            "Qualitative evaluation",
            value=qualitative_value, height=160)
        quantitative = st.slider("Rank this candidate on a scale from 1 (Clear No) to 5 (Clear Yes)", min_value=1, max_value=5, step=1, value=quantitative_int)
        interview = st.selectbox("Should we interview this candidate?", interview_options,
                                 index=interview_index)
        notes = st.text_area("Additional Notes", value=notes_value, height=120)
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

            elif db.update_evaluation(screener_nr, submission_id, qualitative, quantitative, interview, notes,
                                      complete):
                st.success("Evaluation submitted successfully!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Error submitting evaluation. Please try again.")

    if completed:
        with st.container(border=True):
            st.subheader("Further Information")
            st.write("The following discloses name, gender and/or university of the candidate.")
            st.markdown("""
                <style>
                .answer {
                    font-size: 16px !important;
                }
                </style>
                """, unsafe_allow_html=True)

            for i in range(len(links)):
                if application[links[i]]:
                    link = application[links[i]]
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown(f"**{links[i].strip()}**")

                    with col2:
                        st.markdown(f"[click to open]({link})")


# Load css and apply to streamlit
def apply_css():
    css = open("static/css/style.css")
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


def format_submission_title(submission_id, submissions):
    completed = submissions[submission_id][1]
    return f"{submission_id} - {'✅' if completed else '📄'}"


def main():
    # Check if user is logged in
    status, user = auth.logged_in()

    if not status:
        st.switch_page("main.py")

    else:
        questions = db.load_questions()
        links = db.load_links()
        submissions, n_completed = db.load_submission_id_for_user(user)

        apply_css()

        # Sidebar texts
        st.sidebar.title(f"Hey, {user}! 👋")
        st.sidebar.markdown(f"""<p>You have <span class="colored">{len(submissions) - n_completed}</span> applications left to review. Let's go!</p>""", unsafe_allow_html=True)
        st.sidebar.divider()

        submission_ids = list(submissions.keys())
        selected_submission_index = submission_ids.index(st.session_state.selected_submission) if "selected_submission" in st.session_state else 0

        # Select submission
        st.sidebar.selectbox("Select an application:", submission_ids,
                             key="selected_submission",
                             index=selected_submission_index,
                             format_func=lambda x: format_submission_title(x, submissions)
                             )

        st.sidebar.button("Logout", on_click=auth.logout)

        if not st.session_state["selected_submission"]:
            st.subheader("You weren't assigned any applications.")
            st.text("Please try again later.")

        else:
            selected_submission = st.session_state.selected_submission
            evaluation_result = db.evaluations.getByQuery({"Submission ID": selected_submission})
            application_result = db.applications.getByQuery({"Submission ID": selected_submission})

            if evaluation_result and application_result:
                evaluation = evaluation_result[0]
                application = application_result[0]
                render_page(
                    submission_id=selected_submission,
                    screener_nr=submissions[selected_submission][0],
                    completed=submissions[selected_submission][1],
                    evaluation=evaluation,
                    application=application,
                    questions=questions,
                    links=links
                )

            else:
                st.error("Error loading application. Please try again.")


if __name__ == '__main__':
    main()
