# Domain Layer Patterns

The domain layer is the **heart of your application**. It contains business logic, rules, and entities. This layer should be **pure Python** with no dependencies on frameworks, databases, or external libraries.

## Entities

Entities are objects with a unique identity that persists over time.

### Using Dataclasses

```python
# domain/entities.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID, uuid4


@dataclass
class Customer:
    """Domain entity representing a customer."""
    id: UUID
    name: str
    email: str
    created_at: datetime
    is_active: bool = True
    orders: List["Order"] = field(default_factory=list)
    
    @staticmethod
    def create(name: str, email: str) -> "Customer":
        """Factory method to create a new customer."""
        if not name.strip():
            raise ValueError("Customer name cannot be empty")
        
        if not email or "@" not in email:
            raise ValueError("Invalid email address")
        
        return Customer(
            id=uuid4(),
            name=name,
            email=email,
            created_at=datetime.now(),
        )
    
    def deactivate(self) -> None:
        """Deactivate the customer account."""
        if not self.is_active:
            raise ValueError("Customer is already inactive")
        
        self.is_active = False
    
    def add_order(self, order: "Order") -> None:
        """Add an order to the customer."""
        if not self.is_active:
            raise ValueError("Cannot add order to inactive customer")
        
        self.orders.append(order)
    
    def total_spent(self) -> float:
        """Calculate total amount spent by customer."""
        return sum(order.total_amount for order in self.orders)
```

### Entity Validation

Keep validation logic in the entity:

```python
@dataclass
class Product:
    """Domain entity representing a product."""
    id: UUID
    name: str
    description: str
    price: float
    stock_quantity: int
    
    def __post_init__(self):
        """Validate entity after initialization."""
        self._validate()
    
    def _validate(self) -> None:
        """Validate business rules."""
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        
        if self.stock_quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        
        if len(self.name) < 3:
            raise ValueError("Product name must be at least 3 characters")
    
    def update_price(self, new_price: float) -> None:
        """Update product price with validation."""
        if new_price < 0:
            raise ValueError("Price cannot be negative")
        
        if new_price == 0:
            raise ValueError("Price cannot be zero")
        
        self.price = new_price
    
    def reduce_stock(self, quantity: int) -> None:
        """Reduce stock quantity."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        if self.stock_quantity < quantity:
            raise ValueError(
                f"Insufficient stock. Available: {self.stock_quantity}, "
                f"Requested: {quantity}"
            )
        
        self.stock_quantity -= quantity
    
    def restock(self, quantity: int) -> None:
        """Add stock quantity."""
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        self.stock_quantity += quantity
```

## Value Objects

Value objects are **immutable** objects defined by their attributes, not by identity. Two value objects with the same attributes are considered equal.

### Money Value Object

```python
# domain/value_objects.py
from dataclasses import dataclass
from enum import Enum


class Currency(str, Enum):
    """Supported currencies."""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"


@dataclass(frozen=True)
class Money:
    """Value object representing money."""
    amount: float
    currency: Currency
    
    def __post_init__(self):
        """Validate money value."""
        if self.amount < 0:
            raise ValueError("Money amount cannot be negative")
        
        # Round to 2 decimal places
        object.__setattr__(self, "amount", round(self.amount, 2))
    
    def add(self, other: "Money") -> "Money":
        """Add two money values."""
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot add different currencies: {self.currency} and {other.currency}"
            )
        
        return Money(self.amount + other.amount, self.currency)
    
    def subtract(self, other: "Money") -> "Money":
        """Subtract money values."""
        if self.currency != other.currency:
            raise ValueError(
                f"Cannot subtract different currencies: {self.currency} and {other.currency}"
            )
        
        result = self.amount - other.amount
        if result < 0:
            raise ValueError("Result cannot be negative")
        
        return Money(result, self.currency)
    
    def multiply(self, factor: float) -> "Money":
        """Multiply money by a factor."""
        if factor < 0:
            raise ValueError("Factor cannot be negative")
        
        return Money(self.amount * factor, self.currency)
    
    def __str__(self) -> str:
        """String representation."""
        return f"{self.currency.value} {self.amount:.2f}"
```

### Email Value Object

```python
import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Email:
    """Value object representing an email address."""
    value: str
    
    def __post_init__(self):
        """Validate email format."""
        if not self._is_valid_email(self.value):
            raise ValueError(f"Invalid email address: {self.value}")
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        """Check if email format is valid."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def domain(self) -> str:
        """Get email domain."""
        return self.value.split("@")[1]
    
    def __str__(self) -> str:
        return self.value


# Usage in entity
@dataclass
class User:
    id: UUID
    name: str
    email: Email  # Using value object instead of str
    
    @staticmethod
    def create(name: str, email_address: str) -> "User":
        """Create user with validated email."""
        email = Email(email_address)  # Validation happens here
        return User(
            id=uuid4(),
            name=name,
            email=email,
        )
```

### Address Value Object

