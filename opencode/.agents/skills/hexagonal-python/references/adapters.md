# Adapters Patterns

Adapters are **concrete implementations** of ports. They connect your application to external systems like databases, APIs, message queues, and user interfaces. Adapters translate between your domain model and external technologies.

## Types of Adapters

### Input Adapters (Primary/Driving)

**Purpose:** Allow external actors to interact with your application

**Examples:**
- REST API endpoints (FastAPI, Flask)
- GraphQL resolvers
- CLI commands (Click, Typer)
- Message queue consumers (RabbitMQ, Kafka)
- Web UI controllers
- Scheduled jobs (APScheduler, Celery)

### Output Adapters (Secondary/Driven)

**Purpose:** Allow your application to interact with external systems

**Examples:**
- Database repositories (SQLAlchemy, SQLModel, MongoDB)
- External API clients (HTTP, gRPC)
- Message publishers (RabbitMQ, Kafka)
- File storage (S3, local filesystem)
- Email services (SMTP, SendGrid)
- Cache services (Redis, Memcached)

## Output Adapters

### Database Repository Adapter (SQLModel)

```python
# adapters/output/repositories.py
from typing import Optional, List
from uuid import UUID

from sqlmodel import Session, select, SQLModel, Field

from domain.entities import Order
from ports.output import OrderRepository


# ORM Model (infrastructure layer)
class OrderModel(SQLModel, table=True):
    """SQLModel for order persistence."""
    __tablename__ = "orders"
    
    id: UUID = Field(primary_key=True)
    customer_id: UUID
    total_amount: float
    status: str
    created_at: str
    updated_at: Optional[str] = None


# Repository Adapter
class SQLModelOrderRepository(OrderRepository):
    """SQLModel implementation of OrderRepository port."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, order: Order) -> None:
        """Save order to database."""
        # Check if order exists
        existing = self.session.get(OrderModel, order.id)
        
        if existing:
            # Update existing
            existing.customer_id = order.customer_id
            existing.total_amount = order.total_amount
            existing.status = order.status
            existing.updated_at = order.updated_at.isoformat() if order.updated_at else None
        else:
            # Create new
            db_order = OrderModel(
                id=order.id,
                customer_id=order.customer_id,
                total_amount=order.total_amount,
                status=order.status,
                created_at=order.created_at.isoformat(),
                updated_at=order.updated_at.isoformat() if order.updated_at else None,
            )
            self.session.add(db_order)
        
        self.session.commit()
    
    def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """Find order by ID."""
        db_order = self.session.get(OrderModel, order_id)
        
        if not db_order:
            return None
        
        return self._to_domain(db_order)
    
    def find_by_customer(self, customer_id: UUID) -> List[Order]:
        """Find all orders for a customer."""
        statement = select(OrderModel).where(OrderModel.customer_id == customer_id)
        db_orders = self.session.exec(statement).all()
        
        return [self._to_domain(db_order) for db_order in db_orders]
    
    def find_by_status(self, status: str) -> List[Order]:
        """Find orders by status."""
        statement = select(OrderModel).where(OrderModel.status == status)
        db_orders = self.session.exec(statement).all()
        
        return [self._to_domain(db_order) for db_order in db_orders]
    
    def delete(self, order_id: UUID) -> None:
        """Delete an order."""
        db_order = self.session.get(OrderModel, order_id)
        
        if db_order:
            self.session.delete(db_order)
            self.session.commit()
    
    def _to_domain(self, db_order: OrderModel) -> Order:
        """Convert ORM model to domain entity."""
        from datetime import datetime
        
        return Order(
            id=db_order.id,
            customer_id=db_order.customer_id,
            total_amount=db_order.total_amount,
            status=db_order.status,
            created_at=datetime.fromisoformat(db_order.created_at),
            updated_at=datetime.fromisoformat(db_order.updated_at) if db_order.updated_at else None,
        )
```

### MongoDB Repository Adapter

