# Complete Example Project: Task Management System

This is a complete, working example of a task management system built with hexagonal architecture in Python. You can use this as a template for your own projects.

## Project Overview

A simple task management system that allows users to:
- Create tasks
- Mark tasks as completed
- List tasks by user
- Get task statistics

## Project Structure

```
task_manager/
├── domain/
│   ├── __init__.py
│   ├── entities.py
│   ├── value_objects.py
│   └── exceptions.py
├── application/
│   ├── __init__.py
│   └── use_cases.py
├── ports/
│   ├── __init__.py
│   ├── input.py
│   └── output.py
├── adapters/
│   ├── __init__.py
│   ├── input/
│   │   ├── __init__.py
│   │   ├── rest_api.py
│   │   └── cli.py
│   └── output/
│       ├── __init__.py
│       ├── repositories.py
│       └── models.py
├── config/
│   ├── __init__.py
│   ├── database.py
│   └── dependencies.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── fakes/
├── main.py
├── pyproject.toml
└── README.md
```

## Implementation

### Domain Layer

#### Entities

```python
# domain/entities.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from domain.exceptions import InvalidOperationException


@dataclass
class Task:
    """Task entity representing a user task."""
    id: UUID
    user_id: UUID
    title: str
    description: str
    is_completed: bool
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    @staticmethod
    def create(user_id: UUID, title: str, description: str = "") -> "Task":
        """Factory method to create a new task."""
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        
        if len(title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")
        
        return Task(
            id=uuid4(),
            user_id=user_id,
            title=title.strip(),
            description=description.strip(),
            is_completed=False,
            created_at=datetime.now(),
        )
    
    def complete(self) -> None:
        """Mark task as completed."""
        if self.is_completed:
            raise InvalidOperationException("Task is already completed")
        
        self.is_completed = True
        self.completed_at = datetime.now()
    
    def reopen(self) -> None:
        """Reopen a completed task."""
        if not self.is_completed:
            raise InvalidOperationException("Task is not completed")
        
        self.is_completed = False
        self.completed_at = None
    
    def update(self, title: Optional[str] = None, description: Optional[str] = None) -> None:
        """Update task details."""
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            self.title = title.strip()
        
        if description is not None:
            self.description = description.strip()
```

#### Value Objects

```python
# domain/value_objects.py
from dataclasses import dataclass


@dataclass(frozen=True)
class TaskStatistics:
    """Value object representing task statistics."""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_rate: float
    
    def __post_init__(self):
        """Validate statistics."""
        if self.total_tasks < 0:
            raise ValueError("Total tasks cannot be negative")
        
        if self.completed_tasks < 0:
            raise ValueError("Completed tasks cannot be negative")
        
        if self.pending_tasks < 0:
            raise ValueError("Pending tasks cannot be negative")
        
        if not 0 <= self.completion_rate <= 100:
            raise ValueError("Completion rate must be between 0 and 100")
    
    @staticmethod
    def calculate(total: int, completed: int) -> "TaskStatistics":
        """Calculate statistics from totals."""
        pending = total - completed
        rate = (completed / total * 100) if total > 0 else 0.0
        
        return TaskStatistics(
            total_tasks=total,
            completed_tasks=completed,
            pending_tasks=pending,
            completion_rate=round(rate, 2),
        )
```

#### Exceptions

```python
# domain/exceptions.py
class DomainException(Exception):
    """Base exception for domain errors."""
    pass


class TaskNotFoundException(DomainException):
    """Raised when a task is not found."""
    
    def __init__(self, task_id: str):
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")


class InvalidOperationException(DomainException):
    """Raised when an operation is not allowed."""
    pass
```

### Ports

#### Output Ports

```python
# ports/output.py
from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from domain.entities import Task


class TaskRepository(ABC):
    """Port for task persistence."""
    
    @abstractmethod
    def save(self, task: Task) -> None:
        """Save a task."""
        pass
    
    @abstractmethod
    def find_by_id(self, task_id: UUID) -> Optional[Task]:
        """Find task by ID."""
        pass
    
    @abstractmethod
    def find_by_user(self, user_id: UUID) -> List[Task]:
        """Find all tasks for a user."""
        pass
    
    @abstractmethod
    def find_by_user_and_status(self, user_id: UUID, is_completed: bool) -> List[Task]:
        """Find tasks by user and completion status."""
        pass
    
    @abstractmethod
    def count_by_user(self, user_id: UUID) -> int:
        """Count total tasks for a user."""
        pass
    
    @abstractmethod
    def count_by_user_and_status(self, user_id: UUID, is_completed: bool) -> int:
        """Count tasks by user and status."""
        pass
    
    @abstractmethod
    def delete(self, task_id: UUID) -> None:
        """Delete a task."""
        pass
```

