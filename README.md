🏥 Clinic Licensing Application API

A backend service built with Django REST Framework that enables clinics to submit licensing applications. Each application includes details about clinic branches, required specialists, and necessary equipment. The system supports full CRUD operations for authenticated users and administrators.

🚀 Features

📝 Licensing Application Management

* Clinics can create and submit applications for obtaining a license
* Each application includes:

  * Clinic branches
  * Required specialists
  * Required equipment

🔧 CRUD Functionality

Authenticated users and admins can create, update, delete, and retrieve:

* Branches
* Specialties
* Specialists
* Required specialists
* Equipment
* required equipment

🔐 User Authentication & Profile Management

* User registration
* Login and logout
* Retrieve and update user profile
* JWT authentication using DRF SimpleJWT

🛠 Admin Panel

* Modern and customizable admin UI using Jazzmin
* Administrators can manage all entities easily through the admin dashboard

⚙️ Dependency Management with uv

* The project uses **uv** instead of pip for package installation
* All dependencies can be installed with:

  ```bash
  uv sync
  ```
* uv automatically handles the virtual environment and package resolution

🌐 Deployment

* Deployed on a real server with a live domain: https://girlshub.uz/
* Configured for production use

🧰 Tech Stack

| Component          | Technology                       |
| ------------------ | -------------------------------- |
| Backend Framework  | Django, Django REST Framework    |
| Authentication     | DRF SimpleJWT                    |
| Admin UI           | Jazzmin                          |
| Dependency Manager | uv                               |
| Apps               | `users`, `application`, `common` |

📦 Installation & Setup

1. Clone the Repository

```bash
git clone https://github.com/yourusername/yourproject.git
cd yourproject
```

2. Install Dependencies Using uv

```bash
uv sync
```

3. Apply Migrations

```bash
python manage.py migrate
```

4. Run the Server

```bash
python manage.py runserver
```

🔐 Authentication

Authentication is handled through SimpleJWT:

* Access and refresh tokens
* Token refresh endpoint
* Protected endpoints for managing clinic application data

🛡 Admin Panel

Jazzmin provides a clean and organized admin interface where staff can manage:

* Users
* Applications
* Branches
* Specialties
* Specialists
* Equipment

