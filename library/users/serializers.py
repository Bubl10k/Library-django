from rest_framework import serializers

from .models import ReadingStats


class ReadingStatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingStats
        fields = ['year', 'month', 'pages_read']
        