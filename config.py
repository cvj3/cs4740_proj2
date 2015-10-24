# if True uses context from immediate sentence, else uses ALL words
TEST_BY_SENTENCE = False


# if True, will filter tokens by part_of_speech (see common.py for details)
# WARNING: turning this on will greatly reduce performance (i.e., speed) of processing
POS_FILTER = True


# if True uses 100% data, else 75% training and then tests on 25%
WRITE_TEST = False
# if True, only failed results are included in test debug output
FAIL_DEBUG_ONLY = True

# value must be greater than zero, or will be ignored
WRITE_LIMIT = 8000


# csv file name, if WRITE_TEST = True
RESULTS_FILE = "kaggle-test"


# String descriptor to remember what change was made
# very useful for debug output at the end of a slow processing run
BUILD = "EXPERIMENT #n+1: misc. test"
