# Testing Strategies

One of the greatest benefits of hexagonal architecture is **excellent testability**. By separating concerns and using dependency injection, you can test each layer independently with appropriate strategies.

## Test Pyramid

Follow the test pyramid approach:

```
        /\
       /  \    E2E Tests (Few)
      /----\
     / Inte-\  Integration Tests (Some)
    / gration\
   /----------\
  /   Unit     \ Unit Tests (Many)
 /--------------\
```

- **Many unit tests** (fast, isolated, test domain logic)
- **Some integration tests** (test adapters with real infrastructure)
- **Few end-to-end tests** (test complete flows)

## Testing Tools

```bash
# Install testing dependencies
pip install pytest pytest-asyncio pytest-cov pytest-mock faker
```

## Unit Testing

Unit tests should be **fast**, **isolated**, and test business logic without external dependencies.

### Testing Domain Entities

```python
# tests/unit/domain/test_order_entity.py
import pytest
from uuid import uuid4
from datetime import datetime

from domain.entities import Order
from domain.exceptions import InvalidOperationException


class TestOrder:
    """Unit tests for Order entity."""
    
    def test_create_order_with_valid_data(self):
        """Test creating an order with valid data."""
        customer_id = uuid4()
        total_amount = 100.0
        
        order = Order.create(customer_id, total_amount)
        
        assert order.customer_id == customer_id
        assert order.total_amount == total_amount
        assert order.status == "pending"
        assert isinstance(order.id, type(uuid4()))
        assert isinstance(order.created_at, datetime)
    
    def test_create_order_with_negative_amount_raises_error(self):
        """Test that negative amount raises ValueError."""
        customer_id = uuid4()
        
        with pytest.raises(ValueError, match="Total amount must be positive"):
            Order.create(customer_id, -50.0)
    
    def test_create_order_with_zero_amount_raises_error(self):
        """Test that zero amount raises ValueError."""
        customer_id = uuid4()
        
        with pytest.raises(ValueError, match="Total amount must be positive"):
            Order.create(customer_id, 0.0)
    
    def test_confirm_pending_order(self):
        """Test confirming a pending order."""
        order = Order.create(uuid4(), 100.0)
        
        order.confirm()
        
        assert order.status == "confirmed"
        assert order.updated_at is not None
    
    def test_confirm_non_pending_order_raises_error(self):
        """Test that confirming non-pending order raises error."""
        order = Order.create(uuid4(), 100.0)
        order.status = "completed"
        
        with pytest.raises(InvalidOperationException):
            order.confirm()
    
    def test_cancel_order(self):
        """Test cancelling an order."""
        order = Order.create(uuid4(), 100.0)
        
        order.cancel()
        
        assert order.status == "cancelled"
        assert order.updated_at is not None
    
    def test_cancel_completed_order_raises_error(self):
        """Test that cancelling completed order raises error."""
        order = Order.create(uuid4(), 100.0)
        order.status = "completed"
        
        with pytest.raises(InvalidOperationException):
            order.cancel()


# Using pytest fixtures
@pytest.fixture
def customer_id():
    """Fixture providing a customer ID."""
    return uuid4()


@pytest.fixture
def valid_order(customer_id):
    """Fixture providing a valid order."""
    return Order.create(customer_id, 100.0)


def test_confirm_order_with_fixture(valid_order):
    """Test using fixtures."""
    valid_order.confirm()
    assert valid_order.status == "confirmed"
```

### Testing Value Objects

