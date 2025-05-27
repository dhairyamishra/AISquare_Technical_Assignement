from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.contrib.auth.models import User
from .models import SummaryEntry
from .serializers import SummaryEntrySerializer
from .utils import generate_summary, generate_bullet_points

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
