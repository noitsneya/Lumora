from rest_framework import serializers
from .models import Memory, Patient, Caretaker

#serializers - convert mongoDB data into JSON (so we can send it using API)
class MemorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Memory
        fields = '__all__'  

class PatientSerializer(serializers.ModelSerializer):
    memories = MemorySerializer(many=True) 

    class Meta:
        model = Patient
        fields = '__all__'

class CaretakerSerializer(serializers.ModelSerializer):
    patient = PatientSerializer() 
    class Meta:
        model = Caretaker
        fields = '__all__'
