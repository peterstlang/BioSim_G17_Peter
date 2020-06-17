# -*- coding: utf-8 -*-

"""

"""

__author__ = 'Peter Langdalen'
__email__ = 'pelangda@nmbu.no'

from biosim.animals import Animal, Herbivore, Carnivore
import pytest


class TestAnimal:

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

    @pytest.mark.parametrize("animal_class", [Herbivore, Carnivore])
    def test_constructor(self, animal_class):
        a = animal_class(5, 20)
        assert hasattr(a, 'age')
        assert hasattr(a, 'weight')
        assert hasattr(a, 'fitness')

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

    @pytest.mark.parametrize("animal_class", [Herbivore, Carnivore])
    def test_herbivore_age(self, animal_class):
        a = animal_class()
        assert a.age == 0

    @pytest.mark.parametrize("animal_class", [Herbivore, Carnivore])
    def test_update_age(self, animal_class):
        a = animal_class()
        a.update_age()
        assert a.age == 1

    @pytest.mark.parametrize("animal_class", [Herbivore, Carnivore])
    def test_birth_weight(self, animal_class):
        a = animal_class()
        assert a.weight >= 0

    @pytest.mark.parametrize("animal_class", [Herbivore, Carnivore])
    def test_fitness_increase(self, animal_class):
        a1 = animal_class(5, 10)
        a2 = animal_class(5, 30)
        assert a1.fitness <= a2.fitness

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

    def test_birth(self, mocker):
        mocker.patch("numpy.random.random", return_value=0)
        h = Herbivore(5, 50)
        c = Carnivore(5, 50)
        herbs = h.give_birth(10)
        carns = c.give_birth(10)
        assert herbs
        assert carns

    @pytest.mark.parametrize("animal_class", [Herbivore, Carnivore])
    def test_death(self, mocker, animal_class):
        mocker.patch("numpy.random.random", return_value=0)

        a = animal_class(5, 0)
        dead_animal = a.death()
        assert dead_animal

    def test_kill_herb_is_herb_sorted(self):
        import operator
        h1 = Herbivore(5, 10)
        h2 = Herbivore(3, 5)
        h3 = Herbivore(10, 20)
        h_list = [h1, h2, h3]
        sorted_list = sorted(h_list, key=operator.attrgetter("fitness"))
        print(sorted_list)
        assert set(h_list) == set(sorted_list)

    @pytest.mark.parametrize("animal_class", [Herbivore, Carnivore])
    def test_gaussian_distribution_ini_weight(self, animal_class):
        from scipy.stats import kstest
        alpha = 0.01
        list_of_ini_weights = []
        for _ in range(1000):
            a = animal_class()
            list_of_ini_weights.append(a.weight)
            ks, p_value = kstest(list_of_ini_weights, 'norm')
            assert p_value < alpha
