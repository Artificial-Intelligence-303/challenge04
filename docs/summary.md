# Challenge 4 Reflection

Answer both questions. **200 words minimum across the whole document.**
You are graded on whether the reasoning is correct and specific to what
your own run printed. Replace every `TODO` before you submit.

Run `uv run python src/main.py` before you start writing. Everything these
questions ask about is in its output.

---

> **1. Explain turn 8.**
>
> Turn 8 shows you one card, the office. Four cards change status after it.
> The office is the one you were shown. For each of the other three, name
> the earlier sentences it follows from: which turn, or which half of
> `exactly_one`. Nobody ever showed you any of those three cards.

TODO

---

> **2. What model checking costs.**
>
> `main.py` reports how many symbols the game has, how many models
> `model_check` tries per question, how many questions it asked, and how
> long that took.
>
> A full game of Clue has 6 suspects, 6 weapons, and 9 rooms. How many
> models would `model_check` try per question, and how many times more is
> that than yours? Using your own measured time, estimate how long the same
> eight turns would take to replay at that size.
>
> Then: `model_check` can stop as soon as it finds one model where the
> knowledge is true and the query is false. Explain why it can never stop
> early when the answer is YES.

TODO

---

> **AI tool disclosure**
>
> State what AI tools you used on this challenge, if any, and what they
> did. "None" is a complete answer if it is true. Be specific: "I used X to
> explain what a refuted suggestion means" and "I used X to write
> `encode_turn`" are very different disclosures.

TODO
