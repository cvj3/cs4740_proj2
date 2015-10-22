import datetime
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
# from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords


__author__ = "Alin Barsan, Curtis Josey"

s = SnowballStemmer("english")
stopwords = stopwords.words("english")
lm = WordNetLemmatizer()
# a simple debug timer (see start() and end(messge))
TIMER = None


# cache system time prior to running code block
def start():
    global TIMER
    TIMER = datetime.datetime.now()


# output current time - start time with debug msg
def end(message):
    global TIMER
    end = datetime.datetime.now()
    print "\n" + message + " in %s seconds.\n" % str((end-TIMER).seconds)
    TIMER = None


# automated pre-processing of tokens
def filter_tokens(tokens):
    filtered_tokens = []

    tokens_with_pos = nltk.pos_tag(tokens)
    for pair in tokens_with_pos:
        token = pair[0]
        pos = pair[1]

    for token in tokens:
        token = token.lower().strip()
        token = lm.lemmatize(token)

        # if all punct
        if not any(char.isalnum() for char in token):
            continue
        # keep nouns & adjects, discards prepositions + conjunctions (IN)
        # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
        elif not (("N" in pos and "I" not in pos) or ("J" in pos)):
            continue
        # if token is a stopword
        if token in stopwords:
            continue
        # if token has useless word fragment
        if token == "n't":
            continue
        # if token is very short
        if len(token) <= 3:
            continue
        # if all numerals
        if token.isdigit():
            continue
        # if token has target tag still remaining
        if "/tar" in token:
            continue
        else:
            # filtered_tokens.append(token)
            filtered_tokens.append(s.stem(token))
    return filtered_tokens


def write_results_to_csv(results, filename):
    f = open(filename + ".csv", "w")
    f.write("Id,Prediction\n")
    output = "\n".join(results)
    f.write(output)
    f.close()


# test filtering tokens
if __name__ == "__main__":
    import sys
    args = sys.argv
    filtered = filter_tokens(nltk.word_tokenize(args[1]))
    print filtered
    print "\nLength: %d" % len(filtered)
