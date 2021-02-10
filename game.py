from datetime import datetime
from typing import Callable, Dict, Tuple, List

from database import db_insert, db_select
from strings import strings

MINIMUM_MEMBER = 2
game_strings = strings.game


class Game:
    instances: Dict[int, 'Game'] = {}

    def __init__(self, inviter_id: str):
        self.inviter_id = inviter_id
        self.is_active = 1
        self.created_at = datetime.now()
        self.deleted_at = None
        self.members = []

        self.game_id = self.__class__.insert(self)
        self.__class__.instances[self.game_id] = self
        print("game created: ", self)

    @classmethod
    def insert(cls, game: 'Game') -> int:
        columns = ('inviter_id', 'is_active', 'created_at')
        values = (game.inviter_id, game.is_active, game.created_at)
        return db_insert('game', columns, values)

    @classmethod
    def load_all(cls):
        game_tuples: List[Tuple] = db_select('game')

        for t in game_tuples:
            game = cls.convert_tuple_to_game(t)
            if game.deleted_at or game.is_active == 0:
                continue
            members: List[Tuple] = db_select('member', where_clause='game_id=' + str(game.game_id))
            game.members = members
            cls.instances[game.game_id] = game

        print(cls.instances)

    @classmethod
    def convert_tuple_to_game(cls, t: Tuple[str, str, str, str, str]) -> 'Game':
        game = cls.__new__(cls)
        game.game_id = t[0]
        game.inviter_id = t[1]
        game.is_active = t[2]
        game.created_at = t[3]
        game.deleted_at = t[4]
        return game

    @classmethod
    def get_instance(cls, game_id: int):
        print("Games: ", cls.instances)
        return cls.instances[int(game_id)]

    def start(self, starter_id: str, alert: Callable[[str], None]):
        if starter_id != self.inviter_id:
            alert(game_strings.alert.start_non_inviter)
        if len(self.members) < MINIMUM_MEMBER:
            alert(game_strings.alert.start_minimum)

        # todo

    def get_in(self, ):
        pass
