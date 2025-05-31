
import unittest
import sys

from navigation_tests import NavigationTests
from tender_tests import TenderTests
from offer_tests import OfferTests

def run_all_tests():
    
    test_suite = unittest.TestSuite()
    
    test_suite.addTest(unittest.makeSuite(NavigationTests))
    test_suite.addTest(unittest.makeSuite(TenderTests))
    test_suite.addTest(unittest.makeSuite(OfferTests))
    
    runner = unittest.TextTestRunner(verbosity=2)
    
    result = runner.run(test_suite)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(run_all_tests())