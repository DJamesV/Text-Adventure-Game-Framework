import subprocess
import sys
from enum import Enum
from time import sleep

from termcolor import colored

from commands import processCommand

# from commonMessages import (
#     QuitException,
#     GameException,
#     get_user_input,
#     displayChoice,
#     display_text,
#     getChoice,
#     get_valid_input,
# )


### Exceptions


# TODO: Consider whether it's better to raise custom exceptions or to have the process exit nicely by passing back
# a variable (i.e. quit class)
class QuitException(Exception):
    """Raised to indicate the user requested quitting the game."""


class GameException(Exception):
    """Raised to indicate an error while playing the game."""


### Enums and Dictionaries


# types of things a switch can switch to - using Index not recommended (and not yet implemented)
class SwitchToTypes(Enum):
    Place = "Place"
    Scene = "Scene"
    SubPlace = "SubPlace"
    Person = "Person"
    Route = "Route"
    Flag = "Flag"
    IndexValue = "IndexValue"
    IndexOffset = "IndexOffset"


# Aspect-to-Color Mapping
aspectColors = {
    "sorrow": "blue",
    "anger": "red",
    "happiness": "yellow",
}

### Parent Classes


class DisplaysText:
    def __init__(self):
        pass

    # TODO: Consider doing :c <color>: :c: for coloring
    def display_text(
        self,
        text: str,
        new_line_number: int = 0,
        indent: int | str = 0,
        color: str | tuple[int, int, int] | None = None,
        speaker=None,
    ):
        if isinstance(indent, int):
            indent = "    " * indent

        new_line = "\n" * new_line_number

        if speaker is not None:
            smart_new_line_value = "\n" + " " * (len(speaker.name) + 2)
            name_to_add = speaker.name.upper() + ": "
            initial_indent = ""
        else:
            smart_new_line_value = "\n" + str(indent)
            name_to_add = ""
            initial_indent = indent

        control_characters = {
            ":n:": smart_new_line_value,
            ":t:": "     ",
            ":i:": indent,
        }
        keysCC = list(control_characters.keys())

        for i in range(len(keysCC)):
            text = text.replace(keysCC[i], control_characters[keysCC[i]])

        formattedText = colored(f"{new_line}{initial_indent}{name_to_add}{text}", color)
        secondToLast = -1

        formattedList = formattedText.split(":l:")
        for i in range(len(formattedList) - 1):
            formattedText.replace(":l:", "")
            print(formattedText[i])
            Lull().do()  # type: ignore
            secondToLast = i

        print(formattedList[secondToLast + 1])

    def print_slowly(self, text: str, seconds: float = 0.05):
        for char in text:
            print(
                char, end="", flush=True
            )  # The flush is necessary or else the print will only print out it's cache periodically
            sleep(seconds)
        print("\n")

    def print_static(self, random):
        try:
            random.randint(0, 2)
        except NameError:
            import random

        for _ in range(7777):
            rand_int = random.randint(0, 2)
            if rand_int == 0:
                print(" ", end="")
            if rand_int == 1:
                print("█", end="")


