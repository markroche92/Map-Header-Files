from main import *
import unittest
from test_vectors import *


class TestClass(unittest.TestCase):

	# Tests for the function findDirectIncludes()
	def test_findDirectIncludes(self):
		self.assertEqual(findDirectIncludes(testString1), {("firstHeader.h", 4, 46, 74),
	                   									   ("secondHeader.h", 5, 75, 109), 
	                   									   ("thirdHeader.h", 6, 110, 139), 
	                   									   ("fourthHeader.h", 7, 140, 175), 
	                   									   ("fifthHeader.h", 8, 176, 200), 
	                  									   ("sixthHeader.h", 9, 201, 224),
	                  									   ("seventhHeader.h", 10, 248, 274),
	                   									   ("eight_Header.h", 11, 297, 322),
	                   									   ("firstHeader.h", 12, 323, 347)})

		self.assertRaises(Exception, findDirectIncludes, testString2, msg = exceptionBase.format("#include \"promptException.c\""))
		self.assertRaises(Exception, findDirectIncludes, testString3, msg = exceptionBase.format("#include <promptException.H>"))
		self.assertRaises(Exception, findDirectIncludes, testString4, msg = exceptionBase.format("#include <promptException.hh>"))
		self.assertRaises(Exception, findDirectIncludes, testString5, msg = exceptionBase.format("#include \"promptException.hh\""))

	# Tests for the function findIncludesFromFilename()
	def test_findIncludesFromFilename(self):
		self.assertEqual(findIncludesFromFilename("./testFiles/example.c"), {("firstHeader.h", 2, 2, 30),
			                                                                 ("secondHeader.h", 3, 31, 65),
			                                                                 ("thirdHeader.h", 4, 66, 95)})
		self.assertEqual(findIncludesFromFilename("./testFiles/example2.c"), {("secondHeader.h", 2, 2, 36),
			                                                                  ("seventhHeader.h", 3, 37, 68),
			                                                                  ("sixthHeader.h", 4, 69, 98)})
		self.assertEqual(findIncludesFromFilename("./testFiles/fourthHeader.h"), {("fifthHeader.h", 4, 4, 28)})

		self.assertRaises(Exception, findIncludesFromFilename, "./exceptionFiles/exception.c", 
			                                                   msg = exceptionBase.format("#include <secondHeader.X>"))
		self.assertRaises(Exception, findIncludesFromFilename, "./nonExistantFile.c") 


if __name__ == "__main__":
	unittest.main()