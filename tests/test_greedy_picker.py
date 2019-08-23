import pytest

from nfl_survivor.greedy_picker import GreedyPicker
from nfl_survivor.season import Season


@pytest.fixture
@pytest.mark.usefixtures('season')
def greedy_picker(season):
    return GreedyPicker(season)


@pytest.fixture
def infeasible_season():
    return Season.from_dict([{'week': {'number': 1,
                                       'games': [{'game': [{'team': {'name': 'a',
                                                                     'probability': 0.1}},
                                                           {'team': {'name': 'b',
                                                                     'probability': 0.9}}]}]}},
                             {'week': {'number': 2,
                                       'games': [{'game': [{'team': {'name': 'a',
                                                                     'probability': 0.1}},
                                                           {'team': {'name': 'c',
                                                                     'probability': 0.9}}]}]}},
                             {'week': {'number': 3,
                                       'games': [{'game': [{'team': {'name': 'b',
                                                                     'probability': 0.1}},
                                                           {'team': {'name': 'c',
                                                                     'probability': 0.9}}]}]}}])


@pytest.fixture
@pytest.mark.usefixtures('infeasible_season')
def infeasible_greedy_picker(infeasible_season):
    # greedy algo on infeasible season leaves us with no team to pick in week 3
    return GreedyPicker(infeasible_season)


@pytest.mark.usefixtures('greedy_picker', 'infeasible_greedy_picker')
class TestGreedyPicker:

    def test_picks_feasible(self, greedy_picker):
        assert greedy_picker.picks() == {1: 'b',
                                         2: 'd',
                                         3: 'f'}

    def test_picks_infeasible(self, infeasible_greedy_picker):
        with pytest.raises(ValueError) as exception:
            infeasible_greedy_picker.picks()

        exception_msg = str(exception.value)

        assert 'Cannot solve' in exception_msg and 'week 3' in exception_msg
