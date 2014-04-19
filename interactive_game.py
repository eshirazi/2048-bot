from board import Board, IllegalMoveException
import move

KEY_TO_MOVE = {
    "Up": move.UP,
    "Down": move.DOWN,
    "Left": move.LEFT,
    "Right": move.RIGHT,
}


def start_interactive_game():
    a = Board()
    print(repr(a))

    try:
       # Python2
        import Tkinter as tk
    except ImportError:
        # Python3
        import tkinter as tk

    def key(event):
        if event.keysym in KEY_TO_MOVE:
            try:
                a.move(KEY_TO_MOVE[event.keysym])
                print(repr(a))
            except IllegalMoveException:
                pass

        if event.keysym == 'Escape' or not a.get_legal_moves():
            root.destroy()

    root = tk.Tk()
    root.bind_all('<Key>', key)

    # don't show the tk window
    root.withdraw()
    root.mainloop()

if __name__ == "__main__":
    start_interactive_game()