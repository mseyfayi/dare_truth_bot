import random
from datetime import datetime
from typing import Callable, Tuple, List, Optional, Union, Dict

from entities.database import db_insert, db_select, db_update
from entities.question import Question
from entities.user import MyUser
from strings import strings

MINIMUM_MEMBER = 2
game_strings = strings.game


class Game:
    instances: Dict[int, 'Game'] = {}

    def __init__(self, inviter: MyUser):
        self.inviter: MyUser = inviter
        self.turn: Optional[MyUser] = None
        self.is_active: int = 1
        self.created_at: datetime = datetime.now()
        self.deleted_at: Optional[datetime] = None
        self.members: List[MyUser] = [inviter]
        # user_id -> question_id
        self.member_questions: Dict[int, List[int]] = {}

        self.game_id = self.__class__._insert(self)
        self.__class__.instances[self.game_id] = self
        print("game created: ", self)

    @classmethod
    def _insert(cls, game: 'Game') -> int:
        columns1 = ('inviter_id', 'is_active', 'created_at')
        values1 = (game.inviter.id, game.is_active, game.created_at)
        game_id = db_insert('game', columns1, values1)

        columns2 = ('member_id', 'game_id')
        values2 = (game.inviter.id, game_id)
        db_insert('member', columns2, values2)

        return game_id

    @classmethod
    def _convert_tuple_member(cls, t: Tuple[str, str]) -> MyUser:
        return MyUser.new(int(t[0]), t[1])

    @classmethod
    def _fetch_members(cls, game_id: int) -> List[MyUser]:
        columns = ('id', 'name')
        join_table = ('user', 'id')
        table_join_id = 'member_id'
        select_result = db_select('member', column_names=columns, join_table_table_id=join_table,
                                  table_id_to_join=table_join_id, where_clause='game_id=' + str(game_id))
        return [cls._convert_tuple_member(m) for m in select_result]

    @classmethod
    def _fetch_member_questions(cls, game_id: int) -> Dict[int, List[int]]:
        columns = ('member_id', 'question_id')
        select_result = db_select('game_member_question', column_names=columns, where_clause='game_id=' + str(game_id))
        new_dict: Dict[int, List[int]] = {}
        for m in select_result:
            if new_dict[m[0]]:
                new_dict[m[0]].append(m[1])
            else:
                new_dict[m[0]] = []
        return new_dict

    @classmethod
    def load_all(cls):
        game_tuples: List[Tuple] = db_select('game')

        for t in game_tuples:
            game = cls._convert_tuple(t)
            if game.deleted_at or game.is_active == 0:
                continue
            members: List[MyUser] = cls._fetch_members(game.game_id)
            member_questions: Dict[int, List[int]] = cls._fetch_member_questions(game.game_id)
            game.members = members
            game.member_questions = member_questions
            cls.instances[game.game_id] = game

    @classmethod
    def _convert_tuple(cls, t: Tuple[str, str, str, str, str, str]) -> 'Game':
        game = cls.__new__(cls)
        game.game_id = t[0]
        inviter_id = t[1]
        game.inviter = MyUser.instances[int(inviter_id)]
        turn_id = t[2]
        game.turn = MyUser.instances[int(turn_id)] if turn_id else None
        game.is_active = t[3]
        game.created_at = t[4]
        game.deleted_at = t[5]
        return game

    def add_member(self, member: MyUser):
        self.members.append(member)
        columns = ('game_id', 'member_id')
        values = (self.game_id, member.id)
        db_insert('member', columns, values)

    def next_turn(self):
        self.turn = random.choice(self.members)
        db_update('game', ('turn_id', self.turn.id), 'id=' + str(self.game_id))

    def next_question(self) -> Question:
        turn_asked_questions = self.member_questions[self.turn.id]
        remained_questions: List[Question] = []
        for qid, value in Question.instances.items():
            if qid not in turn_asked_questions:
                remained_questions.append(value)
        next_q = random.choice(remained_questions)
        self.member_questions[self.turn.id].append(next_q.id)
        return next_q

    def start(self, starter_id: str, alert: Callable[[str], None], edit_game_inline: Callable[[], None]):
        if starter_id != self.inviter.id:
            alert(game_strings.alert.start_non_inviter)
        elif len(self.members) < MINIMUM_MEMBER:
            alert(game_strings.alert.start_minimum)
        else:
            self.next_turn()
            edit_game_inline()

    def get_in(self, user: MyUser, alert: Callable[[str], None], edit_game_inline: Callable[[], None]):
        if any(m.id == user.id for m in self.members):
            alert(game_strings.alert.already_got_in)
            return
        self.add_member(user)
        alert(game_strings.alert.successfully_got_in)
        edit_game_inline()

    def choose(self, user_id: int, alert: Callable[[str], None], edit_question: Callable[[MyUser, Question], None]):
        if self.turn.id != user_id:
            alert(game_strings.alert.not_ur_turn)
            return
        next_q: Question = self.next_question()
        edit_question(self.turn, next_q)

    def answer(self, user_id: int, alert: Callable[[str], None], edit_game_inline: Callable[[], None]):
        if self.turn.id != user_id:
            alert(game_strings.alert.not_ur_turn)
            return
        self.next_turn()
        edit_game_inline()

    @classmethod
    def get_instance(cls, entity_id: int) -> Union[None, 'Game']:
        if int(entity_id) in cls.instances:
            return cls.instances[int(entity_id)]
        return None
