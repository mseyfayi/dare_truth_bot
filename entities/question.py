from typing import List, Tuple, Union, Dict

from entities.database import db_select, db_insert


class Question:
    instances: Dict[int, 'Question'] = {}

    def __init__(self, text: str, q_type: str):
        self.text = text
        self.type = q_type
        self.id = self.__class__._insert(self)
        self.__class__.instances[self.id] = self

    @classmethod
    def _insert(cls, question: 'Question') -> int:
        columns = ('text', 'type')
        values = (question.text, question.type)
        return db_insert('question', columns, values)

    @classmethod
    def load_all(cls):
        q_tuples: List[Tuple] = db_select('question')

        for t in q_tuples:
            question = cls._convert_tuple(t)
            cls.instances[question.id] = question

    @classmethod
    def _convert_tuple(cls, t: Tuple[str, str, str]) -> 'Question':
        question = cls.__new__(cls)
        question.id = t[0]
        question.text = t[1]
        question.type = t[2]
        return question

    @classmethod
    def get_instance(cls, entity_id: int) -> Union[None, 'Question']:
        if int(entity_id) in cls.instances:
            return cls.instances[int(entity_id)]
        return None
