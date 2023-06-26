import Levenshtein
import string
from enum import Enum
import jellyfish


class Lex_Methods(Enum):
    levinshtein = 1
    jaro = 2
    jaro_winkler = 3
    hamming = 4
    indel = 5


class Phone_Methods(Enum):
    mra = 1
    soundex = 2
    metaphone = 3
    nysiis = 4


def lex_dist(
    string1: str,
    string2: str,
    dist_threshold=0.8,
    found_count_threshold=0.7,
    lex_method: Lex_Methods = Lex_Methods.jaro_winkler,
    phone_method: Phone_Methods = Phone_Methods.nysiis,
):
    words1 = string1.translate(str.maketrans("", "", string.punctuation)).split(" ")
    words2 = string2.translate(str.maketrans("", "", string.punctuation)).split(" ")

    short = words1
    long = words2
    if len(words1) > len(words2):
        short = words2
        long = words1

    found_count = 0
    exact_matches = True
    for word in short:
        lex_found = sorted(
            list(
                map(
                    lambda x: compare_lex_string(x, word, lex_method, dist_threshold),
                    long,
                )
            ),
            reverse=True,
        )
        phone_found = sorted(
            list(
                map(
                    lambda x: compare_phone_string(x, word, phone_method),
                    long,
                )
            ),
            reverse=True,
        )
        if lex_found[0] > 0 or phone_found[0]:
            found_count += 1

        if lex_found[0] != 1:
            exact_matches = False

    return (exact_matches, found_count / len(short) > found_count_threshold)


def compare_lex_string(string1, string2, method: Lex_Methods, threshold):
    if method == Lex_Methods.levinshtein:
        dist = Levenshtein.distance(string1, string2)
    elif method == Lex_Methods.hamming:
        dist = Levenshtein.hamming(string1, string2)
    elif method == Lex_Methods.jaro:
        dist = Levenshtein.jaro(string1, string2, score_cutoff=threshold)
    elif method == Lex_Methods.jaro_winkler:
        dist = Levenshtein.jaro_winkler(string1, string2, score_cutoff=threshold)
    elif method == Lex_Methods.indel:
        dist = Levenshtein.ratio(string1, string2, score_cutoff=threshold)

    if method == Lex_Methods.levinshtein or method == Lex_Methods.hamming:
        dist = 1 - (dist / max(len(string1), len(string2)))
        if dist < threshold:
            return 0
        else:
            return dist
    else:
        return dist


def compare_phone_string(string1, string2, method: Phone_Methods):
    if method == Phone_Methods.mra:
        dist = jellyfish.match_rating_comparison(string1, string2)
        if dist == None:
            return False
        else:
            return dist
    elif method == Phone_Methods.metaphone:
        return (
            compare_lex_string(
                jellyfish.metaphone(string1),
                jellyfish.metaphone(string2),
                Lex_Methods.levinshtein,
                0.7,
            )
            > 0
        )
    elif method == Phone_Methods.nysiis:
        return (
            compare_lex_string(
                jellyfish.nysiis(string1),
                jellyfish.nysiis(string2),
                Lex_Methods.levinshtein,
                0.7,
            )
            > 0
        )
    elif method == Phone_Methods.soundex:
        return (
            compare_lex_string(
                jellyfish.soundex(string1),
                jellyfish.soundex(string2),
                Lex_Methods.levinshtein,
                0.7,
            )
            > 0
        )


def setratio(string1, string2, threshold=0.8):
    return (
        Levenshtein.setratio(
            string1.translate(str.maketrans("", "", string.punctuation)).split(" "),
            string2.translate(str.maketrans("", "", string.punctuation)).split(" "),
        )
        > threshold
    )


print(
    lex_dist(
        "order Mojito",
        "Hello, my name is Beth Schoon and I want to order a more Mochi.",
        lex_method=Lex_Methods.jaro_winkler,
    )
)


# print(
#     Levenshtein.setratio(
#         "Hello my name is Sebastian and I want to order a Mojito".translate(
#             str.maketrans("", "", string.punctuation)
#         ).split(" "),
#         "Hello I want a Mojito.".translate(
#             str.maketrans("", "", string.punctuation)
#         ).split(" "),
#     )
# )
