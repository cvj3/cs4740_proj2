import nltk
#nltk.download('punkt')  # Uncomment these if the package is not yet installed
#nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
lm = WordNetLemmatizer()
from nltk.corpus import wordnet as wn
import sys
import datetime
from common import *

POINTS_FOR_CONSECUTIVE_WORD = 2
POINTS_FOR_NONCONSECUTIVE_WORD = 1
ADDITIONAL_POINTS_FOR_SIMPLIFIED_LESK = 2
POINTS_FOR_EXAMPLE_MATCH = .5

def words_to_parsed_definitions(context_words, target_word):
	definition_glob = []
	for word in context_words:
		for syn in wn.synsets(word):
			definition_glob += nltk.word_tokenize(syn.definition())
			definition_glob.append("<delim>")
		definition_glob.append(word)
		definition_glob.append("<context_word>")
	target_definitions = [nltk.word_tokenize(syn.definition()) for syn in wn.synsets(target_word, pos=wn.NOUN)]
	definition_glob = filter_tokens(definition_glob)
	return definition_glob, target_definitions

def score_parsed_definitions(definition_glob, target_definitions):
	definitions_with_scores = []
	for definition in target_definitions:
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
		definitions_with_scores.append((definition, score))
	return definitions_with_scores

def print_definition_scores(definitions_with_scores):
	print "Score:\tDefinition:"
	for pair in definitions_with_scores:
		definition = " ".join(pair[0])
		definition = (definition[:65] + '...') if len(definition) > 65 else definition
		print str(pair[1]) + "\t" + definition

def predict_definition(context_words, target_word):
	definition_glob, target_definitions = words_to_parsed_definitions(context_words, target_word)
	definitions_with_scores = score_parsed_definitions(definition_glob, target_definitions)
	print_definition_scores(definitions_with_scores)
	highest = definitions_with_scores[0][1]
	best_def = definitions_with_scores[0][0]
	for pair in definitions_with_scores:
		score = pair[1]
		definition = pair[0]
		if score > highest:
			highest = score
			best_def = definition
	return " ".join(best_def)

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