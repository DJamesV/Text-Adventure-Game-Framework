# from commonMessages import (
#     QuitException,  # noqa
#     GameException,
#     getUserInput,
#     displayChoice,
#     displayText,
#     getChoice,
#     getValidInput,
# )
from enum import Enum
from termcolor import colored
import subprocess
import sys
from time import sleep
from commands import processCommand
from State import People, Routes, Scenes, Places  # noqa - Clean up later, once it is determined what imports will be needed

### Exceptions


# TODO: Move both Exceptions to CommonClasses
class QuitException(Exception):
    """Raised to indicate the user requested quitting the game."""

    pass


class GameException(Exception):
    """Raised to indicate an error while playing the game."""

    pass


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
    def displayText(
        self,
        text: str,
        newLineNumber: int = 0,
        indent: int | str = 0,
        color: str | tuple[int, int, int] | None = None,
        speaker=None,
    ):
        if isinstance(indent, int):
            indent = "    " * indent
        else:
            indent = indent
        newLine = "\n" * newLineNumber

        # if newLineNumber == 0:
        #     newLine = ""

        if speaker is not None:
            smartNewLineValue = "\n" + " " * (len(speaker.name) + 2)
            nameToAdd = speaker.name.upper() + ": "
        else:
            smartNewLineValue = "\n" + str(indent)
            nameToAdd = ""

        controlCharacters = {":n:": smartNewLineValue, ":t:": "     ", ":i:": indent}
        keysCC = list(controlCharacters.keys())

        for i in range(len(keysCC)):
            text = text.replace(keysCC[i], controlCharacters[keysCC[i]])

        formattedText = colored(f"{newLine}{indent}{nameToAdd}{text}", color)
        secondToLast = -1

        formattedList = formattedText.split(":l:")
        for i in range(len(formattedList) - 1):
            formattedText.replace(":l:", "")
            print(formattedText[i])
            Lull().do()  # type: ignore # noqa
            secondToLast = i

        print(formattedList[secondToLast + 1])

    def printSlowly(self, text: str, seconds: float = 0.05):
        for char in text:
            print(
                char, end="", flush=True
            )  # The flush is necessary or else the print will only print out it's cache periodically
            sleep(seconds)
        print("\n")

    def printStatic(self, random):
        try:
            random.randint(0, 2)
        except NameError:
            import random

        for i in range(7777):
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

    def getUserInput(self) -> str:
        dataIn = input(colored("\n> ", "light_green"))
        newResult = processCommand(dataIn)
        if newResult and newResult != "h" and newResult != "q":
            return newResult
        elif newResult == "q":
            print()
            raise QuitException()
        else:
            return dataIn

    def getValidInput(self, dataRange: range | list):
        # ** Vars **
        invalidInputMessage = colored(
            "\n\n     I appologise, but this response is either invalid or hasn't been added to the game yet."
            "\n     please try again\n",
            "magenta",
        )

        dataIn = self.getUserInput()
        try:
            dataIn = int(dataIn)
        except:  # noqa
            pass

        while True:  # Currently not working - just continues looping
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
                        self.displayText(invalidInputMessage)  # noqa # type: ignore : This error is due to people being a global defined in AlmostGone.
                        dataIn = self.getUserInput()
                elif isinstance(dataRange, list):  # if it's a list of text responses
                    if dataIn in dataRange:
                        validData = dataIn
                        break
                    else:
                        self.displayText(invalidInputMessage)  # noqa # type: ignore : This error is due to people being a global defined in AlmostGone.
                        dataIn = self.getUserInput()
                else:
                    self.displayText(invalidInputMessage)  # noqa # type: ignore : This error is due to people being a global defined in AlmostGone.
                    dataIn = self.getUserInput()
            except:  # noqa # type: ignore : While a bare except is not ideal, neither is dealing with raw user input
                self.displayText(invalidInputMessage)  # noqa # type: ignore : This error is due to people being a global defined in AlmostGone.
                # TODO: Consider depency chain and how best to implement (i.e. cannot use speaker = People["system"] here)
                dataIn = self.getUserInput()

        return validData

    def getChoice(
        self,
        message,
        dataRange: range | list,
        color: str | tuple[int, int, int] | None = None,
    ):
        print("")
        if message is not None:
            print(colored(message, color))
        validData = self.getValidInput(dataRange)
        print("")
        return validData

    def displayChoice(
        self,
        displayChoices: list[str],
        indent: str | int = 0,
        color: str | tuple[int, int, int] | None = None,
    ):
        for i in range(len(displayChoices)):
            self.displayText(f"{indent}:t:[{i + 1}] {displayChoices[i]}", color=color)

    def invalidResponse(self, pI) -> str:
        self.displayText(
            "\n\n     I appologise, but this response is either invalid or hasn't been added to the game yet."
            "\n     Please try again\n",
            color="magenta",
        )
        inputRetry = self.getUserInput()
        print("")
        return inputRetry  ### NOTE: Now returns the input so that it can be fed back into the dealWithInput function


