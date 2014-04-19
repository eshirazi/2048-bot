import random
import itertools
from board import Board, IllegalMoveException, ALL_TILES
from config import WIN_VALUE
import helpers
from moves import ALL_MOVES

avg = lambda values: sum(values) / len(values)

class Bot(object):
    def get_board_score(self, board):
        """
        This is a heuristic trying to give a score to a given board state.
        Higher scores are given to "better" board constellations.

        This is the heart of the algorithm, and is still the main part that needs
        to be improved.
        """

        # The basic score is calculated as the sum of the squares of the tile values on the board.
        # The idea behind this odd calculation is to give more score to constellations where
        # the most high values appear. This will for example prefer merging two 128 tiles, instead of merging
        # two 64 tiles.

        score = float(
            sum(
                (board[y, x] ** 2 for y, x in ALL_TILES),
                0
            )
        )

        # We also want to give the algorithm a sense of survival. Therefore we
        # significantly deduct score for "tight" constellations where there's not much room left
        # on the board. This helps the algorithm try to avoid staying in tight situations for a long time.

        num_free_tiles = board.get_free_tiles()

        if num_free_tiles < 4:
            score /= 2
        if num_free_tiles < 2:
            score /= 2
        if num_free_tiles < 1:
            score /= 2

        return score


    def get_next_move_simple(self, board):
        """
        This strategy simply tries the four possible moves, checks the
        score of the resulting board constellations, and picks the best out of the four.
        """

        def calc_score_for_move(move):
            board_copy = Board(board)
            try:
                board_copy.move_only_swipe(move)
                return self.get_board_score(board_copy)
            except IllegalMoveException:
                return -1.0

        return max(ALL_MOVES, key=calc_score_for_move)

    def get_next_move_advanced(self, board, agg_func=avg):
        """
        This strategy is similar to the simple one, but tries to "peek into the future".
        It tries various options that different moves lead to, and chooses a move according to
        agg_func - a score aggregation function.
        """
        def calc_score_for_board(board, iteration=1):
            if iteration == max_depth:
                return self.get_board_score(board)

            scores = []

            for tile in board.get_free_tiles():
                cur_board = Board(board)
                cur_board[tile] = 2

                if not cur_board.has_legal_moves():
                    # Things are bad if there aren't possible moves at all
                    scores += [-1]
                else:
                    for move in ALL_MOVES:
                        move_board = Board(cur_board)

                        try:
                            move_board.move_only_swipe(move)
                        except IllegalMoveException:
                            # Only counting possible moves
                            continue

                        scores.append(calc_score_for_board(move_board, iteration=iteration+1))

            if scores:
                return agg_func(scores)
            return -1

        def calc_score_for_move(move):
            cur_board = Board(board)
            try:
                cur_board.move_only_swipe(move)
                return calc_score_for_board(cur_board)
            except IllegalMoveException:
                return -10.0

        num_free_tiles_left = board.get_num_free_tiles() - 1

        if num_free_tiles_left == 0:
            max_depth = 5
        elif num_free_tiles_left < 2:
            max_depth = 4
        elif num_free_tiles_left < 7:
            max_depth = 3
        else:
            max_depth = 2

        return max(ALL_MOVES, key=calc_score_for_move)

    get_next_move = get_next_move_advanced

    def play(self, board, show_steps=True):
        """
        runs the algorithm on given board and attempts to solve it.
        returns True if successfully solved and False if failed.
        """
        while board.has_legal_moves() and not board.has_tile(WIN_VALUE):
            if show_steps:
                print repr(board)

            next_move = self.get_next_move(board)

            if show_steps:
                print "Chosen move:", next_move

            board.move(next_move)

        if show_steps:
            print repr(board)

        return board.has_tile(WIN_VALUE)


if __name__ == "__main__":
    board = Board()
    success = Bot().play(board, show_steps=True)

    print "Success!" if success else "Failure!", "({})".format(board.get_max_tile())
