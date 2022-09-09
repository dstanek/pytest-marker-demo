"""Customer API tests.
"""

from typing import Any
from uuid import UUID

import pytest

# all tests are related to v2beta1
pytestmark = pytest.mark.api_version("customer_api:v2beta1")


# Not marked for a specific version so it's compatible with *all* known versions
def test_customers_always_have_an_id(customer_api: Any, customer_id: UUID) -> None:
    customer = customer_api.get(customer_id)
    assert customer_id == customer["id"], "assert customer id is expected"


def test_customers_have_a_first_and_last_properties(
    customer_api: Any, customer_id: UUID
) -> None:
    customer = customer_api.get(customer_id)
    assert "first" in customer, "assert customer has a first property"
    assert "last" in customer, "assert customer has a last property"


def test_customers_have_actions(customer_api: Any, customer_id: UUID) -> None:
    customer = customer_api.get(customer_id)
    assert "actions" in customer, "assert customer has actions"
