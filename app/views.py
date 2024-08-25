from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from .models import Paciente, Consumos, RegistroEliminado
from .forms import PacienteForm, ConsumosForm
from django.contrib import messages
from django.db.models import Q, Sum
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import transaction

# para la vista de pacientes
@login_required
def paciente_index(request):
    # Inicializar queryset
    pacientes = Paciente.objects.all()

    # Búsqueda general
    search_query = request.GET.get('search', '')
    # Filtros de fecha
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    # Bandera para indicar si se ha realizado una búsqueda
    is_search = bool(search_query or year or month or day)

    # Inicializar total_pacientes
    total_pacientes = 0  # Inicialización aquí

    # Aplicar filtros si hay una búsqueda
    if is_search:
        if year:
            pacientes = pacientes.filter(fecha__year=year)
            if month:
                pacientes = pacientes.filter(fecha__month=month)
                if day:
                    pacientes = pacientes.filter(fecha__day=day)

        if search_query:
            pacientes = pacientes.filter(
                Q(nombre__icontains=search_query) |
                Q(apellido__icontains=search_query) |
                Q(cedula__contains=search_query) |
                Q(sexo__icontains=search_query) |
                Q(procedimiento__icontains=search_query) |
                Q(costo__contains=search_query) |
                Q(forma_de_pago__icontains=search_query)
            )

    # Ordenar el queryset después de aplicar los filtros
    pacientes = pacientes.order_by('-fecha', 'id')

    # Calcular la suma total de costos
    if is_search:
        total_costos = pacientes.aggregate(total=Sum('costo'))['total'] or 0
        # Calcular el total de pacientes
        total_pacientes = pacientes.count()
    else:
        total_costos = None

    # Verificar si no se encontraron pacientes
    no_results_message = "No se encontraron coincidencias." if not pacientes.exists() else None

    # Paginación
    paginator = Paginator(pacientes, 7)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'pacientes': page_obj,
        'no_results_message': no_results_message,
        'search_query': search_query,
        'year': year,
        'month': month,
        'day': day,
        'total_costos': total_costos,
        'total_pacientes': total_pacientes,
        'is_search': is_search
    }
    return render(request, 'paciente/index.html', context)


@login_required
def paciente_view(request, id):
    paciente = Paciente.objects.get(id=id)
    context = {
        'paciente': paciente
    }
    return render(request, 'paciente/detail.html', context)


# para que al darle al botón de whatsapp nos redirija a whatsapp
@login_required
def whatsapp_redirect(request, paciente_id):
    paciente = get_object_or_404(Paciente, id=paciente_id)
    telefono = ''.join(filter(str.isdigit, paciente.telefono))
    
    # Verificar si es un dispositivo móvil
    user_agent = request.META.get('HTTP_USER_AGENT', '').lower()
    mobile_agents = ['android', 'webos', 'iphone', 'ipad', 'ipod', 'blackberry', 'windows phone']
    is_mobile = any(agent in user_agent for agent in mobile_agents)
    
    if is_mobile:
        whatsapp_url = f"https://api.whatsapp.com/send?phone={telefono}"
    else:
        whatsapp_url = f"https://web.whatsapp.com/send?phone={telefono}"
    
    # Redirigir directamente a la URL de WhatsApp
    return HttpResponseRedirect(whatsapp_url)


@login_required
def paciente_edit(request, id):
    paciente = Paciente.objects.get(id=id)

    # para que al darle al botón de editar nos muestre el formulario lleno y poder editarlo
    if request.method == 'GET':
        form = PacienteForm(instance=paciente)
        context = {
            'form': form,
            'id': id
        }
        return render(request, 'paciente/edit.html', context)

    # para que al editarlo y darle a guardar este guarde lo editado y sustituya al anterior
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
        context = {
            'form': form,
            'id': id
        }
        messages.success(request, "Paciente actualizado.")
        return render(request, 'paciente/edit.html', context)


