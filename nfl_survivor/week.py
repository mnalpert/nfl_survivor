
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

    @property
    def _team_to_game(self):
        """ Map of team to game for the given week

        Returns
        -------
        dict(str->game.Game)

        """
        try:
            t_to_g = self.__team_to_game
        except AttributeError:
            t_to_g = self.__team_to_game = {team: game
                                            for game in self.games
                                            for team in game}

        return t_to_g

    def team_game(self, team):
        """ Week's game for a team

        Parameters
        ----------
        team : str
            Team to find game for

        Returns
        -------
        game.Game
            Game that team is playing in during week

        """
        try:
            return self._team_to_game[team]
        except KeyError:
            raise ValueError(f'Team {team} is not playing week {self}')
