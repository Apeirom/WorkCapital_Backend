# projects/models.py
from django.db import models
from workcapital_api.basemodels import BaseModel
from freelancers.models import Freelancer, Contractor # Importa os novos modelos

class Project(BaseModel):
    # Relacionamentos 1:N com os perfis
    freelancer = models.ForeignKey(
        Freelancer, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='projects_trabalhados'
    )
    contractor = models.ForeignKey(
        Contractor, 
        on_delete=models.CASCADE, 
        related_name='projects_contratados'
    )
    
    # Parâmetros solicitados
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=50)
    status = models.CharField(max_length=50, default='Open')
    project_start = models.DateField()
    project_forecast = models.DateField()
    url = models.URLField(null=True, blank=True)
    responsible = models.CharField(max_length=100) # Quem está gerenciando o projeto

    def __str__(self):
        return self.title