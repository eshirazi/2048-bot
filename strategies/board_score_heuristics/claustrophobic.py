def claustrophobic_heuristic(board):
    num_free_tiles = board.get_free_tiles()

    score = 1.0

    if num_free_tiles < 4:
        score /= 2
    if num_free_tiles < 2:
        score /= 2
    if num_free_tiles < 1:
        score /= 2

    return score