from typing import Union, Dict

from bson import ObjectId

from entities.mongodb import mdb_select, mdb_insert, mdb_update


class Question:
    instances: Dict[str, 'Question'] = {}

    def __init__(self, text: str, q_type: str):
        self.text: str = text
        self.type: str = q_type
        self.is_active: bool = False
        self.id: str = self.__class__._insert(self)
        self.__class__.instances[self.id] = self

    @classmethod
    def _insert(cls, question: 'Question') -> str:
        return mdb_insert('question', question.convert_into_dict())

    def convert_into_dict(self) -> Dict[str, str]:
        return {
            'text': self.text,
            'type': self.type,
            'is_active': self.is_active
        }

    @classmethod
    def load_all(cls):
        questions = mdb_select('question')
        for q in questions:
            question = cls._convert_dict_into_question(q)
            cls.instances[question.id] = question

    @classmethod
    def get_instance(cls, entity_id: str) -> Union[None, 'Question']:
        if entity_id in cls.instances:
            return cls.instances[entity_id]
        return None

    @classmethod
    def _convert_dict_into_question(cls, q: Dict[str, str]) -> 'Question':
        question = cls.__new__(cls)
        question.id = q["_id"]
        question.text = q['text']
        question.type = q['type']
        question.is_active = bool(q['is_active'])
        return question

    def active(self):
        self.is_active = True
        mdb_update('game', {'is_active': True},
                   {'_id': ObjectId(self.id)})
