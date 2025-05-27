from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
import requests
from django.conf import settings

API_URL = "http://127.0.0.1:8000/api/quiz/"

@login_required
def play_quiz(request):
    if request.method == "POST":
        try:
            questions_json = request.POST.get("questions", "")
            questions = json.loads(questions_json)
        except json.JSONDecodeError as e:
            return render(request, "quizui/error.html", {
                "error": f"Could not decode quiz data: {e}",
                "raw": questions_json
            })

        user_answers = [request.POST.get(f"q{i}") for i in range(len(questions))]
        score = sum(1 for i, q in enumerate(questions) if q["answer"] == user_answers[i])
        return render(request, "quizui/result.html", {
            "score": score,
            "total": len(questions),
            "questions": zip(questions, user_answers)
        })

    # GET: fetch quiz from backend API
    token = request.user.auth_token.key
    response = requests.post(API_URL, headers={
        "Authorization": f"Token {token}",
        "Content-Type": "application/json"
    })
    data = response.json()
    questions = data["quiz"]

    return render(request, "quizui/quiz.html", {
        "title": data["title"],
        "questions": questions,
        "json_questions": json.dumps(questions)
    })
