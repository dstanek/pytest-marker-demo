"""Order API clients.

Different classes that simulate talking to different versions of an API.
"""

from typing import Any

from tests.lib.version import Version, registry


@registry.register("order_api", Version.from_string("v5"))
class OrdersV5:
    def get_by_customer(self, id: str) -> list[dict[str, Any]]:
        return [
            {
                "id": f"{id}-order",
                "customer_id": id,
                "description": "Some order places",
                "item_count": 2,
            }
        ]


@registry.register("order_api", Version.from_string("v6beta1"))
class OrdersV6beta1:
    def get_by_customer(self, id: str) -> list[dict[str, Any]]:
        return [
            {
                "id": f"{id}-order",
                "customer_id": id,
                "description": "Some order places",
                "items": [
                    "widget",
                    "what's it called",
                ],
            }
        ]
