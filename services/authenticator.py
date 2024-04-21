import hashlib
import streamlit as st
from services import database as db


def login(user, password):
    salt = "FinOps is awesome!"
    hashed_password = hashlib.sha512((password + salt).encode("utf-8")).hexdigest()

    user_result = db.users.getByQuery({"Username": user, "Password": hashed_password})
    print(f"User result: {user_result}")

    if user_result:
        token = hashlib.sha512((user + password + salt).encode("utf-8")).hexdigest()
        print(f"Set token: {token}")
        db.users.updateByQuery({"Username": user}, {"Token": token})
        st.session_state["token"] = token
        return True, user_result[0]["Name"]

    return False, None


def logged_in():
    if "token" in st.session_state:
        token = st.session_state["token"]

        user_result = db.users.getByQuery({"Token": token})
        if user_result:
            return True, user_result[0]["Name"]

    return False, None


def logout():
    st.session_state.clear()



