import re
from collections import defaultdict
from dataclasses import dataclass
from typing import Any, Callable, Type, TypeVar

T = TypeVar("T")


class DuplicateRegistrationError(Exception):
    """Used for duplicate registration errors."""

    def __init__(self, fixture_name: str, version: "Version") -> None:
        super().__init__(f"Duplicate registration for {fixture_name}:{version}")


class NoVersionsFound(Exception):
    """Used when no versions are found for a givent fixture name."""

    def __init__(self, fixture_name: str) -> None:
        super().__init__(f"No versions for for {fixture_name!r}")


class Registry:
    def __init__(self) -> None:
        self._registry: dict[str, dict["Version", Any]] = defaultdict(dict)

    def register(
        self, fixture_name: str, api_version: "Version"
    ) -> Callable[[Type[T]], Type[T]]:
        def _wrapper(cls: Type[T]) -> Type[T]:
            setattr(cls, "__demo_fixture_name__", fixture_name)
            setattr(cls, "__demo_api_version__", api_version)
            try:
                self._registry[fixture_name][api_version]
                raise DuplicateRegistrationError(fixture_name, api_version)
            except KeyError:
                self._registry[fixture_name][api_version] = cls
            return cls

        return _wrapper

    def available_fixtures(self) -> set[str]:
        return set(self._registry)

    def lookup(self, fixture_name: str, version: "Version") -> Any:
        try:
            return self._registry[fixture_name][version]
        except KeyError:
            raise NoVersionsFound(f"{fixture_name}:{version}")

    def available_versions(self, fixture_name: str) -> set["Version"]:
        versions = set(self._registry[fixture_name])
        if not versions:
            raise NoVersionsFound(fixture_name)
        return versions


registry = Registry()


class VersionError(Exception):
    """Invalid version provided"""


@dataclass
class Version:
    _regex = re.compile(
        "^v"
        r"((?P<major>[0-9]+)(?:\.(?P<minor>[0-9]+))?)(?:\.(?P<patch>[\d]+))?"
        r"(?:(?P<tag>alpha|beta)(?P<tag_version>\d+))?"
        "$"
    )

    major: int
    minor: int | None = None
    patch: int | None = None
    tag: str | None = None
    tag_version: int | None = None

    @classmethod
    def from_string(cls, value: str) -> "Version":
        m = Version._regex.match(value)
        if not m:
            raise VersionError()

        data = m.groupdict()
        return cls(
            major=int(data["major"]),
            minor=int(data["minor"]) if data["minor"] is not None else None,
            patch=int(data["patch"]) if data["patch"] is not None else None,
            tag=data["tag"] if data["tag"] is not None else None,
            tag_version=int(data["tag_version"])
            if data["tag_version"] is not None
            else None,
        )

    def _values(self) -> tuple[int, int, int, str, int]:
        return (
            self.major,
            self.minor if self.minor is not None else -1,
            self.patch if self.patch is not None else -1,
            self.tag or "zzz",
            self.tag_version if self.tag_version is not None else -1,
        )

    def __str__(self) -> str:
        parts = [f"v{self.major}"]
        if self.minor:
            parts.append(f".{self.minor}")
        if self.patch:
            parts.append(f".{self.patch}")
        if self.tag:
            parts.append(self.tag)
        if self.tag_version:
            parts.append(str(self.tag_version))
        return "".join(parts)

    def __lt__(self, other: "Version") -> bool:
        return self._values() < other._values()

    def __hash__(self) -> int:
        return hash(self._values())

    def __eq__(self, other: object) -> bool:
        return self.__hash__() == other.__hash__()
