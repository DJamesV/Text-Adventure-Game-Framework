from termcolor import colored
from commonMessages import achievementGet, printSystem, printStatic, displayText, enumerateLoot
from PlayerClass import Player

name = input(f"{colored("> ", "light_green")}" + "Enter your name: ")
player = Player(name, "light_grey")
globalPlayerColor = "light_grey"
if name == "":
    quit()

def updatePlayerSorrow():
    player.playerColor = "blue"
    globalPlayerColor = "blue"
    player.alignment = "sorrow"

    printSystem("\n     Congratulations!(?) You are now aligned with the aspect of:")
    print(colored("\n          SORROW", "blue", attrs=["bold"]))
    enumerateLoot(1, 10, 2, ["Tear of Lonliness"], player.playerColor)
    printSystem("\n     You have lost:")
    print(colored("\n          - YOUR HUMANITY", attrs=["bold"]), end="")
    displayText("", 0, 1, player.playerColor)

joinGirlByFireDict = None

inspectCabinDict = {
    "actionItems":[
        {"type":"displayText", "text":"     Alongside the fireplace and the girl there is also a bed, a nightstand, and a desk with a chair."},
        {"type":"choiceText", "text":"     [1] Join the girl by the fire\n     [2] Inspect bed\n     [3] Inspect nightstand\n     [4] Inspect desk"}
    ],

    1:{
        "actionItems":[
            {"type":"switchTo", "dict":joinGirlByFireDict}
        ]
    },

    2:{
        "actionItems":[
            {"type":"displayText", "text":"     Looks like a comfy bed. You could sleep comfortably in it if you were tired."},
            {"type":"displayText", "text":"     Come to think of it, you're not hungry either."},
            {"type":"switchTo", "dict":"self"}
        ]
    },

    3:{
        "actionItems":[
            {"type":"displayText", "text":"     The nightstand is simply constructed, and a single candle stands\n     upon it alongside a drawer."},
            {"type":"displayText", "text":"     Upon opening said drawer, you find nothing. What are you meant to put in there anyway?"},
            {"type":"switchTo", "dict":"self"}
        ]
    },

    4:{
        "actionItems":[
            {"type":"displayText", "text":"     You go and sit at the desk. The chair is suprisingly comfortable, and the\n     desk has a single drawer, which bears a keyhole."},
            {"type":"displayText", "text":"     In attempting to open it, you find that it is locked."},
            {"type":"switchTo", "dict":"self"}
        ]
    }
}

gardenOfLifeDict = None

worldAblazeDict = None

darkestDreamsDict = {
    "actionItems":[
        {"type":"function", "funct":updatePlayerSorrow},
        {"type":"displayText", "text":"JUDGE: Interesting choice."},
        {"type":"displayText", "text":"Not many souls go there, but as it turns out I've just recently sent one there."},
        {"type":"displayText", "text":"A special soul."},
        {"type":"displayText", "text":"Maybe you'll meet them"},
        {"type":"displayText", "text":f"JUDGE: Well, good luck, {name}"},
        {"type":"displayText", "text":"     You feel the cold grasp of something coiling around your leg."},
        {"type":"displayText", "text":"     Upon inspection you find an animated chain which only tightens as you attempt to pull away."},
        {"type":"displayText", "text":"     The world around you goes dark, and you become unable to breath.\n     You are desperate for oxygen, but it fails to reach your lungs,\n     and eventually you lose your grip on reality."},
        {"type":"displayText", "text":"     ..."},
        {"type":"displayText", "text":"     You open your eyes."},
        {"type":"displayText", "text":"     It takes a moment for them to adjust to the darkness, but when\n     they do you can clearly see before you a silent forest blanketed by fog."},
        {"type":"displayText", "text":"     Looking around you, there is but one point of interest. A solitary light, flickering in the distance."},
        {"type":"choiceText", "text":"\n     [1] Approach the light\n     [2] Go deeper into the forest"}
    ],

    1:{
        "actionItems":[
            {"type":"displayText", "text":"     A single step takes you to your destination. You see now that the\n     flickering light is produced by a gas-lit lamp affixed to a log cabin."},
            {"type":"displayText", "text":"     The cabin looks as though it has been there for centuries. It is\n     overgrown with vines, and the wood looks damp and rotten through. Still,\n     it stands."},
            {"type":"displayText", "text":"     You climb the steps with caution, and open the door with reckless abandon."},
            {"type":"displayText", "text":"     The interior is a stark contrast to the exterior. It is furnished, clean, and appears new.\n     Despite the cabin being made of wood, it houses a brick fireplace, which is lit."},
            {"type":"displayText", "text":"     Huddled next to the fire is a girl. She is shivering, clearly quite cold."},
            {"type":"displayText", "text":"     Now that you think about it, it is quite cold, isn't it?"},
            {"type":"choiceText", "text":"     [1] Join the girl by the fire\n     [2] Inspect the cabin"}
        ],

        1:{
            "actionItems":[
                {"type":"switchTo", "dict":joinGirlByFireDict}
            ]
        },

        2:{
            "actionItems":[
                {"type":"switchTo", "dict":inspectCabinDict}
            ]
        }
    },

    2:{
        "actionItems":[
            {"type":"displayText", "text":"     Unfortunately the dev hasn't made anything here yet. Come back later."},
            {"type":"function", "funct":quit}
        ]
    }
}

