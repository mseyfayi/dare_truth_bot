from typing import Callable
from uuid import UUID


class Game:
    instances = {}  # todo put in database

    def __init__(self, game_id: UUID, inviter_id: str):
        self.game_id = game_id
        self.inviter_id = inviter_id
        self.__class__.instances[game_id.hex] = self
        print("Game '{}' created by '{}'".format(game_id, inviter_id))

    @classmethod
    def get_instance(cls, game_id: UUID):
        print("Games: ", cls.instances)
        return cls.instances[game_id.hex]

    def start(self, starter_id: str, alert: Callable[[str], None]):
        if starter_id != self.inviter_id:
            alert("دعوت کننده میتونه شروع کنه فقط")

    def get_in(self, ):
        pass
