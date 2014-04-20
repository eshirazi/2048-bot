from moves import ALL_MOVES
from strategies.base_strategy import BaseStrategy


class BaseBoardScoreStrategy(BaseStrategy):
    def __init__(self, board_score_heuristic):
        self._board_score_heuristic = board_score_heuristic

    def get_next_move(self, board):
        return max(
            (move for move in board.get_legal_moves()),
            key=lambda move: self.calc_score_for_move(board, move)
        )

    def calc_score_for_move(self, board, move):
        raise NotImplementedError()