from pronomial import replace_corefs, link_pronouns, normalize, \
    word_tokenize, score_corefs

sentence = "London has been a major settlement for two millennia. It was founded by the Romans, who named it Londinium."

# normalize text + tokenize
# (automatically done but you might need it for comparisons)
normalized = "London has been a major settlement for two millennia . It was founded by the Romans , who named it Londinium ."
assert normalize(sentence) == normalized

tokens = ['London', 'has', 'been', 'a', 'major', 'settlement', 'for', 'two', 'millennia', '.', 'It', 'was', 'founded', 'by', 'the', 'Romans', ',', 'who', 'named', 'it', 'Londinium', '.']
assert word_tokenize(sentence) == tokens
assert word_tokenize(normalized) == tokens

# replace pronouns
solved = "London has been a major settlement for two millennia . London was founded by the Romans , Romans named London Londinium ."
result = replace_corefs(sentence, lang="en")
assert result == solved


# work with the raw prediction
tokens = word_tokenize(sentence)
pred = score_corefs(sentence, lang="en")
# {10: {0: 0.56, 5: 0.06, 8: 0.39},
# 17: {5: 0.02, 8: 0.28, 15: 0.7},
# 19: {0: 0.56, 5: 0.06, 8: 0.39}}

for tok_idx, match in pred.items():
    tok = tokens[tok_idx]
    for tok2_idx, score in match.items():
        tok2 = tokens[tok2_idx]
        print(tok, tok2, score)
    # It London 0.56
    # It settlement 0.06
    # It millennia 0.39
    # who settlement 0.02
    # who millennia 0.28
    # who Romans 0.7
    # it London 0.56
    # it settlement 0.06
    # it millennia 0.39


