from termcolor import colored
from commonMessages import achievementGet, printSystem, printStatic, displayText

import subprocess
import sys

name = input(f"{colored('> ', 'light_green')}" + "Enter your name: ")
if name == "":
    quit()

gardenOfLifeDict = None

worldAblazeDict = None

inspectCabinDict = {  # Inspect the cabin
    "actionItems": [
        {
            "type": "displayText",
            "text": "     Alongside the fireplace and the girl there is also a bed, a nightstand, and a desk with a chair.",
        },
        {
            "type": "choiceText",
            "text": "     [1] Join the girl by the fire\n     [2] Inspect bed\n     [3] Inspect nightstand\n     [4] Inspect desk",
        },
    ],
    1: {
        "actionItems": [{"type": "switchTo", "dict": "talkToGirlDict"}]
    },  # join girl scene reuse
    2: {
        "actionItems": [
            {
                "type": "displayText",
                "text": "     Looks like a comfy bed. You could sleep comfortably in it if you were tired.",
            },
            {
                "type": "displayText",
                "text": "     Come to think of it, you're not hungry either.",
            },
            # {"type": "displayText", "text": "     The injuries you sustained earlier still hurt though."},
            {"type": "switchToSelf"},
        ]
    },
    3: {
        "actionItems": [
            {
                "type": "displayText",
                "text": "     The nightstand is simply constructed, and a single candle stands\n     upon it alongside a drawer.",
            },
            {
                "type": "displayText",
                "text": "     Upon opening said drawer, you find nothing. What are you meant to put in there anyway?",
            },
            {"type": "switchToSelf"},
        ]
    },
    4: {
        "actionItems": [
            {
                "type": "displayText",
                "text": "     You go and sit at the desk. The chair is suprisingly comfortable, and the\n     desk has a single drawer, which bears a keyhole.",
            },
            {
                "type": "displayText",
                "text": "     In attempting to open it, you find that it is locked.",
            },
            {"type": "switchToSelf"},
        ]
    },
}

talkToGirlDict = {  # Join the girl by the fire
    "actionItems": [
        {
            "type": "displayText",
            "text": "     Being rather cold yourself, you decide to join the girl by the fire.",
        },
        {
            "type": "displayText",
            "text": "     The fire is not warm, and as you reach your hands closer, you realise the only\n     indication that fire exists there at all is the pain it produces in your fingertips\n     if you get too close.",
        },
        {
            "type": "displayText",
            "text": "     Looking over at the girl's face, you are a little startled, for her lips\n     are sealed shut by metal wire sewn through her flesh.",
        },
        {
            "type": "displayText",
            "text": "     You figure she can still answer yes or no questions, though.",
        },
        {
            "type": "choiceText",
            "text": "     [1] 'Did you die?'\n     [2] 'Can you speak?'\n     [3] 'Can I remove those wires?'\n     [4] 'What is your name?'",
        },
    ],
    1: {
        "actionItems": [
            {
                "type": "displayText",
                "text": "     She appears pensive for a moment, then nods her head. She seems to regret this fact.",
            },
            {"type": "switchToSelf"},
        ]
    },
    2: {
        "actionItems": [
            {
                "type": "displayText",
                "text": "     She shakes her head. Perhaps she already tried.",
            },
            {"type": "switchToSelf"},
        ]
    },
    3: {
        "actionItems": [
            {
                "type": "displayText",
                "text": "     She quickly shakes her head. She seems to be worried about this.",
            },
            {"type": "switchToSelf"},
        ]
    },
    4: {
        "actionItems": [
            {
                "type": "displayText",
                "text": "     She thinks for a moment, then stands up and offers her hand to you.",
            },
            {
                "type": "choiceText",
                "text": "     [1] Take hand and stand up\n     [2] Stand up by yourself",
            },
        ],
        1: {
            "actionItems": [
                {
                    "type": "displayText",
                    "text": "     You take her hand and she helps you up. She will remember this.",
                },
                {
                    "type": "displayText",
                    "text": "     The girl leads you outside the cabin where she picks a stick up off the ground. She scrawls\n     the name 'Abby' into the dirt and looks at you.",
                },
                {"type": "switchTo", "dict": "outsideCabinDict"},
            ]
        },
        2: {
            "actionItems": [
                {
                    "type": "displayText",
                    "text": "     You stand up on your own. She will remember this.",
                },
                {
                    "type": "displayText",
                    "text": "     The girl leads you outside the cabin where she picks a stick up off the ground. She scrawls\n     the name 'Abby' into the dirt and looks at you.",
                },
                {"type": "switchTo", "dict": "outsideCabinDict"},
            ]
        },
    },
}

