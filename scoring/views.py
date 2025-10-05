# scoring/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Financing
from .serializers import FinancingSerializer

class FinancingViewSet(viewsets.ModelViewSet):
    queryset = Financing.objects.all()
    serializer_class = FinancingSerializer
    permission_classes = [IsAuthenticated]