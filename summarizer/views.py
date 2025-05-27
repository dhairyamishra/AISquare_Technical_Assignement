from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from .models import SummaryEntry
from .serializers import SummaryEntrySerializer
from .utils import generate_summary, generate_bullet_points
from wikipedia import page, random
from rest_framework.permissions import IsAuthenticated
from .utils import client, MODEL_NAME
import json
from rest_framework.authtoken.models import Token
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import requests
from .utils import sanitize_text

class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)

class LogoutUserView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Delete the token to effectively "log out"
            token = Token.objects.get(user=request.user)
            token.delete()
            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Token not found."}, status=status.HTTP_400_BAD_REQUEST)

class GenerateSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SummaryEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data["text"]

        summary = generate_summary(text)
        entry = SummaryEntry.objects.create(text=text, summary=summary)

        return Response({"summary": summary}, status=status.HTTP_200_OK)

class GenerateBulletPointsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SummaryEntrySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        text = serializer.validated_data["text"]

        bullet_points = generate_bullet_points(text)
        entry = SummaryEntry.objects.create(text=text, bullet_points=bullet_points)

        return Response({"bullet_points": bullet_points}, status=status.HTTP_200_OK)

class GenerateQuizView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Step 1: Fetch a random Wikipedia article
            while True:
                try:
                    title = random()
                    content = page(title).content[:3000]  # limit size
                    break
                except Exception:
                    continue

            # Step 2: Build prompt for the LLM
            prompt = f"""
                You are an educational assistant. Create a 5-question multiple-choice quiz in JSON format from the following text.

                Each question must include:
                - "question": The question text
                - "options": A list of 4 options
                - "answer": The correct option text (not just the letter)

                TEXT:
                \"\"\"
                {content}
                \"\"\"

                Output ONLY a valid JSON array, no extra commentary. Format:
                [
                {{
                    "question": "...",
                    "options": ["A", "B", "C", "D"],
                    "answer": "B"
                }},
                ...
                ]
                """

            # Step 3: Call the LLM
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are a quiz-generating assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            raw = response.choices[0].message.content.strip()

            # Step 4: Parse JSON safely
            try:
                quiz = json.loads(raw)
            except json.JSONDecodeError:
                return Response({
                    "error": "Invalid JSON returned by LLM",
                    "raw": raw
                }, status=500)

            # Step 5: Return parsed quiz and article title
            return Response({
                "title": title,
                "quiz": quiz
            })

        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
@login_required
def summary_ui_view(request):
    result = None
    error = None

    if request.method == "POST":
        text = request.POST.get("text", "")
        text = sanitize_text(text)
        if not text.strip():
            error = "Please enter text to summarize."
        else:
            token, _ = Token.objects.get_or_create(user=request.user)
            response = requests.post("http://127.0.0.1:8000/api/generate-summary/",
                                     headers={"Authorization": f"Token {token.key}"},
                                     json={"text": text})
            if response.status_code == 200:
                result = response.json()["summary"]
            else:
                error = response.text

    return render(request, "summarizer/summary_ui.html", {"result": result, "error": error})


@login_required
def bullet_ui_view(request):
    result = None
    error = None

    if request.method == "POST":
        text = request.POST.get("text", "")
        text = sanitize_text(text)
        if not text.strip():
            error = "Please enter text for bullet extraction."
        else:
            token, _ = Token.objects.get_or_create(user=request.user)
            response = requests.post("http://127.0.0.1:8000/api/generate-bullet-points/",
                                     headers={"Authorization": f"Token {token.key}"},
                                     json={"text": text})
            if response.status_code == 200:
                result = response.json()["bullet_points"]
            else:
                error = response.text

    return render(request, "summarizer/bullet_ui.html", {"result": result, "error": error})







