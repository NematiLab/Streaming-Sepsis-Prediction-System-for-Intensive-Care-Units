import random

class FakeSepsisScorer:

    def __init__(self):
        pass

    def initialize(self):
        pass

    def get_sepsis_score_python(self, *args):
        if len(args) >= 1:
            prior_score = args[0]
            r = random.random()
            if r < 0.34:
                change = -0.05
            elif r < 0.67:
                change = 0
            else:
                change = 0.05
            return prior_score + change
        else:
            return random.random()