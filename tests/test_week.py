import pytest


@pytest.fixture
@pytest.mark.usefixtures('week_three')
def week(week_three):
    return week_three


@pytest.fixture
@pytest.mark.usefixtures('game_one',
                         'game_two',
                         'game_three')
def games(game_one, game_two, game_three):
    return (game_one, game_two, game_three)


@pytest.mark.usefixtures('week', 'games')
class TestWeek:

    def test_week_number(self, week):
        assert week.week_number == 3

    def test_games(self, week, games):
        assert week.games == games

    def test_iter(self, week, games):
        assert tuple(week) == games

    def test_team_to_game(self, week, games):
        game_one, game_two, game_three = games

        assert week._team_to_game == {'a': game_one,
                                      'b': game_one,
                                      'c': game_two,
                                      'd': game_two,
                                      'e': game_three,
                                      'f': game_three}

    def team_game(self, week, games):
        game_one, game_two, game_three = games

        assert week.team_game('a') == game_one
        assert week.team_game('b') == game_one
        assert week.team_game('c') == game_two
        assert week.team_game('d') == game_two
        assert week.team_game('e') == game_three
        assert week.team_game('f') == game_three

        with pytest.raises(ValueError) as exception:
            week.team_game('g')

        exception_msg = str(exception.value)
        assert 'g' in exception_msg and 'not playing' in exception_msg

    def test_teams(self, week):
        assert set(week.teams) == {'a', 'b', 'c', 'd', 'e', 'f'}