darkestDreamsDict = {
    "actionItems": [
        {"type": "displayText", "text": "JUDGE: Interesting choice."},
        {
            "type": "displayText",
            "text": "Not many souls go there, but as it turns out I've just recently sent one.",
        },
        {"type": "displayText", "text": "A special soul."},
        {"type": "displayText", "text": "Maybe you'll meet them."},
        {"type": "displayText", "text": f"JUDGE: Well, good luck, {name}."},
        {
            "type": "displayText",
            "text": "     You feel the cold grasp of something coiling around your leg.",
        },
        {
            "type": "displayText",
            "text": "     Upon inspection you find an animated chain which only tightens as you attempt to pull away.",
        },
        {
            "type": "displayText",
            "text": "     More and more chains wrap themselves around you, pulling you through the ground.",
        },
        # {"type": "displayText", "text": "In the process you are hurt, and take 2 damage."},
        {
            "type": "displayText",
            "text": "     The world around you goes dark, and you become unable to breath.\n     You are desperate for oxygen, but it fails to reach your lungs,\n     and eventually you lose your grip on reality.",
        },
        {"type": "displayText", "text": "     ..."},
        {"type": "displayText", "text": "     You open your eyes."},
        {
            "type": "displayText",
            "text": "     It takes a moment for them to adjust to the darkness, but when\n     they do you can clearly see before you a silent forest blanketed by fog.",
        },
        {
            "type": "displayText",
            "text": "     Looking around you, there is but one point of interest. A solitary light, flickering in the distance.",
        },
        {
            "type": "choiceText",
            "text": "     [1] Approach the light\n     [2] Go deeper into the forest",
        },
    ],
    1: {  # Approach the light
        "actionItems": [
            {
                "type": "displayText",
                "text": "     A single step takes you to your destination. You see now that the"
                "\n     flickering light is produced by a gas-lit lamp affixed to a log cabin.",
            },
            {
                "type": "displayText",
                "text": "     The cabin looks as though it has been there for centuries. It is"
                "\n     overgrown with vines, and the wood looks damp and rotten through. Still,\n     it stands.",
            },
            {
                "type": "displayText",
                "text": "     You climb the steps with caution, and open the door with reckless abandon.",
            },
            {
                "type": "displayText",
                "text": "     The interior is a stark contrast to the exterior. It is furnished, clean, and appears new.\n     Despite the cabin being made of wood, it houses a brick fireplace, which is lit.",
            },
            {
                "type": "displayText",
                "text": "     Huddled next to the fire is a girl. She is shivering, clearly quite cold.",
            },
            {
                "type": "displayText",
                "text": "     Now that you think about it, it is quite cold, isn't it?",
            },
            {
                "type": "choiceText",
                "text": "     [1] Join the girl by the fire\n     [2] Inspect the cabin",
            },
        ],
        1: {"actionItems": [{"type": "switchTo", "dict": "talkToGirlDict"}]},
        2: {"actionItems": [{"type": "switchTo", "dict": "inspectCabinDict"}]},
    },
    2: {  # Go deeper into the forest (branch placeholder)
        "actionItems": [
            {
                "type": "displayText",
                "text": "You wander deeper into the forest, the fog thickening as you proceed...",
            },
        ]
    },
}

