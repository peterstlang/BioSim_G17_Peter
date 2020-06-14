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
        ll = Lowland()
        a_list = [Herbivore(), Carnivore()]
        ll.place_animals(a_list)
        assert len(ll.herbivores) == 1
        assert len(ll.carnivores) == 1

    def test_animal_is_birthed(self, mocker):
        # mocker.patch('give_birth', return_value=True)
        # h1 = Herbivore()
        # h2 = Herbivore()
        # h_list = [h1, h2]
        # c = Lowland
        # c.place_animals(h_list)
        # c.procreation_animals()
        # assert len(h_list) == 4
        pass

    def test_feed_herbivores(self):
        h_list = [Herbivore()]
        ll = Lowland()
        ll.place_animals(h_list)
        ll.feed_herbivores()
        assert ll.fodder == 790
