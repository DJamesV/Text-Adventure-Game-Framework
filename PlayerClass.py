from termcolor import colored

from CommonClasses import *  # noqa - Tighten imports once more polished


class Player:
    def __init__(self, name, playerColor):
        self.isDefending = False
        self.isFirst = False

        self.name = name
        self.playerColor = playerColor

        self.hp = 10
        self.maxHp = 10
        self.atk = 2
        self.spd = 3
        self.dfn = 1
        self.lvl = 1
        self.exp = 0
        self.maxExp = 100

        self.alignment = "none"

        self.playerAttacks = ["Basic Attack"]
        self.playerItems = [""]
        self.playerSpecials = ["Full Heal"]

        self.secrets = {}
        self.peopleMet = []
        self.placesBeen = []
        self.roadsTaveled = []
        self.inventory = {}

        self.happinessBP = 0
        self.angerBP = 0
        self.sorrowBP = 0

        if self.alignment == "none":
            self.playerColor = "light_grey"
        elif self.alignment == "anger":
            self.playerColor = "red"
            self.angerBP += 1
        elif self.alignment == "happiness":
            self.playerColor = "yellow"
            self.happinessBP += 1
        elif self.alignment == "sorrow":
            self.playerColor = "blue"
            self.sorrowBP += 1

    def updateStats(
        self, hpMod, maxHpMod, atkMod, spdMod, dfnMod, lvlMod, expMod, maxExpMod
    ):
        self.hp += hpMod
        self.maxHp += maxHpMod
        self.atk += atkMod
        self.spd += spdMod
        self.dfn += dfnMod
        self.lvl += lvlMod
        self.exp += expMod
        self.maxExp += maxExpMod

    def updateHp(self, hpMod):
        self.hp += hpMod
        self.hp = max(0, min(self.hp, self.maxHp))

    def updateExp(self, expMod):
        self.exp += expMod
        print("")
        if self.exp >= self.maxExp:
            self.levelUp(expMod)
        else:
            pass  # TODO: Fix this
            # printSystem(
            #     f"You gained {expMod} EXP! You now have {self.exp}/{self.maxExp} EXP and need {self.maxExp - self.exp} more to level up."
            # )

    def levelUp(self, expMod):
        self.lvl += 1
        self.maxExp *= 2
        self.exp = 0
        # TODO: Fix
        # printSystem(
        #     f"You gained {expMod} EXP! You now have {self.exp}/{self.maxExp} EXP and need {self.maxExp - self.exp} more to level up."
        # )
        # printSystem(f"Congratulations! You leveled up to level {self.lvl}!")

    def displayStats(self):
        print(colored(f"\n{self.name}:\n", self.playerColor))
        print(colored(f"     HP: {self.hp}/{self.maxHp}", self.playerColor))
        print(colored(f"     ATK: {self.atk}", self.playerColor))
        print(colored(f"     SPD: {self.spd}", self.playerColor))
        print(colored(f"     DFN: {self.dfn}", self.playerColor))
        print(colored(f"     LVL: {self.lvl}", self.playerColor))
        print(colored(f"     EXP: {self.exp}/{self.maxExp}", self.playerColor))

    def displayItmMenu(self):
        print(colored("\nWhich item will you use?\n", self.playerColor))

        lastSelection = 0

        # Displays the player's items
        for i, item in enumerate(self.playerItems, start=1):
            print(f"     [{i}] {item}")
            lastSelection = i + 1

        # Displays the option to go back
        print(f"     [{lastSelection}] BACK")

        # Gets the player's selection
        selectedNumber = input(f"{colored('\n> ', 'light_green')}")

        # Checks if the player wants to go back
        if selectedNumber == str(lastSelection):
            return self.getActionName()

        return self.playerItems[
            int(selectedNumber) - 1
        ]  # This returns the selected item name

    def displaySpMenu(self):
        print(colored("\nWhich special will you use?\n", self.playerColor))

        lastSelection = 0

        # Displays the player's specials
        for i, special in enumerate(self.playerSpecials, start=1):
            print(f"     [{i}] {special}")
            lastSelection = i + 1

        # Displays the option to go back
        print(f"     [{lastSelection}] BACK")

        # Gets the player's selection
        selectedNumber = input(f"{colored('\n> ', 'light_green')}")

        # Checks if the player wants to go back
        if selectedNumber == str(lastSelection):
            return self.getActionName()

        return self.playerSpecials[
            int(selectedNumber) - 1
        ]  # This returns the selected special name

    def getActionName(self):
        # Displays the player's options
        print(colored("\nWhat will you do?\n", self.playerColor))
        print("     [1] ATK")
        print("     [2] ITM")
        print("     [3] DEF")
        print("     [4] SP")

        # Gets the player's action
        playerAction = input(colored("\n> ", "light_green"))

        # Checks the player's action
        if playerAction == "1":
            return "Attack"
        elif playerAction == "2":
            return self.displayItmMenu()
        elif playerAction == "3":
            return "Defend"
        elif playerAction == "4":
            return self.displaySpMenu()
        # TODO: Fix
        # elif playerAction == "7":
        #     printSystem("\nNice number, but that doesn't do anything.")
        # else:
        #     printSystem("\nInvalid action.")

    def gainKnowledge(self, knowledge: Knowledge):  # noqa - Tighten imports
        print(f"    You realize that {colored(knowledge.knowledge, self.playerColor)}")

        self.secrets[knowledge.name] = knowledge.knowledge

    def gainItem(self, item):
        if item.aspect == "sorrow":
            colorToPrint = "blue"
        elif item.world == "anger":
            colorToPrint = "red"
        elif item.aspect == "happiness":
            colorToPrint = "yellow"
        else:
            colorToPrint = "light_grey"
        print(f" You have gained {colored(item.name, colorToPrint)}")
        self.inventory[item.name] = item

    # TODO: Decide if this stays here or goes elsewhere
    def enumerateLoot(self, lvl, hp, atk, items, color):
        pass
        # TODO: Fix
        # printSystem("\n     You have gained:")
        # print(
        #     colored(
        #         f"\n          - +{lvl} level(s)!"
        #         f"\n          - +{hp} health!"
        #         f"\n          - +{atk} attack!",
        #         f"{color}",
        #     )
        # )
        # printSystem("\n     You have found:")
        # for item in items:
        #     print(colored(f"\n          - {item}", f"{color}"))
