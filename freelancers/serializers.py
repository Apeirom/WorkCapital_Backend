# freelancers/serializers.py
from rest_framework import serializers
from .models import Freelancer, UserProfile, Contractor, Investor, CreditTaker
from django.contrib.auth.models import User # Para o modelo de autenticação

# Serializers para os Perfis (simples para o MVP)
class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class ContractorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contractor
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

class CreditTakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditTaker
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
        
# Serializer do Freelancer (melhorado)
class FreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freelancer
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'avaliation_score') # Avaliação é gerada
        
# Serializer Principal do Usuário (CRUCIAL para Cadastro)
class UserProfileSerializer(serializers.ModelSerializer):
    # Relacionamento OneToOne para Perfis
    investor_profile = InvestorSerializer(read_only=True)
    contractor_profile = ContractorSerializer(read_only=True)
    credit_taker_profile = CreditTakerSerializer(read_only=True)
    
    # Exibe todos os perfis de freelancer relacionados (Many-to-One)
    freelancer_profiles = FreelancerSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at', 'user') # O campo user será lidado separadamente