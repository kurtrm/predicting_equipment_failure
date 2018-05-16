"""
File that contains various SQL commands via psycopg2.
"""
import os

from typing import List

import psycopg2 as pg2


my_params = {'dbname': os.environ['DB_NAME'],
             'user': os.environ['DB_USERNAME'],
             'password': os.environ['DB_PASSWORD'],
             'host': os.environ['DB_HOST'],
             'port': os.environ['DB_PORT']}


def select_threshold() -> tuple:
    """
    Get the threshold value from the treshold table.
    """
    conn = pg2.connect(**my_params)
    cur = conn.cursor()
    cur.execute('SELECT value FROM threshold;')
    fetched = cur.fetchone()
    conn.close()

    return fetched


def get_profit_curve_data() -> List[tuple]:
    """
    Get all the data from the profit curve table.
    """
    conn = pg2.connect(**my_params)
    cur = conn.cursor()
    cur.execute('SELECT * FROM profit_curve;')
    fetched = cur.fetchall()
    conn.close()

    return fetched


def get_roc_data() -> List[tuple]:
    """
    Retrieve all the data from the rocdata table.
    """
    conn = pg2.connect(**my_params)
    cur = conn.cursor()
    cur.execute('SELECT * FROM rocdata;')
    fetched = cur.fetchall()
    conn.close()

    return fetched


def update_threshold(threshold: str) -> None:
    """
    Update the threshold value in the database.
    """
    conn = pg2.connect(**my_params)
    cur = conn.cursor()
    update_statement = 'UPDATE threshold SET value = %s WHERE id = 1;'
    cur.execute(update_statement, (float(threshold),))
    conn.commit()
    conn.close()


def purge_update_profit_curve(data: list) -> None:
    """
    Purge all the data from the profit curve table then
    insert new data.
    """
    conn = pg2.connect(**my_params)
    cur = conn.cursor()
    cur.execute('DELETE FROM profit_curve;')
    tupled_data = [(record['loss'], record['threshold'])
                   for record in data]
    format_str = ','.join(['%s'] * len(tupled_data))
    insert_statement = ('INSERT INTO profit_curve(loss, threshold)'
                        f'VALUES {format_str}')
    cur.execute(cur.mogrify(insert_statement, tupled_data))
    conn.commit()
    conn.close()
