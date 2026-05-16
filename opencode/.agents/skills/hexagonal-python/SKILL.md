---
name: hexagonal-python
description: Implement hexagonal architecture (ports and adapters pattern) in Python. Build maintainable, testable applications with clear separation between business logic and external dependencies. Includes domain layer, ports, adapters, dependency injection, and testing patterns.
---

# Hexagonal Architecture in Python

Official skill for implementing hexagonal architecture (also known as ports and adapters pattern) in Python applications. This architecture promotes clean separation of concerns, testability, and flexibility by decoupling business logic from external dependencies.

## What is Hexagonal Architecture?

Hexagonal architecture is a software design pattern that:

- **Isolates business logic** in the domain layer (core)
- **Defines interfaces** (ports) for all external interactions
- **Implements adapters** that connect ports to concrete technologies
- **Inverts dependencies** so the core depends on nothing external

### Core Benefits

1. **Testability**: Test business logic without databases, APIs, or frameworks
2. **Flexibility**: Swap implementations (database, API framework, message queue) without changing core logic
3. **Maintainability**: Clear boundaries and responsibilities
4. **Framework independence**: Core logic doesn't depend on Django, FastAPI, Flask, etc.

## Project Structure

Organize your Python project following this structure:

```
my_project/
├── domain/                    # Core business logic (no external dependencies)
│   ├── __init__.py
│   ├── entities.py           # Domain entities
│   ├── value_objects.py      # Immutable value objects
│   ├── exceptions.py         # Domain exceptions
│   └── services.py           # Domain services (complex business logic)
│
├── application/               # Use cases / application services
│   ├── __init__.py
│   └── use_cases.py          # Orchestrate domain logic
│
├── ports/                     # Interfaces (contracts)
│   ├── __init__.py
│   ├── input.py              # Driving ports (use cases, commands)
│   └── output.py             # Driven ports (repositories, external services)
│
├── adapters/                  # Implementations
│   ├── __init__.py
│   ├── input/                # Primary/driving adapters
│   │   ├── __init__.py
│   │   ├── rest_api.py      # FastAPI/Flask endpoints
│   │   └── cli.py           # CLI interface (Click/Typer)
│   └── output/               # Secondary/driven adapters
│       ├── __init__.py
│       ├── repositories.py   # Database access (SQLAlchemy, SQLModel)
│       └── external_api.py   # Third-party API clients
│
├── config/                    # Configuration and DI setup
│   ├── __init__.py
│   └── dependencies.py       # Dependency injection wiring
│
└── tests/
    ├── unit/                 # Domain and use case tests
    ├── integration/          # Adapter tests
    └── fakes/               # Fake implementations for testing
```

## Domain Layer

The domain layer contains your business logic and has **zero external dependencies**.

### Domain Entities

```python
# domain/entities.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4


@dataclass
class Order:
    """Domain entity representing an order."""
    id: UUID
    customer_id: UUID
    total_amount: float
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @staticmethod
    def create(customer_id: UUID, total_amount: float) -> "Order":
        """Factory method to create a new order."""
        if total_amount <= 0:
            raise ValueError("Total amount must be positive")
        
        return Order(
            id=uuid4(),
            customer_id=customer_id,
            total_amount=total_amount,
            status="pending",
            created_at=datetime.now(),
        )
    
    def confirm(self) -> None:
        """Confirm the order."""
        if self.status != "pending":
            raise ValueError(f"Cannot confirm order with status: {self.status}")
        
        self.status = "confirmed"
        self.updated_at = datetime.now()
    
    def cancel(self) -> None:
        """Cancel the order."""
        if self.status in ["completed", "cancelled"]:
            raise ValueError(f"Cannot cancel order with status: {self.status}")
        
        self.status = "cancelled"
        self.updated_at = datetime.now()
```

### Domain Services

For complex business logic that doesn't belong to a single entity:

```python
# domain/services.py
from domain.entities import Order


class OrderPricingService:
    """Domain service for calculating order prices."""
    
    def calculate_total_with_discount(
        self,
        order: Order,
        discount_percentage: float,
    ) -> float:
        """Calculate order total with discount applied."""
        if not 0 <= discount_percentage <= 100:
            raise ValueError("Discount must be between 0 and 100")
        
        discount_amount = order.total_amount * (discount_percentage / 100)
        return order.total_amount - discount_amount
```

## Ports (Interfaces)

Ports define **contracts** for interactions with the outside world. Use `typing.Protocol` or `abc.ABC` for defining ports.

### Output Ports (Driven/Secondary)

These are interfaces that the domain needs:

```python
# ports/output.py
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
        """Find an order by ID."""
        pass
    
    @abstractmethod
    def delete(self, order_id: UUID) -> None:
        """Delete an order."""
        pass


class NotificationService(ABC):
    """Port for sending notifications."""
    
    @abstractmethod
    def send_order_confirmation(self, order: Order) -> None:
        """Send order confirmation notification."""
        pass
```

