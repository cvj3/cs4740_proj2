from common import *
from predictDefinition import predict_definition, predict_random, predict_definition_by_trained_context, predict_definition_by_trained_context_defs
from context import get_all_contexts
from data.testData import wsddata as test_set
from random import randint

TEST_BY_CONTEXT = True
WRITE_TEST = True

if __name__ == "__main__":
	summary = {}
	start()
	results = []
	if TEST_BY_CONTEXT and not WRITE_TEST: splitter = 0 # tracks index to help split training data into 75% for training, and 25% for test.

	for i in range(len(test_set)):
		ind = i #randint(0,len(test_set)-1)
		text = test_set[ind]["context"]
		target = test_set[ind]["word"]
		answers = test_set[ind]["answer_ids"]
		instance = test_set[ind]["id"]
		contexts = get_all_contexts(text, target)

		if TEST_BY_CONTEXT:
			if not WRITE_TEST:
				splitter += 1
				if splitter < 4: # Every 4th training item is used for testing.
					continue
				else:
					splitter = 0
				summary["total"] = summary.get("total", 0) + 1
				print "TEST " + str(i + 1) + ": " + target.upper()
			for pair in contexts:
				context = pair[0]
				description = pair[1]
				try:
					prediction = predict_definition_by_trained_context_defs(context, target, description)
				except:
					prediction = predict_definition(context, target) #Fall back to Lesk approach if senseid has not been seen
					summary["Lesk Fallback - " + description] = summary.get("Lesk Fallback - " + description, 0) + 1
				results.append(instance + "," + prediction)
				if not WRITE_TEST:
					result = "FAIL"
					if prediction in answers:
						result = "PASS"
						summary[description] = summary.get(description, 0) + 1
					print "\t" + description + "-" + "context" + "\t-\t" + result
				
		else:
			print "TEST " + str(i + 1) + ": " + target.upper()
			summary["total"] = summary.get("total", 0) + 1
			for pair in contexts:
				context = pair[0]
				description = pair[1]
				prediction = predict_definition(context, target)
				result = "FAIL"
				if prediction in answers:
					result = "PASS"
					summary[description] = summary.get(description, 0) + 1
				print "\t" + description + "\t-\t" + result		

		'''
		prediction = predict_random(target)
		description = "Random"
		result = "FAIL"
		if prediction in answers:
			result = "PASS"
			summary[description] = summary.get(description, 0) + 1
		print "\t" + description + "\t\t-\t" + result
		'''

	if not WRITE_TEST:
		print "\n\nSUMMARY"
		for description in summary.keys():
			if description == "total": continue
			print description + ": " + str(float(summary[description]) / summary["total"])
		print "\n"
		end(("Finished %d tests" % summary['total']))
	else:
		write_results_to_csv(results)
		end("Finished creating test file")
