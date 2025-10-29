"""
URL configuration for inventario project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from inventario_app import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('modificar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('detalle/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
]
