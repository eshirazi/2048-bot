class BaseStrategy(object):
    def get_next_move(self, board):
        raise NotImplementedError()