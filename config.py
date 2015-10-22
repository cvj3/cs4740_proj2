# if True uses context from immediate sentence, else uses ALL words
TEST_BY_SENTENCE = False

# if True uses 100% data, else 75% training and then tests on 25%
WRITE_TEST = False

# csv file name, if WRITE_TEST = True
RESULTS_FILE = "no-scaling"

# String descriptor to remember what change was made
# very useful for debug output at the end of a slow processing run
BUILD = "no bayes-ian scaling"
