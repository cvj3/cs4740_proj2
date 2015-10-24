import datetime
import string
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
# from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from config import *


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


# shared token clensing code
def clense_token(token, debugMode = False):
    # convert to lower case, and remove extra spaces
    token_pre = token.lower().strip()
    # get lemma, the base form of word
    token_post = lm.lemmatize(token_pre)

    if debugMode:
        if token_pre != token_post:
            print "%s -> %s" % (token_pre, token_post)

    return token_post


# automated pre-processing of tokens
def filter_tokens(tokens):
    filtered_tokens = []

    if POS_FILTER:
        # get part of speech for tokens
        tokens_with_pos = nltk.pos_tag(tokens)
        for pair in tokens_with_pos:
            token = pair[0]
            pos = pair[1]

            # skip if token is only punctuation
            if token in string.punctuation:
                # print "discarding token2: %s (%s) " % (token, pos)
                continue

            # exclude some parts of speech (cardinal numbers, unknowns, etc)
            # Penn Treebank Tag list:
            # https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
            if (pos == "CD") or (pos == ".") or (pos == "AT") or (pos == "IN"):
                # print "Discarding due to pos tag (%s): %s" % (pos, token)
                continue

            # convert to lower case and strip excess spaces
            token = token.lower().strip()

            # if token is a stopword
            if token in stopwords:
                continue

            # if all punct
            if not any(char.isalnum() for char in token):
                print "discarding token: %s (%s) " % (token, pos)
                continue

            # unused code, attempts to uses part of speech lemmatization
            # # default / initialize wordnet part of speech tag variable
            # w_pos = ''
            # # convert treebank tags to wordnet pos
            # # http://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
            # if pos.startswith('J'):
            #     w_pos = nltk.corpus.wordnet.ADJ
            # elif pos.startswith('V'):
            #     w_pos = nltk.wordnet.wordnet.VERB
            # elif pos.startswith('N'):
            #     w_pos = nltk.wordnet.wordnet.NOUN
            # elif pos.startswith('R'):
            #     w_pos = nltk.wordnet.wordnet.ADV
            # # lemmatize; ~base word
            # if w_pos != '':
            #     token = lm.lemmatize(token, w_pos)
            # else:
            #     token = lm.lemmatize(token)

            token = lm.lemmatize(token)

#                if token != s.stem(token):
#                    print "Stemming diff (%s): %s" % (s.stem(token), token)

            # TODO: consider special tagging and comparing (number to number?)

            # if token has target tag still remaining
            if "/tar" in token:
                continue
            else:
                # filtered_tokens.append(token)
                filtered_tokens.append(s.stem(token))

    else:
        for token in tokens:
            # strip spaces, lemmatize, etc
            token = clense_token(token)

            # if all punct
            if not any(char.isalnum() for char in token):
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


# export to CSV format (per Kaggle specifications)
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