```python
from typing import Optional, List
from uuid import UUID

from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument

from domain.entities import Order
from ports.output import OrderRepository


class MongoOrderRepository(OrderRepository):
    """MongoDB implementation of OrderRepository port."""
    
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.orders
    
    async def save(self, order: Order) -> None:
        """Save order to MongoDB."""
        document = {
            "_id": str(order.id),
            "customer_id": str(order.customer_id),
            "total_amount": order.total_amount,
            "status": order.status,
            "created_at": order.created_at.isoformat(),
            "updated_at": order.updated_at.isoformat() if order.updated_at else None,
        }
        
        await self.collection.update_one(
            {"_id": str(order.id)},
            {"$set": document},
            upsert=True,
        )
    
    async def find_by_id(self, order_id: UUID) -> Optional[Order]:
        """Find order by ID."""
        document = await self.collection.find_one({"_id": str(order_id)})
        
        if not document:
            return None
        
        return self._to_domain(document)
    
    async def find_by_customer(self, customer_id: UUID) -> List[Order]:
        """Find all orders for a customer."""
        cursor = self.collection.find({"customer_id": str(customer_id)})
        documents = await cursor.to_list(length=None)
        
        return [self._to_domain(doc) for doc in documents]
    
    async def delete(self, order_id: UUID) -> None:
        """Delete an order."""
        await self.collection.delete_one({"_id": str(order_id)})
    
    def _to_domain(self, document: dict) -> Order:
        """Convert MongoDB document to domain entity."""
        from datetime import datetime
        
        return Order(
            id=UUID(document["_id"]),
            customer_id=UUID(document["customer_id"]),
            total_amount=document["total_amount"],
            status=document["status"],
            created_at=datetime.fromisoformat(document["created_at"]),
            updated_at=datetime.fromisoformat(document["updated_at"]) if document.get("updated_at") else None,
        )
```

### External API Client Adapter

```python
# adapters/output/external_api.py
from typing import Optional
import httpx

from domain.value_objects import Money, Currency
from ports.output import PaymentGateway


class StripePaymentGateway(PaymentGateway):
    """Stripe implementation of PaymentGateway port."""
    
    def __init__(self, api_key: str, base_url: str = "https://api.stripe.com/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/x-www-form-urlencoded",
            }
        )
    
    async def charge(self, amount: Money, payment_method: str) -> PaymentResult:
        """Charge a payment method using Stripe."""
        try:
            response = await self.client.post(
                f"{self.base_url}/payment_intents",
                data={
                    "amount": int(amount.amount * 100),  # Stripe uses cents
                    "currency": amount.currency.value.lower(),
                    "payment_method": payment_method,
                    "confirm": True,
                }
            )
            response.raise_for_status()
            
            data = response.json()
            
            return PaymentResult(
                transaction_id=data["id"],
                status="success",
                amount=amount,
            )
        
        except httpx.HTTPStatusError as e:
            error_data = e.response.json()
            return PaymentResult(
                transaction_id=None,
                status="failed",
                amount=amount,
                error_message=error_data.get("error", {}).get("message"),
            )
    
    async def refund(self, transaction_id: str, amount: Money) -> RefundResult:
        """Refund a transaction using Stripe."""
        response = await self.client.post(
            f"{self.base_url}/refunds",
            data={
                "payment_intent": transaction_id,
                "amount": int(amount.amount * 100),
            }
        )
        response.raise_for_status()
        
        data = response.json()
        
        return RefundResult(
            refund_id=data["id"],
            status=data["status"],
            amount=amount,
        )
    
    async def get_transaction_status(self, transaction_id: str) -> str:
        """Get transaction status from Stripe."""
        response = await self.client.get(
            f"{self.base_url}/payment_intents/{transaction_id}"
        )
        response.raise_for_status()
        
        data = response.json()
        return data["status"]
```

### Email Service Adapter

