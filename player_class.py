from termcolor import colored

from common_classes import *  # noqa - Tighten imports once more polished


class Player:
    def __init__(self, name, player_color):
        self.is_defending = False
        self.is_first = False

        self.name = name
        self.player_color = player_color

        self.hp = 10
        self.max_hp = 10
        self.atk = 2
        self.spd = 3
        self.dfn = 1
        self.lvl = 1
        self.exp = 0
        self.max_exp = 100

        self.alignment = "none"

        self.player_attacks = ["Basic Attack"]
        self.player_items = [""]
        self.player_specials = ["Full Heal"]

        self.secrets = {}
        self.people_met = []
        self.places_been = []
        self.roads_traveled = []
        self.inventory = {}

        self.happiness_bp = 0
        self.anger_bp = 0
        self.sorrow_bp = 0

        if self.alignment == "none":
            self.player_color = "light_grey"
        elif self.alignment == "anger":
            self.player_color = "red"
            self.anger_bp += 1
        elif self.alignment == "happiness":
            self.player_color = "yellow"
            self.happiness_bp += 1
        elif self.alignment == "sorrow":
            self.player_color = "blue"
            self.sorrow_bp += 1

    def updateStats(
        self,
        hp_mod,
        max_hp_mod,
        atk_mod,
        spd_mod,
        dfn_mod,
        lvl_mod,
        exp_mod,
        max_exp_mod,
    ):
        self.hp += hp_mod
        self.max_hp += max_hp_mod
        self.atk += atk_mod
        self.spd += spd_mod
        self.dfn += dfn_mod
        self.lvl += lvl_mod
        self.exp += exp_mod
        self.max_exp += max_exp_mod

    def updateHp(self, hp_mod):
        self.hp += hp_mod
        self.hp = max(0, min(self.hp, self.max_hp))

    def update_exp(self, exp_mod):
        self.exp += exp_mod
        print("")
        if self.exp >= self.max_exp:
            self.level_up(exp_mod)
        else:
            pass  # TODO: Fix this
            # printSystem(
            #     f"You gained {exp_mod} EXP! You now have {self.exp}/{self.max_exp} EXP and need {self.max_exp - self.exp} more to level up."
            # )

    def level_up(self, exp_mod):
        self.lvl += 1
        self.max_exp *= 2
        self.exp = 0
        # TODO: Fix
        # printSystem(
        #     f"You gained {exp_mod} EXP! You now have {self.exp}/{self.max_exp} EXP and need {self.max_exp - self.exp} more to level up."
        # )
        # printSystem(f"Congratulations! You leveled up to level {self.lvl}!")

    def display_stats(self):
        print(colored(f"\n{self.name}:\n", self.player_color))
        print(colored(f"     HP: {self.hp}/{self.max_hp}", self.player_color))
        print(colored(f"     ATK: {self.atk}", self.player_color))
        print(colored(f"     SPD: {self.spd}", self.player_color))
        print(colored(f"     DFN: {self.dfn}", self.player_color))
        print(colored(f"     LVL: {self.lvl}", self.player_color))
        print(colored(f"     EXP: {self.exp}/{self.max_exp}", self.player_color))

    def display_item_menu(self):
        print(colored("\nWhich item will you use?\n", self.player_color))

        last_selection = 0

        # Displays the player's items
        for i, item in enumerate(self.player_items, start=1):
            print(f"     [{i}] {item}")
            last_selection = i + 1

        # Displays the option to go back
        print(f"     [{last_selection}] BACK")

        # Gets the player's selection
        selected_number = input(f"{colored('\n> ', 'light_green')}")

        # Checks if the player wants to go back
        if selected_number == str(last_selection):
            return self.get_action_name()

        return self.player_items[
            int(selected_number) - 1
        ]  # This returns the selected item name

    def display_sp_menu(self):
        print(colored("\nWhich special will you use?\n", self.player_color))

        last_selection = 0

        # Displays the player's specials
        for i, special in enumerate(self.player_specials, start=1):
            print(f"     [{i}] {special}")
            last_selection = i + 1

        # Displays the option to go back
        print(f"     [{last_selection}] BACK")

        # Gets the player's selection
        selected_number = input(f"{colored('\n> ', 'light_green')}")

        # Checks if the player wants to go back
        if selected_number == str(last_selection):
            return self.get_action_name()

        return self.player_specials[
            int(selected_number) - 1
        ]  # This returns the selected special name

    def get_action_name(self):
        # Displays the player's options
        print(colored("\nWhat will you do?\n", self.player_color))
        print("     [1] ATK")
        print("     [2] ITM")
        print("     [3] DEF")
        print("     [4] SP")

        # Gets the player's action
        player_action = input(colored("\n> ", "light_green"))

        # Checks the player's action
        if player_action == "1":
            return "Attack"
        elif player_action == "2":
            return self.display_item_menu()
        elif player_action == "3":
            return "Defend"
        elif player_action == "4":
            return self.display_sp_menu()
        # TODO: Fix
        # elif player_action == "7":
        #     printSystem("\nNice number, but that doesn't do anything.")
        # else:
        #     printSystem("\nInvalid action.")

    def gain_knowledge(self, knowledge: Knowledge):  # noqa - Tighten imports
        print(f"    You realize that {colored(knowledge.knowledge, self.player_color)}")

        self.secrets[knowledge.name] = knowledge.knowledge

    def gain_item(self, item):
        if item.aspect == "sorrow":
            color_to_print = "blue"
        elif item.world == "anger":
            color_to_print = "red"
        elif item.aspect == "happiness":
            color_to_print = "yellow"
        else:
            color_to_print = "light_grey"
        print(f" You have gained {colored(item.name, color_to_print)}")
        self.inventory[item.name] = item

    # TODO: Decide if this stays here or goes elsewhere
    def enumerate_loot(self, lvl, hp, atk, items, color):
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
