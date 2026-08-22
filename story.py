from state import player, People, Places, Routes, Scenes
from common_classes import *

start_here = Switch(SwitchToTypes.Scene, "intro")


def main():
    player.name = "Test Human"

    People["System"] = Person("???", speechColor="light_grey")

    # Quick placeholder scene
    Scenes["intro"] = Scene(
        [
            Display("WHAT IS YOUR NAME?:n:SPEAK, HUMAN.", speaker=People["System"]),
            # Get some way to get the players name here.
            Display(f"GREETINGS, {player.name}"),
        ]
    )
