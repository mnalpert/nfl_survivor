import mock

import pulp
import pytest

from nfl_survivor.lp_picker import LpPicker


@pytest.fixture
@pytest.mark.usefixtures('season', 'picks')
def lp_picker(season, picks):
    return LpPicker(season, picks)


@pytest.fixture
def linear_program():
    return pulp.LpProblem(name='test_problem')


@pytest.mark.usefixtures('lp_picker', 'season', 'linear_program')
class TestTestLpPicker:

    def test_week_team_to_lp_variable(self, lp_picker, season):
        wt_to_lp_var = lp_picker._week_team_to_lp_variable

        assert set(wt_to_lp_var.keys()) == set((week.week_number, team)
                                               for week in season
                                               for team in week.teams)
        for var in wt_to_lp_var.values():
            assert isinstance(var, pulp.LpVariable)
            assert var.isBinary()

    def test_week_constraints(self, lp_picker):
        for wc in lp_picker._week_constraints():
            assert isinstance(wc, pulp.LpConstraint)

            assert wc.sense == pulp.LpConstraintEQ
            assert abs(wc.constant) == 1

        # 3 weeks in season
        assert len(tuple(lp_picker._week_constraints())) == 3

    def test_team_constraints(self, lp_picker, season):
        for tc in lp_picker._team_constraints():
            assert isinstance(tc, pulp.LpConstraint)

            assert tc.sense == pulp.LpConstraintLE
            assert abs(tc.constant) == 1

        assert len(tuple(lp_picker._team_constraints())) == len(season.teams)

    def test_previous_pick_constraints(self, lp_picker, season):
        for ppc in lp_picker._previous_pick_constraints():
            assert isinstance(ppc, pulp.LpConstraint)

            assert ppc.sense == pulp.LpConstraintEQ
            assert abs(ppc.constant) == 1

    def test_max_probability_objective(self, lp_picker):
        obj = lp_picker._max_probability_objective()

        assert isinstance(obj, pulp.LpAffineExpression)

        assert len(obj) == len(lp_picker._week_team_to_lp_variable)

    def test_add_constraints(self, lp_picker, linear_program, season):
        lp_picker._add_constraints(linear_program)

        assert len(linear_program.constraints) == (len(tuple(season.weeks)) +
                                                   len(season.teams) +
                                                   len(lp_picker.previous_picks))

    def test_linear_program(self, lp_picker):
        lp = lp_picker._linear_program()

        assert isinstance(lp, pulp.LpProblem)
        assert lp.sense == pulp.LpMaximize
        assert len(lp.constraints) > 0
        assert len(lp.objective) > 0

    @mock.patch('pulp.LpProblem.solve')
    def test_picks_optimal(self, pulp_solve, lp_picker, season):
        pulp_solve.return_value = pulp.LpStatusOptimal
        for var in lp_picker._week_team_to_lp_variable.values():
            var.varValue = 1

        picks = lp_picker.picks()

        assert all(week.week_number in picks for week in season.weeks)

    @mock.patch('pulp.LpProblem.solve')
    def test_picks_nonoptimal(self, pulp_solve, lp_picker):
        pulp_solve.return_value = pulp.LpStatusInfeasible

        picks = lp_picker.picks()

        assert picks is None
