import math

import pulp

from nfl_survivor.utils import cached_property


class LpPicker:

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
    def _team_week_to_lp_variable(self):
        """ Map between team and week to LP variable corresponding
        to picking that team in given week. LP variable value of 1
        indicates that pick was made and 0 indicates pick was not made

        Returns
        -------
        dict(tuple(str, int)->pulp.LpVariable)

        """
        return {(team, week.week_number): pulp.LpVariable(name=f'{team}_{week.week_number}',
                                                          cat=pulp.constants.LpBinary)
                for week in self.season
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

        Yields
        ------
        pulp.LpConstraint
            LP constraint for next week

        """
        tw_to_lp_var = self._team_week_to_lp_variable

        for week in self.season:
            yield pulp.LpConstraint(e=((tw_to_lp_var[team, week.week_number], 1) for team in week.teams),
                                    rhs=1,
                                    sense=pulp.LpConstraintEQ,
                                    name=f'week_{week.week_number}_constraint')

    def _team_constraints(self):
        """ Constraint of not picking a given team more than once per season

        Yields
        ------
        pulp.LpConstraint
            LP constraint for next team

        """
        tw_to_lp_var = self._team_week_to_lp_variable

        for team in self.season.teams:
            yield pulp.LpConstraint(e=((tw_to_lp_var[team, week.week_number], 1)
                                       for week in self.season.team_weeks(team)),
                                    rhs=1,
                                    sense=pulp.LpConstraintLE,
                                    name=f'team_{team}_constraint')

    def _max_probability_objective(self):
        """ LP objective for maximizing probability of winning all weeks in season

        Returns
        -------
        pulp.LpAffineExpression

        """
        tw_to_lp_var = self._team_week_to_lp_variable

        return pulp.LpAffineExpression(e=((tw_to_lp_var[team, week.week_number],
                                           math.log(game.win_probability(team)))
                                          for week in self.season
                                          for game in week
                                          for team in game))

    def _add_objective(self, lp):
        """ Add objective of maximizing win probability

        Returns
        -------
        None
            Modifies the linear program in place
        """
        lp.objective = self._max_probability_objective()

    def _linear_program(self):
        """ Linear program given by season

        Returns
        -------
        pulp.LpProblem

        """
        lp = pulp.LpProblem(name='NFL Picker', sense=pulp.LpMaximize)

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

        status = linear_program.solve()

        return status, ({week_number: team
                         for (team, week_number), var in self._team_week_to_lp_variable.items()
                         if var.varValue == 1} if status == pulp.LpStatusOptimal else {})
