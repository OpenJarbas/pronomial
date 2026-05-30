# OVOS plugin (opm.agents.coref)

`pronomial` ships an OVOS Plugin Manager entry point so any component that
discovers `opm.agents.coref` plugins gets offline, rule-based coreference for
free. The plugin class is `pronomial.opm.PronomialCoreferenceEngine`.

The entry point is declared in `setup.py`:

```python
entry_points={
    "opm.agents.coref": [
        "pronomial = pronomial.opm:PronomialCoreferenceEngine",
    ],
}
```

When `ovos-plugin-manager` is installed, the engine subclasses its
`CoreferenceEngine` template; without it, the module still imports against a
minimal fallback base so you can use the class directly.

## Direct use

```python
from pronomial.opm import PronomialCoreferenceEngine

engine = PronomialCoreferenceEngine({"lang": "en"})

engine.contains_corefs("It was founded by them", "en")
# True

engine.solve_corefs("London is old. It was founded by Romans.", "en")
# 'London is old . London was founded by Romans .'
```

## Methods

### `__init__(config=None)`

`config` is an optional dict. The only key read is `lang` (BCP-47, default
`"en"`); it warms the pronoun cache for that language at construction time.

### `contains_corefs(text, lang) -> bool`

Fast word-list check: `True` when any known pronoun for `lang` appears in
`text`. Returns `False` for an unsupported language. Use it as a cheap gate
before the heavier `solve_corefs`.

```python
engine.contains_corefs("the cat sat down", "en")   # False
engine.contains_corefs("she sat down", "en")        # True
```

### `solve_corefs(text, lang) -> str`

Resolve coreferences via `pronomial.replace_corefs` and return the rewritten
text. Only the segment of `lang` before `-` is used. If resolution fails or the
language is unsupported, the original `text` is returned unchanged.

## Supported languages

`en`, `pt`, `es`, `ca` for the pronoun word-list gate (`contains_corefs`). Full
rewriting (`solve_corefs`) follows the core library, so it covers `en`, `pt`,
and `es`; `ca` falls back to returning the input unchanged because Catalan POS
tagging is not wired up.

## Where next

- [quickstart.md](quickstart.md) — install and first calls
- [api.md](api.md) — the underlying library surface
- [advanced.md](advanced.md) — scoring internals, multi-language notes, gotchas
