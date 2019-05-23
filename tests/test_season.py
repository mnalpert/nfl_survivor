import pytest


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

    def test_nth_week(self, season, weeks):
        week_one, week_two, week_three = weeks

        assert season.nth_week(1) == week_one
        assert season.nth_week(2) == week_two
        assert season.nth_week(3) == week_three

        with pytest.raises(ValueError) as exception:
            season.nth_week(4)

        exception_msg = str(exception.value)

        assert '4' in exception_msg and 'not included' in exception_msg
