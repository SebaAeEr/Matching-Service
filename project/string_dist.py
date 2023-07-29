import Levenshtein
import string
from enum import Enum
import jellyfish
import schemas


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
    rule: str,
    msg: str,
    phone_dist: False,
    dist_threshold=0.8,
    found_count_threshold=0.7,
    lex_method: Lex_Methods = Lex_Methods.jaro_winkler,
    phone_method: Phone_Methods = Phone_Methods.nysiis,
):
    """ "
    Match all words of rule with all words of message lexicraphicly or phoneticly.
    Calculate percentage of words in rule who found a matching partner.

    rule: rules for matching
    msg: messages for matching
    phone_dist: True: use phone_dist; False: use lex_dist
    dist_threshold: threshold for distance between each word
    found_count_threshold: threshold for percentage of matches in rule
    lex_method: method used by lexicographical matching
    phone_method: method used by phonetic matching

    returns boolean if rule was matched with message
    """

    # split strings into their words and remove all puntuation
    rule = rule.translate(str.maketrans("", "", string.punctuation)).split(" ")
    msg = msg.translate(str.maketrans("", "", string.punctuation)).split(" ")

    found_count = 0
    for word in rule:
        if phone_dist:
            for m in msg:
                if compare_phone_string(m, word, phone_method, dist_threshold):
                    found_count += 1
                    break
        else:
            for m in msg:
                if compare_lex_string(m, word, lex_method, dist_threshold):
                    found_count += 1
                    break

    return found_count / len(rule) > found_count_threshold


def compare_lex_string(string1, string2, method: Lex_Methods, threshold):
    """
    Run lexicographic matching on the two words.
    Returns boolean if distance is above threshold
    """

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
        # levinshtein and hamming count changes you have to make to the words in order to make them equal.
        # dist is the quota of changes in relation to the letters in the longest word
        dist = 1 - (dist / max(len(string1), len(string2)))
        if dist < threshold:
            return False
        else:
            return True
    else:
        return dist > 0


def compare_phone_string(string1, string2, method: Phone_Methods, threshold):
    """
    Run phonetical matching on the two words.
    Returns boolean if distance is above threshold
    """

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
                threshold,
            )
            > 0
        )
    elif method == Phone_Methods.nysiis:
        return (
            compare_lex_string(
                jellyfish.nysiis(string1),
                jellyfish.nysiis(string2),
                Lex_Methods.levinshtein,
                threshold,
            )
            > 0
        )
    elif method == Phone_Methods.soundex:
        return (
            compare_lex_string(
                jellyfish.soundex(string1),
                jellyfish.soundex(string2),
                Lex_Methods.levinshtein,
                threshold,
            )
            > 0
        )