class TakesInput(
    DisplaysText
):  # If a class TakesInput, it need not inherit DisplaysText as well
    def __init__(self):
        pass

    def get_user_input(self) -> str:
        dataIn = input(colored("\n> ", "light_green"))
        newResult = processCommand(dataIn)
        if newResult and newResult != "h" and newResult != "q":
            return newResult
        elif newResult == "q":
            print()
            raise QuitException()
        else:
            return dataIn

    def get_valid_input(self, dataRange: range | list):
        # ** Vars **
        invalidInputMessage = colored(
            "\n\n     I appologise, but this response is either invalid or hasn't been added to the game yet."
            "\n     please try again\n",
            "magenta",
        )

        dataIn = self.get_user_input()
        try:
            dataIn = int(dataIn)
        except:  # noqa # TODO: Restrict this more specifically
            pass

        while True:
            try:
                if isinstance(dataRange, range) or (
                    isinstance(dataRange, list) and isinstance(option, int)
                    for option in dataRange
                ):  # if it's a range of numbers
                    intData = int(dataIn)
                    if intData in dataRange:
                        validData = intData
                        break
                    else:
                        self.display_text(invalidInputMessage)  # type: ignore : This error is due to people being a global defined in AlmostGone.
                        dataIn = self.get_user_input()
                elif isinstance(dataRange, list):  # if it's a list of text responses
                    if dataIn in dataRange:
                        validData = dataIn
                        break
                    else:
                        self.display_text(invalidInputMessage)
                        dataIn = self.get_user_input()
            except:  # noqa # type: ignore : While a bare except is not ideal, neither is dealing with raw user input
                self.display_text(invalidInputMessage)
                dataIn = self.get_user_input()

        return validData

    def getChoice(
        self,
        message,
        dataRange: range | list,
        color: str | tuple[int, int, int] | None = None,
    ):
        print()
        if message is not None:
            print(colored(message, color))
        validData = self.get_valid_input(dataRange)
        print()
        return validData

    def displayChoice(
        self,
        displayChoices: list[str],
        indent: str | int = 0,
        color: str | tuple[int, int, int] | None = None,
    ):
        for i in range(len(displayChoices)):
            self.display_text(f"{indent}:t:[{i + 1}] {displayChoices[i]}", color=color)

    # TODO: This code is currently unused. Evaluate if it should be deleted.
    def invalidResponse(self) -> str:
        self.display_text(
            "\n\n     I appologise, but this response is either invalid or hasn't been added to the game yet."
            "\n     Please try again\n",
            color="magenta",
        )
        inputRetry = self.get_user_input()
        print()
        return inputRetry  ### NOTE: Now returns the input so that it can be fed back into the dealWithInput function


# The Class that all Playable Classes Inherit
class Playable:  # Every playable class will extend this function
    def __init__(self):
        self.people = {}
        self.routesIn = {}
        self.items_in = {}
        self.places = {}
        self.routes_elsewhere = {}

    def playStory(self, player, listToPlay: list):
        """
        ## Description
        A function that allows for the 'playing' of a list using OOP (Object-Oriented Programming)

        """

        # ---- Defining our variables -----
        # i will be the variable we use to move through the Story
        # I'm using a while instead of for because that allows me to move back and forth more easily
        i = 0
        # This defines what is accessible from a switch in this Place
        stayInPlace = ["SubPlace", "Route", "Person", "SubList", "Flag"]

        # ---- Looping through the list -----
        while i < len(listToPlay) and not i < 0:
            # Defining switchTo as the result of doing the next item
            switchTo = listToPlay[i].do(player, self)

            # variables
            stillSwitchOrList = True

            # dealing with switchTo
            # deals with cases where switchTo may be changed an need to be re-evaluated multiple times
            while stillSwitchOrList:
                # if switchTo is a list, we'll play through it
                if isinstance(switchTo, list):
                    switchTo = self.playStory(player, switchTo)

                # if switchTo is a Switch, then we'll see if we can get there from within the Place
                elif isinstance(switchTo, Switch):
                    # If the switch type is in stay in place and you are in a place (as opposed to a SubPlace)
                    if switchTo.type.value in stayInPlace and isinstance(self, Place):
                        if switchTo.type.value == "Person":
                            switchTo = self.playStory(
                                player, self.people[switchTo.name].interact_story
                            )
                        elif switchTo.type.value == "SubPlace":
                            switchTo = self.playStory(
                                player, self.places[switchTo.name].interact_story
                            )
                        elif switchTo.type.value == "Route":
                            switchTo = self.playStory(
                                player,
                                self.routes_elsewhere[switchTo.name].interact_story,
                            )
                        elif switchTo.type.value == "Flag":
                            switchTo = str(switchTo.name)
                    # if you cannot get there from within the Place or you are not in a place
                    else:
                        return switchTo  # return to AlmostGone to continue play with
                else:
                    stillSwitchOrList = False

            ## Once switchTo isn't a switch or list:
            # if switchTo is an integer, we'll move that many paces through the list (not recommended to do this except with value 1 - possibly 0 to redo same action. This could be used for choices, theoretically)
            if isinstance(switchTo, int):
                i += switchTo

            # if switchTo is a string, we look for a Flag with that name
            elif isinstance(switchTo, str):
                for j in range(len(listToPlay)):
                    if (
                        isinstance(listToPlay[j], Flag)
                        and listToPlay[j].name == switchTo
                    ):
                        i = j

            # if switchTo is neither, raise a GameException
            else:
                print(
                    "There was an error with the game: the item to go to was not found"
                )
                raise GameException

        return 1


