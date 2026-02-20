from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from decimal import Decimal
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import Product
from .serializers import ProductSerializer, UserSerializer, ResetPasswordSerializer

class ProductListView(GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get(self, request):
        search = request.query_params.get('search', None)
        price_min = request.query_params.get('price', None)
        
        queryset = self.get_queryset()

        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )
        
        if price_min:
            queryset = queryset.filter(price__gte=Decimal(price_min))

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Products list',
            'data': serializer.data
        })

class ProductCreateView(GenericAPIView):
    serializer_class = ProductSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'Product created',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        
        return Response({
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Error',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ProductRetrieveView(GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product)
        return Response({
            'status': status.HTTP_200_OK,
            'data': serializer.data
        })

class ProductUpdateView(GenericAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    lookup_field = 'id'

    def put(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Updated',
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        product = self.get_object()
        serializer = self.get_serializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'status': status.HTTP_200_OK,
                'data': serializer.data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDeleteView(GenericAPIView):
    queryset = Product.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        product.delete()
        return Response({
            'status': status.HTTP_204_NO_CONTENT,
            'message': 'Deleted successfully'
        }, status=status.HTTP_204_NO_CONTENT)


class SignupView(GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'status': status.HTTP_201_CREATED,
                'message': 'User registered successfully',
                'token': token.key,
                'user': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(GenericAPIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'status': status.HTTP_200_OK,
                'message': 'Login successful',
                'token': token.key
            })
        return Response({
            'status': status.HTTP_401_UNAUTHORIZED,
            'message': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({
            'status': status.HTTP_200_OK,
            'message': 'Logged out successfully'
        })

class ResetPasswordView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.data.get("old_password")):
                return Response({
                    "message": "Old password is incorrect"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.set_password(serializer.data.get("new_password"))
            user.save()
            return Response({
                "status": status.HTTP_200_OK,
                "message": "Password updated successfully"
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)