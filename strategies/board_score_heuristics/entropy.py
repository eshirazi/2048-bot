import math
from config import BOARD_SIZE
from helpers import irange


def get_entropy_heuristic(board):
    positives = 0.0
    negatives = 0.0

    for orientation in ["x", "y"]:
        get = lambda y, x: board[(y, x) if orientation == "x" else (x, y)]

        for i in irange(BOARD_SIZE):
            last_stumbled = None
            direction = None

            for j in irange(BOARD_SIZE):
                cur = get(i, j)

                if cur != 0:
                    if last_stumbled is not None:
                        log_cur = math.log(cur, 2)

                        if last_stumbled < cur:
                            if direction == 1:
                                positives += log_cur
                            elif direction == -1:
                                negatives += log_cur
                            direction = 1

                        elif last_stumbled > cur:
                            if direction == -1:
                                positives += log_cur
                            elif direction == 1:
                                negatives += log_cur
                            direction = -1

                    last_stumbled = cur

    return (positives - negatives) * 100