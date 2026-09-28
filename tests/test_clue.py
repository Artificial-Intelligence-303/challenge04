"""Checks for Challenge 4.

Readable on purpose. If a check fails, read the test: it says in words what
your code was supposed to do.

The checks on `exactly_one` and `encode_turn` compare what your sentence
means, not how you wrote it. Two sentences mean the same thing when they
are true in exactly the same models, so any correct way of writing a
sentence passes.
"""

from clue import (
    CARDS,
    TRANSCRIPT,
    Turn,
    encode_turn,
    exactly_one,
    knowledge_after,
    status,
)
from logic import And, Not, Or, Sentence, Symbol, all_models


def same_meaning(first: Sentence, second: Sentence) -> bool:
    """Return whether two sentences are true in exactly the same models."""
    names = sorted(first.symbols() | second.symbols())
    return all(
        first.evaluate(model) == second.evaluate(model)
        for model in all_models(names)
    )


def only(true_names: list[str], names: list[str]) -> dict[str, bool]:
    """Return the model where exactly `true_names` are true."""
    return {name: name in true_names for name in names}


FOUR = ["ada", "alan", "edsger", "grace"]


def test_exactly_one_is_true_when_one_name_is_true() -> None:
    """Each single suspect on their own satisfies the rule."""
    sentence = exactly_one(FOUR)
    for name in FOUR:
        assert sentence.evaluate(only([name], FOUR)), name


def test_exactly_one_is_false_when_no_name_is_true() -> None:
    """The case file cannot be missing its suspect."""
    assert not exactly_one(FOUR).evaluate(only([], FOUR))


def test_exactly_one_is_false_when_two_names_are_true() -> None:
    """Two suspects in the case file breaks the rule: at most one."""
    assert not exactly_one(FOUR).evaluate(only(["ada", "grace"], FOUR))


def test_exactly_one_is_right_in_every_model() -> None:
    """All sixteen models over four names, not only the ones above."""
    sentence = exactly_one(FOUR)
    for model in all_models(FOUR):
        assert sentence.evaluate(model) == (sum(model.values()) == 1), model


def test_exactly_one_of_a_single_name_is_that_name() -> None:
    """With one name to choose from, that name must be true."""
    assert same_meaning(exactly_one(["mug"]), Symbol("mug"))


def test_a_card_you_hold_is_not_in_the_case_file() -> None:
    """Every card in your hand is ruled out."""
    turn = Turn("hold", ["ada", "stapler", "lab"])
    expected = And(
        Not(Symbol("ada")), Not(Symbol("stapler")), Not(Symbol("lab"))
    )
    assert same_meaning(encode_turn(turn), expected)


def test_a_card_you_are_shown_is_not_in_the_case_file() -> None:
    """A card somebody showed you is in their hand, not the case file."""
    assert same_meaning(encode_turn(Turn("shown", ["mug"])), Not(Symbol("mug")))


def test_a_refuted_suggestion_rules_out_at_least_one_card() -> None:
    """At least one of the three is not in the case file."""
    turn = Turn("refuted", ["alan", "cable", "library"])
    expected = Or(
        Not(Symbol("alan")), Not(Symbol("cable")), Not(Symbol("library"))
    )
    assert same_meaning(encode_turn(turn), expected)


def test_a_refuted_suggestion_does_not_rule_out_all_three() -> None:
    """Two of the three can still be in the case file: you saw one card."""
    names = ["alan", "cable", "library"]
    sentence = encode_turn(Turn("refuted", names))
    assert sentence.evaluate(only(["cable", "library"], names))


def test_a_refuted_suggestion_allows_none_of_its_cards() -> None:
    """The turn never says any of the three is in the case file."""
    names = ["alan", "cable", "library"]
    sentence = encode_turn(Turn("refuted", names))
    assert sentence.evaluate(only([], names))


def test_the_rules_alone_settle_nothing() -> None:
    """Before any turn, every card is possible."""
    knowledge = knowledge_after(0)
    assert all(status(knowledge, card) == "MAYBE" for card in CARDS)


def test_a_refuted_suggestion_alone_settles_none_of_its_cards() -> None:
    """After turn 2, Alan, the cable, and the library are all still MAYBE."""
    knowledge = knowledge_after(2)
    for card in TRANSCRIPT[1].cards:
        assert status(knowledge, card) == "MAYBE", card


def test_no_turn_leaves_the_knowledge_base_contradicting_itself() -> None:
    """Every turn describes a real game, so some model always survives."""
    for turns in range(len(TRANSCRIPT) + 1):
        knowledge = knowledge_after(turns)
        assert any(knowledge.evaluate(m) for m in all_models(CARDS)), turns


def test_the_weapon_is_known_after_turn_7() -> None:
    """Three weapons ruled out leaves the cable, though nobody showed it."""
    assert status(knowledge_after(7), "cable") == "YES"


def test_the_case_is_solved_after_turn_8() -> None:
    """Grace, the cable, and the library; every other card ruled out."""
    knowledge = knowledge_after(8)
    solution = {"grace", "cable", "library"}
    for card in CARDS:
        expected = "YES" if card in solution else "NO"
        assert status(knowledge, card) == expected, card
