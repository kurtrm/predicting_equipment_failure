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


def fetch_all_threshold() -> tuple:
    """
    Get all the data from the threshold table (1 row)
    """
    conn = pg2.connect(**my_params)
    cur = conn.cursor()
    cur.execute('SELECT * FROM threshold;')
    fetched = cur.fetchone()
    conn.close()

    return fetched


def select_threshold() -> tuple:
    """
    Get the threshold value from the threshold table.
    """
    conn = pg2.connect(**my_params)
    cur = conn.cursor()
    cur.execute('SELECT threshold FROM threshold;')
    fetched = cur.fetchone()
    conn.close()

    return fetched


def fetch_test_data() -> List[tuple]:
    """
    Fetch all test set data to perform cost benefit
    calculations.
    """
    conn = pg2.connect(**my_params)
    cur = conn.cursor()
    cur.execute('SELECT * FROM testset;')
    fetched = cur.fetchall()
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


def update_threshold(threshold: float,
                     cost: int,
                     revenue: float,
                     maintenance: float,
                     repair: float) -> None:
    """
    Update the threshold value in the database.
    This function also updates the time at which the change was made.
    """
    conn = pg2.connect(**my_params)
    cur = conn.cursor()
    joined_args = ','.join(['%s'] * 5)  # 5 args to the statement
    format_chunk = f' = ({joined_args}, NOW()) WHERE id = 1;'
    update_statement = ('UPDATE threshold'
                        ' SET (threshold, cost, revenue, maintenance, repair, time_of_change)' +
                        format_chunk)
    cur.execute(update_statement, (threshold,
                                   cost,
                                   revenue,
                                   maintenance,
                                   repair))
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


def fetch_map_data() -> None:
    """
    Get all the map data to display on the map.
    """
    conn = pg2.connect(**my_params)
    cur = conn.cursor()
    cur.execute('SELECT * FROM latlong;')
    fetched = cur.fetchall()
    conn.close()

    return fetched
