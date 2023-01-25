# Solver of Wordle

import random
import pandas as pd
import logging
from utils import fetch_common_syllables
logging.basicConfig(level=logging.DEBUG)

pd.set_option("display.max_columns", None)

class WordleSolver:
    def __init__(self, corpus, max_attempts=6):
        self.word_corpus = corpus
        self.max_attempts = max_attempts


    def anti_wordle(self, target_word):
        """
        :param target_word: word we want to guess
        :param corpus: list of words we use as our corpus
        :param max_attempts: count of max attempts
        :return: 1/0 - sucess; attempt when we matched the word
        """

        target_word = target_word.upper()
        logging.info(f"Wordle solver for word: {target_word}")
        def fetch_green_brown_bull(testword, myword):
            """
            :param testword: the word we are trying with
            :param myword: the word we want to match
            :return: green - pure letter/place match; brown - letter-1;place-0; bullshit - letter - 0; place-0
            """

            myword_map = [(i, l) for i, l in enumerate(myword)]
            first_map = [(i, l) for i, l in enumerate(testword)]
            green = [i for i in first_map for y in myword_map if i == y]
            green_letters = [g[1] for g in green]
            brown = [i for i in first_map if i[1] in list(myword) and i not in green]
            brown_letters = [x[1] for x in brown]
            bullshit_letters = [l for l in testword if l not in green_letters and l not in brown_letters]

            return green, brown, bullshit_letters

        def get_first(best_words, myword, bullshit_letters_=[]):
            first_ = ''
            if not bullshit_letters_:
                first_ = random.choice(best_words)
            else:
                while not any(bs in first_ for bs in bullshit_letters_):
                    first_ = random.choice(best_words)

            green, brown, bullshit_letters = fetch_green_brown_bull(testword=first_, myword=myword)

            return first_, green, brown, bullshit_letters

        def iter_test(corpus, green, brown,
                      fours, thres, twos, ones,
                      bullshit_letters_=[]):

            brown_letters = [b[1] for b in brown]

            possib_gr = [w for w in corpus if all(syll in w for syll in green)]
            possib_br = [w for w in corpus if not any(syll in w for syll in brown)
                         and any(br in syll for br in brown_letters for syll in w)]  # todo brown in w or w in brown

            if possib_br:
                possibilities = [c for c in possib_br if c in possib_gr]
            else:
                possibilities = possib_gr
            possibs_joined = ["".join([x[1] for x in w]) for w in possibilities]

            if target_word not in possibs_joined:
                raise Exception("lost target word")


            # if not best_possi:
            for i, var_ in enumerate([fours, thres, twos, ones]):
                best_possi = [w for w in possibs_joined if
                              any(f[0] in w for f in var_) and not any(bs in w for bs in bullshit_letters_)]
                if len(best_possi) > 0:
                    break

            next_choice = random.choice(best_possi)

            return next_choice

        corpus = self.word_corpus.corpus.copy()
        attempt_cnt = 0
        used_ls = []
        bullshit_letters = []
        green = []
        brown = []
        # step 1: Get first word that matches something while excluding bullshit letters
        while not green and not brown and attempt_cnt < self.max_attempts:
            used, green, brown, bullshit_letters = get_first(self.word_corpus.best_words, target_word, bullshit_letters_=bullshit_letters)
            attempt_cnt += 1
            logging.info(f"{attempt_cnt} :: {used}")
            used_ls.append(used)
            if used == target_word:
                logging.info(f"Congrats! You won. Attemp #{attempt_cnt}")
                return 1, attempt_cnt, used_ls
            if attempt_cnt == self.max_attempts:
                logging.info(f"Sorry! You didn't guess the word! All 6 of your first attempts were wrong")
                return 0, attempt_cnt, used_ls

        # step 2: all other attempt matches until we get correct word (WIN) or not
        corpus = list(set((w for w in corpus if w not in used_ls)))
        corpus = [[x for x in enumerate(list(w))] for w in corpus]
        test_word = ''
        while attempt_cnt < self.max_attempts and test_word != target_word:
            attempt_cnt += 1
            test_word = iter_test(corpus, green, brown,
                                  self.word_corpus.fours, self.word_corpus.threes, self.word_corpus.twos,
                                  self.word_corpus.ones,
                                  bullshit_letters)
            logging.info(f"{attempt_cnt} :: {test_word}")
            green0, brown0, bullshit0 = fetch_green_brown_bull(test_word, target_word)
            used_ls.append(test_word)
            used_ls_splt = [[x for x in enumerate(list(w))] for w in used_ls]
            corpus = [c for c in corpus if used_ls_splt not in c]

            green += green0
            brown += brown0
            bullshit_letters += bullshit0

        if test_word == target_word:
            logging.info(f"Success! We guessed the word: {target_word}")
            return 1, attempt_cnt, used_ls
        else:
            logging.info(f"Sorry! We didn't guess the word. It was: {target_word}")
            return 0, attempt_cnt, used_ls

    def generate_random_word_set(self, set_size=100):
        # below is testing
        mywords = []
        # todo de-harcode thresholds:
        popular_words = fetch_common_syllables(self.word_corpus.corpus, size=5, cnt_comm=1000)
        popular_words = [x[0] for x in popular_words]

        for i in range(0, set_size):
            mywords.append(random.choice(popular_words) )
        return mywords


    def test_wordle_solver(self, mywords):
        results = []

        mywords = [w.upper() for w in mywords]
        cnt_experiments = 1
        for word in mywords:
            if word not in self.word_corpus.corpus:
                logging.warning(f"{word} not in corpus. Proceeding to next.")
                continue
            res = self.anti_wordle(word)
            for id in range(0, cnt_experiments):
                results.append(res + tuple([word]))

        res_df = pd.DataFrame(results, columns=[['success', 'number of attempts', 'words', 'target word']])
        #todo clean corpus from _ - etc '
        logging.info(f"Mean Wordle solver success: {res_df['success'].mean()}")
        return res_df

