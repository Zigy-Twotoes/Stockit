from django.urls import path
from . import views


urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', views.Home.as_view(), name='login'),
    path('', views.Home.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='products-list'),
    path('products/create/', views.ProductCreateView.as_view(), name='products-create'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='products-detail'),
    path('products/<int:pk>/update/', views.ProductUpdateView.as_view(), name='products-update'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='products-delete'),
    path('orders/create/', views.OrderGuideCreateView.as_view(), name='orders-create'),
    path('orders/<int:pk>/update/', views.OrderGuideUpdateView.as_view(), name='orders-update'), 
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='orders-detail'),
    path('orders/', views.OrderHistoryListView.as_view(), name='orders-history'), 
    path('orders/<int:pk>/delete/', views.OrderDeleteView.as_view(), name='orders-delete'),  
]