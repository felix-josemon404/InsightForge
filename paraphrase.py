import random
import nltk
from nltk.corpus import wordnet
from nltk.tokenize import sent_tokenize, word_tokenize

nltk.download('punkt')
nltk.download('wordnet')

def get_synonym(word):
    synsets = wordnet.synsets(word)
    synonyms = set()

    for syn in synsets:
        for lemma in syn.lemmas():
            name = lemma.name().replace("_", " ")
            if name.lower() != word.lower():
                synonyms.add(name)

    if synonyms:
        return random.choice(list(synonyms))
    return word


def paraphrase_sentence(sentence, replacement_prob=0.2):
    words = word_tokenize(sentence)
    new_words = []

    for word in words:
        if random.random() < replacement_prob and word.isalpha():
            new_words.append(get_synonym(word))
        else:
            new_words.append(word)

    return " ".join(new_words)


def paraphrase_text(text):
    sentences = sent_tokenize(text)
    new_sentences = []

    for s in sentences:
        new_sentences.append(paraphrase_sentence(s))

    return " ".join(new_sentences)


# Example
text = """

The increasing trend of data-driven decision making has led to a growing amount of
research in the areas of business intelligence systems, natural language interfaces for
databases, and automated analytics tools. Traditional business intelligence systems pro-
vide organizations with the capability to analyze large datasets and extract meaningful
insights. However, the use of such systems often requires knowledge of structured query
languages such as SQL.

To address this limitation, researchers have developed systems that allow users to in-
teract with databases using natural language. These systems are commonly referred to
as Natural Language Interfaces for Databases (NLIDB). With the advancement of ma-
chine learning algorithms and large language models, it has become possible to develop
tools that translate natural language queries into structured database queries with higher
accuracy

"""

result = paraphrase_text(text)

print("Original:\n", text)
print("\nParaphrased:\n", result)