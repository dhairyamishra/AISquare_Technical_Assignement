from rest_framework import serializers
from .models import SummaryEntry
from .utils import sanitize_text

class SummaryEntrySerializer(serializers.ModelSerializer):
    text = serializers.CharField(
        max_length=10000,
        required=True,
        allow_blank=False,
        help_text="The full article or input text to summarize.",
    )
    
    class Meta:
        model = SummaryEntry
        fields = '__all__'
        read_only_fields = ('summary', 'bullet_points', 'created_at')
    
    def validate_text(self, value):
        return sanitize_text(value)
