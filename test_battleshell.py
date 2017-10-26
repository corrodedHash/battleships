import unittest

import battleshell
import field


class BattleShellTest(unittest.TestCase):
    def test_standard(self):
        myshell = battleshell.BattleShell()
        myshell.do_init("10 10")
        myshell.do_hit("B4")
        self.assertEqual(myshell.field.cells[3][1], field.Field.States.hit)
        myshell.do_miss("C1")
        self.assertEqual(myshell.field.cells[0][2], field.Field.States.miss)
        myshell.do_reset("B4")
        self.assertEqual(myshell.field.cells[3][1], field.Field.States.empty)
        myshell.do_reset("J9")
        self.assertEqual(myshell.field.cells[8][9], field.Field.States.empty)
