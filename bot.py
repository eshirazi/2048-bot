import time
from board import Board, IllegalMoveException, ALL_TILES
from config import WIN_VALUE, NEVER_STOP
from strategies.advanced_board_score_strategy import ExpectimaxStrategy
from strategies.board_score_heuristics.best import ace_heuristic, supxtra_heuristic, perfect_heuristic


class Bot(object):
    def __init__(self, strategy):
        self._strategy = strategy

    def play(self, board, show_steps=True, stop_at=WIN_VALUE):
        """
        runs the algorithm on given board and attempts to solve it.
        returns True if successfully solved and False if failed.
        """
        while board.has_legal_moves() and not board.has_tile(stop_at):
            if show_steps:
                print repr(board)

            next_move = self._strategy.get_next_move(board)

            if show_steps:
                print "Chosen move:", next_move

            board.move(next_move)

        if show_steps:
            print repr(board)

        return board.get_max_tile() >= WIN_VALUE


if __name__ == "__main__":
    board = Board()
    start_time = time.time()

    success = Bot(
        ExpectimaxStrategy(
            perfect_heuristic,
            depth_modifier=0,
        )
    ).play(board, show_steps=True, stop_at=NEVER_STOP)

    duration = int(time.time() - start_time)

    print "Time %02d:%02d:%02d" % (duration / 60 / 60, (duration / 60) % 60, duration % 60)
    print "Success!" if success else "Failure!", "({})".format(board.get_max_tile())