# The Class that all Playable Classes Inherit
class Playable:  # Every playable class will extend this function
    def __init__(self):
        self.people = {}
        self.routesIn = {}
        self.itemsIn = {}
        self.places = {}
        self.routesElsewhere = {}

    def playStory(
        self, player, listToPlay: list
    ):  # The new and improved playStory function
        """
        ## Description
        A function that allows for the 'playing' of a list using OOP (Object-Oriented Programming)

        """
        i = 0

        while i < len(listToPlay) and not i < 0:
            switchTo = listToPlay[i].do(player, self)

            # variables
            stayInPlace = ["SubPlace", "Route", "Person", "SubList", "Flag"]
            stillSwitchOrList = True

            # dealing with switchTo
            # deals with cases where switchTo may be changed an need to be re-evaluated multiple times
            while stillSwitchOrList:
                # if switchTo is a list, we'll play thorugh it
                if isinstance(switchTo, list):
                    switchTo = self.playStory(player, switchTo)

                # if switchTo is a Switch, then we'll see if we can get there from within the Place
                elif isinstance(
                    switchTo, Switch
                ):  # TODO: Decide whether it should first try within the place and then try outside the place
                    if switchTo.type.value in stayInPlace and isinstance(self, Place):
                        if switchTo.type.value == "Person":
                            self.playStory(
                                player, self.people[switchTo.name].interactStory
                            )
                        elif switchTo.type.value == "SubPlace":
                            self.playStory(
                                player, self.places[switchTo.name].interactStory
                            )
                        elif switchTo.type.value == "Route":
                            self.playStory(
                                player,
                                self.routesElsewhere[switchTo.name].interactStory,
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
                    if isinstance(listToPlay[j], Flag):
                        if listToPlay[j].name == switchTo:
                            i = j

            # if switchTo is neither, raise a GameExcdption
            else:
                print(
                    "There was an error with the game: the item to go to was not found"
                )
                raise GameException  # noqa
        return 1


## Classes For Story Play


# a class that returns a certain item to switch to
class Switch:
    def __init__(self, type: SwitchToTypes, name: str):
        self.type = type
        self.name = name

    def do(
        self, player, place
    ):  # note that it takes player, place - this is so that all do functions can be called the same
        return self  # it returns a type Switch - this will get passed all the way back to the while loop in newAlmostGone, if the switch points to a place or scene


# a class that acts as a marker within the larger story so that it can be switched to (useful for choices, especially with conversation)
class Flag:
    def __init__(self, name: str):
        self.name = name

    def do(self, player, place):
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
        newLineNumber: int = 0,
        speaker: Person | None = None,  # noqa
        lull: bool = True,
    ):  # noqa
        self.textToDisplay = textToDisplay
        self.indent = indent
        self.newLineNumber = newLineNumber
        self.speaker = speaker
        self.lull = lull

        if speaker is None:
            self.textColor = None
        else:
            self.textColor = speaker.speechColor  # may be None

    def do(self, player, place):
        if isinstance(
            self.textToDisplay, str
        ):  # So that text to display can be entered in list format. It's a little easier, sometimes.
            self.textToDisplay = [self.textToDisplay]

        for display in self.textToDisplay:
            # displayText applies special formatting such as indents and smart new lines
            self.displayText(  # noqa
                display, self.newLineNumber, self.indent, self.textColor, self.speaker
            )  # noqa

        if self.lull:
            Lull().do(player, place)

        return 1  # increments story by 1


class Lull(TakesInput):
    def __init__(self):
        pass

    def do(self, player=None, place=None):
        self.getUserInput()  # noqa
        print("")
        return 1


