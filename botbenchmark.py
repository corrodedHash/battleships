"""Contains random shit to benchmarks the bots"""
import bot.marginbot
import bot.checkerbot
import bot.randombot
import bot.grounds
from management.field import Field
from util import Size


def margin_bench():
    """Create a ground with a marginbot attacker and play"""
    attacker = bot.marginbot.MarginBotOffensive(Field(Size(10, 10)))
    defender = bot.randombot.RandomBotDefensive(Field(Size(10, 10)))
    ground = bot.grounds.OneWayGround(attacker, defender)

    while not ground.tick():
        # input()
        # print(attacker.enemy_field.print_table())
        pass
    return ground.tick_count


def checker_bench():
    """Create a ground with a checkerbot attacker and play"""
    attacker = bot.checkerbot.CheckerBotOffensive(Field(Size(10, 10)))
    defender = bot.randombot.RandomBotDefensive(Field(Size(10, 10)))
    ground = bot.grounds.OneWayGround(attacker, defender)

    while not ground.tick():
        print("\033[1;1H")
        print(attacker.enemy_field.print_table())
        input()
    return ground.tick_count


def main():
    """Run the benchmarks"""
    results = []
    for _ in range(10):
        results.append(checker_bench())
        print(results[-1])

    print(sorted(results))
    results = []
    for _ in range(10):
        results.append(margin_bench())
        print(results[-1])

    print(sorted(results))


checker_bench()
