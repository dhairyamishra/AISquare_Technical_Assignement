# 🧠 LLM Summary & Bullet Point Generator API

A Django REST API that uses OpenAI to generate intelligent summaries and bullet points from any input text. Built as part of the AISquare Backend Developer assignment.

## 🚀 Features

- 🔐 Token-based authentication
- 📝 Summarize long passages using GPT-3.5
- 📌 Extract bullet points from dense text
- 💾 Store all entries in a database
- ✅ Unit tested with Django's test framework
- 📄 `.env` support for secure API key handling

## 📦 Tech Stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- OpenAI API (GPT-3.5)
- Token Authentication
- `python-dotenv` for secure key management

## ⚙️ Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/llm-summary-api.git
   cd llm-summary-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**
   ```
   OPENAI_API_KEY=your_openai_key_here
   DEBUG=True
   ```

5. **Apply migrations and create a superuser**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 🔐 Authentication

All endpoints require token-based authentication.

To obtain a token:
```bash
POST /api/token-auth/
{
  "username": "yourusername",
  "password": "yourpassword"
}
```

Use the returned token in the `Authorization` header for all requests:
```
Authorization: Token your_token_here
```

## 📡 API Endpoints

### `POST /api/generate-summary/`

- Input:
  ```json
  {
    "text": "The quick brown fox jumps over the lazy dog."
  }
  ```

- Response:
  ```json
  {
    "summary": "A quick brown fox leaps over a lazy dog."
  }
  ```

### `POST /api/generate-bullet-points/`

- Input:
  ```json
  {
    "text": "Python is a versatile language. It is used in data science, AI, and web development."
  }
  ```

- Response:
  ```json
  {
    "bullet_points": [
      "Python is a versatile language.",
      "Used in data science, AI, and web development."
    ]
  }
  ```

## 🧪 Running Tests

To run the full test suite and save the results:

```bash
python manage.py test summarizer --testrunner=summarizer.tests.ReportRunner
```

This will generate a `test_report.txt` file with all test results.

## 🗂️ Project Structure

```
llm_summary_api/
├── summarizer/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── utils.py
│   └── tests.py
├── llm_summary_api/
│   └── settings.py, urls.py
├── manage.py
├── .env
├── requirements.txt
└── README.md
```

## 🧠 Example `.env`

```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEBUG=True
```

## 📄 License

MIT License
