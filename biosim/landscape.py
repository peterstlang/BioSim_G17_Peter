# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'


class Cell:
    """
    cell superclass
    """

    def __init__(self):
        pass

    def grow_fodder(self):
        pass

    def feed_animals(self):
        pass

    def procreation(self):
        pass

    def aging_animals(self):
        pass

    def animals_weight_loss(self):
        pass

    def animals_die(self):
        pass


class Water(Cell):
    pass


class Desert(Cell):
    pass


class Lowland(Cell):
    pass


class Highland(Cell):
    pass