#### Input Ports

```python
# ports/input.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional
from uuid import UUID

from domain.entities import Task
from domain.value_objects import TaskStatistics


@dataclass
class CreateTaskCommand:
    """Command to create a task."""
    user_id: UUID
    title: str
    description: str = ""


class CreateTaskUseCase(ABC):
    """Use case for creating a task."""
    
    @abstractmethod
    def execute(self, command: CreateTaskCommand) -> Task:
        """Execute create task use case."""
        pass


class CompleteTaskUseCase(ABC):
    """Use case for completing a task."""
    
    @abstractmethod
    def execute(self, task_id: UUID) -> Optional[Task]:
        """Execute complete task use case."""
        pass


class ListTasksQuery(ABC):
    """Query for listing tasks."""
    
    @abstractmethod
    def execute(self, user_id: UUID, only_pending: bool = False) -> List[Task]:
        """Execute list tasks query."""
        pass


class GetTaskStatisticsQuery(ABC):
    """Query for getting task statistics."""
    
    @abstractmethod
    def execute(self, user_id: UUID) -> TaskStatistics:
        """Execute get statistics query."""
        pass
```

### Application Layer

```python
# application/use_cases.py
from typing import List, Optional
from uuid import UUID

from domain.entities import Task
from domain.value_objects import TaskStatistics
from domain.exceptions import TaskNotFoundException
from ports.input import (
    CreateTaskCommand,
    CreateTaskUseCase,
    CompleteTaskUseCase,
    ListTasksQuery,
    GetTaskStatisticsQuery,
)
from ports.output import TaskRepository


class CreateTask(CreateTaskUseCase):
    """Implementation of CreateTask use case."""
    
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    
    def execute(self, command: CreateTaskCommand) -> Task:
        """Create and save a new task."""
        task = Task.create(
            user_id=command.user_id,
            title=command.title,
            description=command.description,
        )
        
        self.repository.save(task)
        
        return task


class CompleteTask(CompleteTaskUseCase):
    """Implementation of CompleteTask use case."""
    
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    
    def execute(self, task_id: UUID) -> Optional[Task]:
        """Complete a task."""
        task = self.repository.find_by_id(task_id)
        
        if not task:
            return None
        
        task.complete()
        self.repository.save(task)
        
        return task


class ListTasks(ListTasksQuery):
    """Implementation of ListTasks query."""
    
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    
    def execute(self, user_id: UUID, only_pending: bool = False) -> List[Task]:
        """List tasks for a user."""
        if only_pending:
            return self.repository.find_by_user_and_status(user_id, is_completed=False)
        
        return self.repository.find_by_user(user_id)


class GetTaskStatistics(GetTaskStatisticsQuery):
    """Implementation of GetTaskStatistics query."""
    
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    
    def execute(self, user_id: UUID) -> TaskStatistics:
        """Get statistics for a user."""
        total = self.repository.count_by_user(user_id)
        completed = self.repository.count_by_user_and_status(user_id, is_completed=True)
        
        return TaskStatistics.calculate(total, completed)
```

### Adapters

#### Database Models

```python
# adapters/output/models.py
from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import SQLModel, Field


class TaskModel(SQLModel, table=True):
    """SQLModel for task persistence."""
    __tablename__ = "tasks"
    
    id: UUID = Field(primary_key=True)
    user_id: UUID = Field(index=True)
    title: str = Field(max_length=200)
    description: str = Field(default="")
    is_completed: bool = Field(default=False, index=True)
    created_at: datetime
    completed_at: Optional[datetime] = None
```

#### Repository Implementation

