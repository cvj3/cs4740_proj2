# cs4740_proj2
Word Sense Disambiguation


Running Our Suite:
There are multiple files that work together, and we focused on building and tweaking many approaches,
so many of these files are not necessary or wholly relevant to the main approach we settled on.  We left
this code to show the various approaches we explored and the functions we built (many of which we didn't 
want to delete in case we found ourselves wanting to use them later).  Note that this also includes trained
data and files used for other approaches and submissions.

To run our whole suite, you'll need to modify config.py to your liking:
(note that this doesn't do the training / file setup, as these are already pre-built and included with the submission.)

TEST_BY_SENTENCE	- Set this to True to run our algorithm with the context being pulled just from the immediate sentence.
					- Set this to False to run our algorithm with the context being pulled from all words in the paragraph.

WRITE_TEST	- Set this to False to run our algorithm trained on only 75% of the training set, and tested on the remaining 25%.
			- Set this to True to run our algorithm trained on 100% of the training set on the test set and to output the csv.
			
RESULTS_FILE	- This is the filename that will be given to the csv if WRITE_TEST is True.

BUILD	- This string will be printed at the end of the test run (used for remembering what the run is testing/what change was made)

We recommend TEST_BY_SENTENCE to be set to False and WRITE_TEST to be set to False so you can see the "All Words" context approach
in action on our local test set.

Once these flags are set, save the file, and run "python test.py" from the command line.

You may need to install some nltk libraries if you have not done so.  Open a python shell, type:
import nltk
nltk.download()
A window should come up.  We isntalled every package to be safe, and we reccomend you do the same.
You may also need to install numpy for python 2.7 on windows.  We included the necessary file for this in our "setup" folder with a
README explaining how to isntall numpy for python 2.7 on windows.  
