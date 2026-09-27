from rest_framework import serializers

from .models import KBEntry


class KBEntrySerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)

    class Meta:
        model = KBEntry
        fields = ['id', 'question', 'answer', 'category']
