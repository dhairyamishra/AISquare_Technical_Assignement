# 🧠 LLM Summary & Bullet Point Generator API

A Django REST Framework API that generates summaries and bullet points using OpenAI's GPT-3.5 or Groq's LLaMA 3 models. Includes a fully automated CLI demo using random Wikipedia articles and `curl`.

## 🚀 Features

- Token-based authentication
- Supports both OpenAI and Groq clients (fallback logic built-in)
- Summarization and bullet point generation using LLMs
- RESTful endpoints with persistent storage
- Full test suite with timestamped reports
- CLI script with `curl` demonstration and random Wikipedia integration
- Output saved automatically to `.md` files

## 📦 Tech Stack

- Python 3.10+
- Django 5.x
- Django REST Framework
- OpenAI / Groq APIs
- `wikipedia` Python module
- `python-dotenv` for `.env` config
- `curl` for API interaction in demo mode

---

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

```env
# Use either or both. OpenAI is preferred if both are present.
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
GROQ_API_KEY=groq-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
DEBUG=True
```

5. **Apply migrations and create a superuser (for admin access)**

```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Run the server**

```bash
python manage.py runserver
```

---

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

---

## 💡 How the LLM Client Works

- Uses `gpt-3.5-turbo` via OpenAI if `OPENAI_API_KEY` is present
- Falls back to `llama3-8b-8192` via Groq if `GROQ_API_KEY` is set
- Only loads from `.env` — no reliance on OS env vars
- Raises error if no valid API key is available

---

## 📡 API Endpoints

### `POST /api/register/`

Registers a new user:

```bash
curl -X POST http://127.0.0.1:8000/api/register/ \
  -H "Content-Type: application/json" \
  -d "{\"username\": \"demo\", \"password\": \"password123\"}"
```

---

### `POST /api/generate-summary/`

```bash
curl -X POST http://127.0.0.1:8000/api/generate-summary/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"The Eiffel Tower was built in 1889 and is one of the most iconic landmarks in the world.\"}"
```

Response:
```json
{
  "summary": "The Eiffel Tower, built in 1889, is a globally recognized landmark."
}
```

---

### `POST /api/generate-bullet-points/`

```bash
curl -X POST http://127.0.0.1:8000/api/generate-bullet-points/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Python is widely used in data science, machine learning, and web development.\"}"
```

Response:
```json
{
  "bullet_points": [
    "Python is widely used in data science.",
    "It is used in machine learning.",
    "Also popular for web development."
  ]
}
```

---

## 🧪 Running Tests

```bash
python manage.py test summarizer --testrunner=summarizer.tests.ReportRunner
```

Outputs to: `test_report_YYYYMMDD_HHMM.txt`

---

## 🖥️ Demo Script: Wikipedia → LLM → Markdown

```bash
python demo_curl_runner.py
```

This script will:

1. Register and authenticate a user
2. Fetch a random Wikipedia article
3. Call your API via `curl`
4. Print the summary and bullet points
5. Save output to: `summary_<topic>.md`

---

## 📁 Project Structure

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
├── demo_curl_runner.py
├── manage.py
├── .env
├── requirements.txt
└── README.md
```

## 📄 License

MIT License
