# API reference

Everything below is importable straight from the package root:

```python
from pronomial import (
    PronomialCoreferenceSolver,
    replace_corefs,
    link_pronouns,
    score_corefs,
    detect_nouns,
    normalize,
    word_tokenize,
    pos_tag,
    predict_gender,
    is_plural,
)
```

The module-level functions (`replace_corefs`, `link_pronouns`, `score_corefs`,
`detect_nouns`, `normalize`) are thin wrappers over the matching
`PronomialCoreferenceSolver` methods — use whichever style you prefer; they take
the same arguments and return the same shapes.

Every call accepts a `lang` argument as a BCP-47 code (`"en"`, `"pt"`, `"es"`,
`"ca"`, or regional variants like `"pt-PT"`); only the part before `-` is read.

## Coreference functions

### `replace_corefs(text, lang="en") -> str`

Resolve every pronoun and return the text with each one replaced by its
top-scoring antecedent. The result is space-tokenized (punctuation separated).

```python
from pronomial import replace_corefs

replace_corefs("Anna lost her keys. She found them later.", lang="en")
# 'Anna lost Anna keys . Anna found them later .'
```

### `link_pronouns(text, lang="en", return_idx=True) -> list`

Return the chosen `(pronoun, antecedent, score)` link for each pronoun.

- `return_idx=True` (default): triples of token *indices*
  `(pronoun_idx, antecedent_idx, score)`.
- `return_idx=False`: triples of the token *strings*.

```python
from pronomial import link_pronouns

text = ("London has been a major settlement for two millennia. "
        "It was founded by the Romans, who named it Londinium.")

link_pronouns(text, lang="en")
# [(10, 0, 0.56), (17, 15, 0.7), (19, 0, 0.56)]

link_pronouns(text, lang="en", return_idx=False)
# [('It', 'London', 0.56), ('who', 'Romans', 0.7), ('it', 'London', 0.56)]
```

Indices line up with `word_tokenize(text)`. This is the same as
`PronomialCoreferenceSolver.solve_corefs`.

### `score_corefs(text, lang="en") -> dict`

The full scored candidate table — the raw material `link_pronouns` picks from.
Maps each pronoun's token index to a `{antecedent_idx: score}` dict. Scores for a
given pronoun are normalized to sum to roughly `1.0`; zero-score candidates are
dropped.

```python
from pronomial import score_corefs, word_tokenize

text = ("London has been a major settlement for two millennia. "
        "It was founded by the Romans, who named it Londinium.")

score_corefs(text, lang="en")
# {10: {0: 0.56, 5: 0.06, 8: 0.39},
#  17: {5: 0.02, 8: 0.28, 15: 0.7},
#  19: {0: 0.56, 5: 0.06, 8: 0.39}}

tokens = word_tokenize(text)
scores = score_corefs(text, lang="en")
for pron_idx, cands in scores.items():
    for ante_idx, score in cands.items():
        print(tokens[pron_idx], "->", tokens[ante_idx], score)
# It -> London 0.56
# It -> settlement 0.06
# It -> millennia 0.39
# ...
```

### `detect_nouns(text, lang="en", return_idx=True) -> dict`

Bucket the nouns of a sentence by the role they can play as antecedents. Returns
a dict whose values are token indices (or token strings when
`return_idx=False`), plus a `"tokens"` key holding the full token list.

Buckets: `male`, `female`, `first`, `neutral`, `plural`, `subject`,
`verb_subject`.

```python
from pronomial import detect_nouns

nouns = detect_nouns(
    "London has been a major settlement for two millennia. "
    "It was founded by the Romans, who named it Londinium.",
    lang="en", return_idx=False,
)
nouns["male"]          # ['London', 'Londinium']
nouns["plural"]        # ['Romans']
nouns["verb_subject"]  # ['London']
```

A noun can appear in several buckets at once; the scorer uses these
memberships to award gender, plurality, and subject bonuses.

### `normalize(text) -> str`

Tokenize and re-join with single spaces — the same normalization the solver
applies internally. Useful for comparing your input against resolved output.

```python
from pronomial import normalize

normalize("It was founded by the Romans.")
# 'It was founded by the Romans .'
```

## The class

### `PronomialCoreferenceSolver`

All methods are `@staticmethod`/`@classmethod`, so you call them on the class
without instantiating it. They mirror the functions above:

| Method | Equivalent function |
| --- | --- |
| `PronomialCoreferenceSolver.replace_corefs(text, lang="en")` | `replace_corefs` |
| `PronomialCoreferenceSolver.solve_corefs(text, lang="en", return_idx=True)` | `link_pronouns` |
| `PronomialCoreferenceSolver.score_corefs(text, lang="en")` | `score_corefs` |
| `PronomialCoreferenceSolver.detect_nouns(text, lang="en", return_idx=True)` | `detect_nouns` |
| `PronomialCoreferenceSolver.normalize(text)` | `normalize` |

```python
from pronomial import PronomialCoreferenceSolver

PronomialCoreferenceSolver.replace_corefs("Anna lost her keys.", lang="en")
# 'Anna lost Anna keys .'
```

## Helpers

These come from `pronomial.utils` and are also re-exported from the package root.

### `word_tokenize(text) -> list[str]`

Re-exported from `quebra_frases`. Splits text into the token list every index in
`link_pronouns`/`score_corefs` refers to.

```python
from pronomial import word_tokenize

word_tokenize("It was founded by the Romans.")
# ['It', 'was', 'founded', 'by', 'the', 'Romans', '.']
```

### `pos_tag(text, lang="en") -> list[tuple[str, str]]`

POS-tag a string into `(token, tag)` pairs. English uses the NLTK
averaged-perceptron tagger (Penn Treebank tags); `pt`/`es` load a bundled
pickle. The per-language tag sets the solver checks against (`NOUN`, `PRON`,
`ADJ`, ...) are defined in `pronomial/lang/*.py`.

```python
from pronomial import pos_tag

pos_tag("The Romans named it.", lang="en")
# [('The', 'DT'), ('Romans', 'NNPS'), ('named', 'VBD'), ('it', 'PRP'), ('.', '.')]
```

### `predict_gender(word, text="", lang="en") -> str`

Guess `"male"` or `"female"` for a word. It first checks the language's gendered
word lists (and, for `pt`/`es`/`ca`, morphological rules using surrounding
`text`), then falls back to a NaiveBayes classifier trained on name suffixes.

```python
from pronomial import predict_gender

predict_gender("Sarah")   # 'female'
predict_gender("John")    # 'male'
```

### `is_plural(text, lang="en") -> bool`

Whether a token is plural. English uses morphological rules; other languages use
a trailing-`s` check.

```python
from pronomial import is_plural

is_plural("Romans", lang="en")   # True
is_plural("Rome", lang="en")     # False
```

## Where next

- [quickstart.md](quickstart.md) — install and first calls
- [advanced.md](advanced.md) — how scoring works, multi-language notes, gotchas
- [opm.md](opm.md) — the OVOS `opm.agents.coref` plugin
