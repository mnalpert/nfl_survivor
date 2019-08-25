from nfl_survivor.picker import Picker


class GreedyPicker(Picker):

    def picks(self):
        """ Make picks for a particular season using greedy algorithm

        Parameters
        ----------
        season : season.Season
            Season to make picks for

        Returns
        -------
        dict(int->str)
            Week number to team team
        """
        week_to_team, already_picked = dict(), set()

        for week in sorted(self.season.weeks, key=lambda w: w.week_number):
            pick = max((team for team in week.teams if team not in already_picked),
                       key=week.team_win_probability, default=None)

            if pick is None:
                raise ValueError(f'Cannot solve for week {week.week_number} since all teams '
                                 'playing this week have been picked already.')

            week_to_team[week.week_number] = pick
            already_picked.add(pick)

        return week_to_team