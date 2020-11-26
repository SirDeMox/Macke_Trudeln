from play_game import PlayGame
import pandas as pd

from play_game import PlayGame


class RunSession():
    def __init__(self, method, threshold):
        self.method = method
        self.threshold = threshold
        self.final_score = 0
        self.macke_count = 0
        self.game_number = 0
        self.current_game = None
        self.missed_points = 0

    def play_until_5k(self):
        while self.final_score <= 5000:
            self.current_game = PlayGame(method=self.method, threshold=self.threshold)
            self.current_game.run()
            self.final_score += self.current_game.total_score
            self.game_number += 1
            if self.current_game.stopping_reason == "Macke":
                self.macke_count += 1
                self.missed_points += self.current_game.score_before_end

    def create_output_dict(self):
        return {
            "method": self.method,
            "threshold": self.threshold,
            "final_score": self.final_score,
            "games_n": self.game_number,
            "macke_count": self.macke_count,
            "missed_points": self.missed_points,
        }