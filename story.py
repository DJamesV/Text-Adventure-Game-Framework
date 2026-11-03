from common_classes import *
from custom import Aspect, Favor
from state import People, Places, Routes, Scenes, player

start_here = Switch(SwitchToTypes.Scene, "intro")


def main(player_name: str = ""):
    People["System"] = Person("???", speechColor="light_grey") # Narrator
    player_name = player_name.strip()
    if not player_name: # If the character does not have a pre-set name, ask.
        Display(
            "WHAT IS YOUR NAME?:n:SPEAK, HUMAN.",
            speaker=People["System"],
            lull=False,
        ).do(None, None)
        player_name = TakesInput().get_user_input().strip() or "Human"

    player.name = player_name

    Scenes["intro"] = Scene(
        [
            Display(f"GREETINGS, {player.name.upper()}.", speaker=People["System"]),
            Display(
                "Three feelings wait at the edge of the dark. Which one do you take?",
                lull=False,
            ),
            Choice(
                thingsToDo=[
                    [
                        Display(
                            "You let sorrow in.",
                            lull=False,
                        ),
                        Favor(Aspect.SORROW),
                    ],
                    [
                        Display(
                            "You take anger by the hand.",
                            lull=False,
                        ),
                        Favor(Aspect.ANGER),
                    ],
                    [
                        Display(
                            "You choose happiness.",
                            lull=False,
                        ),
                        Favor(Aspect.HAPPINESS),
                    ],
                    [
                        Display("You refuse all three. The dark does not mind.", lull=False,),
                        Display("You walk on with no aspect at all."),
                    ],
                ],
                textToDisplay="Which aspect answers?",
                toDoDisplayText=[
                    "Sorrow",
                    "Anger",
                    "Happiness",
                    "Refuse them all",
                ],
            ),
        ]
    )
