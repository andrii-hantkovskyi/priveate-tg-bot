from datetime import date

import psycopg2
from monthdelta import monthdelta

from settings import DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT


def check_if_user_registered(user_id):
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor()

    cursor.execute(f"SELECT user_id from pass WHERE user_id={user_id}")
    try:
        user = cursor.fetchone()[0]
        return True
    except TypeError:
        return False


def clear_expire_date(user_id):
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor()

    cursor.execute(f"UPDATE pass SET pass_expires = NULL WHERE user_id={user_id}")
    connection.commit()


def get_all_subscribers_id() -> list[int]:
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor()

    cursor.execute("SELECT user_id FROM pass")
    subscribers_id = [i[0] for i in cursor.fetchall()]
    return subscribers_id


def check_for_pass(user_id):
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor()

    cursor.execute(f"SELECT has_pass FROM pass WHERE user_id={user_id}")
    has_pass: bool = cursor.fetchone()[0]

    return has_pass


def set_has_pass(user_id, has_pass):
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor()

    cursor.execute(f"UPDATE pass SET has_pass = {has_pass} WHERE user_id={user_id}")
    connection.commit()


def get_expire_date(user_id):
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor()

    cursor.execute(f"SELECT pass_expires FROM pass WHERE user_id={user_id}")
    return cursor.fetchone()[0] or date.today()


def add_user_to_db(user_id):
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor()

    cursor.execute(f"INSERT INTO pass(user_id, has_pass) VALUES ({user_id}, false)")
    connection.commit()


def add_months_for_pass(user_id, months):
    connection = psycopg2.connect(dbname=DB_NAME, user=DB_USERNAME, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT)
    cursor = connection.cursor()

    expire_date = get_expire_date(user_id)

    cursor.execute(f"UPDATE pass SET pass_expires = '{expire_date + monthdelta(months)}' WHERE user_id={user_id}")
    connection.commit()


if __name__ == '__main__':
    check_if_user_registered(54634124)