class Choice(
    TakesInput
):  # Used for making choices, will use a list of what to return for each item
    def __init__(
        self,
        thingsToDo: list,
        textToDisplay: str | None = None,
        toDoDisplayText: list = [],
        speaker: Person | None = None,  # noqa
    ):  # noqa
        self.textToDisplay = textToDisplay
        self.thingsToDo = thingsToDo
        self.toDoDisplayText = toDoDisplayText
        self.speaker = speaker

    def do(self, player, place):
        displayList = []
        if len(self.toDoDisplayText) == len(self.thingsToDo):
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
        choice = self.getChoice(None, range(1, len(self.thingsToDo) + 1))  # noqa
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

    def do(self, player, place):
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
        addHealth,
        addDamage,
        addDefense,
        knowledge: Knowledge,
        discoverMessage: str,
        keepable: bool,
        aspect="none",
    ):
        self.name = name
        self.addHealth = addHealth
        self.addDamage = addDamage
        self.addDefense = addDefense
        self.knowledge = knowledge
        self.discoverMessage = discoverMessage
        self.keepable = keepable
        self.aspect = aspect

    def keep(self):
        print(f" Do you want to keep {self.name}? y/n")
        answer = self.getUserInput()  # noqa

    def do(self, player, place):
        """
        ### Function for items

        :param player: Takes the player
        :param place: Takes the SubPlace
        """
        print(
            self.displayText(
                (
                    f"{self.discoverMessage}"
                    f"Do you want to keep {colored(self.name, aspectColors[self.aspect])}? [y/n]"
                )
            )
        )  # noqa
        answer = self.getValidInput(["y", "n"])  # noqa

        if answer == "y":
            player.inventory[self.name] = self
            place.itemsIn.pop(self.name)

        return 1

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
#       I'm not honestly entirely sure how Python will handle my modifying place in the function, but I guess we'll see.
class SubPlace(Playable):
    def __init__(
        self,
        name: str,
        interactStory: list,
        itemsIn: dict[str, Item],
        opened: bool = False,
        isScene=False,
    ):
        self.name = name
        self.interactStory = interactStory
        self.itemsIn = itemsIn
        self.opened = opened
        self.isScene = isScene

    def do(self, player, place):
        self.opened = True

        if not self.isScene:
            place.places[self.name] = self

        switchTo = self.playStory(player, self.interactStory)

        return switchTo

    # def interact(self, player):
    #     print(" "+self.interactMessage)
    #     itemsRemoved = []
    #     for item in self.itemsIn.values():
    #         print(f" {item.discoverMessage}")
    #         if item.knowledge:
    #             player.gainKnowledge(item.knowledge)
    #         if item.keepable == True:
    #             if input(f"Do you wish to keep {item.name}? y/n ") == 'y':
    #                 player.gainItem(item)
    #                 itemsRemoved.append(item.name)

    #     for i in itemsRemoved:
    #         self.itemsIn.pop(i)


class Person(Playable):  # For NPCs
    def __init__(
        self,
        name: str,
        secrets: list = [],
        placesBeen: list = [],
        pronouns: list[str] = ["they", "their"],
        interactStory: list = [],
        speechColor: str | None = None,
        optionDisplayText: str | None = None,
    ):
        self.name = name
        self.secrets = secrets
        self.placesBeen = placesBeen
        self.pronouns = pronouns
        self.interactStory = interactStory
        self.speechColor = speechColor
        self.optionDisplayText = optionDisplayText


class Route(Playable):
    def __init__(
        self, name: str, interactStory: list, optionDisplayText: str | None = None
    ):
        self.name = name
        self.interactStory = interactStory
        self.optionDisplayText = optionDisplayText


# class Route(Playable):
#     def __init__(self, name:str, comingFrom, goingTo, textDict, optionMessage: str | None = None):
#         self.name = name
#         self.comingFrom = comingFrom
#         self.goingTo = goingTo
#         self.textDict = textDict
#         self.optionMessage = optionMessage

#     def takeRoute(self, player) -> str:
#         self.playStory(player, self.textDict)
#         return self.goingTo


class Place(Playable):
    def __init__(
        self,
        name,
        welcomeMessage,
        places: dict[str, SubPlace] = {},
        people: dict[str, Person] = {},
        routesElsewhere: dict[str, Route] = {},
    ):
        self.name = name
        self.places = places
        self.people = people
        self.routesElsewhere = routesElsewhere
        self.welcomeMessage = welcomeMessage

    def explore(self, player):
        return self.playStory(player, self.welcomeMessage)

    def addSubPlace(
        self,
        nameOfSubplace: str,
        message: str,
        interactStory: list,
        itemsIn: dict[str, Item],
        opened: bool = False,
        showInOptions: bool = True,
        inOptionsMessage: None | str = None,
    ):
        self.places[nameOfSubplace] = SubPlace(
            nameOfSubplace, interactStory, itemsIn, opened
        )
        # add show in options code here, as well as message code

    def removeSubPlace(self, nameOfSubplace: str):
        self.places.pop(nameOfSubplace)

    def addRoute(self, route: Route):
        self.routesElsewhere[route.name] = route

    def removeRoute(self, name: str):
        self.routesElsewhere.pop(name)

    def addPerson(self, person: Person):
        self.people[person.name] = person

    def removePerson(self, personName) -> Person:
        self.people[personName].placesBeen.append(self.name)
        return self.people.pop(personName)
