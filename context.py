from common import *
from lib.Dictionary import wsdDictionary as defs
from data.trainingData import wsddata as train_set
import nltk
import sys
import string
from parseData import writeData
from config import TEST_BY_SENTENCE, WRITE_TEST
#assuming target location is wrapped in <tar>word</tar>

def get_context_from_sentence(text, target):
	context = text
	ind = context.find("<tar>")
	while ind >= 0 and context[ind] not in [".", "!", "?"]:
		ind -= 1
	context = context[ind + 1:]
	ind = context.find("</tar>")
	while ind < len(context) and context[ind] not in [".", "!", "?"]:
		ind += 1
	context = context[:ind]
	context = context.replace("<tar>" + target.strip() + "</tar>", "").lower().replace(target,"")
	context = nltk.word_tokenize(context)
	context = filter_tokens(context)
	return context

def get_skipgram(text, target):
	context = get_context_from_sentence(text, target)
	while len(context) >= 10:
		context = context[1:-1]
	return context

def get_context_from_largest_words(text, target):
	context = text
	LARGEST = 10 # No words over length 10 will be taken
	SETS = 4 # All words of the largest 4 lengths <= 10 will be chosen
	context = context.replace("<tar>" + target.strip() + "</tar>", "").lower().replace(target,"")
	context = nltk.word_tokenize(context)
	filtered = filter_tokens(context)
	t = {}
	for token in filtered:
		if not len(token) in t.keys(): t[len(token)] = []
		t[len(token)].append(token)
	highest_lens = t.keys()[len(t.keys()) - SETS:]
	context = []
	for l in highest_lens:
		context += t[l]
	return context

def get_context_from_all_words(text, target):
	context = text
	context = context.replace("<tar>" + target.strip() + "</tar>", "").lower().replace(target,"")
	context = nltk.word_tokenize(context)
	context = filter_tokens(context)
	return context

def get_context(text, target):
	if TEST_BY_SENTENCE: context, description = get_context_from_sentence(text, target), "Sentence"
	else: context, description = get_skipgram(text, target), "Skipgram"
	#context, description = get_context_from_largest_words(text, target), "Largest Words"
	#context, description = get_context_from_all_words(text, target), "All Words"
	return context, description

if __name__ == "__main__":
	start()
	if not WRITE_TEST: splitter = 0 # tracks index to help split training data into 75% for training, and 25% for test.
	contexts = {}
	for i in range(len(train_set)):
		if not WRITE_TEST:
			splitter += 1
			if splitter == 4: # Every 4th training item is left for testing.
				splitter = 0
				continue
		text = train_set[i]["context"]
		target = train_set[i]["word"]		
		answers = train_set[i]["answer_ids"]
		contexts[target] = contexts.get(target, {})
		context, description = get_context(text, target)
		for senseid in answers:
			contexts[target][senseid] = contexts[target].get(senseid, {})				
			contexts[target][senseid][description] = contexts[target][senseid].get(description, [])
			contexts[target][senseid][description] += context
			contexts[target][senseid][description].append("<") #delim to prevent consecutive matches between different context groups
			contexts[target][senseid][description] = [x for x in contexts[target][senseid][description] if x != "tar"]
			contexts[target][senseid]["count"] =  contexts[target][senseid].get("count", 0) + 1
			contexts[target]["total"] = contexts[target].get("total", 0) + 1
	end("Finished building Context object")
	start()
	file_name = "contextSkip"
	if TEST_BY_SENTENCE: file_name = "contextData"
	if WRITE_TEST: file_name = file_name + "Full"
	writeData("data", file_name + ".py", contexts)
	#writeData("data", "contextLargestFull.py", contexts)
	end("Finsihed writing Context Data")