import mock

from nfl_survivor.utils import cached_property


def compute():
    return 1


class C:

    @cached_property
    def cp(self):
        return compute()

    @property
    def rp(self):
        return compute()


@mock.patch('tests.test_utils.compute')
def test_cached_property(mocked_compute):
    mocked_compute.return_value = 1

    c = C()

    # first time we call compute
    assert c.cp == 1
    assert mocked_compute.call_count == 1

    # second time we don't so call count remains 1
    assert c.cp == 1
    assert mocked_compute.call_count == 1


@mock.patch('tests.test_utils.compute')
def test_regular_property(mocked_compute):
    mocked_compute.return_value = 1

    c = C()

    # first time we call compute
    assert c.rp == 1
    assert mocked_compute.call_count == 1

    # second time we don't so call count remains 1
    assert c.rp == 1
    assert mocked_compute.call_count == 2
