from termcolor import colored, cprint
import random

from PlayerClass import Player
from Opponents import Telephone

def updatePlayerLevel(op):
    player.exp += op.exp
    if player.exp >= player.maxExp:
        player.lvl += 1
        player.maxExp *= 2
        player.exp = 0
        print(f"\nCongratulations! You leveled up to level {player.lvl}!")

player = Player("Sorrow", "light_blue")

def enterCombat(op):
    opAlive = True

    print(f"Name: {op.name}")
    print(f"Health: {op.hp}")
    print(f"Attack: {op.atk}")

    while opAlive:
        print(f"\nCurrent Health: {op.hp}/{op.maxHp}")
        print("\nYour options:" \
        "\n\n     [1] Attack")
        action = input(f"{colored("\n> ", "light_green")}")
        if action == "1":
            op.updateStats(-player.atk, 0)
        if op.hp == 0:
            updatePlayerLevel(op)
            print(f"\nYou defeated the {op.name}!")
            opAlive = False

print("Hey there! My name is KiTe, but you can just call me Ki." \
"\nI am a fully functional combat testing unit. You may select which" \
"\nentity you would like to brutally murder." \
"\n\nI mean- knock out. Tee hee ^^")

print("\n     [1] Telephone")

selection = input(f"{colored("\n> ", "light_green")}")

if selection == "1":
    enterCombat(Telephone())
else:
    quit()

