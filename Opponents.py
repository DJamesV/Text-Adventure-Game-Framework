from termcolor.termcolor import colored
from commonMessages import displayText, printSystem
import random

def displayStats(op, color):
    print(colored(f"\n{op.name}:\n", color))
    print(colored(f"     HP: {op.hp}/{op.maxHp}", color))
    print(colored(f"     ATK: {op.atk}", color))
    print(colored(f"     DFN: {op.dfn}", color))
    print(colored(f"     SPD: {op.spd}", color))
    print(colored(f"     LVL: {op.lvl}", color))
    print(colored(f"     EXP: {op.exp}", color))

class Telephone():

    def __init__(self):
        self.isDefending = False
        self.isFirst = False

        self.name = "Telephone"
        self.maxHp = 10
        self.hp = 10
        self.atk = 1
        self.dfn = 2
        self.spd = 2
        self.lvl = 1
        self.exp = 100

        self.pAtk = 0.8
        self.pDfn = 0.2

    def getActionName(self):
        actions = ["atk", "dfn"]
        probabilities = [self.pAtk, self.pDfn]

        chosen = random.choices(actions, weights=probabilities, k=1)[0]
        if chosen == "atk":
            return "Attack"
        elif chosen == "dfn":
            return "Defend"

    def updateHp(self, hpMod):
        self.hp += hpMod
        self.hp = max(0, self.hp)

    def updateStats(self, hpMod, atkMod):
        self.hp += hpMod
        self.hp = max(0, self.hp)
        self.atk += atkMod