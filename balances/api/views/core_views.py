from rest_framework import status
from rest_framework import viewsets,generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser, MultiPartParser
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from balances.models import *
from usuarios.models import *
import time
import pymysql
from rest_framework.decorators import action
from datetime import datetime


from balances.api.serializers.core_serializers import *


import os
from dotenv import load_dotenv

# Carga las variables de entorno
load_dotenv()

# Accede a las credenciales
db_user = os.getenv('DATABASE_USER')
db_password = os.getenv('LOCAL_MYSQL_PASSWORD')
request_user = os.getenv('REQUEST_USER')
request_password = os.getenv('REQUEST_PASSWORD')
request_url_login = os.getenv('REQUEST_URL_LOGIN')
request_url = os.getenv('REQUEST_URL')






class Usuario_participacionViewSet(viewsets.ModelViewSet):
    queryset = Usuario_participacion.objects.all()
    serializer_class = Usuario_participacionSerializer

class Pnl_liveViewSet(viewsets.ModelViewSet):
    queryset = Pnl_live.objects.all()
    serializer_class = Pnl_liveSerializer


class Altcoins_totalesViewSet(viewsets.ModelViewSet):
    queryset = Altcoins_totales.objects.all()
    serializer_class = Altcoins_totalesSerializer

class Balances_totalesViewSet(viewsets.ModelViewSet):
    queryset = Balances_totales.objects.all()
    serializer_class = Balances_totalesSerializer


class TasasViewSet(viewsets.ModelViewSet):
    queryset = Tasas.objects.all()
    serializer_class = TasasSerializer

class OperacionViewSet(viewsets.ModelViewSet):
    queryset = Operacion.objects.all()
    serializer_class = OperacionSerializer

class Balances_totales_amount_usdtViewSet(viewsets.ModelViewSet):
    queryset = Balances_totales_amount_usdt.objects.all()
    serializer_class = Balances_totales_amount_usdtSerializer
    #lookup_field = 'id'  # El campo que se utilizará para buscar clientes (puede ser 'id', 'nombre', etc.)

"""
class Notification_apiViewSet(viewsets.ModelViewSet):
    queryset = Notification_api.objects.all()
    serializer_class = Notification_apiSerializer
    #lookup_field = 'id'  # El campo que se utilizará para buscar clientes (puede ser 'id', 'nombre', etc.)
    """


class Notification_apiViewSet(viewsets.ModelViewSet):
    serializer_class = Notification_apiSerializer

    def get_queryset(self):
        if self.action == 'list':
            return Notification_api.objects.filter(leido=False)
        return Notification_api.objects.all()
    
    

    def update_leido(self, request, pk=None):
        print("voy por aca")
        notification = self.get_object()
        notification.leido = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return self.update_leido(request, *args, **kwargs)
        
    
    def create(self, request, *args, **kwargs):
        print("voy por aca 3")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        print("voy por aca 2")
        notification = self.get_object()
        notification.leido = True
        notification.save()
        serializer = self.get_serializer(notification)
        return Response(serializer.data, status=status.HTTP_200_OK)
        


class ComprasBullViewSet(viewsets.ViewSet):
    serializer_class = ComprasBullSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = ComprasBull.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = ComprasBull.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)


class VentasBullViewSet(viewsets.ViewSet):
    serializer_class = VentasBullSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = VentasBull.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = VentasBull.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)


class VentasCierreViewSet(viewsets.ViewSet):
    serializer_class = VentasCierreSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = VentasCierre.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = VentasCierre.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
            
class BalancesTotalesHistoricosViewSet(viewsets.ViewSet):
    serializer_class = BalancesTotalesHistoricosSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = BalancesTotalesHistoricos.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = BalancesTotalesHistoricos.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
            

class BalanceTotalHistoricoViewSet(viewsets.ViewSet):
    serializer_class = BalanceTotalHistoricoSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = BalanceTotalHistorico.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = BalanceTotalHistorico.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
    
    

class BaseTradesViewSet(viewsets.ViewSet):
    serializer_class = BaseTradesSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = BaseTrades.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = BaseTrades.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)


class IndiceWuftoViewSet(viewsets.ViewSet):
    serializer_class = IndiceWuftoSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = IndiceWufto.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = IndiceWufto.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
            

class SaldosTotalesViewSet(viewsets.ViewSet):
    serializer_class = SaldosTotalesSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = SaldosTotales.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = SaldosTotales.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

