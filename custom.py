"""Game-specific functions, enums, and classes for this text adventure.

The framework files (common_classes.py, player_class.py) stay generic. Content
that belongs to one story lives here instead and is imported by that story:

    from custom import Aspect, AspectItem, print_favor

"""

from enum import Enum

from termcolor import colored

from common_classes import Item
from player_class import Player


class Aspect(Enum):
    SORROW = "sorrow"
    ANGER = "anger"
    HAPPINESS = "happiness"


# Aspect-to-Color Mapping
aspectColors = {
    Aspect.SORROW: "blue",
    Aspect.ANGER: "red",
    Aspect.HAPPINESS: "yellow",
}


def print_favor(aspect: Aspect, player_color: str):
    """Print the "an aspect smiles upon you" beat and wait for input."""
    print(
        colored(f"\n     {aspect.name} ", aspectColors[aspect], attrs=["bold"])
        + colored("smiles upon you.", player_color)
        + colored("\n\n> ", "light_green")
    )
    input()


class AspectItem(Item):
    """An item whose name is colored by the aspect it belongs to."""

    def __init__(
        self,
        name: str,
        add_health,
        add_damage,
        add_defense,
        knowledge,
        discover_message: str,
        keepable: bool,
        aspect: Aspect | None = None,
    ):
        super().__init__(
            name,
            add_health,
            add_damage,
            add_defense,
            knowledge,
            discover_message,
            keepable,
        )
        self.aspect = aspect

    def get_item_color(self) -> str | None:
        return aspectColors.get(self.aspect)


class AlignedPlayer(Player):
    """A player carrying an aspect alignment and its breakthrough points."""

    def __init__(
        self,
        name: str,
        player_color: str = "light_grey",
        aspect: Aspect | None = None,
    ):
        super().__init__(name, player_color)

        self.alignment = None
        self.happiness_bp = 0
        self.anger_bp = 0
        self.sorrow_bp = 0
        self.apply_alignment(aspect)

    def apply_alignment(self, aspect: Aspect | None):
        """Adopt an aspect, recolor the player, and bank a breakthrough point."""
        self.alignment = aspect

        if aspect is None:
            self.player_color = "light_grey"
            return

        self.player_color = aspectColors[aspect]
        if aspect is Aspect.ANGER:
            self.anger_bp += 1
        elif aspect is Aspect.HAPPINESS:
            self.happiness_bp += 1
        elif aspect is Aspect.SORROW:
            self.sorrow_bp += 1


class Favor:
    """Story beat that aligns the player and plays the aspect's favor message."""

    def __init__(self, aspect: Aspect):
        self.aspect = aspect

    def do(self, player, _place):
        if isinstance(player, AlignedPlayer):
            player.apply_alignment(self.aspect)
        print_favor(self.aspect, player.player_color)
        return 1


# state.py builds the global player from this name. Point it at Player to use
# the plain framework player, or at your own Player subclass.
PLAYER_CLASS = AlignedPlayer