```python
# adapters/output/notifications.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from domain.entities import Order
from ports.output import NotificationService


class SMTPNotificationService(NotificationService):
    """SMTP implementation of NotificationService port."""
    
    def __init__(self, host: str, port: int, username: str, password: str):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
    
    def send_email(self, to: str, subject: str, body: str) -> None:
        """Send email using SMTP."""
        message = MIMEMultipart()
        message["From"] = self.username
        message["To"] = to
        message["Subject"] = subject
        
        message.attach(MIMEText(body, "plain"))
        
        with smtplib.SMTP(self.host, self.port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.send_message(message)
    
    def send_order_confirmation(self, order: Order) -> None:
        """Send order confirmation email."""
        subject = f"Order Confirmation - {order.id}"
        body = f"""
        Thank you for your order!
        
        Order ID: {order.id}
        Status: {order.status}
        Total: ${order.total_amount:.2f}
        
        We'll notify you when your order ships.
        """
        
        # In real implementation, you'd fetch customer email
        customer_email = "customer@example.com"
        
        self.send_email(customer_email, subject, body)


# Alternative: Third-party service adapter
class SendGridNotificationService(NotificationService):
    """SendGrid implementation of NotificationService port."""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.AsyncClient(
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }
        )
    
    async def send_email(self, to: str, subject: str, body: str) -> None:
        """Send email using SendGrid API."""
        await self.client.post(
            "https://api.sendgrid.com/v3/mail/send",
            json={
                "personalizations": [{"to": [{"email": to}]}],
                "from": {"email": "noreply@example.com"},
                "subject": subject,
                "content": [{"type": "text/plain", "value": body}],
            }
        )
```

### Event Publisher Adapter

```python
# adapters/output/events.py
import json
from typing import List

from domain.events import DomainEvent
from ports.output import EventPublisher


class RabbitMQEventPublisher(EventPublisher):
    """RabbitMQ implementation of EventPublisher port."""
    
    def __init__(self, connection):
        self.connection = connection
        self.channel = connection.channel()
        self.exchange = "domain_events"
        
        # Declare exchange
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type="topic",
            durable=True,
        )
    
    def publish(self, event: DomainEvent) -> None:
        """Publish a single domain event."""
        routing_key = f"{event.__class__.__module__}.{event.__class__.__name__}"
        
        message = json.dumps({
            "event_type": event.__class__.__name__,
            "data": self._serialize_event(event),
            "occurred_at": event.occurred_at.isoformat(),
        })
        
        self.channel.basic_publish(
            exchange=self.exchange,
            routing_key=routing_key,
            body=message,
        )
    
    def publish_batch(self, events: List[DomainEvent]) -> None:
        """Publish multiple domain events."""
        for event in events:
            self.publish(event)
    
    def _serialize_event(self, event: DomainEvent) -> dict:
        """Serialize event to dictionary."""
        from dataclasses import asdict
        event_dict = asdict(event)
        
        # Convert UUIDs to strings
        for key, value in event_dict.items():
            if hasattr(value, 'hex'):  # UUID
                event_dict[key] = str(value)
        
        return event_dict


class InMemoryEventPublisher(EventPublisher):
    """In-memory implementation for testing."""
    
    def __init__(self):
        self.published_events: List[DomainEvent] = []
    
    def publish(self, event: DomainEvent) -> None:
        """Store event in memory."""
        self.published_events.append(event)
    
    def publish_batch(self, events: List[DomainEvent]) -> None:
        """Store multiple events in memory."""
        self.published_events.extend(events)
    
    def clear(self) -> None:
        """Clear all published events."""
        self.published_events.clear()
```

### Cache Adapter

```python
# adapters/output/cache.py
from typing import Any, Optional
import json
import redis

from ports.output import CacheService


class RedisCacheService(CacheService):
    """Redis implementation of CacheService port."""
    
    def __init__(self, redis_client: redis.Redis):
        self.client = redis_client
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis cache."""
        value = self.client.get(key)
        
        if value is None:
            return None
        
        return json.loads(value)
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        """Set value in Redis cache with optional TTL."""
        serialized = json.dumps(value)
        
        if ttl_seconds:
            self.client.setex(key, ttl_seconds, serialized)
        else:
            self.client.set(key, serialized)
    
    def delete(self, key: str) -> None:
        """Delete value from Redis cache."""
        self.client.delete(key)
    
    def exists(self, key: str) -> bool:
        """Check if key exists in Redis cache."""
        return bool(self.client.exists(key))
    
    def clear(self) -> None:
        """Clear all cache entries."""
        self.client.flushdb()


class InMemoryCacheService(CacheService):
    """In-memory implementation for testing."""
    
    def __init__(self):
        self._cache: dict[str, Any] = {}
    
    def get(self, key: str) -> Optional[Any]:
        return self._cache.get(key)
    
    def set(self, key: str, value: Any, ttl_seconds: Optional[int] = None) -> None:
        # TTL not implemented for simplicity
        self._cache[key] = value
    
    def delete(self, key: str) -> None:
        self._cache.pop(key, None)
    
    def exists(self, key: str) -> bool:
        return key in self._cache
    
    def clear(self) -> None:
        self._cache.clear()
```

