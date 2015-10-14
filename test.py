from common import *
from predictDefinition import predict_definition
from context import get_all_contexts
from data.trainingData import wsddata as test_set



if __name__ == "__main__":
	summary = {}
	start()
	for i in range(len(test_set)):
		text = test_set[i]["context"]
		target = test_set[i]["word"]
		print target.upper() + " TEST " + str(i + 1)
		answers = test_set[i]["answer_ids"]
		contexts = get_all_contexts(text, target)
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
	print "\n\nSUMMARY"
	for description in summary.keys():
		if description == "total": continue
		print description + ": " + str(float(summary[description]) / summary["total"])
	print "\n"
	end(("Finished %d tests" % summary['total']))