beginEscapeDarkestDreamsDict = {
    "actionItems": [
        {"type": "displayText", "text": "     Abby writes 'eSCaPe?' into the dirt."},
        {
            "type": "choiceText",
            "text": "     [1] 'I was told there was a way to escape.'\n     [2] 'I know a way out.'",
        },
    ],
    1: {
        "actionItems": [
            {"type": "displayText", "text": "     Abby writes 'Where?'"},
            {"type": "displayText", "text": f"{name}: I don't know."},
            {"type": "displayText", "text": "Abby: 'STiCk TOgeTher?'"},
            {"type": "choiceText", "text": "     [1] 'Yes.'\n     [2] 'No.'"},
        ],
        1: {
            "actionItems": [
                {
                    "type": "displayText",
                    "text": "     Abby smiles at you painfully, the wires preventing her from forming\n     a full grin.",
                },
                {"type": "displayText", "text": "     There's only one way to go."},
                {
                    "type": "displayText",
                    "text": "     The two of you make your way through the forest in silence.",
                },
                {
                    "type": "displayText",
                    "text": "     There's a certain peace in this place. Maybe it's just because you're dead\n     but you do not fear the shadows of the trees or what could be inside them\n     lurking just beyond your vision.",
                },
                {
                    "type": "displayText",
                    "text": f"     Time doesn't seem to exist here either. What could {colored('The Judge', 'dark_grey')} have meant when he called\n     it {colored('The Darkest Dreams', 'blue', attrs=['bold'])}?",
                },
                {"type": "displayText", "text": "     ..."},
                {"type": "displayText", "text": "     Oh, that's what he meant."},
                {
                    "type": "displayText",
                    "text": "     The little amount of light inherent to this place flickers out.",
                },
                {"type": "displayText", "text": f"{name}: Abby? Where did you go?"},
                {
                    "type": "displayText",
                    "text": "     Your blindness now twofold, you reach out in front of you to feel your way around, discovering\n     you can see yourself just fine.",
                },
                {"type": "displayText", "text": f"{name}: ... Where did I go?"},
                {"type": "displayText", "text": "     A voice from behind speaks out."},
                {
                    "type": "displayText",
                    "text": colored("???: You're new. did ", color="blue")
                    + colored("Watch", color="red")
                    + colored(" send you here?", color="blue"),
                },
                {
                    "type": "displayText",
                    "text": "     You turn around to face your speaker. He, she... it? It is a humanoid with chains\n     for hair. It is shackled at the wrists, at the feet, and by the neck. The chains\n     fall into the water (?) below and disappear. It looks is malnourished, and wears\n     an unclasped straightjacket. Its eyes are blue and bloodshot, tears\n     streaming from them at an abnormal pace.",
                },
                {
                    "type": "displayText",
                    "text": f"     It approaches you. In attempting to step back you realise the same chains which dragged\n     you into {colored('The Darkest Dreams', 'blue', attrs=['bold'])} are coiled around your legs once more.",
                },
                {
                    "type": "displayText",
                    "speaker": "The Dispair",
                    "text": "???: But you look so...",
                },
                {
                    "type": "displayText",
                    "text": "     It raises its cold, chilling, bony hand and grabs your face to take a closer look,\n     looking directly into your eyes.",
                },
                {
                    "type": "displayText",
                    "speaker": "The Dispair",
                    "text": "???: Harmless.",
                },
                {
                    "type": "displayText",
                    "text": "     It digs its thumbnail into the skin below your eye and carves down.",
                },
                {
                    "type": "displayText",
                    "text": "     The light of the forest returns at once.",
                },
                {
                    "type": "displayText",
                    "text": "     You search for Abby, finding her frantically searching for you.",
                },
                {
                    "type": "displayText",
                    "text": "     When she sees you she rushes over to hug you.",
                },
                {
                    "type": "choiceText",
                    "text": "     [1] 'Were you scared?'\n     [2] Say nothing",
                },
                {
                    "type": "displayText",
                    "text": "     Abby points at the newly aquired scratch on your face and tilts her head.",
                },
                {
                    "type": "displayText",
                    "text": f"{name}: I went to a dark place that smelled like gasoline, and a shackled man cut me.",
                },
                {
                    "type": "displayText",
                    "text": "     You run your hand along the cut, and find your blood is blue.",
                },
                {"type": "displayText", "text": f"{name}: ... How?"},
                {
                    "type": "displayText",
                    "text": "     Abby finds a pointer end of her drawing stick and cuts her finger on it intentionally.\n     She then holds up her hand so you can see the wound.",
                },
                {"type": "displayText", "text": "     Her blood is yellow."},
                {
                    "type": "displayText",
                    "text": "     She then takes a nearby leaf and allows a drop of blood to fall onto it.",
                },
                {
                    "type": "displayText",
                    "text": "     The leaf absorbs the blood, forming cracks throughout its surface.",
                },
            ],
            1: {
                "actionItems": [
                    {"type": "displayText", "text": "     She nods her head."},
                    {"type": "displayText", "text": f"{name}: I'm sorry."},
                ]
            },
            2: {"actionItems": []},
        },
        2: {
            "actionItems": [
                {
                    "type": "displayText",
                    "text": "     Abby seems confused and irritated by this.",
                },
                {
                    "type": "displayText",
                    "text": "     She walks back into the cabin and closes the door behind her.",
                },
            ]
        },
    },
    2: {
        "actionItems": [
            {"type": "displayText", "text": "     Abby writes 'Where?'"},
            {
                "type": "choiceText",
                "text": "     [1] '...'\n     [2] 'Just follow me.'",
            },
        ],
        1: {
            "actionItems": [
                {"type": "displayText", "text": "     Abby will remember this."}
            ]
        },
        2: {
            "actionItems": [
                {
                    "type": "displayText",
                    "text": "     Abby seems suspicious of this, but it's not like she has anywhere else\n     to go.",
                }
            ]
        },
    },
}

