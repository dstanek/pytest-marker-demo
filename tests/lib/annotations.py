from _pytest.nodes import Node

from tests.lib.version import Version

SupportedVersions = list[tuple[str, Version]]


def get_api_versions(node: Node, name: str | None = None) -> SupportedVersions:
    supported_versions = []
    for mark in node.iter_markers("api_version"):
        for arg in mark.args:
            if name and not arg.startswith(name):
                continue
            fixture_name, version = arg.split(":")
            supported_versions.append((fixture_name, Version.from_string(version)))
    return supported_versions
