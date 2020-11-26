import random as rd


class DiceRolls():
    def __init__(self,
                 number_dice=None,
                 fixed_rolls=None,
                 _previous_score=None):

        self.roll_results = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
        }
        self.wanted_rolls = fixed_rolls
        self.toak = None
        self.macke = None
        if self.wanted_rolls:
            self.count_rolled_dice = sum(self.wanted_rolls)
        else:
            self.count_rolled_dice = number_dice
        self.dice_remaining = None
        self.score = None
        self.previous_score = _previous_score

    def roll_dice(self):
        """
        rolls n dice
        """
        for i in range(self.count_rolled_dice):
            self.roll_results[rd.randint(1, 6)] += 1

    def set_fixed_rolls(self):
        """
        takes a list of 6 numbers and inputs them into the roll_results
        """

        self.roll_results = {
            1: self.wanted_rolls[0],
            2: self.wanted_rolls[1],
            3: self.wanted_rolls[2],
            4: self.wanted_rolls[3],
            5: self.wanted_rolls[4],
            6: self.wanted_rolls[5],
        }

    def evaluate_macke(self):
        """
        evaluates if the dice don't score any points
        """

        has_1 = self.roll_results[1] >= 1
        has_5 = self.roll_results[5] >= 1
        has_toak = any([x >= 3 for x in self.roll_results.values()])

        conditions = [has_1, has_5, has_toak]
        self.macke = not (any(conditions))

    def roll_results_toak_cleanup(self):
        """
        checks if there is a toak
        notes the kind of toak
        cleans up the rolldict accordingly
        """

        for roll in self.roll_results:
            if self.roll_results[roll] >= 3:
                self.toak = roll  # kind of toak
                self.roll_results[roll] -= 3  # correcting dice counts

    def count_dice_remaining(self):
        """
        counts the number of dice remaining
        """

        self.dice_remaining = sum([self.roll_results[x] for x in [2, 3, 4, 6]])

    def evaluate_points(self):
        """
            This function evaluates a dice roll:
            counts 50 points for a 5
            counts 100 points for a 1
            counts 100*pips for a three-of-a-kind
            counts 1000 for three 1s
            returns number of dice rolled
            returns points (score)
            returns if there was no score (macke)
            returns number of used dice in scoring
            returns number of remaining dice (non-scoring dice)
        """

        points_1s = self.roll_results[1] * 100
        points_5s = self.roll_results[5] * 50
        points_toaks = 0

        if self.toak:
            if self.toak == 1:
                points_toaks = 1000
            if self.toak in range(2, 6):
                points_toaks = self.toak * 100

        self.score = points_1s + points_5s + points_toaks

    def run(self):

        if self.wanted_rolls:
            self.set_fixed_rolls()
        else:
            self.roll_dice()

        self.evaluate_macke()
        self.roll_results_toak_cleanup()
        self.count_dice_remaining()
        self.evaluate_points()

        return self

    def print(self):
        print(
            self.roll_results,
            self.toak,
            self.score,
            self.macke,
            self.dice_remaining
        )

