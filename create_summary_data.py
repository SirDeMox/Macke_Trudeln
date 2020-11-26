from run_session import RunSession
import pandas as pd

class CreateSummaryData():
    def __init__(self, n=100, method=None, threshold=None):
        self.n = n
        self.method = method
        self.threshold = threshold

    def output_results_df_single_threshold(self):
        results_list = []
        for i in range(self.n):
            a_session = RunSession(method=self.method, threshold=self.threshold)
            a_session.play_until_5k()
            results_list.append(a_session.create_output_dict())

        return pd.DataFrame(results_list)

    def output_results_df_range_threshold(self):
        results_list = []
        if self.threshold == "multiple":
            for threshold in range(100, 1050, 50):
                for i in range(self.n):
                    a_session = RunSession(method=self.method, threshold=threshold)
                    a_session.play_until_5k()
                    results_list.append(a_session.create_output_dict())

        return pd.DataFrame(results_list)