import pytest

from objects.domain import createNewDomain


def test_domain_wrong_hostname():
    with pytest.raises(Exception) as excinfo:
        createNewDomain("-domain")

    assert "contains invalid characters or has a" in str(excinfo.value)
