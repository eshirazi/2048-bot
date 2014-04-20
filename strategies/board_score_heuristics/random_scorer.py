import random
from strategies.board_score_heuristics.base_board_score_heuristic import BaseBoardScoreHeuristic


class RandomScorer(BaseBoardScoreHeuristic):
    def get_board_score(self, board):
        return random.random()