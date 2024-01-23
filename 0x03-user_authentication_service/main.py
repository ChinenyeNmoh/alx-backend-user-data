#!/usr/bin/env python3
"""
Main file
"""
from http import cookies
import requests
from auth import Auth

AUTH = Auth()
URL = 'http://127.0.0.1:5000'


def register_user(email: str, password: str) -> None:
    """ test to register user route """
    r = requests.post(URL + '/users', data={
        'email': email,
        'password': password})
    assert r.status_code == 200
    assert r.json() == {
        'email': email,
        'message': 'user created'}


def log_in_wrong_password(email: str, password: str) -> None:
    """ test to log in wrong password """
    r = requests.post(URL + '/sessions', data={
        'email': email,
        'password': password})
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """ test to correct login """
    r = requests.post(URL + '/sessions', data={
        'email': email,
        'password': password})
    assert r.status_code == 200
    assert r.json() == {
            'email': email,
            'message': 'logged in'}
    assert r.cookies.get('session_id')


def profile_unlogged() -> None:
    """ test to profile unlogged """
    r = requests.get(URL + '/profile')
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    """ test to profile logged """
    r = requests.get(URL + '/profile', cookies={
        'session_id': session_id
    })
    user_session = AUTH.get_user_from_session_id(session_id)
    assert r.status_code == 200
    assert r.json() == {'email': user_session.email}


def log_out(session_id: str) -> None:
    """ test to log out session """
    r = requests.delete(URL + '/sessions', cookies={
        'session_id': session_id})
    for resp in r.history:
        assert resp.status_code == 302


def reset_password_token(email: str) -> str:
    """ test to reset password token """
    r = requests.post(URL + '/reset_password', data={
        'email': email})
    user_session = AUTH._db.find_user_by(email=email)
    assert r.status_code == 200
    assert r.json() == {
        'email': email,
        'reset_token': user_session.reset_token}
    return user_session.reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ test to update password """
    r = requests.put(URL + '/reset_password', data={
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password})
    assert r.status_code == 200
    assert r.json() == {'email': email, 'message': 'Password updated'}


EMAIL = "Chinenyeumeaku@gmail.com"
PASSWD = "testing1"
NEW_PASSWD = "testing2"


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
