import datetime
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.stem.snowball import SnowballStemmer
s = SnowballStemmer("english")
from nltk.corpus import stopwords
stopwords = stopwords.words("english")

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
	for token in tokens:
		token = token.lower().strip()
		#token = lm.lemmatize(token)
		if not any(char.isalnum() for char in token): continue #if all punct
		if token in stopwords: continue # if token is a stopword
		if token == "n't": continue # if token has useless word fragment
		if len(token) <= 3: continue # if token is very short
		if token.isdigit(): continue # if all numerals
		if "/tar" in token: continue # if token has target tag still remaining
		else:			
			filtered_tokens.append(token)
			#filtered_tokens.append(s.stem(token))
	return filtered_tokens

def write_results_to_csv(results, filename):
	f = open(filename + ".csv", "w")
	f.write("Id,Prediction\n")
	output = "\n".join(results)
	f.write(output)
	f.close()

if __name__ == "__main__": # test filtering tokens
	import sys
	args = sys.argv
	filtered = filter_tokens(nltk.word_tokenize(args[1]))
	print filtered
	print "\nLength: %d" % len(filtered)