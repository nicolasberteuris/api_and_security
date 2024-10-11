from django.db import models
from usuarios.models import Usuario
from django.utils import timezone



class Usuario_participacion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    participacion = models.DecimalField(max_digits=16, decimal_places=8, default=0.0)
    saldo_inicial = models.DecimalField(max_digits=16, decimal_places=8, default=0.0)
    participacion_anterior = models.DecimalField(max_digits=16, decimal_places=8, default=0.0)
    fecha = models.DateField()

    def __str__(self):
        return self.nombre_usuario
    

    class Meta:
        db_table = 'wufto_participaciones'
        verbose_name = 'wufto_participaciones'
        verbose_name_plural = 'wufto_participaciones'
        ordering = ['participacion']


class Balances_totales(models.Model):
    moneda = models.CharField(max_length=300, primary_key= True)
    percentage = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.moneda

    class Meta:
        db_table = 'balances_porcentajes'
        verbose_name = 'Balances_porcentajes'
        verbose_name_plural = 'Balances_porcentajes'
        ordering = ['percentage']

class Altcoins_totales(models.Model):
    moneda = models.CharField(max_length=300, primary_key= True)
    percentage_balance = models.DecimalField(max_digits=10, decimal_places=2)
    percentage_profit = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.moneda

    class Meta:
        db_table = 'altcoins_porcentajes'
        verbose_name = 'Altcoins_porcentajes'
        verbose_name_plural = 'Altcoins_porcentajes'
        ordering = ['percentage_balance']

     

class Estrategia_principal_mensual(models.Model):
    moneda = models.CharField(max_length=300, primary_key= True)
    porcentaje_tiempo_invertido = models.DecimalField(max_digits=10, decimal_places=2)
    

    def __str__(self):
        return self.moneda

    class Meta:
        db_table = 'estrategia_principal_mensual'
        verbose_name = 'Estrategia_principal_mensual'
        verbose_name_plural = 'Estrategia_principal_mensual'
        ordering = ['porcentaje_tiempo_invertido']


class Tasas(models.Model):
    fecha_inicio_tasa = models.CharField(max_length=45)
    fecha_fin_tasa = models.CharField(max_length=45)
    tasa = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_tasa = models.CharField(max_length=45)
    


    class Meta:
        db_table = 'tasas'
        verbose_name = 'tasas'
        verbose_name_plural = 'tasas'

class Operacion(models.Model):
    TIPOS_OPERACION = [
        ('INGRESO', 'Ingreso'),
        ('RETIRO', 'Retiro'),
    ]

    tipo = models.CharField(max_length=10, choices=TIPOS_OPERACION)
    fecha = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    moneda = models.CharField(max_length=50)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_inicial = models.DecimalField(max_digits=10, decimal_places=2)
    saldo_actual = models.DecimalField(max_digits=10, decimal_places=2)
    interes = models.DecimalField(max_digits=5, decimal_places=2)
    posicion = models.CharField(max_length=50)
    confirmacion = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.tipo} - {self.fecha} - {self.usuario.username} - {self.moneda} - {self.cantidad}"
    

class Balances_totales_amount_usdt(models.Model):
    symbol = models.CharField(max_length=50)
    wallet = models.CharField(max_length=50)
    amount_usdt = models.FloatField()
    amount_nominal = models.FloatField()
    price = models.FloatField()

    def __str__(self):
        return f"{self.symbol} - {self.wallet}"
    
    class Meta:
        db_table = 'balances_totales'
        verbose_name = 'balances_totales'
        verbose_name_plural = 'balances_totales'
        ordering = ['amount_usdt']


class Notification_api(models.Model):
    mensaje = models.CharField(max_length=500)
    leido = models.BooleanField(default=False)
    fecha = models.CharField(max_length=45)

    def __str__(self):
        return self.mensaje
    
    class Meta:
        db_table = 'notificacion_api'
        verbose_name = 'notificacion_api'
        verbose_name_plural = 'notificacion_api'
        ordering = ['fecha']


