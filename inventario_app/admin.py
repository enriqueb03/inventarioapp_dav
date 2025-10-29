from django.contrib import admin
from .models import Categoria  
from .models import  Producto 

admin.site.register(Categoria)

admin.site.register(Producto)