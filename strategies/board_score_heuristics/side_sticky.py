from board import ALL_TILES
from config import BOARD_SIZE
from helpers import irange


def side_sticky_heuristic(board):
    # Prefer having a dominant side
    #

    board_sum = sum(board[y, x] for y, x in ALL_TILES)

    max_side_sum = max(
        sum(board[i, 0] for i in irange(4)),
        sum(board[i, BOARD_SIZE - 1] for i in irange(4)),
        sum(board[0, i] for i in irange(4)),
        sum(board[BOARD_SIZE - 1, i] for i in irange(4))
    )

    if (board_sum - max_side_sum) == 0 or max_side_sum / (board_sum - max_side_sum) >= 3.0:
        return max_side_sum

    return 0
