import datetime
from typing import List, Union, Tuple, Optional

import mysql.connector
from decouple import config

mydb = mysql.connector.connect(
    host=config("DB_HOST"),
    user=config("DB_USER"),
    password=config("DB_PASS"),
    database=config("DB_SCHEMA")
)

cursor = mydb.cursor()


def join(ll: Union[Tuple, List]):
    return ', '.join(map(str, ll))


def join_values(ll: Tuple):
    new_list = ['%s' for i in ll]
    return join(new_list)


def insert(table_name: str, column_names: Tuple, values: Union[Tuple, List[Tuple]]) -> int:
    sql = "INSERT INTO {} ({}) VALUES ({})".format(table_name, join(column_names), join_values(values))
    cursor.execute(sql, values)
    mydb.commit()
    return cursor.lastrowid


def select(table_name: str, column_names: Optional[Tuple] = None) -> List:
    column_names2 = join(column_names) if column_names else '*'
    sql = "SELECT {} FROM {}".format(column_names2, table_name)
    cursor.execute(sql)
    return cursor.fetchall()
