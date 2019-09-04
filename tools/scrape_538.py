import logging
import pprint
import re

import click
import requests
from bs4 import BeautifulSoup

from nfl_survivor import utils

logger = logging.getLogger(__name__)

SEASON_URL = 'https://projects.fivethirtyeight.com/{year}-nfl-predictions/games/'


class Scraper:

    def __init__(self, url):
        """ Scraper for probabilities from 538

        Parameters
        ----------
        url : str
            URL of site to be scraped

        """
        self._url = url
        logger.info('Created scraper for %s', self.url)

    @property
    def url(self):
        return self._url

    @staticmethod
    def _team_dict(team_tag):
        """ Form team dictionary

        Parameters
        ----------
        team_tag : bs4.element.Tag

        Returns
        -------
        dict

        """
        return {'team': {'name': team_tag.find('td', class_=re.compile('^td text team')).text.strip(),
                         'probability': int(team_tag.find('td', class_='td number chance').
                                            text.split('%')[0]) / 100}}

    @staticmethod
    def _game_dict(game_tag):
        """ Form game dictionary

        Parameters
        ----------
        game_tag : bs4.element.Tag

        Returns
        -------
        dict

        """
        game = [Scraper._team_dict(team_tag)
                for team_tag in
                game_tag.find('table', class_='game-body').find_all('tr', class_='tr')]

        logger.info('Scraped game between %s and %s', *(team['team']['name'] for team in game))

        return {'game': game}

    @staticmethod
    def _week_dict(week_tag):
        """ Form week dictionary

        Parameters
        ----------
        week_tag : bs4.element.Tag

        Returns
        -------
        dict

        """
        week_number = int(week_tag.h3.text.strip().split()[1])
        logger.info('Scraping games for week %s', week_number)

        return {'number': week_number,
                'games': [Scraper._game_dict(game_tag)
                          for game_tag in week_tag.find_all('div', class_='game')]}

    def _season_dict(self, soup):
        """ Form season dictionary

        Parameters
        ----------
        soup : bs4.BeautifulSoup

        Returns
        -------
        dict

        """
        return [{'week': self._week_dict(week_soup)}
                for week_soup in soup.find_all('section', class_='week')
                if 'Week' in week_soup.h3.text]

    def _site_html(self):
        """ Get plain text site HTML

        Returns
        -------
        str

        """
        logger.info('Fetching content from %s', self.url)
        return requests.get(self.url).text

    def _site_soup(self):
        """ Get structured representation of site HTML

        Returns
        -------
        bs4.BeautifulSoup

        """
        logger.info('Parsing HTML from %s', self.url)
        return BeautifulSoup(self._site_html(), 'html.parser')

    def scraped_season_dict(self):
        """ Season dictionary for URL

        Parameters
        ----------
        url : str

        Returns
        -------
        dict

        """
        try:
            return self._season_dict(self._site_soup())
        except ConnectionError:
            exception_msg = f'Could not connect to {self.url}'
            logger.exception(exception_msg)
            raise ConnectionError(exception_msg)
        except requests.exceptions.RequestException:
            exception_msg = f'Error requesting content from {self.url}'
            logger.exception(exception_msg)
            raise ValueError(exception_msg)
        except Exception:
            exception_msg = f'Error in connecting to, requesting content, and scraping from {self.url}'
            logger.exception(exception_msg)
            raise ValueError(exception_msg)

    def write_season_yaml(self, file_path):
        """ Write season to YAML file

        Parameters
        ----------
        file_path : str
            Path to write YAML output to
        """
        utils.write_yaml(self.scraped_season_dict(), file_path)


@click.command()
@click.option('-o', '--output', 'output', type=str,
              help='YAML file path to write season to')
@click.option('-y', '--year', 'year', type=int,
              help='Year of season to scrape')
@utils.initialize_logging()
def scrape(year, output):
    """Scrape NFL season for a given year with probabilitys from fivethirtyeight.com"""
    scraper = Scraper(SEASON_URL.format(year=year))

    if output:
        scraper.write_season_yaml(output)
        logger.info('Wrote season YAML to %s', output)
    else:
        pprint.pprint(scraper.scraped_season_dict())