deadzoneDict = None

introDict2 = {
    "actionItems":[
        {"type":"displayText", "text":"JUDGE: Welcome to Gen V. You're blind, you're deaf, you're mute, and you're dead."},
        {"type":"displayText", "text":"For now."},
        {"type":"displayText", "text":f"This is my Domain. This is {colored("The Deadzone", "dark_grey")}."},
        {"type":"displayText", "text":"     Before you lies field of brown grass, a blanket of grey clouds tempting rain."
        "\n     Dead trees and shrubbery dot the landscape, all the leaves long gone, and the insides hollow."},
        {"type":"displayText", "text":"     The only approximation of life in this environment is the cold breeze which occassionally blows through,"
        "\n     sending shivers down your spine."},
        {"type":"displayText", "text":"JUDGE: As you might have guessed, this is a sort of purgatory."
        "\nYou're not 'dead', death implies life, but dead is far easier to explain."},
        {"type":"displayText", "text":"The dead ones stop by, though."},
        {"type":"displayText", "text":"The important thing here is that I can give you the opptrunity to come back from the dead."},
        {"type":"displayText", "text":"     The wind disappears"},
        {"type":"displayText", "text":"JUDGE: Beyond that you're on your own."},
        {"type":"displayText", "speaker":"System", "text":f"SYSTEM: Hi! I'm SYSTEM, it's nice to meet you {name} ^^ I'll be providing you information throughout game."},
        {"type":"displayText", "text":f"     {colored("WARNING!", "yellow", attrs=["bold"])}"},
        {"type":"displayText", "speaker":"System", "text":"The choice you are about to make is PERMENANT and will FOREVER CHANGE the rest of the game."},
        {"type":"displayText", "speaker":"System", "text":"It'll FOREVER CHANGE you as well."},
        {"type":"displayText", "speaker":"System", "text":"Though, I suppose you could say that about all your choices."},
        {"type":"displayText", "text":f"JUDGE: I am {colored("The Judge", "dark_grey")} of the afterlife, or in other words, I pass"
         "\njudgement on the souls which enter, and send them to one of three places."},
        {"type":"displayText", "text":"You're special though. I do not have the ability to pass judgement upon you,"
        "\nbecause there is nothing to judge."},
        {"type":"displayText", "text":f"And well, I could just send you to one of the afterlives at {colored("random", "yellow")},"},
        {"type":"displayText", "text":f"or even {colored("eliminate", "red")} you entierly,"},
        {"type":"displayText", "text":f"but since {colored("The Fallen", "light_yellow")} likes you so much..."},
        {"type":"choiceText", "text":f"I'll let you choose:\n\n     {colored("[1] The Garden of Life", "red", attrs=["bold"])}\n     {colored("[2] The World Ablaze", "yellow", attrs=["bold"])}\n     {colored("[3] The Darkest Dreams", "blue", attrs=["bold"])}\n\nJUDGE: Or, you know:\n\n     [4] Stay."}
    ],

    1:{
        "actionItems":[
            {"type":"switchTo", "dict":gardenOfLifeDict}
        ]
    },

    2:{
        "actionItems":[
            {"type":"switchTo", "dict":worldAblazeDict}
        ]
    },

    3:{
        "actionItems":[
            {"type":"switchTo", "dict":darkestDreamsDict}
        ]
    },

    4:{
        "actionItems":[
            {"type":"switchTo", "dict":deadzoneDict}
        ]
    }
}