class ComprasBull(models.Model):
    symbol = models.CharField(max_length=45)
    total_amount_usdt = models.DecimalField(max_digits=15, decimal_places=2)
    fecha = models.CharField(max_length=45)
    fecha_seg = models.CharField(max_length=45)

    def __str__(self):
        return self.symbol
    
class VentasBull(models.Model):
    symbol = models.CharField(max_length=45)
    total_amount_usdt = models.DecimalField(max_digits=15, decimal_places=2)
    fecha = models.CharField(max_length=45)
    fecha_seg = models.CharField(max_length=45)

    def __str__(self):
        return self.symbol
    
class VentasCierre(models.Model):
    symbol = models.CharField(max_length=45)
    total_amount_usdt = models.DecimalField(max_digits=15, decimal_places=2)
    fecha = models.CharField(max_length=45)
    fecha_seg = models.CharField(max_length=45)

    def __str__(self):
        return self.symbol


class BalanceTotalHistorico(models.Model):
    description = models.CharField(max_length=45)
    amount_usdt = models.FloatField()
    fecha = models.CharField(max_length=45)

    def __str__(self):
        return self.description 
    

class BalancesTotalesHistoricos(models.Model):
    symbol = models.CharField(max_length=45)
    wallet = models.CharField(max_length=45)
    amount_usdt = models.FloatField()
    amount_nominal = models.FloatField()
    fecha = models.CharField(max_length=45)

    def __str__(self):
        return self.symbol 
    


class BaseTrades(models.Model):
    fecha = models.CharField(max_length=45)
    fecha_seg = models.CharField(max_length=45)
    buy_or_sell = models.CharField(max_length=45)
    symbol = models.CharField(max_length=45)
    price = models.FloatField()
    pnl = models.FloatField()
    open_close = models.CharField(max_length=45, null=True, blank=True)
    bad_trade = models.BooleanField(default=False)

    def __str__(self):
        return self.symbol 
    


class IndiceWufto(models.Model):
    symbol = models.CharField(max_length=100)
    porcentaje = models.FloatField()
    type = models.CharField(max_length=100)
    price = models.FloatField()
    amount_nominal = models.FloatField()
    amount_usdt = models.FloatField()
    fecha = models.CharField(max_length=100)


    class Meta:
        db_table = 'indice_wufto'
        verbose_name = 'indice_wufto'
        verbose_name_plural = 'indice_wufto'
        ordering = ['fecha']


    def __str__(self):
        return f"IndiceWufto: {self.symbol}"
    

class Pnl_live(models.Model):
    symbol = models.CharField(max_length=45)
    compras = models.FloatField()
    ventas_bull = models.FloatField()
    ventas_bear = models.FloatField()
    balance = models.FloatField()
    profit_loss_amount = models.FloatField()
    profit_loss_percentage = models.FloatField()


    def __str__(self):
        return self.symbol
    



class SaldosTotales(models.Model):
    fecha = models.CharField(max_length=45, primary_key=True)
    amount_usdt = models.FloatField()

    def __str__(self):
        return f"Fecha: {self.fecha}, Amount USDT: {self.amount_usdt}"

    class Meta:
        db_table = 'saldos_totales'


class SaldosTotales_historico(models.Model):
    fecha = models.CharField(max_length=45, primary_key=True)
    amount_usdt = models.FloatField()

    def __str__(self):
        return f"Fecha: {self.fecha}, Amount USDT: {self.amount_usdt}"

    class Meta:
        db_table = 'saldos_totales_historico'


