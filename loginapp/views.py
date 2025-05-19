from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
import jwt, time, random, string, requests, logging

logger = logging.getLogger(__name__)

def root_redirect(request):
    return redirect('/login/')

def generar_jti():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=32))

def login_view(request):
    if request.method == 'POST':
        cuil = request.POST.get('username') # en el form sigue llamándose "username"
        password = request.POST.get('password') # que también será el CUIL
        
        user = authenticate(username=cuil, password=password)
        if user is not None:
            login(request, user)

            if user.is_staff:
                # Usuario administrador: redirigir al panel de administración
                return redirect('/admin/')

            # Usuario director: generar JWT y redirigir al sistema nacional
            payload = {
                'user_id': user.id,
                'nombre': user.first_name,
                'apellido': user.last_name,
                'email': user.email,
                'login': user.username,
                'CUE': [c.cue for c in user.cues.all()],
                'jti': generar_jti(),
                'exp': time.time() + 300  # 5 minutos
            }

            token = jwt.encode(payload, settings.JWT_SECRET, algorithm='HS256')

            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
            }
            
            # Enviar POST al sistema nacional
            try:
                response = requests.post(
                    settings.LOGIN_REDIRECT_URL,
                    # json={'token': token},
                    headers=headers,
                    timeout=10
                )

                if response.status_code == 200:
                    data = response.json()
                    final_url = data.get('url')
                    if final_url:
                        return redirect(final_url)
                    else:
                        return render(request, 'loginapp/login.html', {
                            'error': 'El sistema nacional no devolvió una URL válida.'
                        })
                else:
                    logger.error(f"[POST ERROR] Código {response.status_code} - Contenido: {response.text}")
                    
                    return render(request, 'loginapp/login.html', {
                        # 'error': f'Error desde sistema nacional ({response.status_code})'
                        'error': 'Error desde sistema nacional. Por favor, intente nuevamente más tarde.'
                    })
            except requests.RequestException as e:
                return render(request, 'loginapp/login.html', {
                    'error': f'No se pudo conectar con sistema nacional: {e}'
                })
        else:
            return render(request, 'loginapp/login.html', {
                'error': 'Credenciales inválidas'
            })

    return render(request, 'loginapp/login.html')

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib import messages
from .models import CUEUsuario
import csv
from io import TextIOWrapper

@staff_member_required
def importar_directores_view(request):
    resultado = None

    if request.method == 'POST' and request.FILES.get('archivo_csv'):
        archivo = request.FILES['archivo_csv']
        try:
            contenido = TextIOWrapper(archivo.file, encoding='latin-1')
            reader = csv.DictReader(contenido)

            total, nuevos, actualizados, errores = 0, 0, 0, 0

            for fila in reader:
                total += 1
                try:
                    email = fila['email'].strip().lower()
                    cuil = fila['cuil'].strip()
                    nombre = fila['nombre'].strip()
                    apellido = fila['apellido'].strip()
                    cues = [c.strip() for c in fila['cues'].split(';') if c.strip()]

                    user, creado = User.objects.get_or_create(username=cuil, defaults={
                        'email': email,
                        'first_name': nombre,
                        'last_name': apellido,
                    })
                    user.set_password(cuil)
                    user.save()

                    if not creado:
                        actualizados += 1
                    else:
                        nuevos += 1

                    CUEUsuario.objects.filter(user=user).delete()
                    for cue in cues:
                        CUEUsuario.objects.create(user=user, cue=cue)

                except Exception:
                    errores += 1
                    continue

            resultado = {
                'total': total,
                'nuevos': nuevos,
                'actualizados': actualizados,
                'errores': errores
            }

        except Exception as e:
            messages.error(request, f"Error al procesar el archivo: {e}")

    return render(request, 'loginapp/importar_directores.html', {'resultado': resultado})
