from unidecode import unidecode
import logging
import nltk
nltk.download('reuters')
nltk.download('brown')
nltk.download('conll2000')
nltk.download('nps_chat')
nltk.download('gutenberg')
nltk.download('reuters')
nltk.download('shakespeare')
nltk.download('stopwords')
nltk.download('genesis')
nltk.download('framenet')
nltk.download('framenet_v15')
nltk.download('framenet_v17')
nltk.download('cmudict')
nltk.download('words')
from nltk.corpus import words as nltkwords
from nltk.corpus import gutenberg, reuters, brown, shakespeare, stopwords, genesis, \
    framenet, framenet15, nps_chat, cmudict, conll2000
from utils import fetch_common_syllables

logging.basicConfig(level = logging.DEBUG)

class WordCorpus:
    def __init__(self, word_len=5):
        self.word_len = word_len
        self.corpus = []
        self.ones = None
        self.twos = None
        self.threes = None
        self.fours = None
        self.common_words = None
        self.best_words = None
        self.create_corpus()
        self.generate_corpus_properties()

    def clean_corpus(self):
        exclude_characters = [",", "_", "-", "'", ";"]
        self.corpus = [x for x in self.corpus if unidecode(x) == x]
        self.corpus = [x for x in self.corpus if not any(bs in x for bs in exclude_characters)]
        logging.info(f"Corpus size before dropping duplicates: {len(self.corpus)}")
        self.corpus = list(set(self.corpus))
        self.corpus = [x.upper() for x in self.corpus]


    def create_corpus(self):
        # documentation here: https://www.nltk.org/book/ch02.html

        self.corpus = []
        dicts_categories = [reuters, brown]
        dict_files = [conll2000, nps_chat, framenet, framenet15, genesis, shakespeare, gutenberg]
        for d in dicts_categories:
            words = [w for w in d.words(categories=d.categories())]
            self.corpus += words
            self.corpus += d.categories()

        for d in dict_files:
            files = d.fileids()
            for f in files:
                logging.info(f"Fetching words from {f}")
                for w in d.words(f):
                    self.corpus.append(w)

        nltk_words = set(nltkwords.words())
        self.corpus += nltk_words
        self.corpus += cmudict.words()
        self.corpus += stopwords.words('english')

        self.corpus = [w for w in self.corpus if len(w) == self.word_len]

        self.clean_corpus()
        logging.info(f"Successfully created word coprus. Size:{len(self.corpus)}")

    def generate_corpus_properties(self):
        self.common_words = fetch_common_syllables(self.corpus, size=5, cnt_comm=1000)
        self.fours = fetch_common_syllables(self.corpus, size=4)  # most common 4s
        self.threes = fetch_common_syllables(self.corpus, size=3)
        self.twos = fetch_common_syllables(self.corpus, size=2)
        self.ones = fetch_common_syllables(self.corpus, size=1)
        self.best_words = [w for (w, c) in self.common_words if len(list(set(list(w)))) == len(list(w))]



