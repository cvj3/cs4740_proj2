import xml.etree.ElementTree as ET
import os
import sys


__author__ = "Alin Barsan, Curtis Josey"


# load/parse/cache data-set as dictionary object
def main(param1, param2):
    # Read and Parse XML
    wsdData = buildData(param1, param2, False)

    # Write out to a dictionary file (lib/data.py)
    writeData(param1, param2, wsdData)

    quit()


def buildData(path, filename, verboseMode=False):
    wsdData = []

    dir = os.path.dirname(__file__)
    filename = os.path.join(dir, path + '/' + filename)
    # read XML and add wrapper tags
    dataSet = open(filename).read()
    # add document wrapper tags
    dataSet = "<docRoot>" + os.linesep + dataSet + os.linesep + "</docRoot>"

    # load xml tree
    try:
        # get root of xml tree
        docRoot = ET.fromstring(dataSet)
        # loop through xml tree
        for lex in docRoot:
            # get first entry
            item = lex.get('item')
            # parse word from part of speech
            temp = str(item).split('.')
            key_word = temp[0]
            part_of_speech = temp[1]
            if verboseMode:
                print "entry: %s, pos: %s" % (key_word, part_of_speech)

            # print lex.tag, lex.attrib

            for instance in lex.iter('instance'):
                answerID = []
                instanceID = instance.get("id")
                for answer in instance.iter('answer'):
                    answerID.append(answer.get("senseid"))
                thisContext = ""
                for context in instance.iter('context'):
                    for text in context.itertext():
                        if " " not in text:
                            text = "<tar>" + text + "</tar>"
                        thisContext += text
                thisContext += os.linesep
                thisContext = thisContext.strip().replace("\r", "").replace("\n", "").replace(" n't", "n't")
                thisContext = thisContext.replace(" '", "'")  # s.replace("'", r"\'")
                # build data object
                wsdData.append({"word": key_word, "type": part_of_speech, "id": instanceID,
                                "answer_ids": answerID, "context": thisContext})

            # wsdData[key_word] = wsdData.get(key_word, {})
            # wsdData[key_word]["defs_and_examples"] = entryDef
            # wsdData[key_word]["type"] = part_of_speech
    except ET.ParseError as e:
        # if error occurs while parsing, create a debug dump with some useful information
        formatted_e = str(e)
        line = int(formatted_e[formatted_e.find("line ") + 5: formatted_e.find(",")])
        column = int(formatted_e[formatted_e.find("column ") + 7:])
        split_str = str("<data-set>" + dataSet + "</data-set>").split("\n")
        print "{}\n{}^".format(split_str[line - 1], len(split_str[line - 1][0:column])*"-")
        print e

    return wsdData


# write dataset to dictionary object file
def writeData(path, filename, dictionaryObject, verboseMode=False):
    f = open(path + "/" + filename.replace(".xml", ".py"), "w")
    output = str(dictionaryObject).replace("{", "{\n\t").replace("}", "\n}").replace("},\n\t", "},\n").replace("\t", "", 1)
    # No longer replacing space after comma with newline since it messes up strings containing commas
    # As a result, generated .py files are less readable.
    output = 'wsddata = ' + output
    f.write(output)
    f.close()


if __name__ == "__main__":
    data_path = "data"
    data_filename = "training-data.xml"

    # cache arguments passed via command line
    args = sys.argv

    # -h or -help or --help or no arguments supplied
    if "-h" in args or "-help" in args or "--help" in args or len(args) < 2:
        print "\n\n" + os.path.basename(__file__) + " USAGE GUIDE:\n\n"

        print "\t-p\tPath Flag\n"
        print "\t\tTo be followed by a string value in double quotes."
        print "\t\tThe relative path to the folder containing the data."
        print "\t\tThis flag is a required parameter.\n\n"

        print "\t-f\tData File\n"
        print "\t\tTo be followed by an integer value that determines"
        print "\t\tThe file name of the data, in xml format."
        print "\t\tThis flag is optional, and defaults to data.xml.\n\n"

        print "\t-h, -help, or --help\n"
        print "\t\tDisplays the help menu, describeing all possible arguments."

        print "\n\n\tSAMPLE USAGE:"
        print "\t\tpython " + os.path.basename(__file__) + \
              " -d \"" + data_path + "\"" + \
              " -f \"" + data_filename + "\""
        quit()

    # -p: the "seed" sentence fragment
    if "-p" in args:
        # get number of sentences to generate
        value_index = args.index("-p") + 1
        if len(args) <= value_index:
            print "\nExpected a field after '-p'"
            quit()
        else:
            data_path = args[value_index]
    else:
        print "-p command missing, use -help for additional details."

    # -f: the number of senteneces to generate, defaults to 1
    if "-f" in args:
        value_index = args.index("-f") + 1
        if len(args) <= value_index:
            print "\nExpected a field after '-f'"
            quit()
        else:
            data_filename = args[value_index]

    main(data_path, data_filename)
