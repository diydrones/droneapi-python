import mock
from mock import MagicMock
import droneapi
from droneapi import FakeAPI
from nose.tools import assert_equals

def test_mode():
    api = FakeAPI(MagicMock())
    assert_equals(len(api.get_vehicles()), 1)
