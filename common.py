import datetime
from nltk.stem.wordnet import WordNetLemmatizer
import nltk
lm = WordNetLemmatizer()


TIMER = None

def start():
	global TIMER
	TIMER = datetime.datetime.now()

def end(message):
	global TIMER
	end = datetime.datetime.now()
	print "\n" + message + " in %s seconds.\n" % str((end-TIMER).seconds)
	TIMER = None


def filter_tokens(tokens):
	filtered_tokens = []
	tokens_with_pos = nltk.pos_tag(tokens)
	for pair in tokens_with_pos:
		token = pair[0]
		pos = pair[1]
		token = token.lower().strip()
		if not any(char.isalnum() for char in token): continue #if all punct
		elif not ("N" in pos and not "I" in pos): continue #https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
		else:
			token = lm.lemmatize(token)
			filtered_tokens.append(token)
	return filtered_tokens

def write_results_to_csv(results, filename):
	f = open(filename + ".csv", "w")
	f.write("Id,Prediction\n")
	output = "\n".join(results)
	f.write(output)
	f.close()