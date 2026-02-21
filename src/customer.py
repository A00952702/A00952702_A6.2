"""
customer.py
Customer entity + persistence operations.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Optional

from src.storage import read_json_list, write_json_list

CUSTOMERS_FILE = "data/customers.json"


@dataclass
class Customer:
    """Represents a customer."""
    customer_id: str
    name: str
    email: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dict for JSON persistence."""
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
        }

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Customer":
        """Create a Customer from a dict."""
        return Customer(
            customer_id=str(data["customer_id"]),
            name=str(data["name"]),
            email=str(data["email"]),
        )


def _load_all() -> list[Customer]:
    items = read_json_list(CUSTOMERS_FILE)
    return [Customer.from_dict(x) for x in items]


def _save_all(customers: list[Customer]) -> None:
    write_json_list(CUSTOMERS_FILE, [c.to_dict() for c in customers])


def create_customer(customer: Customer) -> bool:
    """Create a customer. Returns False if ID already exists."""
    customers = _load_all()
    if any(c.customer_id == customer.customer_id for c in customers):
        print(
            "[Customer] Error: customer_id already exists: "
            f"{customer.customer_id}"
        )
        return False

    if not customer.name.strip():
        print("[Customer] Error: name cannot be empty.")
        return False

    if "@" not in customer.email or not customer.email.strip():
        print("[Customer] Error: invalid email.")
        return False

    customers.append(customer)
    _save_all(customers)
    return True


def delete_customer(customer_id: str) -> bool:
    """Delete customer by ID."""
    customers = _load_all()
    new_list = [c for c in customers if c.customer_id != customer_id]
    if len(new_list) == len(customers):
        print(f"[Customer] Error: customer_id not found: {customer_id}")
        return False
    _save_all(new_list)
    return True


def get_customer(customer_id: str) -> Optional[Customer]:
    """Get customer by ID."""
    customers = _load_all()
    for c in customers:
        if c.customer_id == customer_id:
            return c
    return None


def update_customer(customer_id: str, name: str, email: str) -> bool:
    """Update customer info."""
    customers = _load_all()
    for c in customers:
        if c.customer_id == customer_id:
            if not name.strip():
                print("[Customer] Error: name cannot be empty.")
                return False
            if "@" not in email or not email.strip():
                print("[Customer] Error: invalid email.")
                return False
            c.name = name
            c.email = email
            _save_all(customers)
            return True

    print(f"[Customer] Error: customer_id not found: {customer_id}")
    return False
