import itertools
import random
from config import BOARD_SIZE
from move import MOVES

ALL_INDICES = list(itertools.product(range(BOARD_SIZE), range(BOARD_SIZE)))

class IllegalMoveException(Exception):
    pass

class Board:
    b = None

    def clear(self):
        self.b = [
            [0 for j in range(BOARD_SIZE)]
            for i in range(BOARD_SIZE)
        ]

    def __init__(self, init_board = None):
        if init_board is None:
            # Create a new empty board
            self.clear()

            # Initialize it with 2, 2 or 2, 4
            initializers = list(random.choice([
                (2, 4),
                (2, 2)
            ]))

            for y, x in random.sample(ALL_INDICES, len(initializers)):
                self[y, x] = initializers.pop()
        else:
            self.b = [
                [
                    init_board[y, x]
                    for x in range(BOARD_SIZE)
                ]
                for y in range(BOARD_SIZE)
            ]

    def __getitem__(self, indices):
        return self.b[indices[0]][indices[1]]

    def __setitem__(self, indices, value):
        self.b[indices[0]][indices[1]] = value

    def __repr__(self):
        cell_size = max(len(str(self[y, x])) for y, x in ALL_INDICES)
        line_size = (cell_size + 1) * BOARD_SIZE
        sap_line = "+".join("-" * (cell_size + 2) for i in range(BOARD_SIZE))

        ret = ""
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                if self[y, x] != 0:
                    ret += " " + (" " * cell_size + str(self[y, x]))[-cell_size:] + " "
                else:
                    ret += " " * (cell_size + 2)

                if x != BOARD_SIZE - 1:
                    ret += "|"

            if y != BOARD_SIZE - 1:

                ret += "\n" + sap_line + "\n"
        return ret + "\n"

    def _move_swipe_internal(self, move):
        move_axis = move.get_move_axis()
        static_axis = move.get_static_axis()
        direction = sum(move.get_dir())

        done_something = False

        adapt = \
            lambda i: \
            i if direction != 1 else (BOARD_SIZE - i - 1)

        conv_i_j = \
            lambda i, j: \
            (
                i if static_axis == "y" else adapt(j),
                adapt(j) if move_axis == "x" else i
            )

        def get(i, j):
            return self[conv_i_j(i, j)]

        def put(i, j, value):
            self[conv_i_j(i, j)] = value

        for i in range(BOARD_SIZE):
            last_stumbled = None
            last_stumbled_idx = None
            first_free_idx = None

            for j in range(BOARD_SIZE):
                cur = get(i, j)

                if cur != 0:
                    if last_stumbled == cur:
                        put(i, j, 0)
                        put(i, last_stumbled_idx, cur * 2)
                        first_free_idx = last_stumbled_idx + 1
                        last_stumbled = None
                        last_stumbled_idx = None
                        done_something = True
                    elif first_free_idx is not None:
                        put(i, j, 0)
                        put(i, first_free_idx, cur)
                        last_stumbled = cur
                        last_stumbled_idx = first_free_idx
                        first_free_idx += 1
                        done_something = True
                    else:
                        last_stumbled_idx = j
                        last_stumbled = cur
                elif first_free_idx is None:
                    first_free_idx = j

        return done_something

    def get_legal_moves(self):
        ret = []
        for move in MOVES:
            if Board(self)._move_swipe_internal(move):
                ret.append(move)
        return ret

    def move_swipe(self, move):
        if not self._move_swipe_internal(move):
            raise IllegalMoveException()

    def add_random_tile(self):
        try:
            self[random.choice([
                (y, x)
                for (y, x) in ALL_INDICES
                if self[y, x] == 0
            ])] = 2
        except IndexError:
            raise IllegalMoveException()

    def move(self, move):
        self.move_swipe(move)
        self.add_random_tile()
