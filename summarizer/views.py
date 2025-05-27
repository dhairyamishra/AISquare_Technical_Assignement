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