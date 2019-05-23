import pytest


@pytest.fixture
@pytest.mark.usefixtures('game_one')
def game(game_one):
    return game_one


@pytest.mark.usefixtures('game')
class TestGame:

    def test_init(self, game):
        assert game._team_to_probability == {'a': 0.1,
                                             'b': 0.9}

    def test_iter(self, game):
        assert set(game) == {'a', 'b'}

    def test_repr(self, game):
        representation = repr(game)

        assert all(('Game' in representation,
                    'a' in representation,
                    'b' in representation))

    def test_contains(self, game):
        assert 'a' in game
        assert 'b' in game
        assert 'c' not in game

    def test_teams(self, game):
        assert set(game.teams) == {'a', 'b'}

    def test_win_probability(self, game):
        assert game.win_probability('a') == 0.1
        assert game.win_probability('b') == 0.9

        with pytest.raises(ValueError) as exception:
            game.win_probability('c')

        exception_msg = str(exception.value)
        assert 'c' in exception_msg and 'not playing' in exception_msg
