import pytest

from nfl_survivor.season import Season


@pytest.fixture
@pytest.mark.usefixtures('week_one',
                         'week_two',
                         'week_three')
def weeks(week_one, week_two, week_three):
    return (week_one, week_two, week_three)


@pytest.mark.usefixtures('season', 'weeks')
class TestSeason:

    def test_init(self, season, weeks):
        week_one, week_two, week_three = weeks

        assert season._week_number_to_week == {1: week_one,
                                               2: week_two,
                                               3: week_three}

    def test_iter(self, season, weeks):
        assert tuple(season) == weeks

    def test_weeks(self, season, weeks):
        assert tuple(season.weeks) == weeks

    def test_teams(self, season):
        assert season.teams == {'a', 'b', 'c', 'd', 'e', 'f'}

    def test_nth_week(self, season, weeks):
        week_one, week_two, week_three = weeks

        assert season.nth_week(1) == week_one
        assert season.nth_week(2) == week_two
        assert season.nth_week(3) == week_three

        with pytest.raises(ValueError) as exception:
            season.nth_week(4)

        exception_msg = str(exception.value)

        assert '4' in exception_msg and 'not included' in exception_msg

    def test_team_to_weeks(self, season, weeks):
        week_one, week_two, week_three = weeks

        expected_team_to_weeks = {'a': [week_one, week_two, week_three],
                                  'b': [week_one, week_two, week_three],
                                  'c': [week_two, week_three],
                                  'd': [week_two, week_three],
                                  'e': [week_three],
                                  'f': [week_three]}

        assert all(sorted(weeks, key=lambda w: w.week_number) ==
                   expected_team_to_weeks[team]
                   for team, weeks in season._team_to_weeks.items())

    def test_team_weeks(self, season, weeks):
        week_one, week_two, week_three = weeks

        expected_team_to_weeks = {'a': [week_one, week_two, week_three],
                                  'b': [week_one, week_two, week_three],
                                  'c': [week_two, week_three],
                                  'd': [week_two, week_three],
                                  'e': [week_three],
                                  'f': [week_three]}

        assert all(sorted(season.team_weeks(team), key=lambda w: w.week_number) ==
                   expected_team_to_weeks[team] for team in ('a', 'b', 'c', 'd',
                                                             'e', 'f'))

        assert season.team_weeks('g') == []

    def test_picks_win_probability(self, season):
        picks = {1: 'b',
                 2: 'd',
                 3: 'f'}

        assert season.picks_win_probability(picks) == 0.9 * 0.8 * 0.7

    def test_from_dict(self):
        season = Season.from_dict([{'week': {'number': 1,
                                             'games': [{'game': [{'team': {'name': 'a',
                                                                           'probability': 0.1}},
                                                                 {'team': {'name': 'b',
                                                                           'probability': 0.9}}]}]}}])

        assert len(tuple(season.weeks)) == 1
        assert season.teams == {'a', 'b'}

    def test_from_yaml(self):
        season = Season.from_yaml('./tests/test_data/test_season.yaml')

        assert len(tuple(season.weeks)) == 3
        assert season.teams == {'a', 'b', 'c', 'd', 'e', 'f'}
