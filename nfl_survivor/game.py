
class Game:

    def __init__(self, team_prob_one, team_prob_two):
        """ One game between two teams and their respective win probabilities

        Parameters
        ----------
        team_prob_one : str, float
            Name of team one and probability of team winning game
        team_prob_two : str, float
            Name of team two and probability of team winning game

        """
        self._team_to_probability = dict((team_prob_one, team_prob_two))

    def __iter__(self):
        """ Iterate through team names

        `yield from` produces regular generator instead of `dict_keys`

        Yields
        ------
        str
            Next team name

        """
        yield from self._team_to_probability.keys()

    def __repr__(self):
        """ Readable representation of game

        Returns
        -------
        str

        """
        return f'Game({self._team_to_probability})'

    def __contains__(self, team):
        """ Indicate whether team is playing in game

        Parameters
        ----------
        team : str
            Team to check

        Returns
        -------
        bool
            True if team is playing in game otherwise False

        """
        return team in self._team_to_probability

    @property
    def teams(self):
        """ Names of teams in game

        Yields
        ------
        str
            Next team in game

        """
        yield from self

    def win_probability(self, team):
        """ Find probability a given team wins the game

        Parameters
        ----------
        team : str
            Team to find win probability for

        Returns
        -------
        float
            Win probability

        """
        try:
            return self._team_to_probability[team]
        except KeyError:
            raise ValueError(f'Team {team} is not playing in game {self}')
