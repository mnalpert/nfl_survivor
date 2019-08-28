import logging

from nfl_survivor.picker import Picker
from nfl_survivor.picks import Picks

logger = logging.getLogger(__name__)


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
        picks, already_picked = Picks(), set()

        for week in sorted(self.season.weeks, key=lambda w: w.week_number):
            logger.info('Determing pick for week %s', week.week_number)
            pick = max((team for team in week.teams if team not in already_picked),
                       key=week.team_win_probability, default=None)

            if pick is None:
                exception_msg = (f'Cannot solve for week {week.week_number} since all teams '
                                 'playing this week have been picked already.')
                logger.exception(exception_msg)
                raise ValueError(exception_msg)

            picks[week.week_number] = pick
            already_picked.add(pick)

        return picks
