from typing import Callable


def start(starter_id: str, game_id: str, alert: Callable[[str], None]):
    print("in start function")
    if starter_id == "234681539":
        alert("وایستا دو دقیقه")
