# Test Vectors for findDirectIncludes function

# Test 1
# ======
# This is a unit test for the function findDirectIncludes
# The test string is a set of #include statements written in different formats
# The test string specifies which statements should be matched, and which should not
testString1 = '''

# MATCH THE FOLLOWING
=====================
#include     <firstHeader.h>
#include     <     secondHeader.h>
#include<thirdHeader.h      >
#include      		  	"fourthHeader.h"
#include "fifthHeader.h"
#include"sixthHeader.h"
Text immediately before#include "seventhHeader.h"Text immediately after
#include "eight_Header.h"
#include "firstHeader.h"

DON'T MATCH THE FOLLOWING
=========================
#include <firstNonValid>
#include <secondNonValid.h
#include thirdNonValid.h>
#include "fourthNonValid"
#include "fifthNonValid.h
#include sixthNonValid.h"

'''

# Test 2
# ======
# This is a unit test for the function findDirectIncludes
# No matched headers should be displayed on the output
# Exception should occur for #include "promptException.c"
testString2 = testString1 + """

#include "promptException.c"

"""

# Test 3
# ======
# This is a unit test for the function findDirectIncludes
# No matched headers should be displayed on the output
# Exception should occur for #include <promptException.H>		
testString3 = testString1 + """

#include <promptException.H>

"""

# Test 4
# ======
# This is a unit test for the function findDirectIncludes
# No matched headers should be displayed on the output
# Exception should occur for #include <promptException.hh>
testString4 = testString1 + """

#include <promptException.hh>

"""

# Test 5
# ======
# This is a unit test for the function findDirectIncludes
# No matched headers should be displayed on the output
# Exception should occur for #include "promptException.hh"
testString5 = testString1 + """

#include "promptException.hh"

"""