# scoring/views.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Financing, Payment
from .serializers import FinancingSerializer, PaymentSerializer

from django.db import transaction

class FinancingViewSet(viewsets.ModelViewSet):
    queryset = Financing.objects.all()
    serializer_class = FinancingSerializer
    permission_classes = [IsAuthenticated]

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # 1. Salva o Payment no DB
        payment = serializer.save()
        
        # Usamos uma transação atômica para garantir que ambas as atualizações de saldo aconteçam
        with transaction.atomic():
            # 2. ATUALIZA O SALDO DO PAGADOR (Payer - Diminui o valor)
            if payment.payer:
                payment.payer.account_balance -= payment.amount
                payment.payer.save()

            # 3. ATUALIZA O SALDO DO RECEPTOR (Recipient - Aumenta o valor)
            if payment.recipient:
                payment.recipient.account_balance += payment.amount
                payment.recipient.save()