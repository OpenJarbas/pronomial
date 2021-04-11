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

# work with tokens instead
for tok_idx, tok, word in link_pronouns(sentence, lang="en"):
    assert tokens[tok_idx] == tok
    tokens[tok_idx] = word

assert tokens == word_tokenize(result)

# work with the raw prediction
sentence = "Bob loves his dog"
tokens = word_tokenize(sentence)
raw = score_corefs(sentence, lang="en")
# tok_idx, score, word_idx
# [(2, 10, 0)]
# tokens[2] == "his" == "Bob"

sentence = "Joe was talking to Bob and told him to go home because he was drunk"


tokens = word_tokenize(sentence)
pred = score_corefs(sentence, lang="en")
# {7: {0: 0.45454545454545453, 4: 0.5454545454545454},
# 12: {0: 0.4166666666666667, 4: 0.5, 10: 0.08333333333333333}}

for tok_idx, match in pred.items():
    tok = tokens[tok_idx]
    for tok2_idx, score in match.items():
        tok2 = tokens[tok2_idx]
        print(tok, tok2, score)
    # him Joe 0.45454545454545453
    # him Bob 0.5454545454545454
    # he Joe 0.4166666666666667
    # he Bob 0.5
    # he home 0.08333333333333333