## Classes For Story Play


# a class that returns a certain item to switch to
class Switch:
    def __init__(self, type: SwitchToTypes, name: str):
        self.type = type
        self.name = name

    def do(
        self, _player, _place
    ):  # note that it takes player, place - this is so that all do functions can be called the same
        return self  # it returns a type Switch - this will get passed all the way back to the while loop in newAlmostGone, if the switch points to a place or scene


# a class that acts as a marker within the larger story so that it can be switched to (useful for choices, especially with conversation)
class Flag:
    def __init__(self, name: str):
        self.name = name

    def do(self, _player, _place):
        return 1  # this will increment the index value by 1
        # So, when you get to a flag in a list, it does nothing and moves right along to the next item


# a class that stores a list to play through
class List:
    def __init__(self, listToPlay):
        self.listToPlay = listToPlay

    def do(self):
        return self.listToPlay


# displays text
class Display(DisplaysText):
    def __init__(
        self,
        textToDisplay: str | list,
        indent: int | str = 1,
        new_line_number: int = 0,
        speaker: Person | None = None,  # noqa
        lull: bool = True,
    ):
        self.textToDisplay = textToDisplay
        self.indent = indent
        self.new_line_number = new_line_number
        self.speaker = speaker
        self.lull = lull

        if speaker is None:
            self.textColor = None
        else:
            self.textColor = speaker.speechColor  # may be None

    def do(self, _player, _place):
        if isinstance(
            self.textToDisplay, str
        ):  # So that text to display can be entered in list format. It's a little easier, sometimes.
            self.textToDisplay = [self.textToDisplay]

        for display in self.textToDisplay:
            # display_text applies special formatting such as indents and smart new lines
            self.display_text(
                display, self.new_line_number, self.indent, self.textColor, self.speaker
            )

        if self.lull:
            Lull().do(None, None)

        return 1  # increments story by 1


class Lull(TakesInput):
    def __init__(self):
        pass

    def do(self, _player=None, _place=None):
        self.get_user_input()
        print()
        return 1


class Choice(
    TakesInput
):  # Used for making choices, will use a list of what to return for each item
    def __init__(
        self,
        thingsToDo: list,
        textToDisplay: str | None = None,
        toDoDisplayText: list
        | None = None,  # TODO: Change to None, adjust do function to deal with None appropriately
        speaker: Person | None = None,  # noqa
    ):
        self.textToDisplay = textToDisplay
        self.thingsToDo = thingsToDo
        self.toDoDisplayText = toDoDisplayText
        self.speaker = speaker

    def do(self, _player, _place):
        displayList = []
        if self.toDoDisplayText != None and len(self.toDoDisplayText) == len(
            self.thingsToDo
        ):
            displayList = self.toDoDisplayText
        else:
            for toDo in self.thingsToDo:
                if isinstance(toDo, str):
                    displayList.append(toDo)
                else:
                    displayList.append(toDo.name)

        if self.speaker:
            indent = (len(self.speaker.name) + 2) * " "
        else:
            indent = ""

        if self.textToDisplay is not None:
            print(indent + self.textToDisplay)
        self.displayChoice(displayList, indent=indent)
        choice = self.getChoice(None, range(1, len(self.thingsToDo) + 1))
        switchTo = self.thingsToDo[choice - 1]  # type: ignore
        # TODO: Get this to work for y/n and other custom option types (so that a custom list can be used - change it so that it can be a dictionary)
        # TODO: Troubleshoot - currently loops choice although returns str
        return switchTo


