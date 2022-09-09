"""Customer API clients.

Different classes that simulate talking to different versions of an API.
"""

from typing import Any

from tests.lib.version import Version, registry


@registry.register("customer_api", Version.from_string("v1"))
class CustomerV1:
    def get(self, id: str) -> dict[str, Any]:
        return {
            "id": id,
            "name": "Test User",
            "email": "test_user@example.com",
        }


@registry.register("customer_api", Version.from_string("v2alpha1"))
class CustomerV2Alpha1:
    def get(self, id: str) -> dict[str, Any]:
        return {
            "id": id,
            "first": "Test",
            "last": "User",
            "email": "test_user@example.com",
        }


@registry.register("customer_api", Version.from_string("v2beta1"))
class CustomerV2Beta1:
    def get(self, id: str) -> dict[str, Any]:
        return {
            "id": id,
            "first": "Test",
            "last": "User",
            "email": "test_user@example.com",
            "actions": {
                "log_hours": f"https://localhost/{id}/log_hours",
            },
        }

    def get_by_email(self, email: str) -> dict[str, Any]:
        return self.get(email)
