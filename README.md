# MediaFeed

MediaFeed is a Django-based multi-media application where users can share media (images, videos, and documents), engage with posts via likes and comments, and manage their personal profile feeds.

## Features

- **User Authentication:** Registration, login, and profile management.
- **Media Creation & Uploads:** Create posts supporting:
  - Images (`.jpg`, `.png`, `.webp`, `.gif`)
  - Videos (`.mp4`, `.mov`)
  - Documents (`.pdf`, `.docx`)
  - Optional captions
- **Social Engagement:** Like/unlike posts, post comments, and delete owned comments.
- **Content Management:** Update and delete your own posts.
- **Validation:** Server-side file size and media format validation.
- **Cloud Storage Integration:** Cloudinary integration for scalable media hosting in production.

## Tech Stack

- **Backend:** Python, Django
- **Frontend:** JavaScript, HTML5, CSS3 (Custom Dark Theme UI)
- **Database:** PostgreSQL
- **Media Storage:** Cloudinary
- **Containerization:** Docker 
- **WSGI Server:** Gunicorn

## Project Structure

```text
├── accounts/          # User authentication and profile logic
├── interactions/      # Likes and comments models and views
├── posts/             # Core post creation, feed, and file handling
├── mediafeed/         # Django project settings and root routing
├── static/            # Global static assets (CSS, JS)
├── templates/         # Modular HTML templates
├── Dockerfile         # Production container definition
├── manage.py
└── requirements.txt
```
## Local Setup & Development
1. Prerequisites
Python 3.10+

PostgreSQL database instance

Cloudinary account (for media storage)

2. Manual Installation

```Bash
# Clone the repository
git clone <repository-url>
cd mediafeed

# Create and activate virtual environment
python -m venv .venv

# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

<<<<<<< HEAD
3. Environment Variables
```text
Create a .env file in the project root:

Code snippet
SECRET_KEY=your-django-secret-key
DEBUG=True #should be False in production
ALLOWED_HOSTS=127.0.0.1,localhost

# Database Configuration
DATABASE_URL=postgres://<db_user>:<db_password>@<db_host>:5432/<db_name>

# Cloudinary Configuration
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
```

4. Run Migrations & Start Server
```Bash
#Apply migrations
python manage.py migrate

# Start development server
python manage.py runserver
Access the application at http://127.0.0.1:8000/.
```

5. Docker Deployment
You can run the application, including the PostgreSQL database and app server, using Docker Compose.

Run with Docker Compose
```Bash
# Build and launch containers in detached mode
docker-compose up -d --build

# Run database migrations inside the container
docker-compose exec web python manage.py migrate

# Create a superuser (optional)
docker-compose exec web python manage.py createsuperuser
Access the Dockerized application at http://localhost:8000/.
```

## Author
**Joshua Oguejiofor**


