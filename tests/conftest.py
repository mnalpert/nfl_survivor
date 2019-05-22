import pytest

from nfl_survivor.game import Game


@pytest.fixture
def game():
    return Game(('a', 0.6), ('b', 0.4))
