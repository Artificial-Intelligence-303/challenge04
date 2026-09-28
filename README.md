# Challenge 4: Clue

|                    |                                             |
| :----------------- | :------------------------------------------ |
| `Tuesday 29 Sep`   | Released, in class                          |
| `Tuesday 6 Oct`    | Due at 2:30pm, the start of lab             |
| `Tuesday 6 Oct`    | Verbal checks, during that same lab session |
| Points             | 3                                           |

A knowledge-based agent writes down what it knows as sentences, and asks
whether a question follows from them. In this
challenge the agent is you, playing Clue: every turn you see adds a
sentence, and `model_check` tells you which cards must be in the case file,
which cannot be, and which are still open.

You write the part that turns the game into sentences. The logic engine
and the game transcript are provided.

## Course learning outcomes

1. **Outcome 3.** Design, implement, and assess an intelligent system. You
   build the knowledge base for a logic-based agent and assess what it can
   and cannot conclude after each turn, and what checking it costs.

## The game

The case file holds one suspect, one weapon, and one room. Every other card
is dealt to a player.

| Suspects | Weapons  | Rooms   |
| :------- | :------- | :------ |
| ada      | cable    | lab     |
| alan     | keyboard | library |
| edsger   | mug      | lounge  |
| grace    | stapler  | office  |

Each card is one symbol, true when that card is in the case file.
`TRANSCRIPT` in `src/clue.py` is what you saw during one game, as three
kinds of turn:

- **`hold`**: cards dealt to you.
- **`shown`**: a card another player showed you.
- **`refuted`**: another player's suggestion of three cards was refuted,
  and you did not see which card was shown.

## What you implement

Two functions in `src/clue.py`. Everything else is provided.

### 1. `exactly_one(names)`

Return a sentence that is true when exactly one of the named symbols is
true. `game_rules` uses it three times, once per kind of card.

### 2. `encode_turn(turn)`

Return a sentence that says what one turn tells you about the case file,
and nothing more.

Build both from the classes in `src/logic.py`: `Symbol`, `Not`, `And`,
`Or`, `Implication`. Read its docstring first; the example at the top shows
every piece you need.

## Running it

```
uv run python src/main.py           replay the game, one board per turn
uv run python src/main.py rules     print the rules and every turn as formulas
uv run pytest                       run the tests
uv run ruff check src tests         check your style
uv run ruff format src tests        fix most style problems automatically
uv run gatorgrade                   run the checks the way they are graded
```

`main.py` prints YES, NO or MAYBE for every card after every turn, and marks
what that turn changed with `*`. If it prints `CONTRADICTION`, one of your
sentences rules out every possible case file; `rules` shows which.

## Style

Same as last time: the [Google Python Style
Guide](https://google.github.io/styleguide/pyguide.html), checked by
`uv run ruff check src tests`.

## Evaluation

This challenge is worth **3 points**.

| Component                 | Value   |
| :------------------------ | :------ |
| Programming               | 1       |
| Written reflection        | 1       |
| Verbal check              | 1       |
| **Total**                 | **3**   |

### Programming, 1 point

Run by `gatorgrade`, awarded as the fraction of the **code** checks that
pass. These are:

- `exactly_one` is true with one name true, and false with none or two.
- `encode_turn` rules out the cards you hold and the cards you are shown,
  and says of a refuted suggestion exactly what the turn tells you.
- Replayed turn by turn, the game settles what it should when it should,
  and no turn leaves the knowledge base contradicting itself.
- Style passes `ruff` and type annotations check out under `mypy`.
- No `TODO` markers are left in `src/clue.py`.

The checks compare what your sentences mean, not how you wrote them, so any
correct way of writing one passes.

`gatorgrade` also runs two checks on `docs/summary.md`. Those belong to the
reflection below, not to this point.

Autograder results are preliminary. The final grade is determined by the
instructor.

### Written reflection, 1 point

Complete `docs/summary.md`. Two questions and the disclosure, **200 words
minimum across all of them**. You are graded on whether the reasoning is
correct and specific to what your run printed, not on length.

### Verbal check, 1 point

During lab you answer two or three questions about your own code, in the
context of this assignment. Nothing to prepare beyond understanding what
you wrote.

## AI use on this challenge

Full policy: **[AI in this course](https://areweagentsyet.com/ai/)**. AI
tools are allowed here, you disclose them, and you have to be able to
explain what you submit.

> ### The skill this time: make it show its work against a spec
>
> A sentence in logic means the set of models where it is true. When a
> tool hands you a sentence, ask it for those models, and check each one
> against what the turn actually says happened. A sentence that reads
> plausibly and allows the wrong case files is still wrong.

Concretely, for this assignment:

- **Write `exactly_one` and `encode_turn` yourself.** They are this week's
  idea.
- **`uv run python src/main.py rules` is your spec check.** It prints every
  sentence your code builds. Read each one against the turn it came from.
- **A tool is useful** for the Python around the logic: what `*symbols`
  does in a call, or how `enumerate` pairs items.

## How this assignment was built

You are asked below to disclose your AI use, so here is mine.

I decided the shape: a Clue transcript you encode rather than a logic
engine you write, three kinds of turn, and a game where one card is only
ever settled by the refuted suggestion from turn 2.

I used Claude to draft `logic.py`, the tests and `main.py`, and to check
that the transcript settles each card on the turn it should. I ran the
reference solution and the unfinished starter against every check, and
checked the checks against wrong encodings, not only against an empty one.
The wording throughout is mine.

## Disclosing your AI use

At the end of `docs/summary.md` there is a disclosure section. Answer three
things, a sentence or two each:

1. **Which tool.** Name it. If you used more than one, name each.
2. **What you used it for.** Which part of the assignment.
3. **What you did with what it gave you.** Accepted it, edited it, checked
   it against something, or threw it out.

**If you did not use any tool, write that.** That is a complete and
perfectly good answer.

Disclosing costs you nothing. There is no version of this where naming a
tool loses you points.
