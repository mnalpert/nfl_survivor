import logging

import numpy as np
import pulp

from nfl_survivor.utils import cached_property
from nfl_survivor.picker import Picker
from nfl_survivor.picks import Picks

logger = logging.getLogger(__name__)


class LpPicker(Picker):

    def __init__(self, season, previous_picks=None):
        """ Pick maker for a season using linear programming

        Parameters
        ----------
        season : season.Season
            Season to make picks for

        """
        super().__init__(season, previous_picks)

        # constraints to be implemented
        self._constraint_handlers = (self._week_constraints,
                                     self._team_constraints,
                                     self._previous_pick_constraints)

    @cached_property
    def _week_team_to_lp_variable(self):
        """ Map between week and team to LP variable corresponding
        to picking that team in given week. LP variable value of 1
        indicates that pick was made and 0 indicates pick was not made

        Returns
        -------
        dict(tuple(int, str)->pulp.LpVariable)

        """
        return {(week.week_number, team): pulp.LpVariable(name=f'{week.week_number}_{team}',
                                                          cat=pulp.LpBinary)
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
        logger.info('Adding one team per week constraints')
        wt_to_lp_var = self._week_team_to_lp_variable

        for week in self.season:
            logger.info('Adding constraint to pick exactly one team for week %d', week.week_number)
            yield pulp.LpConstraint(e=((wt_to_lp_var[week.week_number, team], 1) for team in week.teams),
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
        logger.info('Adding do not pick same team twice constraints')
        wt_to_lp_var = self._week_team_to_lp_variable

        for team in self.season.teams:
            logger.info('Adding constraint to pick team %s at most once', team)
            yield pulp.LpConstraint(e=((wt_to_lp_var[week.week_number, team], 1)
                                       for week in self.season.team_weeks(team)),
                                    rhs=1,
                                    sense=pulp.LpConstraintLE,
                                    name=f'team_{team}_constraint')

    def _previous_pick_constraints(self):
        """ Constraint ensuring that previous picks are respected

        Yields
        ------
        pulp.LpConstraint
            LpConstraint for a previous pick
        """
        logger.info('Adding previous picks constraints')
        wt_to_lp_var = self._week_team_to_lp_variable

        for week_number, team in self.previous_picks.items():
            logger.info('Add constraint to respect previous picks for week %d, team %s',
                        week_number, team)
            yield pulp.LpConstraint(e=((wt_to_lp_var[week_number, team], 1),),
                                    rhs=1,
                                    sense=pulp.LpConstraintEQ,
                                    name=f'previous_pick_{week_number}_{team}')

    def _max_probability_objective(self):
        """ LP objective for maximizing probability of winning all weeks in season

        Returns
        -------
        pulp.LpAffineExpression

        """
        logger.info('Adding objective to maximize win probability')
        wt_to_lp_var = self._week_team_to_lp_variable

        return pulp.LpAffineExpression(e=((wt_to_lp_var[week.week_number, team],
                                           np.log(game.win_probability(team)))
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
        lp = pulp.LpProblem(name='NFL Survivor', sense=pulp.LpMaximize)

        self._add_constraints(lp)

        self._add_objective(lp)

        return lp

    def picks(self):
        """ Make picks for a particular season using LP

        Parameters
        ----------
        season : season.Season
            Season to make picks for

        Returns
        -------
        dict(int->str)
            Week number to team name. None if LP solve was unsuccessful

        """
        logger.info('Creating linear program to determine picks')
        linear_program = self._linear_program()

        logger.info('Solving linear program')
        status = linear_program.solve()

        logger.info('Linear program status %s', pulp.LpStatus[status])

        logger.info('Forming picks')
        return (Picks(week_team
                      for week_team, var in self._week_team_to_lp_variable.items()
                      if var.varValue == 1) if status == pulp.LpStatusOptimal else None)
