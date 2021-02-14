from typing import Tuple, List, Union, Dict

from entities.database import db_select, db_insert, db_update


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
        else:
            return instance

    def update(self, new_name: str):
        self.name = new_name
        where_clause = 'id=' + str(self.id)
        db_update('user', ('name', new_name), where_clause)

    @classmethod
    def _insert(cls, user: 'MyUser') -> int:
        columns = ('id', 'name')
        values = (user.id, user.name)
        cls.instances[user.id] = user
        return db_insert('user', columns, values)

    @classmethod
    def load_all(cls):
        user_tuples: List[Tuple] = db_select('user')

        for t in user_tuples:
            user = cls._convert_tuple(t)
            cls.instances[user.id] = user

    @classmethod
    def _convert_tuple(cls, t: Tuple[str, str]) -> 'MyUser':
        user = cls.__new__(cls)
        user.id = t[0]
        user.name = t[1]
        return user

    @classmethod
    def get_instance(cls, entity_id: str) -> Union[None, 'MyUser']:
        if entity_id in cls.instances:
            return cls.instances[entity_id]
        return None

    def convert_into_dict(self) -> Dict[str, str]:
        return {
            '_id': self.id,
            'name': self.name
        }
