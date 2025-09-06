from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CandidatoUserCreationForm
from .forms import EmpleadorRegistrationForm
from .forms import EmpleadorRegistrationForm
from django.contrib import messages
from .forms import CandidatoForm
from .models import CandidatoPerfil, Candidato, PuestoDeTrabajo, Asignacion
from .forms import SeleccionCandidatoForm, AsignacionPuestoForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from .models import BaseUser
from django.shortcuts import get_object_or_404
from django.contrib.auth import update_session_auth_hash


#identificador central de pagina
def Identificador(request):
    infosu = "Información de identificador"
    return render(request, 'identificador.html', {'infosu': infosu})

#Informacion de infosu_cl
def home_infosu(request):
    infosu = "Información de identificador"
    return render(request, 'home_infosu.html', {'infosu': infosu})



#iniciar sesion candidato
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


#cerrar sesion candidato

def logout_view(request):
    logout(request)
    return redirect('login')



#registrar usuarios candidato
def register_view(request):
    if request.method == 'POST':
        form = CandidatoUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = CandidatoUserCreationForm()
    return render(request, 'register.html', {'form': form})




#registro de empleadores
def empleador_register_view(request):
    if request.method == 'POST':
        form = EmpleadorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('empleador_login')  # Redirige al inicio de sesión
    else:
        form = EmpleadorRegistrationForm()
    return render(request, 'empleador_register.html', {'form': form})



#incicio de sesion empleadores
def empleador_login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('empleador_dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'empleador_login.html', {'form': form})



#cierre de sesion empleadores
def empleador_logout_view(request):
    logout(request)
    return redirect(reverse('empleador_login'))


#requiere que los empleadores puedan contemplar las necesidades de login
@login_required
def empleador_dashboard_view(request):
    user = request.user
    candidatos = Candidato.objects.all()
    puestos_trabajo = PuestoDeTrabajo.objects.all()
    asignaciones = Asignacion.objects.all()
    asignacion_form = AsignacionPuestoForm() 

    if request.method == 'POST':
        asignacion_form = AsignacionPuestoForm(request.POST)
        if asignacion_form.is_valid():
            asignacion_form.save()
            return redirect('empleador_dashboard')

        candidato_id = request.POST.get('candidato_id')
        puesto_id = request.POST.get('puesto_id')
        Asignacion.objects.create(candidato_id=candidato_id, puesto_trabajo_id=puesto_id)
        form = SeleccionCandidatoForm(request.POST)



        return render(request, 'empleador_dashboard.html', {'user': user,  'puestos_trabajo': puestos_trabajo, 'asignaciones': asignaciones, 'puestos_trabajo': puestos_trabajo, 'form': form, 'asignacion_form': asignacion_form})
    else:
        form = SeleccionCandidatoForm()

    context = {
        'user': user,
        'form': form,
        'candidatos': candidatos,
        'puestos_trabajo': puestos_trabajo,
        'asignacion_form': asignacion_form,
    }
    return render(request, 'empleador_dashboard.html', context)





# Manejo de presentacion de los datos y su recepcion
def dashboard_view(request):
    candidato_data = CandidatoPerfil.objects.filter(user=request.user).first()
    puesto_asignado = candidato_data.puesto_de_trabajo if candidato_data else None
    asignaciones = Asignacion.objects.filter(candidato=request.user.candidato)
    # Obtiene el puesto de trabajo a través del modelo Candidato
    puesto_asignado = request.user.candidato.puesto_de_trabajo if request.user.candidato else None

    if request.method == 'POST':
        form = CandidatoForm(request.POST, request.FILES, instance=candidato_data)
        if form.is_valid():
            candidato_data = form.save(commit=False)
            candidato_data.user = request.user
            candidato_data.save()
            return redirect('dashboard')
    else:   
        form = CandidatoForm(instance=candidato_data)

    return render(request, 'dashboard.html', {'form': form, 'candidato_data': candidato_data, 'puesto_asignado': puesto_asignado, 'asignaciones': asignaciones})



#muestra los candidatos con lo que ingresaron en su vista
def mostrar_candidatos(request):
    if request.method == 'POST':
        form = SeleccionCandidatoForm(request.POST)
        if form.is_valid():
            candidato_seleccionado = form.cleaned_data['candidato']
            usuario_1 = CandidatoPerfil.objects.get(user=candidato_seleccionado)
            return render(request, 'empleador_dashboard.html', {'candidato_seleccionado': usuario_1, 'form': form})
    return redirect('empleador_dashboard')


# funcion para descargar
def descargar_archivo_candidato(request, candidato_perfil_id, archivo):
    candidato_perfil = get_object_or_404(CandidatoPerfil, pk=candidato_perfil_id)

    # Determina el campo de archivo correspondiente
    if archivo == 'archivo1':
        archivo_candidato = candidato_perfil.archivo1
    elif archivo == 'archivo2':
        archivo_candidato = candidato_perfil.archivo2
    elif archivo == 'archivo3':
        archivo_candidato = candidato_perfil.archivo3
    else:
        # Manejo de error si el archivo no es válido
        return HttpResponse("Archivo no válido", status=400)

    # Configura la respuesta HTTP para la descarga del archivo
    response = HttpResponse(archivo_candidato, content_type='application/force-download')
    response['Content-Disposition'] = f'attachment; filename="{archivo_candidato.name}"'

    return response


#asigna el puesto de trabajador 
def asignarpuesto(request):
    if request.method == 'POST':
        form = AsignacionPuestoForm(request.POST)
        if form.is_valid():
            asignacion = form.save()
    else:
        form = AsignacionPuestoForm()

    data = {'form': form}
    return render(request, 'empleador_dashboard.html', data)


#resbtalece contraseña de candidato y empleador
def reset_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        try:
            # Busca el usuario por su dirección de correo electrónico
            user = BaseUser.objects.get(email=email)
            
            # Cambia la contraseña del usuario
            user.set_password(new_password)
            user.save()

            # Asegúra de que el usuario siga autenticado después de cambiar la contraseña
            update_session_auth_hash(request, user)

            messages.success(request, 'Contraseña actualizada exitosamente. Inicia sesión con tu nueva contraseña.')
            return redirect('identificador')  # Redirige al candidato o empleador al inicio de sesión después de cambiar la contraseña
        
        except BaseUser.DoesNotExist:
            messages.error(request, 'El correo electrónico proporcionado no está registrado.')

    return render(request, 'reset_password.html')