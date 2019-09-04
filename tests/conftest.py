import pytest

from nfl_survivor.game import Game
from nfl_survivor.picks import Picks
from nfl_survivor.season import Season
from nfl_survivor.week import Week


@pytest.fixture
def game_one():
    return Game(('a', 0.1), ('b', 0.9))


@pytest.fixture
def game_two():
    return Game(('c', 0.2), ('d', 0.8))


@pytest.fixture
def game_three():
    return Game(('e', 0.3), ('f', 0.7))


@pytest.fixture
@pytest.mark.usefixtures('game_one')
def week_one(game_one):
    return Week(1, (game_one,))


@pytest.fixture
@pytest.mark.usefixtures('game_one',
                         'game_two')
def week_two(game_one, game_two):
    return Week(2, (game_one, game_two))


@pytest.fixture
@pytest.mark.usefixtures('game_one',
                         'game_two',
                         'game_three')
def week_three(game_one, game_two, game_three):
    return Week(3, (game_one, game_two, game_three))


@pytest.fixture
@pytest.mark.usefixtures('week_one',
                         'week_two',
                         'week_three')
def season(week_one, week_two, week_three):
    return Season((week_one, week_two, week_three))


@pytest.fixture
def picks():
    return Picks(((1, 'a'), (2, 'c')))
