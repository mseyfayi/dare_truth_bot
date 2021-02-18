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
        self.question: Optional[Question] = None
        # user_id -> question_id
        self.member_questions: Dict[str, List[str]] = {}
        # for voting (List of User id)
        self.yes_list: List[MyUser] = []
        self.no_list: List[MyUser] = []

        self.id = self.__class__._insert(self)
        self.__class__.instances[self.id] = self
        print("game created: ", self)

    @classmethod
    def _insert(cls, game: 'Game') -> str:
        return mdb_insert('game', game.convert_into_dict())

    def convert_into_dict(self) -> Dict[str, str]:
        return {
            "inviter_id": str(self.inviter.id),
            'turn_id': self.turn.id if self.turn else None,
            'is_active': self.is_active,
            'created_at': self.created_at,
            'deleted_at': self.deleted_at,
            'question_id': self.question.id if self.question else None,
            'members': [x.id for x in self.members],
            'member_questions': self.member_questions,
            'yes_list': [x.id for x in self.yes_list],
            'no_list': [x.id for x in self.no_list],
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
        game.inviter = MyUser.get_instance(d['inviter_id'])
        game.turn = MyUser.get_instance(d['turn_id']) if d['turn_id'] else None
        game.members = [MyUser.get_instance(x) for x in d['members']]
        game.member_questions = d['member_questions']
        game.yes_list = [MyUser.get_instance(x) for x in d['yes_list']]
        game.no_list = [MyUser.get_instance(x) for x in d['no_list']]
        game.question = Question.get_instance(d['question_id']) if d['question_id'] else None
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

    def next_question(self, q_type: str):
        if str(self.turn.id) not in self.member_questions:
            self.member_questions[str(self.turn.id)] = []

        turn_asked_questions = self.member_questions[str(self.turn.id)]

        remained_questions: List[Question] = [q for q in Question.instances.values()
                                              if q.type == q_type and q.id not in turn_asked_questions]
        next_q = random.choice(remained_questions)
        self.member_questions[str(self.turn.id)].append(next_q.id)
        self.question = next_q
        mdb_update('game', {'member_questions': self.member_questions, 'question_id': self.question.id},
                   {'_id': ObjectId(self.id)})

    def init_member_question(self):
        for m in self.members:
            self.member_questions[m.id] = []

    def start(self, starter_id: str, alert: Callable[[str], None], edit_game_inline: Callable[[], None]):
        if str(starter_id) != str(self.inviter.id):
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

    def choose(self, user_id: str, q_type: str, alert: Callable[[str], None],
               edit_question: Callable[[], None]):
        if self.is_not_member(user_id, alert):
            return
        if str(self.turn.id) != str(user_id):
            alert(game_strings.alert.not_ur_turn)
            return
        self.next_question(q_type)
        edit_question()

    def answer(self, user_id: str, alert: Callable[[str], None], edit_game_inline: Callable[[], None]):
        if self.is_not_member(user_id, alert):
            return
        if str(self.turn.id) != str(user_id):
            alert(game_strings.alert.not_ur_turn)
            return
        edit_game_inline()

    def vote(self, user_id: str, result: str, alert: Callable[[str], None],
             edit_game_inline: Callable[[bool, bool], None]):
        if self.is_not_member(user_id, alert):
            return
        if str(user_id) == self.turn.id:
            alert(game_strings.alert.cannot_vote_ur_turn)
            return
        yes_list_id = [x.id for x in self.yes_list]
        no_list_id = [x.id for x in self.no_list]
        if str(user_id) in yes_list_id or user_id in no_list_id:
            alert(game_strings.alert.voted_before)
            return
        user = MyUser.get_instance(user_id)
        if result == "yes":
            self.yes_list.append(user)
        else:
            self.no_list.append(user)
        alert(game_strings.alert.vote_successful)
        is_voting_finished = len(self.yes_list) + len(self.no_list) == len(self.members) - 1
        is_repeated = is_voting_finished and len(self.yes_list) <= len(self.no_list)
        if is_voting_finished:
            self.yes_list = []
            self.no_list = []
        if is_voting_finished and not is_repeated:
            self.next_turn()

        edit_game_inline(is_voting_finished, is_repeated)

    def is_not_member(self, user_id: str, alert: Callable[[str], None] = None) -> bool:
        res = any(m.id == str(user_id) for m in self.members)
        if alert and not res:
            alert(game_strings.alert.ur_not_member)
        return not res

    @classmethod
    def get_instance(cls, entity_id: str) -> Union[None, 'Game']:
        if entity_id in cls.instances:
            return cls.instances[entity_id]
        return None
