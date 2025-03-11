#from django.shortcuts import render
from rest_framework import viewsets
from .models import Memory, Patient, Caretaker
from .serializers import MemorySerializer, PatientSerializer, CaretakerSerializer

class MemoryViewSet(viewsets.ModelViewSet):
    queryset = Memory.objects.all()
    serializer_class = MemorySerializer

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

class CaretakerViewSet(viewsets.ModelViewSet):
    queryset = Caretaker.objects.all()
    serializer_class = CaretakerSerializer


