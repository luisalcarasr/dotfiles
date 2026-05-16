# Ports Patterns

Ports are **interfaces** that define contracts between your domain/application layer and the external world. They represent the boundaries of your system and enforce the dependency inversion principle.

## Types of Ports

### Input Ports (Driving/Primary Ports)

These ports **drive** your application. They define what your application can do (use cases).

**Who uses them:** External actors like REST APIs, CLI commands, message consumers, scheduled jobs

**Direction:** Outside → Inside

### Output Ports (Driven/Secondary Ports)

These ports are **driven** by your application. They define what your application needs from external systems.

**Who implements them:** Adapters for databases, external APIs, file systems, message queues

**Direction:** Inside → Outside

## Defining Ports in Python

You have two main options for defining ports:

### Option 1: Using Protocol (Structural Typing)

More Pythonic, supports duck typing:

```python
from typing import Protocol, Optional
from uuid import UUID

from domain.entities import Order


class OrderRepository(Protocol):
    """Port for order persistence."""
    
    def save(self, order: Order) -> None:
        """Save an order."""
        ...
    
    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """Find order by ID."""
        ...
    
    def find_all(self) -> list[Order]:
        """Find all orders."""
        ...
    
    def delete(self, order_id: UUID) -> None:
        """Delete an order."""
        ...
```

### Option 2: Using ABC (Abstract Base Classes)

More explicit, traditional OOP approach:

```python
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities import Order


class OrderRepository(ABC):
    """Port for order persistence."""
    
    @abstractmethod
    def save(self, order: Order) -> None:
        """Save an order."""
        pass
    
    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """Find order by ID."""
        pass
    
    @abstractmethod
    def find_all(self) -> list[Order]:
        """Find all orders."""
        pass
    
    @abstractmethod
    def delete(self, order_id: UUID) -> None:
        """Delete an order."""
        pass
```

**Recommendation:** Use `Protocol` for most cases (more Pythonic). Use `ABC` when you need runtime checking or want more explicit inheritance.

## Output Ports (Driven Ports)

### Repository Port

```python
# ports/output.py
from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar, List
from uuid import UUID


T = TypeVar('T')


class Repository(ABC, Generic[T]):
    """Generic repository port."""
    
    @abstractmethod
    def save(self, entity: T) -> None:
        """Save an entity."""
        pass
    
    @abstractmethod
    def find_by_id(self, entity_id: UUID) -> Optional[T]:
        """Find entity by ID."""
        pass
    
    @abstractmethod
    def find_all(self) -> List[T]:
        """Find all entities."""
        pass
    
    @abstractmethod
    def delete(self, entity_id: UUID) -> None:
        """Delete an entity."""
        pass


class OrderRepository(ABC):
    """Specific port for order persistence."""
    
    @abstractmethod
    def save(self, order: Order) -> None:
        """Save an order."""
        pass
    
    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """Find order by ID."""
        pass
    
    @abstractmethod
    def find_by_customer(self, customer_id: UUID) -> List[Order]:
        """Find all orders for a customer."""
        pass
    
    @abstractmethod
    def find_by_status(self, status: str) -> List[Order]:
        """Find orders by status."""
        pass
    
    @abstractmethod
    def count_by_status(self, status: str) -> int:
        """Count orders by status."""
        pass
```

### External Service Ports

```python
class NotificationService(ABC):
    """Port for sending notifications."""
    
    @abstractmethod
    def send_email(self, to: str, subject: str, body: str) -> None:
        """Send an email."""
        pass
    
    @abstractmethod
    def send_sms(self, phone: str, message: str) -> None:
        """Send an SMS."""
        pass


class PaymentGateway(ABC):
    """Port for payment processing."""
    
    @abstractmethod
    def charge(self, amount: Money, payment_method: str) -> PaymentResult:
        """Charge a payment method."""
        pass
    
    @abstractmethod
    def refund(self, transaction_id: str, amount: Money) -> RefundResult:
        """Refund a transaction."""
        pass
    
    @abstractmethod
    def get_transaction_status(self, transaction_id: str) -> str:
        """Get transaction status."""
        pass


class EventPublisher(ABC):
    """Port for publishing domain events."""
    
    @abstractmethod
    def publish(self, event: DomainEvent) -> None:
        """Publish a domain event."""
        pass
    
    @abstractmethod
    def publish_batch(self, events: List[DomainEvent]) -> None:
        """Publish multiple domain events."""
        pass
```

