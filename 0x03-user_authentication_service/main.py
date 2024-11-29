#!/usr/bin/env python3

import requests

""" End-to-end integration test
"""


def register_user(email: str, password: str) -> None:
    """ Tests register_user
    """
    register_user = {
        "email": email,
        "password": password
    }
    req = requests.post(f'{URL}/users', data=register_user)

    response = {"email": EMAIL, "message": "user created"}
    assert req.status_code == 200
    assert req.json() = response


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test logging in with wrong password
    """
    register_user = {
        "email": email,
        "password": password
    }
    req = requests.post(f'{URL}/sessions', data=register_user)

    assert req.status_code == 200


def log_in(email: str, password: str) -> str:
    """ Test log-in
    """
    register_user = {
        "email": email,
        "password": password
    }
    req = requests.post(f'{URL}/sessions', data=register_user)

    response = {"email": EMAIL, "message": "logged in"}
    assert req.status_code == 200
    assert req.json() = response
    return req.cookies.get("session_id")


def profile_unlogged() -> None:
    """ Test profile unlogged
    """
    req = requests.delete(f'{URL}/sessions')

    assert req.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Test profile logged
    """
    cookie = {
        "session_id": session_id
    }
    req = requests.get(f'{URL}/profile', cookies=cookie)

    response = {
        "email": EMAIL,
    }

    assert req.status_code == 200
    assert req.json() == response


def log_out(session_id: str) -> None:
    """ Test logout
    """
    cookie = {
        "session_id": session_id
    }
    req = requests.delete(f'{URL}/sessions', cookies=cookie)

    response = {
        "email": EMAIL,
    }

    assert req.status_code == 200


def reset_password_token(email: str) -> str:
    """ Test reset password
    """
    register_user = {
        "email": email
    }
    req = requests.post(f'{URL}/reset_password', data=register_user)

    reset_token = req.json().get('reset_token', None)
    response = {"email": email, "reset_token": reset_token}

    assert req.status_code == 200
    assert req.json() == response

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Test
    """
    register_user = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password,
    }
    req = requests.put(f'{URL}/reset_password', data=register_user)

    response = {"email": email, "message": "Password updated"}

    assert req.status_code == 200
    assert req.json() == response


URL = "http://localhost:5000"
EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
