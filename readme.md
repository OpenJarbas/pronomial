# Pronomial

Pronomial is a fast, rule-based coreference solver. It links each pronoun in a
text to the noun it most likely refers to, using part-of-speech tags, a word
gender classifier, and lists of pronouns. It supports English, Portuguese,
Spanish, and Catalan.

## Install

```bash
pip install pronomial
```

## Usage

```python
from pronomial import replace_corefs

replace_corefs("London has been a major settlement for two millennia. "
               "It was founded by the Romans, who named it Londinium.", 
               lang="en")
"""
"London has been a major settlement for two millennia . "
"London was founded by the Romans , Romans named London Londinium ."
"""
```

See [docs/quickstart.md](docs/quickstart.md) for more examples, and
[docs/api.md](docs/api.md) for the full function and class reference.

## About

Pronomial works well on short sentences. It is safe to use for simple text,
but it can fail on complex sentences with several competing antecedents.

For a full coreference resolution library, see
[neuralcoref](https://github.com/huggingface/neuralcoref) or
[coreferee](https://github.com/msg-systems/coreferee).

Pronomial is a baseline. It shows how well simple heuristics can solve
coreference resolution. Do not rely on it for production use.

## Related projects

- [TigreGotico/quebra_frases](https://github.com/TigreGotico/quebra_frases): the tokenizer Pronomial uses to split text into words.

## License

Apache License 2.0. See [LICENSE](LICENSE).
