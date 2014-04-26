from board import ALL_TILES
from config import BOARD_SIZE
from helpers import irange


def side_sticky_heuristic(board):
    # Prefer having a dominant side
    #

    board_sum = sum(board[y, x] for y, x in ALL_TILES)

    max_side_sum = max(
        sum(board[i, 0] for i in irange(BOARD_SIZE)),
        sum(board[i, BOARD_SIZE - 1] for i in irange(BOARD_SIZE)),
        sum(board[0, i] for i in irange(BOARD_SIZE)),
        sum(board[BOARD_SIZE - 1, i] for i in irange(BOARD_SIZE))
    )

    if (board_sum - max_side_sum) == 0 or max_side_sum / (board_sum - max_side_sum) >= 3.0:
        return max_side_sum

    return 0


def side_smooth_sticky_heuristic(board):
    # Prefer having a dominant side, and numbers are arranged from higher to lower
    #

    board_sum = sum(board[y, x] for y, x in ALL_TILES)
    sorted_board = sorted([board[y, x] for y, x in ALL_TILES], reverse=True)
    rel_point = board.get_max_tile() * .9


    def score_for_edge(edge_values):
        score = 0

        edge_max = max(edge_values)
        edge_sum = sum(edge_values)
        rest_sum = board_sum - edge_sum

        if rest_sum > 0:
            ratio = edge_sum / rest_sum
        else:
            ratio = 100

        if ratio >= 4:
            score += rel_point
        elif ratio >= 3:
            score += rel_point / 2
        elif ratio >= 2:
            score += rel_point / 4
        elif ratio >= 1:
            score += rel_point / 8

        if edge_values[0] == sorted_board[0]:
            score *= 1.5

            if edge_values[1] == sorted_board[1]:
                score *= 1.4

                if edge_values[2] == sorted_board[2]:
                    score *= 1.2

        elif edge_values[3] == sorted_board[0]:
            score *= 1.5

            if edge_values[2] == sorted_board[1]:
                score *= 1.4

                if edge_values[1] == sorted_board[2]:
                    score *= 1.2

        return score

    edges = (
        [board[i, 0] for i in irange(BOARD_SIZE)],
        [board[i, BOARD_SIZE - 1] for i in irange(BOARD_SIZE)],
        [board[0, i] for i in irange(BOARD_SIZE)],
        [board[BOARD_SIZE - 1, i] for i in irange(BOARD_SIZE)]
    )

    return max(score_for_edge(edge) for edge in edges)
