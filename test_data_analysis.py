import unittest
from data_analysis import analyze_data

class TestAnalyzeData(unittest.TestCase):

    def test_analyze_data(self):
        data = [1, 2, 3, 4, 5]
        result = analyze_data(data)
        self.assertEqual(result, 3.0)

    def test_analyze_data_empty(self):
        result = analyze_data([])
        self.assertIsNone(result)

    def test_analyze_data_none(self):
        result = analyze_data(None)
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()