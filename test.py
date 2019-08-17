from main import *
from test_vectors import *

def testFunction(testName, testString):
	
	# Run the function
	output = findDirectIncludes(testString)

	if 1:
		pass
	else:
		# Display output to Command Line
		print("\n" + testName)
		if isinstance(output, set):
			for idx, header in enumerate(output):
				print("Header {}: {}".format(idx + 1, header))
		elif isinstance(output, Exception):
			print("Encountered Exception:\n{}".format(output))

	return output




print("Test Suite:\t findDirectIncludes")

testVectors = {1: ("Test 1:", testString1),
			   2: ("Test 2:", testString2),
			   3: ("Test 3:", testString3),
			   4: ("Test 4:", testString4),
			   5: ("Test 5:", testString5)}

expectedOutputs = {1: {("firstHeader.h", 4, 46, 74),
	                   ("secondHeader.h", 5, 75, 109), 
	                   ("thirdHeader.h", 6, 110, 139), 
	                   ("fourthHeader.h", 7, 140, 175), 
	                   ("fifthHeader.h", 8, 176, 200), 
	                   ("sixthHeader.h", 9, 201, 224),
	                   ("seventhHeader.h", 10, 248, 274),
	                   ("eight_Header.h", 11, 297, 322),
	                   ("firstHeader.h", 12, 323, 347)},
				   2: Exception(exceptionBase.format("#include \"promptException.c\"")),
				   3: Exception(exceptionBase.format("#include <promptException.H>")),
				   4: Exception(exceptionBase.format("#include <promptException.hh>")),
				   5: Exception(exceptionBase.format("#include \"promptException.hh\""))}

for testNumber in range(1, 6, 1):

	# Select Inputs
	testName, testString = testVectors[testNumber]

	# Run the Test
	output = testFunction(testName, testString)

	# Check the Results
	if testNumber == 1:
		success = 1 if output == expectedOutputs[testNumber] else 0
	else:
		success = 1 if type(output) is type(expectedOutputs[testNumber]) and expectedOutputs[testNumber].args == output.args else 0

	# Display Result
	print("{}\t{}".format(testName, "Pass" if success == 1 else "Fail"))