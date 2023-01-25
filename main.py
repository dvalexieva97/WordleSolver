
from datetime import datetime
import logging
from WordCorpus import WordCorpus
from Wordle import WordleSolver

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":

    word_length = 5
    test_word = "party"
    word_set_size = 100
    corp = WordCorpus(word_len=word_length)

    solver = WordleSolver(corp, max_attempts=6)

    # Solve single word:
    is_success, count_attempts, used_words = solver.anti_wordle(test_word)

    # Get stats on solution of random test sample
    random_words = solver.generate_random_word_set(set_size=word_set_size)
    results = solver.test_wordle_solver(random_words)
    time_now = str(datetime.now())[:16].replace(" ", "_").replace(":", "_")
    results.to_csv(f"./data/Results_{time_now}.csv", index=False)