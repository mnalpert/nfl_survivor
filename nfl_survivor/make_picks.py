import click

from nfl_survivor.greedy_picker import GreedyPicker
from nfl_survivor.lp_picker import LpPicker
from nfl_survivor.picks import Picks
from nfl_survivor.season import Season
from nfl_survivor.utils import initialize_logging

PICKERS = (GreedyPicker, LpPicker)


@click.command()
@click.option('-pp', '--previous_picks', 'previous_picks', type=str)
@click.option('-p', '--picker', 'picker_name', type=str, default='LpPicker')
@click.option('-o', '--output', 'output', type=str)
@click.option('-s', '--season', 'season_path', type=str)
def make_picks(season_path, output, picker_name, previous_picks):
    initialize_logging()

    season = Season.from_yaml(season_path)
    previous_picks = Picks.from_yaml(previous_picks) if previous_picks else None
    picker = {picker.__name__.lower(): picker
              for picker in PICKERS}[picker_name.lower()]

    picks = picker(season, previous_picks).picks()
    picks.to_yaml(output)


if __name__ == '__main__':
    make_picks()
