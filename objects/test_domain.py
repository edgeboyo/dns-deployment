import pytest

from objects.domain import createNewDomain
from objects.records import checkIfIP


def test_domain_wrong_hostname():
    with pytest.raises(Exception) as excinfo:
        createNewDomain("-domain")

    assert "contains invalid characters or has a" in str(excinfo.value)


def test_IP_Validator():

    assert checkIfIP('127.0.0.1')

    assert not checkIfIP('127.0.0.1', "IPv6")

    assert not checkIfIP('0.0.0.0')

    assert not checkIfIP('0:0::0:0:0', "IPv6")

    assert checkIfIP('7416:33f4:5f43:0b2d:745f:80d2:afe9:dfca', "IPv6")
