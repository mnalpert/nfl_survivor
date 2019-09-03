from abc import ABCMeta, abstractmethod

from nfl_survivor.picks import Picks


class Picker(metaclass=ABCMeta):

    def __init__(self, season, previous_picks=None):
        """ Pick maker for a season

        Parameters
        ----------
        season : season.Season
            Season to make picks for
        previous_picks : picks.Picks, optional
            Predetermined picks

        """
        self._season = season
        self._previous_picks = previous_picks if previous_picks is not None else Picks()

    @property
    def season(self):
        """ Getter for season

        Returns
        -------
        season.Season

        """
        return self._season

    @property
    def previous_picks(self):
        """ Getter for previous picks

        Returns
        -------
        picks.Picks

        """
        return self._previous_picks

    @abstractmethod
    def picks(self):
        pass
