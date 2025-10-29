from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto
from .forms import ProductoForm

# 🟩 Listar
def lista_productos(request):
    productos = Producto.objects.all()  # type: ignore
    return render(request, 'inventario_app/lista_productos.html', {'productos': productos})

# 🟦 Crear
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm() 
    return render(request, 'inventario_app/crear_producto.html', {'form': form})

# 🟨 Editar
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

# 🟧 Detalle (Leer)
def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'inventario_app/detalle_producto.html', {'producto': producto})

# 🟥 Eliminar
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'inventario_app/eliminar_producto.html', {'producto': producto})
