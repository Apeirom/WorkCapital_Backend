# freelancers/models.py
from django.db import models
from django.contrib.auth.models import User # Importa o User padrão do Django
from workcapital_api.basemodels import BaseModel # Importa a Base que acabamos de criar

# -----------------
# 1. PERFIL CENTRAL DO USUÁRIO (UserProfile)
# Será a 'ponte' para todos os tipos de perfil e a base de dados
# -----------------
class UserProfile(BaseModel):
    # Relacionamento de 1 para 1 com o modelo User padrão do Django
    # Isso lida com email, password e autenticação.
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')

    # Parâmetros solicitados no seu esboço
    cpf = models.CharField(max_length=14, unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10) # Considere usar choices para padronização
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    account_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # RELACIONAMENTOS (Um-para-Muitos ou Um-para-Um)
    # Você não armazena listas de IDs em um campo, você usa ForeignKey (o inverso)
    # ou OneToOneField para perfis únicos.

    # Relacionamentos de OneToOne (se só puder ter 1 por vez)
    investor_profile = models.OneToOneField(
        'Investor', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profile'
    )
    contractor_profile = models.OneToOneField(
        'Contractor', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profile'
    )
    credit_taker_profile = models.OneToOneField(
        'CreditTaker', on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profile'
    )
    # Lista de Freelancer é 1:N (um perfil de usuário pode ter N perfis de freelancer - útil para diferentes CNPJs)
    # Usaremos uma relação reversa (ForeignKey) no modelo Freelancer.

    def __str__(self):
        return f"Perfil de {self.user.email}"
    
    # Método auxiliar para verificar se é freelancer (útil no futuro)
    @property
    def is_freelancer(self):
        return self.freelancer_profiles.exists() # O nome 'freelancer_profiles' será definido abaixo

# -----------------
# 2. MODELO FREELANCER (Agora ligado ao UserProfile)
# -----------------
class Freelancer(BaseModel):
    # Relacionamento 1:N (Um UserProfile pode ter N perfis de Freelancer)
    user_profile = models.ForeignKey(
        UserProfile, 
        on_delete=models.CASCADE, 
        related_name='freelancer_profiles'
    )
    
    # DADOS DO FREELANCER
    prof_title = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50) # Considere Choices
    suggest_hourly_rate = models.DecimalField(max_digits=6, decimal_places=2, default=0.00)
    
    # DADOS CHAVE PARA O SCORE (Serão alimentados pelos Projetos - relação reversa)
    avaliation_score = models.DecimalField(max_digits=3, decimal_places=2, default=0.00) 
    
    # Campo para a lista de experiências (em vez de lista de strings, use um modelo separado se for detalhado)
    # Para o MVP, Textfield pode ser mais simples:
    freelancer_experiences = models.TextField(default="[]", help_text="Lista JSON de experiências.") 
    
    # O campo projectsIds será a relação reversa (ForeignKey) no modelo Project.
    
    def __str__(self):
        return f"Freelancer: {self.name} ({self.user_profile.user.email})"
    
class Investor(BaseModel):
    # O relacionamento com o UserProfile já foi estabelecido acima (investor_profile)
    # O campo financingsids será a relação reversa (ForeignKey) no modelo Financing
    
    # Parâmetros relevantes
    risk_tolerance = models.CharField(max_length=50) 

    def __str__(self):
        return f"Investidor (ID: {self.id})"


class CreditTaker(BaseModel):
    # O relacionamento com o UserProfile já foi estabelecido acima (credit_taker_profile)
    # O campo financingsids será a relação reversa (ForeignKey) no modelo Financing
    
    contact_details = models.CharField(max_length=255)
    # O score WC é o score de crédito gerado pela sua IA
    wc_score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True) 

    def __str__(self):
        return f"Tomador de Crédito (ID: {self.id})"


class Contractor(BaseModel):
    # O relacionamento com o UserProfile já foi estabelecido acima (contractor_profile)
    # O campo projectsids será a relação reversa (ForeignKey) no modelo Project
    # O campo paymentsIds é melhor ser uma relação reversa (ForeignKey) de um modelo Payment
    
    company_name = models.CharField(max_length=100, null=True, blank=True) 

    def __str__(self):
        return f"Contratante (ID: {self.id})"