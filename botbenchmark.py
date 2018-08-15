"""Contains random shit to benchmarks the bots"""
from typing import Type

from bot import MarginBotOffensive, CheckerBotOffensive
from bot import RandomBotDefensive, OneWayGround, BaseBotOffensive
from management.field import Field
from util import Size


def benchbot(OffensiveBotClass: Type[BaseBotOffensive]) -> int:
    """Create a ground with a marginbot attacker and play"""
    attacker = OffensiveBotClass(Field(Size(10, 10)))
    defender = RandomBotDefensive(Field(Size(10, 10)))
    ground = OneWayGround(attacker, defender)

    while not ground.tick():
        pass
    return ground.tick_count


def main() -> None:
    """Run the benchmarks"""
    for BotClass in (CheckerBotOffensive, MarginBotOffensive):
        results = []
        print(BotClass.__name__)
        print("[", end="")
        for _ in range(20):
            results.append(benchbot(BotClass))
            print(str(results[-1]) + ", ", end="", flush=True)
        print()
        print(sorted(results))


if __name__ == "__main__":
    main()
