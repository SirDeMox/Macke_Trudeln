import unittest
import random as rd
from run_session import RunSession

class MyTestCase(unittest.TestCase):
    def test_session_setup(self):
        session = RunSession()
        message = "{} should be 0"
        self.assertEqual(session.final_score, 0, message.format("final_score"))
        self.assertEqual(session.macke_count, 0, message.format("macke_count"))
        self.assertEqual(session.game_number, 0, message.format("game_number"))
        self.assertEqual(session.missed_points, 0, message.format("missed_points"))

    def test_parsing(self):
        session = RunSession(method="earlystop", threshold=300, special=["run4s"])
        self.assertEqual(session.method, "earlystop")
        self.assertEqual(session.threshold, 300)
        self.assertTrue("run4s" in session.special)

    def test_curve(self):
        session = RunSession()

        self.assertTrue(len(session.curve)==21)

        actual = max(session.curve.values())
        expected = 5000
        message = "Maximum value of the curve must be 5000, not {}".format(actual)
        self.assertTrue(actual == expected, message)

        actual = min(session.curve.values())
        expected = 0
        message = "The curve has to start at {}, not {}".format(expected, actual)
        self.assertTrue(actual == expected, message)

    def test_curve_gains(self):
        session = RunSession()
        gains = [session.curve[roll+1] - session.curve[roll] \
                             for roll in session.curve \
                             if roll+1 <= len(session.curve)-1]
        message = "All gains on the curve must be positive, {negative_gain} is not".\
            format(negative_gain = [gain for gain in gains if gain<0])
        self.assertTrue(all([gain >= 0 for gain in gains]), message)



    def test_play_until_5k(self):
        rd.seed(42)
        session = RunSession(method="earlystop", threshold=300, special=["run4s"])
        session.play_until_5k()
        self.assertTrue(session.final_score >= 5000)
        self.assertTrue(session.game_number == 14)
        self.assertTrue(session.macke_count == 4)
        self.assertTrue(session.missed_points == 650)

    def test_create_output_dict(self):
        rd.seed(42)
        session = RunSession(method="earlystop", threshold=300, special=["run4s"])
        session.play_until_5k()
        actual = session.create_output_dict()
        expected = {
            'method': 'earlystop',
            'threshold': 300,
            'special': ["run4s"],
            'final_score': 5500,
            'games_n': 14,
            'macke_count': 4,
            'missed_points': 650,
        }

        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
