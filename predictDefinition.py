import nltk
#go to python shell, do import nltk, then do nltk.download(), then download all packages.
from nltk.corpus import wordnet as wn
from lib.Dictionary import wsdDictionary as defs
from data.contextData import wsddata as contexts
import sys
import datetime
from common import *
from random import randint


POINTS_FOR_CONSECUTIVE_WORD = 3
POINTS_FOR_NONCONSECUTIVE_WORD = 1
ADDITIONAL_POINTS_FOR_SIMPLIFIED_LESK = 3
#POINTS_FOR_EXAMPLE_MATCH = .5 #not currently being used

def words_to_parsed_definitions(context_words, target_word):
	definition_glob = []
	for word in context_words:
		for syn in wn.synsets(word):
			definition_glob += nltk.word_tokenize(syn.definition())
			definition_glob.append("<delim>")
		definition_glob.append(word)
		definition_glob.append("<context_word>")
	target_definitions = defs[target_word]["defs_and_examples"]
	definition_glob = filter_tokens(definition_glob)
	return definition_glob, target_definitions

def score_parsed_definitions(definition_glob, target_definitions):
	senseids_with_scores = []
	for data in target_definitions:
		example = data[1]
		senseid = data[2]		
		#definition = nltk.word_tokenize(data[0])
		definition = nltk.word_tokenize(data[0] + " " + example)
		fdefinition = filter_tokens(definition)
		score = 0
		consecutive = False
		for i in range(len(definition_glob) - 1):
			token = definition_glob[i]
			next_token = definition_glob[i+1]
			if token in fdefinition:
				if consecutive: score += POINTS_FOR_CONSECUTIVE_WORD
				else:
					score += POINTS_FOR_NONCONSECUTIVE_WORD
					consecutive = True
				if next_token == "<context_word>":  # if current word is flagged as being a context word, award additional points
					score += ADDITIONAL_POINTS_FOR_SIMPLIFIED_LESK
			else:
				consecutive = False
		senseids_with_scores.append((senseid, score))
	return senseids_with_scores

def print_definition_scores(senseids_with_scores):
	print "Score:\tSenseId:"
	for pair in senseids_with_scores:
		print str(pair[1]) + "\t" + str(pair[0])

def predict_definition(context_words, target_word, verbose=False):
	definition_glob, target_definitions = words_to_parsed_definitions(context_words, target_word)
	senseids_with_scores = score_parsed_definitions(definition_glob, target_definitions)
	if verbose: print_definition_scores(senseids_with_scores)
	highest = senseids_with_scores[0][1]
	best_def = senseids_with_scores[0][0]
	for pair in senseids_with_scores:
		score = pair[1]
		senseid = pair[0]
		if score > highest:
			highest = score
			best_def = senseid
	return best_def

def predict_random(target_word):
	definitions = defs[target_word]["defs_and_examples"]
	ind = randint(0, len(definitions) - 1)
	return definitions[ind][2]



def predict_definition_by_trained_context(context, target_word, description):
	target_definitions = defs[target_word]["defs_and_examples"]
	scores = {}
	for data in target_definitions:
		senseid = data[2]
		if not contexts[target_word].get(senseid):
			continue
		con = contexts[target_word][senseid][description]
		for c in context:
			if c in con:
				scores[senseid] = scores.get(senseid, 0) + 1
	best_def = scores.keys()[0]
	best_score = scores[scores.keys()[0]]
	for senseid in scores.keys():
		score = scores[senseid]
		if score > best_score:
			best_score = score
			best_def = senseid
	return best_def

def score_contexts(context_target, context_history):
	score = 0
	tar_glob = []
	for word in context_target:
		for syn in wn.synsets(word):
			tar_glob += nltk.word_tokenize(syn.definition())
	his_glob = []
	for word in context_history:
		for syn in wn.synsets(word):
			his_glob += nltk.word_tokenize(syn.definition())
	for item in tar_glob:
		if item in his_glob:
			score += 1
	return score

def predict_definition_by_trained_context_defs(context, target_word, description):
	target_definitions = defs[target_word]["defs_and_examples"]
	scores = {}
	for data in target_definitions:
		senseid = data[2]
		if not contexts[target_word].get(senseid):
			continue
		con = contexts[target_word][senseid][description]
		scores[senseid] = score_contexts(context, con)
	best_def = scores.keys()[0]
	best_score = scores[scores.keys()[0]]
	for senseid in scores.keys():
		score = scores[senseid]
		if score > best_score:
			best_score = score
			best_def = senseid
	return best_def

#usage: 'main.py [context_word1,context_word2] target_word'
if __name__ == "__main__":
	args = sys.argv[1:]
	if len(args) > 2:
		print "\nPlease use command format: 'main.py [context_word1,context_word2] target_word'\nBe sure to avoid spaces in your list of context words."
		quit()
	context_words = args[0][1:-1].split(",")
	target_word = args[1]
	start()
	definition = predict_definition(context_words, target_word)
	end("Predicted definition")
	print "\nDefinition:"
	print "\t" + definition