from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.conf import settings
import jwt, time, random, string

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
            return redirect(f'https://censo-demo.die.educacion.gob.ar/login?token={token}')
        else:
            return render(request, 'loginapp/login.html', {
                'error': 'Credenciales inválidas'
            })

    return render(request, 'loginapp/login.html')
