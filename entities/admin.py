import hashlib
from typing import Dict, List

from decouple import config

from entities.mongodb import mdb_select, mdb_insert


class Admin:
    instances_list: List['Admin'] = []

    def __init__(self, chat_id: str, password: str):
        if hashlib.md5(password.encode()) != config("ADMIN_PASSWORD"):
            raise PermissionError()
        self.chat_id: str = chat_id
        self.id = self.__class__._insert(self)

    @classmethod
    def _insert(cls, admin: 'Admin') -> str:
        id_ = mdb_insert('admin', admin.convert_into_dict())
        cls.instances_list.append(admin)
        return id_

    @classmethod
    def load_all(cls):
        admins = mdb_select('admin')
        for a in admins:
            admin = cls._convert_dict_into_user(a)
            cls.instances_list.append(admin)

    @classmethod
    def _convert_dict_into_user(cls, a: Dict[str, any]) -> 'Admin':
        admin = cls.__new__(cls)
        admin.id = str(a['_id'])
        admin.chat_id = str(a['chat_id'])
        admin.password = str(a['password'])
        return admin

    def convert_into_dict(self) -> Dict[str, str]:
        return {
            '_id': self.id,
            'chat_id': self.chat_id,
        }
