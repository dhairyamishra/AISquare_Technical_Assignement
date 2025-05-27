import json
import requests
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework.authtoken.models import Token

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

    # GET request: fetch quiz from backend API
    token, _ = Token.objects.get_or_create(user=request.user)

    response = requests.post(API_URL, headers={
        "Authorization": f"Token {token.key}",
        "Content-Type": "application/json"
    })

    try:
        data = response.json()
        questions = data["quiz"]
        title = data.get("title", "Untitled Quiz")
    except (ValueError, KeyError) as e:
        return render(request, "quizui/error.html", {
            "error": f"Quiz could not be loaded: {e}",
            "raw": response.text
        })

    return render(request, "quizui/quiz.html", {
        "title": title,
        "questions": questions,
        "json_questions": json.dumps(questions)
    })
