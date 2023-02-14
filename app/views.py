
# from base64 import urlsafe_b64decode, urlsafe_b64encode # esto es para decodificar el token y codificarlo
from django.core.mail import EmailMessage
# me cago en la puta madre, no me funcionaba el urlsafe_base64_encode, y era porque no habia importado esto
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  # POR ESTO NO FUNCIONABA, ME CAGO EN LA PUTA MADRE  
# puto django, no me funcionaba el urlsafe_base64_encode, y era porque no habia importado esto
from django.utils.encoding import force_bytes
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . tokens import account_activation_token as tokenGenerator
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from core import settings
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode # esto es para decodificar el token

# creacion de las vistas




# vista home
def home(request):
    return render(request, 'home.html')


# vista privada
@login_required
def pagina_privada(request):
    return render(request, 'authentication/ruta.html')


def crear_cuenta(request):

    if request.method == 'POST':
        usuario = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=usuario).exists():
            messages.error(request, "El usuario ya existe")
            return redirect('crear_cuenta')
        if User.objects.filter(email=email).exists():
            messages.error(request, "El email ya existe")
            return redirect('crear_cuenta')
        
        
        myuser = User.objects.create_user(usuario, email, password) # aqui creamos el usuario
        myuser.username = usuario # aqui le asignamos el nombre de usuario
        myuser.is_active = False # aqui le decimos que el usuario no esta activo, para que no pueda iniciar sesion
        myuser.save() # guardamos el usuario

        # le enviamos el email de confirmacion
        
        subject = 'Bienvenido, Por favor confirma tu email'
        
        message = render_to_string('authentication/confirmacion_email.html', {
            'user': myuser,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': tokenGenerator.make_token(myuser),
        })

        email = EmailMessage(subject, message, settings.EMAIL_HOST_USER, [myuser.email])
        email.fail_silently = True
        email.send()
        return redirect('iniciar_sesion')
        
    else:
        return render(request, 'authentication/crear_cuenta.html')


def iniciar_sesion(request):

    if request.method == 'POST':
        usuario = request.POST['username']
        passowrd = request.POST['password']

        validar = authenticate(username=usuario, password=passowrd)
        if validar is not None:
            login(request, validar)
            return redirect('pagina_privada')
           
    else:
        return render(request, 'authentication/iniciar_sesion.html')


def cerrar_sesion(request):
    logout(request)
    return redirect('home')


def activar_cuenta(request, uidb64, token):
    """
    Se intenta decodificar el valor de uidb64 en una cadena usando la función urlsafe_b64decode de la 
    biblioteca base64. Luego, se intenta obtener un objeto de usuario de la base de datos con el 
    identificador de usuario decodificado (uid).

    Si no se puede decodificar uidb64 o no se encuentra un objeto de usuario con el 
    identificador proporcionado, la variable user se establece en None.

    Si user no es None, se verifica si el token proporcionado es 
    válido usando el método check_token del generador de tokens (tokenGenerator).

    Si el token es válido, se establece el atributo is_active del usuario en True, 
    se guarda el usuario en la base de datos y se inicia la sesión del usuario con la 
    función login. Después, el usuario es redirigido a la página de inicio (home).

    Si el token no es válido, se renderiza la plantilla authentication/activar_cuenta.html 
    en el contexto de la petición request.
    """
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64)).decode('utf-8')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and tokenGenerator.check_token(user, token):
        user.is_active = True
        user.save()
        # login(request, user)
        return redirect('home')
    else:
        messages.error(request, 'No se pudo activar la cuenta!')
        return render(request, 'authentication/fallo_activar.html')


