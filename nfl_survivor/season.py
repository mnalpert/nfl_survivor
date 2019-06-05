import collections

import yaml

from nfl_survivor.utils import cached_property
from nfl_survivor.week import Week


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

    @property
    def teams(self):
        """ All teams playing in season

        Returns
        -------
        set(str)

        """
        return set.union(*(set(week.teams) for week in self))

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

    @cached_property
    def _team_to_weeks(self):
        """ Map from teams to weeks in which they are playing

        Returns
        -------
        dict(str->list(week.Week))

        """
        team_to_weeks = collections.defaultdict(list)
        for week in self:
            for team in week.teams:
                team_to_weeks[team].append(week)

        return team_to_weeks

    def team_weeks(self, team):
        """ Weeks in which a team plays in

        If a team is not playing in the season this will return empty list

        Parameters
        ----------
        team : str
            Team to get weeks playing for

        Returns
        -------
        list(week.Week)
            Weeks in which team is playing

        """
        return self._team_to_weeks[team]

    @classmethod
    def from_dict(cls, season_dict):
        """ Form season from dictionary represenation

        Parameters
        ----------
        season_dict : dict

        Returns
        -------
        season.Season

        """
        return cls(Week.from_dict(week_dict['week']) for week_dict in season_dict)

    @classmethod
    def from_yaml(cls, yaml_file_path):
        """ Form season from representation in YAML file

        Parameters
        ----------
        yaml_file_path : str
            Path to YAML file of season representation

        Returns
        -------
        season.Season

        """
        with open(yaml_file_path, 'r') as yaml_file:
            return cls.from_dict(yaml.load(yaml_file, Loader=yaml.Loader))
