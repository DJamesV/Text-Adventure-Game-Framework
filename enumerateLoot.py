from termcolor import colored, cprint
import random

from commonMessages import printSystem

def enumerateLoot(lvl, hp, atk, items, color):
    printSystem("\n     You have gained:")
    print(colored(f"\n          - +{lvl} level(s)!" \
                  f"\n          - +{hp} health!" \
                  f"\n          - +{atk} attack!", f"{color}"))
    printSystem("\n     You have found:")
    for item in items:
        print(colored(f"\n          - {item}", f"{color}"))