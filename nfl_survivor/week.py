from nfl_survivor.game import Game
from nfl_survivor.utils import cached_property


class Week:

    def __init__(self, week_number, games):
        """ One week's worth of games

        Parameters
        ----------
        week_number : int
            Identifier of week
        games : iterable(game.Game)
            Games to be played in week

        """
        self._week_number = week_number
        self._games = tuple(games)

    @property
    def week_number(self):
        """ Week number

        Returns
        -------
        int

        """
        return self._week_number

    @property
    def games(self):
        """ Games taking place during week

        Returns
        -------
        tuple(game.Game)

        """
        return self._games

    def __iter__(self):
        """ Iterate through games of week

        Yields
        ------
        game.Game
            Next game of the week

        """
        yield from self.games

    @cached_property
    def _team_to_game(self):
        """ Map of team to game for the given week

        Returns
        -------
        dict(str->game.Game)

        """
        return {team: game
                for game in self
                for team in game}

    def team_game(self, team):
        """ Week's game for a team

        If a team is not playing in the week this returns None

        Parameters
        ----------
        team : str
            Team to find game for

        Returns
        -------
        game.Game
            Game that team is playing in during week

        """
        return self._team_to_game.get(team)

    def team_win_probability(self, team):
        """ Probability that team wins this week

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
            return self.team_game(team).win_probability(team)
        except AttributeError:
            raise ValueError(f'Team {team} is not playing in week {self.week_number}')

    @property
    def teams(self):
        """ All teams playing in the week

        Yields
        ------
        str
            Next team playing

        """
        yield from self._team_to_game.keys()

    @classmethod
    def from_dict(cls, week_dict):
        """ Form week from dictionary representation

        Parameters
        ----------
        week_dict : dict

        Returns
        -------
        week.Week

        """
        return cls(week_dict['number'], (Game.from_dict(game_dict)
                                         for game_dict in week_dict['games']))
