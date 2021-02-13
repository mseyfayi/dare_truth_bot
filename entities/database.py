from abc import ABC
from typing import List, Union, Tuple, Optional, Dict

import mysql.connector
from decouple import config

ignore_db = config("IGNORE_DB")


class AutoIncreaseId:
    instance: 'AutoIncreaseId' = None

    def __init__(self):
        self.auto_increase_id: int = 0
        raise NotImplementedError()

    def get_ai_id(self) -> int:
        temp = self.auto_increase_id
        self.auto_increase_id = temp + 1
        return temp

    @classmethod
    def get_instance(cls):
        return cls.instance


mydb = mysql.connector.connect(
    host=config("DB_HOST"),
    user=config("DB_USER"),
    password=config("DB_PASS"),
    database=config("DB_SCHEMA")
)

cursor = mydb.cursor()


def csv(ll: Union[Tuple, List]) -> str:
    return ', '.join(map(str, ll))


def csv4values(ll: Tuple) -> str:
    new_list = ['%s' for i in ll]
    return csv(new_list)


def join_clause(to_join: Tuple[str, str], table_name: str, table_id: str) -> str:
    return "{} JOIN {} ON {}.{} = {}.{}".format(table_name, to_join[0], table_name, table_id, to_join[0], to_join[1])


def db_insert(table_name: str, column_names: Tuple, values: Union[Tuple, List[Tuple]]) -> int:
    if ignore_db:
        return AutoIncreaseId.get_instance().get_ai_id()
    sql = "INSERT INTO {} ({}) VALUES ({})".format(table_name, csv(column_names), csv4values(values))
    print("insert: ", sql)
    cursor.execute(sql, values)
    mydb.commit()
    return cursor.lastrowid


def db_update(table_name: str, column_value: Tuple[str, str], where_clause: str):
    if ignore_db:
        return
    sql = "UPDATE {} SET {}={} WHERE {}".format(table_name, column_value[0], column_value[1], where_clause)
    print("update: ", sql)
    cursor.execute(sql)
    mydb.commit()


def db_select(
        table_name: str,
        column_names: Optional[Tuple] = None,
        where_clause: Optional[str] = None,
        join_table_table_id: Optional[Tuple[str, str]] = None,
        table_id_to_join: Optional[str] = None
) -> List[Tuple]:
    if ignore_db:
        return []
    column_names2 = csv(column_names) if column_names else '*'
    if join_table_table_id and table_id_to_join:
        from_clause = join_clause(join_table_table_id, table_name, table_id_to_join)
    else:
        from_clause = table_name
    sql = "SELECT {} FROM {}".format(column_names2, from_clause)
    if where_clause:
        sql += " WHERE " + where_clause
    print("select: ", sql)
    cursor.execute(sql)
    return cursor.fetchall()