### Input Ports (Driving/Primary)

These define use cases that drive the application:

```python
# ports/input.py
from abc import ABC, abstractmethod
from typing import Optional
from uuid import UUID

from domain.entities import Order


class CreateOrderUseCase(ABC):
    """Port for creating an order."""
    
    @abstractmethod
    def execute(self, customer_id: UUID, total_amount: float) -> Order:
        """Create a new order."""
        pass


class ConfirmOrderUseCase(ABC):
    """Port for confirming an order."""
    
    @abstractmethod
    def execute(self, order_id: UUID) -> Optional[Order]:
        """Confirm an order by ID."""
        pass
```

## Application Layer (Use Cases)

Use cases orchestrate domain logic and coordinate between ports:

```python
# application/use_cases.py
from typing import Optional
from uuid import UUID

from domain.entities import Order
from ports.input import CreateOrderUseCase, ConfirmOrderUseCase
from ports.output import OrderRepository, NotificationService


class CreateOrder(CreateOrderUseCase):
    """Use case for creating an order."""
    
    def __init__(self, repository: OrderRepository):
        self.repository = repository
    
    def execute(self, customer_id: UUID, total_amount: float) -> Order:
        """Create and save a new order."""
        order = Order.create(customer_id, total_amount)
        self.repository.save(order)
        return order


class ConfirmOrder(ConfirmOrderUseCase):
    """Use case for confirming an order."""
    
    def __init__(
        self,
        repository: OrderRepository,
        notification_service: NotificationService,
    ):
        self.repository = repository
        self.notification_service = notification_service
    
    def execute(self, order_id: UUID) -> Optional[Order]:
        """Confirm an order and send notification."""
        order = self.repository.find_by_id(order_id)
        
        if not order:
            return None
        
        order.confirm()
        self.repository.save(order)
        self.notification_service.send_order_confirmation(order)
        
        return order
```

## Adapters

Adapters are concrete implementations of ports. They connect your core logic to external systems.

See detailed adapter patterns in [the adapters reference](references/adapters.md).

### Output Adapter Example (Repository)

```python
# adapters/output/repositories.py
from typing import Optional
from uuid import UUID

from sqlmodel import Session, select

from domain.entities import Order
from ports.output import OrderRepository


class SQLModelOrderRepository(OrderRepository):
    """SQLModel implementation of OrderRepository."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, order: Order) -> None:
        """Save order to database."""
        # Convert domain entity to ORM model
        db_order = self._to_orm_model(order)
        self.session.add(db_order)
        self.session.commit()
    
    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """Find order by ID."""
        statement = select(OrderModel).where(OrderModel.id == order_id)
        db_order = self.session.exec(statement).first()
        
        if not db_order:
            return None
        
        return self._to_domain_entity(db_order)
    
    def delete(self, order_id: UUID) -> None:
        """Delete order from database."""
        statement = select(OrderModel).where(OrderModel.id == order_id)
        db_order = self.session.exec(statement).first()
        
        if db_order:
            self.session.delete(db_order)
            self.session.commit()
    
    def _to_orm_model(self, order: Order) -> "OrderModel":
        """Convert domain entity to ORM model."""
        # Implementation details...
        pass
    
    def _to_domain_entity(self, db_order: "OrderModel") -> Order:
        """Convert ORM model to domain entity."""
        # Implementation details...
        pass
```

### Input Adapter Example (FastAPI)

```python
# adapters/input/rest_api.py
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from ports.input import CreateOrderUseCase, ConfirmOrderUseCase


router = APIRouter(prefix="/orders", tags=["orders"])


class CreateOrderRequest(BaseModel):
    """Request model for creating an order."""
    customer_id: UUID
    total_amount: float = Field(gt=0)


class OrderResponse(BaseModel):
    """Response model for order."""
    id: UUID
    customer_id: UUID
    total_amount: float
    status: str


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    request: CreateOrderRequest,
    use_case: Annotated[CreateOrderUseCase, Depends()],
) -> OrderResponse:
    """Create a new order."""
    order = use_case.execute(
        customer_id=request.customer_id,
        total_amount=request.total_amount,
    )
    
    return OrderResponse(
        id=order.id,
        customer_id=order.customer_id,
        total_amount=order.total_amount,
        status=order.status,
    )


@router.post("/{order_id}/confirm", response_model=OrderResponse)
async def confirm_order(
    order_id: UUID,
    use_case: Annotated[ConfirmOrderUseCase, Depends()],
) -> OrderResponse:
    """Confirm an order."""
    order = use_case.execute(order_id)
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found",
        )
    
    return OrderResponse(
        id=order.id,
        customer_id=order.customer_id,
        total_amount=order.total_amount,
        status=order.status,
    )
```

