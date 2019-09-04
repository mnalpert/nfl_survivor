import logging
import pprint

import click

from nfl_survivor.greedy_picker import GreedyPicker
from nfl_survivor.lp_picker import LpPicker
from nfl_survivor.picks import Picks
from nfl_survivor.season import Season
from nfl_survivor.utils import initialize_logging

logger = logging.getLogger(__name__)

PICKERS = (GreedyPicker, LpPicker)


@click.command()
@click.option('-pp', '--previous_picks', 'previous_picks', type=str, default=None,
              help='File path to YAML file with previous picks')
@click.option('-p', '--picker', 'picker_name', type=str, default='lp',
              help='Name of picker to use when making picks (lp | greedy)')
@click.option('-o', '--output', 'output', type=str, default=None,
              help='YAML file path to write picks to')
@click.option('-s', '--season', 'season_path', type=str,
              help='File path to season YAML')
@initialize_logging()
def make_picks(season_path, output, picker_name, previous_picks):
    """Make picks for a given season and set of previous picks"""
    season = Season.from_yaml(season_path)
    previous_picks = Picks.from_yaml(previous_picks) if previous_picks else None
    try:
        picker = {picker.__name__.lower(): picker
                  for picker in PICKERS}[picker_name.lower() + 'picker']
    except KeyError:
        exception_msg = f'No picker matching {picker_name}'
        logger.exception(exception_msg)
        raise ValueError(exception_msg)

    picks = picker(season, previous_picks).picks()

    if output is not None:
        picks.to_yaml(output)
    else:
        pprint.pprint(picks.yaml_dict())
