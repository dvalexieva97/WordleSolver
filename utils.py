
from collections import Counter


def get_syllables(word, siz):
    syllables = []

    for i, l in enumerate(word):
        syllables.append(word[i:i + siz])

    return [s for s in syllables if len(s) == siz]


def fetch_common_syllables(corpus, size=2, cnt_comm=20):
    sricki_list = [get_syllables(wrd, size) for wrd in corpus]
    flat_ = [x for y in sricki_list for x in y]

    counter_obj = Counter(flat_)
    common = counter_obj.most_common(cnt_comm)

    return common
