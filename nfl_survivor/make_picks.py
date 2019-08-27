import click

from nfl_survivor.greedy_picker import GreedyPicker
from nfl_survivor.lp_picker import LpPicker
from nfl_survivor.season import Season
from nfl_survivor.utils import initialize_logging


PICKERS = (GreedyPicker, LpPicker)


@click.command()
@click.option('-p', '--picker', 'picker_name', type=str, default='LpPicker')
@click.option('-o', '--output', 'output', type=str)
@click.option('-s', '--season', 'season_path', type=str)
def make_picks(season_path, output, picker_name):
    initialize_logging()

    season = Season.from_yaml(season_path)
    picker = {picker.__name__.lower(): picker
              for picker in PICKERS}[picker_name.lower()]

    picks = picker(season).picks()
    picks.to_yaml(output)


if __name__ == '__main__':
    make_picks()
