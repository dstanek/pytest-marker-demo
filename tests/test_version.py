import operator
from typing import Callable

import pytest

from tests.lib.version import Version, VersionError


@pytest.mark.parametrize(
    "version_str,expected_version",
    (
        ("v1", Version(major=1)),
        ("v73", Version(major=73)),
        ("v7.1", Version(major=7, minor=1)),
        ("v7.1alpha2", Version(major=7, minor=1, tag="alpha", tag_version=2)),
        ("v1.1.5", Version(major=1, minor=1, patch=5)),
        (
            "v99.66.33beta27",
            Version(major=99, minor=66, patch=33, tag="beta", tag_version=27),
        ),
    ),
)
def test_valid_versions(version_str: str, expected_version: Version) -> None:
    observed_version = Version.from_string(version_str)
    assert observed_version == expected_version


@pytest.mark.parametrize(
    "version_str",
    (
        "1",
        "vx",
        "v1theta4",
        "v2alpha",
    ),
)
def test_invalid_versions(version_str: str) -> None:
    with pytest.raises(VersionError):
        Version.from_string(version_str)


@pytest.mark.parametrize(
    "v0,op,v1",
    (
        (Version(major=1), operator.eq, Version(major=1)),
        (Version(major=2), operator.gt, Version(major=1)),
        (Version(major=1), operator.lt, Version(major=2)),
        (Version(major=1, minor=1), operator.gt, Version(major=1)),
        (Version(major=1, minor=1, patch=1), operator.gt, Version(major=1, minor=1)),
        (
            Version(major=1, minor=1),
            operator.gt,
            Version(major=1, minor=1, tag="alpha", tag_version=1),
        ),
        (
            Version(major=1),
            operator.lt,
            Version(major=2, tag="alpha", tag_version=1),
        ),
        (
            Version(major=1, tag="beta", tag_version=1),
            operator.gt,
            Version(major=1, tag="alpha", tag_version=1),
        ),
        (
            Version(major=1, tag="beta", tag_version=2),
            operator.gt,
            Version(major=1, tag="beta", tag_version=1),
        ),
    ),
)
def test_sorting(
    v0: Version, op: Callable[[Version, Version], bool], v1: Version
) -> None:
    assert op(v0, v1)
