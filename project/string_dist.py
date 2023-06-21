import Levenshtein
import string
from enum import Enum


class Methods(Enum):
    levinshtein = 1
    jaro = 2
    jaro_winkler = 3
    hamming = 4
    indel = 5


def levinshtein(
    string1: str,
    string2: str,
    dist_threshold=0.8,
    found_count_threshold=0.7,
    method: Methods = Methods.jaro_winkler,
):
    words1 = string1.translate(str.maketrans("", "", string.punctuation)).split(" ")
    words2 = string2.translate(str.maketrans("", "", string.punctuation)).split(" ")

    short = words1
    long = words2
    if len(words1) > len(words2):
        short = words2
        long = words1

    found_count = 0
    for word in short:
        if (
            len(
                list(
                    filter(
                        lambda x: compare_string(x, word, method, dist_threshold) > 0,
                        long,
                    )
                )
            )
            > 0
        ):
            found_count += 1

    return found_count / len(short) > found_count_threshold


def compare_string(string1, string2, method: Methods, threshold):
    if method == Methods.levinshtein:
        dist = Levenshtein.distance(string1, string2)
    elif method == Methods.hamming:
        dist = Levenshtein.hamming(string1, string2)
    elif method == Methods.jaro:
        dist = Levenshtein.jaro(string1, string2, score_cutoff=threshold)
    elif method == Methods.jaro_winkler:
        dist = Levenshtein.jaro_winkler(string1, string2, score_cutoff=threshold)
    elif method == Methods.indel:
        dist = Levenshtein.ratio(string1, string2, score_cutoff=threshold)

    if method == Methods.levinshtein or method == Methods.hamming:
        dist = 1 - (dist / max(len(string1), len(string2)))
        if dist < threshold:
            return 0
        else:
            return dist
    else:
        return dist


def setratio(string1, string2, threshold=0.8):
    return (
        Levenshtein.setratio(
            string1.translate(str.maketrans("", "", string.punctuation)).split(" "),
            string2.translate(str.maketrans("", "", string.punctuation)).split(" "),
        )
        > threshold
    )


# print(
#     levinshtein(
#         "Hello my name is Sebastian and I like a Motho",
#         "Hello I want a Mojito.",
#         method=Methods.jaro_winkler,
#     )
# )

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
