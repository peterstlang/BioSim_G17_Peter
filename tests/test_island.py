# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.animals import Herbivore, Carnivore
from biosim.landscape import Cell, Lowland, Highland, Desert, Water
from biosim.island import Island
import pytest
import textwrap
import numpy as np

default_map = """
    WWWWWWWWWWWWWWWWWWWWW
    WWWWWWWWHWWWWLLLLLLLW
    WHHHHHLLLLWWLLLLLLLWW
    WHHHHHHHHHWWLLLLLLWWW
    WHHHHHLLLLLLLLLLLLWWW
    WHHHHHLLLDDLLLHLLLWWW
    WHHLLLLLDDDLLLHHHHWWW
    WWHHHHLLLDDLLLHWWWWWW
    WHHHLLLLLDDLLLLLLLWWW
    WHHHHLLLLDDLLLLWWWWWW
    WWHHHHLLLLLLLLWWWWWWW
    WWWHHHHLLLLLLLWWWWWWW
    WWWWWWWWWWWWWWWWWWWWW"""

default_map = textwrap.dedent(default_map)


class TestIsland:
    """
    The island testclass
    """

    def test_constructor(self):
        """
        Tests the constructor of the island class
        """
        i = Island(default_map)
        assert hasattr(i, 'island')

    def test_wrong_map(self):
        """
        Tests that a ValueError is raised when you input a map
        that doesn't have the correct borders (only water cells)
        """
        with pytest.raises(ValueError):
            i = Island("""WL
                          LW""")
            i.create_map("""WL
                            LW""")



