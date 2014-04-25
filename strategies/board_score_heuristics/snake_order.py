import itertools
from board import Board, ALL_TILES
from config import BOARD_SIZE
from helpers import chop_generator, tuplify


def is_in_board(pos):
    return (0 <= pos[0] < BOARD_SIZE) and (0 <= pos[1] < BOARD_SIZE)

def vec_add(pos, vec):
    return (
        pos[0] + vec[0],
        pos[1] + vec[1],
    )

def vec_rotate(vec, rotate_orientation):
    return (
        vec[1] * rotate_orientation,
        -vec[0] * rotate_orientation,
    )


@tuplify
@chop_generator(16)
def snake_path(origin, start_direction, rotate_orientation):
    pos = origin
    d = start_direction
    rot = rotate_orientation

    while True:
        yield pos

        if not is_in_board(vec_add(pos, d)):
            d = vec_rotate(d, rot)
            pos = vec_add(pos, d)
            d = vec_rotate(d, rot)

            rot *= -1
        else:
            pos = vec_add(pos, d)

_S = BOARD_SIZE - 1

ALL_SNAKES = \
    [
        snake_path(snake_origin, start_direction, rotate_orientation)
        for snake_origin, start_direction, rotate_orientation in (
            (( 0,  0), ( 1,  0), -1),
            (( 0,  0), ( 0,  1),  1),
            (( 0, _S), ( 1,  0),  1),
            (( 0, _S), ( 0, -1), -1),
            ((_S, _S), (-1,  0), -1),
            ((_S, _S), ( 0, -1),  1),
            ((_S,  0), (-1,  0),  1),
            ((_S,  0), ( 0,  1), -1),
        )
    ]

def snake_board(board, snake):
    return (board[tile] for tile in snake)

def longest_snake_match_length(board):
    sorted_board = sorted((board[y, x] for y, x in ALL_TILES), reverse=True)

    def snake_match_length(board, snake):
        l = 0

        for a, b in itertools.izip(sorted_board, snake_board(board, snake)):
            if a != b:
                break
            l += 1
        return l

    return max(snake_match_length(board, snake) for snake in ALL_SNAKES)

def snake_order_heuristic(board):
    sorted_board = sorted((board[y, x] for y, x in ALL_TILES), reverse=True)

    return sum(sorted_board[:longest_snake_match_length(board)], 0)

DECAY = 0.75
def snake_decay_order_heuristic(board):
    def decay_score(board, snake):
        mult = 1.0
        ret = 0

        for value in snake_board(board, snake):
            mult *= DECAY
            ret += value * mult

        return ret

    return max(decay_score(board, snake) for snake in ALL_SNAKES)


if __name__ == "__main__":
    assert(longest_snake_match_length(Board(
        [
            [0,     1,      2,      3],
            [4,     5,      6,      7],
            [8,     9,      10,     11],
            [12,    13,     14,     15],
        ]
    )) == 4)

    assert(longest_snake_match_length(Board(
        [
            [3,     2,      1,      0],
            [4,     5,      6,      7],
            [11,    10,     9,      8],
            [12,    13,     14,     15],
        ]
    )) == 16)

    assert(longest_snake_match_length(Board(
        [
            [3,     2,      1,      0],
            [4,     5,      6,      7],
            [11,    10,     9,      8],
            [12,    13,     14,     13],
        ]
    )) == 0)