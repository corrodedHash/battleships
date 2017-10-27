import bot.marginbot
import bot.randombot
import bot.grounds
from management.field import Field
from util import Size

def main():
    attacker = bot.marginbot.MarginBotOffensive(Field(Size(10, 10)))
    defender = bot.randombot.RandomBotDefensive(Field(Size(10, 10)))
    ground = bot.grounds.OneWayGround(attacker, defender)
    
    while True:
        print(attacker.enemy_field.print_table())
        ground.tick()
        input()
main()

