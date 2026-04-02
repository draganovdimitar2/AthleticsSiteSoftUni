from rest_framework import serializers
from .models import Athlete, Discipline

class DisciplineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discipline
        fields = ['id', 'name']

class AthleteSerializer(serializers.ModelSerializer):
    disciplines = DisciplineSerializer(many=True, read_only=True)
    discipline_ids = serializers.PrimaryKeyRelatedField(
        many=True, 
        write_only=True, 
        queryset=Discipline.objects.all(),
        source='disciplines'
    )

    class Meta:
        model = Athlete
        fields = [
            'id', 'first_name', 'last_name', 'nationality', 
            'birth_date', 'gender', 'disciplines', 'discipline_ids',
            'created_at', 'updated_at'
        ]
