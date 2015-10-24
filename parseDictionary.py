import xml.etree.ElementTree as ET
import os
import sys


__author__ = "Alin Barsan, Curtis Josey"


# load/parse/cache dictionary as dictionary object
def main(param1, param2):
    # Read and Parse XML
    wsdDictionary = buildDictionary(param1, param2, True)

    # Write out to a dictionary file (lib/Dictionary.py)
    writeDictionary(param1, param2, wsdDictionary)

    # done
    quit()


def buildDictionary(path, filename, verboseMode=False):
    wsdDictionary = {}

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, path + '/' + filename)
    # load xml tree
    tree = ET.parse(filename)
    # get root of xml tree
    root = tree.getroot()
    # loop through xml tree
    for lex in root:
        # get first entry
        item = lex.get('item')
        # parse word from part of speech
        temp = str(item).split('.')
        key_word = temp[0]
        part_of_speech = temp[1]
        if verboseMode:
            print "entry: %s, pos: %s" % (key_word, part_of_speech)

        entryDef = []
        # get definitions of word
        for x in lex.iter("sense"):
            # source: unused
            # synset: unused
            if verboseMode:
                print "id: %s, gloss: %s" % (x.get("id"), x.get("gloss"))

            # split gloss between definition and samples
            temp = str(x.get("gloss")).split('"')
            gloss = temp[0]
            example = ""
            for ex in temp[1:]:
                example += ex

            entryDef.append([gloss, example, x.get("id")])
        # build dictionary object
        wsdDictionary[key_word] = wsdDictionary.get(key_word, {})
        wsdDictionary[key_word]["defs_and_examples"] = entryDef
        wsdDictionary[key_word]["type"] = part_of_speech

    return wsdDictionary


def writeDictionary(path, filename, dictionary, verboseMode=False):
    f = open(path + "/" + filename.replace(".xml", ".py"), "w")
    output = str(dictionary).replace("{", "{\n\t").replace("}", "\n}").replace("},\n\t", "},\n").replace("\t", "", 1)
    # No longer replacing space after comma with newline since it messes up strings containing commas
    # As a result, generated .py files are less readable.
    output = 'wsdDictionary = ' + output
    f.write(output)
    f.close()



if __name__ == "__main__":
    dictionary_path = "lib"
    dictionary_filename = "Dictionary.xml"

    # cache arguments passed via command line
    args = sys.argv

    # -h or -help or --help or no arguments supplied
    if "-h" in args or "-help" in args or "--help" in args or len(args) < 2:
        print "\n\n" + os.path.basename(__file__) + " USAGE GUIDE:\n\n"

        print "\t-p\tPath Flag\n"
        print "\t\tTo be followed by a string value in double quotes."
        print "\t\tThe relative path to the folder containing the dictionary."
        print "\t\tThis flag is a required parameter.\n\n"

        print "\t-f\tDictionary File\n"
        print "\t\tTo be followed by an integer value that determines"
        print "\t\tThe file name of the dictionary, in xml format."
        print "\t\tThis flag is optional, and defaults to Dictionary.xml.\n\n"

        print "\t-h, -help, or --help\n"
        print "\t\tDisplays the help menu, describeing all possible arguments."

        print "\n\n\tSAMPLE USAGE:"
        print "\t\tpython " + os.path.basename(__file__) + \
              " -d \"" + dictionary_path + "\"" + \
              " -f \"" + dictionary_filename + "\""
        quit()

    # -p: the "seed" sentence fragment
    if "-p" in args:
        # get number of sentences to generate
        value_index = args.index("-p") + 1
        if len(args) <= value_index:
            print "\nExpected a field after '-p'"
            quit()
        else:
            dictionary_path = args[value_index]
    else:
        print "-p command missing, use -help for additional details."

    # -f: the number of senteneces to generate, defaults to 1
    if "-f" in args:
        value_index = args.index("-f") + 1
        if len(args) <= value_index:
            print "\nExpected a field after '-f'"
            quit()
        else:
            dictionary_filename = args[value_index]

    main(dictionary_path, dictionary_filename)
