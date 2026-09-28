"""Replay the transcript and print what you know after every turn.

Provided. Run it once `exactly_one` and `encode_turn` are written.

    uv run python src/main.py            every turn, and what changed
    uv run python src/main.py rules      the rules and each turn as formulas
"""

import sys
import time

from clue import (
    CARDS,
    ROOMS,
    SUSPECTS,
    TRANSCRIPT,
    WEAPONS,
    encode_turn,
    game_rules,
    knowledge_after,
    status,
)


def show_board(known: dict[str, str], changed: set[str]) -> None:
    """Print every card's status, one row per category.

    Args:
        known: Each card's status after this turn.
        changed: The cards whose status this turn changed, marked with *.
    """
    for label, cards in (
        ("suspect", SUSPECTS),
        ("weapon", WEAPONS),
        ("room", ROOMS),
    ):
        cells = []
        for card in cards:
            mark = "*" if card in changed else " "
            cells.append(f"{card:>9} {known[card]:<5}{mark}")
        print(f"  {label:<8}" + "".join(cells))


def replay() -> None:
    """Print the board after the rules alone, then after every turn."""
    before = {card: "MAYBE" for card in CARDS}
    questions = 0
    started = time.perf_counter()
    for turns in range(len(TRANSCRIPT) + 1):
        knowledge = knowledge_after(turns)
        after = {card: status(knowledge, card) for card in CARDS}
        questions += 2 * len(CARDS)
        changed = {card for card in CARDS if after[card] != before[card]}
        if turns == 0:
            print("\nBefore any turn: the rules alone")
        else:
            print(f"\nTurn {turns}: {TRANSCRIPT[turns - 1].describe()}")
        show_board(after, changed)
        if "CONTRADICTION" in after.values():
            print(
                "\n  The knowledge base has no model left: some sentence"
                " says something the game did not."
            )
            return
        before = after
    elapsed = time.perf_counter() - started

    models = 2 ** len(CARDS)
    print(
        f"\n{len(CARDS)} symbols, so {models:,} models per question."
        f"\n{questions} questions asked, in {elapsed:.1f} seconds."
    )


def show_rules() -> None:
    """Print the rules and every encoded turn as formulas."""
    print(f"\nRules:\n  {game_rules().formula()}")
    for number, turn in enumerate(TRANSCRIPT, start=1):
        print(f"\nTurn {number}: {turn.describe()}")
        print(f"  {encode_turn(turn).formula()}")


if __name__ == "__main__":
    if sys.argv[1:] == ["rules"]:
        show_rules()
    else:
        replay()
