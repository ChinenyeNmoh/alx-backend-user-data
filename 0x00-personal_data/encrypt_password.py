#!/usr/bin/env python3
""" Module named encrypt_password """
import bcrypt


def hash_password(password: str) -> bytes:
    """ Implement a function that expects one string argument
        name password and returns a salted, hashed password,
        which is a byte string.
    """
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Function to check valid password """
    hashed = bcrypt.checkpw(password.encode("utf-8"), hashed_password)
    return hashed
