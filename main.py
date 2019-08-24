import re
import getopt
import sys
from visualise import *

exceptionBase = 'Found inclusion of file not ending in .h: \nExample: {}';

# If invalid header found within #include statement: 	
# Exception object returned.
#
# If no invalid headers found: 							
# Output in the for of a set of tuples.
# Each tuple consists of (header file name, line number, char number start, char number end)
# 'char number start' and 'char number end' refer to span '#include ... "/>'
def findDirectIncludes(searchString):

	matchSetSingleFile = set()

	matches = re.finditer(r'#include\s*["<][\sa-zA-Z0-9_]+[.][a-zA-Z]+\s*[>"]', searchString)

	for match in matches:

		matchString = match.group(0)
		lineNumber = searchString.count('\n', 0, match.start())

		if not re.search(r'[.]h\s*[>""]', matchString): raise Exception(exceptionBase.format(matchString))
		
		inQuotes = re.search(r'["<][\sa-zA-Z0-9_]+.h', matchString).group(0)
		headerName = re.search(r'[a-zA-Z0-9_]+.h', inQuotes).group(0)

		matchSetSingleFile.add((headerName, lineNumber, match.start(), match.end()))
	
	return matchSetSingleFile

# Read the content of a text file and pass to findDirectIncludes function
def findIncludesFromFilename(filename):

	with open(filename, 'r') as file:
		return findDirectIncludes(file.read())

# Function takes a filename and a base mapping between filenames and included headers
# The base mapping contains information for previously analysed files
# When identifying new files to search, previously searched files are ignored
def searchTranslationUnit(filename, previousMappings):

	mapping = {filename : None}
	filesSearched = set()

	while(mapping.keys() > filesSearched):
		# Get includes for a single file. Update list of keys, for new headers found
		mapping[filename] = findIncludesFromFilename(sys.argv[1] + filename)
		# New keys are those found in file which have not yet been searched for this Translation Unit
		newKeys = {tup[0] for tup in mapping[filename] if tup[0] not in mapping.keys()}

		# Find which new keys have been previously mapped within another Translation Unit
		newKeysPrevMapped = newKeys.intersection(set(previousMappings))

		checkedChildren = set()
		# Get children - these are known to be previously searched for other TU
		while(newKeysPrevMapped > checkedChildren):
			# Get names of files includes within files which are known to have been checked for another TU
			childNewKeys = {tup[0] for name in newKeysPrevMapped - checkedChildren for tup in previousMappings[name]}
			# Add to set of checked child keys
			checkedChildren |= newKeysPrevMapped - checkedChildren
			# Add to set of keys known to be mapped during previous search
			newKeysPrevMapped |= childNewKeys


		# Merge results from search of previous Translation Units
		mapping.update({**{key: previousMappings[key] for key in newKeysPrevMapped}})
		# Add these keys to searched file list
		filesSearched |= newKeysPrevMapped

		# Initialise new files to search
		mapping.update(dict(zip(newKeys - newKeysPrevMapped, [None] * len(newKeys - newKeysPrevMapped))))

		# Mark file as searched. Pick a new filename to search
		filesSearched.add(filename)


		unsearched = mapping.keys() - filesSearched
		if unsearched: filename = list(unsearched)[0]

	return mapping


def main(sourceFileNames = sys.argv[2:]):

	sourceDictsList = []

	for filename in sourceFileNames:
		# Second argument to searchTranslationUnit is a dictionary of all file : match entries found so far
		sourceDictsList.append(searchTranslationUnit(filename, dict(collections.ChainMap(*sourceDictsList))))

	visualise(sourceDictsList, sourceFileNames)

main()