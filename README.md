## TaskFlow — Multi-Tenant Task Management Backend

TaskFlow is a backend API for managing organizations, projects, and tasks in a **multi-tenant environment**.
It is designed to model how real SaaS tools (e.g. Linear, Jira, Notion) handle **authentication, authorization, and data isolation** across teams.

The system focuses on **correct access control**, **clean domain boundaries**, and **production-ready architecture** rather than simple CRUD operations.

---

## Core Concepts

### Multi-Tenancy

- A single backend serves **multiple organizations**
- Users can belong to **multiple organizations**
- A user’s permissions depend on their **role per organization**

### Role-Based Access Control (RBAC)

Users have roles **per organization**, not globally:

- Owner
- Admin
- Member

Permissions are enforced at:

- **Queryset level** (what data a user can see)
- **Object permission level** (what actions a user can perform)

---

## Features

### Authentication

- JWT-based authentication
- Secure login & registration
- Protected endpoints

### Organizations

- Create organizations
- Automatic owner membership creation
- Organization-scoped access

### Memberships

- User ↔ Organization relationship
- Role stored per membership
- Single source of truth for permissions

### Projects

- Projects belong to organizations
- Only owners/admins can create projects
- Members have read-only access

### Tasks

- Tasks belong to projects
- Tasks can be assigned to members
- Only assigned members or privileged roles can update tasks

### Invitations

- Organization members can invite users via email
- Token-based invite acceptance
- Invite expiration handling

### Activity Logging

- Important actions are logged
- Provides an audit trail per organization

---

## Architecture Overview

This project follows a **domain-driven app structure**, where each app owns its responsibility:

```
accounts/        → authentication & user model
organizations/  → organizations, memberships, invites
projects/       → projects within organizations
tasks/          → task management & workflow
activity/       → audit logs
common/          → shared utilities (testing helpers, etc.)
```

### Key Design Principle

> **Membership is the core authorization model**

All access checks flow through:

```
User → Membership → Organization → Project → Task
```

This ensures strict isolation between organizations.

---

## Data Model (Simplified)

```
User
  │
  ├── Membership (role)
  │       │
  │       └── Organization
  │               │
  │               └── Project
  │                       │
  │                       └── Task
```

---

## Permissions Strategy

Two layers of protection are used:

### 1. Queryset Scoping (Visibility)

Ensures users can only **see** objects they belong to.

Example:

```python
Task.objects.filter(
    project__organization__memberships__user=request.user
)
```

### 2. Object Permissions (Actions)

Ensures users can only **modify** objects they are allowed to act on.

Example:

- Only assigned users can update a task
- Only owners/admins can create projects

---

## Tech Stack

- **Python**
- **Django**
- **Django REST Framework**
- **PostgreSQL**
- **Docker & Docker Compose**
- **JWT Authentication**

---

## Local Development Setup

### Requirements

- Docker
- Docker Compose

### Run the project

```bash
docker-compose up --build
```

### Run migrations

```bash
docker-compose exec web python manage.py migrate
```

### Create superuser

```bash
docker-compose exec web python manage.py createsuperuser
```

---

## Running Tests

Automated tests cover:

- Authentication flow
- Organization membership logic
- Permission enforcement
- Task access control

Run tests with:

```bash
docker-compose exec web python manage.py test
```

---

## API Overview (Sample)

```
POST   /api/v1/auth/register/
POST   /api/v1/auth/login/

POST   /api/v1/organizations/
GET    /api/v1/organizations/

POST   /api/v1/projects/
GET    /api/v1/projects/

POST   /api/v1/tasks/
PATCH  /api/v1/tasks/{id}/

POST   /api/v1/invites/
POST   /api/v1/invites/accept/{token}/
```

---

## Future Improvements

- Pagination & filtering
- Async email delivery for invites
- Webhooks / notifications
- Deployment (AWS / Fly.io / Railway)
- API documentation (Swagger / Redoc)