```python
# tests/unit/domain/test_value_objects.py
import pytest

from domain.value_objects import Money, Currency, Email


class TestMoney:
    """Unit tests for Money value object."""
    
    def test_create_money_with_valid_values(self):
        """Test creating money with valid values."""
        money = Money(100.50, Currency.USD)
        
        assert money.amount == 100.50
        assert money.currency == Currency.USD
    
    def test_create_money_with_negative_amount_raises_error(self):
        """Test that negative amount raises error."""
        with pytest.raises(ValueError, match="cannot be negative"):
            Money(-50.0, Currency.USD)
    
    def test_add_money_with_same_currency(self):
        """Test adding money with same currency."""
        money1 = Money(100.0, Currency.USD)
        money2 = Money(50.0, Currency.USD)
        
        result = money1.add(money2)
        
        assert result.amount == 150.0
        assert result.currency == Currency.USD
    
    def test_add_money_with_different_currency_raises_error(self):
        """Test that adding different currencies raises error."""
        money1 = Money(100.0, Currency.USD)
        money2 = Money(50.0, Currency.EUR)
        
        with pytest.raises(ValueError, match="Cannot add different currencies"):
            money1.add(money2)
    
    def test_money_immutability(self):
        """Test that Money is immutable."""
        money = Money(100.0, Currency.USD)
        
        with pytest.raises(AttributeError):
            money.amount = 200.0
    
    def test_money_equality(self):
        """Test Money equality."""
        money1 = Money(100.0, Currency.USD)
        money2 = Money(100.0, Currency.USD)
        money3 = Money(100.0, Currency.EUR)
        
        assert money1 == money2
        assert money1 != money3


class TestEmail:
    """Unit tests for Email value object."""
    
    @pytest.mark.parametrize("email_address", [
        "user@example.com",
        "john.doe@company.co.uk",
        "test+tag@gmail.com",
    ])
    def test_create_valid_email(self, email_address):
        """Test creating email with valid addresses."""
        email = Email(email_address)
        assert email.value == email_address
    
    @pytest.mark.parametrize("invalid_email", [
        "not-an-email",
        "@example.com",
        "user@",
        "user @example.com",
    ])
    def test_create_invalid_email_raises_error(self, invalid_email):
        """Test that invalid email raises error."""
        with pytest.raises(ValueError, match="Invalid email"):
            Email(invalid_email)
    
    def test_email_domain(self):
        """Test extracting email domain."""
        email = Email("user@example.com")
        assert email.domain() == "example.com"
```

### Testing Domain Services

```python
# tests/unit/domain/test_services.py
import pytest
from uuid import uuid4

from domain.entities import Order
from domain.services import PricingService
from domain.value_objects import Money, Currency


class TestPricingService:
    """Unit tests for PricingService."""
    
    @pytest.fixture
    def pricing_service(self):
        """Fixture providing PricingService."""
        return PricingService()
    
    @pytest.fixture
    def order(self):
        """Fixture providing an order."""
        return Order.create(uuid4(), 100.0)
    
    def test_calculate_vip_discount(self, pricing_service):
        """Test VIP discount calculation."""
        amount = Money(100.0, Currency.USD)
        
        discount = pricing_service._calculate_vip_discount(amount)
        
        assert discount.amount == 10.0
        assert discount.currency == Currency.USD
    
    def test_calculate_tax(self, pricing_service):
        """Test tax calculation."""
        amount = Money(100.0, Currency.USD)
        
        tax = pricing_service._calculate_tax(amount)
        
        assert tax.amount == 8.0
        assert tax.currency == Currency.USD
```

## Testing Use Cases with Fake Adapters

Use **fake implementations** of ports for testing use cases in isolation.

### Fake Repository

```python
# tests/fakes/repositories.py
from typing import Dict, List, Optional
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
    
    def find_by_customer(self, customer_id: UUID) -> List[Order]:
        """Find orders by customer."""
        return [
            order for order in self._orders.values()
            if order.customer_id == customer_id
        ]
    
    def find_by_status(self, status: str) -> List[Order]:
        """Find orders by status."""
        return [
            order for order in self._orders.values()
            if order.status == status
        ]
    
    def delete(self, order_id: UUID) -> None:
        """Delete order."""
        self._orders.pop(order_id, None)
    
    def clear(self) -> None:
        """Clear all orders (testing helper)."""
        self._orders.clear()
```

### Fake Notification Service

