"""Customer API tests.
"""

from typing import Any
from uuid import UUID

import pytest

# all tests are related to v1
pytestmark = pytest.mark.api_version("customer:v1")


# Not marked for a specific version so it's compatible with *all* known versions
def test_customers_always_have_an_id(
    customer_api_random: Any, customer_id: UUID
) -> None:
    customer = customer_api_random.get(customer_id)
    assert customer_id == customer["id"], "assert customer id is expected"


def test_customers_have_a_name_property(
    customer_api_random: Any, customer_id: UUID
) -> None:
    customer = customer_api_random.get(customer_id)
    assert "name" in customer, "assert customer has a name property"


@pytest.mark.xfail(
    raises=AssertionError
)  # fails because we are using the wrong API version
def test_customers_have_actions_fails(
    customer_api_random: Any, customer_id: UUID
) -> None:
    customer = customer_api_random.get(customer_id)
    assert "actions" in customer, "assert customer has actions"
