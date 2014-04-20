from board import Board, IllegalMoveException
from moves import ALL_MOVES
from strategies.base_board_score_strategy import BaseBoardScoreStrategy

average = lambda values: sum(values) / len(values)


class AdvancedBoardScoreStrategy(BaseBoardScoreStrategy):
    """
    This strategy is similar to the simple one, but tries to "peek into the future".
    It tries various options that different moves lead to, and chooses a move according to
    agg_func - a score aggregation function.
    """

    def calc_max_depth(self, board):
        num_free_tiles_left = board.get_num_free_tiles()

        if num_free_tiles_left < 3:
            max_depth = 4
        elif num_free_tiles_left < 8:
            max_depth = 3
        else:
            max_depth = 2

        return max_depth

    def calc_score_for_board(self, board, agg_func=average, iteration=1, max_depth=None):
        if max_depth is None:
            max_depth = self.calc_max_depth(board)

        if iteration == max_depth:
            return self._board_score_heuristic.get_board_score(board)

        scores = []

        for tile in board.get_free_tiles():
            cur_board = Board(board)
            cur_board[tile] = 2

            legal_move_found = False

            for move in ALL_MOVES:
                move_board = Board(cur_board)

                try:
                    move_board.move_only_swipe(move)
                except IllegalMoveException:
                    # Only counting possible moves
                    continue

                legal_move_found = True

                scores.append(
                    self.calc_score_for_board(
                        move_board,
                        agg_func=agg_func,
                        iteration=iteration + 1,
                        max_depth=max_depth
                    )
                )

            if not legal_move_found:
                scores.append(-1)

        if scores:
            return agg_func(scores)
        return -1

    def calc_score_for_move(self, board, move):
        cur_board = Board(board)
        cur_board.move_only_swipe(move)
        return self.calc_score_for_board(
            cur_board
        )