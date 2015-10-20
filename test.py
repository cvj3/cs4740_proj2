from config import TEST_BY_SENTENCE, WRITE_TEST, BUILD, RESULTS_FILE
from common import *
from predictDefinition import predict_definition, predict_random, predict_definition_by_trained_context, predict_definition_by_trained_context_defs
from context import get_context
if not WRITE_TEST: from data.trainingData import wsddata as test_set
else: from data.testData import wsddata as test_set
from random import randint

if __name__ == "__main__":
	summary = {}
	start()
	results = []
	counts = {}
	scores = []
	lowest_correct_score = 100
	threshold = .001
	pass_under_threshold = 0
	fail_under_threshold = 0
	if not WRITE_TEST: splitter = 0 # tracks index to help split training data into 75% for training, and 25% for test.
	count = 0
	for i in range(len(test_set)):
		text = test_set[i]["context"]
		target = test_set[i]["word"]
		answers = test_set[i]["answer_ids"]
		instance = test_set[i]["id"]
		context, description = get_context(text, target)
			
		if not WRITE_TEST:
			splitter += 1
			if splitter < 4: # Every 4th training item is used for testing.
				continue
			else:
				splitter = 0
			summary["total"] = summary.get("total", 0) + 1
			print "TEST " + str(i + 1) + ": " + target.upper()			
		try:
			prediction, score = predict_definition_by_trained_context(context, target, description)
			source = 1
		except:
			try:
				prediction, score = predict_definition_by_trained_context_defs(context, target, description) #fall back to context def matching if no match between contexts
				counts["Context Def Fallbacks"] = counts.get("Context Def Fallbacks", 0) + 1
				source = 2
			except:
				prediction, score = predict_definition(context, target) #Fall back to Lesk approach if no match between context defs
				counts["Lesk Fallbacks"] = counts.get("Lesk Fallbacks", 0) + 1
				source = 3
		results.append(instance + "," + prediction)
		scores.append(score)
		if WRITE_TEST and not (i % 10): print "Parsed line: %d" % (i)
		if not WRITE_TEST:
			result = "FAIL"
			if prediction == "U": count +=1
			if prediction in answers:
				if source == 2: counts["Context Def Fallback Successes"] = counts.get("Context Def Fallback Successes", 0) + 1
				if source == 3: counts["Lesk Fallback Successes"] = counts.get("Lesk Fallback Successes", 0) + 1
				result = "PASS"
				summary[description] = summary.get(description, 0) + 1
				if score < lowest_correct_score: lowest_correct_score = score
				if score < threshold: pass_under_threshold += 1
			else:
				if score < threshold: fail_under_threshold += 1
			print "\t" + description + "-" + "context" + "\t-\t" + result + " - " + str(score)

	if not WRITE_TEST:
		print "\n\nSUMMARY"
		for description in summary.keys():
			if description == "total": continue
			print description + ": " + str(float(summary[description]) / summary["total"])
		print "\n"
		end(("Finished %d tests" % summary['total']))
	else:
		write_results_to_csv(results, RESULTS_FILE)
		end("Finished creating test file")

	print "CHANGES: " + BUILD + "\n"
	print "Predicted U: %d" % count

	for key in counts.keys():
		print key + ": %d" % counts[key]

	print "\nAvg Score: %f" % (float(sum(scores))/float(len(scores)))
	print "Lowest Correct Score: %f" % lowest_correct_score
	print "Preset Threshold Score: %f" % threshold
	print "\tPassed While Under Threshold: %d" % pass_under_threshold
	print "\tFailed While Under Threshold: %d" % fail_under_threshold