## Input Adapters

### REST API Adapter (FastAPI)

```python
# adapters/input/rest_api.py
from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from ports.input import (
    CreateOrderUseCase,
    ConfirmOrderUseCase,
    GetOrderQuery,
    ListOrdersQuery,
)


router = APIRouter(prefix="/api/orders", tags=["orders"])


# Request/Response DTOs (Data Transfer Objects)
class OrderItemRequest(BaseModel):
    """Request model for order item."""
    product_id: UUID
    quantity: int = Field(gt=0)


class CreateOrderRequest(BaseModel):
    """Request model for creating an order."""
    customer_id: UUID
    items: List[OrderItemRequest]


class OrderResponse(BaseModel):
    """Response model for order."""
    id: UUID
    customer_id: UUID
    total_amount: float
    status: str


# Endpoints
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    request: CreateOrderRequest,
    use_case: Annotated[CreateOrderUseCase, Depends()],
) -> OrderResponse:
    """Create a new order."""
    from application.use_cases import CreateOrderCommand, OrderItemData
    
    command = CreateOrderCommand(
        customer_id=request.customer_id,
        items=[
            OrderItemData(product_id=item.product_id, quantity=item.quantity)
            for item in request.items
        ],
    )
    
    order = use_case.execute(command)
    
    return OrderResponse(
        id=order.id,
        customer_id=order.customer_id,
        total_amount=order.total_amount,
        status=order.status,
    )


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: UUID,
    query: Annotated[GetOrderQuery, Depends()],
) -> OrderResponse:
    """Get an order by ID."""
    order = query.execute(order_id)
    
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


@router.get("/", response_model=List[OrderResponse])
async def list_orders(
    customer_id: UUID,
    query: Annotated[ListOrdersQuery, Depends()],
) -> List[OrderResponse]:
    """List orders for a customer."""
    orders = query.execute(customer_id)
    
    return [
        OrderResponse(
            id=order.id,
            customer_id=order.customer_id,
            total_amount=order.total_amount,
            status=order.status,
        )
        for order in orders
    ]
```

### CLI Adapter (Typer)

```python
# adapters/input/cli.py
from uuid import UUID
import typer

from config.dependencies import (
    get_create_order_use_case,
    get_confirm_order_use_case,
    get_list_orders_query,
)


app = typer.Typer()


@app.command()
def create_order(
    customer_id: UUID,
    product_id: UUID,
    quantity: int = typer.Option(1, help="Quantity to order"),
):
    """Create a new order."""
    from application.use_cases import CreateOrderCommand, OrderItemData
    
    use_case = get_create_order_use_case()
    
    command = CreateOrderCommand(
        customer_id=customer_id,
        items=[OrderItemData(product_id=product_id, quantity=quantity)],
    )
    
    order = use_case.execute(command)
    
    typer.echo(f"✅ Order created: {order.id}")
    typer.echo(f"   Status: {order.status}")
    typer.echo(f"   Total: ${order.total_amount:.2f}")


@app.command()
def confirm_order(order_id: UUID):
    """Confirm an order."""
    use_case = get_confirm_order_use_case()
    
    order = use_case.execute(order_id)
    
    if not order:
        typer.echo(f"❌ Order {order_id} not found", err=True)
        raise typer.Exit(1)
    
    typer.echo(f"✅ Order confirmed: {order.id}")
    typer.echo(f"   Status: {order.status}")


@app.command()
def list_orders(customer_id: UUID):
    """List orders for a customer."""
    query = get_list_orders_query()
    
    orders = query.execute(customer_id)
    
    if not orders:
        typer.echo("No orders found")
        return
    
    typer.echo(f"Orders for customer {customer_id}:")
    for order in orders:
        typer.echo(f"  • {order.id} - {order.status} - ${order.total_amount:.2f}")


if __name__ == "__main__":
    app()
```

