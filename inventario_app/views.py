from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required, permission_required 
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import user_passes_test
from .forms import RegistroUsuarioForm


def es_admin(user):
    return user.is_superuser

@login_required
@user_passes_test(es_admin)  
def panel_admin(request):
    usuarios = User.objects.all()
    contexto = {
        'usuarios': usuarios
    }
    return render(request, 'inventario_app/panel_admin.html', contexto)


@login_required
@permission_required('inventario_app.view_producto', raise_exception=True)
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'inventario_app/lista_productos.html', {'productos': productos})


@login_required
@permission_required('inventario_app.add_producto', raise_exception=True)
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()
    return render(request, 'inventario_app/form_productos.html', {'form': form, 'accion': 'Agregar'})



@login_required
@permission_required('inventario_app.change_producto', raise_exception=True)
def editar_producto(request, pk):
    

    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':

        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
 
        form = ProductoForm(instance=producto)
        

    return render(request, 'inventario_app/form_productos.html', {'form': form, 'accion': 'Editar'})


@login_required
@permission_required('inventario_app.delete_producto', raise_exception=True)
def eliminar_producto(request, pk):
    

    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':

        producto.delete()
        return redirect('lista_productos')
    
    return render(request, 'inventario_app/eliminar_producto.html', {'producto': producto})

@login_required
@permission_required('inventario_app.view_producto', raise_exception=True)
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'inventario_app/detalles_producto.html', {'producto': producto})

def vista_registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            login(request, user)
            
            return redirect('lista_productos')
    else:
        form = RegistroUsuarioForm()
        
    return render(request, 'registration/signup.html', {'form': form})
