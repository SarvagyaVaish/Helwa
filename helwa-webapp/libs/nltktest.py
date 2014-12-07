import numpy
from nltk import tokenize
from nltk import tag

text = tokenize.word_tokenize("And now for something completely different")
tags = tag.pos_tag(text)

print text
print tags
