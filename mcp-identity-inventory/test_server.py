"""Basic tests for the identity inventory."""

import pytest

from server import (
    find_inactive_identities,
    get_identity,
    list_identities,
)


def test_list_identities() -> None:
    identities = list_identities()

    assert len(identities) == 3


def test_get_identity() -> None:
    identity = get_identity("user-001")

    assert identity.name == "Bob"


def test_unknown_identity() -> None:
    with pytest.raises(ValueError, match="Identity not found"):
        get_identity("missing")


def test_invalid_days() -> None:
    with pytest.raises(ValueError, match="days must be at least 1"):
        find_inactive_identities(0)
