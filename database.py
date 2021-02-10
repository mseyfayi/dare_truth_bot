from abc import ABC
from typing import List, Union, Tuple, Optional, Dict

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


def db_insert(table_name: str, column_names: Tuple, values: Union[Tuple, List[Tuple]]) -> int:
    sql = "INSERT INTO {} ({}) VALUES ({})".format(table_name, join(column_names), join_values(values))
    print("insert: ", sql)
    cursor.execute(sql, values)
    mydb.commit()
    return cursor.lastrowid


def db_update(table_name: str, column_value: Tuple[str, str], where_clause: str):
    sql = "UPDATE {} SET {}={} WHERE {}".format(table_name, column_value[0], column_value[1], where_clause)
    print("update: ", sql)
    cursor.execute(sql)
    mydb.commit()


def db_select(table_name: str, column_names: Optional[Tuple] = None, where_clause: Optional[str] = None) -> List[Tuple]:
    column_names2 = join(column_names) if column_names else '*'
    sql = "SELECT {} FROM {}".format(column_names2, table_name)
    if where_clause:
        sql += " WHERE " + where_clause
    print("select: ", sql)
    cursor.execute(sql)
    return cursor.fetchall()


class Entity(ABC):
    instances: Dict[int, 'Entity'] = {}

    @classmethod
    def _insert(cls, game: 'Entity') -> int:
        pass

    @classmethod
    def load_all(cls):
        pass

    @classmethod
    def _convert_tuple(cls, t: Tuple) -> 'Entity':
        pass

    @classmethod
    def get_instance(cls, entity_id: int) -> Union[None, 'Entity']:
        if int(entity_id) in cls.instances:
            return cls.instances[int(entity_id)]
        return None
