from __future__ import annotations
from abc import ABC, abstractmethod

import layer_util
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import CircularQueue
from data_structures.array_sorted_list import ArraySortedList
from data_structures.sorted_list_adt import ListItem
from layer_util import Layer


class LayerStore(ABC):


    def __init__(self) -> None:
        pass

    @abstractmethod
    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def get_color(self,start, timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        """
        pass

    @abstractmethod
    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.
        """
        pass

    @abstractmethod
    def special(self):
        """
        Special mode. Different for each store implementation.
        """
        pass





class SetLayerStore(LayerStore):

    """
    Set layer store. A single layer can be stored at a time (or nothing at all)
    - add: Set the single layer.
    - erase: Remove the single layer. Ignore what is currently selected.
    - special: Invert the colour output.
    """

    def __init__(self) -> None:
        """
        Doc:
        call the super to grab method of a superclass from a subclass as for this
        case the layerstore class .besides that the self.layer is set to none and
        special mode is false

        """
        super().__init__()
        self.layer = None
        self.special_mode = False




    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.


        Doc:
        add a given layer to the self.layer to store it and can be used for the
        get_color function later

        Time complexity:
        O(1) simple increment
        """
        if layer is not self.layer:
            self.layer = layer
            return True
        return False





    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.

        Doc:
        erase a given layer to the self.layer to store it to none
        so regardless of any input it will set the layer to none for the
        get_color function later

        Time complexity:
        O(1) simple increment
        """

        if layer is not self.layer:
            self.layer = None
            return True
        return False



    def special(self):
       """
       Special mode. Different for each store implementation.

       Doc :
       toggle the special to True if this is called

       """
       self.special_mode = not self.special_mode



    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        Doc:
        this code get_color returns a tuple of the color to be implemented into the
        paint app . For the start if there isnt any layer inputted it will just
        return the start value . If there is a layer (which is not none) it will
        update the self.color calling the apply function with the given layer inputted by
        the user to use the function that is placed inside the layer_util.py file
        to access the layer.py file to call the functions in it . for the special, if
        the special is called it will invert the tuple valus by having it to minus
        255 and update the self.color and return it

        Time complexity:
        O(1) simple increment as there is no loops
        """

        if self.layer is None:
            return start
        if self.layer is not None:
            self.color = self.layer.apply(start, timestamp, x, y)
            if self.special_mode:
                self.color = tuple(255 - c for c in self.layer.apply(start, timestamp, x, y))
            return self.color






class AdditiveLayerStore(LayerStore):
     """
    Additive layer store. Each added layer applies after all previous ones.
    - add: Add a new layer to be added last.
    - erase: Remove the first layer that was added. Ignore what is currently selected.
    - special: Reverse the order of current layers (first becomes last, etc.)
    """

     def __init__(self) -> None:
         """
         Doc:
         Set the Queue and the Stack inside the self.layer_list and self.stack_
         layer_list with a max capacity of 100. also initialising the self.color and 0,0,0
         and special mode as false

         """
         super().__init__()
         self.special_mode = False
         self.color = (0,0,0)
         self.layer_list = CircularQueue(max_capacity=100)
         self.stack_layer_list = ArrayStack(max_capacity=100)


     def add(self,layer: Layer):
         """
         Doc:
         add the layer into a queue using the special callee append to add the
         elements from the left in the queue and return true if it is none
         return false

         time complexity:
         O(1) it is a simple increment


         """
         if layer == None:
             return False
         self.layer_list.append(layer)
         return True

     def erase(self,layer: Layer):
         """
         Doc:
         erase the layer into a queue using the special callee serv to erase the
         first element that was put into the queue from the right  and return true if it is none
         return false

         time complexity:
         O(1) it is a simple increment
         """
         if self.layer_list.is_empty():
             return False
         self.layer_list.serve()
         return True

     def special(self):
         """
         Doc:
         Create the temperorary Queue and Stack to store the layer value
         What this special does is that it will reverse the order of the queue
         by using the queue to take the last element in the list (also the first to entered)
         and put it into a stack and then take the latest element to put it back into the queue
         with this id will reverse the order as first element in become the last to take inside the stack

         Time complexity:
         O(n) as the code takes the queue elements and serve them and then it
         pushes them back into a stack
         """
         temp_q = CircularQueue(max_capacity=100)
         temp_stack = ArrayStack(max_capacity=100)
         while not self.layer_list.is_empty():
             temp_stack.push(self.layer_list.serve())
         while not temp_stack.is_empty():
             temp_q.append(temp_stack.pop())
             self.layer_list.append(temp_q.serve())




     def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
         """
         Doc:
         First it identify itself as self.color is the start value and if
         there isnt a layer it will return the start value tuple . if the
         queue list(self.layer_list) is not empty it again create a new temporary
         list of the queue to store it for a while and it will go through another
         loop of while not as this while loop what it does is grabs all of the layer one
         by one by serving(grab end element) it and store it to layer_serve and add it
         to the temporary queue . The reason why i put into temporary queue is that
         since serve removes the layer in the queue and return it i need the queue to
         store the layers and not lose it when the serve is called to use.apply
          to call the layer function in the layer_util.py and layer.py. so to prevent this i
         create the temporary queue save the serve layers and once it is done with using
         the serve layers the queue will refilled with the temporary queue layers which are
         the same as before and then it will return the color tuple of that served layer.
         If it is special , what this does is that it will use the special queue where
         all of the layers are reverse and do the same . it will create a temporary queue special
         store the layers into temporary queue before serving the original queue which is
         self.layer_list to use the .apply function .so when it is done it will refill the
         original queue back to where it was with al the layers so that the next input
         can use the same ordered layers in the queue


         Time comeplexity:
         O(n^2) this is becaus there seems to be two while loops running
         where the while loop iterates thorugh the queue twice to store it into
         the temporary queue one for original and one for special


         """


         self.color = start
         if self.layer_list.is_empty():
             return self.color
         if not self.layer_list.is_empty():
             temporary_q = CircularQueue(max_capacity = 100)
             while not self.layer_list.is_empty():
                 layer_serve = self.layer_list.serve()
                 if layer_serve == None:
                     return
                 temporary_q.append(layer_serve)
                 self.color = layer_serve.apply(self.color, timestamp, x, y)
                 if self.special_mode:
                     self.color = start
                     while not self.layer_list.special().is_empty():
                         temporary_q_special = CircularQueue(max_capacity=100)
                         layer_serve_special = self.layer_list.special().serve()
                         temporary_q_special.append(layer_serve_special)
                         self.color = layer_serve_special.apply(self.color, timestamp, x, y)
                     self.layer_list = temporary_q_special
                     return self.color
             self.layer_list = temporary_q
             return self.color










class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    def __init__(self) -> None:
        super().__init__()
        self.layer_list = ArraySortedList(max_capacity=100)
        self.layer_list_special = ArraySortedList(max_capacity=100)
        self.color = (0,0,0)
        self.special_mode = False
        self.enter_special = 0





    def add(self, layer: Layer):
        if layer == None:
            return
        for layer_add in self.layer_list:
            if layer_add is None:
                self.layer_list.add(ListItem(layer.name, layer.index))
                break

            if layer_add.value == layer.name and layer_add.key == layer.index:
                return


    def erase(self, layer: Layer):
        """
                for layer_erase in self.layer_list:
            if layer_erase is None:
                break
            if layer_erase.value == layer.name and layer_erase.key == layer.index:
                self.layer_list.remove(layer_erase)
                self.layer_list.delete_at_index()
                break



        """
        for i in range(len(self.layer_list)):
            if self.layer_list[i] is None:
                break
            if self.layer_list[i].value == layer.name and self.layer_list[i].key == layer.index:
                self.layer_list.delete_at_index(i)
                self.layer_list._resize()
                break


    def special(self):
        """

        """



        apply_layers = len(self.layer_list)

        if apply_layers % 2 == 0:
            median_index = (apply_layers // 2) - 1
            temp_layer_list = [x for x in self.layer_list if x is not None]
            sort_layer_name = sorted(temp_layer_list, key=lambda x: x.value)
            for j in self.layer_list:
                if j is not None and j.value == sort_layer_name[median_index].value:
                    self.layer_list.remove(j)
                    self.layer_list._resize()
                    break


        else:
            median_index = apply_layers // 2
            temp_layer_list = [x for x in self.layer_list if x is not None]
            sort_layer_name = sorted(temp_layer_list, key=lambda x: x.value)
            for j in self.layer_list:
                if j is not None and j.value == sort_layer_name[median_index].value:
                    self.layer_list.remove(j)
                    self.layer_list._resize()
                    break


    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """

        """


        if self.layer_list.is_empty():
            return start
        for layer_sort in self.layer_list:
            if layer_sort is None:
                break
            name_layer = layer_sort.value
            for layer in layer_util.LAYERS:
                if layer.name == name_layer:
                     self.color = layer.apply(start, timestamp, x, y)
                     start = self.color
                     break
        return self.color





