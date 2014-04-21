import math
from board import ALL_TILES, Board
from bot import Bot
from helpers import irange, average
from strategies.advanced_board_score_strategy import AdvancedBoardScoreStrategy
from strategies.board_score_heuristics.best import ace_heuristic
from strategies.board_score_heuristics.side_sticky import side_sticky_heuristic
from strategies.board_score_heuristics.sum_square import sum_square_heuristic


def get_final_board_score(board):
    l = sorted(board[y, x] for y, x in ALL_TILES)

    return l.pop()

def benchmark_strategy(strategy, rounds=25, show_logs=True):
    def dbg_print(text):
        if show_logs:
            print(text)

    dbg_print("Starting Benchmark of strategy: " + repr(strategy.__class__.__name__))
    bot = Bot(strategy)
    score = 0.0

    for round in irange(1, rounds + 1):
        board = Board()

        bot.play(board, show_steps=False)

        final_board_score = get_final_board_score(board)

        score += final_board_score

        dbg_print(
            "Finished round %d/%d.\t\t(avg: %.3f,\tcur: %d)" %
            (
              round,
              rounds,
              score / round,
              final_board_score
            )
        )


    ret = score / rounds

    dbg_print("Benchmark Result: " + str(ret))

    return ret

if __name__ == "__main__":
    benchmark_strategy(
        AdvancedBoardScoreStrategy(
            ace_heuristic,
            depth_modifier=0,
            agg_func=lambda scores: average(scores)
        ),
        rounds=50,
        show_logs=True
    )