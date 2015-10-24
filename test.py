from config import WRITE_TEST, BUILD, RESULTS_FILE  # TEST_BY_SENTENCE,
from common import *
from predictDefinition import predict_definition, predict_definition_by_trained_context, predict_definition_by_trained_context_defs
# predict_random,
from context import get_context
# from random import randint
if not WRITE_TEST:
    from data.trainingData import wsddata as test_set
else:
    from data.testData import wsddata as test_set


__author__ = "Alin Barsan, Curtis Josey"


if __name__ == "__main__":
    summary = {}
    start()
    results = []
    counts = {}
    scores = []
    lowest_correct_score = 100
    threshold = 10
    pass_under_threshold = 0
    fail_under_threshold = 0
    wordsuccess = {}
    wordtotal = {}
    count = 0
    # tracks index to help split training data into 75% for training, and 25% for test.
    if not WRITE_TEST:
        splitter = 0

    # if WRITE_LIMIT is set, then abort process at new threshold
    if (WRITE_LIMIT > 0) and (WRITE_LIMIT < len(test_set)):  # and (WRITE_TEST)
        loop_limit = WRITE_LIMIT
        # print "WRITE_LIMIT SET: %d" % loop_limit
    else:
        loop_limit = len(test_set)

    for i in range(loop_limit):
        text = test_set[i]["context"]
        target = test_set[i]["word"]
        answers = test_set[i]["answer_ids"]
        instance = test_set[i]["id"]
        context, description = get_context(text, target)
        if not WRITE_TEST:
            splitter += 1
            # Every 4th training item is used for testing.
            if splitter < 4:
                continue
            else:
                splitter = 0
            summary["total"] = summary.get("total", 0) + 1
            wordtotal[target] = wordtotal.get(target, 0) + 1
            print "TEST " + str(i + 1) + ": " + target.upper()

        # if confidence level in prediction is too low, fallback to a different prediction strategy
        try:
            prediction, score = predict_definition_by_trained_context(context, target, description)
            source = 1
        except:
            try:
                # fall back to context def matching if no match between contexts
                prediction, score = predict_definition_by_trained_context_defs(context, target, description)
                counts["Context Def Fallbacks"] = counts.get("Context Def Fallbacks", 0) + 1
                source = 2
            except:
                # Fall back to Lesk approach if no match between context defs
                prediction, score = predict_definition(context, target)
                counts["Lesk Fallbacks"] = counts.get("Lesk Fallbacks", 0) + 1
                source = 3

        results.append(instance + "," + prediction)
        scores.append(score)
        if WRITE_TEST and not (i % 10):
            print "Parsed line: %d" % (i)
        if not WRITE_TEST:
            result = "FAIL"
            if prediction == "U":
                count += 1
            if prediction in answers:
                if source == 2:
                    counts["Context Def Fallback Successes"] = counts.get("Context Def Fallback Successes", 0) + 1
                if source == 3:
                    counts["Lesk Fallback Successes"] = counts.get("Lesk Fallback Successes", 0) + 1
                result = "PASS"
                summary[description] = summary.get(description, 0) + 1
                if score < lowest_correct_score:
                    lowest_correct_score = score
                if score < threshold:
                    pass_under_threshold += 1
                wordsuccess[target] = wordsuccess.get(target, 0) + 1
            else:
                if score < threshold:
                    fail_under_threshold += 1
            if (FAIL_DEBUG_ONLY and result == "FAIL") or (FAIL_DEBUG_ONLY != True):
                print "\t" + description + "-" + "context" + "\t-\t" + result + " - " + str(score)
#                if score == 1:
#                    print prediction

    # write csv file for Kaggle test
    if WRITE_TEST:
        write_results_to_csv(results, RESULTS_FILE)
        end("Finished creating test file")

    # fallback use - debug output
    if not WRITE_TEST:
        print "\nPERFORMANCE SUMMARY"
        for description in summary.keys():
            if description == "total":
                continue
            print "\t" + description + ": " + str(float(summary[description]) / summary["total"])
        print "\n"
        # time stats
        end(("\tProcessed %d tests" % summary['total']))

    print "\nBUILD OPTIONS"
    print "\tPOS Filter:\t\t%s" % ("Disabled", "Enabled")[POS_FILTER]
    print "\tSentence Context only:\t%s" % ("Disabled", "Enabled")[TEST_BY_SENTENCE]
    print "\tTest Limit:\t\t%d" % WRITE_LIMIT
    print "\tNote(s):\t\t" + BUILD + "\n"

    # unknown count metrics
    print "Predicted U: %d" % count
    for key in counts.keys():
        print key + ": %d" % counts[key]

    # overall prediction stat summary
    print "\nAvg Score: %f" % (float(sum(scores))/float(len(scores)))
    print "Lowest Correct Score: %f" % lowest_correct_score
    print "Preset Threshold Score: %f" % threshold
    print "\tPassed While Under Threshold: %d" % pass_under_threshold
    print "\tFailed While Under Threshold: %d" % fail_under_threshold

    # word-specific prediction stats (sorted by alpha order for convenience)
    print "\nWord Accuracy"
    for word in sorted(wordtotal.keys()):
        print word + ": %f" % (float(wordsuccess.get(word, 0))/float(wordtotal.get(word, 0)))

# thoughts for diagnosing cause of failure
# 1. word sense (e.g., is word sense 'unknown' and thus will always be wrong?)
# 2. number of senses (e.g., does it have a large number of entries, which are subtly different?)
# 3. is lemmatization causing issues (e.g., add vs added)