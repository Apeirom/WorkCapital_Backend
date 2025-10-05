from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UserRegistrationSerializer, UserProfileSerializer, FreelancerSerializer, InvestorSerializer, ContractorSerializer, CreditTakerSerializer
from .models import UserProfile, Freelancer, Investor, Contractor, CreditTaker 

from rest_framework.permissions import IsAuthenticated

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

class InvestorViewSet(viewsets.ModelViewSet):
    queryset = Investor.objects.all()
    serializer_class = InvestorSerializer
    permission_classes = [IsAuthenticated]

class ContractorViewSet(viewsets.ModelViewSet):
    queryset = Contractor.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = [IsAuthenticated]

class CreditTakerViewSet(viewsets.ModelViewSet):
    queryset = CreditTaker.objects.all()
    serializer_class = CreditTakerSerializer
    permission_classes = [IsAuthenticated]