@login_required
def paciente_add(request):
    # para darle al botón añadir y crear el formulario
    if request.method == 'GET':
        form = PacienteForm()
        context = {
            'form': form
        }
        return render(request, 'paciente/add.html', context)
    
    # para crear y guardar el nuevo paciente
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Paciente registrado exitosamente.")
            return redirect('paciente_add')
    else:
        form = PacienteForm()
    
    context = {
        'form': form
    }
    return render(request, 'paciente/add.html', context)


@login_required
def paciente_delete(request, id):
    return redirect('paciente_confirm_delete', id=id)  


@login_required
def paciente_confirm_delete(request, id):
    paciente = get_object_or_404(Paciente, id=id)
    if request.method == 'POST':
        # para que si hay un error en el registro no se guarde nada 
        with transaction.atomic():
            # Guardar el registro del paciente eliminado
            datos_paciente = {
                'id': paciente.id,
                'nombre': paciente.nombre,
                'apellido': paciente.apellido,
                'cedula': paciente.cedula,
                'sexo': paciente.sexo,
                'telefono': paciente.telefono,
                'procedimiento': paciente.procedimiento,
                'costo': str(paciente.costo),
                'forma_de_pago': paciente.forma_de_pago,
                'fecha': str(paciente.fecha),
                # Añade aquí todos los campos relevantes del paciente
            }
            RegistroEliminado.objects.create(
                tipo='paciente',
                datos=datos_paciente,
                eliminado_por=request.user
            )
            
            # Eliminar el paciente
            paciente.delete()
        
        messages.success(request, "Paciente eliminado")
        return redirect('paciente')
    context = {
        'paciente': paciente
    }
    return render(request, 'paciente/paciente_confirm_delete.html', context)

##############################################################################################

@login_required
def consumo_index(request):
    # Inicializar queryset
    consumos = Consumos.objects.all()

    # Búsqueda general
    search_query = request.GET.get('search', '')
    # Filtros de fecha
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    # Bandera para indicar si se ha realizado una búsqueda
    is_search = bool(search_query or year or month or day)

    # Inicializar total_consumos
    numero_consumos = 0  # Inicialización aquí
    
    # Aplicar filtros si hay una búsqueda
    if is_search:
        if year:
            consumos = consumos.filter(fecha__year=year)
            if month:
                consumos = consumos.filter(fecha__month=month)
                if day:
                    consumos = consumos.filter(fecha__day=day)

        if search_query:
            consumos = consumos.filter(
                Q(producto__icontains=search_query) |
                Q(costo__contains=search_query)
            )

    # Ordenar el queryset después de aplicar los filtros
    consumos = consumos.order_by('-fecha', 'id')

    # Calcular la suma total de costos
    if is_search:
        total_costos = consumos.aggregate(total=Sum('costo'))['total'] or 0
        # Calcular el total de pacientes
        numero_consumos = consumos.count()
    else:
        total_costos = None

    # Verificar si no se encontraron consumos
    no_results_message = "No se encontraron coincidencias." if not consumos.exists() else None

    # Paginación
    paginator = Paginator(consumos, 7)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.get_page(1)
    except EmptyPage:
        page_obj = paginator.get_page(paginator.num_pages)

    context = {
        'consumos': page_obj,
        'no_results_message': no_results_message,
        'search_query': search_query,
        'year': year,
        'month': month,
        'day': day,
        'total_costos': total_costos,
        'numero_consumos': numero_consumos,
        'is_search': is_search
    }
    return render(request, 'consumos/index.html', context)


@login_required
def consumo_view(request, id):
    consumo = Consumos.objects.get(id=id)
    context = {
        'consumo': consumo
    }
    return render(request, 'consumos/detail.html', context)


