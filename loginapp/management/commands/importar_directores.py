import csv
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from loginapp.models import CUEUsuario

class Command(BaseCommand):
    help = 'Importa usuarios desde un archivo CSV y asigna CUEs'

    def add_arguments(self, parser):
        parser.add_argument('--archivo', type=str, required=True, help='Ruta al archivo CSV a importar')

    def handle(self, *args, **options):
        archivo_csv = options['archivo']

        try:
            with open(archivo_csv, newline='', encoding='latin-1') as csvfile:
                reader = csv.DictReader(csvfile)
                total = 0
                nuevos = 0
                actualizados = 0
                errores = 0

                for fila in reader:
                    total += 1
                    email = fila['email'].strip().lower()
                    cuil = fila['cuil'].strip()
                    nombre = fila['nombre'].strip()
                    apellido = fila['apellido'].strip()
                    cues_raw = fila['cues'].strip()

                    if not email or not cuil or not cues_raw:
                        self.stderr.write(f"Fila inválida (faltan campos): {fila}")
                        errores += 1
                        continue

                    user, creado = User.objects.get_or_create(username=email, defaults={
                        'email': email,
                        'first_name': nombre,
                        'last_name': apellido
                    })

                    user.set_password(cuil)  # CUIL como contraseña
                    user.save()

                    if creado:
                        nuevos += 1
                        self.stdout.write(f"✓ Usuario nuevo: {email}")
                    else:
                        actualizados += 1
                        self.stdout.write(f"• Usuario actualizado: {email}")

                    # Eliminar CUEs previos para evitar duplicados
                    CUEUsuario.objects.filter(user=user).delete()

                    cues = [c.strip() for c in cues_raw.split(';') if c.strip()]
                    for cue in cues:
                        CUEUsuario.objects.create(user=user, cue=cue)

                self.stdout.write(self.style.SUCCESS(f"\nImportación finalizada:"))
                self.stdout.write(f"Total procesados: {total}")
                self.stdout.write(f"Nuevos: {nuevos}, Actualizados: {actualizados}, Errores: {errores}")

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"No se encontró el archivo: {archivo_csv}"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Error inesperado: {e}"))
