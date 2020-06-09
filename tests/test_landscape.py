# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.landscape import Cell, Lowland, Highland, Desert, Water


class TestCell:

    def test_constructor(self):
        c = Cell()
        l = Lowland()
        h = Highland()
        d = Desert()
        w = Water()
        assert isinstance(c, Cell)
        assert isinstance(l, Lowland)
        assert isinstance(h, Highland)
        assert isinstance(d, Desert)
        assert isinstance(w, Water)
