import pulp

from nfl_survivor.utils import cached_property


class LPPicker:

    def __init__(self, season):
        """ Pick maker for a season

        Parameters
        ----------
        season : season.Season
            Season to make picks for

        """
        self._season = season

        # constraints to be implemented
        self._constraint_handlers = (self._week_constraints,
                                     self._team_constraints)

    @property
    def season(self):
        """ Getter for season

        Returns
        -------
        season.Season

        """
        return self._season

    @cached_property
    def _week_team_to_linear_variable(self):
        """

        Parameters
        ----------

        Returns
        -------
        """
        return {(week.week_number, team): pulp.LpVariable(name=f'{week.week_number}_{team}',
                                                          cat=pulp.constants.LpBinary)
                for week in self
                for team in week.teams}

    def _add_constraints(self, lp):
        """ Add constraints to linear program

        Parameters
        ----------
        lp : pulp.LpProblem

        Returns
        -------
        None
            Modifies the linear program in place

        """
        for constraint_handler in self._constraint_handlers:
            for constraint in constraint_handler():
                lp.addConstraint(constraint)

    def _week_constraints(self):
        """ Constraint of picking exactly one team per week

        Returns
        -------
        iterable(pulp.LpConstraint)
            LP constraints indicating that exactly one team must be picked per week

        """
        pass

    def _team_constraints(self):
        """ Constraint of not picking a given team more than once per season

        Returns
        -------
        iterable(pulp.LpConstraint)
            LP constraints indicating that teams cannot be picked more than once a season

        """
        pass

    def _add_objective(self, lp):
        """ Add objective of maximizing win probability

        Returns
        -------
        None
            Modifies the linear program in place
        """
        pass

    def _linear_program(self):
        """ Linear program given by season

        Returns
        -------
        pulp.LpProblem

        """
        lp = pulp.LpProblem(sense='Maximize')

        self._add_constraints(lp)

        self._add_objective(lp)

        return lp

    def picks(self):
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
        linear_program = self._linear_program()

        status, solution = linear_program.solve()
