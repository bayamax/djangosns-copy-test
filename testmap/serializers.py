from rest_framework import serializers
from testmap.models import Border

class BorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Border
        fields = ('__all__')