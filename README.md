# 🧠 LLM Summary & Bullet Point Generator API

A Django REST Framework API that generates summaries and bullet points using OpenAI's GPT-3.5 or Groq's LLaMA 3 models. Built for the AISquare Backend Developer assignment.

## 🚀 Features

- Token-based authentication
- Supports OpenAI and Groq AI clients
- Automatic fallback from OpenAI → Groq
- Summarization and bullet point generation using LLMs
- RESTful endpoints with persistent storage
- Fully tested with timestamped test reports

## 📦 Tech Stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- OpenAI / Groq LLM APIs
- `python-dotenv` for secure `.env` config

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
# Use either or both. OpenAI is preferred if both are present.

OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY=groq-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEBUG=True
```

5. **Apply migrations and create a superuser**

```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Run the server**

```bash
python manage.py runserver
```

## 🔐 Authentication

All endpoints require token-based authentication.

### Get token:
```bash
curl -X POST http://127.0.0.1:8000/api/token-auth/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"your_username\", \"password\": \"your_password\"}"

```

### Use in headers:
```
Authorization: Token your_token_here
```

## 💡 How the LLM Client Works

The backend will:

- Use `gpt-3.5-turbo` if `OPENAI_API_KEY` is present
- Otherwise fall back to `llama3-8b-8192` via Groq if `GROQ_API_KEY` is available
- Raise an error if neither key is present

No system environment variables are used — only values from `.env`.

## 📡 API Endpoints

### `POST /api/generate-summary/`

```
curl -X POST http://127.0.0.1:8000/api/generate-summary/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"The Eiffel Tower was built in 1889 and is one of the most iconic landmarks in the world.\"}"


Response:
{
  "summary": "The Eiffel Tower, built in 1889, is a globally recognized landmark."
}
```

---

### `POST /api/generate-bullet-points/`

```
curl -X POST http://127.0.0.1:8000/api/generate-bullet-points/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Python is widely used in data science, machine learning, and web development.\"}"


Response:
{
  "bullet_points": [
    "Python is widely used in data science.",
    "It is used in machine learning.",
    "Also popular for web development."
  ]
}
```

## 🧪 Running Tests

To run all unit tests and save a timestamped report:

```bash
python manage.py test summarizer --testrunner=summarizer.tests.ReportRunner
```

Generates: `test_report_YYYYMMDD_HHMM.txt`

## 🗂️ Project Structure

```
llm_summary_api/
├── summarizer/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── llm_summary_api/
│   └── settings.py, urls.py
├── .env
├── manage.py
├── requirements.txt
└── README.md
```

## 👨‍💻 Author

Developed by Your Name  
https://github.com/yourusername

## 📄 License

MIT License
