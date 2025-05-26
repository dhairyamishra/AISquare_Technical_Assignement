from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import SummaryEntry
from .serializers import SummaryEntrySerializer
from .utils import generate_summary, generate_bullet_points

class GenerateSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get('text')
        if text is None or text.strip() == "":
            return Response({"error": "Missing or empty 'text' field"}, status=status.HTTP_400_BAD_REQUEST)

        summary = generate_summary(text)
        entry = SummaryEntry.objects.create(text=text, summary=summary)
        return Response({"summary": summary}, status=status.HTTP_200_OK)


class GenerateBulletPointsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        text = request.data.get('text')
        if text is None or text.strip() == "":
            return Response({"error": "Missing or empty 'text' field"}, status=status.HTTP_400_BAD_REQUEST)

        bullet_points = generate_bullet_points(text)
        entry = SummaryEntry.objects.create(text=text, bullet_points=bullet_points)
        return Response({"bullet_points": bullet_points}, status=status.HTTP_200_OK)
