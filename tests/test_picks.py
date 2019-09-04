import tempfile

import pytest

from nfl_survivor.picks import Picks


@pytest.fixture
def invalid_picks():
    return Picks(((1, 'a'), (2, 'a')))


@pytest.mark.usefixtures('picks', 'invalid_picks')
class TestPicks:

    def test_yaml_dict(self, picks):
        assert picks.yaml_dict() == [{'week': {'number': 1,
                                               'pick': 'a'}},
                                     {'week': {'number': 2,
                                               'pick': 'c'}}]

    def test_from_list(self, picks):
        assert Picks.from_list([{'week': {'number': 1,
                                          'pick': 'a'}},
                                {'week': {'number': 2,
                                          'pick': 'c'}}]) == picks

    def test_from_to_yaml(self, picks):
        with tempfile.NamedTemporaryFile('wt') as tmp_file:
            picks.to_yaml(tmp_file.name)

            assert Picks.from_yaml(tmp_file.name) == picks

    def test_invalid_picks(self, invalid_picks):
        with tempfile.NamedTemporaryFile('wt') as tmp_file:
            invalid_picks.to_yaml(tmp_file.name)

            with pytest.raises(ValueError) as exception:
                Picks.from_yaml(tmp_file.name)

        assert 'invalid picks' in str(exception.value).lower()
