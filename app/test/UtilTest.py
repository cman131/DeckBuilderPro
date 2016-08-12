import unittest
from .. import utils

class UtilsTest(unittest.TestCase):

    def testLocationFilter(self):
        testSet = [{'latitude': 24.9932, 'longitude': -23.23422},
                {'latitude': 34.9932, 'longitude': -13.23422},
                {'latitude': -14.9932, 'longitude': 23.23422}]
        results = filterToLocation(testSet, baseCoords, distance)
        print(results)
        self.assertEqual('foo'.upper(), 'FOO')

if __name__ == '__main__':
    unittest.main()
