from typing import Tuple, List, Union, Dict

from entities.database import db_select, db_insert, db_update


class MyUser:
    instances: Dict[int, 'MyUser'] = {}

    def __init__(self):
        self.id = None
        self.name = None
        raise NotImplementedError()

    @classmethod
    def new(cls, user_id: int, name: str) -> 'MyUser':
        instance = cls.get_instance(user_id)
        if not instance:
            user = cls.__new__(cls)
            user.id = user_id
            user.name = name
            cls._insert(user)
            return user
        elif instance.name != name:
            instance.update(name)
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
    def get_instance(cls, entity_id: int) -> Union[None, 'MyUser']:
        if int(entity_id) in cls.instances:
            return cls.instances[int(entity_id)]
        return None
