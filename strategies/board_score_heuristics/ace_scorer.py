from board import ALL_TILES
from strategies.board_score_heuristics.base_board_score_heuristic import BaseBoardScoreHeuristic


class AceScorer(BaseBoardScoreHeuristic):
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
