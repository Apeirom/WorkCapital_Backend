from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserRegistrationSerializer, UserProfileSerializer, FreelancerSerializer, InvestorSerializer, ContractorSerializer, CreditTakerSerializer
from .models import UserProfile, Freelancer, Investor, Contractor, CreditTaker 

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

class RegisterView(APIView):
    # Permite acesso mesmo sem estar autenticado
    permission_classes = [] 

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    # Permite apenas usuários logados!
    permission_classes = [IsAuthenticated]

class FreelancerViewSet(viewsets.ModelViewSet):
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        """
        GET /api/freelancers/{id}/projects/
        Retorna todos os projetos em que este freelancer trabalhou.
        """
        freelancer = self.get_object()
        # Usa o related_name 'projects_worked_on' definido no modelo Project
        projects = freelancer.projects_worked_on.all() 
        
        # Você deve usar o ProjectSerializer aqui
        serializer = ProjectSerializer(projects, many=True) 
        return Response(serializer.data)

class InvestorViewSet(viewsets.ModelViewSet):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer
    permission_classes = [IsAuthenticated]

class ContractorViewSet(viewsets.ModelViewSet):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        """
        GET /api/contractors/{id}/projects/
        Retorna todos os projetos criados por este contratante.
        """
        contractor = self.get_object()
        # Usa o related_name 'created_projects' definido no modelo Project
        projects = contractor.created_projects.all()
        
        # Você deve usar o ProjectSerializer aqui
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

class CreditTakerViewSet(viewsets.ModelViewSet):
    queryset = CreditTaker.objects.all()
    serializer_class = CreditTakerSerializer
    permission_classes = [IsAuthenticated]
