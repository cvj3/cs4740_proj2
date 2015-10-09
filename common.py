import datetime
from nltk.stem.wordnet import WordNetLemmatizer
lm = WordNetLemmatizer()

NON_VALUED_WORDS = ["for", "and", "nor", "but", "or", "yet", "to", "in", "of", "at", "on", "a", "an", "the"]
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
	for token in tokens:
		token = token.lower().strip()
		if not any(char.isalnum() for char in token): continue #if all punct
		elif token in NON_VALUED_WORDS: continue
		else:
			token = lm.lemmatize(token)
			filtered_tokens.append(token)
	return filtered_tokens