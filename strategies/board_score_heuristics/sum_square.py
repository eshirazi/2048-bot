from board import ALL_TILES


def sum_square_heuristic(board):
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

    return score
