import unittest

from create_summary_data import CreateSummaryData


class MyTestCase(unittest.TestCase):
    def test_single_threshold_parsing(self):
        expected_threshold = 300
        expected_threshold_range = [300]
        actual = CreateSummaryData(threshold=300)
        self.assertEqual(actual.threshold, expected_threshold)
        self.assertEqual(actual.threshold_range, expected_threshold_range)
        # TODO add expected, actual pattern to other tests

    def test_multiple_threshold_parsing(self):
        a_summary = CreateSummaryData(threshold="multiple")
        self.assertEqual(a_summary.threshold, "multiple")
        self.assertEqual(a_summary.threshold_range, range(100, 1050, 50))

    def test_run_on_10_sessions(self):
        _n = 2
        a_summary = CreateSummaryData(n=_n, threshold=300)
        a_summary_df = a_summary.run()
        threshold_count = len(a_summary.threshold_range)
        self.assertEqual(threshold_count, 1)
        self.assertEqual(len(a_summary_df), _n)

    def test_multiple_thresholds_run_on_2_sessions(self):
        _n = 2
        a_summary = CreateSummaryData(n=_n, threshold="multiple")
        a_summary_df = a_summary.run()
        threshold_count = len(a_summary.threshold_range)
        self.assertEqual(threshold_count, 19)
        self.assertEqual(len(a_summary_df), _n * threshold_count)


if __name__ == '__main__':
    unittest.main()
