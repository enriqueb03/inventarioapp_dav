from django import forms
from inventario_app.models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['id', 'nombre', 'categoria', 'cantidad', 'precio', 'activo']
