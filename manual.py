import bot.marginbot
import bot.checkerbot
import bot.randombot
import bot.grounds
from management.field import Field
from util import Size
import os


def margin_bench():
    attacker = bot.marginbot.MarginBotOffensive(Field(Size(10, 10)))
    defender = bot.randombot.RandomBotDefensive(Field(Size(10, 10)))
    ground = bot.grounds.OneWayGround(attacker, defender)

    while not ground.tick():
        # input()
        # print(attacker.enemy_field.print_table())
        pass
    return ground.tick_count


def checker_bench():
    attacker = bot.checkerbot.CheckerBotOffensive(Field(Size(10, 10)))
    defender = bot.randombot.RandomBotDefensive(Field(Size(10, 10)))
    ground = bot.grounds.OneWayGround(attacker, defender)

    os.system("clear")
    while not ground.tick():
        print("\033[1;1H")
        print(attacker.enemy_field.print_table())
        input()
        pass
    return ground.tick_count


def main():
    results = []
    for i in range(10):
        results.append(checker_bench())
        print(results[-1])

    print(sorted(results))
    results = []
    for i in range(10):
        results.append(margin_bench())
        print(results[-1])

    print(sorted(results))


checker_bench()
