import re
import getopt
import sys
import os
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

def getCheckedChildren(newKeysPrevMapped, previousMappings):

	assert type(newKeysPrevMapped) is set, 'First argument of getCheckedChildren() should be a set()'
	assert type(previousMappings) is dict, 'Second argument of getCheckedChildren() should be a dictionary of sets of tuples'

	checkedChildren = set()
	# Get children - these are known to be previously searched for other TU
	while(newKeysPrevMapped > checkedChildren):
		# Get names of files includes within files which are known to have been checked for another TU
		childNewKeys = {tup[0] for name in newKeysPrevMapped - checkedChildren for tup in previousMappings[name]}
		# Add to set of checked child keys
		checkedChildren |= newKeysPrevMapped - checkedChildren
		# Add to set of keys known to be mapped during previous search
		newKeysPrevMapped |= childNewKeys

	return newKeysPrevMapped

# Function takes a filename and a base mapping between filenames and included headers
# The base mapping contains information for previously analysed files
# When identifying new files to search, previously searched files are ignored
def searchTranslationUnit(abPaths, filename, previousMappings):

	assert type(abPaths) is dict, 'First argument of searchTranslationUnit() should be a dictionary'
	assert type(filename) is str, 'Second argument of searchTranslationUnit() should be a string'
	assert type(previousMappings) is dict, 'Third argument of searchTranslationUnit() should be a dictionary'


	mapping = {filename : None}
	filesSearched = set()

	while(mapping.keys() > filesSearched):
		# Get includes for a single file. Update list of keys, for new headers found
		mapping[filename] = findIncludesFromFilename(os.path.join(abPaths["source"], filename) if ".c" == filename[-2:] 
			                                                 else os.path.join(abPaths["includes"], filename))

		# New keys are those found in file which have not yet been searched for this Translation Unit
		newKeys = {tup[0] for tup in mapping[filename] if tup[0] not in mapping.keys()}

		# Find which new keys have been previously mapped within another Translation Unit
		newKeysPrevMapped = newKeys.intersection(set(previousMappings))

		getCheckedChildren(newKeysPrevMapped, previousMappings)

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

# Check whether the specified subdirectory exists, and that in contains a 'source' and 'includes' directory. If not, raise exception.
# Acceptable input from user for directory command line argument are of the form:
# ===============================================================================
# .                      : current directory - this means that 'includes' and 'source' should be immediate subdirectories
# ./directory/directory2 : directory of interest is downstream of current directory. 
# ./../../directory      : directory of interest is a parent of current working directory. 
def getAbsolutePaths(relativePath):

	if not relativePath or relativePath[0] != '.': 
		raise Exception("{} is not a valid relative path, as it does not begin with \'.\'".format(relativePath))

	if len(relativePath) == 1:
		absolutePaths = {'base' : os.getcwd()}
	elif relativePath[0:2] == "..":
		absolutePaths = {'base' : os.path.join(os.getcwd(), relativePath)}
	else:
		absolutePaths = {'base' : os.path.join(os.getcwd(), relativePath[2:])}


	for directory in ('','source', 'includes'):
		if directory: absolutePaths[directory] = os.path.join(absolutePaths['base'], directory)
		path = os.path.join(absolutePaths['base'], directory)
		if not os.path.isdir(path): raise Exception("{} is not a valid directory".format(path))

	return absolutePaths



def main():

	# Check number of command line arguments
	if len(sys.argv) < 4: raise Exception("Insufficient number of command-line arguments provided")

	# Check validity of path
	absolutePaths = getAbsolutePaths(sys.argv[1])

	# Check validity of command to run function
	if sys.argv[2] == "-m":
		sourceFileNames = sys.argv[3:]
	elif sys.argv[2] == "-f":
		with open(sys.argv[3], 'r') as textFile:
			sourceFileNames = textFile.read().split("\n")
			# Remove empty lines read in from .txt file. Set also removes duplicate filenames
			sourceFileNames = list(filter(lambda val: val != "", sourceFileNames))
			sourceFileNames.sort()
	else:
		raise Exception("Command line argument \"{}\" not recognised".format(sys.argv[2]))

	sourceDictsList = []

	for filename in sourceFileNames:
		# Check file extension is either .c or .h
		if filename[-2:] != ".c" and filename[-2:] != ".h": raise Exception("Attempting to analyse file with unrecognised extension: {}".format(filename))
		# Second argument to searchTranslationUnit is a dictionary of all file : match entries found so far
		sourceDictsList.append(searchTranslationUnit(absolutePaths, filename, dict(collections.ChainMap(*sourceDictsList))))

	visualise(sourceDictsList, sourceFileNames)

	return sourceDictsList

if __name__ == "__main__":
	main()