class PnlAltcoins(models.Model):
    symbol = models.CharField(max_length=45, primary_key=True)
    compras = models.FloatField()
    ventas_bull = models.FloatField()
    ventas_bear = models.FloatField()
    balance = models.FloatField()
    profit_loss_amount = models.FloatField()
    profit_loss_percentage = models.FloatField()

    def __str__(self):
        return f"Symbol: {self.symbol}, Compras: {self.compras}, Ventas Bull: {self.ventas_bull}, Ventas Bear: {self.ventas_bear}, Balance: {self.balance}, Profit Loss Amount: {self.profit_loss_amount}, Profit Loss Percentage: {self.profit_loss_percentage}"

    class Meta:
        db_table = 'pnl_altcoins'


class TasasBull(models.Model):
    date = models.CharField(max_length=45, primary_key=True)
    tasa_acumulada = models.FloatField()
    tasa_mensual = models.FloatField()

    def __str__(self):
        return f"Date: {self.date}, Tasa Acumulada: {self.tasa_acumulada}, Tasa Mensual: {self.tasa_mensual}"

    class Meta:
        db_table = 'tasas_bull'


class TasasBull_reales(models.Model):
    date = models.CharField(max_length=45, primary_key=True)
    tasa_acumulada = models.FloatField()
    tasa_mensual = models.FloatField()

    def __str__(self):
        return f"Date: {self.date}, Tasa Acumulada: {self.tasa_acumulada}, Tasa Mensual: {self.tasa_mensual}"

    class Meta:
        db_table = 'tasas_bull_reales'


class BtcActualBull(models.Model):
    date = models.CharField(primary_key=True, max_length=45)
    price_close = models.FloatField()

    class Meta:
        db_table = 'btc_actual_bull'


class NewDeposits(models.Model):
    id = models.CharField(max_length=45, primary_key=True)
    amount = models.FloatField()
    fecha = models.CharField(max_length=45)
    symbol = models.CharField(max_length=45)

    class Meta:
        db_table = 'new_deposits'


class NewWithdraws(models.Model):
    id = models.CharField(max_length=45, primary_key=True)
    amount = models.FloatField()
    fecha = models.CharField(max_length=45)
    symbol = models.CharField(max_length=45)

    class Meta:
        db_table = 'new_withdraws'



