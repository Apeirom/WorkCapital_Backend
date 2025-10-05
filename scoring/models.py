# scoring/models.py
from django.db import models
from workcapital_api.basemodels import BaseModel
from freelancers.models import CreditTaker, Investor # Importa os novos modelos

class Financing(BaseModel):
    # Relacionamento com Tomador de Crédito
    credit_taker = models.ForeignKey(
        CreditTaker, 
        on_delete=models.CASCADE, 
        related_name='financings'
    )
    
    # Campo para a lista de investidores (Relação M:N)
    # Isso é melhor do que uma lista de IDs para o Django
    investors = models.ManyToManyField(
        Investor,
        related_name='invested_financings',
        blank=True
    )
    
    # Parâmetros solicitados
    code = models.CharField(max_length=20, unique=True)
    motivation = models.TextField()
    amount_request = models.DecimalField(max_digits=12, decimal_places=2)
    amount_invested = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    installments = models.IntegerField()
    first_installment_date = models.DateField()
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Financiamento {self.code} - Solicitado: {self.amount_request}"