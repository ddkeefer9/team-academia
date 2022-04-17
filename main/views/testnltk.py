from nltk.corpus import wordnet
import nltk
syns = syns = wordnet.synsets("gerontology")
print(syns)
sent = "Demonstrate understanding of fundamental interdisciplinary evidence-based knowledge and theories for competent gerontological practice."
synonyms = []
for syn in wordnet.synsets("gerontology"):
		for l in syn.lemmas():
			synonyms.append(l.name())
print(synonyms)
