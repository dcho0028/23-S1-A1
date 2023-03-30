from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.queue_adt import CircularQueue


class ReplayTracker:

    def __init__(self):
        """
        Doc:
        set the queue into self.actions and the self.is_replay to false

        """
        self.actions = CircularQueue(max_capacity=1000)
        self.is_replay = False
        self.replay_started = False



    def start_replay(self) -> None:
        """
        Called whenever we should stop taking actions, and start playing them back.

        Useful if you have any setup to do before `play_next_action` should be called.

        Doc:
        set the self.is_replay to true and to check if the self.replay is true or
        not if its true clear the queue

        time complexity:
        O(1) it is a simple increment


        """
        self.is_replay = True
        if self.replay_started:
            self.actions.clear()
        self.replay_started = True




    def add_action(self, action: PaintAction, is_undo: bool=False) -> None:
        """
        Adds an action to the replay.

        `is_undo` specifies whether the action was an undo action or not.
        Special, Redo, and Draw all have this is False.

        Doc:
        append the action and is_undo value
        """
        #if not self.is_replay:
        self.actions.append((action,is_undo))



    def play_next_action(self, grid: Grid) -> bool:
        """
        Plays the next replay action on the grid.
        Returns a boolean.
            - If there were no more actions to play, and so nothing happened, return True.
            - Otherwise, return False.

        Doc:
        to check if the queue is empty or not if its empty it means that the replay
        has ended and return true if not empty then it will serve the action and undo
        seperately and it will undo or redo the grid layers and return false

        time complexity:
        O(1)
        """

        if self.actions.is_empty():
            return True

        action, is_undo = self.actions.serve()

        if is_undo:
            action.undo_apply(grid)

        else:
            action.redo_apply(grid)


        return False




if __name__ == "__main__":
    action1 = PaintAction([], is_special=True)
    action2 = PaintAction([])

    g = Grid(Grid.DRAW_STYLE_SET, 5, 5)

    r = ReplayTracker()
    # add all actions
    r.add_action(action1)
    r.add_action(action2)
    r.add_action(action2, is_undo=True)
    # Start the replay.
    r.start_replay()
    f1 = r.play_next_action(g) # action 1, special
    f2 = r.play_next_action(g) # action 2, draw
    f3 = r.play_next_action(g) # action 2, undo
    t = r.play_next_action(g)  # True, nothing to do.
    assert (f1, f2, f3, t) == (False, False, False, True)