### File Storage Port

```python
from typing import BinaryIO


class FileStorage(ABC):
    """Port for file storage operations."""
    
    @abstractmethod
    def upload(self, file_path: str, content: BinaryIO) -> str:
        """Upload a file and return its URL."""
        pass
    
    @abstractmethod
    def download(self, file_path: str) -> BinaryIO:
        """Download a file."""
        pass
    
    @abstractmethod
    def delete(self, file_path: str) -> None:
        """Delete a file."""
        pass
    
    @abstractmethod
    def exists(self, file_path: str) -> bool:
        """Check if file exists."""
        pass
    
    @abstractmethod
    def get_url(self, file_path: str) -> str:
        """Get public URL for a file."""
        pass
```

### Cache Port

```python
from typing import Any, Optional


class CacheService(ABC):
    """Port for caching operations."""
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Set value in cache with optional TTL."""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> None:
        """Delete value from cache."""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        pass
    
    @abstractmethod
    def clear(self) -> None:
        """Clear all cache entries."""
        pass
```

## Input Ports (Driving Ports)

Input ports define **use cases** - the things your application can do.

### Command Pattern

Commands represent actions that change state:

```python
# ports/input.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from domain.entities import Order


@dataclass
class CreateOrderCommand:
    """Command to create an order."""
    customer_id: UUID
    items: List[OrderItemData]


@dataclass
class OrderItemData:
    """Data for an order item."""
    product_id: UUID
    quantity: int


class CreateOrderUseCase(ABC):
    """Use case for creating an order."""
    
    @abstractmethod
    def execute(self, command: CreateOrderCommand) -> Order:
        """Execute the create order use case."""
        pass


class ConfirmOrderUseCase(ABC):
    """Use case for confirming an order."""
    
    @abstractmethod
    def execute(self, order_id: UUID) -> Optional[Order]:
        """Execute the confirm order use case."""
        pass


class CancelOrderUseCase(ABC):
    """Use case for cancelling an order."""
    
    @abstractmethod
    def execute(self, order_id: UUID, reason: str) -> Optional[Order]:
        """Execute the cancel order use case."""
        pass
```

### Query Pattern

Queries represent read operations that don't change state:

```python
@dataclass
class OrderQuery:
    """Query for finding orders."""
    customer_id: Optional[UUID] = None
    status: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None


class GetOrderQuery(ABC):
    """Query to get a single order."""
    
    @abstractmethod
    def execute(self, order_id: UUID) -> Optional[Order]:
        """Get an order by ID."""
        pass


class ListOrdersQuery(ABC):
    """Query to list orders."""
    
    @abstractmethod
    def execute(self, query: OrderQuery) -> List[Order]:
        """List orders matching query criteria."""
        pass


class GetOrderStatisticsQuery(ABC):
    """Query to get order statistics."""
    
    @abstractmethod
    def execute(self, customer_id: UUID) -> OrderStatistics:
        """Get statistics for a customer."""
        pass
```

### CQRS Pattern (Command Query Responsibility Segregation)

Separate read and write operations:

```python
# Write side (Commands)
class OrderCommands(ABC):
    """Port for order write operations."""
    
    @abstractmethod
    def create_order(self, command: CreateOrderCommand) -> Order:
        pass
    
    @abstractmethod
    def confirm_order(self, order_id: UUID) -> Optional[Order]:
        pass
    
    @abstractmethod
    def cancel_order(self, order_id: UUID, reason: str) -> Optional[Order]:
        pass


# Read side (Queries)
class OrderQueries(ABC):
    """Port for order read operations."""
    
    @abstractmethod
    def get_order(self, order_id: UUID) -> Optional[Order]:
        pass
    
    @abstractmethod
    def list_orders(self, query: OrderQuery) -> List[Order]:
        pass
    
    @abstractmethod
    def get_statistics(self, customer_id: UUID) -> OrderStatistics:
        pass
```