class AuthToken_nico(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    token = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    key = models.CharField(max_length=255)
    secretkey = models.CharField(max_length=255)
    ip = models.CharField(max_length=50)
    encrypted_key = models.CharField(max_length=255)
    clave_secreta_fernet = models.CharField(max_length=255)
    token_jwt = models.TextField()
    ultimo_acceso = models.DateTimeField()
    inicio_sesion = models.DateTimeField()
    user_agent = models.TextField()

    def __str__(self):
        return self.token
    




class AccessAttempt(models.Model):
    username = models.CharField(max_length=150)  # Campo para almacenar el nombre de usuario
    ip_address = models.CharField(max_length=39)  # Campo para almacenar la dirección IP
    blocked = models.BooleanField(default=False)  # Campo para indicar si la IP está bloqueada
    timestamp = models.DateTimeField(auto_now_add=True)  # Campo para almacenar la marca de tiempo del intento de acceso

    def __str__(self):
        return f"Username: {self.username}, IP Address: {self.ip_address}, Blocked: {self.blocked}, Timestamp: {self.timestamp}"
    


class UserIP(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ip_address = models.CharField(max_length=100)
    last_login = models.DateTimeField(null=True)
    validation_token = models.CharField(null=True, max_length=100)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.usuario.username} - {self.ip_address}"


class RateLimit(models.Model):
    ip_address = models.CharField(max_length=45, unique=True)
    request_count = models.IntegerField(default=0)
    last_reset = models.DateTimeField(auto_now_add=True)

    def reset_request_count(self):
        self.request_count = 0
        self.last_reset = timezone.now()
        self.save()



class FlagEmergency(models.Model):
    flag_emergency = models.CharField(max_length=255)
    flag = models.BooleanField(default=False)

    class Meta:
        db_table = 'flag_emergency'



class trade_manual_operaciones(models.Model):
    symbol = models.CharField(max_length=10)
    amount_usdt = models.FloatField()
    type = models.CharField(max_length=20)
    table = models.CharField(max_length=20)

    class Meta:
        db_table = 'trade_manual_operaciones'

    def __str__(self):
        return self.symbol
    


class Usuario_historico_web(models.Model):
    id = models.IntegerField()
    username = models.CharField('Username/Mail', unique=True, max_length=100)
    email = models.EmailField(unique=True, default=username, verbose_name='email')
    nombre = models.CharField(max_length = 200, blank = True, default=None, verbose_name='nombre')
    participacion = models.DecimalField(max_digits=16, decimal_places=8, default=0)
    tipo_usuario = models.IntegerField(default=1)
    direccion = models.CharField(max_length = 100, blank = True, default='', null=True,verbose_name='direccion')
    dni = models.CharField(max_length = 100, blank = True, default='', null=True,verbose_name='dni')
    ciudad = models.CharField(max_length = 250, blank = True, default='', null=True,verbose_name='ciudad')
    telefono = models.CharField(max_length = 100, blank = True, default='', null=True,verbose_name='telefono')
    cobrar_comision = models.BooleanField(default=True)
    enviar_mail = models.BooleanField(default=True)
    ERC20 = models.CharField(max_length = 250, blank = True, default='', null=True,verbose_name='ERC20')
    TCR20 = models.CharField(max_length = 100, blank = True, default='', null=True,verbose_name='TCR20')
    BEP20 = models.CharField(max_length = 100, blank = True, default='', null=True,verbose_name='BEP20')
    is_active = models.BooleanField(default=True) #usuarios que inician sesión
    is_staff = models.BooleanField(default=False) #usuario en el administrador de django
    partner = models.IntegerField(default=0)
    saldo_inicial = models.DecimalField(max_digits=16, decimal_places=8, default=0)
    saldo_actual = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tasa = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tasa_mensual = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tasa_anual = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    ganancia_anual = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    ganancia_de_hoy = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    tasa_hoy = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    rendimiento = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    inversion = models.DecimalField(max_digits=16, decimal_places=2, default=0)
    fecha = models.DateTimeField(auto_now_add=True)
    

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombre','direccion','email']

    class Meta:
        db_table = 'usuarios_historico_web'
        verbose_name = 'usuarios_historico_web'
        verbose_name_plural = 'usuarios_historico_web'
        ordering = ['fecha']
    

    def __str__(self):
        return f'{self.username} {self.id} {self.participacion} {self.username}'
    



class Participaciones(models.Model):
    id_incremental = models.AutoField(primary_key=True)
    id = models.IntegerField()  # Campo autoincremental (INT)
    
    # Campo varchar(45) para fecha, lo puedes cambiar a DateField si es una fecha real
    fecha = models.CharField(max_length=45)  
    
    # Campos float para los valores de participación y saldo
    participacion_antes_de_rev = models.FloatField()  
    participacion_rev = models.FloatField()
    participacion_antes_rev_ajustada_x_decimales = models.FloatField()
    participacion_antes_rev_ajustada_por_negativos = models.FloatField()
    saldo_antes_operacion = models.FloatField()
    saldo_actual = models.FloatField()
    
    # Campo varchar(200) para comentario
    comentario = models.CharField(max_length=200)

    class Meta:
        db_table = 'participaciones'  # Cambia 'nombre_de_tu_tabla' por el nombre real de la tabla

    def __str__(self):
        return f'ID: {self.id}, Fecha: {self.fecha}'
    
    
"""


class Usuario_participacion(models.Model):


    nombre = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    participacion = models.FloatField(null=True, blank=True)
    saldo_inicial = models.FloatField(null=True, blank=True)
    participacion_anterior = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'Usuario_participacion'
        verbose_name = 'Usuario_participacion'
        verbose_name_plural = 'Usuario_participacion'
        ordering = ['participacion']


        """