from main import *
import unittest
from test_vectors import *
import argparse




class TestClass(unittest.TestCase):

	def setUp(self):
		print("\n\tRunning test suite for {}".format(self.shortDescription()), end = "")

	# Tests for the function findDirectIncludes()
	def test_findDirectIncludes(self):

		""" findDirectIncludes() """

		# Finding valid includes in a number of forms
		self.assertEqual(findDirectIncludes(testString1), {("firstHeader.h", 4, 46, 74),
	                   									   ("secondHeader.h", 5, 75, 109), 
	                   									   ("thirdHeader.h", 6, 110, 139), 
	                   									   ("fourthHeader.h", 7, 140, 175), 
	                   									   ("fifthHeader.h", 8, 176, 200), 
	                  									   ("sixthHeader.h", 9, 201, 224),
	                  									   ("seventhHeader.h", 10, 248, 274),
	                   									   ("eight_Header.h", 11, 297, 322),
	                   									   ("firstHeader.h", 12, 323, 347)})
		# Exception for included file ending with .c
		with self.assertRaises(Exception) as ex1:
			findDirectIncludes(testString2)
		self.assertEqual(exceptionBase.format("#include \"promptException.c\"") , str(ex1.exception))

		# Exception for file ending with .H
		with self.assertRaises(Exception) as ex2:
			findDirectIncludes(testString3)
		self.assertEqual(exceptionBase.format("#include <promptException.H>") , str(ex2.exception))

		# Exception for file ending with .hh
		with self.assertRaises(Exception) as ex3:
			findDirectIncludes(testString4)
		self.assertEqual(exceptionBase.format("#include <promptException.hh>") , str(ex3.exception))

		# Exception for file endoing with .hh
		with self.assertRaises(Exception) as ex4:
			findDirectIncludes(testString5)
		self.assertEqual(exceptionBase.format("#include \"promptException.hh\"") , str(ex4.exception))



	# Tests for the function findIncludesFromFilename()
	def test_findIncludesFromFilename(self):

		""" findIncludesFromFilename() """

		# Finding includes for example.c
		self.assertEqual(findIncludesFromFilename("./testFiles/source/example.c"), {("firstHeader.h", 2, 2, 30),
			                                                                        ("secondHeader.h", 3, 31, 65),
			                                                                        ("thirdHeader.h", 4, 66, 95)})
		
		# Finding includes for example2.c
		self.assertEqual(findIncludesFromFilename("./testFiles/source/example2.c"), {("secondHeader.h", 2, 2, 36),
			                                                                         ("seventhHeader.h", 3, 37, 68),
			                                                                         ("sixthHeader.h", 4, 69, 98)})
		
		# Finding includes from fourthHeader.h
		self.assertEqual(findIncludesFromFilename("./testFiles/includes/fourthHeader.h"), {("fifthHeader.h", 4, 4, 28)})

		# Exception for included file ending with .X
		with self.assertRaises(Exception) as ex1:
			findIncludesFromFilename("./exceptionFiles/exception.c")
		self.assertEqual(exceptionBase.format("#include <secondHeader.X>"), str(ex1.exception))

		# Exception for file not existing
		with self.assertRaises(Exception) as ex2:
			findIncludesFromFilename("./nonExistantFile.c")
		self.assertEqual("[Errno 2] No such file or directory: \'./nonExistantFile.c\'", str(ex2.exception))


	def test_main(self):

		""" main() """

		# Finding include map for example.c
		if "includeMap.pdf" in os.listdir(): os.remove("includeMap.pdf")

		sys.argv = ["main.py", "./testFiles/", "-m", "example.c"]
		self.assertEqual(main(), [{'example.c': {('firstHeader.h', 2, 2, 30),
                								 ('secondHeader.h', 3, 31, 65),
                								 ('thirdHeader.h', 4, 66, 95)},
								  'fifthHeader.h': set(),
								  'firstHeader.h': {('secondHeader.h', 3, 17, 42)},
			  					  'fourthHeader.h': {('fifthHeader.h', 4, 4, 28)},
								  'secondHeader.h': {('fourthHeader.h', 2, 11, 36)},
								  'sixthHeader.h': set(),
								  'thirdHeader.h': {('fourthHeader.h', 7, 67, 92),
								                    ('sixthHeader.h', 3, 16, 40)}}])
		# Check includeMap.pdf is generated
		self.assertTrue("includeMap.pdf" in os.listdir())

		# Finding include map for example2.c
		if "includeMap.pdf" in os.listdir(): os.remove("includeMap.pdf")

		sys.argv = ["main.py", "./testFiles/", "-m", "example2.c"]
		self.assertEqual(main(), [{'example2.c': {('secondHeader.h', 2, 2, 36),
                 								  ('seventhHeader.h', 3, 37, 68),
                 								  ('sixthHeader.h', 4, 69, 98)},
  								   'fifthHeader.h': set(),
  								   'fourthHeader.h': {('fifthHeader.h', 4, 4, 28)},
  								   'secondHeader.h': {('fourthHeader.h', 2, 11, 36)},
  								   'seventhHeader.h': {('thirdHeader.h', 4, 4, 28)},
  								   'sixthHeader.h': set(),
  								   'thirdHeader.h': {('fourthHeader.h', 7, 67, 92),
                   									 ('sixthHeader.h', 3, 16, 40)}}])
		# Check includeMap.pdf is generated
		self.assertTrue("includeMap.pdf" in os.listdir())

		# Finding include map for example.c and example2.c as specified in input_two_files.txt
		if "includeMap.pdf" in os.listdir(): os.remove("includeMap.pdf")

		sys.argv = ["main.py", "./testFiles/", "-f", "./testFiles/input_two_files.txt"]
		self.assertEqual(main(), [{'example2.c': {('secondHeader.h', 2, 2, 36),
								                  ('seventhHeader.h', 3, 37, 68),
								                  ('sixthHeader.h', 4, 69, 98)},
								   'fifthHeader.h': set(),
								   'fourthHeader.h': {('fifthHeader.h', 4, 4, 28)},
								   'secondHeader.h': {('fourthHeader.h', 2, 11, 36)},
								   'seventhHeader.h': {('thirdHeader.h', 4, 4, 28)},
								   'sixthHeader.h': set(),
								   'thirdHeader.h': {('fourthHeader.h', 7, 67, 92),
								                     ('sixthHeader.h', 3, 16, 40)}},
								  {'example.c': {('firstHeader.h', 2, 2, 30),
                    							 ('secondHeader.h', 3, 31, 65),
                    							 ('thirdHeader.h', 4, 66, 95)},
							       'fifthHeader.h': set(),
							       'firstHeader.h': {('secondHeader.h', 3, 17, 42)},
							       'fourthHeader.h': {('fifthHeader.h', 4, 4, 28)},
							       'secondHeader.h': {('fourthHeader.h', 2, 11, 36)},
							       'sixthHeader.h': set(),
							       'thirdHeader.h': {('fourthHeader.h', 7, 67, 92),
							                         ('sixthHeader.h', 3, 16, 40)}}])

		# Check includeMap.pdf is generated
		self.assertTrue("includeMap.pdf" in os.listdir())


		# Unrecognised command-line argument
		with self.assertRaises(Exception) as ex1:
			sys.argv = ["main.py", "./testFiles/", "-x", "example.c"]
			main()
		self.assertEqual("Command line argument \"-x\" not recognised", str(ex1.exception))

		# Specified extention is not .c or .h
		with self.assertRaises(Exception) as ex2:
			sys.argv = ["main.py", "./testFiles/", "-m", "example.x"]
			main()
		self.assertEqual("Attempting to analyse file with unrecognised extension: example.x", str(ex2.exception))

		# Insufficient number of command line arguments
		with self.assertRaises(Exception) as ex3:
			sys.argv = []
			main()
		self.assertEqual("Insufficient number of command-line arguments provided", str(ex3.exception))

		# Insufficient number of command line arguments
		with self.assertRaises(Exception) as ex4:
			sys.argv = ["Arg1"]
			main()
		self.assertEqual("Insufficient number of command-line arguments provided", str(ex4.exception))

		# Insufficient number of command line arguments
		with self.assertRaises(Exception) as ex5:
			sys.argv = ["Arg1", "Arg2"]
			main()
		self.assertEqual("Insufficient number of command-line arguments provided", str(ex5.exception))

		# Insufficient number of command line arguments
		with self.assertRaises(Exception) as ex6:
			sys.argv = ["Arg1", "Arg2", "Arg3"]
			main()
		self.assertEqual("Insufficient number of command-line arguments provided", str(ex6.exception))











	def test_getAbsolutePaths(self):

		""" getAbsolutePaths() """

		# Finding the absolute path for a valid relative path (/ given at end of subdir)
		self.assertEqual(getAbsolutePaths("./testFiles/"), {"base"    : "{}/testFiles/".format(os.getcwd()),
			          										"source"  : "{}/testFiles/source".format(os.getcwd()),
			          										"includes": "{}/testFiles/includes".format(os.getcwd())})

		# Finding the absolute path for a valid relative path (/ not given at end of subdir)
		self.assertEqual(getAbsolutePaths("./testFiles"),  {"base"    : "{}/testFiles".format(os.getcwd()),
			          										"source"  : "{}/testFiles/source".format(os.getcwd()),
			          										"includes": "{}/testFiles/includes".format(os.getcwd())})

		# Specified directory requires movement up a directory
		d = os.getcwd()
		os.chdir("./images/")
		self.assertEqual(getAbsolutePaths("../testFiles"),  {"base"    : "{}/images/../testFiles".format(d),
					          								 "source"  : "{}/images/../testFiles/source".format(d),
					          								 "includes": "{}/images/../testFiles/includes".format(d)})
		os.chdir("..")

		# Specified directory is current working directory (.)
		os.chdir("./testFiles")
		self.assertEqual(getAbsolutePaths("."),             {"base"    : "{}".format(os.getcwd()),
					          								 "source"  : "{}/source".format(os.getcwd()),
					          								 "includes": "{}/includes".format(os.getcwd())})

		# Specified directory is current working directory (./)
		self.assertEqual(getAbsolutePaths("./"),            {"base"    : "{}/".format(os.getcwd()),
					          								 "source"  : "{}/source".format(os.getcwd()),
					          								 "includes": "{}/includes".format(os.getcwd())})

		os.chdir("..")

		# Specified relative path does not begin with '.'
		with self.assertRaises(Exception) as ex1:
			getAbsolutePaths("/nonExistent")
		self.assertEqual("/nonExistent is not a valid relative path, as it does not begin with \'.\'", str(ex1.exception))

		# Specified directory does not exist
		with self.assertRaises(Exception) as ex2:
			getAbsolutePaths("./nonExistent")
		self.assertEqual("{}/nonExistent/ is not a valid directory".format(os.getcwd()), str(ex2.exception))

		# Sepcified directory does not have a 'source' subdirectory
		with self.assertRaises(Exception) as ex3:
			getAbsolutePaths("./images")
		self.assertEqual("{}/images/source is not a valid directory".format(os.getcwd()), str(ex3.exception))

		# Specified directory does not have an 'includes' subdirectory
		os.mkdir('tempDir')
		os.mkdir('tempDir/source/')

		with self.assertRaises(Exception) as ex4:
			getAbsolutePaths("./tempDir")
		self.assertEqual("{}/tempDir/includes is not a valid directory".format(os.getcwd()), str(ex4.exception))

		os.rmdir('tempDir/source')
		os.rmdir('tempDir/')




if __name__ == "__main__":
	unittest.main()