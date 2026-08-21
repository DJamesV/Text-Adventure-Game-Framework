from CommonClasses import Display, Place, SwitchToTypes, Switch, QuitException  # noqa - Tighten imports once more polished
from State import Places, Scenes, Routes, People, player
import sys
import Story

State = Story.main()


def goTo(switch, player):
    if switch.type == SwitchToTypes.Place:
        switchToNext = Places[switch.name].explore(player)
    elif switch.type == SwitchToTypes.Route:
        switchToNext = Routes[switch.name].explore(player)
    elif switch.type == SwitchToTypes.Scene:
        switchToNext = Scenes[switch.name].explore(player)
    else:
        switchToNext = Switch(SwitchToTypes.Place, "Log Cabin")

    return switchToNext


try:
    stillExploring = True
    exploreNext = Switch(SwitchToTypes.Scene, "Intro")

    while stillExploring:
        if isinstance(exploreNext, int):
            raise QuitException

        exploreNext = goTo(exploreNext, player)


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