### Message Consumer Adapter

```python
# adapters/input/message_consumer.py
import json
from typing import Callable

from ports.input import CreateOrderUseCase


class OrderMessageConsumer:
    """RabbitMQ consumer for order messages."""
    
    def __init__(self, connection, create_order_use_case: CreateOrderUseCase):
        self.connection = connection
        self.channel = connection.channel()
        self.create_order_use_case = create_order_use_case
        
        # Declare queue
        self.queue_name = "orders.create"
        self.channel.queue_declare(queue=self.queue_name, durable=True)
    
    def start(self) -> None:
        """Start consuming messages."""
        self.channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=self._handle_message,
            auto_ack=False,
        )
        
        print(f"Starting to consume from {self.queue_name}")
        self.channel.start_consuming()
    
    def _handle_message(self, ch, method, properties, body) -> None:
        """Handle incoming message."""
        try:
            data = json.loads(body)
            
            # Convert to command
            from application.use_cases import CreateOrderCommand, OrderItemData
            
            command = CreateOrderCommand(
                customer_id=UUID(data["customer_id"]),
                items=[
                    OrderItemData(
                        product_id=UUID(item["product_id"]),
                        quantity=item["quantity"],
                    )
                    for item in data["items"]
                ],
            )
            
            # Execute use case
            order = self.create_order_use_case.execute(command)
            
            print(f"✅ Created order: {order.id}")
            
            # Acknowledge message
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        except Exception as e:
            print(f"❌ Error processing message: {e}")
            # Reject and requeue
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
```

## Adapter Best Practices

### 1. Keep Adapters Thin

Adapters should only translate between external systems and domain:

```python
# ✅ Good - Thin adapter
@router.post("/orders")
async def create_order(
    request: CreateOrderRequest,
    use_case: Annotated[CreateOrderUseCase, Depends()],
):
    order = use_case.execute(request.to_command())
    return OrderResponse.from_domain(order)


# ❌ Bad - Fat adapter with business logic
@router.post("/orders")
async def create_order(request: CreateOrderRequest, db: Session):
    # Business logic in adapter!
    if request.total_amount < 0:
        raise HTTPException(400)
    
    order = Order(...)
    db.add(order)
    db.commit()
```

### 2. Separate ORM Models from Domain Entities

```python
# ✅ Good - Separate models
class OrderModel(SQLModel, table=True):
    """ORM model."""
    id: UUID
    ...

class Order:
    """Domain entity."""
    id: UUID
    ...

# Adapter converts between them
def _to_domain(self, orm_model: OrderModel) -> Order:
    return Order(...)


# ❌ Bad - Same class for both
class Order(SQLModel, table=True):
    """Domain entity mixed with ORM!"""
    id: UUID
    ...
```

### 3. Handle Adapter-Specific Errors

```python
# ✅ Good - Convert infrastructure errors to domain errors
class SQLModelOrderRepository(OrderRepository):
    def save(self, order: Order) -> None:
        try:
            # Database operation
            self.session.add(orm_order)
            self.session.commit()
        except IntegrityError as e:
            raise DuplicateOrderException(order.id) from e
        except DatabaseError as e:
            raise RepositoryException("Failed to save order") from e


# ❌ Bad - Let infrastructure errors leak
class SQLModelOrderRepository(OrderRepository):
    def save(self, order: Order) -> None:
        # Infrastructure exception leaks to application!
        self.session.add(orm_order)
        self.session.commit()
```

### 4. Use DTOs for API Boundaries

```python
# ✅ Good - Use Pydantic models for API
class OrderResponse(BaseModel):
    """API response DTO."""
    id: UUID
    status: str
    
    @classmethod
    def from_domain(cls, order: Order) -> "OrderResponse":
        return cls(id=order.id, status=order.status)


# ❌ Bad - Return domain entities directly
@router.get("/orders/{id}")
async def get_order(id: UUID) -> Order:  # Don't expose domain!
    return order_repository.find_by_id(id)
```

This comprehensive guide covers all major adapter patterns for hexagonal architecture in Python! 🚀
