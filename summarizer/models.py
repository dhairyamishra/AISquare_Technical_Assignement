from django.db import models

class SummaryEntry(models.Model):
    text = models.TextField()
    summary = models.TextField(blank=True)
    bullet_points = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"SummaryEntry #{self.id}"
