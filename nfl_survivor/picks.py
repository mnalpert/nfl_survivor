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

    def to_yaml(self, file_path):
        """ Write down picks to file

        Parameters
        ----------
        file_path : str
            Path to write picks to

        """
        write_yaml(self.yaml_dict(), file_path)