## Async Ports

For async operations (useful with FastAPI, async databases):

```python
from typing import Protocol


class AsyncOrderRepository(Protocol):
    """Async port for order persistence."""
    
    async def save(self, order: Order) -> None:
        """Save an order asynchronously."""
        ...
    
    async def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """Find order by ID asynchronously."""
        ...
    
    async def find_all(self) -> List[Order]:
        """Find all orders asynchronously."""
        ...


class AsyncNotificationService(Protocol):
    """Async port for notifications."""
    
    async def send_email(self, to: str, subject: str, body: str) -> None:
        """Send email asynchronously."""
        ...
    
    async def send_sms(self, phone: str, message: str) -> None:
        """Send SMS asynchronously."""
        ...
```

## Port Organization

### Single Responsibility

Each port should have a single, well-defined responsibility:

```python
# ✅ Good - Focused ports
class OrderRepository(ABC):
    """Only handles order persistence."""
    @abstractmethod
    def save(self, order: Order) -> None: pass


class OrderNotifier(ABC):
    """Only handles order notifications."""
    @abstractmethod
    def notify_order_created(self, order: Order) -> None: pass


# ❌ Bad - Mixed responsibilities
class OrderService(ABC):
    """Too many responsibilities!"""
    @abstractmethod
    def save(self, order: Order) -> None: pass
    
    @abstractmethod
    def send_notification(self, order: Order) -> None: pass
    
    @abstractmethod
    def process_payment(self, order: Order) -> None: pass
```

### Interface Segregation

Don't force clients to depend on methods they don't use:

```python
# ✅ Good - Segregated interfaces
class OrderReader(ABC):
    """Read-only operations."""
    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]: pass


class OrderWriter(ABC):
    """Write operations."""
    @abstractmethod
    def save(self, order: Order) -> None: pass
    @abstractmethod
    def delete(self, order_id: UUID) -> None: pass


# Use case only needs reading
class GetOrderUseCase:
    def __init__(self, repository: OrderReader):  # Only requires reading
        self.repository = repository


# ❌ Bad - Forcing unnecessary dependencies
class OrderRepository(ABC):
    """Too broad - forces all clients to depend on all methods."""
    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]: pass
    
    @abstractmethod
    def save(self, order: Order) -> None: pass
    
    @abstractmethod
    def delete(self, order_id: UUID) -> None: pass


class GetOrderUseCase:
    def __init__(self, repository: OrderRepository):  # Needs full interface even though it only reads
        self.repository = repository
```

## Port Design Best Practices

### 1. Use Domain Types in Port Signatures

```python
# ✅ Good - Uses domain entities and value objects
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order) -> None: pass
    
    @abstractmethod
    def find_by_customer(self, customer_id: UUID) -> List[Order]: pass


# ❌ Bad - Uses primitive types or infrastructure types
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order_dict: dict) -> None: pass
    
    @abstractmethod
    def find_by_customer(self, customer_id: str) -> List[dict]: pass
```

### 2. Keep Ports Simple and Focused

```python
# ✅ Good - Simple, clear methods
class EmailService(ABC):
    @abstractmethod
    def send(self, to: Email, subject: str, body: str) -> None: pass


# ❌ Bad - Too complex, too many options
class EmailService(ABC):
    @abstractmethod
    def send(
        self,
        to: Email,
        subject: str,
        body: str,
        cc: Optional[List[Email]] = None,
        bcc: Optional[List[Email]] = None,
        attachments: Optional[List[Attachment]] = None,
        priority: str = "normal",
        reply_to: Optional[Email] = None,
        html: bool = False,
        template: Optional[str] = None,
        template_vars: Optional[dict] = None,
    ) -> None:
        pass
```

### 3. Return Domain Objects, Not Infrastructure Objects

```python
# ✅ Good - Returns domain entity
class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]: pass


# ❌ Bad - Returns ORM model or dict
class OrderRepository(ABC):
    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[OrderModel]: pass  # ORM model!
```

### 4. Use Type Hints

