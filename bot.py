import time
from board import Board, IllegalMoveException, ALL_TILES
from config import WIN_VALUE
from strategies.advanced_board_score_strategy import AdvancedBoardScoreStrategy
from strategies.board_score_heuristics.best import ace_heuristic
from strategies.board_score_heuristics.side_sticky import side_sticky_heuristic
from strategies.board_score_heuristics.sum_square import sum_square_heuristic


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
    start_time = time.time()

    success = Bot(
        AdvancedBoardScoreStrategy(
            ace_heuristic,
            depth_modifier=1
        )
    ).play(board, show_steps=True)

    duration = int(time.time() - start_time)

    print "Time %02d:%02d:%02d" % (duration / 60 / 60, (duration / 60) % 60, duration % 60)
    print "Success!" if success else "Failure!", "({})".format(board.get_max_tile())
