from math import sqrt
from strategies.board_score_heuristics.claustrophobic import claustrophobic_heuristic
from strategies.board_score_heuristics.side_sticky import side_sticky_heuristic, side_smooth_sticky_heuristic
from strategies.board_score_heuristics.sum_square import sum_square_heuristic

supxtra_heuristic = lambda board: sqrt(sum_square_heuristic(board)) + side_smooth_sticky_heuristic(board)
ace_heuristic = lambda board: sum_square_heuristic(board) + side_sticky_heuristic(board)
king_heuristic = lambda board: sum_square_heuristic(board) * claustrophobic_heuristic(board)