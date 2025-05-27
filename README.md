# 🧠 LLM Summary, Bullet Point & Quiz Generator API

A Django REST Framework API powered by **OpenAI’s GPT-3.5** or **Groq’s LLaMA 3** that can:

- Generate **summaries** and **bullet points** from raw text  
- Create **AI-generated 5-question multiple-choice quizzes** from random Wikipedia articles  
- Let users **play those quizzes** in a clean web UI with auto-scoring  
- Demonstrate everything end-to-end via an automated **CLI script using `curl`**  
- Store all outputs as structured **Markdown (`.md`) files**

---

## 🚀 Features

| Category | Details |
| -------- | ------- |
| 🔐 Auth & Users | Token-based authentication and registration |
| 🧠 LLM Tasks | Text summarization • Bullet extraction • Quiz generation |
| 🎮 Frontend | Django template–based quiz UI with scoring and error handling |
| 🪄 Automation | CLI script: Wikipedia → API calls → Markdown |
| 🧪 Quality | Unit-test suite with timestamped reports |
| 🔄 Fallback | Seamless switch between OpenAI and Groq keys defined in `.env` |
| 📂 Persistence | All requests & results stored in the database and/or `.md` files |

---

## 📦 Tech Stack

- **Python 3.10+**
- **Django 5.x** & **Django REST Framework**
- **OpenAI** & **Groq** LLM APIs
- `wikipedia` Python module (random article fetch)
- `python-dotenv` for configuration
- **HTML templates** (Django) for the quiz UI
- `curl` for the demo script

---

## ⚙️ Setup Instructions

> Commands below show **Windows-style paths**.  
> On macOS/Linux, replace `.venv\Scripts\activate` with `source venv/bin/activate`.

1. **Clone the repo**

   ```bash
   git clone https://github.com/dhairyamishra/AISquare_Technical_Assignement.git
   cd AISquare_Technical_Assignement
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**

   ```env
   # One or both keys may be present. OpenAI is preferred if both exist.
   OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   GROQ_API_KEY=groq-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
   DEBUG=True
   ```

5. **Apply migrations & create a superuser**

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

---

## 🔐 Authentication Workflow

All API endpoints require a valid **Token** header.

1. **Register**

   ```bash
   curl -X POST http://127.0.0.1:8000/api/register/ -H "Content-Type: application/json" -d "{\"username\": \"demo\", \"password\": \"password123\"}"
   ```

2. **Obtain a token**

   ```bash
   curl -X POST http://127.0.0.1:8000/api/token-auth/ -H "Content-Type: application/json" -d "{\"username\": \"demo\", \"password\": \"password123\"}"
   ```

   Use the returned token in subsequent requests:

   ```
   Authorization: Token your_token_here
   ```

---

## 💡 LLM Client Behavior

- Defaults to **`gpt-3.5-turbo`** if `OPENAI_API_KEY` exists.  
- Falls back to **`llama3-8b-8192`** via Groq when only `GROQ_API_KEY` is set.  
- **Exclusively** reads keys from **`.env`** (no OS env-var reliance).  
- Raises a clear error if neither key is provided.

---

## 📡 API Endpoints

| Method & Path | Purpose |
|---------------|---------|
| `POST /api/register/` | Create a new user |
| `POST /api/token-auth/` | Obtain an auth token |
| `POST /api/generate-summary/` | Single-sentence summary |
| `POST /api/generate-bullet-points/` | Bullet-point extraction |
| `POST /api/quiz/` | Generate a 5-question MCQ quiz from a random Wikipedia article |

### Examples

```bash
# Summary
curl -X POST http://127.0.0.1:8000/api/generate-summary/ -H "Authorization: Token your_token_here" -H "Content-Type: application/json" -d "{\"text\": \"The Eiffel Tower was completed in 1889 and is one of the most iconic landmarks in Paris.\"}"

# Bullets
curl -X POST http://127.0.0.1:8000/api/generate-bullet-points/ -H "Authorization: Token your_token_here" -H "Content-Type: application/json" -d "{\"text\": \"Python is widely used in data science, machine learning, and web development.\"}"

# Quiz
curl -X POST http://127.0.0.1:8000/api/quiz/ -H "Authorization: Token your_token_here" -H "Content-Type: application/json"
```

---

## 🖥️ Web UI (Quiz Player)

Visit **`http://127.0.0.1:8000/quiz/play/`** (login required).

- Fetches a quiz from a random Wikipedia article
- Lets you choose answers and shows your score instantly
- Displays friendly error messages if quiz creation fails

---

## 🧪 Running Tests

```bash
python manage.py test summarizer --testrunner=summarizer.tests.ReportRunner
```

Reports are saved as:

```
test_report_YYYYMMDD_HHMM.txt
```

---

## 💻 CLI Demo: Wikipedia → LLM → Markdown

```bash
python demo_curl_runner.py
```

The script will:

1. Register & authenticate a user  
2. Pull a random Wikipedia article  
3. Call summary **and** bullet-point endpoints via `curl`  
4. Save output as `summary_<topic>.md`

---

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
├── quizui/
│   ├── views.py
│   ├── urls.py
├── templates/
│   ├── base.html
│   ├── registration/
│   │   └── login.html
│   └── quizui/
│       ├── quiz.html
│       ├── result.html
│       └── error.html
├── demo_curl_runner.py
├── manage.py
├── .env
├── requirements.txt
└── README.md
```

---

## 📄 License

MIT License
