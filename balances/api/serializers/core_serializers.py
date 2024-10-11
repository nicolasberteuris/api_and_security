
from rest_framework import serializers
from decimal import Decimal

from balances.models import *

class Usuario_participacionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Usuario_participacion
        fields = '__all__'


class Pnl_liveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Pnl_live
        fields = '__all__'

class TasasSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tasas
        fields = '__all__'

class Altcoins_totalesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Altcoins_totales
        fields = '__all__'


class Balances_totalesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Balances_totales
        fields = '__all__'


class OperacionSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Operacion
        fields = '__all__'


class Balances_totales_amount_usdtSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Balances_totales_amount_usdt
        fields = '__all__'


class Notification_apiSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Notification_api
        fields = '__all__'


class ComprasBullSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = ComprasBull
        fields = '__all__'

class VentasBullSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = VentasBull
        fields = '__all__'

class VentasCierreSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = VentasCierre
        fields = '__all__'

class BalancesTotalesHistoricosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BalancesTotalesHistoricos
        fields = '__all__'

class BalanceTotalHistoricoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BalanceTotalHistorico
        fields = '__all__'


class BaseTradesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BaseTrades
        fields = '__all__'


class IndiceWuftoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = IndiceWufto
        fields = '__all__'
        


class SaldosTotalesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SaldosTotales
        fields = '__all__'


class SaldosTotales_historicoSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = SaldosTotales_historico
        fields = '__all__'

class PnlAltcoinsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PnlAltcoins
        fields = '__all__'

class TasasBullSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TasasBull
        fields = '__all__'

class TasasBull_realesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TasasBull_reales
        fields = '__all__'

class BtcActualBullSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = BtcActualBull
        fields = '__all__'

class NewWithdrawsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewWithdraws
        fields = '__all__'

class NewDepositsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = NewDeposits
        fields = '__all__'


class FlagEmergencySerializer(serializers.ModelSerializer):
    class Meta:
        model = FlagEmergency
        fields = ['flag_emergency', 'flag']


class trade_manual_operacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = trade_manual_operaciones
        fields = '__all__'



class ParticipacionesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participaciones
        fields = '__all__'

class Usuario_historico_webSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario_historico_web
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for key, value in representation.items():
            if isinstance(value, Decimal):
                representation[key] = float(value)  # Convertir Decimal a float
        return representation
