from abc import ABCMeta, abstractmethod


class Picker(metaclass=ABCMeta):

    def __init__(self, season):
        """ Pick maker for a season

        Parameters
        ----------
        season : season.Season
            Season to make picks for

        """
        self._season = season

    @property
    def season(self):
        """ Getter for season

        Returns
        -------
        season.Season

        """
        return self._season

    @abstractmethod
    def picks(self):
        pass
