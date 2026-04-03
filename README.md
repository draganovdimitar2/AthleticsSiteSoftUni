> [!NOTE]
> 🚀 **Live Demo**: [https://athleticssitesoftuni.onrender.com](https://athleticssitesoftuni.onrender.com)
> 
> This project is hosted on Render's free plan. If the site feels a bit slow to load initially, it's just the server "waking up" from sleep mode (usually takes about a minute). I sincerely apologize for "stealing" sixty seconds of your life!

# Athletics Site

**Athletics Site** is a comprehensive competition and results management platform designed for the track and field community. Built with **Django**, it provides a centralized hub for tracking athlete performance, organizing event categories, and maintaining historical records. 

The system features a robust validation engine to ensure data integrity—automatically matching results to age categories and competition timeframes—while offering a seamless, permission-based experience for both public visitors and administrators.

## ✨ Features

* 🏃‍♂️ **Athlete Management**: Full CRUD support for athlete profiles for **authenticated users**, including personal details and discipline associations.
* 🔐 **Secure Authentication**: Built-in user registration and login system to protect administrative actions while maintaining public visibility.
* 🏷️ **Age Category Management**: Manage age categories (e.g., U14, U16, Veterans) with gender-specific rules.
* 🏆 **Competition Management**: Organize competitions with start/end dates, location, and categorization (Indoor/Outdoor/Championship/Masters).
* 📊 **Results Tracking**: Record and view athlete performance. Includes automatic validation to ensure results match the athlete's age category and the competition's timeframe.
* 🏋️‍♀️ **Discipline Information**: A dedicated section for managing and viewing athletic disciplines.
* 📧 **Contact Page**: A simple contact interface.

## 📂 Project Structure

The project is organized into several Django apps:

* `athletes`: The core app for managing athlete profiles, disciplines, and age categories. It handles the logic for age calculation, category assignment, and provides full CRUD functionality for authorized users.
* `competitions`: Handles the organization of competitions, including categories (Indoor, Outdoor, etc.) and age group eligibility.
* `records`: Manages competition results. Features strict data integrity checks to ensure results are valid for the given athlete and competition dates.
* `accounts`: Manages user authentication, registration, and login/logout processes.
* `common`: Contains the core layout, shared templates, and static files for the home page, disciplines page, and contact page.

## 🔐 Access Control

The project implements a clear permission model:

* **Anonymous Users**: Have **read-only** access. They can browse athletes, competitions, results, and disciplines.
* **Registered Users**: Have **full CRUD** (Create, Read, Update, Delete) permissions. Once logged in, users can add new athletes, create competitions, record results, and manage site content.

## 🗄️ Database Schema (ER Diagram)

The following Entity Relationship Diagram (ERD) illustrates the database structure and relationships between models in
the project.

![Athletics Site ERD](https://github.com/user-attachments/assets/81024046-d86f-4f4f-a52c-ca1114e51128)

## 🚀 Local Setup (Docker)

### ✅ Prerequisites

- Docker & Docker Compose
- Git

> No local Python or PostgreSQL installation is required — everything runs in containers.

### ⬇️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/draganovdimitar2/AthleticsSiteSoftUni.git
   cd AthleticsSiteSoftUni
   ```
2. **Create a `.env` file in the project root and add:**

> [!IMPORTANT]
> **Notes About `.env` Configuration**
>
> You can modify some values, but others must remain unchanged for the Docker setup to work correctly:
>
> ### 🔒 Do NOT change (Required for Docker)
> * `DB_HOST=db` — Must match the Docker service name.
> * `DB_PORT=5432` — Default PostgreSQL port used by the container.
>
> ### ⚠️ Change with caution
> * `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
> * If you change these, you must reset the database volumes:
>   ```bash
>   docker-compose down -v
>   docker-compose up -d --build
>   ```
>
> ### ✅ Safe to change
> * `SECRET_KEY` — Set your own unique value.
> * `DEBUG` — Can be `True` or `False`.
> * `ALLOWED_HOSTS` — Can be extended if needed.
> * `CSRF_TRUSTED_ORIGINS` — Adjust if using a different domain/port.

- Example `.env` structure that you can copy and paste.
   ```env
   SECRET_KEY=your-secret-key  # we will add this in the next step
   DEBUG=True
   
   ALLOWED_HOSTS=localhost,127.0.0.1
   CSRF_TRUSTED_ORIGINS=http://localhost:8000
   
   POSTGRES_DB=athletics_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=postgres
   
   DB_HOST=db
   DB_PORT=5432
   ```

3. **Generate a Django secret key**

    - You can generate a random secret key **without local Python** by using Docker:
    ```bash
    docker run --rm python:3.10-slim python -c "import secrets; print(secrets.token_urlsafe(50))"
    ```
    - Alternatively, if you have Python installed:
    ```bash
    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
    ```
    - Copy the output and replace `your-secret-key` in your `.env` file.


4. **Build and run the containers:**

   ```bash
   docker-compose up -d --build
   ```

5. **Open the application:**
   ```
   http://localhost:8000
   ```

## 🧪 Testing 
1. **Open a shell inside the running web container:**
   ```bash
   docker compose exec web python3 manage.py test
   ```
- This will execute all available tests (24 total).


## 🛠️ Technologies Used

* **Backend Language**: Python
* **Framework**: Django
* **Database**: PostgreSQL (Docker for local development, [Neon](https://neon.tech/) for production)
* **Containerization:** Docker & Docker Compose
* **Deployment Platform:** [Render](https://render.com/)
* **Frontend**: HTML, CSS, JavaScript
