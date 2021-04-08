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