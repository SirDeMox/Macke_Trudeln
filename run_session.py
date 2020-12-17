from play_game import PlayGame
import pandas as pd

from play_game import PlayGame


class RunSession():
    def __init__(self,
                 method="earlystop",
                 threshold=300,
                 special=[],):
        """
        This class runs games until it reaches 5k total_score
            and returns a summary of all games played

        :param method: either "earlystop" or "nrolls"
        :param threshold: a integer which goes with the method
        :param special: a list containing special options as strings
        """
        self.method = method
        self.threshold = threshold
        self.final_score = 0
        self.macke_counter = 0
        self.game_counter = 0
        self.current_game = None
        self.missed_points = 0
        self.threshold_curved = None
        self.special = special
        self.curve = {0: 0,
             1: 250,
             2: 500,
             3: 750,
             4: 1000,
             5: 1250,
             6: 1500,
             7: 1750,
             8: 2000,
             9: 2250,
             10: 2500,
             11: 2750,
             12: 3000,
             13: 3250,
             14: 3500,
             15: 3750,
             16: 4000,
             17: 4250,
             18: 4500,
             19: 4750,
             20: 5000,}

    def curve_state_interpreter(self):
        # calc diff curve versus total
        # if diff  > X:
        #   raise/lower threshold
        # if diff < Y:
        #   raise/lower threshold
        if self.curve_state == "behind":
            self.threshold_curved = 500

        if self.curve_state == "ahead":
            self.threshold_curved = 250


    def play_until_5k(self):
        """
        this method runs PlayGame and scores the games until it reached 5k points.

        it runs a game, scores the points in final_score and ++ the game_counter counter
        if the game ended in a Macke, it will ++ the macke_counter

        :return: None
        """
        while self.final_score < 5000:
            #todo curve interpreter here!?
            #self.curve_state_interpreter()
            #replace threshold below

            self.current_game = PlayGame(
                method=self.method,
                threshold=self.threshold,
                special=self.special,
            )

            self.current_game.run()
            self.final_score += self.current_game.total_score
            self.game_counter += 1

            if self.current_game.stopping_reason == "Macke":
                self.macke_counter += 1
                self.missed_points += self.current_game.score_before_end

    def create_output_dict(self):
        return {
            "method": self.method,
            "threshold": self.threshold,
            "special": self.special,
            "final_score": self.final_score,
            "games_n": self.game_counter,
            "macke_counter": self.macke_counter,
            "missed_points": self.missed_points,
        }