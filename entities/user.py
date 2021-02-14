from typing import Union, Dict

from bson import ObjectId

from entities.mongodb import mdb_select, mdb_insert, mdb_update


class MyUser:
    instances: Dict[str, 'MyUser'] = {}

    def __init__(self):
        self.id: str = ''
        self.name: str = ''
        raise NotImplementedError()

    @classmethod
    def new(cls, user_id: str, name: str) -> 'MyUser':
        instance = cls.get_instance(user_id)
        if not instance:
            user = cls.__new__(cls)
            user.id = user_id
            user.name = name
            cls._insert(user)
            return user
        elif instance.name != name:
            instance.update(name)
        return instance

    def update(self, new_name: str):
        self.name = new_name
        mdb_update('user', {'name': self.name}, {'_id': ObjectId(self.id)})

    @classmethod
    def _insert(cls, user: 'MyUser') -> str:
        id_ = mdb_insert('user', user.convert_into_dict())
        cls.instances[str(id_)] = user
        return id_

    @classmethod
    def load_all(cls):
        users = mdb_select('user')
        for u in users:
            user = cls._convert_dict_into_user(u)
            cls.instances[user.id] = user

    @classmethod
    def _convert_dict_into_user(cls, d: Dict[str, any]) -> 'MyUser':
        user = cls.__new__(cls)
        user.id = str(d["_id"])
        user.name = d["name"]
        return user

    def convert_into_dict(self) -> Dict[str, str]:
        return {
            '_id': self.id,
            'name': self.name
        }

    @classmethod
    def get_instance(cls, entity_id: str) -> Union[None, 'MyUser']:
        entity_id = str(entity_id)
        if entity_id in cls.instances:
            return cls.instances[entity_id]
        return None
