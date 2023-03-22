from __future__ import annotations
from abc import ABC, abstractmethod
from data_structures.stack_adt import ArrayStack
from data_structures.queue_adt import Queue, CircularQueue
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
        self.color = (0,0,0)



    def add(self, layer: Layer) -> bool:
        """
        Add a layer to the store.
        Returns true if the LayerStore was actually changed.
        """
        if layer != self.layer:
            self.layer = layer
            return True
        return False





    def erase(self, layer: Layer) -> bool:
        """
        Complete the erase action with this layer
        Returns true if the LayerStore was actually changed.

        """

        if layer != self.layer:
            self.layer = None
            return True
        return False



    def special(self):
       """
       Special mode. Different for each store implementation.
              if self.special_mode:
           self.color = (255 - self.color[0], 255 - self.color[1], 255 - self.color[2])

       """
       self.special_mode = not self.special_mode



    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        """

        if self.layer is None:
            return start

        if self.add:
            self.color = self.layer.apply(start, timestamp, x, y)
            if self.special_mode:
                self.color = tuple(255 - c for c in self.layer.apply(start,timestamp,x,y))
            start = self.color
            return self.color
        else:
            raise Exception("error")



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
         self.layer_list.append(layer)

     def erase(self,layer: Layer):
         self.layer_list.serve()

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
             while not self.layer_list.is_empty():
                 if self.special_mode:
                     color = tuple(255 - c for c in self.layer_list.serve().apply(start, timestamp, x, y))
                     return color
                 color = self.layer_list.serve().apply(start, timestamp, x, y)
             return color
         else:
             raise Exception("error")



        """

         if self.layer_list.is_empty():
             return start
         if not self.layer_list.is_empty():
             temporary_q = CircularQueue(max_capacity = 100)
             while not self.layer_list.is_empty():
                 layer_serve = self.layer_list.serve()
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









class SequenceLayerStore(LayerStore):
    """
    Sequential layer store. Each layer type is either applied / not applied, and is applied in order of index.
    - add: Ensure this layer type is applied.
    - erase: Ensure this layer type is not applied.
    - special:
        Of all currently applied layers, remove the one with median `name`.
        In the event of two layers being the median names, pick the lexicographically smaller one.
    """

    pass