@login_required
def consumo_edit(request, id):
    consumo = Consumos.objects.get(id=id)

    if request.method == 'GET':
        form = ConsumosForm(instance=consumo)
        context = {
            'form': form,
            'id': id
        }
        return render(request, 'consumos/edit.html', context)

    if request.method == 'POST':
        form = ConsumosForm(request.POST, instance=consumo)
        if form.is_valid():
            form.save()
        context = {
            'form': form,
            'id': id
        }
        messages.success(request, "Consumo actualizado.")
        return render(request, 'consumos/edit.html', context)


@login_required
def consumo_add(request):
    if request.method == 'GET':
        form = ConsumosForm()
        context = {
            'form': form
        }
        return render(request, 'consumos/add.html', context)
    
    if request.method == 'POST':
        form = ConsumosForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Consumo registrado exitosamente.")
            return redirect('consumo_add')
    else:
        form = ConsumosForm()
    
    context = {
        'form': form
    }
    return render(request, 'consumos/add.html', context)


@login_required
def consumo_delete(request, id):
    return redirect('consumo_confirm_delete', id=id)  


@login_required
def consumo_confirm_delete(request, id):
    consumo = get_object_or_404(Consumos, id=id)
    if request.method == 'POST':
        with transaction.atomic():
            datos_consumo = {
                'id': consumo.id,
                'producto': consumo.producto,
                'costo': str(consumo.costo),
                'fecha': str(consumo.fecha),
                # Añade aquí todos los campos relevantes del consumo
            }
            RegistroEliminado.objects.create(
                tipo='consumo',
                datos=datos_consumo,
                eliminado_por=request.user
            )
            
            consumo.delete()
        
        messages.success(request, "Consumo eliminado")
        return redirect('consumo')
    context = {
        'consumo': consumo
    }
    return render(request, 'consumos/consumo_confirm_delete.html', context)


#########################################################################################

@login_required
def total_costos(request):
    # Inicializar variables
    total_pacientes = 0
    total_consumos = 0
    total_general = 0
    is_search = False

    # Filtros de fecha
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    # Búsqueda general
    search_paciente = request.GET.get('search_paciente', '')
    search_consumo = request.GET.get('search_consumo', '')

    if year or month or day or search_paciente or search_consumo:
        is_search = True
        
        # Filtrar pacientes
        pacientes = Paciente.objects.all()
        if year:
            pacientes = pacientes.filter(fecha__year=year)
        if month:
            pacientes = pacientes.filter(fecha__month=month)
        if day:
            pacientes = pacientes.filter(fecha__day=day)
        if search_paciente:
            pacientes = pacientes.filter(
                Q(nombre__icontains=search_paciente) |
                Q(apellido__icontains=search_paciente) |
                Q(cedula__contains=search_paciente) |
                Q(sexo__icontains=search_paciente) |
                Q(procedimiento__icontains=search_paciente) |
                Q(costo__contains=search_paciente) |
                Q(forma_de_pago__icontains=search_paciente)
            )
        total_pacientes = pacientes.aggregate(total=Sum('costo'))['total'] or 0

        # Filtrar consumos
        consumos = Consumos.objects.all()
        if year:
            consumos = consumos.filter(fecha__year=year)
        if month:
            consumos = consumos.filter(fecha__month=month)
        if day:
            consumos = consumos.filter(fecha__day=day)
        if search_consumo:
            consumos = consumos.filter(
                Q(producto__icontains=search_consumo) |
                Q(costo__icontains=search_consumo)
            )
        total_consumos = consumos.aggregate(total=Sum('costo'))['total'] or 0

        # Calcular total general
        total_general = total_pacientes - total_consumos

    context = {
        'year': year,
        'month': month,
        'day': day,
        'search_paciente': search_paciente,
        'search_consumo': search_consumo,
        'total_pacientes': total_pacientes,
        'total_consumos': total_consumos,
        'total_general': total_general,
        'is_search': is_search
    }
    return render(request, 'totales/total_costos.html', context)