class SaldosTotales_historicoViewSet(viewsets.ViewSet):
    serializer_class = SaldosTotales_historicoSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = SaldosTotales_historico.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = SaldosTotales_historico.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
            
class PnlAltcoinsViewSet(viewsets.ViewSet):
    serializer_class = PnlAltcoinsSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = PnlAltcoins.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = PnlAltcoins.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
            
class TasasBullViewSet(viewsets.ViewSet):
    serializer_class = TasasBullSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = TasasBull.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = TasasBull.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
            
class TasasBull_realesViewSet(viewsets.ViewSet):
    serializer_class = TasasBull_realesSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = TasasBull_reales.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = TasasBull_reales.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
            

class BtcActualBullViewSet(viewsets.ViewSet):
    serializer_class = BtcActualBullSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = BtcActualBull.objects.filter(date__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = BtcActualBull.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
            

class NewWithdrawsViewSet(viewsets.ViewSet):
    serializer_class = NewWithdrawsSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = NewWithdraws.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = NewWithdraws.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
            

class NewDepositsViewSet(viewsets.ViewSet):
    serializer_class = NewDepositsSerializer
    
    def list(self, request):
        # Obtener los parámetros de fecha de inicio y fecha de fin de la solicitud
        fecha_inicio_str = request.query_params.get('fecha_inicio', None)
        fecha_fin_str = request.query_params.get('fecha_fin', None)

        if fecha_inicio_str and fecha_fin_str:
            try:
                # Convertir las cadenas de fecha a objetos de fecha
                fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                # Filtrar objetos por rango de fechas
                queryset = NewDeposits.objects.filter(fecha__range=(fecha_inicio, fecha_fin))
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                # Si no se proporciona una fecha, devolver todos los objetos
                queryset = NewDeposits.objects.all()
                serializer = self.serializer_class(queryset, many=True)
                return Response(serializer.data)
            except ValueError:
                return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
            


class FlagEmergencyViewSet(viewsets.ModelViewSet):
    print("entro por ModelViewSet !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")

    try:

        queryset = FlagEmergency.objects.all()
        serializer_class = FlagEmergencySerializer

        def create(self, request, *args, **kwargs):
            print("entro por ModelViewSet en create!!!!!!!create!!!!!!!!!!!!!!!!!create!!!!!create ")
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        def perform_create(self, serializer):
            serializer.save()

        def list(self, request, *args, **kwargs):
            print("entro por ModelViewSet en list!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")

            print(request.data)
            print(request)
            queryset = self.filter_queryset(self.get_queryset())
            print(queryset)


            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            print(serializer.data)
            return Response(serializer.data)
        
        def update(self, request, *args, **kwargs):
            print("entro por ModelViewSet en update!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        def perform_update(self, serializer):
            serializer.save()

        def partial_update(self, request, *args, **kwargs):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)

    except Exception as e:
        print(f"se genero un error en ModelViewSet", e)


class trade_manual_operacionesViewSet(viewsets.ModelViewSet):
    print("entro por ModelViewSet !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")

    try:

        queryset = trade_manual_operaciones.objects.all()
        serializer_class = trade_manual_operacionesSerializer

        def create(self, request, *args, **kwargs):
            print("entro por ModelViewSet en create!!!!!!!create!!!!!!!!!!!!!!!!!create!!!!!create ")
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        def perform_create(self, serializer):
            serializer.save()

        def list(self, request, *args, **kwargs):
            print("entro por ModelViewSet en list!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")

            print(request.data)
            print(request)
            queryset = self.filter_queryset(self.get_queryset())
            print(queryset)


            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)

            serializer = self.get_serializer(queryset, many=True)
            print(serializer.data)
            return Response(serializer.data)
        
        def update(self, request, *args, **kwargs):
            print("entro por ModelViewSet en update!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        def perform_update(self, serializer):
            serializer.save()

        def partial_update(self, request, *args, **kwargs):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)

    except Exception as e:
        print(f"se genero un error en ModelViewSet", e)


