
class Season:

    def __init__(self, weeks):
        """ Weeks spanning a season

        Parameters
        ----------
        weeks : iter(week.Week)
            Weeks of the season

        """
        self._week_number_to_week = {week.week_number: week
                                     for week in weeks}

    def __iter__(self):
        """ Iterate through weeks

        `yield from` produces regular generator instead of `dict_values`

        Yields
        ------
        week.Week
            Next week of season

        """
        yield from self._week_number_to_week.values()

    @property
    def weeks(self):
        """ Weeks in season

        Yields
        ------
        week.Week
            Next week of season

        """
        yield from self

    def nth_week(self, week_number):
        """ Get nth week of season

        Parameters
        ----------
        week_number : int
            Week number

        Returns
        -------
        week.Week

        """
        try:
            return self._week_number_to_week[week_number]
        except KeyError:
            raise ValueError(f'Week {week_number} is not included in season {self}')
