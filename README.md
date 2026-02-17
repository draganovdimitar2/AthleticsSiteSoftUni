# Athletics Site

An athletics competition and results tracking website built with Django. This platform allows users to view information about athletes, competitions, and athletic records.

## Features

*   **Athlete Management**: Create, update, view and delete athlete profiles. (Full CRUD)
*   **Competition Listings**: View a list of upcoming and past competitions.
*   **Results Tracking**: View results from various competitions, with options to filter by year and competition.
*   **Discipline Information**: A dedicated page listing all supported athletic disciplines.
*   **Contact Page**: A page to display contact information.

## Project Structure

The project is organized into several Django apps:

*   `athletes`: Manages athlete profiles, including creation, updating, and listing.
*   `competitions`: Handles the display of competition information.
*   `records`: Manages the display of results and records, including filtering capabilities.
*   `common`: Contains the core layout, shared templates, and static files for the home page, disciplines page and contact page.
## Database Schema (ER Diagram)

The following Entity Relationship Diagram (ERD) illustrates the database structure and relationships between models in the project.

![Athletics Site ERD](https://github.com/user-attachments/assets/81024046-d86f-4f4f-a52c-ca1114e51128)

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.10 or higher
*   PostgreSQL
*   Git

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/AthleticsSiteSoftUni.git
    cd AthleticsSiteSoftUni
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Database Setup

1.  **Create a PostgreSQL database.**

2.  **Create a `.env` file** in the project root directory and add your database credentials. You can use the `.env.example` as a template:
    ```
    SECRET_KEY=your-secret-key
    DB_NAME=your-db-name
    DB_USER=your-db-user
    DB_PASSWORD=your-db-password
    DB_HOST=localhost
    DB_PORT=5432
    ```

3.  **Run the database migrations:**
    ```bash
    python manage.py migrate
    ```

### Running the Development Server

Once the setup is complete, you can start the development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`.

## Data Loading

The project includes a script to populate the database with sample data for athletes, competitions, and results.

To load the data, run the following command:

```bash
python load_data.py
```
## Custom 404 Page

This project includes a custom 404 error page located at `common/templates/common/404.html`.

### How to view it
1. **Set `DEBUG=False`**  
   The 404 page with styling and images only works when `DEBUG=False`.  
   Update your `settings.py` for local testing:

   ```python
   DEBUG = False
   ALLOWED_HOSTS = ['localhost', '127.0.0.1']  # or ['*']
   ```

2. **Ensure static files are set up**  
   The 404 page uses CSS and images located in `common/static/common/`. Make sure `STATIC_URL` and `STATIC_ROOT` are configured in `settings.py`:

   ```python
   STATIC_URL = '/static/'
   STATIC_ROOT = BASE_DIR / "staticfiles"
3. **Run `collectstatic`**  
    With DEBUG=False, Django doesn’t serve static files automatically. Collect all static files:
    ```bash
    python manage.py collectstatic
    ```
4. **Keep WhiteNoise (or your static server) active**

    The project uses WhiteNoise to serve static files when DEBUG=False. Make sure this middleware is enabled:
    ```bash
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
   This will show the 404 page

### Notes
* The 404 page will only render correctly when DEBUG=False.
* For local development, you can temporarily set DEBUG=True to bypass static serving issues, but the full 404 experience requires production/static setup.
## Technologies Used

*   **Backend Language**: Python
*   **Framework**: Django
*   **Database**: PostgreSQL
*   **Frontend**: HTML, CSS, JavaScript