```python
# tests/fakes/notifications.py
from typing import List
from dataclasses import dataclass

from domain.entities import Order
from ports.output import NotificationService


@dataclass
class SentEmail:
    """Record of sent email."""
    to: str
    subject: str
    body: str


class FakeNotificationService(NotificationService):
    """Fake notification service for testing."""
    
    def __init__(self):
        self.sent_emails: List[SentEmail] = []
    
    def send_email(self, to: str, subject: str, body: str) -> None:
        """Record sent email."""
        self.sent_emails.append(SentEmail(to, subject, body))
    
    def send_order_confirmation(self, order: Order) -> None:
        """Record order confirmation."""
        self.send_email(
            to="customer@example.com",
            subject=f"Order Confirmation - {order.id}",
            body=f"Order {order.id} confirmed",
        )
    
    def clear(self) -> None:
        """Clear sent emails (testing helper)."""
        self.sent_emails.clear()
```

### Testing Use Cases

```python
# tests/unit/application/test_create_order_use_case.py
import pytest
from uuid import uuid4

from application.use_cases import CreateOrder
from tests.fakes.repositories import FakeOrderRepository


class TestCreateOrderUseCase:
    """Unit tests for CreateOrder use case."""
    
    @pytest.fixture
    def repository(self):
        """Fixture providing fake repository."""
        return FakeOrderRepository()
    
    @pytest.fixture
    def use_case(self, repository):
        """Fixture providing use case with fake repository."""
        return CreateOrder(repository)
    
    def test_create_order_saves_to_repository(self, use_case, repository):
        """Test that creating order saves it to repository."""
        customer_id = uuid4()
        total_amount = 150.0
        
        order = use_case.execute(customer_id, total_amount)
        
        # Verify order was saved
        saved_order = repository.find_by_id(order.id)
        assert saved_order is not None
        assert saved_order.id == order.id
        assert saved_order.customer_id == customer_id
        assert saved_order.total_amount == total_amount
    
    def test_create_order_returns_order_with_correct_data(self, use_case):
        """Test that use case returns order with correct data."""
        customer_id = uuid4()
        total_amount = 200.0
        
        order = use_case.execute(customer_id, total_amount)
        
        assert order.customer_id == customer_id
        assert order.total_amount == total_amount
        assert order.status == "pending"


# tests/unit/application/test_confirm_order_use_case.py
class TestConfirmOrderUseCase:
    """Unit tests for ConfirmOrder use case."""
    
    @pytest.fixture
    def repository(self):
        """Fixture providing fake repository."""
        return FakeOrderRepository()
    
    @pytest.fixture
    def notification_service(self):
        """Fixture providing fake notification service."""
        return FakeNotificationService()
    
    @pytest.fixture
    def use_case(self, repository, notification_service):
        """Fixture providing use case."""
        from application.use_cases import ConfirmOrder
        return ConfirmOrder(repository, notification_service)
    
    def test_confirm_existing_order(self, use_case, repository, notification_service):
        """Test confirming an existing order."""
        # Arrange
        from domain.entities import Order
        order = Order.create(uuid4(), 100.0)
        repository.save(order)
        
        # Act
        result = use_case.execute(order.id)
        
        # Assert
        assert result is not None
        assert result.status == "confirmed"
        
        # Verify order was saved
        saved_order = repository.find_by_id(order.id)
        assert saved_order.status == "confirmed"
        
        # Verify notification was sent
        assert len(notification_service.sent_emails) == 1
        assert order.id in str(notification_service.sent_emails[0].subject)
    
    def test_confirm_non_existing_order_returns_none(self, use_case):
        """Test confirming non-existing order returns None."""
        non_existing_id = uuid4()
        
        result = use_case.execute(non_existing_id)
        
        assert result is None
```

## Integration Testing

Integration tests verify that adapters work correctly with real external systems.

### Testing Database Repository

