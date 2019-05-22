
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
        self.week_number = week_number
        self.games = games

    def __repr__(self):
        """ Readable representation of week

        Parameters
        ----------
        str

        """
        return f'Week({self.week_number})'

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
        return {team: game
                for game in self.games
                for team in game.teams}

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
            raise ValueError(f'Team {team} is not playing in this week')


    import pdb; pdb.set_trace()
