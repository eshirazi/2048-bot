from board import Board
from strategies.base_board_score_strategy import BaseBoardScoreStrategy


class SimpleBoardScoreStrategy(BaseBoardScoreStrategy):
    """
    This strategy simply tries the four possible moves, checks the
    score of the resulting board constellations, and picks the best out of the four.
    """
    def calc_score_for_move(self, board, move):
        board_copy = Board(board)
        board_copy.move_only_swipe(move)
        return self._board_score_heuristic.get_board_score(board_copy)