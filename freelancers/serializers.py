# freelancers/serializers.py
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
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
    # 1. CAMPOS VIRTUAIS (Novas informações para o frontend)
    
    # title: Já existe como 'prof_title' no modelo, vamos criar um alias
    title = serializers.CharField(source='prof_title', read_only=True)
    
    # city: Busca a cidade e o estado do UserProfile relacionado (relacionamento 1:N)
    city = serializers.SerializerMethodField() 
    
    # profileType: Gera um rótulo baseado em alguma métrica (simulação de lógica de negócio)
    profileType = serializers.SerializerMethodField()

    # images: Retorna uma lista de URLs fixas (Mock)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Freelancer
        # Campos que o frontend vai ver (title substitui prof_title)
        fields = (
            'id', 'title', 'profileType', 'description', 'city', 
            'avaliation_score', 'suggest_hourly_rate', 'category'
        )
        read_only_fields = ('id', 'created_at', 'updated_at', 'avaliation_score') 

    # --- MÉTODOS CUSTOMIZADOS (Implementando a Lógica) ---
    
    # 1. Método para obter a cidade (City, State)
    def get_city(self, obj):
        # obj é o objeto Freelancer. Acessa o UserProfile para pegar cidade/estado.
        if obj.user_profile and obj.user_profile.city and obj.user_profile.state:
            return f"{obj.user_profile.city}, {obj.user_profile.state}"
        return "Local não informado"

    # 2. Método para obter o Tipo de Perfil (Simulação)
    def get_profileType(self, obj):
        # Lógica: Baseado no score (avaliation_score) ou em projetos.
        score = obj.avaliation_score or 0 # Pega o score (0 se for null)
        
        if score >= 85:
            return "Perfil Campeão"
        elif score >= 50:
            return "Perfil Verificado"
        else:
            return "Novo Talento"

    # 3. Método para obter a Descrição
    def get_description(self, obj):
        # Para o MVP, você pode retornar algo fixo ou usar o campo 'prof_title'
        return f"{obj.prof_title} focado em resultados, criativo e pontual. Transforma ideias em soluções digitais que impulsionam negócios."

        
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
        
        # 1. Cria o User Padrão
        user = User.objects.create_user(
            username=email_data,
            email=email_data,
            password=password_data
        )
        
        # 2. Cria o Contractor (Obrigatório para o UserProfile)
        contractor = Contractor.objects.create() 

        # 3. Cria o UserProfile, LIGANDO O CONTRACTOR NA HORA
        # Os dados restantes do validated_data (cpf, city, state) são usados aqui
        profile = UserProfile.objects.create(
            user=user,
            contractor_profile=contractor, # FAZ A LIGAÇÃO
            **validated_data
        )
        # O profile.save() é desnecessário agora

        return profile
    
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer customizado que adiciona os dados do UserProfile à resposta JWT.
    """
    @classmethod
    def get_token(cls, user):
        # Chama a função base para gerar os tokens
        token = super().get_token(user)
        
        # Adiciona campos extras ao payload do token, se necessário.
        # token['username'] = user.username 
        
        return token

    def validate(self, attrs):
        # Executa a validação padrão (que gera os tokens 'access' e 'refresh')
        data = super().validate(attrs)

        # Após a validação (e geração bem-sucedida dos tokens), 
        # anexa os dados do UserProfile serializados.
        
        try:
            # Pega o UserProfile via a relação 'profile'
            user_profile = self.user.profile
            
            # Serializa o UserProfile usando o Serializer que já existe
            profile_serializer = UserProfileSerializer(user_profile)
            
            # Adiciona a chave 'user' (com os dados do perfil) à resposta
            data['user'] = profile_serializer.data
            
        except UserProfile.DoesNotExist:
            # Caso o usuário logado não tenha um UserProfile, retorna um erro ou um perfil vazio.
            # Para o hackathon, vamos retornar vazio.
            data['user'] = None
        
        return data