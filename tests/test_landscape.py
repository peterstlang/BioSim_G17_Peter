# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.landscape import Cell, Lowland, Highland, Desert, Water
from biosim.animals import Herbivore, Carnivore
import pytest


class TestCell:
    """
    the Cell testclass
    """

    def test_constructor(self):
        """
        Tests that the subclasses are created
        :return:
        """
        ll = Lowland()
        h = Highland()
        d = Desert()
        w = Water()
        assert isinstance(ll, Lowland)
        assert isinstance(h, Highland)
        assert isinstance(d, Desert)
        assert isinstance(w, Water)

    def test_type_error_parameters(self):
        """
        Tests that a TypeError is raised when you don't input a dictionary in set_parameters
        :return:
        """
        with pytest.raises(TypeError):
            ll = Lowland
            ll.set_parameters([1, 2, 3])

    def test_is_there_fodder(self):
        """
        Tests that there is fodder in a Lowland cell
        :return:
        """
        ll = Lowland()
        assert ll.fodder == 800

    def test_place_animals(self):
        """
        Tests that Animals can be placed in a cell
        :return:
        """
        c = Cell()
        herbs = [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]
        carns = [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(40)]

        assert c.place_animals(herbs) == c.herbivore.append(herbs)
        assert c.place_animals(carns) == c.carnivore.append(carns)

    def test_procreation(self, mocker):
        """
        Tests that animals can procreate
        :return:
        """
        mocker.patch('numpy.random.random', return_value=0)
        l = Lowland()
        l.herbivore = [Herbivore(5, 50), Herbivore(5, 50)]
        l.carnivore = [Carnivore(5, 50), Carnivore(5, 50)]
        l.procreation_animals()

        assert len(l.herbivore) >= 3
        assert len(l.carnivore) >= 3

    def test_animals_die(self):
        """
        Tests that animals die
        :return:
        """
        c = Cell()
        c.herbivore = [Herbivore(5, 0), Herbivore(5, 100)]
        c.carnivore = [Carnivore(5, 0), Carnivore(5, 100)]
        c.herbivore[0].fitness = 0
        c.herbivore[1].fitness = 1
        c.carnivore[0].fitness = 0
        c.carnivore[1].fitness = 1
        c.animals_die()

        assert len(c.herbivore) == 1
        assert len(c.carnivore) == 1

