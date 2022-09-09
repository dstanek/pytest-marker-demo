import glob
import random
import uuid
from collections import defaultdict
from itertools import product
from typing import Any, cast

import pytest
from _pytest.config.argparsing import Parser
from _pytest.fixtures import FixtureRequest
from _pytest.python import Metafunc

from .lib.annotations import get_api_versions
from .lib.version import Version, registry

# Dynamically load all fixtures
pytest_plugins = [
    fn[:-3].replace("/", ".")
    for fn in glob.glob("tests/fixtures/**/[!_]*.py", recursive=True)
]


VersionMapT = dict[str, set[Version]]


@pytest.fixture
def customer_id() -> str:
    return uuid.uuid4().hex


@pytest.fixture
def customer_api_random(request: FixtureRequest) -> Any:
    versions = [
        version for name, version in get_api_versions(request.node, "customer_api")
    ]
    if not versions:
        versions = [Version(major=1)]
    selected_version = random.choice(versions)  # select any supported version
    return registry.lookup("customer_api", selected_version)()


#
# <plugin stuff>
#

test_id_gen = (
    lambda instance: f"{instance.__demo_fixture_name__}:{instance.__demo_api_version__}"
)


def only_latest(version_map: VersionMapT) -> VersionMapT:
    for name, versions in version_map.items():
        selected_version = sorted(versions)[-1]
        version_map[name] = {selected_version}
    return version_map


def pick_at_random(version_map: VersionMapT) -> VersionMapT:
    for name, versions in version_map.items():
        selected_version = random.choice(list(versions))  # select any supported version
        version_map[name] = {selected_version}
    return version_map


def pytest_addoption(parser: Parser) -> None:
    parser.addoption(
        "--demo-strategy", choices=["latest", "random", "cartesian"], default="latest"
    )


def pytest_generate_tests(metafunc: Metafunc) -> None:
    version_map: VersionMapT = defaultdict(set)  # api name: [version, ...]

    # collect all supported versions annotated using a mark
    for name, version in get_api_versions(metafunc.definition):
        # The following conditional allows us to use both the parametrize
        # and custom fixtues at the same time.
        if name in metafunc.fixturenames:
            version_map[name].add(version)

    # set the default versions so *all* for known fixutes that have
    # no annotations
    for name in metafunc.fixturenames:
        if name in registry.available_fixtures() and not version_map[name]:
            version_map[name] = registry.available_versions(name)

    if not version_map:
        return

    match metafunc.config.option.demo_strategy:
        case "latest":
            version_map = only_latest(version_map)
        case "random":
            version_map = pick_at_random(version_map)
        case "cartesian":
            "We've collected all annotated versions. No need to filter."

    argnames0, argvalues0 = zip(*version_map.items())
    argnames = []
    argvalues = []
    for name, versions in version_map.items():
        argnames.append(name)
        # resolve fixtures
        argvalues.append([registry.lookup(name, v)() for v in versions])

    if len(argvalues) == 1:
        argvalues = argvalues[0]
    elif len(argvalues) > 1:
        argvalues = cast(list[list[Any]], product(*argvalues))
    metafunc.parametrize(",".join(argnames), argvalues, ids=test_id_gen)


#
# </plugin stuff>
#

# TODO: in verbose mode can we print out the marker used?
