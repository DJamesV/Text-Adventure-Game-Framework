from termcolor import colored, cprint

from PlayerClass import Player
from commonMessages import printSystem, displayText
from Opponents import Telephone
from Opponents import displayStats

player = Player("Fallen", "light_grey")

# These functions handle the combat actions
def basicAttackFunc(attacker, defender):
    if defender.isDefending:
        print(colored(f"{attacker.name} attempts to attack {defender.name}, but it's blocked!", player.playerColor))
    else:
        print(colored(f"\n{attacker.name} attacks {defender.name} and deals {attacker.atk} damage!", player.playerColor))
        defender.updateHp(-attacker.atk)

def defendFunc(attacker, op):
    print(colored(f"\n{attacker.name} braces for the next attack.", player.playerColor))
    attacker.isDefending = True
    if op.isDefending or op.isFirst:
        print(colored(f"... And does so too slowly!", player.playerColor))

def fullHealFunc(attacker):
    print(colored(f"\n{attacker.name} uses Full Heal!", player.playerColor))
    attacker.updateHp(attacker.maxHp)

# This function executes the action based on the action name
def executeAction(actionName, attacker, defender):
    if actionName == "Attack":
        basicAttackFunc(attacker, defender)
    elif actionName == "Defend":
        defendFunc(attacker, defender)
    elif actionName == "Full Heal":
        fullHealFunc(attacker)
    else:
        printSystem(f"Unknown action: {actionName}")

def runCombat(op):
    opAlive = True
    opponentAction = ""
    playerAction = ""

    playerFirst = True

    printSystem(f"\nYou have encountered a(n) {op.name}!")

    if player.spd >= op.spd:
        playerFirst = True
        player.isFirst = True
        op.isFirst = False
    else:
        playerFirst = False
        player.isFirst = False
        op.isFirst = True

    while opAlive:
        displayStats(op, player.playerColor)
        player.displayStats()
        print("")

        playerAction = player.getActionName()
        opponentAction = op.getActionName()

        if playerFirst:
            executeAction(playerAction, player, op)
            executeAction(opponentAction, op, player)
        else:
            executeAction(opponentAction, op, player)
            executeAction(playerAction, player, op)
        
        player.isDefending = False
        op.isDefending = False

        if op.hp <= 0:
            print("")
            printSystem(f"{op.name} has been defeated!")
            player.updateExp(op.exp)
            print(colored("\n     You have won the combat! Here are your final stats:", "light_magenta"))
            player.displayStats()
            opAlive = False

            again = input(colored("\n> ", "light_green"))
            if again == "again":
                op.hp = op.maxHp
                runCombat(op)

        if player.hp <= 0:
            opAlive = False
            printSystem(f"\n\n{op.name} has defeated you! Here are your final stats:")
            player.displayStats()

            again = input(colored("\n> ", "light_green"))
            if again == "again":
                op.hp = op.maxHp
                runCombat(op)

runCombat(Telephone())