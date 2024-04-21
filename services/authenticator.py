import hashlib

import streamlit as st
from streamlit_cookies_controller import CookieController
from services import database as db

controller = CookieController()


def login(user, password):
    salt = "FinOps is awesome!"
    hashed_password = hashlib.sha512((password + salt).encode("utf-8")).hexdigest()

    user_result = db.users.getByQuery({"Username": user, "Password": hashed_password})
    if user_result:
        token = hashlib.sha512((user + password + salt).encode("utf-8")).hexdigest()
        db.users.updateByQuery({"Username": user}, {"Token": token})
        controller.set("token", token)
        return True, user_result[0]["Name"]

    return False, None


def logged_in():
    cookies = controller.getAll()

    if "token" in cookies:
        token = cookies["token"]

        user_result = db.users.getByQuery({"Token": token})
        if user_result:
            return True, user_result[0]["Name"]

    return False, None


def logout():
    st.session_state.clear()
    controller.remove("token")