## Dependency Injection

Wire everything together using dependency injection. You can use manual DI or libraries like `dependency-injector`.

### Manual Dependency Injection

```python
# config/dependencies.py
from functools import lru_cache

from sqlmodel import Session

from adapters.output.repositories import SQLModelOrderRepository
from adapters.output.notifications import EmailNotificationService
from application.use_cases import CreateOrder, ConfirmOrder
from ports.input import CreateOrderUseCase, ConfirmOrderUseCase


@lru_cache
def get_order_repository(session: Session) -> SQLModelOrderRepository:
    """Get order repository instance."""
    return SQLModelOrderRepository(session)


@lru_cache
def get_notification_service() -> EmailNotificationService:
    """Get notification service instance."""
    return EmailNotificationService()


def get_create_order_use_case(
    session: Session,
) -> CreateOrderUseCase:
    """Get create order use case instance."""
    repository = get_order_repository(session)
    return CreateOrder(repository)


def get_confirm_order_use_case(
    session: Session,
) -> ConfirmOrderUseCase:
    """Get confirm order use case instance."""
    repository = get_order_repository(session)
    notification_service = get_notification_service()
    return ConfirmOrder(repository, notification_service)
```

### Using with FastAPI

```python
# main.py
from fastapi import FastAPI, Depends
from sqlmodel import Session

from adapters.input.rest_api import router
from config.dependencies import get_create_order_use_case, get_confirm_order_use_case
from config.database import get_session


app = FastAPI()


# Register dependency providers
app.dependency_overrides[CreateOrderUseCase] = get_create_order_use_case
app.dependency_overrides[ConfirmOrderUseCase] = get_confirm_order_use_case


app.include_router(router)
```

## Testing

Hexagonal architecture makes testing straightforward by allowing you to test each layer independently.

See [the testing reference](references/testing.md) for comprehensive testing strategies.

### Unit Testing Domain Logic

```python
# tests/unit/test_order_entity.py
import pytest
from uuid import uuid4
from domain.entities import Order


def test_create_order_with_valid_data():
    """Test creating an order with valid data."""
    customer_id = uuid4()
    total_amount = 100.0
    
    order = Order.create(customer_id, total_amount)
    
    assert order.customer_id == customer_id
    assert order.total_amount == total_amount
    assert order.status == "pending"


def test_create_order_with_negative_amount_raises_error():
    """Test that creating an order with negative amount raises error."""
    customer_id = uuid4()
    
    with pytest.raises(ValueError, match="Total amount must be positive"):
        Order.create(customer_id, -50.0)


def test_confirm_order():
    """Test confirming a pending order."""
    order = Order.create(uuid4(), 100.0)
    
    order.confirm()
    
    assert order.status == "confirmed"
    assert order.updated_at is not None
```

### Testing Use Cases with Fake Adapters

```python
# tests/fakes/repositories.py
from typing import Optional, Dict
from uuid import UUID

from domain.entities import Order
from ports.output import OrderRepository


class FakeOrderRepository(OrderRepository):
    """Fake in-memory repository for testing."""
    
    def __init__(self):
        self._orders: Dict[UUID, Order] = {}
    
    def save(self, order: Order) -> None:
        """Save order in memory."""
        self._orders[order.id] = order
    
    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """Find order by ID."""
        return self._orders.get(order_id)
    
    def delete(self, order_id: UUID) -> None:
        """Delete order."""
        self._orders.pop(order_id, None)


# tests/unit/test_create_order_use_case.py
from uuid import uuid4

from application.use_cases import CreateOrder
from tests.fakes.repositories import FakeOrderRepository


def test_create_order_use_case():
    """Test creating an order through use case."""
    repository = FakeOrderRepository()
    use_case = CreateOrder(repository)
    customer_id = uuid4()
    
    order = use_case.execute(customer_id, 150.0)
    
    assert order.customer_id == customer_id
    assert order.total_amount == 150.0
    
    # Verify it was saved
    saved_order = repository.find_by_id(order.id)
    assert saved_order is not None
    assert saved_order.id == order.id
```

## Best Practices

### 1. Domain Layer Should Be Pure Python

The domain layer should have **no external dependencies** (no SQLAlchemy, FastAPI, etc.):

```python
# ✅ Good - Pure Python domain entity
@dataclass
class Product:
    id: UUID
    name: str
    price: float
    
    def apply_discount(self, percentage: float) -> float:
        return self.price * (1 - percentage / 100)


# ❌ Bad - Domain entity with ORM dependency
from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Product(Base):  # Don't mix domain with infrastructure
    __tablename__ = "products"
    id = Column(String, primary_key=True)
    name = Column(String)
```

### 2. Use Protocol or ABC for Ports

Use `typing.Protocol` for structural typing or `abc.ABC` for explicit interfaces:

```python
# Using Protocol (more Pythonic, duck typing)
from typing import Protocol

class Repository(Protocol):
    def save(self, entity: Entity) -> None: ...
    def find_by_id(self, id: UUID) -> Optional[Entity]: ...


# Using ABC (more explicit, Java-like)
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def save(self, entity: Entity) -> None:
        pass
```

### 3. Keep Adapters Thin

Adapters should only translate between external systems and your domain:

```python
# ✅ Good - Thin adapter that delegates to use case
@router.post("/orders")
async def create_order(
    request: CreateOrderRequest,
    use_case: Annotated[CreateOrderUseCase, Depends()],
):
    return use_case.execute(request.customer_id, request.total_amount)


# ❌ Bad - Adapter with business logic
@router.post("/orders")
async def create_order(request: CreateOrderRequest, db: Session):
    # Business logic in adapter - wrong!
    if request.total_amount < 0:
        raise HTTPException(400, "Invalid amount")
    
    order = Order(...)
    db.add(order)
    db.commit()
```

### 4. Use Value Objects for Domain Concepts

```python
# domain/value_objects.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Money:
    """Value object representing money."""
    amount: float
    currency: str
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if self.currency not in ["USD", "EUR", "GBP"]:
            raise ValueError(f"Unsupported currency: {self.currency}")
    
    def add(self, other: "Money") -> "Money":
        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")
        return Money(self.amount + other.amount, self.currency)
```

### 5. Separate ORM Models from Domain Entities

Don't use the same class for domain entities and database models:

```python
# ✅ Good - Separate models
# domain/entities.py
@dataclass
class Order:
    id: UUID
    customer_id: UUID
    total: Money

# adapters/output/models.py (ORM models)
from sqlmodel import SQLModel, Field

class OrderModel(SQLModel, table=True):
    __tablename__ = "orders"
    
    id: UUID = Field(primary_key=True)
    customer_id: UUID
    amount: float
    currency: str
```

### 6. Handle Async Operations Properly

When using async frameworks like FastAPI, adapters can be async while domain stays sync:

```python
# Domain layer - sync (pure business logic)
class Order:
    def confirm(self) -> None:
        self.status = "confirmed"


# Adapter - async (handles I/O)
class AsyncOrderRepository:
    async def save(self, order: Order) -> None:
        await self.db.execute(...)
        await self.db.commit()


# Use case - can be sync or async depending on adapters
class ConfirmOrder:
    def __init__(self, repository: AsyncOrderRepository):
        self.repository = repository
    
    async def execute(self, order_id: UUID) -> Optional[Order]:
        order = await self.repository.find_by_id(order_id)
        if order:
            order.confirm()  # Sync domain method
            await self.repository.save(order)  # Async persistence
        return order
```

## When to Use Hexagonal Architecture

### ✅ Good fit for:

- Applications with complex business logic
- Long-lived projects that will evolve
- Systems requiring high testability
- Projects with uncertain technology choices
- Domain-Driven Design implementations
- Microservices with clear bounded contexts

### ❌ Not recommended for:

- Simple CRUD applications with minimal business logic
- Prototypes or MVPs with tight deadlines
- Small scripts or utilities
- Teams unfamiliar with the pattern (without training)

## Common Patterns

### Repository Pattern

See [the adapters reference](references/adapters.md) for repository implementations.

### Use Case Pattern

Each use case should:
- Have a single responsibility
- Be independently testable
- Orchestrate domain objects
- Coordinate between ports

### Domain Events

For complex workflows, consider domain events:

```python
# domain/events.py
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class OrderConfirmed:
    """Domain event emitted when an order is confirmed."""
    order_id: UUID
    customer_id: UUID
    occurred_at: datetime


# domain/entities.py
class Order:
    def __init__(self):
        self._events: list = []
    
    def confirm(self) -> None:
        self.status = "confirmed"
        self._events.append(OrderConfirmed(
            order_id=self.id,
            customer_id=self.customer_id,
            occurred_at=datetime.now(),
        ))
    
    def collect_events(self) -> list:
        events = self._events.copy()
        self._events.clear()
        return events
```

## Additional Resources

- [Domain Layer Patterns](references/domain-layer.md) - Entities, value objects, services
- [Ports Patterns](references/ports.md) - Interface design and contracts
- [Adapters Patterns](references/adapters.md) - REST, database, CLI, messaging adapters
- [Testing Strategies](references/testing.md) - Unit, integration, and fake implementations
- [Complete Example Project](references/example-project.md) - Full working implementation

## References

- Hexagonal Architecture by Alistair Cockburn (2005)
- Clean Architecture by Robert C. Martin
- Domain-Driven Design by Eric Evans
- [Hexagonal Architecture in Python](https://douwevandermeij.medium.com/hexagonal-architecture-in-python-7468c2606b63)