```python
# adapters/output/repositories.py
from typing import List, Optional
from uuid import UUID

from sqlmodel import Session, select

from adapters.output.models import TaskModel
from domain.entities import Task
from ports.output import TaskRepository


class SQLModelTaskRepository(TaskRepository):
    """SQLModel implementation of TaskRepository."""
    
    def __init__(self, session: Session):
        self.session = session
    
    def save(self, task: Task) -> None:
        """Save task to database."""
        existing = self.session.get(TaskModel, task.id)
        
        if existing:
            # Update existing
            existing.user_id = task.user_id
            existing.title = task.title
            existing.description = task.description
            existing.is_completed = task.is_completed
            existing.completed_at = task.completed_at
        else:
            # Create new
            db_task = TaskModel(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                is_completed=task.is_completed,
                created_at=task.created_at,
                completed_at=task.completed_at,
            )
            self.session.add(db_task)
        
        self.session.commit()
    
    def find_by_id(self, task_id: UUID) -> Optional[Task]:
        """Find task by ID."""
        db_task = self.session.get(TaskModel, task_id)
        
        if not db_task:
            return None
        
        return self._to_domain(db_task)
    
    def find_by_user(self, user_id: UUID) -> List[Task]:
        """Find all tasks for a user."""
        statement = select(TaskModel).where(TaskModel.user_id == user_id)
        db_tasks = self.session.exec(statement).all()
        
        return [self._to_domain(db_task) for db_task in db_tasks]
    
    def find_by_user_and_status(self, user_id: UUID, is_completed: bool) -> List[Task]:
        """Find tasks by user and status."""
        statement = (
            select(TaskModel)
            .where(TaskModel.user_id == user_id)
            .where(TaskModel.is_completed == is_completed)
        )
        db_tasks = self.session.exec(statement).all()
        
        return [self._to_domain(db_task) for db_task in db_tasks]
    
    def count_by_user(self, user_id: UUID) -> int:
        """Count tasks for a user."""
        statement = select(TaskModel).where(TaskModel.user_id == user_id)
        return len(self.session.exec(statement).all())
    
    def count_by_user_and_status(self, user_id: UUID, is_completed: bool) -> int:
        """Count tasks by user and status."""
        statement = (
            select(TaskModel)
            .where(TaskModel.user_id == user_id)
            .where(TaskModel.is_completed == is_completed)
        )
        return len(self.session.exec(statement).all())
    
    def delete(self, task_id: UUID) -> None:
        """Delete a task."""
        db_task = self.session.get(TaskModel, task_id)
        
        if db_task:
            self.session.delete(db_task)
            self.session.commit()
    
    def _to_domain(self, db_task: TaskModel) -> Task:
        """Convert ORM model to domain entity."""
        return Task(
            id=db_task.id,
            user_id=db_task.user_id,
            title=db_task.title,
            description=db_task.description,
            is_completed=db_task.is_completed,
            created_at=db_task.created_at,
            completed_at=db_task.completed_at,
        )
```

#### REST API

```python
# adapters/input/rest_api.py
from typing import Annotated, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from pydantic import BaseModel, Field

from ports.input import (
    CreateTaskCommand,
    CreateTaskUseCase,
    CompleteTaskUseCase,
    ListTasksQuery,
    GetTaskStatisticsQuery,
)


router = APIRouter(prefix="/api/tasks", tags=["tasks"])


# DTOs
class CreateTaskRequest(BaseModel):
    """Request model for creating a task."""
    user_id: UUID
    title: str = Field(min_length=1, max_length=200)
    description: str = Field(default="")


class TaskResponse(BaseModel):
    """Response model for task."""
    id: UUID
    user_id: UUID
    title: str
    description: str
    is_completed: bool


class StatisticsResponse(BaseModel):
    """Response model for statistics."""
    total_tasks: int
    completed_tasks: int
    pending_tasks: int
    completion_rate: float


# Endpoints
@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: CreateTaskRequest,
    use_case: Annotated[CreateTaskUseCase, Depends()],
) -> TaskResponse:
    """Create a new task."""
    command = CreateTaskCommand(
        user_id=request.user_id,
        title=request.title,
        description=request.description,
    )
    
    task = use_case.execute(command)
    
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
    )


@router.get("/", response_model=List[TaskResponse])
async def list_tasks(
    user_id: UUID,
    only_pending: bool = Query(default=False),
    query: Annotated[ListTasksQuery, Depends()],
) -> List[TaskResponse]:
    """List tasks for a user."""
    tasks = query.execute(user_id, only_pending=only_pending)
    
    return [
        TaskResponse(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            is_completed=task.is_completed,
        )
        for task in tasks
    ]


@router.post("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(
    task_id: UUID,
    use_case: Annotated[CompleteTaskUseCase, Depends()],
) -> TaskResponse:
    """Complete a task."""
    task = use_case.execute(task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    
    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        title=task.title,
        description=task.description,
        is_completed=task.is_completed,
    )


@router.get("/statistics", response_model=StatisticsResponse)
async def get_statistics(
    user_id: UUID,
    query: Annotated[GetTaskStatisticsQuery, Depends()],
) -> StatisticsResponse:
    """Get task statistics for a user."""
    stats = query.execute(user_id)
    
    return StatisticsResponse(
        total_tasks=stats.total_tasks,
        completed_tasks=stats.completed_tasks,
        pending_tasks=stats.pending_tasks,
        completion_rate=stats.completion_rate,
    )
```

