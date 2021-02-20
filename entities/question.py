from typing import Union, Dict, Optional

from bson import ObjectId

from entities.mongodb import mdb_select, mdb_insert, mdb_update, mdb_delete


class Question:
    instances: Dict[str, 'Question'] = {}

    def __init__(self, text: str, q_type: str, is_active: Optional[bool] = False):
        from admin_bot import call_new_question_event

        self.text: str = text
        self.type: str = q_type
        self.is_active: bool = is_active
        self.id: str = self.__class__._insert(self)
        call_new_question_event()
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
        question.id = str(q["_id"])
        question.text = q['text']
        question.type = q['type']
        question.is_active = bool(q['is_active'])
        return question

    def confirm(self):
        self.is_active = True
        mdb_update('question', {'is_active': str(True)},
                   {'_id': ObjectId(self.id)})

    def refuse(self):
        del self.__class__.instances[self.id]
        mdb_delete('question', {'_id': ObjectId(self.id)})