```python
# tests/integration/test_sqlmodel_order_repository.py
import pytest
from uuid import uuid4
from sqlmodel import Session, SQLModel, create_engine

from adapters.output.repositories import SQLModelOrderRepository, OrderModel
from domain.entities import Order


@pytest.fixture
def engine():
    """Create in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(engine):
    """Create database session."""
    with Session(engine) as session:
        yield session


@pytest.fixture
def repository(session):
    """Create repository with test session."""
    return SQLModelOrderRepository(session)


class TestSQLModelOrderRepository:
    """Integration tests for SQLModelOrderRepository."""
    
    def test_save_and_find_order(self, repository):
        """Test saving and finding an order."""
        # Arrange
        order = Order.create(uuid4(), 100.0)
        
        # Act
        repository.save(order)
        found_order = repository.find_by_id(order.id)
        
        # Assert
        assert found_order is not None
        assert found_order.id == order.id
        assert found_order.customer_id == order.customer_id
        assert found_order.total_amount == order.total_amount
    
    def test_find_non_existing_order_returns_none(self, repository):
        """Test finding non-existing order returns None."""
        non_existing_id = uuid4()
        
        found_order = repository.find_by_id(non_existing_id)
        
        assert found_order is None
    
    def test_update_existing_order(self, repository):
        """Test updating an existing order."""
        # Arrange
        order = Order.create(uuid4(), 100.0)
        repository.save(order)
        
        # Act - Modify and save again
        order.confirm()
        repository.save(order)
        
        # Assert
        found_order = repository.find_by_id(order.id)
        assert found_order.status == "confirmed"
    
    def test_find_by_customer(self, repository):
        """Test finding orders by customer."""
        # Arrange
        customer_id = uuid4()
        order1 = Order.create(customer_id, 100.0)
        order2 = Order.create(customer_id, 200.0)
        order3 = Order.create(uuid4(), 300.0)  # Different customer
        
        repository.save(order1)
        repository.save(order2)
        repository.save(order3)
        
        # Act
        orders = repository.find_by_customer(customer_id)
        
        # Assert
        assert len(orders) == 2
        assert all(order.customer_id == customer_id for order in orders)
    
    def test_delete_order(self, repository):
        """Test deleting an order."""
        # Arrange
        order = Order.create(uuid4(), 100.0)
        repository.save(order)
        
        # Act
        repository.delete(order.id)
        
        # Assert
        found_order = repository.find_by_id(order.id)
        assert found_order is None
```

### Testing API Endpoints

```python
# tests/integration/test_rest_api.py
import pytest
from uuid import uuid4
from fastapi.testclient import TestClient

from main import app
from tests.fakes.repositories import FakeOrderRepository
from ports.output import OrderRepository


@pytest.fixture
def fake_repository():
    """Provide fake repository."""
    return FakeOrderRepository()


@pytest.fixture
def client(fake_repository):
    """Provide test client with fake repository."""
    # Override dependency
    app.dependency_overrides[OrderRepository] = lambda: fake_repository
    
    with TestClient(app) as client:
        yield client
    
    # Clear overrides
    app.dependency_overrides.clear()


class TestOrderAPI:
    """Integration tests for Order API."""
    
    def test_create_order(self, client):
        """Test creating an order via API."""
        customer_id = str(uuid4())
        
        response = client.post(
            "/api/orders/",
            json={
                "customer_id": customer_id,
                "total_amount": 150.0,
            }
        )
        
        assert response.status_code == 201
        
        data = response.json()
        assert data["customer_id"] == customer_id
        assert data["total_amount"] == 150.0
        assert data["status"] == "pending"
    
    def test_get_existing_order(self, client, fake_repository):
        """Test getting an existing order."""
        # Arrange
        from domain.entities import Order
        order = Order.create(uuid4(), 100.0)
        fake_repository.save(order)
        
        # Act
        response = client.get(f"/api/orders/{order.id}")
        
        # Assert
        assert response.status_code == 200
        
        data = response.json()
        assert data["id"] == str(order.id)
        assert data["total_amount"] == 100.0
    
    def test_get_non_existing_order_returns_404(self, client):
        """Test getting non-existing order returns 404."""
        non_existing_id = uuid4()
        
        response = client.get(f"/api/orders/{non_existing_id}")
        
        assert response.status_code == 404
    
    def test_confirm_order(self, client, fake_repository):
        """Test confirming an order."""
        # Arrange
        from domain.entities import Order
        order = Order.create(uuid4(), 100.0)
        fake_repository.save(order)
        
        # Act
        response = client.post(f"/api/orders/{order.id}/confirm")
        
        # Assert
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "confirmed"
```

