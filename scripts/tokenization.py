"""
Set of methods to tokenize text and get list
of emojies attached to a word.
"""

from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
from pke.unsupervised import YAKE
from nltk.corpus import stopwords

import os


"""
Tokenizing text.
"""


def get_kphrases(text, n=100):
    """Return key phrases for input text
    """

    tokenizer = RegexpTokenizer(r'\w+')
    text_split = tokenizer.tokenize(text)
    extractor = YAKE()
    try:
        # load the content of the document, here document is expected to be in raw
        # format (i.e. a simple text file) and preprocessing is carried out using spacy
        extractor.load_document(text, language='en')

        # keyphrase candidate selection, in the case of TopicRank: sequences of nouns
        # and adjectives (i.e. `(Noun|Adj)*`)
        extractor.candidate_selection(n=1)

        # candidate weighting, in the case of TopicRank: using a random walk algorithm
        extractor.candidate_weighting()

        # N-best selection, keyphrases contains the 10 highest scored candidates as
        # (keyphrase, score) tuples
        keyphrases = extractor.get_n_best(n=n)

        phrases = []
        for phrase, _ in keyphrases:
            phrases.append(phrase)

        order_phrases = []
        for phrase in text_split:
            if phrase in phrases:
                order_phrases.append(phrase)
        return order_phrases

    except Exception:
        return []


"""
Norming words and getting list of emojies.
"""


def norm(text):
    """Normilizing word.
    """

    try:
        tokenizer = RegexpTokenizer(r'\w+')
        text = tokenizer.tokenize(text)
        lemmatizer = PorterStemmer()

        word_list = [lemmatizer.stem(textik).lower() for textik in text]

        filtered_words = [word for word in word_list if word not in stopwords.words('english')]
        return filtered_words

    except Exception:
        return []


def get_filename(file):
    """Getting list of tags from emoji name.
    """

    try:
        base = os.path.basename(format(file))
        return norm(' '.join(os.path.splitext(base)[0].split('_')))

    except Exception:
        return []


def get_emoji(word, file_path="../support_files/emoji/"):
    """Getting list of paths to emojies containing given word.
    """

    try:
        lis = []
        onlyfiles = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f))]
        for file in onlyfiles:
            if norm(word)[0] in get_filename(file):
                lis.append(file_path+file)
        return lis
    except Exception:
        return []
