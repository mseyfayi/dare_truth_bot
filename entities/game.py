import random
from datetime import datetime
from typing import Callable, List, Optional, Union, Dict

from bson import ObjectId

from entities.mongodb import mdb_insert, mdb_select, mdb_update
from entities.question import Question
from entities.user import MyUser
from strings import strings

MINIMUM_MEMBER = 2
game_strings = strings.game


class Game:
    instances: Dict[str, 'Game'] = {}

    def __init__(self, inviter: MyUser):
        self.inviter: MyUser = inviter
        self.turn: Optional[MyUser] = None
        self.is_active: int = 1
        self.created_at: datetime = datetime.now()
        self.deleted_at: Optional[datetime] = None
        self.members: List[MyUser] = [inviter]
        # user_id -> question_id
        self.member_questions: Dict[str, List[str]] = {}

        self.id = self.__class__._insert(self)
        self.__class__.instances[self.id] = self
        print("game created: ", self)

    @classmethod
    def _insert(cls, game: 'Game') -> str:
        return mdb_insert('game', game.convert_into_dict())

    def convert_into_dict(self) -> Dict[str, str]:
        return {
            "inviter_id": self.inviter.id,
            'turn_id': self.turn.id if self.turn else None,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'deleted_at': self.deleted_at,
            'members': [x.id for x in self.members],
            'member_questions': self.member_questions,
        }

    @classmethod
    def load_all(cls):
        games = mdb_select('game')
        for g in games:
            game = cls._convert_dict_into_game(g)
            cls.instances[game.id] = game

    @classmethod
    def _convert_dict_into_game(cls, d: Dict[str, any]) -> 'Game':
        game = cls.__new__(cls)
        game.id = str(d['_id'])
        game.inviter = MyUser.instances[d['inviter_id']]
        game.turn = MyUser.instances[d['turn_id']] if d['turn_id'] else None
        game.members = [MyUser.instances[x] for x in d['members']]
        game.member_questions = d['member_questions']
        game.is_active = d['is_active']
        game.created_at = d['created_at']
        game.deleted_at = d['deleted_at']
        return game

    def add_member(self, member: MyUser):
        self.members.append(member)
        mdb_update('game', {'members': [m.id for m in self.members]}, {'_id': ObjectId(self.id)})

    def next_turn(self):
        self.turn = random.choice(self.members)
        mdb_update('game', {'turn_id': self.turn.id}, {'_id': ObjectId(self.id)})

    def next_question(self, q_type: str) -> Question:
        if self.turn.id not in self.member_questions:
            self.member_questions[str(self.turn.id)] = []

        turn_asked_questions = self.member_questions[str(self.turn.id)]

        remained_questions: List[Question] = [q for q in Question.instances.values()
                                              if q.type == q_type and q.id not in turn_asked_questions]
        next_q = random.choice(remained_questions)
        self.member_questions[str(self.turn.id)].append(next_q.id)
        mdb_update('game', {'member_questions': self.member_questions}, {'_id': ObjectId(self.id)})
        return next_q

    def init_member_question(self):
        for m in self.members:
            self.member_questions[m.id] = []

    def start(self, starter_id: str, alert: Callable[[str], None], edit_game_inline: Callable[[], None]):
        if starter_id != self.inviter.id:
            alert(game_strings.alert.start_non_inviter)
        elif len(self.members) < MINIMUM_MEMBER:
            alert(game_strings.alert.start_minimum)
        else:
            self.init_member_question()
            self.next_turn()
            edit_game_inline()

    def get_in(self, user: MyUser, alert: Callable[[str], None], edit_game_inline: Callable[[], None]):
        if any(m.id == user.id for m in self.members):
            alert(game_strings.alert.already_got_in)
            return
        self.add_member(user)
        alert(game_strings.alert.successfully_got_in)
        edit_game_inline()

    def choose(self, user_id: int, q_type: str, alert: Callable[[str], None],
               edit_question: Callable[[MyUser, Question], None]):
        if self.turn.id != user_id:
            alert(game_strings.alert.not_ur_turn)
            return
        next_q: Question = self.next_question(q_type)
        edit_question(self.turn, next_q)

    def answer(self, user_id: int, alert: Callable[[str], None], edit_game_inline: Callable[[], None]):
        if self.turn.id != user_id:
            alert(game_strings.alert.not_ur_turn)
            return
        self.next_turn()
        edit_game_inline()

    @classmethod
    def get_instance(cls, entity_id: str) -> Union[None, 'Game']:
        if entity_id in cls.instances:
            return cls.instances[entity_id]
        return None
