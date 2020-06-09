# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.animals import Animal, Herbivore, Carnivore
import pytest


class TestAnimal:

    # Heavily inspired by biolab, need to ask some questions regarding this
    # @pytest.fixture
    # def set_parameters(request):
    #    Herbivore.set_parameters(request.param)
    #    yield
    #    Herbivore.set_parameters(Herbivore.parameters)

    def test_type_error_set_parameters(self):
        with pytest.raises(TypeError):
            h = Herbivore()
            h.set_parameters([1, 2, 3])

    def test_key_error_set_parameters(self):
        with pytest.raises(KeyError):
            h = Herbivore()
            h.set_parameters({'w_birth': 8.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05,
                              'a_half': 40.0, 'phi_age': 0.6, 'w_half': 10.0, 'phi_weight':
                                  0.1, 'mu': 0.25, 'gamma': 0.2, 'zeta': 3.5, 'xi': 1.2,
                              'omega': 0.4, 'F': 10.0, 'this_param_doesnt_belong': 0.0})

    def test_updated_parameters(self):
        h = Herbivore()
        new_params = {'w_birth': 10.0, 'sigma_birth': 1.5, 'beta': 0.9, 'eta': 0.05,
                      'a_half': 40.0, 'phi_age': 2.6, 'w_half': 10.0, 'phi_weight':
                          0.1, 'mu': 0.5, 'gamma': 7.2, 'zeta': 3.5, 'xi': 1.2,
                      'omega': 0.4, 'F': 20.0}
        h.set_parameters(new_params)
        assert h.parameters == new_params

    def test_constructor(self):
        h = Herbivore()
        c = Carnivore()
        assert isinstance(h, Herbivore)
        assert isinstance(c, Carnivore)

    def test_subclass(self):
        h = Herbivore()
        c = Carnivore()
        assert issubclass(h.__class__, Animal)
        assert issubclass(c.__class__, Animal)

    def test_type_error_age(self):
        with pytest.raises(TypeError):
            h = Herbivore([1, 2], 1)

    def test_value_error_age(self):
        with pytest.raises(ValueError):
            h = Herbivore(-1, 1)

    def test_type_and_value_error_weight(self):
        with pytest.raises(TypeError):
            h = Herbivore(1, 'a')
        with pytest.raises(ValueError):
            h = Herbivore(1, -1)

    def test_herbivore_age(self):
        h = Herbivore()
        assert h.age == 0

    def test_update_age(self):
        h = Herbivore()
        h.update_age()
        assert h.age == 1

    def test_birth_weight(self):
        h = Herbivore()
        assert h.weight >= 0

    def test_yearly_weight_loss(self):
        h = Herbivore(age=1, weight=7)
        h.yearly_weight_loss()
        assert h.weight < 7

    def test_compute_fitness_with_no_weight(self):
        h = Herbivore(1, 0)
        h.compute_fitness()
        assert h.fitness == 0

    def test_eat_weight_gain(self):
        food_available = 50
        h = Herbivore(1, 7)
        h.eat(food_available)
        assert h.weight > 7