class Conditional(
    Playable
):  # for conditional. Intended to add functionality for just a list, but it's not yet build that way. I may do that later.
    def __init__(self, storyToUse: list[list], conditionsForStoryLine: list):
        """
        ## Description
        Conditional text function

        :param storyToUse: All possible story lines
        :param conditionsForStoryLine: One callable per story line. Each callable should accept (player, place)
            and return True when that story line should be shown.
        """

        self.storyToUse = storyToUse
        self.conditionsForStoryLine = conditionsForStoryLine

    def do(
        self, player, place
    ):  # the only do function that uses either player or place
        switchTo = 1

        for condition, story in zip(self.conditionsForStoryLine, self.storyToUse):
            conditionIsTrue = False
            if callable(condition):
                conditionIsTrue = condition(player, place)
            else:
                conditionIsTrue = bool(condition)

            if conditionIsTrue:
                switchTo = self.playStory(player, story)
                break

        if isinstance(switchTo, str):
            switchTo = 1

        return switchTo


class Image:
    def __init__(self, pathToImage: str):
        self.pathToImage = pathToImage

    def do(self, _player, _place):
        subprocess.Popen([sys.executable, "show_image.py", self.pathToImage])


## Places, Playables, and General Classes


class Knowledge:
    def __init__(self, name: str, world: str, knowledge: str, secretAbout=""):
        self.name = name
        self.world = world
        self.knowledge = knowledge
        self.secretAbout = secretAbout

    def do(self, player, place):
        Display(f":t:You realize {self.knowledge}").do(player, place)
        player.secrets[self.name] = self
        return 1


class Achievement(DisplaysText):
    def __init__(self, achievmentName, achievmentDescription):
        self.achievmentName = achievmentName
        self.achievmentDescription = achievmentDescription

    def achievementGet(self):
        print(
            f"\n{colored('     Achievment get!', 'light_blue')}\n"
            f"\n{colored(f'     Name: {self.achievmentName}', 'light_blue')}"
            f"\n\n{colored(f'     Description: {self.achievmentDescription}', 'light_blue')}\n"
        )


class Item(TakesInput):
    def __init__(
        self,
        name: str,
        add_health,
        add_damage,
        add_defense,
        knowledge: Knowledge,
        discover_message: str,
        keepable: bool,
        aspect="none",
    ):
        self.name = name
        self.add_health = add_health
        self.add_damage = add_damage
        self.add_defense = add_defense
        self.knowledge = knowledge
        self.discover_message = discover_message
        self.keepable = keepable
        self.aspect = aspect

    def do(self, player, place):
        """
        ### Function for items

        :param player: Takes the player
        :param place: Takes the SubPlace
        """
        print(
            self.display_text(
                f"{self.discover_message}"
                f"Do you want to keep {colored(self.name, aspectColors[self.aspect])}? [y/n]"
            )
        )
        answer = self.get_valid_input(["y", "n"])

        if answer == "y":
            player.inventory[self.name] = self
            place.items_in.pop(self.name)

        return 1

    # TODO/NOTE: This is actually a function specific to my friend's text adventure game.
    # I don't plan on keeping it in the framework, but I leave it here because I think it's good to consider
    # how things *like* this are going to work. Will people be able to code their own functions for text that
    # they use often or is often repeated in their story? How will that get implemented?
    # By the way, the emptyInput is (I'm fairly certain) from when my friend was writing this and before I wrote
    # the Lull class.
    def printFavor(self, aspect, playerColor):
        if aspect == "anger":
            print(
                colored("\n     ANGER ", "red", attrs=["bold"])
                + colored("smiles upon you.", playerColor)
                + colored("\n\n> ", "light_green")
            )
            emptyInput = input()
        elif aspect == "happiness":
            print(
                colored("\n     HAPPINESS ", "yellow", attrs=["bold"])
                + colored("smiles upon you.", playerColor)
                + colored("\n\n> ", "light_green")
            )
            emptyInput = input()
        elif aspect == "sorrow":
            print(
                colored("\n     SORROW ", "blue", attrs=["bold"])
                + colored("smiles upon you.", playerColor)
                + colored("\n\n> ", "light_green")
            )
            emptyInput = input()  # noqa


