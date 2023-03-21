from __future__ import annotations
from abc import ABC, abstractmethod

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
       """
       self.special_mode = not self.special_mode



    def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
        """
        Returns the colour this square should show, given the current layers.

        """

        if self.layer is None:
            return start

        if self.add:
            if self.special_mode:
                color = tuple(255 - c for c in self.layer.apply(start,timestamp,x,y))
                return color
            color = self.layer.apply(start,timestamp,x,y)
            return color
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
         self.layer_list = CircularQueue(max_capacity=100)


     def add(self,layer: Layer):
         self.layer_list.append(layer)

     def erase(self,layer: Layer):
         self.layer_list.serve()

     def special(self):
         q_layer_lst = list(self.layer_list.queue)
         q_layer_lst.reverse()
         self.layer_list = Queue()
         for layer in q_layer_lst:
             self.layer_list.append(layer)


     def get_color(self, start: tuple[int, int, int], timestamp: int, x: int, y: int) -> tuple[int, int, int]:
         pass





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
