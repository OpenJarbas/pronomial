# Pronomial

simple and fast coreference solver, uses pos tags, a word gender classifier 
and lists of pronouns

Supported languages: English, Portuguese, Spanish, Catalan

# Install

```bash
pip install pronomial
```

# Usage

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

## About

Pronomial will work fine for short sentences and should be safe to use in 
the context of simple things like intent parsing, but it tends to fail 
horribly in long sentences.

It you want a proper coreference resolution library I suggest you check out
[neuralcoref](https://github.com/huggingface/neuralcoref)

Pronomial should not be used in production most of the
time, it is intended as baseline and an experiment on how well this
task can be solved using only heuristics. 


Keep an eye on this section for future benchmarks