```python
# ✅ Good - Full type hints
class OrderRepository(ABC):
    @abstractmethod
    def find_by_status(self, status: str) -> List[Order]: pass
    
    @abstractmethod
    def count_by_status(self, status: str) -> int: pass


# ❌ Bad - No type hints
class OrderRepository(ABC):
    @abstractmethod
    def find_by_status(self, status): pass
    
    @abstractmethod
    def count_by_status(self, status): pass
```

### 5. Document Port Contracts

```python
class PaymentGateway(ABC):
    """Port for payment processing operations.
    
    Implementations must handle:
    - Network failures with appropriate exceptions
    - Idempotency for charge operations
    - PCI compliance for sensitive data
    """
    
    @abstractmethod
    def charge(self, amount: Money, payment_method: str) -> PaymentResult:
        """Charge a payment method.
        
        Args:
            amount: Amount to charge (must be positive)
            payment_method: Payment method token
        
        Returns:
            PaymentResult with transaction ID and status
        
        Raises:
            PaymentFailedException: If payment fails
            InvalidPaymentMethodException: If payment method is invalid
            InsufficientFundsException: If insufficient funds
        """
        pass
```

## Port Naming Conventions

- **Repositories:** `{Entity}Repository` (e.g., `OrderRepository`, `CustomerRepository`)
- **Services:** `{Capability}Service` (e.g., `NotificationService`, `PaymentService`)
- **Gateways:** `{System}Gateway` (e.g., `PaymentGateway`, `ShippingGateway`)
- **Use Cases:** `{Action}{Entity}UseCase` (e.g., `CreateOrderUseCase`, `ConfirmOrderUseCase`)
- **Queries:** `{Action}{Entity}Query` (e.g., `GetOrderQuery`, `ListOrdersQuery`)

## Example: Complete Port Set

```python
# ports/output.py
"""Output ports (driven by application)."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities import Order, Customer, Product
from domain.events import DomainEvent


class OrderRepository(ABC):
    """Port for order persistence."""
    
    @abstractmethod
    def save(self, order: Order) -> None: pass
    
    @abstractmethod
    def find_by_id(self, order_id: UUID) -> Optional[Order]: pass
    
    @abstractmethod
    def find_by_customer(self, customer_id: UUID) -> List[Order]: pass


class CustomerRepository(ABC):
    """Port for customer persistence."""
    
    @abstractmethod
    def save(self, customer: Customer) -> None: pass
    
    @abstractmethod
    def find_by_id(self, customer_id: UUID) -> Optional[Customer]: pass
    
    @abstractmethod
    def find_by_email(self, email: str) -> Optional[Customer]: pass


class ProductRepository(ABC):
    """Port for product persistence."""
    
    @abstractmethod
    def find_by_id(self, product_id: UUID) -> Optional[Product]: pass
    
    @abstractmethod
    def update_stock(self, product_id: UUID, quantity: int) -> None: pass


class EventPublisher(ABC):
    """Port for publishing domain events."""
    
    @abstractmethod
    def publish(self, event: DomainEvent) -> None: pass


class NotificationService(ABC):
    """Port for notifications."""
    
    @abstractmethod
    def send_order_confirmation(self, order: Order) -> None: pass


# ports/input.py
"""Input ports (drive the application)."""

from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities import Order


class CreateOrderUseCase(ABC):
    """Use case for creating an order."""
    
    @abstractmethod
    def execute(self, customer_id: UUID, items: List[OrderItemData]) -> Order: pass


class ConfirmOrderUseCase(ABC):
    """Use case for confirming an order."""
    
    @abstractmethod
    def execute(self, order_id: UUID) -> Optional[Order]: pass


class GetOrderQuery(ABC):
    """Query for getting an order."""
    
    @abstractmethod
    def execute(self, order_id: UUID) -> Optional[Order]: pass


class ListOrdersQuery(ABC):
    """Query for listing orders."""
    
    @abstractmethod
    def execute(self, customer_id: UUID) -> List[Order]: pass
```

This comprehensive guide covers all the patterns and best practices for defining ports in hexagonal architecture! 🎯