### Configuration

#### Database Setup

```python
# config/database.py
from sqlmodel import Session, SQLModel, create_engine


DATABASE_URL = "sqlite:///./tasks.db"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Create database and tables."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session
```

#### Dependency Injection

```python
# config/dependencies.py
from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from adapters.output.repositories import SQLModelTaskRepository
from application.use_cases import CreateTask, CompleteTask, ListTasks, GetTaskStatistics
from config.database import get_session
from ports.input import (
    CreateTaskUseCase,
    CompleteTaskUseCase,
    ListTasksQuery,
    GetTaskStatisticsQuery,
)
from ports.output import TaskRepository


def get_task_repository(
    session: Annotated[Session, Depends(get_session)]
) -> TaskRepository:
    """Get task repository instance."""
    return SQLModelTaskRepository(session)


def get_create_task_use_case(
    repository: Annotated[TaskRepository, Depends(get_task_repository)]
) -> CreateTaskUseCase:
    """Get create task use case."""
    return CreateTask(repository)


def get_complete_task_use_case(
    repository: Annotated[TaskRepository, Depends(get_task_repository)]
) -> CompleteTaskUseCase:
    """Get complete task use case."""
    return CompleteTask(repository)


def get_list_tasks_query(
    repository: Annotated[TaskRepository, Depends(get_task_repository)]
) -> ListTasksQuery:
    """Get list tasks query."""
    return ListTasks(repository)


def get_task_statistics_query(
    repository: Annotated[TaskRepository, Depends(get_task_repository)]
) -> GetTaskStatisticsQuery:
    """Get task statistics query."""
    return GetTaskStatistics(repository)
```

### Main Application

```python
# main.py
from fastapi import FastAPI

from adapters.input.rest_api import router
from config.database import create_db_and_tables
from config.dependencies import (
    get_create_task_use_case,
    get_complete_task_use_case,
    get_list_tasks_query,
    get_task_statistics_query,
)
from ports.input import (
    CreateTaskUseCase,
    CompleteTaskUseCase,
    ListTasksQuery,
    GetTaskStatisticsQuery,
)


# Create FastAPI app
app = FastAPI(title="Task Manager API", version="1.0.0")


# Register dependency providers
app.dependency_overrides[CreateTaskUseCase] = get_create_task_use_case
app.dependency_overrides[CompleteTaskUseCase] = get_complete_task_use_case
app.dependency_overrides[ListTasksQuery] = get_list_tasks_query
app.dependency_overrides[GetTaskStatisticsQuery] = get_task_statistics_query


# Include routers
app.include_router(router)


@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    create_db_and_tables()


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Task Manager API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Dependencies

```toml
# pyproject.toml
[project]
name = "task-manager"
version = "1.0.0"
description = "Task management system with hexagonal architecture"
requires-python = ">=3.11"

dependencies = [
    "fastapi>=0.109.0",
    "sqlmodel>=0.0.14",
    "uvicorn[standard]>=0.27.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "pytest-cov>=4.1.0",
    "httpx>=0.26.0",
]

[tool.fastapi]
entrypoint = "main:app"
```

## Running the Application

```bash
# Install dependencies
pip install -e .
pip install -e ".[dev]"

# Run the application
fastapi dev

# Or using uvicorn
python main.py
```

## Testing the API

```bash
# Create a task
curl -X POST http://localhost:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Learn hexagonal architecture",
    "description": "Study the patterns and implement a project"
  }'

# List tasks
curl "http://localhost:8000/api/tasks/?user_id=123e4567-e89b-12d3-a456-426614174000"

# Complete a task
curl -X POST "http://localhost:8000/api/tasks/{task_id}/complete"

# Get statistics
curl "http://localhost:8000/api/tasks/statistics?user_id=123e4567-e89b-12d3-a456-426614174000"
```

## What's Next?

This example demonstrates the core concepts. You can extend it by adding:

1. **Authentication & Authorization**: Add user authentication
2. **Task Assignment**: Allow assigning tasks to other users
3. **Due Dates**: Add deadline tracking
4. **Tags & Categories**: Organize tasks better
5. **Events**: Add domain events for task lifecycle
6. **Notifications**: Email/SMS when tasks are assigned
7. **CLI Interface**: Add Typer-based CLI
8. **Message Queue**: Process tasks asynchronously

This complete example provides a solid foundation for building maintainable applications with hexagonal architecture! 🎯