introDict = {
    "actionItems":[
        {"type":"displayText", "speaker":"System", "text":"SYSTEM: Hey there, I'll see you in a bit, but for now,"
        "\n     I'm just here to give you some important information."},
        {"type":"displayText", "speaker":"System", "text":"You can type 'h' to see all of the available commands at any time"
        "\n     and type 'q' to exit the game."},
        {"type":"displayText", "speaker":"System", "text":"Have fun, and read carefully!"},
        {"type":"displayText", "text":f"???: Greetings, {name}."},
        {"type":"displayText", "text":"???: It is truly unfortunate that you have chosen to play this game,"
        "\nbut I can't stop you."},
        {"type":"displayText", "text":f"JUDGE: My Title is {colored("The Judge", "dark_grey")}."},
        {"type":"displayText", "text":"     It is humanoid, but only possesses the head, arms, and heart. The heart, which is entirely exposed,"
        "\n     slowly pulses, pushing a bioluminescent yellow fluid up through its equally exposed veins"
        "\n     and into its extremities."},
        {"type":"displayText", "text":f"     Perhaps the slow heartbeat indicates that this thing-\n{colored("     The Judge", "dark_grey")}-\n     is calm."},
        {"type":"displayText", "text":f"     Its three eye sockets are inlain with {colored("heter", "red")}{colored("ochro", "yellow")}{colored("matic", "blue")} gems,"
         "\n     and it bears no mouth- yet the sound reaches you nonetheless."},
        {"type":"displayText", "text":f"     Even if you really couldn't hear it speak,\n     you could {colored("feel", attrs=["bold"])} it speak."},
        {"type":"choiceText", "text":"JUDGE: The first thing you will need to do is make a choice:\n\n     [1] Play\n     [2] Perish"}
    ],

    1:{
        "actionItems":[
            {"type":"choiceText", "text":"JUDGE: You'd really be better off leaving, are you sure?\n\n     [1] 'Yes, I am sure'\n     [2] 'No, I choose to perish'"}
        ],
        1:{
            "actionItems":[
                {"type":"displayText", "text":f"JUDGE: Well, that's a {colored("shame", "blue")}."},
                {"type":"switchTo", "dict":introDict2}
            ]
        },
        2:{
            "actionItems":[
                {"type":"switchTo", "dict":introDict2}
            ]
        }
    },
    2:{
        "actionItems":[
            {"type":"displayText", "text":f"JUDGE: {colored("Hahaha", "yellow")},"},
            {"type":"displayText", "text":"     The laugh is deep, and genuine. It makes it sound as though it has weathered every summer,"
            "\n     and every winter. It says 'I have lived, but I have also died"
            "\n     a thousand times.'"},
            {"type":"displayText", "text":"JUDGE: I was just kidding with you. You're already dead. Well- somewhat, anyway."},
            {"type":"switchTo", "dict":introDict2}
        ]
    }
}

def evaluateCommand(input):
    if input == "q":
        quit()
    elif input == "h":
        printSystem("\n     Available commands:\n\n     [h] Display commands\n     [q] Quit the game")
        return True
    else:
        return False

def playStory(dict, textDisplayed):
    for innerDict in dict["actionItems"]: # Travserses the list of dictionaries in actionItems
        if innerDict["type"] == "displayText" and not textDisplayed:
            try:
                if innerDict["speaker"] == "System":
                    print("\n     " + colored(innerDict["text"], "light_magenta"))
            except:
                print("\n" + colored(f"{innerDict["text"]}", player.playerColor))
            print(colored("\n> ", "light_green"), end="")
            tempo = input()
            evaluateCommand(tempo)
        elif innerDict["type"] == "choiceText":
            print("\n" + f"{colored(f"{innerDict["text"]}", player.playerColor)}")
            print(colored("\n> ", "light_green"), end="")
            choice = input()
            try:
                if 0 < int(choice) < len(dict):
                    playStory(dict[int(choice)], False)
                else:
                    print("\nThis response is either invalid or hasn't been added to the game yet. ET1 input outside choice range")
            except ValueError:
                if not evaluateCommand(choice):
                    print("\nThis response is either invalid or hasn't been added to the game yet. ET2 input not int and not command")
                playStory(dict, True)
        elif innerDict["type"] == "switchTo":
            if innerDict["dict"] == "self":
                textDisplayed = False
                continue
            else:
                playStory(innerDict["dict"], False)
        elif innerDict["type"] == "function" and not textDisplayed:
            innerDict["funct"]()

playStory(introDict, False)