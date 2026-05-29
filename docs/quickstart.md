# Quickstart

`pronomial` is a fast, heuristic coreference solver: it points each pronoun at
the noun it most likely refers to, then can rewrite the sentence with the
pronoun replaced by that noun. It works on POS tags plus curated pronoun and
gendered-word lists — no neural model, no network, no GPU. English, Portuguese,
Spanish, and Catalan are supported.

## 1. Install

```bash
pip install -e .
```

Runtime dependencies are `nltk` and `quebra_frases`. On the first English POS
call, NLTK downloads `averaged_perceptron_tagger`. The Portuguese, Spanish, and
Catalan taggers plus the name/gender classifier ship as pickles inside the
package, so those languages work offline from the first call.

## 2. The one idea

A coreference is a pronoun ("It", "who", "Ela") that stands in for an earlier
noun ("London", "the Romans", "Maria"). `pronomial` scores every candidate
antecedent for each pronoun, picks the best, and hands you back either the
links or a rewritten string.

```python
from pronomial import replace_corefs

text = ("London has been a major settlement for two millennia. "
        "It was founded by the Romans, who named it Londinium.")

print(replace_corefs(text, lang="en"))
# London has been a major settlement for two millennia . London was founded
# by the Romans , Romans named London Londinium .
```

`replace_corefs` is the highest-level call: text in, resolved text out. Note the
output is tokenized (spaces around punctuation) because the rewrite happens on
tokens.

## 3. See the links instead of the rewrite

When you want the antecedent decisions rather than a rewritten string, use
`link_pronouns`. By default it returns token-*index* triples
`(pronoun_idx, antecedent_idx, score)`; pass `return_idx=False` for the words.

```python
from pronomial import link_pronouns

text = ("London has been a major settlement for two millennia. "
        "It was founded by the Romans, who named it Londinium.")

print(link_pronouns(text, lang="en", return_idx=False))
# [('It', 'London', 0.56), ('who', 'Romans', 0.7), ('it', 'London', 0.56)]
```

Each score is that candidate's share of the total score mass for the pronoun, so
the values for one pronoun sum to roughly `1.0`.

## 4. Another language

Pass any BCP-47 code; only the language part (before `-`) is used.

```python
from pronomial import replace_corefs, link_pronouns

pt = "A Maria comprou um carro. Ela gosta dele."
print(replace_corefs(pt, lang="pt"))
# A Maria comprou um carro . Maria gosta dele .

print(link_pronouns(pt, lang="pt", return_idx=False))
# [('Ela', 'Maria', 0.8), ('dele', 'dele', 0.67)]
```

## Where next

- [api.md](api.md) — every public function and class, real signatures, return shapes
- [advanced.md](advanced.md) — scoring internals, multi-language notes, gotchas, recipes
- [opm.md](opm.md) — using `pronomial` as an OVOS `opm.agents.coref` plugin
