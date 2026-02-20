from django.urls import path
from .views import (
    ProductListView, 
    ProductCreateView, 
    ProductRetrieveView, 
    ProductUpdateView, 
    ProductDeleteView,
    SignupView,
    LoginView,
    LogoutView
)

urlpatterns = [
    path('list/', ProductListView.as_view(), name='product-list'),
    path('create/', ProductCreateView.as_view(), name='product-create'),
    path('detail/<int:id>/', ProductRetrieveView.as_view(), name='product-detail'),
    path('update/<int:id>/', ProductUpdateView.as_view(), name='product-update'),
    path('delete/<int:id>/', ProductDeleteView.as_view(), name='product-delete'),

    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]