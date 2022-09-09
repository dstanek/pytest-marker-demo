"""Customer API tests.
"""

from typing import Any
from uuid import UUID

import pytest


# Not marked for a specific version so it's compatible with *all* known versions
def test_customers_always_have_an_id(customer_api: Any, customer_id: UUID) -> None:
    customer = customer_api.get(customer_id)
    assert customer_id == customer["id"], "assert customer id is expected"


@pytest.mark.api_version("customer_api:v1")
def test_customers_have_a_name_property_x(customer_api: Any, customer_id: UUID) -> None:
    customer = customer_api.get(customer_id)
    assert "name" in customer, "assert customer has a name property"


@pytest.mark.api_version("customer_api:v2alpha1", "customer_api:v2beta1")
def test_customers_have_a_first_and_last_properties(
    customer_api: Any, customer_id: UUID
) -> None:
    customer = customer_api.get(customer_id)
    assert "first" in customer, "assert customer has a first property"
    assert "last" in customer, "assert customer has a last property"


@pytest.mark.xfail(
    raises=AssertionError
)  # fails because we are using the wrong API version
@pytest.mark.api_version("customer_api:v2alpha1")
def test_customers_have_actions_fails(customer_api: Any, customer_id: UUID) -> None:
    customer = customer_api.get(customer_id)
    assert "actions" in customer, "assert customer has actions"


@pytest.mark.api_version("customer_api:v2beta1")
def test_customers_have_actions(customer_api: Any, customer_id: UUID) -> None:
    customer = customer_api.get(customer_id)
    assert "actions" in customer, "assert customer has actions"


@pytest.mark.api_version("customer_api:v2beta1", "order_api:v5")
def test_customers_have_orders(customer_api: Any, order_api: Any) -> None:
    customer = customer_api.get_by_email("test_user@example.com")
    orders = order_api.get_by_customer(customer["id"])
    assert orders[0]["item_count"] == 2


@pytest.mark.api_version("customer_api:v1")
@pytest.mark.api_version("customer_api:v2alpha1")
@pytest.mark.api_version("customer_api:v2beta1")
@pytest.mark.api_version("order_api:v5", "orders:v6beta1")
def test_customers_have_orders_generic(
    customer_api: Any, order_api: Any, customer_id: UUID
) -> None:
    customer = customer_api.get(customer_id)
    orders = order_api.get_by_customer(customer["id"])
    assert orders
