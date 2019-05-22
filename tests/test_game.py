import pytest


@pytest.mark.usefixtures('game')
class TestGame:

    def test_init(self, game):
        assert game._team_to_probability == {'a': 0.6,
                                             'b': 0.4}

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
        assert game.win_probability('a') == 0.6
        assert game.win_probability('b') == 0.4

        with pytest.raises(ValueError) as exception:
            game.win_probability('c')

        assert 'c' in str(exception.value) and 'not playing' in str(exception.value)
