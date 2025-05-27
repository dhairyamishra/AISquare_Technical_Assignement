# 🧠 LLM Summary, Bullet Point & Quiz Generator API

A Django REST Framework API powered by **OpenAI’s GPT-3.5** or **Groq’s LLaMA 3** that can:

- Generate **summaries** and **bullet points** from raw text  
- Create **AI-generated 5-question multiple-choice quizzes** from random Wikipedia articles  
- Provide **HTML UI** for both summarization and bullet extraction tasks  
- Let users **play those quizzes** in a clean web UI with auto-scoring  
- Demonstrate everything end-to-end via an automated **CLI script using `curl`**  
- Sanitize and process all input text to avoid API failures on special characters  
- Store all outputs as structured **Markdown (`.md`) files**

---

## 🚀 Features

| Category | Details |
| -------- | ------- |
| 🔐 Auth & Users | Token-based authentication and registration |
| 🧠 LLM Tasks | Text summarization • Bullet extraction • Quiz generation |
| 🧼 Input Safety | Hidden or special characters removed from input |
| 🎮 Frontend | Django template–based UI for quizzes, summaries, and bullets |
| 🪄 Automation | CLI script: Wikipedia → API calls → Markdown |
| 🧪 Quality | Unit-test suite with token, form, and API coverage |
| 🔄 Fallback | Seamless switch between OpenAI and Groq keys defined in `.env` |
| 📂 Persistence | All requests & results stored in the database and/or `.md` files |

---

## 📦 Tech Stack

- **Python 3.10+**
- **Django 5.x** & **Django REST Framework**
- **OpenAI** & **Groq** LLM APIs
- `wikipedia` Python module (random article fetch)
- `python-dotenv` for configuration
- **HTML templates** (Django) for the quiz/summarizer UI
- `curl` for the demo script

---

## ⚙️ Setup Instructions

> On macOS/Linux, replace `.venv\Scripts\activate` with `source venv/bin/activate`.

1. **Clone the repo**

   ```bash
   git clone https://github.com/dhairyamishra/AISquare_Technical_Assignement.git
   cd AISquare_Technical_Assignement
   ```

2. **Create & activate a virtual environment**

   ```bash
   python -m venv .venv
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

1. **Register via API**

   ```bash
   curl -X POST http://127.0.0.1:8000/api/register/ -H "Content-Type: application/json" -d "{\"username\": \"demo\", \"password\": \"password123\"}"
   ```

2. **Obtain a token**

   ```bash
   curl -X POST http://127.0.0.1:8000/api/token-auth/ -H "Content-Type: application/json" -d "{\"username\": \"demo\", \"password\": \"password123\"}"
   ```

   Use the returned token in subsequent requests:

   ```text
   Authorization: Token your_token_here
   ```

3. **Logout (API)**

   ```bash
   curl -X POST http://127.0.0.1:8000/api/logout/ -H "Authorization: Token your_token_here"
   ```

---

## 📡 API Endpoints

| Method & Path | Purpose |
|---------------|---------|
| `POST /api/register/` | Create a new user |
| `POST /api/token-auth/` | Obtain an auth token |
| `POST /api/logout/` | Invalidate the user's token |
| `POST /api/generate-summary/` | Single-sentence summary |
| `POST /api/generate-bullet-points/` | Bullet-point extraction |
| `POST /api/quiz/` | Generate a 5-question MCQ quiz from a random Wikipedia article |

---
### Example API Calls with `curl`

```bash
# Summary
curl -X POST http://127.0.0.1:8000/api/generate-summary/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"The Eiffel Tower was completed in 1889 and is one of the most iconic landmarks in Paris.\"}"
```

```bash
# Bullet Points
curl -X POST http://127.0.0.1:8000/api/generate-bullet-points/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d "{\"text\": \"Python is widely used in data science, machine learning, and web development.\"}"
```

```bash
# Quiz
curl -X POST http://127.0.0.1:8000/api/quiz/ \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json"
```
---

## 🖥️ Web UI Endpoints

| URL | View |
|-----|------|
| `/` | Home page |
| `/accounts/login/` | Login form |
| `/accounts/register/` | Register form |
| `/accounts/logout/` | Secure logout |
| `/quiz/play/` | AI-generated quiz interface |
| `/summarizer/ui/summary/` | Summary form UI |
| `/summarizer/ui/bullets/` | Bullet-point form UI |

---

## 🧪 Running Tests

```bash
python manage.py test summarizer --testrunner=summarizer.tests.ReportRunner
python manage.py test quizui
```

Reports from `ReportRunner` are saved as:

```
test_report_YYYYMMDD_HHMM.txt
```

---
## 💻 CLI Demo Script: Wikipedia → LLM → Markdown

The project includes a helper script: `demo_curl_runner.py`  
It automates a full flow using the live API endpoints.

### 🔧 What It Does:

| Step | Action |
|------|--------|
| 1️⃣ | Prompts for a username and password |
| 2️⃣ | Registers the user (or skips if already exists) |
| 3️⃣ | Authenticates and fetches an API token |
| 4️⃣ | Retrieves a random Wikipedia article |
| 5️⃣ | Calls `/generate-summary/` and `/generate-bullet-points/` using `curl` |
| 6️⃣ | Displays results in the terminal |
| 7️⃣ | Saves a structured Markdown file: `summary_<topic>.md`

### ▶️ How to Run It

```bash
python demo_curl_runner.py
```
---

## 📄 License

MIT License  
© 2025 dhairyamishra