```python
@dataclass(frozen=True)
class Address:
    """Value object representing a physical address."""
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    
    def __post_init__(self):
        """Validate address components."""
        if not all([self.street, self.city, self.state, self.postal_code, self.country]):
            raise ValueError("All address fields are required")
        
        if len(self.postal_code) < 3:
            raise ValueError("Invalid postal code")
    
    def is_same_city(self, other: "Address") -> bool:
        """Check if two addresses are in the same city."""
        return (
            self.city.lower() == other.city.lower() and
            self.country.lower() == other.country.lower()
        )
    
    def __str__(self) -> str:
        """Format address as string."""
        return (
            f"{self.street}, {self.city}, "
            f"{self.state} {self.postal_code}, {self.country}"
        )
```

## Domain Services

Domain services contain business logic that doesn't naturally fit into a single entity. Use them when:

- Logic involves multiple entities
- Logic is a significant business process
- Logic doesn't belong to any particular entity

### Pricing Service

```python
# domain/services.py
from domain.entities import Order, Customer
from domain.value_objects import Money


class PricingService:
    """Domain service for pricing calculations."""
    
    def calculate_order_total(self, order: Order) -> Money:
        """Calculate total price for an order including discounts and taxes."""
        subtotal = sum(
            item.price.multiply(item.quantity)
            for item in order.items
        )
        
        # Apply customer discount if applicable
        if order.customer.is_vip:
            discount = self._calculate_vip_discount(subtotal)
            subtotal = subtotal.subtract(discount)
        
        # Add tax
        tax = self._calculate_tax(subtotal)
        total = subtotal.add(tax)
        
        return total
    
    def _calculate_vip_discount(self, amount: Money) -> Money:
        """Calculate VIP customer discount (10%)."""
        return amount.multiply(0.10)
    
    def _calculate_tax(self, amount: Money) -> Money:
        """Calculate tax (8%)."""
        return amount.multiply(0.08)


class ShippingService:
    """Domain service for shipping calculations."""
    
    def calculate_shipping_cost(
        self,
        origin: Address,
        destination: Address,
        weight_kg: float,
    ) -> Money:
        """Calculate shipping cost based on distance and weight."""
        if weight_kg <= 0:
            raise ValueError("Weight must be positive")
        
        # Base rate
        base_rate = Money(5.0, Currency.USD)
        
        # Same city shipping
        if origin.is_same_city(destination):
            return base_rate
        
        # Domestic shipping
        if origin.country == destination.country:
            weight_charge = Money(weight_kg * 2.0, Currency.USD)
            return base_rate.add(weight_charge)
        
        # International shipping
        weight_charge = Money(weight_kg * 5.0, Currency.USD)
        international_fee = Money(20.0, Currency.USD)
        
        return base_rate.add(weight_charge).add(international_fee)
```

### Inventory Service

```python
class InventoryService:
    """Domain service for inventory management."""
    
    def is_available(self, product: Product, requested_quantity: int) -> bool:
        """Check if product is available in requested quantity."""
        return product.stock_quantity >= requested_quantity
    
    def reserve_stock(self, product: Product, quantity: int) -> None:
        """Reserve stock for an order."""
        if not self.is_available(product, quantity):
            raise ValueError(
                f"Cannot reserve {quantity} units of {product.name}. "
                f"Only {product.stock_quantity} available."
            )
        
        product.reduce_stock(quantity)
    
    def release_stock(self, product: Product, quantity: int) -> None:
        """Release reserved stock (e.g., when order is cancelled)."""
        product.restock(quantity)
    
    def needs_reorder(self, product: Product, threshold: int = 10) -> bool:
        """Check if product needs to be reordered."""
        return product.stock_quantity <= threshold
```

## Domain Exceptions

Create specific exceptions for domain errors:

```python
# domain/exceptions.py
class DomainException(Exception):
    """Base exception for domain errors."""
    pass


class EntityNotFoundException(DomainException):
    """Raised when an entity is not found."""
    
    def __init__(self, entity_type: str, entity_id: str):
        self.entity_type = entity_type
        self.entity_id = entity_id
        super().__init__(f"{entity_type} with ID {entity_id} not found")


class InsufficientStockException(DomainException):
    """Raised when there's insufficient stock."""
    
    def __init__(self, product_name: str, available: int, requested: int):
        self.product_name = product_name
        self.available = available
        self.requested = requested
        super().__init__(
            f"Insufficient stock for {product_name}. "
            f"Available: {available}, Requested: {requested}"
        )


class InvalidOperationException(DomainException):
    """Raised when an operation is not allowed in the current state."""
    pass


class BusinessRuleViolationException(DomainException):
    """Raised when a business rule is violated."""
    pass


# Usage in entities
class Order:
    def cancel(self) -> None:
        """Cancel the order."""
        if self.status in ["shipped", "delivered"]:
            raise InvalidOperationException(
                f"Cannot cancel order with status: {self.status}"
            )
        
        self.status = "cancelled"
```

## Aggregates

An aggregate is a cluster of entities and value objects with a clear boundary and a root entity.

### Order Aggregate

