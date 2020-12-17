from dice_rolls import DiceRolls


class PlayGame():
    def __init__(self,
                 method="earlystop",
                 threshold=300,
                 special=[], ):
        """
        This class plays a game of Macke.

        :param method: either "earlystop" or "nrolls"
        :param threshold: a integer which goes with the method
        :param special: a list containing special options as strings
        """

        self.rolls = 0
        self.resets = 0
        self.total_score = 0
        self.score_before_end = 0
        self.macke = None
        self.continued = True
        self.dice_remaining = 5
        self.method = method
        self.threshold = threshold
        self.current_roll = None
        self.stopping_reason = None
        self.curve_state = None
        if "run4s" in special:
            self.run4s = True
        else:
            self.run4s = None

    def check_for_macke(self):
        """
        this method checks for macke and adjusts the gamestate accordingly.

        if DiceRolls.evaluate_macke() evaluated a macke in the current role,
        this method will :
        - set continued to false,
        - saves all lost points to score_before_end
        - sets totalscore to 0
        - sets stopping_reason to "Macke"

        :return: None
        """
        if self.current_roll.macke is True:
            self.continued = False
            self.score_before_end = self.total_score
            self.total_score = 0
            self.stopping_reason = "Macke"

    def account_for_new_score(self):
        """
        this method adds rolled scores to totals.

        - adds 1 to the number of rolls
        then, if the game shall continue:
        - adds the rolled score to the total_score
        - sets the new number of dice_remaining
        - if no dice_remaining, it will set it to 5 and adds 1 to resets

        :return: None
        """
        self.rolls += 1
        if self.continued is True:
            self.total_score += self.current_roll.score
            self.dice_remaining = self.current_roll.dice_remaining

            if self.dice_remaining == 0:
                self.resets += 1
                self.dice_remaining = 5

    def method_interpreter(self):
        """
        this method evaluates a gamestate based on the chosen method and specials

        if the special "run4s" is given, it will add 4 to the dont_stop_at

        "earlystop": stops the rolling once self.threshold is surpassed by the self.total_score
        "nrolls": stops ones you rolled n (threshold) times

        :return: None
        """

        dont_stop_at = [5]

        if self.run4s:
            dont_stop_at.append(4)

        if self.method == "earlystop":
            if self.total_score >= self.threshold \
                    and (not self.dice_remaining in dont_stop_at):
                self.continued = False
                self.stopping_reason = "Earlystop"

        if self.method == "nrolls":
            if self.rolls >= self.threshold \
                    and (not self.dice_remaining in dont_stop_at):
                self.continued = False
                self.stopping_reason = "Nrolls"

        # todo compare against curve

    def run(self):
        """
        this method rolls dice and keeps checking and scoring them
        until ending condition is met by check_for_macke or method_interpreter
        """
        while self.continued is True:
            self.current_roll = DiceRolls(self.dice_remaining).run()
            self.check_for_macke()
            self.account_for_new_score()
            self.method_interpreter()
