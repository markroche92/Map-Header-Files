import re
import getopt
import sys

exceptionBase = 'Found inclusion of file not ending in .h: \nExample: {}';

# If invalid header found within #include statement: 	
# Exception object returned.
#
# If no invalid headers found: 							
# Output in the for of a set of tuples.
# Each tuple consists of (header file name, line number, char number start, char number end)
# 'char number start' and 'char number end' refer to span '#include ... "/>'
def findDirectIncludes(searchString):

	includeInfo = set()

	matches = re.finditer(r'#include\s*["<][\sa-zA-Z0-9_]+[.][a-zA-Z]+\s*[>"]', searchString)

	for match in matches:

		lineNumber = searchString.count('\n', 0, match.start())

		if not re.search(r'[.]h\s*[>""]', match.group(0)):
			 return Exception(exceptionBase.format(match.group(0)))
		
		inQuotes = re.search(r'["<][\sa-zA-Z0-9_]+.h', match.group(0)).group(0)
		headerName = re.search(r'[a-zA-Z0-9_]+.h', inQuotes).group(0)

		includeInfo.add((headerName, lineNumber, match.start(), match.end()))
	
	return includeInfo