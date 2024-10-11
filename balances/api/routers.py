from rest_framework.routers import DefaultRouter #Depende de la ruta el viewset que usemos
from balances.api.views.core_views import *
from django.urls import path
#from dashboard.api.views.general_views import *

router = DefaultRouter()

router.register(r'balances', Usuario_participacionViewSet, basename='balances'),
router.register(r'Pnl_live', Pnl_liveViewSet, basename='Pnl_live'),
router.register(r'altcoins_totales', Altcoins_totalesViewSet, basename='altcoins_totales')
router.register(r'Balances_totales', Balances_totalesViewSet, basename='Balances_totales')
router.register(r'Tasas', TasasViewSet, basename='Tasas')
router.register(r'Operacion', OperacionViewSet, basename='Operacion')
router.register(r'balances_totales_amount_usdt', Balances_totales_amount_usdtViewSet, basename='balances_totales_amount_usdt')
router.register(r'notification_api', Notification_apiViewSet, basename='notification_api')
#router.register(r'balances/notification_api/<int:pk>/update_leido', Notification_apiViewSet, basename='update_leido')
router.register(r'ComprasBull', ComprasBullViewSet, basename='ComprasBull')
router.register(r'VentasCierre', VentasCierreViewSet, basename='VentasCierre')
router.register(r'VentasBull', VentasBullViewSet, basename='VentasBull')
router.register(r'BalancesTotalesHistoricos', BalancesTotalesHistoricosViewSet, basename='BalancesTotalesHistoricos')
router.register(r'BalanceTotalHistorico', BalanceTotalHistoricoViewSet, basename='BalanceTotalHistorico')
router.register(r'BaseTrades', BaseTradesViewSet, basename='BaseTrades')
router.register(r'IndiceWufto', IndiceWuftoViewSet, basename='IndiceWufto')
router.register(r'SaldosTotales', SaldosTotalesViewSet, basename='SaldosTotales')
router.register(r'SaldosTotales_historico', SaldosTotales_historicoViewSet, basename='SaldosTotales_historico')
router.register(r'PnlAltcoins', PnlAltcoinsViewSet, basename='PnlAltcoins')
router.register(r'TasasBull', TasasBullViewSet, basename='TasasBull')
router.register(r'TasasBull_reales', TasasBull_realesViewSet, basename='TasasBull_reales')
router.register(r'BtcActualBull', BtcActualBullViewSet, basename='BtcActualBull')
router.register(r'NewWithdraws', NewWithdrawsViewSet, basename='NewWithdraws')
router.register(r'NewDeposits', NewDepositsViewSet, basename='NewDeposits')
router.register(r'FlagEmergency', FlagEmergencyViewSet, basename='FlagEmergency')
router.register(r'trade_manual_operaciones', trade_manual_operacionesViewSet, basename='trade_manual_operaciones')
router.register(r'Participaciones', ParticipacionesViewSet, basename='Participaciones')
router.register(r'Usuario_historico_web', Usuario_historico_webViewSet, basename='Usuario_historico_web')


urlpatterns = [
    # Otras rutas de la aplicación...
    path('notification_api/<int:pk>/update_leido/', Notification_apiViewSet.as_view({'post': 'update_leido'}), name='update_leido'),
    path('ComprasBull/filter-by-date/', ComprasBullViewSet.as_view({'get': 'list'}), name='ComprasBull-filter-by-date'),
    path('FlagEmergencyApi/', FlagEmergencyAPIView.as_view(), name='FlagEmergencyApi'),
]


urlpatterns += router.urls
