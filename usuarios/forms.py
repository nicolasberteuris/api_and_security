
"""

from logging import PlaceHolder
from django import forms
from django.contrib.auth.forms import UserCreationForm
from usuarios.models import Categoria_Usuario, Usuario
from django.contrib.auth.forms import AuthenticationForm




class FormularioLogin (AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(FormularioLogin, self).__init__(*args,**kwargs)
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Ingrese nombre de usuario'
        self.fields['password'].widget.attrs['class'] = 'form-control'
        self.fields['password'].widget.attrs['placeholder'] = 'Ingrese contraseña'


class FormularioUsuario (forms.ModelForm):
    #Formulario de registro de un usuario en la base de datos


    
    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña',
            'id': 'password1',
            'required': 'required',
        }
    ))

    password2 = forms.CharField(label = 'Contraseña de confirmación', widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente su contraseña',
            'id': 'password2',
            'required': 'required',
        }
    ))

    class Meta:
        model = Usuario
        fields = ('username', 'nombre', 'direccion', 'email')
        labels = {
                'username': "Username:",
                'nombre': "Nombre del Usuario:",
                'direccion': "dirección:",
                'email': "email",
            }        
        widgets = {
            'username': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Usuario:'
                }
            ),
            'nombre': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'Nombre:'
                }
            ),
            'direccion': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'dirección:'
                }
            ),
            'email': forms.TextInput(
                attrs = {
                    'class': 'form-control',
                    'placeholder': 'email:'
                }
            )
        }

    def clean_password2(self):
        print(self.cleaned_data)
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden')
        return password2
    
    def save(self,commit = True):
        user = super().save(commit = False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class CambiarPasswordForm(forms.Form):
    password1 = forms.CharField(label = 'Contraseña', widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese su nueva contraseña',
            'id': 'password1',
            'required': 'required',
        }
    ))

    password2 = forms.CharField(label = 'Contraseña de confirmación', widget = forms.PasswordInput(
        attrs = {
            'class': 'form-control',
            'placeholder': 'Ingrese nuevamente su nueva contraseña',
            'id': 'password2',
            'required': 'required',
        }
    ))

    def clean_password2(self):
        print(self.cleaned_data)
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError('Contraseñas no coinciden')
        return password2
    

class Categoria_UsuarioForm(forms.ModelForm):
    class Meta:
        model = Categoria_Usuario
        fields = ['name','id']
        labels = {
                'name': "Nombre de la categoría de cliente:",
                'id': "Código de la categoría de cliente:",
            }
        widgets = {
            'name': forms.TextInput(
                attrs = {
                    'class':'form-control',
                    'placeholder':'Ingrese el nombre de la categoría de Cliente',
                    'id':'name'
                }
            ),
        }


"""