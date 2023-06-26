import spacy


def tokenize(text):
    nlp = spacy.load("en_core_web_lg")
    doc = nlp(text)
    whitelist = ["NOUN", "PROPN", "VERB"]

    doc_white = list(filter(lambda token: token.pos_ in whitelist, doc))

    string_white = " ".join(map(lambda token: token.text, doc_white))
    return string_white
    # doc_num = list(filter(lambda token: token.pos_ == "NUM", doc))
    # for token in doc_white:
    #     print(str(token) + " " + token.pos_)

    # for ent in doc.ents:
    #     print(ent.text, ent.label_)