outsideCabinDict = {
    "actionItems": [
        {
            "type": "choiceText",
            "text": "     [1] 'How did you die?'\n     [2] 'Do you want to escape with me?'",
        }
    ],
    1: {
        "actionItems": [
            {
                "type": "displayText",
                "text": "     Abby writes 'LUNaTiC' into the dirt.",
            },
            {
                "type": "choiceText",
                "text": "     [1] 'Who killed you?'\n     [2] 'Do you want to escape with me?'",
            },
        ],
        1: {
            "actionItems": [
                {
                    "type": "displayText",
                    "text": "     Abby slowly inscribes 'SALVATOre' into the dirt.",
                },
                {"type": "switchToSelf"},
            ]
        },
        2: {
            "actionItems": [
                {"type": "switchTo", "dict": "beginEscapeDarkestDreamsDict"}
            ]
        },
    },
    2: {"actionItems": [{"type": "switchTo", "dict": "beginEscapeDarkestDreamsDict"}]},
}

deadzoneDict = None

introDict2 = {
    "actionItems": [
        {
            "type": "displayText",
            "text": "JUDGE: Welcome to Gen V. You're blind, you're deaf, you're mute, and you're dead.",
        },
        {"type": "displayText", "text": "For now."},
        {
            "type": "displayText",
            "text": f"This is my Domain. This is {colored('The Deadzone', 'dark_grey')}.",
        },
        {
            "type": "displayText",
            "text": "     Before you lies field of brown grass, a blanket of grey clouds tempting rain."
            "\n     Dead trees and shrubbery dot the landscape, all the leaves long gone, and the insides hollow.",
        },
        {
            "type": "displayText",
            "text": "     The only approximation of life in this environment is the cold breeze which occassionally blows through,"
            "\n     sending shivers down your spine.",
        },
        {
            "type": "displayText",
            "text": "JUDGE: As you might have guessed, this is a sort of purgatory."
            "\nYou're not 'dead', death implies life, but dead is far easier to explain.",
        },
        {"type": "displayText", "text": "The dead ones do stop by, though."},
        {
            "type": "displayText",
            "text": "The important thing is that I can give you the opptrunity to come back from the dead.",
        },
        {"type": "displayText", "text": "     The wind disappears."},
        {"type": "displayText", "text": "JUDGE: Beyond that you're on your own."},
        {
            "type": "displayText",
            "speaker": "System",
            "text": f"SYSTEM: Hi! I'm SYSTEM, it's nice to meet you {name} ^^ I'll be providing you information throughout game.",
        },
        {
            "type": "displayText",
            "text": f"     {colored('WARNING!', 'yellow', attrs=['bold'])}",
        },
        {
            "type": "displayText",
            "speaker": "System",
            "text": "The choice you are about to make is PERMENANT and will FOREVER CHANGE the rest of the game.",
        },
        {
            "type": "displayText",
            "speaker": "System",
            "text": "It'll FOREVER CHANGE you as well.",
        },
        {
            "type": "displayText",
            "speaker": "System",
            "text": "I suppose you could say that about all your choices though,",
        },
        {"type": "displayText", "speaker": "System", "text": "couldn't you?"},
        {
            "type": "displayText",
            "text": f"JUDGE: I am {colored('The Judge', 'dark_grey')} of the afterlife, or in other words, I pass"
            "\njudgement on the souls which enter, and send them to one of three places.",
        },
        {
            "type": "displayText",
            "text": "You're special though. I do not have the ability to pass judgement upon you,"
            "\nbecause there is nothing to judge.",
        },
        {
            "type": "displayText",
            "text": f"And I could just send you to one of the afterlives at {colored('random', 'yellow')},",
        },
        {
            "type": "displayText",
            "text": f"or even {colored('eliminate', 'red')} you entierly,",
        },
        {
            "type": "displayText",
            "text": f"but since {colored('The Fallen', 'light_yellow')} likes you so much...",
        },
        {
            "type": "choiceText",
            "text": f"I'll let you choose:\n\n     {colored('[1] The Garden of Life', 'red', attrs=['bold'])}\n     {colored('[2] The World Ablaze', 'yellow', attrs=['bold'])}\n     {colored('[3] The Darkest Dreams', 'blue', attrs=['bold'])}\n\nJUDGE: Or, you know:\n\n     [4] Stay.",
        },
    ],
    1: {"actionItems": [{"type": "switchTo", "dict": gardenOfLifeDict}]},
    2: {"actionItems": [{"type": "switchTo", "dict": worldAblazeDict}]},
    3: {"actionItems": [{"type": "switchTo", "dict": darkestDreamsDict}]},
    4: {"actionItems": [{"type": "switchTo", "dict": deadzoneDict}]},
}

