import yaml

from nfl_survivor.utils import write_yaml


class Picks(dict):

    def yaml_dict(self):
        """ Convert mapping of week number to picks to YAML style dictionary

        Returns
        -------
        dict

        """
        return [{'week': {'number': week_number,
                          'pick': pick}}
                for week_number, pick in sorted(self.items())]

    @classmethod
    def from_list(cls, list_):
        """ Create map from week number to team from list of dictionarys

        Parameters
        ----------
        list_ : list(dict)

        Returns
        -------
        Picks

        """
        return cls((week['week']['number'], week['week']['pick']) for week in list_)

    @classmethod
    def from_yaml(cls, yaml_file_path):
        """ Create map from week number to team from YAML file

        Parameters
        ----------
        yaml_file_path : str

        Returns
        -------
        Picks

        """
        with open(yaml_file_path, 'r') as yaml_file:
            return cls.from_list(yaml.load(yaml_file, Loader=yaml.Loader))

    def to_yaml(self, file_path):
        """ Write down picks to file

        Parameters
        ----------
        file_path : str
            Path to write picks to

        """
        write_yaml(self.yaml_dict(), file_path)
