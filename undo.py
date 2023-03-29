from __future__ import annotations
from action import PaintAction
from grid import Grid
from data_structures.stack_adt import ArrayStack

class UndoTracker:

    def __init__(self):
        self.undo_stack = ArrayStack(max_capacity=100)
        self.redo_stack = ArrayStack(max_capacity=100)

    def add_action(self, action: PaintAction) -> None:
        """
        Adds an action to the undo tracker.

        If your collection is already full,
        feel free to exit early and not add the action.


        Doc:
        for this it will check the stack is full or not if its full then return none unless
        stack isnt full it will push the action into the stack(undo_stack) and
        reset the redo stack

        time complexity
        O(1) it is a simple increment
        """
        if self.undo_stack.is_full():
            return
        self.undo_stack.push(action)
        self.redo_stack = ArrayStack(max_capacity=100)

    def undo(self, grid: Grid) -> PaintAction|None:
        """
        Undo an operation, and apply the relevant action to the grid.
        If there are no actions to undo, simply do nothing.

        :return: The action that was undone, or None.

        Doc:
        check the stack if its empty or not if empty return none else
        it will update the action and pop out the latest layer put into the
        stack and then the redo_stack is pushed with the action value
        and using the undo_apply function it apply the grid with that
        layer and return the action

        time complexity:
        O(1) as this is just a simple increment of updating the stack
        but in the worst case it will be O(n)

        """
        if not self.undo_stack:
            return None
        action = self.undo_stack.pop()
        self.redo_stack.push(action)
        action.undo_apply(grid)
        return action

    def redo(self, grid: Grid) -> PaintAction|None:
        """
        Redo an operation that was previously undone.
        If there are no actions to redo, simply do nothing.

        :return: The action that was redone, or None.

        Doc:
        same as before check the stack if its empty or not if empty return none else
        it will update the action and pop out the latest layer put into the
        stack and then the redo_stack is pushed with the action value
        and using the redo_apply function it apply the grid with that action
        layer and return the action

        Time complexity:
        O(1) as this is just a simple increment of updating the stack
        but in the worst case it will be O(n)

        """
        if not self.redo_stack:
            return None
        action = self.redo_stack.pop()
        self.undo_stack.push(action)
        action.redo_apply(grid)
        return action
