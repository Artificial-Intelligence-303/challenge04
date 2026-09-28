"""A game of Clue, as a knowledge base in propositional logic.

**You implement two functions in this file**, `exactly_one` and
`encode_turn`. Everything else is provided. Add anything else you use from
`logic` to the import below.

The case file holds one suspect, one weapon, and one room. Each card gets
one symbol, and a symbol is true when that card is in the case file:
`Symbol("grace")` means "Grace did it", `Symbol("cable")` means "it was the
cable". You are one of the players, and `TRANSCRIPT` is everything you saw
happen in one game, in order.
"""

from dataclasses import dataclass

from logic import And, Not, Sentence, Symbol, model_check

SUSPECTS = ["ada", "alan", "edsger", "grace"]
WEAPONS = ["cable", "keyboard", "mug", "stapler"]
ROOMS = ["lab", "library", "lounge", "office"]
CARDS = SUSPECTS + WEAPONS + ROOMS


@dataclass
class Turn:
    """One thing you saw happen, and the cards it involved.

    `kind` is one of three:

    - `"hold"`: these cards were dealt to you, so you are looking at them.
    - `"shown"`: another player showed you this one card, to disprove a
      suggestion you made.
    - `"refuted"`: another player made this suggestion, and somebody
      showed them one of these three cards. You saw that a card changed
      hands, but not which one.
    """

    kind: str
    cards: list[str]

    def describe(self) -> str:
        """Say what happened in words, for `main.py` to print."""
        names = ", ".join(self.cards)
        if self.kind == "hold":
            return f"You are dealt {names}"
        if self.kind == "shown":
            return f"A player shows you {names}"
        return (
            f"Someone refutes a suggestion of {names}; you do not see the card"
        )


TRANSCRIPT = [
    Turn("hold", ["ada", "stapler", "lab"]),
    Turn("refuted", ["alan", "cable", "library"]),
    Turn("shown", ["edsger"]),
    Turn("refuted", ["grace", "mug", "office"]),
    Turn("shown", ["keyboard"]),
    Turn("shown", ["lounge"]),
    Turn("shown", ["mug"]),
    Turn("shown", ["office"]),
]


def exactly_one(names: list[str]) -> Sentence:
    """Build a sentence that is true when exactly one of `names` is true.

    The case file holds one suspect: at least one suspect symbol is true,
    and no two of them are true together. Build both halves and join them.

    Args:
        names: The symbol names, at least one of them.

    Returns:
        A sentence true in exactly the models where one name is true and
        every other name is false.
    """
    # TODO: implement this
    raise NotImplementedError


def encode_turn(turn: Turn) -> Sentence:
    """Translate one turn of the transcript into a sentence.

    Say only what the turn tells you about the case file, and nothing it
    does not.

    Args:
        turn: One entry of `TRANSCRIPT`.

    Returns:
        A sentence that is true in exactly the models the turn allows.
    """
    # TODO: implement this
    raise NotImplementedError


def game_rules() -> Sentence:
    """Return what every player knows before the first card is dealt."""
    return And(exactly_one(SUSPECTS), exactly_one(WEAPONS), exactly_one(ROOMS))


def knowledge_after(turns: int) -> Sentence:
    """Return the knowledge base after the first `turns` turns.

    Args:
        turns: How many entries of `TRANSCRIPT` to include. Zero gives the
            rules alone.

    Returns:
        The rules joined with every encoded turn up to that point.
    """
    knowledge = And(game_rules())
    for turn in TRANSCRIPT[:turns]:
        knowledge.add(encode_turn(turn))
    return knowledge


def status(knowledge: Sentence, card: str) -> str:
    """Say what the knowledge base tells you about one card.

    Args:
        knowledge: The knowledge base to ask.
        card: The card's name.

    Returns:
        "YES" if the card must be in the case file, "NO" if it cannot be,
        "MAYBE" if the knowledge allows either, and "CONTRADICTION" if the
        knowledge base entails both, which only happens when it has no
        model at all.
    """
    yes = model_check(knowledge, Symbol(card))
    no = model_check(knowledge, Not(Symbol(card)))
    if yes and no:
        return "CONTRADICTION"
    if yes:
        return "YES"
    if no:
        return "NO"
    return "MAYBE"
