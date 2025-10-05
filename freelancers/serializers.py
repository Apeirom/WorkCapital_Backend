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


class UserRegistrationSerializer(serializers.ModelSerializer):
    # Campos que vêm do modelo User padrão
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    # Campos que vêm do modelo UserProfile
    cpf = serializers.CharField(max_length=14)
    # ... adicione aqui outros campos obrigatórios do UserProfile (phone, gender, etc.)

    class Meta:
        model = UserProfile
        # Incluímos os campos necessários para criar o User padrão e o UserProfile
        fields = ('id', 'email', 'password', 'cpf', 'phone', 'gender', 'city', 'state') 
        # Adicione todos os campos do UserProfile que você quer que o usuário preencha

    # Função para salvar (CRIA o User e o UserProfile)
    def create(self, validated_data):
        email_data = validated_data.pop('email')
        password_data = validated_data.pop('password')
        
        # 1. Cria o User Padrão (usa email para username e email)
        user = User.objects.create_user(
            username=email_data, # Username pode ser o email
            email=email_data,
            password=password_data
        )
        
        # 2. Cria o UserProfile (usa o restante dos dados validados)
        profile = UserProfile.objects.create(
            user=user, 
            **validated_data
        )
        return profile