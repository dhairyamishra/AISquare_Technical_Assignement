from rest_framework import serializers
from .models import SummaryEntry

class SummaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = SummaryEntry
        fields = '__all__'
