from board import Board, IllegalMoveException, ALL_TILES
from config import WIN_VALUE
from strategies.advanced_board_score_strategy import AdvancedBoardScoreStrategy
from strategies.board_score_heuristics.ace_scorer import AceScorer


class Bot(object):
    def __init__(self, strategy):
        self._strategy = strategy

    def play(self, board, show_steps=True):
        """
        runs the algorithm on given board and attempts to solve it.
        returns True if successfully solved and False if failed.
        """
        while board.has_legal_moves() and not board.has_tile(WIN_VALUE):
            if show_steps:
                print repr(board)

            next_move = self._strategy.get_next_move(board)

            if show_steps:
                print "Chosen move:", next_move

            board.move(next_move)

        if show_steps:
            print repr(board)

        return board.has_tile(WIN_VALUE)


if __name__ == "__main__":
    board = Board()
    success = Bot(
        AdvancedBoardScoreStrategy(
            AceScorer()
        )
    ).play(board, show_steps=True)

    print "Success!" if success else "Failure!", "({})".format(board.get_max_tile())
