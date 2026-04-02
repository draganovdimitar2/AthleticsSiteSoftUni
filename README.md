# Athletics Site

An athletics competition and results tracking website built with Django. This platform allows users to view information
about athletes, competitions, and athletic records.

## ✨ Features

* 🏃‍♂️ **Athlete Management**: Full CRUD support for athlete profiles, including personal details and discipline associations.
* 🏷️ **Age Category Management**: Manage age categories (e.g., U14, U16, Veterans) with gender-specific rules.
* 🏆 **Competition Management**: Organize competitions with start/end dates, location, and categorization (Indoor/Outdoor/Championship/Masters).
* 📊 **Results Tracking**: Record and view athlete performance. Includes automatic validation to ensure results match the athlete's age category and the competition's timeframe.
* 🏋️‍♀️ **Discipline Information**: A dedicated section for managing and viewing athletic disciplines.
* 📧 **Contact Page**: A simple contact interface.

## 📂 Project Structure

The project is organized into several Django apps:

* `athletes`: Manages athlete profiles, disciplines, and age categories. Includes logic for age calculation and category assignment.
* `competitions`: Handles the organization of competitions, including categories (Indoor, Outdoor, etc.) and age group eligibility.
* `records`: Manages competition results. Features strict data integrity checks to ensure results are valid for the given athlete and competition dates.
* `common`: Contains the core layout, shared templates, and static files for the home page, disciplines page, and
  contact page.

## 🗄️ Database Schema (ER Diagram)

The following Entity Relationship Diagram (ERD) illustrates the database structure and relationships between models in
the project.

![Athletics Site ERD](https://github.com/user-attachments/assets/81024046-d86f-4f4f-a52c-ca1114e51128)

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing
purposes.

### ✅ Prerequisites

* Python 3.10 or higher
* PostgreSQL
* Git

### ⬇️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/draganovdimitar2/AthleticsSiteSoftUni.git
   cd AthleticsSiteSoftUni
   ```
2. **Create a `.env` file** in the project root directory.
    - **Note:** The Postgres image expects these exact variables, otherwise the project won't run.
    - For now, only add database credentials; the secret key will be added in the next step.
   ```
   SECRET_KEY=your-secret-key  # we will add this in the next step
   POSTGRES_DB=athletics_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=1234
   DB_HOST=db
   DB_PORT=5432
   ```

3. **Generate a Django secret key**

    - Open a Python shell:
    ```bash
    python
    ```
    - Inside the Python shell, execute:
    ```bash
    from django.core.management.utils import get_random_secret_key
    print(get_random_secret_key())
    ```
    - It will output a long string, for example:
   ```
   'y$0f+1t@z6&8qv9#(k!xg!e)0s*e3&j5v)1p)f)r3d@%b1w^a'
   ```
    - Copy this string into your .env file, replacing `your-secret-key`:
   ```bash
    SECRET_KEY='y$0f+1t@z6&8qv9#(k!xg!e)0s*e3&j5v)1p)f)r3d@%b1w^a'
   POSTGRES_DB=athletics_db
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=1234
   DB_HOST=db
   DB_PORT=5432
   ```
4. Running the whole project:

   ```bash
   docker compose up -d
   ```


**This command will:**

- Pull the required Docker images
- Build the Django container
- Create the `web` and `db` containers
- Run database migrations

## 🧪 Testing 
1. Open a shell inside the running web container:
   ```bash
   docker compose exec web python3 manage.py test
   ```
- This will execute all available tests (24 total).




## 🚧 Custom 404 Page

This project includes a custom 404 error page located at `common/templates/common/404.html`.

### How to View It

1. **Set `DEBUG=False`**  
   The 404 page, with its styling and images, only works when `DEBUG=False`.  
   Update your `settings.py` for local testing:

   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # or ['*']
   ```

2. **Ensure static files are set up**  
   The 404 page uses CSS and images located in `common/static/common/`. Make sure `STATIC_URL` and `STATIC_ROOT` are
   configured in `settings.py`:

   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = BASE_DIR / "staticfiles"
   ```
3. **Run `collectstatic`**  
   With DEBUG=False, Django doesn't serve static files automatically. Collect all static files:
    ```bash
    python manage.py collectstatic
    ```
4. **Keep WhiteNoise (or your static server) active**

   The project uses WhiteNoise to serve static files when DEBUG=False. Make sure this middleware is enabled:
    ```python
    MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # ... other middleware
    ]
    ```
5. **Trigger the 404 page**

   You can visit a non-existent URL (e.g., /this-page-does-not-exist/) or use the test view:
    ```bash
    http://127.0.0.1:8000/test-404/
    ```
   This action will display the custom 404 page.

### Notes

* The 404 page will only render correctly when `DEBUG=False`.
* For local development, you can temporarily set `DEBUG=True` to bypass static serving issues, but the full 404
  experience requires production/static setup.

## 🛠️ Technologies Used

* **Backend Language**: Python
* **Framework**: Django
* **Database**: PostgreSQL
* **Frontend**: HTML, CSS, JavaScript
