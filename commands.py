def processCommand(command):

    if command == "h":
        print("\nAvailable commands:\n")
        print("     h - Show this help message")
        print("     q - Quit the game")
        print("     s - Save the game (not implemented yet)")
        print("     l - Load the game (not implemented yet)")
        print("     c - Clear the screen (not implemented yet)", end="")
        return "h"
    elif command == "q":
        return "q"
    elif command == "s":
        # import pickle # you may or may not need to install this
        return False
    else:
        return command
