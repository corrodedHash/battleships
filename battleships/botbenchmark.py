"""Contains random shit to benchmarks the bots"""
from typing import Type

from .bot import MarginBot, CheckerBot
from .bot import DefenderBot, OneWayGround, BaseBot
from .bot.randombot import place_ships_random
from .management.field import Field
from .util import Size


def benchbot(offensivebotclass: Type[BaseBot]) -> int:
    """Create a ground with a marginbot attacker and play"""
    attacker = offensivebotclass(Field(Size(10, 10)))
    defender_field = Field(Size(10, 10))
    defender_ships = place_ships_random(defender_field)
    defender = DefenderBot(defender_field, defender_ships)
    ground = OneWayGround(attacker, defender)

    while not ground.tick():
        pass
    return ground.tick_count


def main() -> None:
    """Run the benchmarks"""
    for botclass in (CheckerBot, MarginBot):
        results = []
        print(botclass.__name__)
        print("[", end="")
        for _ in range(20):
            results.append(benchbot(botclass))
            print(str(results[-1]) + ", ", end="", flush=True)
        print()
        print(sorted(results))


if __name__ == "__main__":
    main()
