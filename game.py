from datetime import datetime
from typing import Callable, Tuple, List

from database import db_insert, db_select, Entity
from strings import strings
from user import MyUser

MINIMUM_MEMBER = 2
game_strings = strings.game


class Game(Entity):
    def __init__(self, inviter: MyUser):

        self.inviter = inviter
        self.is_active = 1
        self.created_at = datetime.now()
        self.deleted_at = None
        self.members: List[MyUser] = []

        self.game_id = self.__class__._insert(self)
        self.__class__.instances[self.game_id] = self
        print("game created: ", self)

    @classmethod
    def _insert(cls, game: 'Game') -> int:
        columns = ('inviter_id', 'is_active', 'created_at')
        values = (game.inviter.id, game.is_active, game.created_at)
        return db_insert('game', columns, values)

    @classmethod
    def load_all(cls):
        game_tuples: List[Tuple] = db_select('game')

        for t in game_tuples:
            game = cls._convert_tuple(t)
            if game.deleted_at or game.is_active == 0:
                continue
            members: List[Tuple] = db_select('member', where_clause='game_id=' + str(game.game_id))
            game.members = members
            cls.instances[game.game_id] = game

        print(cls.instances)

    @classmethod
    def _convert_tuple(cls, t: Tuple[str, str, str, str, str]) -> 'Game':
        game = cls.__new__(cls)
        game.game_id = t[0]
        game.inviter_id = t[1]
        game.is_active = t[2]
        game.created_at = t[3]
        game.deleted_at = t[4]
        return game

    def add_member(self, member_id):
        self.members.append(member_id)
        columns = ('game_id', 'member_id')
        values = (self.game_id, member_id)
        db_insert('member', columns, values)

    def start(self, starter_id: str, alert: Callable[[str], None]):
        if starter_id != self.inviter.id:
            alert(game_strings.alert.start_non_inviter)
        if len(self.members) < MINIMUM_MEMBER:
            alert(game_strings.alert.start_minimum)

        # todo

    def get_in(self, user_id: str, alert: Callable[[str], None]):
        if user_id in self.members:
            alert(game_strings.alert.already_got_in)
            return
        self.add_member(user_id)
        alert(game_strings.alert.successfully_got_in)
        # todo edit message
