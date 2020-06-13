# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.landscape import Cell, Lowland, Highland, Desert, Water
from biosim.animals import Animal, Herbivore, Carnivore
import pytest


class TestCell:

    def test_constructor(self):
        ll = Lowland()
        h = Highland()
        d = Desert()
        w = Water()
        assert isinstance(ll, Lowland)
        assert isinstance(h, Highland)
        assert isinstance(d, Desert)
        assert isinstance(w, Water)

    def test_type_error_parameters(self):
        with pytest.raises(TypeError):
            ll = Lowland
            ll.set_parameters([1, 2, 3])

    def test_is_there_fodder(self):
        ll = Lowland()
        assert ll.fodder == 800

    def test_animals_placed(self):
        pass