class FlagEmergencyAPIView(APIView):
    print("entro por APIView ")
    try:

        def post(self, request):
            print("estoy en el post")
            serializer = FlagEmergency(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    except Exception as e:
        print(f"se genero un error en apiview", e)





class ParticipacionesViewSet(viewsets.ModelViewSet):
    print("entro por ModelViewSet !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")

    try:

        queryset = Participaciones.objects.all()
        serializer_class = ParticipacionesSerializer

        def create(self, request, *args, **kwargs):
            print("Participaciones entro por ModelViewSet en create!!!!!!!create!!!!!!!!!!!!!!!!!create!!!!!create ")
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        def perform_create(self, serializer):
            serializer.save()

        def list(self, request, *args, **kwargs):
            print("Participaciones entro por ModelViewSet en list!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")

            fecha_inicio_str = request.query_params.get('fecha_inicio', None)
            fecha_fin_str = request.query_params.get('fecha_fin', None)
            comentario = request.query_params.get('comentario', None)

            if fecha_inicio_str and fecha_fin_str:
                try:
                    # Convertir las cadenas de fecha a objetos de fecha
                    fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').date()
                    fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').date()
                    # Filtrar objetos por rango de fechas
                    queryset = Participaciones.objects.filter(fecha__range=(fecha_inicio, fecha_fin))

                    if comentario:
                        queryset = queryset.filter(comentario__icontains=comentario)  # Búsqueda parcial e insensible a mayúsculas/minúsculas
                    
                    serializer = self.serializer_class(queryset, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                except ValueError:
                    return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                try:
                    # Si no se proporciona una fecha, devolver todos los objetos
                    queryset = Participaciones.objects.all()

                    if comentario:
                        queryset = queryset.filter(comentario__icontains=comentario)  # Búsqueda parcial e insensible a mayúsculas/minúsculas
            
                    serializer = self.serializer_class(queryset, many=True)
                    return Response(serializer.data)
                except ValueError:
                    return Response({'error': 'Formato de fecha no válido. Utilice el formato YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)
            
        
        def update(self, request, *args, **kwargs):
            print("Participaciones entro por ModelViewSet en update!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        def perform_update(self, serializer):
            serializer.save()

        def partial_update(self, request, *args, **kwargs):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)

    except Exception as e:
        print(f"se genero un error en ModelViewSet", e)



 
class Usuario_historico_webViewSet(viewsets.ModelViewSet):
    print("entro por Usuario_historico_webViewSet ModelViewSet !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!1")

    try:

        queryset = Usuario_historico_web.objects.all()
        serializer_class = Usuario_historico_webSerializer

        def create(self, request, *args, **kwargs):
            print("Usuario_historico_webViewSet entro por ModelViewSet en create!!!!!!!create!!!!!!!!!!!!!!!!!create!!!!!create ")
            serializer = self.get_serializer(data=request.data, many=isinstance(request.data, list))
            serializer.is_valid(raise_exception=True)
            if not serializer.is_valid():
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        def perform_create(self, serializer):
            serializer.save()

        def list(self, request, *args, **kwargs):
            print("Usuario_historico_webViewSet entro por ModelViewSet en list!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")

            try:
                queryset = Usuario_historico_web.objects.all()
                print("queryset",queryset)
                serializer = self.serializer_class(queryset, many=True)
                print("serializer",serializer)
                return Response(serializer.data)
            except ValueError:
                    return Response({'error': 'Usuario_historico_webViewSet'}, status=status.HTTP_400_BAD_REQUEST)

        
        def update(self, request, *args, **kwargs):
            print("Usuario_historico_webViewSet entro por ModelViewSet en update!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ")
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)

        def perform_update(self, serializer):
            serializer.save()

        def partial_update(self, request, *args, **kwargs):
            kwargs['partial'] = True
            return self.update(request, *args, **kwargs)

    except Exception as e:
        print(f"se genero un error en ModelViewSet", e)

def search(query:str, variables:list=None):
        results = False
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root', 
                password = db_password,
                db='wufto'
                )
            cur = conn.cursor(pymysql.cursors.DictCursor)
            cur.execute(query, variables)
            results = cur.fetchall()
            conn.close()
            #print(results)
            return results
        except Exception as e:
            conn.close()
            print('Error retrieving MySQL database record.')
            print(e, True)
            
        return False


def query_(query:str):
        try:
            conn = pymysql.connect(
                host='localhost',
                user='root', 
                password = db_password,
                db='wufto_balances'
                )

            cur = conn.cursor()
            results = cur.execute(query)
            conn.commit()
            conn.close()
            return results

        except Exception as e:
            conn.close()
            print(e)
        
        return False