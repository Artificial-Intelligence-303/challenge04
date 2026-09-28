"""Propositional logic: sentences, models, and model checking.

Provided. You do not change this file, but you use every class in it.

A **sentence** is built from symbols and connectives. A **model** is one
assignment of True or False to every symbol, stored here as a dictionary
from symbol name to bool. A knowledge base **entails** a query when the
query is true in every model where the knowledge base is true, and
`model_check` decides that by trying every model there is.

    >>> rain = Symbol("rain")
    >>> wet = Symbol("wet")
    >>> knowledge = And(Implication(rain, wet), rain)
    >>> model_check(knowledge, wet)
    True
"""

import itertools
from collections.abc import Iterator

Model = dict[str, bool]


class Sentence:
    """Anything that is true or false in a given model."""

    def evaluate(self, model: Model) -> bool:
        """Return whether this sentence is true in `model`.

        Args:
            model: A truth value for every symbol this sentence mentions.

        Returns:
            True if the sentence holds in that model.
        """
        raise NotImplementedError

    def formula(self) -> str:
        """Return the sentence written out with logical connectives."""
        raise NotImplementedError

    def symbols(self) -> set[str]:
        """Return the name of every symbol this sentence mentions."""
        raise NotImplementedError

    def __repr__(self) -> str:
        """Show the sentence as its formula."""
        return self.formula()


class Symbol(Sentence):
    """A single proposition, such as "the pencil is in the case file"."""

    def __init__(self, name: str) -> None:
        """Name the proposition.

        Args:
            name: The symbol's name, used as its key in a model.
        """
        self.name = name

    def evaluate(self, model: Model) -> bool:
        """Look the symbol up in the model."""
        return model[self.name]

    def formula(self) -> str:
        """Return the symbol's name."""
        return self.name

    def symbols(self) -> set[str]:
        """Return a set holding only this symbol's name."""
        return {self.name}


class Not(Sentence):
    """True exactly when the sentence inside it is false."""

    def __init__(self, operand: Sentence) -> None:
        """Negate one sentence.

        Args:
            operand: The sentence being negated.
        """
        self.operand = operand

    def evaluate(self, model: Model) -> bool:
        """Return the opposite of the operand's value."""
        return not self.operand.evaluate(model)

    def formula(self) -> str:
        """Return the negation, written with ¬."""
        return f"¬{self.operand.formula()}"

    def symbols(self) -> set[str]:
        """Return the operand's symbols."""
        return self.operand.symbols()


class And(Sentence):
    """True when every sentence inside it is true."""

    def __init__(self, *conjuncts: Sentence) -> None:
        """Join any number of sentences with "and".

        Args:
            *conjuncts: The sentences that must all hold.
        """
        self.conjuncts = list(conjuncts)

    def add(self, conjunct: Sentence) -> None:
        """Add one more sentence that must hold.

        Args:
            conjunct: The sentence to add.
        """
        self.conjuncts.append(conjunct)

    def evaluate(self, model: Model) -> bool:
        """Return True if every conjunct is true."""
        return all(c.evaluate(model) for c in self.conjuncts)

    def formula(self) -> str:
        """Return the conjunction, written with ∧."""
        return "(" + " ∧ ".join(c.formula() for c in self.conjuncts) + ")"

    def symbols(self) -> set[str]:
        """Return every symbol any conjunct mentions."""
        return set().union(*(c.symbols() for c in self.conjuncts))


class Or(Sentence):
    """True when at least one sentence inside it is true."""

    def __init__(self, *disjuncts: Sentence) -> None:
        """Join any number of sentences with "or".

        Args:
            *disjuncts: The sentences of which at least one must hold.
        """
        self.disjuncts = list(disjuncts)

    def evaluate(self, model: Model) -> bool:
        """Return True if any disjunct is true."""
        return any(d.evaluate(model) for d in self.disjuncts)

    def formula(self) -> str:
        """Return the disjunction, written with ∨."""
        return "(" + " ∨ ".join(d.formula() for d in self.disjuncts) + ")"

    def symbols(self) -> set[str]:
        """Return every symbol any disjunct mentions."""
        return set().union(*(d.symbols() for d in self.disjuncts))


class Implication(Sentence):
    """False only when the antecedent is true and the consequent false."""

    def __init__(self, antecedent: Sentence, consequent: Sentence) -> None:
        """Build "if antecedent, then consequent".

        Args:
            antecedent: The "if" part.
            consequent: The "then" part.
        """
        self.antecedent = antecedent
        self.consequent = consequent

    def evaluate(self, model: Model) -> bool:
        """Return False only for a true antecedent and false consequent."""
        return (
            not self.antecedent.evaluate(model)
        ) or self.consequent.evaluate(model)

    def formula(self) -> str:
        """Return the implication, written with →."""
        return f"({self.antecedent.formula()} → {self.consequent.formula()})"

    def symbols(self) -> set[str]:
        """Return the symbols on both sides."""
        return self.antecedent.symbols() | self.consequent.symbols()


def all_models(names: list[str]) -> Iterator[Model]:
    """Yield every model over the given symbol names, one at a time.

    There are 2 ** len(names) of them.

    Args:
        names: The symbols to assign.

    Yields:
        One dictionary per combination of True and False.
    """
    for values in itertools.product([True, False], repeat=len(names)):
        yield dict(zip(names, values))


def model_check(knowledge: Sentence, query: Sentence) -> bool:
    """Return whether `knowledge` entails `query`.

    Tries every model over every symbol either sentence mentions. If any
    model makes the knowledge true and the query false, the knowledge does
    not entail the query. If no model does, it does.

    Args:
        knowledge: What the agent knows, as one sentence.
        query: The sentence being asked about.

    Returns:
        True if the query holds in every model of the knowledge.
    """
    names = sorted(knowledge.symbols() | query.symbols())
    for model in all_models(names):
        if knowledge.evaluate(model) and not query.evaluate(model):
            return False
    return True
