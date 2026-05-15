from django.shortcuts import render, get_object_or_404, redirect
from .models import Producto, Categoria
from .forms import ProductoForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from .forms import RegistroUsuarioForm, CrearUsuarioForm, EditarRolForm
from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.shortcuts import render
from django.db.models import Sum, F
from .models import Producto, MovimientoProducto


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
@permission_required('inventario_app.add_producto', raise_exception=True)
def lista_productos(request):
    productos = Producto.objects.all()

    query = request.GET.get('buscar')

    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(sku__icontains=query)
        )
    context = {
        'productos': productos

    }

    return render(request, 'inventario_app/lista_productos.html', context)


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

    cantidad_anterior = producto.cantidad

    if request.method == 'POST':

        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():

            producto_actualizado = form.save()

            diferencia = producto_actualizado.cantidad - cantidad_anterior

            if diferencia != 0:

                tipo_movimiento = 'ENTRADA' if diferencia > 0 else 'SALIDA'

                MovimientoProducto.objects.create(
                    producto=producto_actualizado,
                    tipo=tipo_movimiento,
                    # abs() convierte números negativos a positivos
                    cantidad=abs(diferencia),
                    descripcion='Ajuste manual desde edición de producto'
                )

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


@login_required
@user_passes_test(es_admin)
@login_required
@user_passes_test(es_admin)
def vista_registro(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            # 1. Guardamos el usuario inicial
            user = form.save()

            # 2. Le damos estatus de staff para que no salga la pantalla blanca (403)
            user.is_staff = True
            user.save()  # Guardamos este cambio

            # 3. Buscamos el grupo 'almacenista' y metemos al usuario ahí
            try:
                grupo_almacenista = Group.objects.get(name='almacenista')
                user.groups.add(grupo_almacenista)
            except Group.DoesNotExist:
                print("Ojo: El grupo 'almacenista' no existe en la base de datos")

            return redirect('panel_admin')
    else:
        form = RegistroUsuarioForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, usuario_id):
    # 1. Buscamos al usuario en la base de datos usando el ID que nos llega
    usuario_a_eliminar = get_object_or_404(User, id=usuario_id)

    # 2. Seguridad: Evitamos que el superusuario se borre a sí mismo
    if usuario_a_eliminar == request.user:
        # Aquí podrías usar messages.error, pero por ahora solo lo redirigimos
        return redirect('panel_admin')

    # 3. Si no es tu propio usuario, lo eliminamos
    usuario_a_eliminar.delete()

    # 4. Volvemos a cargar el panel de administrador
    return redirect('panel_admin')


def dashboard_inventario(request):

    productos_activos = Producto.objects.filter(activo=True)

    total_productos = productos_activos.count()

    calculo_valor = productos_activos.aggregate(
        valor_total=Sum(F('cantidad') * F('precio_compra'))
    )

    valor_inventario = calculo_valor['valor_total'] or 0

    movimientos = MovimientoProducto.objects.all().order_by('-fecha')[:10]

    context = {
        'total_productos': total_productos,
        'valor_inventario': valor_inventario,
        'movimientos': movimientos,
    }

    return render(request, 'inventario_app/dashboard.html', context)