class Scene(Playable):
    def __init__(self, story: list):
        self.story = story

    def explore(self, player):
        return self.playStory(player, self.story)


# NOTE: Because this is one of the driving classes behind the story, I want to integrate it more fully with the do function for ease of use
class SubPlace(Playable):
    def __init__(
        self,
        name: str,
        interact_story: list,
        items_in: dict[str, Item],
        opened: bool = False,
        isScene=False,
    ):
        self.name = name
        self.interact_story = interact_story
        self.items_in = items_in
        self.opened = opened
        self.isScene = isScene

    def do(self, player, place):
        self.opened = True

        if not self.isScene:
            place.places[self.name] = self

        switchTo = self.playStory(player, self.interact_story)

        return switchTo

    # def interact(self, player):
    #     print(" "+self.interactMessage)
    #     itemsRemoved = []
    #     for item in self.items_in.values():
    #         print(f" {item.discover_message}")
    #         if item.knowledge:
    #             player.gainKnowledge(item.knowledge)
    #         if item.keepable == True:
    #             if input(f"Do you wish to keep {item.name}? y/n ") == 'y':
    #                 player.gainItem(item)
    #                 itemsRemoved.append(item.name)

    #     for i in itemsRemoved:
    #         self.items_in.pop(i)


class Person(Playable):  # For NPCs
    def __init__(
        self,
        name: str,
        secrets: list = [],  # noqa: B006 - This is for the error code about setting mutable data types by default, but I want people to be able to see/change these.
        places_been: list = [],  # noqa: B006
        pronouns: list[str] = ["they", "their"],  # noqa: B006
        interact_story: list = [],  # noqa: B006
        speechColor: str | None = None,
        option_display_text: str | None = None,
    ):
        self.name = name
        self.secrets = secrets
        self.places_been = places_been
        self.pronouns = pronouns
        self.interact_story = interact_story
        self.speechColor = speechColor
        self.option_display_text = option_display_text


class Route(Playable):
    def __init__(
        self, name: str, interact_story: list, option_display_text: str | None = None
    ):
        self.name = name
        self.interact_story = interact_story
        self.option_display_text = option_display_text


class Place(Playable):
    def __init__(
        self,
        name,
        welcome_message,
        places: dict[str, SubPlace] = {},  # noqa: B006 - This is for the error code about setting mutable data types by default, but I want people to be able to see/change these.
        people: dict[str, Person] = {},  # noqa: B006
        routes_elsewhere: dict[str, Route] = {},  # noqa: B006
    ):
        self.name = name
        self.places = places
        self.people = people
        self.routes_elsewhere = routes_elsewhere
        self.welcome_message = welcome_message

    def explore(self, player):
        print(self.welcome_message)
        return self.playStory(player, self.welcome_message)

    # TODO: Integrate SubPlace more fully, consider the usefulness of this function and whether it should stay.
    def addSubPlace(
        self,
        name_of_subplace: str,
        message: str,
        interact_story: list,
        items_in: dict[str, Item],
        opened: bool = False,
        show_in_options: bool = True,
        in_options_message: None | str = None,
    ):
        self.places[name_of_subplace] = SubPlace(
            name_of_subplace, interact_story, items_in, opened
        )
        # add show in options code here, as well as message code

    def removeSubPlace(self, name_of_subplace: str):
        self.places.pop(name_of_subplace)

    def addRoute(self, route: Route):
        self.routes_elsewhere[route.name] = route

    def removeRoute(self, name: str):
        self.routes_elsewhere.pop(name)

    def addPerson(self, person: Person):
        self.people[person.name] = person

    def removePerson(self, person_name) -> Person:
        self.people[person_name].places_been.append(self.name)
        return self.people.pop(person_name)