introDict = {
    "actionItems": [
        {
            "type": "displayImage",
            "path": "C:/Users/swftc/OneDrive/AlmostGone/ImageFiles/System.png",
        },
        {
            "type": "displayText",
            "speaker": "System",
            "text": "SYSTEM: Hey there, I'll see you in a bit, but for now,"
            "\n     I'm just here to give you some important information.",
        },
        {
            "type": "displayText",
            "speaker": "System",
            "text": "You can type 'h' to see all of the available commands at any time"
            "\n     and type 'q' to exit the game.",
        },
        {
            "type": "displayText",
            "speaker": "System",
            "text": "Have fun, and read carefully!",
        },
        {"type": "displayText", "text": f"???: Greetings, {name}."},
        {
            "type": "displayText",
            "text": "???: It is truly unfortunate that you have chosen to play this game,"
            "\nbut I can't stop you.",
        },
        {
            "type": "displayText",
            "text": f"JUDGE: My Title is {colored('The Judge', 'dark_grey')}.",
        },
        {
            "type": "displayImage",
            "path": "C:/Users/swftc/OneDrive/AlmostGone/ImageFiles/TheDeadzoneWithJudge.png",
        },
        {
            "type": "displayText",
            "text": "     It is humanoid, but only possesses the head, arms, and heart. The heart, which is entirely exposed,"
            "\n     slowly pulses, pushing a bioluminescent yellow fluid up through its equally exposed veins"
            "\n     and into its extremities.",
        },
        {
            "type": "displayText",
            "text": f"     Perhaps the slow heartbeat indicates that this thing-\n{colored('     The Judge', 'dark_grey')}-\n     is calm.",
        },
        {
            "type": "displayText",
            "text": f"     Its three eye sockets are inlain with {colored('heter', 'red')}{colored('ochro', 'yellow')}{colored('matic', 'blue')} gems,"
            "\n     and it bears no mouth- yet the sound reaches you nonetheless.",
        },
        {
            "type": "displayText",
            "text": f"     Even if you really couldn't hear it speak,\n     you could {colored('feel', attrs=['bold'])} it speak.",
        },
        {
            "type": "choiceText",
            "text": "JUDGE: The first thing you will need to do is make a choice:\n\n     [1] Play\n     [2] Perish",
        },
    ],
    1: {
        "actionItems": [
            {
                "type": "choiceText",
                "text": "JUDGE: You'd really be better off leaving, are you sure?\n\n     [1] 'Yes, I am sure'\n     [2] 'No, I choose to perish'",
            }
        ],
        1: {
            "actionItems": [
                {
                    "type": "displayText",
                    "text": f"JUDGE: Well, that's a {colored('shame', 'blue')}.",
                },
                {"type": "switchTo", "dict": introDict2},
            ]
        },
        2: {"actionItems": [{"type": "switchTo", "dict": introDict2}]},
    },
    2: {
        "actionItems": [
            {"type": "displayText", "text": f"JUDGE: {colored('Hahaha', 'yellow')},"},
            {
                "type": "displayText",
                "text": "     The laugh is deep, and genuine. It makes it sound as though it has weathered every summer,"
                "\n     and every winter. It says 'I have lived, but I have also died"
                "\n     a thousand times.'",
            },
            {
                "type": "displayText",
                "text": "JUDGE: I was just kidding with you. You're already dead. Well- somewhat, anyway.",
            },
            {"type": "switchTo", "dict": introDict2},
        ]
    },
}

