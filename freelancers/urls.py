# freelancers/urls.py (Adicionar no início, antes do router.register)
from django.urls import path
from .views import (
    RegisterView, 
    FreelancerViewSet, 
    UserProfileViewSet, 
    InvestorViewSet, 
    ContractorViewSet, 
    CreditTakerViewSet,
)

# O 'router.urls' é uma lista, então adicionamos nossa rota customizada
urlpatterns = [
    path('register/', RegisterView.as_view(), name='user_register'),
] 
# O restante do código de 'freelancers.urls' que usa o router fica abaixo:
from rest_framework.routers import DefaultRouter
from .views import FreelancerViewSet, UserProfileViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'freelancers', FreelancerViewSet)
router.register(r'investors', InvestorViewSet)         
router.register(r'contractors', ContractorViewSet)
router.register(r'credit-takers', CreditTakerViewSet)

# Combina as rotas customizadas com as rotas geradas pelo router
urlpatterns += router.urls