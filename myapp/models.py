from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Clase donde se guardan los datos generales de los usuarios
class BaseUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        if not username:
            raise ValueError('El nombre de usuario es obligatorio')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Los superusuarios deben tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Los superusuarios deben tener is_superuser=True')

        return self.create_user(email, username, password, **extra_fields)

# Campos donde se guardan los datos generales de los usuarios
class BaseUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_candidate = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)

    objects = BaseUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

# Clase personalizada de Django para crear usuarios personalizados, aplica para candidato y empleador
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, rut=None, **extra_fields):
        return super().create_user(email, username, password=password, **extra_fields, rut=rut)

    def create_superuser(self, email, username, password=None, rut=None, **extra_fields):
        return super().create_superuser(email, username, password=password, **extra_fields, rut=rut)
        
# Modelo de puesto de trabajo
class PuestoDeTrabajo(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

# Usuarios candidatos
class Candidato(BaseUser):
    
    rut = models.CharField(max_length=12, blank=True, null=True)
    date_of_birth = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    puesto_de_trabajo = models.ForeignKey(PuestoDeTrabajo, on_delete=models.SET_NULL, null=True, blank=True)

    objects = CustomUserManager()
    

# Clase para manejar los usuarios empleadores
class EmpleadorManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        return super().create_user(email, username, password=password, **extra_fields)

    def create_superuser(self, email, username, password=None, **extra_fields):
        return super().create_superuser(email, username, password=password, **extra_fields)

# Usuarios empleadores
class Empleador(BaseUser):
    empresa = models.CharField(max_length=128)
    rut_empresa = models.CharField(max_length=128)
    telefono = models.CharField(max_length=128)
    direccion = models.CharField(max_length=128)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    objects = EmpleadorManager()

# Almacenador de los datos ingresados por los candidatos
class CandidatoPerfil(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    puesto_de_trabajo = models.ForeignKey(PuestoDeTrabajo, null=True, blank=True, on_delete=models.SET_NULL)
    COMPT_CHOICES = (
        ('Base de datos (SQL)', 'Base de datos (SQL)'),
        ('Programacion (Python)', 'Programacion (Python)'),
        ('Programacion (Java)', 'Programacion (Java)'),
        ('Programacion Front End', 'Programacion Front End'),
        ('Programacion Back End', 'Programacion Back End'),
        ('Tecnologias Cloud', 'Tecnologias Cloud'),
    )
    competencia_1 = models.CharField(max_length=100, choices=COMPT_CHOICES, blank=True, null=True)
    competencia_2 = models.CharField(max_length=100, choices=COMPT_CHOICES, blank=True, null=True)
    competencia_3 = models.CharField(max_length=100, choices=COMPT_CHOICES, blank=True, null=True)
    competencia_4 = models.CharField(max_length=100, choices=COMPT_CHOICES, blank=True, null=True)
    competencia_5 = models.CharField(max_length=100, choices=COMPT_CHOICES, blank=True, null=True)
    competencia_6 = models.CharField(max_length=100, choices=COMPT_CHOICES, blank=True, null=True)
    comentarios_extra = models.TextField(blank=True, null=True)
    archivo1 = models.FileField(upload_to='archivos/', blank=True, null=True)
    archivo2 = models.FileField(upload_to='archivos/', blank=True, null=True)
    archivo3 = models.FileField(upload_to='archivos/', blank=True, null=True)
    
    
#Asignacion de puesto de trabajo para candidato
class Asignacion(models.Model):
    candidato = models.ForeignKey(Candidato, on_delete=models.CASCADE)
    puesto_trabajo = models.ForeignKey(PuestoDeTrabajo, on_delete=models.CASCADE)