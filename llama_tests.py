#!/usr/bin/env python

import unittest

from lib.ll_string import String

class StringTests(unittest.TestCase):

    def testExtractHelloWorld(self):
        sv = String('$:+ -:-+ -|-: .. :| -*-:X -:. *-+X +. -|* |. -+-| .-: -:*X .+')
        result = sv.extract_string()
        self.assertEquals(result, "Hello World!")


class LlamaTests(unittest.TestCase):
    """ Basic unit test class to check the above Fibonacci generator """

    def setUp(self):
        pass

#    def testStopping(self):
#        # Check the generator stopped when it should have
#        self.assertEqual(FIB_STOP, len(self.fibs))
#
#    def testNumbers(self):
#        # Check the generated list against our known correct list
#        for i in range(len(self.correct)):
#            self.assertEqual(self.fibs[i], self.correct[i])

if __name__ == '__main__':
    unittest.main()


