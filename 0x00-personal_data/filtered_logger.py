#!/usr/bin/env python3
"""" Module named filtered_logger """

import re
from typing import List
import logging
import mysql.connector
import os


# # PII fields to be redacted
PII_FIELDS = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Constructor
        """
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """
        format function
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Function that returns the log message obfuscated
    """
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    """
    get_logger function
    source: https://realpython.com/python-logging/
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    c_handler = logging.StreamHandler()
    c_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(c_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    get_db function
    """
    username = os.getenv("PERSONAL_DATA_DB_USERNAME")
    password = os.getenv("PERSONAL_DATA_DB_PASSWORD")
    host = os.getenv("PERSONAL_DATA_DB_HOST")
    database = os.getenv("PERSONAL_DATA_DB_NAME")
    return mysql.connector.connect(
            user=username,
            password=password,
            host=host,
            database=database
        )


def main():
    """
    main function
    """
    conn = get_db()
    users = conn.cursor()
    users.execute("SELECT CONCAT('name=', name, ';ssn=', ssn, ';ip=', ip, \
        ';user_agent', user_agent, ';') AS message FROM users;")
    formatter = RedactingFormatter(fields=PII_FIELDS)
    logger = get_logger()

    for user in users:
        logger.log(logging.INFO, user[0])


if __name__ == "__main__":
    main()