incomplete = {
    "actionItems": [
        {
            "type": "displayText",
            "speaker": "System",
            "text": "     Unfortunately the developer hasn't put anything here. A shame, but he'll get around to it! ^^",
        }
    ]
}


def showImage(path):
    subprocess.Popen([sys.executable, "show_image.py", path])


def evaluateCommand(input):
    if input == "q":
        quit()
    elif input == "h":
        printSystem(
            "\n     Available commands:\n\n     [h] Display commands\n     [q] Quit the game"
        )
    else:
        return False


outerDict = None


def playStory(dict, isOuterDict, textDisplayed):
    global outerDict
    if isOuterDict:
        outerDict = dict
    for innerDict in dict["actionItems"]:
        if innerDict["type"] == "displayText" and not textDisplayed:
            try:
                if innerDict["speaker"] == "System":
                    print("\n     " + colored(innerDict["text"], "light_magenta"))
                if innerDict["speaker"] == "The Dispair":
                    print("\n     " + colored(innerDict["text"], "Blue"))
            except:
                print("\n" + innerDict["text"])
            print(colored("\n> ", "light_green"), end="")
            tempo = input()
            evaluateCommand(tempo)

        if innerDict["type"] == "choiceText":
            print("\n" + innerDict["text"])
            print(colored("\n> ", "light_green"), end="")
            choice = input()
            try:
                if int(choice) in dict:
                    playStory(dict[int(choice)], False, False)
                else:
                    print("\nInvalid input.")
                    playStory(dict, False, True)
            except:
                if not evaluateCommand(choice):
                    print("\nInvalid input.")
                playStory(dict, False, True)

        if innerDict["type"] == "switchTo":
            target_dict_name = innerDict["dict"]
            target_dict = (
                globals()[target_dict_name]
                if isinstance(target_dict_name, str)
                else target_dict_name
            )
            playStory(target_dict, True, False)
        if innerDict["type"] == "switchToSelf":
            return playStory(outerDict, False, True)
        if innerDict["type"] == "displayImage":
            showImage(innerDict["path"])


playStory(introDict, True, False)

