User
├── id
├── email
└── password

Organization
├── id
├── name
└── owner (FK → User)

Membership
├── user (FK)
├── organization (FK)
└── role (owner/admin/member)

Project
├── id
├── organization (FK)
├── name
└── description

Task
├── id
├── project (FK)
├── assigned_to (FK → User)
├── status
├── priority
└── due_date

ActivityLog
├── id
├── organization (FK)
├── actor (FK → User)
├── action
└── timestamp
