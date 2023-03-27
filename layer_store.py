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
        super().__init__()
        self.layer = None
        self.special_mode = False




    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        if layer is not self.layer:
            self.layer = layer
            return True
        return False





    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.

        """

        if layer is not self.layer:
            self.layer = None
            return True
        return False



    def special(self):
       """
       Special mode. Different for each store implementation.

       """
       self.special_mode = not self.special_mode



    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.
        else:
            raise Exception("error")
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
         super().__init__()
         self.special_mode = False
         self.color = (0,0,0)
         self.layer_list = CircularQueue(max_capacity=100)
         self.stack_layer_list = ArrayStack(max_capacity=100)


     def add(self,layer: Layer):
         if layer == None:
             return False
         self.layer_list.append(layer)
         return True

     def erase(self,layer: Layer):
         if self.layer_list.is_empty():
             return False
         self.layer_list.serve()
         return True

     def special(self):
         temp_q = CircularQueue(max_capacity=100)
         temp_stack = ArrayStack(max_capacity=100)
         while not self.layer_list.is_empty():
             temp_stack.push(self.layer_list.serve())
         while not temp_stack.is_empty():
             temp_q.append(temp_stack.pop())
             self.layer_list.append(temp_q.serve())




     def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
         """
        if self.layer_list.is_empty():
             return start
         if not self.layer_list.is_empty():
             temporary_q = CircularQueue(max_capacity = 100)
             while not self.layer_list.is_empty():
                 layer_serve = self.layer_list.serve()
                 if layer_serve == None:
                     return
                 temporary_q.append(layer_serve)
                 self.color = layer_serve.apply(start, timestamp, x, y)
                 start = self.color
                 if self.special_mode:
                     while not self.layer_list.special().is_empty():
                         temporary_q_special = CircularQueue(max_capacity=100)
                         layer_serve_special = self.layer_list.special().serve()
                         temporary_q_special.append(layer_serve_special)
                         self.color = layer_serve_special.apply(start, timestamp, x, y)
                         start = self.color
                     self.layer_list = temporary_q_special
                     return self.color
             self.layer_list = temporary_q
             return self.color
         else:
             raise Exception("error")

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