```python
from dataclasses import dataclass, field
from typing import List


@dataclass
class OrderItem:
    """Value object representing an item in an order."""
    product_id: UUID
    product_name: str
    quantity: int
    unit_price: Money
    
    def line_total(self) -> Money:
        """Calculate line item total."""
        return self.unit_price.multiply(self.quantity)


@dataclass
class Order:
    """Order aggregate root."""
    id: UUID
    customer_id: UUID
    items: List[OrderItem] = field(default_factory=list)
    status: str = "pending"
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_item(self, item: OrderItem) -> None:
        """Add item to order."""
        if self.status != "pending":
            raise InvalidOperationException(
                "Cannot modify order that is not pending"
            )
        
        if item.quantity <= 0:
            raise ValueError("Item quantity must be positive")
        
        # Check if item already exists
        existing = self._find_item(item.product_id)
        if existing:
            existing.quantity += item.quantity
        else:
            self.items.append(item)
    
    def remove_item(self, product_id: UUID) -> None:
        """Remove item from order."""
        if self.status != "pending":
            raise InvalidOperationException(
                "Cannot modify order that is not pending"
            )
        
        self.items = [item for item in self.items if item.product_id != product_id]
    
    def calculate_total(self) -> Money:
        """Calculate order total."""
        if not self.items:
            return Money(0, Currency.USD)
        
        return sum(
            (item.line_total() for item in self.items),
            start=Money(0, self.items[0].unit_price.currency),
        )
    
    def submit(self) -> None:
        """Submit order for processing."""
        if not self.items:
            raise BusinessRuleViolationException("Cannot submit empty order")
        
        if self.status != "pending":
            raise InvalidOperationException("Order already submitted")
        
        self.status = "submitted"
    
    def _find_item(self, product_id: UUID) -> Optional[OrderItem]:
        """Find item by product ID."""
        return next(
            (item for item in self.items if item.product_id == product_id),
            None,
        )
```

## Domain Events

Domain events represent something significant that happened in the domain:

```python
# domain/events.py
from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass
class DomainEvent:
    """Base class for domain events."""
    occurred_at: datetime = field(default_factory=datetime.now)


@dataclass
class OrderSubmitted(DomainEvent):
    """Event emitted when an order is submitted."""
    order_id: UUID
    customer_id: UUID
    total_amount: Money


@dataclass
class OrderCancelled(DomainEvent):
    """Event emitted when an order is cancelled."""
    order_id: UUID
    reason: str


@dataclass
class ProductOutOfStock(DomainEvent):
    """Event emitted when a product goes out of stock."""
    product_id: UUID
    product_name: str


# Add event collection to aggregate
@dataclass
class Order:
    id: UUID
    customer_id: UUID
    items: List[OrderItem] = field(default_factory=list)
    status: str = "pending"
    _events: List[DomainEvent] = field(default_factory=list, repr=False)
    
    def submit(self) -> None:
        """Submit order and emit event."""
        if not self.items:
            raise BusinessRuleViolationException("Cannot submit empty order")
        
        self.status = "submitted"
        
        # Emit domain event
        self._events.append(OrderSubmitted(
            order_id=self.id,
            customer_id=self.customer_id,
            total_amount=self.calculate_total(),
        ))
    
    def collect_events(self) -> List[DomainEvent]:
        """Collect and clear domain events."""
        events = self._events.copy()
        self._events.clear()
        return events
```

## Best Practices

### 1. Keep Domain Logic Pure

```python
# ✅ Good - Pure domain logic
class Order:
    def calculate_total(self) -> Money:
        return sum(item.line_total() for item in self.items)


# ❌ Bad - Mixed with infrastructure
class Order:
    def calculate_total(self) -> Money:
        # Don't access database from domain!
        tax_rate = database.get_tax_rate(self.customer.region)
        return self.subtotal * (1 + tax_rate)
```

### 2. Use Factory Methods

```python
# ✅ Good - Factory method with validation
class Customer:
    @staticmethod
    def create(name: str, email: str) -> "Customer":
        # Validation and business rules
        if not name.strip():
            raise ValueError("Name is required")
        
        return Customer(
            id=uuid4(),
            name=name,
            email=Email(email),
            created_at=datetime.now(),
        )


# ❌ Bad - Direct construction without validation
customer = Customer(
    id=uuid4(),
    name="",  # No validation!
    email="invalid",
    created_at=datetime.now(),
)
```

### 3. Protect Invariants

```python
# ✅ Good - Invariants protected
class BankAccount:
    def withdraw(self, amount: Money) -> None:
        if amount.amount > self.balance.amount:
            raise InsufficientFundsException()
        
        self.balance = self.balance.subtract(amount)


# ❌ Bad - Direct field access breaks invariants
account.balance = Money(-100, Currency.USD)  # Negative balance!
```

### 4. Use Immutable Value Objects

```python
# ✅ Good - Immutable value object
@dataclass(frozen=True)
class Money:
    amount: float
    currency: Currency


# ❌ Bad - Mutable value object
@dataclass
class Money:
    amount: float
    currency: Currency
    
money = Money(100, Currency.USD)
money.amount = 200  # Should not be allowed!
```

This comprehensive domain layer guide provides patterns for building robust, maintainable business logic in Python! 🎯
