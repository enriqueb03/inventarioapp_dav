from django import forms
from .models import Producto 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

FORM_CONTROL_CLASS = 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline'
CHECKBOX_CLASS = 'h-4 w-4 text-blue-600 border-gray-300 rounded focus:ring-blue-500 ml-2'

FORM_FILE_CLASS = 'block w-full text-sm text-gray-700 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100'
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['sku', 'imagen',  'nombre', 'categoria', 'cantidad', 'precio_compra','precio_venta', 'activo']

        widgets = {
            'sku': forms.TextInput(attrs={'class': FORM_CONTROL_CLASS}),
            'imagen': forms.ClearableFileInput(attrs={'class': FORM_FILE_CLASS}),
            'nombre': forms.TextInput(attrs={'class': FORM_CONTROL_CLASS}),
            'categoria': forms.Select(attrs={'class': FORM_CONTROL_CLASS}),
            'cantidad': forms.NumberInput(attrs={'class': FORM_CONTROL_CLASS}),
            'precio_compra': forms.NumberInput(attrs={'class':    FORM_CONTROL_CLASS}),
            'precio_venta': forms.NumberInput(attrs={'class':    FORM_CONTROL_CLASS}),
            'activo': forms.CheckboxInput(attrs={'class': CHECKBOX_CLASS}),
        }
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'appearance-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
            })