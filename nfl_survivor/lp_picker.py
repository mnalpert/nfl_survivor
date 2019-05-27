import pulp


class LPPicker:

    def _linear_program(self, season):
        """ Linear program given by season

        Parameters
        ----------
        season : season.Season
            Season to form linear program for

        Returns
        -------
        pulp.LpProblem

        """
        lp = pulp.LpProblem(sense='Maximize')

        for team_constraint in self._team_constraints(season):
            lp.addConstraint(team_constraint)

        for week_constraint in self._week_constraints(season):
            lp.addConstraint(week_constraint)

        lp.objective = self._probability_objective(season)

        return lp

    def picks(self, season):
        """ Make picks for a particular season

        Parameters
        ----------
        season : season.Season
            Season to make picks for

        Returns
        -------
        dict(int->str)
            Week number to team name

        """
        linear_program = self._linear_program(season)

        status, solution = linear_program.solve()
