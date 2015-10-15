from common import *
from lib.Dictionary import wsdDictionary as defs
from data.trainingData import wsddata as train_set
import nltk
import sys
import string
from parseData import writeData
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

def get_context_from_largest_words(text, target):
	context = text
	LARGEST = 10 # No words over 10 will be taken
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

def get_all_contexts(text, target):
	contexts = []
	#contexts.append((get_context_from_sentence(text, target), "Sentence"))
	contexts.append((get_context_from_largest_words(text, target), "Largest Words"))
	#contexts.append((get_context_from_all_words(text, target), "All Words"))
	return contexts

if __name__ == "__main__":
	start()
	#splitter = 0 # tracks index to help split training data into 75% for training, and 25% for test.
	contexts = {}
	for i in range(len(train_set)):
		#splitter += 1
		#if splitter == 4: # Every 4th training item is left for testing.
		#	splitter = 0
		#	continue
		text = train_set[i]["context"]
		target = train_set[i]["word"]		
		answers = train_set[i]["answer_ids"]
		contexts[target] = contexts.get(target, {})
		c = get_all_contexts(text, target)
		for pair in c:
			context = pair[0]
			description = pair[1]
			for senseid in answers:
				contexts[target][senseid] = contexts[target].get(senseid, {})				
				contexts[target][senseid][description] = contexts[target][senseid].get(description, [])
				contexts[target][senseid][description] += context
	end("Finished building Context object")
	start()
	writeData("data", "contextDataFull.py", contexts)
	end("Finsihed writing Context Data")