## Testing with Pytest Plugins

### Using pytest-asyncio for Async Tests

```python
# tests/integration/test_async_repository.py
import pytest
from uuid import uuid4

from adapters.output.async_repositories import AsyncOrderRepository
from domain.entities import Order


@pytest.mark.asyncio
async def test_async_save_and_find_order(async_repository):
    """Test async repository operations."""
    order = Order.create(uuid4(), 100.0)
    
    await async_repository.save(order)
    found_order = await async_repository.find_by_id(order.id)
    
    assert found_order is not None
    assert found_order.id == order.id
```

### Using pytest-mock for Mocking

```python
# tests/unit/test_with_mocks.py
import pytest
from uuid import uuid4
from unittest.mock import Mock

from application.use_cases import ConfirmOrder


def test_confirm_order_with_mock(mocker):
    """Test using pytest-mock."""
    # Create mocks
    mock_repository = mocker.Mock()
    mock_notification = mocker.Mock()
    
    # Setup mock behavior
    order = Order.create(uuid4(), 100.0)
    mock_repository.find_by_id.return_value = order
    
    # Execute
    use_case = ConfirmOrder(mock_repository, mock_notification)
    result = use_case.execute(order.id)
    
    # Verify
    mock_repository.find_by_id.assert_called_once_with(order.id)
    mock_repository.save.assert_called_once()
    mock_notification.send_order_confirmation.assert_called_once_with(order)
```

## Test Coverage

Run tests with coverage:

```bash
# Run tests with coverage
pytest --cov=domain --cov=application --cov=adapters --cov-report=html

# View coverage report
open htmlcov/index.html
```

## Test Organization Best Practices

### 1. Follow AAA Pattern

**Arrange, Act, Assert:**

```python
def test_create_order():
    # Arrange
    customer_id = uuid4()
    repository = FakeOrderRepository()
    use_case = CreateOrder(repository)
    
    # Act
    order = use_case.execute(customer_id, 100.0)
    
    # Assert
    assert order.customer_id == customer_id
```

### 2. Use Descriptive Test Names

```python
# ✅ Good - Descriptive names
def test_create_order_with_negative_amount_raises_value_error()
def test_confirm_pending_order_changes_status_to_confirmed()
def test_find_by_customer_returns_only_customer_orders()

# ❌ Bad - Vague names
def test_order()
def test_1()
def test_error()
```

### 3. One Assertion Per Test (When Possible)

```python
# ✅ Good - Focused test
def test_order_status_is_pending_when_created():
    order = Order.create(uuid4(), 100.0)
    assert order.status == "pending"

def test_order_id_is_uuid_when_created():
    order = Order.create(uuid4(), 100.0)
    assert isinstance(order.id, type(uuid4()))


# ❌ Bad - Multiple unrelated assertions
def test_order_creation():
    order = Order.create(uuid4(), 100.0)
    assert order.status == "pending"
    assert isinstance(order.id, type(uuid4()))
    assert order.created_at is not None
```

### 4. Use Parametrize for Similar Tests

```python
@pytest.mark.parametrize("amount,expected_tax", [
    (100.0, 8.0),
    (200.0, 16.0),
    (50.0, 4.0),
])
def test_calculate_tax(amount, expected_tax, pricing_service):
    """Test tax calculation with different amounts."""
    money = Money(amount, Currency.USD)
    tax = pricing_service._calculate_tax(money)
    assert tax.amount == expected_tax
```

## Testing Checklist

- ✅ Domain entities have unit tests
- ✅ Value objects are tested for immutability
- ✅ Domain services are tested with various inputs
- ✅ Use cases are tested with fake adapters
- ✅ Each adapter has integration tests
- ✅ API endpoints have integration tests
- ✅ Error cases are tested
- ✅ Edge cases are covered
- ✅ Test coverage > 80%

This comprehensive testing guide ensures your hexagonal architecture is robust and maintainable! 🎯
