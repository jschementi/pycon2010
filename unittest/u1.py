import sys
sys.path.append("Lib")

import unittest
import test_sequence_functions

suite = unittest.TestLoader().loadTestsFromTestCase(test_sequence_functions.TestSequenceFunctions)
unittest.TextTestRunner(verbosity=2).run(suite)
#unittest.main(test_sequence_functions)

