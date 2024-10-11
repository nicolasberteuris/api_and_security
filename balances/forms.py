
import imp
from django import forms
from .models import *

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class Balances_totalesForm(forms.ModelForm):
    class Meta:
        model = Balances_totales
        fields = ['moneda', 'percentage']
        labels = {
                'moneda': "Moneda:",
                'percentage': "Participacion sobre total:",
            }
        
class Altcoins_totalesForm(forms.ModelForm):
    class Meta:
        model = Altcoins_totales
        fields = ['moneda', 'percentage_balance', 'percentage_profit']
        labels = {
                'moneda': "Moneda:",
                'percentage_balance': "Porcentaje del Balance sobre el total:",
                'percentage_profit': "Porcentaje del rendimiento:"
            }
        
class Estrategia_principal_mensualForm(forms.ModelForm):
    class Meta:
        model = Estrategia_principal_mensual
        fields = ['moneda', 'porcentaje_tiempo_invertido']
        labels = {
                'moneda': "Moneda:",
                'porcentaje_tiempo_invertido': "Porcentaje del Tiempo invertido mensual:",
            }

class TasasForm(forms.ModelForm):
    class Meta:
        model = Tasas
        fields = ['fecha_inicio_tasa', 'fecha_fin_tasa', 'tasa','tipo_tasa']
        labels = {
                'fecha_inicio_tasa': "Desde:",
                'fecha_fin_tasa': "Hasta",
                'tasa': "Tasa",
                'tipo_tasa': "Tipo De Tasa"
            }
        

class OperacionForm(forms.ModelForm):
    class Meta:
        model = Operacion
        fields = ['tipo', 'usuario', 'moneda', 'cantidad', 'saldo_inicial', 'saldo_actual', 'interes', 'posicion', 'confirmacion']
        labels = {
            'tipo': 'Tipo de Operación',
            'fecha': 'Fecha',
            'usuario': 'Usuario',
            'moneda': 'Moneda',
            'cantidad': 'Cantidad',
            'saldo_inicial': 'Saldo Inicial',
            'saldo_actual': 'Saldo Actual',
            'interes': 'Interés',
            'posicion': 'Posición',
            'confirmacion': 'Confirmación',
        }


class IndiceWuftoForm(forms.ModelForm):
    class Meta:
        model = IndiceWufto
        fields = ['symbol', 'porcentaje', 'type', 'price', 'amount_usdt', 'fecha','amount_nominales']
