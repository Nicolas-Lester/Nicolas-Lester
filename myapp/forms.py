from django import forms
from .models import Candidato
from .models import CandidatoPerfil
from .models import Empleador
from .models import Asignacion



#formularios candidatos
class CandidatoUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)
    rut = forms.CharField(label='RUT', max_length=12, required=False)  

    class Meta:
        model = Candidato
        fields = ('email', 'username', 'rut')  

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super(CandidatoUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


#formularios empleadores

class EmpleadorRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = Empleador
        fields = ('email', 'username', 'empresa', 'rut_empresa', 'telefono', 'direccion')  # Agrega los campos personalizados aquí

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return password2

    def save(self, commit=True):
        user = super(EmpleadorRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    
class EmpleadorLoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        try:
            user = Empleador.objects.get(email=email)
        except Empleador.DoesNotExist:
            user = None

        if user is None or not user.check_password(password):
            raise forms.ValidationError("Credenciales incorrectas. Por favor, inténtalo de nuevo.")

        return cleaned_data
    
    

# Formulario para el candidatoperfil
class CandidatoForm(forms.ModelForm): 
    class Meta:
        model = CandidatoPerfil
        fields = ['competencia_1', 'competencia_2', 'competencia_3', 'competencia_4', 'competencia_5', 'competencia_6', 'comentarios_extra', 'archivo1', 'archivo2', 'archivo3']
        
#selecciona un candidato dentro del formulario
class SeleccionCandidatoForm(forms.Form):
    candidato = forms.ModelChoiceField(queryset=Candidato.objects.all(), empty_label="Seleccione un candidato")
    

#clase que permite los form de ingreso de email y nueva contraseña 
class PasswordResetForm(forms.Form):
    email = forms.EmailField(label='Correo electrónico')
    new_password = forms.CharField(widget=forms.PasswordInput, label='Nueva contraseña')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Confirmar nueva contraseña')

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden. Por favor, inténtalo de nuevo.")


# Puesto de trabajo
class AsignacionPuestoForm(forms.ModelForm):
    candidato_seleccionado = forms.BooleanField(widget=forms.HiddenInput(), required=False)
    
    class Meta:
        model = Asignacion
        fields = ['candidato', 'puesto_trabajo']
        
        
        
