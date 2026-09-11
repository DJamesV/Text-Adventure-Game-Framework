import sys

import story
from common_classes import (
    Display,
    GameException,
    QuitException,
    SwitchToTypes,
)
from state import People, Places, Routes, Scenes, player

story.main()


def goTo(switch, player):
    if switch.type == SwitchToTypes.Place:
        switchToNext = Places[switch.name].explore(player)
    elif switch.type == SwitchToTypes.Route:
        switchToNext = Routes[switch.name].explore(player)
    elif switch.type == SwitchToTypes.Scene:
        switchToNext = Scenes[switch.name].explore(player)
    else:
        Display(
            f"A switch was recieved not of type Place, Route, or Scene:\nName: {switch.name}\nType: {switch.type}"
        ).do(None, None)
        raise GameException
    return switchToNext


try:
    still_exploring = True
    explore_next = story.start_here

    while still_exploring:
        if isinstance(explore_next, int):
            raise QuitException

        explore_next = goTo(explore_next, player)


except QuitException:
    Display("Quit requested. Exiting.", speaker=People["System"]).do(None, None)
    sys.exit(0)

except ValueError:
    Display(
        "There was a Value Error while playing through the story. Don't worry - this one isn't your fault.",
        speaker=People["System"],
    ).do(None, None)
    Display(
        "Please contact the devs for assistance (first check for existing bug reports).",
        speaker=People["System"],
    ).do(None, None)
    raise
    sys.exit(1)  # will do something once 'raise' is removed

except SystemError:
    Display("An unkown System Error occured.", speaker=People["System"].do(None, None))
    Display(
        "You're welcome to file a bug report.", speaker=People["System"].do(None, None)
    )
