# 📚 Flashcard App Backend

A **Django REST Framework (DRF)** backend for the **Flashcard App**, providing user authentication, flashcard deck management, and a study mode API. This backend is designed to work with a **React + TypeScript** frontend.

🚀 **Live API URL:** [https://flashcard-app-backend-production.up.railway.app](https://flashcard-app-backend-production.up.railway.app)  
🖥 **Frontend Repository:** [Flashcard App Frontend](https://github.com/carter-loremdigital/flashcard-app-frontend)

---

## ✨ Features

✅ **User Authentication** – Uses **JWT (JSON Web Token)** for secure login and API access.

✅ **Flashcard Management** – Create, edit, delete flashcards and organize them into decks.

✅ **Study Mode API** – Fetch randomized flashcards for studying with progress tracking.

✅ **Rate Limiting Protection** – Limits API requests to prevent abuse.

✅ **PostgreSQL Database** – Fully managed on Railway.

✅ **Deployed on Railway** – Fast, secure, and scalable API hosting.

---

## 🛠️ Technologies Used

- **Backend Framework:** Django, Django REST Framework (DRF)

- **Database:** PostgreSQL (hosted on Railway)

- **Authentication:** JWT (via `djangorestframework-simplejwt`)

- **Rate Limiting:** Django REST Framework Throttling

- **Deployment:** Railway

- **Environment Management:** `django-environ` for `.env` variables

---

## 🚀 Getting Started

> [!NOTE]
> Intalling and configuring [PostgresQL](https://www.postgresql.org/) is required to connect a local database.

### **1️⃣ Clone the Repository**

```sh
git clone https://github.com/carter-loremdigital/flashcard-app-backend
cd flashcard-app-backend
```

### 2️⃣ Set Up a Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate  # On Windows
```

### 3️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 4️⃣ Set Up Environment Variables

Create a `.env` file in the root directory and add:

```
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgres://your_db_user:your_db_password@localhost:5432/your_db_name
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5️⃣ Apply Database Migrations

```sh
python manage.py migrate
```

### 6️⃣ Create a Superuser (Admin)

```sh
python manage.py createsuperuser
```

### 7️⃣ Run the Development Server

```sh
python manage.py runserver
```

The backend will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

---

## 📌 API Endpoints

| Endpoint                       | Method           | Description                                  |
| ------------------------------ | ---------------- | -------------------------------------------- |
| `/api/signup/`                 | POST             | Register a new user                          |
| `/api/token/`                  | POST             | Get access & refresh tokens                  |
| `/api/token/refresh/`          | POST             | Refresh JWT access token                     |
| `/api/decks/`                  | GET, POST        | List all decks / Create a new deck           |
| `/api/decks/{id}/`             | GET, PUT, DELETE | Retrieve, update, or delete a deck           |
| `/api/flashcards/`             | GET, POST        | List all flashcards / Create a new flashcard |
| `/api/flashcards/{id}/`        | GET, PUT, DELETE | Retrieve, update, or delete a flashcard      |
| `/api/flashcards/bulk_create/` | POST             | Create multiple flashcards in bulk           |
| `/api/flashcards/bulk_delete/` | DELETE           | Delete multiple flashcards in bulk           |
| `/api/study/{deck_id}/`        | GET              | Fetch randomized flashcards for studying     |

---

## 🌐 Deployment

This project is deployed using **Railway**.

### Deploying on Railway

1. Go to [Railway](https://railway.com/) and create a new project.

2. Select "**Deploy from GitHub**" and connect this repository.

3. Add a **PostgreSQL database** using the Railway plugin.

4. Set up **Environment Variables** in Railway:

```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=(Copy from database environment variables provided by Railway)
CORS_ALLOWED_ORIGINS="https://your-app-url.com"
CSRF_TRUSTED_ORIGINS="https://your-app-url.com,https://yourbackend.railway.app"
ALLOWED_HOSTS=yourbackend.railway.app
```

5. Click **Deploy** and monitor logs for errors.

---

## 🔗 Related Repositories

- **Frontend Repository**: [Flashcard App Frontend](https://github.com/carter-loremdigital/flashcard-app-frontend)

---

## 📝 License

This project is licensed under the **MIT License**.
