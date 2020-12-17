import pandas as pd

from run_session import RunSession


class CreateSummaryData():
    def __init__(
            self,
            n=10,
            method="earlystop",
            threshold=300,
            special=[]
    ):
        """
        This class runs n sessions of a certain method and threshold.
        if threshold="multiple" the threshold will be set to range(100,1050,50)
        and return n*19 rows

        :param n: int, number of sessions to play
        :param method: str, method of the sessions to play
        :param threshold: int, or "multiple"
        :param special: a list containing special options as strings
        """

        self.n = n
        self.method = method
        self.threshold = threshold
        self.special = special

        if self.threshold == "multiple":
            self.threshold_range = range(100, 1050, 50)
        else:
            self.threshold_range = [self.threshold]

    def run(self):
        results_list = []

        for a_threshold in self.threshold_range:
            for i in range(self.n):
                a_session = RunSession(
                    method=self.method,
                    threshold=a_threshold,
                    special=self.special, )
                a_session.play_until_5k()
                results_list.append(a_session.create_output_dict())

        return pd.DataFrame(results_list)
