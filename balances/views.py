from email import message
from pyexpat import features
from urllib import response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from numpy import product
import time, datetime
from datetime import datetime, timedelta

from django.shortcuts import redirect, render
from balances.forms import Balances_totalesForm, Altcoins_totalesForm,  Estrategia_principal_mensualForm
from .models import Balances_totales, Altcoins_totales,  Tasas,Estrategia_principal_mensual
from ast import Try
from http import client
from multiprocessing import context
from pydoc import cli
from django.shortcuts import redirect, render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.urls import reverse_lazy
from django.views import View, generic
from django.views.generic import TemplateView,ListView, UpdateView, CreateView, DeleteView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy 
from django.http import HttpResponse
from requests import request
from django.core.paginator import Paginator
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
#from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.core.exceptions import ValidationError
from django import forms
from usuarios.models import Categoria_Usuario, Usuario
from django.contrib.auth.decorators import permission_required
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pymysql
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .forms import LoginForm
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login



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


#Clase para inciar#
"""
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        })
    else:
        return Response({'error': 'Invalid credentials'})
        
    

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        # Redirige a la URL deseada después del login exitoso
        return redirect('dashboard_clientes')
    else:
        return render(request, 'login.html', {'error': 'Invalid credentials'})
        """
    

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({'access_token': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@authentication_classes(['rest_framework_simplejwt.authentication.JWTAuthentication'])
@permission_classes([IsAuthenticated])
def ver_balances_totales(request):
        #Balances totales grafico de Datatable 
        try:
            cartera_total = search("SELECT `amount_usdt` FROM `balances_totales` WHERE `symbol`='total' ",)
            #print(cartera_total)
            if cartera_total == ():
                time.sleep(15)
                cartera_total = search("SELECT `amount_usdt` FROM `balances_totales` WHERE `symbol`='total' ",)
        except:
            time.sleep(15)
            try:
                cartera_total = search("SELECT `amount_usdt` FROM `balances_totales` WHERE `symbol`='total' ",)
                #print(cartera_total)
                if cartera_total == ():
                    time.sleep(15)
                    cartera_total = search("SELECT `amount_usdt` FROM `balances_totales` WHERE `symbol`='total' ",)
            except:
                time.sleep(15)
                cartera_total = search("SELECT `amount_usdt` FROM `balances_totales` WHERE `symbol`='total' ",)
        cartera_total = cartera_total[0]['amount_usdt']
        cartera_total_dt = float(cartera_total)
        try:    
            balances_totales_dt = search("SELECT `symbol`, SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales` WHERE NOT `symbol`='total' GROUP BY `symbol`",)
        except:
            time.sleep(5)
            balances_totales_dt = search("SELECT `symbol`, SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales` WHERE NOT `symbol`='total' GROUP BY `symbol`",)
        query = f"TRUNCATE TABLE wufto.balances_porcentajes;"
        ret = query_(query)
        for balances_total in balances_totales_dt:
             if balances_total['symbol'] == "USDT":
                moneda=balances_total['symbol']
             else:
                moneda=balances_total['symbol'][:-4]
             amount_usdt=float(balances_total['amount_usdt'])
             percentage= (amount_usdt * float(100)) / cartera_total_dt
             percentage = truncate(percentage, 2)
             percentage = float(percentage)
             #print(percentage)
             balances_porcentajes=Balances_totales.objects.create(
                    moneda=moneda,
                    percentage=percentage,
                )


        #Balances totales grafico de Altcoins 
        try:
            cartera_total = search("SELECT SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales` WHERE NOT `symbol`='total' AND NOT `symbol`='BTC' AND NOT `symbol`='USDT' AND NOT `symbol`='EUR' AND NOT `symbol`='ETH' ",)
            if cartera_total == ():
                time.sleep(5)
                cartera_total = search("SELECT SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales` WHERE NOT `symbol`='total' AND NOT `symbol`='BTC' AND NOT `symbol`='USDT' AND NOT `symbol`='EUR' AND NOT `symbol`='ETH' ",)
        except:
            time.sleep(5)
            cartera_total = search("SELECT SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales` WHERE NOT `symbol`='total' AND NOT `symbol`='BTC' AND NOT `symbol`='USDT' AND NOT `symbol`='EUR' AND NOT `symbol`='ETH' ",)
        cartera_total = cartera_total[0]['amount_usdt']
        #(cartera_total)
        if cartera_total != None:
            cartera_total = float(cartera_total)

            try:
                balances_totales = search("SELECT `symbol`, SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales` GROUP BY `symbol`",)
                if cartera_total == ():
                    time.sleep(5)
                    balances_totales = search("SELECT `symbol`, SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales` GROUP BY `symbol`",)
            except:
                time.sleep(5)
                balances_totales = search("SELECT `symbol`, SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales` GROUP BY `symbol`",)
            balances_totales_=[]
            for balances_total in balances_totales:
                moneda=balances_total['symbol']
                amount_usdt=float(balances_total['amount_usdt'])
                #print(amount_usdt)
                percentage= (amount_usdt * float(100)) / cartera_total
                percentage = truncate(percentage, 2)
                percentage = float(percentage)
                if moneda != 'total' and moneda !='ETHUSDT' and moneda !='USDT' and moneda !='EUR' and moneda !='BTCUSDT':
                    balances_totales_.append({
                        'symbol':moneda[:-4],
                        '%':percentage
                    })

            colores = ['#FFF10D' ]
            title='Participacion de Altcoins sobre Total de Altcoins'
            bal = pd.DataFrame(balances_totales_, columns=['symbol','%']).set_index(['symbol']).sort_values(by='%', ascending=False).head(20)
            bal.plot(kind = 'barh', align='center', title=title, xlabel='', ylabel=' ', color=['#DBBF33'])
            #print(bal)  

            plt.savefig('static/altcoins_totales.png')
            #plt.close()
            plt.clf()
        else:
            colores = ['#FFF10D' ]
            title='Participacion de Altcoins sobre Total de Altcoins'
            balances_totales_=[]
            balances_totales_.append({
                        'symbol':'',
                        '%':0
                    })
            bal = pd.DataFrame(balances_totales_, columns=['symbol','%']).set_index(['symbol']).sort_values(by='%', ascending=True)
            bal.plot(kind = 'barh', align='center', title=title, xlabel='', ylabel=' ', color=['#DBBF33'])
            #print(bal)  

            plt.savefig('static/altcoins_totales.png')
            #plt.close()
            plt.clf()


        
        #Balances totales grafico de Balances totales
        try:
            cartera_total = search("SELECT `amount_usdt` FROM `balances_totales` WHERE `symbol`='total' ",)
        except:
            time.sleep(5)
            cartera_total = search("SELECT `amount_usdt` FROM `balances_totales` WHERE `symbol`='total' ",)
        cartera_total = cartera_total[0]['amount_usdt']
        cartera_total = float(cartera_total)
        try:
            altcoins_total = search("SELECT SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales` WHERE NOT `symbol`='total' AND NOT `symbol`='BTCUSDT' AND NOT `symbol`='USDT' AND NOT `symbol`='EURUSDT' AND NOT `symbol`='ETHUSDT'",)
            #print(altcoins_total)
            #print(altcoins_total[0]['amount_usdt'])
            if altcoins_total[0]['amount_usdt'] == None:
                    altcoins_total = ({'amount_usdt': 0.0})
                    altcoins_total = [altcoins_total]
                    #print(altcoins_total)
                    
        except:
            time.sleep(5)
            altcoins_total = search("SELECT SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales` WHERE NOT `symbol`='total' AND NOT `symbol`='BTCUSDT' AND NOT `symbol`='USDT' AND NOT `symbol`='EURUSDT' AND NOT `symbol`='ETHUSDT'",)
        altcoins_total = altcoins_total[0]['amount_usdt']
        #print(altcoins_total)
        altcoins_percentage = (altcoins_total * float(100)) / cartera_total
        altcoins_percentage = truncate(altcoins_percentage, 2)
        altcoins_percentage = float(altcoins_percentage)
        balances_totales__=[]
        if altcoins_percentage >= float(1):
            balances_totales__.append({
                        'symbol':'ALTCOINS',
                        'percentage':altcoins_percentage
                    })
        try:
            principal_total = search("SELECT `symbol`, SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales` WHERE `symbol`='BTCUSDT' OR `symbol`='USDT' OR `symbol`='EURUSDT' OR `symbol`='ETHUSDT' GROUP BY `symbol`",)
        except:
            time.sleep(5)
            principal_total = search("SELECT `symbol`, SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales` WHERE `symbol`='BTCUSDT' OR `symbol`='USDT' OR `symbol`='EURUSDT' OR `symbol`='ETHUSDT' GROUP BY `symbol`",)
        for balance_total in principal_total:
             amount_usdt=float(balance_total['amount_usdt'])
             #print(amount_usdt)
             principal_percentage= (amount_usdt * float(100)) / cartera_total
             principal_percentage = truncate(principal_percentage, 2)
             principal_percentage = float(principal_percentage)
             #print(principal_percentage)
             if principal_percentage >= float(1):
                moneda=balance_total['symbol']
                balances_totales__.append({
                        'symbol':moneda,
                        'percentage':principal_percentage
                    })
        #print(balances_totales__)

        #print(balances_totales__)
        bal_ = pd.DataFrame(balances_totales__, columns=['symbol','percentage']).set_index(['symbol'])
        bak__ = bal_.groupby('symbol')['percentage'].sum()
        #a_list = list(range(len(bal_['moneda'])-1))
        a_list = bak__.describe()
        count = int(a_list['count'])
        a_list = list(range(count-1))
        explode = [0.1]
        #print("explode")
        for lis in a_list:
            #print(a_list)
            element = 0.1
            explode.append(element)
            #print(explode)
        colores = ['#DBBF33', '#DBBF60', '#FFD70D', '#FFD97D']
        #print(bal_)
        bal_.plot(kind='pie', subplots=True, explode=explode,  autopct='%.2f%%', ylabel=' ', title='Composicion del Fondo Total', colors = colores)
        #print(bal_)
        
        plt.savefig('static/balances_totales.png')
        #plt.close()
        plt.clf()
        # % tiempo en un mes de estrategia principal invertida 

        #identifico en que mes estoy 
        time_now = time.time()
        fecha = datetime.utcfromtimestamp(int(time_now)).strftime('%Y-%m-%d')
        ano = fecha[0:4]
        mes = fecha[5:7]
        dias = fecha[8:10]  
        start_time = str(ano) + '-' + str(mes) + '-'
        fechas_dias = ['01', '02', '03', '04', '05', '06','07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19','20', '21', '22', '23', '24', '25', '26', '27', '28', '29','30', '31']
        try:
                dias_a_promediar = search("SELECT COUNT(`fecha`) as 'fecha' FROM `balances_totales_historicos` GROUP BY `fecha`")
                dias_a_promediar = len(dias_a_promediar)

        except:
                 time.sleep(2)
                 try:
                     dias_a_promediar = search("SELECT COUNT(`fecha`) as 'fecha' FROM `balances_totales_historicos` GROUP BY `fecha`")
                     dias_a_promediar = len(dias_a_promediar)
                 except:
                    pass

        porcentajes_diarios = []
        #print(dias_a_promediar)
        for fecha in fechas_dias:
            fecha_ = str(start_time) + str(fecha)
            try:
                cartera_total_estartegia_principal_total = search("SELECT SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales_historicos` WHERE `symbol`='BTC' AND `fecha` = %s OR `symbol`='USDT' AND `fecha` = %s OR `symbol`='EUR' AND `fecha` = %s OR `symbol`='ETH' AND `fecha` = %s ",[fecha_, fecha_, fecha_, fecha_])
                cartera_total_estartegia_principal_total = cartera_total_estartegia_principal_total[0]['amount_usdt']
            except:
                 time.sleep(2)
                 try:
                     cartera_total_estartegia_principal_total = search("SELECT SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales_historicos` WHERE `symbol`='BTC' AND `fecha` = %s OR `symbol`='USDT' AND `fecha` = %s OR `symbol`='EUR' AND `fecha` = %s OR `symbol`='ETH' AND `fecha` = %s ",[fecha_, fecha_, fecha_, fecha_])
                     cartera_total_estartegia_principal_total = cartera_total_estartegia_principal_total[0]['amount_usdt']
                 except:
                    pass
            try:
                cartera_total_estartegia_principal = search("SELECT `symbol`, SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales_historicos` WHERE `symbol`='BTC' AND `fecha` = %s OR `symbol`='USDT' AND `fecha` = %s OR `symbol`='EUR' AND `fecha` = %s OR `symbol`='ETH' AND `fecha` = %s GROUP BY `symbol` ",[fecha_, fecha_, fecha_, fecha_])
            except:
                 time.sleep(2)
                 try:
                     cartera_total_estartegia_principal = search("SELECT `symbol`, SUM(`amount_usdt`) as `amount_usdt` FROM `balances_totales_historicos` WHERE `symbol`='BTC' AND `fecha` = %s OR `symbol`='USDT' AND `fecha` = %s OR `symbol`='EUR' AND `fecha` = %s OR `symbol`='ETH' AND `fecha` = %s GROUP BY `symbol` ",[fecha_, fecha_, fecha_, fecha_])
                 except:
                    pass
            for moneda_ in cartera_total_estartegia_principal:
                try:
                    moneda = moneda_['symbol']
                    amount_usdt = float(moneda_['amount_usdt'])
                    percentage_principal = amount_usdt * float(100) / float(cartera_total_estartegia_principal_total)
                    percentage_principal_dias = percentage_principal / int(dias_a_promediar) 
                    porcentajes_diarios.append({
                            'symbol':moneda,
                            'percentage_principal_dias':float(percentage_principal_dias) 
                        })
                        #print(porcentajes_diarios)
                except:
                     pass
        
        porcentajes_mensuales = pd.DataFrame(porcentajes_diarios, columns=['symbol', 'percentage_principal_dias']).set_index(['symbol'])
        porcentajes_mensuales = porcentajes_mensuales.groupby('symbol')['percentage_principal_dias'].sum()
        porcentajes_mensuales = porcentajes_mensuales[porcentajes_mensuales > 0.5]
        print(porcentajes_mensuales)
        a = porcentajes_mensuales.describe()
        print(a)
        count = int(a['count'])
        a_list = list(range(count-1))
        print(a_list)
        explode = [0.1]
        for lis in a_list:
            element = 0.1
            explode.append(element)
        colores = ['#DBBF33', '#DBBF60', '#FFD70D', '#FFD97D']
        #print(porcentajes_mensuales)
        mes_ = convert(int(mes))
        porcentajes_mensuales.plot(kind='pie', subplots=True, explode=explode, autopct='%.2f%%', ylabel=' ', title=f'Tiempo invertido por symbol durante el mes de {str(mes_)}', colors = colores )
   
        plt.savefig('static/balances_mensual_transcurrido.png')
        #plt.close()
        plt.clf()

        #Altcoins
        try:
            take_profit_type = search("SELECT take_profit_type FROM `take_profit_type`",)
        except:
            time.sleep(5)
            take_profit_type = search("SELECT take_profit_type FROM `take_profit_type`",)
        take_profit_type = take_profit_type[0]['take_profit_type']
        if take_profit_type == 'take_profit_bull' or take_profit_type == 'take_profit_bear':
            try:
                cartera_total = search("SELECT `balance` FROM `pnl_live` WHERE `symbol`='TOTAL_ALTCOINS' ",)
                if cartera_total == ():
                    time.sleep(5)
                    cartera_total = search("SELECT `balance` FROM `pnl_live` WHERE `symbol`='TOTAL_ALTCOINS' ",)
            except:
                time.sleep(5)
                cartera_total = search("SELECT `balance` FROM `pnl_live` WHERE `symbol`='TOTAL_ALTCOINS' ",)
            #print(cartera_total)
            if cartera_total != ():
                cartera_total = cartera_total[0]['balance']
                cartera_total = float(cartera_total)
                try:
                    altcoins_totales = search("SELECT * FROM `pnl_live`",)
                except:
                    time.sleep(5)
                    altcoins_totales = search("SELECT * FROM `pnl_live`",)


                query = f"TRUNCATE TABLE wufto.altcoins_porcentajes;"
                ret = query_(query)

                for altcoins_total in altcoins_totales:
                    moneda_alt=altcoins_total['symbol']
                    balance_alt=float(altcoins_total['balance'])
                    profit_alt=float(altcoins_total['profit_loss_percentage'])
                    
                    try:
                        percentage_balance_alt= (balance_alt * 100) / cartera_total
                        percentage_profit_alt = truncate(profit_alt, 2)

                    except:
                        percentage_balance_alt= float(0)
                        percentage_profit_alt = float(0)

                    altcoins_porcentajes=Altcoins_totales.objects.create(
                            moneda=moneda_alt,
                            percentage_balance=percentage_balance_alt,
                            percentage_profit= percentage_profit_alt
                        )
                    

                    
                    #percentage_profit_alt_live grafico de Datatable 
                    try:
                        altcoins_totales_live = search("SELECT * FROM `pnl_live`",)
                    except:
                        time.sleep(5)
                        altcoins_totales_live = search("SELECT * FROM `pnl_live`",)
                    balances_totales_porcentajes = []
                    for altcoins_total in altcoins_totales_live:
                        moneda_alt_=altcoins_total['symbol']
                        balance_alt_=float(altcoins_total['balance'])
                        profit_alt_=float(altcoins_total['profit_loss_percentage'])
                        percentage_profit_alt_live = truncate(profit_alt_, 2)
                        if moneda_alt_ == 'TOTAL_ALTCOINS':
                            moneda_alt_total = 'TOTAL'
                            balances_totales_porcentajes.append({
                            'symbol':moneda_alt_total,
                            '%':(percentage_profit_alt_live)
                        })
                        else:
                            balances_totales_porcentajes.append({
                                'symbol':moneda_alt_,
                                '%':(percentage_profit_alt_live)
                            })

                    #percentage_profit_alt_live grafico de Datatable 
                try:
                    balance_total_historico = search("SELECT * FROM `balance_total_historico`",)
                except:
                    time.sleep(5)
                    balance_total_historico = search("SELECT * FROM `balance_total_historico`",)
                balance_total_historico_ = []
                balance_total_historico_alts = []
                #print(f"balance_total_historicos {balance_total_historico}")
                for balance_total_historicos in balance_total_historico:
                        
                        #print(balance_total_historicos)         	
                        balance_total=balance_total_historicos['description']
                        amount_usdt=balance_total_historicos['amount_usdt']
                        fecha=balance_total_historicos['fecha']
                        if balance_total == 'balance_total':
                            balance_total_historico_.append({
                                'balance_total':balance_total,
                                'amount_usdt':amount_usdt,
                                'fecha':fecha
                            })
                        else:
                            balance_total_historico_alts.append({
                                'balance_total':balance_total,
                                'amount_usdt':amount_usdt,
                                'fecha':fecha
                            })


        
                colores = ['#FFF10D' ]
                title='Porcentaje de Ganancia en Altcoins'
                bal = pd.DataFrame(balances_totales_porcentajes, columns=['symbol','%']).set_index(['symbol']).sort_values(by='%', ascending=False).head(20)
                bal.plot(kind = 'bar', align='center', title=title, xlabel='', ylabel=' ', color=['#DBBF33'])
                #print(bal)  

                plt.savefig('static/percentage_profit.png')
                #plt.close()
                plt.clf()

                colores = ['#FFF10D' ]
                title='balance_total_historico'
                bal = pd.DataFrame(balances_totales_porcentajes, columns=['balance_total','amount_usdt', 'fecha'])
                #bal.plot(kind = 'line', title=title, xlabel='Porcentaje de ganancia', ylabel=' ', color=['#DBBF33'])
                #print(bal)  
                t=bal.loc[:, 'balance_total']
                s=bal.loc[:, 'fecha']
                fig, ax = plt.subplots()
                ax.plot(t,s)
                print(bal.tail())
                plt.savefig('static/balance_total_historico.png')
                #plt.close()
                plt.clf()
            else:
                query = f"TRUNCATE TABLE wufto.altcoins_porcentajes;"
                ret = query_(query)

                altcoins_porcentajes=Altcoins_totales.objects.create(
                        moneda='Total Altcoins',
                        percentage_balance=0,
                        percentage_profit= 0
                )
                colores = ['#FFF10D' ]
                title='Porcentaje de Ganancia en Altcoins'
                balances_totales_porcentajes=[]
                balances_totales_porcentajes.append({
                        'symbol':'',
                        '%':0
                    })
                bal = pd.DataFrame(balances_totales_porcentajes, columns=['symbol','%']).set_index(['symbol']).sort_values(by='%', ascending=True)
                bal.plot(kind = 'bar', align='center', title=title, xlabel='', ylabel=' ', color=['#DBBF33'])
                #print(bal)  

                plt.savefig('static/percentage_profit.png')
                #plt.close()
                plt.clf()


        #tasas_create()

        #ultimo ath
        try:
            ath_last = search("SELECT * FROM `tasas` WHERE `tipo_tasa` = 'ath' ",)
            fecha_inicio_ath_last = ath_last[0]["fecha_inicio_tasa"]
            fecha_fin_ath_last = ath_last[0]["fecha_fin_tasa"] 
            tasa_ath_last = ath_last[0]["tasa"]
            tipo_tasa_ath_last = ath_last[0]["tipo_tasa"]

        except Exception as e:
                                                message = f'Fallo busqueda de ath en tasas  {e}'
                                                print(message)  
                                                pass

        query = f"TRUNCATE TABLE wufto.tasas;"
        ret = query_(query)

        try:
            balances = search("SELECT * FROM `balances_totales_historicos` WHERE `symbol` = 'TOTAL_BALANCE' ",)
            #balances = self.db.fetch("SELECT * FROM `balances_totales_historicos`",)
        except Exception as e:
                                                message = f'Fallo busqueda de balances_totales_historicos  {e}'
                                                print(message)  
                                                pass
        
        try:
            participaciones = search("SELECT * FROM `wufto_participaciones` WHERE `id` = '17'",)
            #participaciones = self.db.fetch("SELECT * FROM `wufto_participaciones` WHERE `id` = '17'",)
        except Exception as e:
                                                message = f'Fallo busqueda de participacion de contabilidad interna {e}'
                                                print(message)  
                                                pass

        fechas_participacion = []

        for part in participaciones:
                fecha = part["fecha"]
                participacion = float(part["participacion"])
                fechas_participacion.append({
                        "fecha": fecha,
                        "participacion":participacion
                })

         
        historical_balances = pd.DataFrame(balances)
        historical_balances['fecha'] = pd.to_datetime(historical_balances['fecha'], format='%Y-%m-%d')
        historical_balances['date'] =  historical_balances['fecha'].dt.strftime('%Y-%m-%d')
        historical_balances = historical_balances.sort_values(by='date')
        #print(historical_balances)

        fechas_participacion_df = pd.DataFrame(fechas_participacion)
        fechas_participacion_df['fecha'] = pd.to_datetime(fechas_participacion_df['fecha'], format='%Y-%m-%d')
        fechas_participacion_df['date'] =  fechas_participacion_df['fecha'].dt.strftime('%Y-%m-%d')
        fechas_participacion_df = fechas_participacion_df.sort_values(by='date')
        #print(fechas_participacion_df)
        merged_df = pd.merge(historical_balances, fechas_participacion_df, on='date', how='left')
        merged_df.sort_values('date', inplace=True)
        merged_df['participacion'].fillna(method='ffill', inplace=True)

        merged_df['saldos'] = merged_df['amount_usdt'] * merged_df['participacion'] / 100
        print(merged_df)



        fecha_inicio = merged_df['date'].iloc[0]
        balance_inicio = merged_df['saldos'].iloc[0] 
        año_inicio = fecha_inicio[0:4]

        fecha_fin = merged_df["date"].iloc[-1]
        balance_fin = merged_df["saldos"].iloc[-1] 
        año_fin = fecha_fin[0:4]

        anios = list(range(int(año_inicio), int(año_fin)+1))

        tasa = (balance_fin - balance_inicio)/balance_inicio * 100

        tasas = []

        tasas.append({
             "fecha_inicio_tasa":str(fecha_inicio),
             "fecha_fin_tasa":str(fecha_fin),
             "tasa": round(tasa,2),
             "tipo_tasa": "total"

        })
        try:
            create_tasas=Tasas.objects.create(
                        fecha_inicio_tasa=str(fecha_inicio),
                        fecha_fin_tasa=str(fecha_fin),
                        tasa=round(tasa,2),
                        tipo_tasa="total"
            )
        except Exception as e:
                message = f'No pudo guardar operacion {e}'
                print(message) 

        #calculo de tasa ath

        if float(tasa) > float(tasa_ath_last):
            tasas_ath = []
            tasas_ath.append({
                "fecha_inicio_tasa":str(fecha_inicio),
                "fecha_fin_tasa":str(fecha_fin),
                "tasa": round(tasa,2),
                "tipo_tasa": "ath"

            })
            try:
                create_tasas=Tasas.objects.create(
                            fecha_inicio_tasa=str(fecha_inicio),
                            fecha_fin_tasa=str(fecha_fin),
                            tasa=round(tasa,2),
                            tipo_tasa="ath"
                )
            except Exception as e:
                    message = f'No pudo guardar operacion {e}'
                    print(message) 
        else:
            tasas_ath = []
            tasas_ath.append({
                "fecha_inicio_tasa":str(fecha_inicio_ath_last),
                "fecha_fin_tasa":str(fecha_fin),
                "tasa": round(tasa_ath_last,2),
                "tipo_tasa": "ath"

            })
            try:
                create_tasas=Tasas.objects.create(
                            fecha_inicio_tasa=str(fecha_inicio_ath_last),
                            fecha_fin_tasa=str(fecha_fin),
                            tasa=round(tasa_ath_last,2),
                            tipo_tasa="ath"
                )
            except Exception as e:
                    message = f'No pudo guardar operacion {e}'
                    print(message) 
             
              

        merged_df['date'] = pd.to_datetime(merged_df['date'])
        merged_df.set_index('date', inplace=True)

        tasas_anuales = merged_df.resample('Y').last()
        tasas_anuales.loc[len(tasas_anuales)] = merged_df.iloc[0]
        tasas_anuales = tasas_anuales.sort_values(by='fecha_x')
        tasas_anuales = tasas_anuales.reset_index()
        tasas_anuales["tasa"] = (tasas_anuales["saldos"] - tasas_anuales["saldos"].shift(1)) / tasas_anuales["saldos"].shift(1) * 100
        tasas_anuales["fecha_inicio"] = tasas_anuales["fecha_x"].shift(1) 
        tasas_anuales["fecha_cierre"] = tasas_anuales["fecha_x"] 
        tasas_anuales = tasas_anuales.drop(0)
        print(tasas_anuales)

        tasas_anuales = tasas_anuales.values.tolist()
        print(tasas_anuales)

        for anio in tasas_anuales:
            fecha_inicio = anio[10]
            fecha_fin = anio[11]
            tasa = anio[9]
            tasas.append({
             "fecha_inicio_tasa":str(fecha_inicio.strftime('%Y-%m-%d')),
             "fecha_fin_tasa":str(fecha_fin.strftime('%Y-%m-%d')),
             "tasa": round(tasa,2),
             "tipo_tasa": "anual"
        })
            try:
                create_tasas=Tasas.objects.create(
                            fecha_inicio_tasa=str(fecha_inicio.strftime('%Y-%m-%d')),
                            fecha_fin_tasa=str(fecha_fin.strftime('%Y-%m-%d')),
                            tasa=round(tasa,2),
                            tipo_tasa="anual"
                )
            except Exception as e:
                message = f'No pudo guardar operacion {e}'
                print(message) 


        

        tasas_trimestrales = merged_df.resample('Q').last()
        tasas_trimestrales.loc[len(tasas_trimestrales)] = merged_df.iloc[0]
        tasas_trimestrales = tasas_trimestrales.sort_values(by='fecha_x')
        tasas_trimestrales = tasas_trimestrales.reset_index()
        tasas_trimestrales["tasa"] = (tasas_trimestrales["saldos"] - tasas_trimestrales["saldos"].shift(1)) / tasas_trimestrales["saldos"].shift(1) * 100
        tasas_trimestrales["fecha_inicio"] = tasas_trimestrales["fecha_x"].shift(1) 
        tasas_trimestrales["fecha_cierre"] = tasas_trimestrales["fecha_x"] 
        tasas_trimestrales = tasas_trimestrales.drop(0)

        tasas_trimestrales = tasas_trimestrales.values.tolist()
        print(tasas_trimestrales)

        for anio in tasas_trimestrales:
            fecha_inicio = anio[10]
            fecha_fin = anio[11]
            tasa = anio[9]
            tasas.append({
             "fecha_inicio_tasa":str(fecha_inicio.strftime('%Y-%m-%d')),
             "fecha_fin_tasa":str(fecha_fin.strftime('%Y-%m-%d')),
             "tasa": round(tasa,2),
             "tipo_tasa": "trimestral"
        })
            try:
                create_tasas=Tasas.objects.create(
                            fecha_inicio_tasa=str(fecha_inicio.strftime('%Y-%m-%d')),
                            fecha_fin_tasa=str(fecha_fin.strftime('%Y-%m-%d')),
                            tasa=round(tasa,2),
                            tipo_tasa="trimestral"
                )
            except Exception as e:
                message = f'No pudo guardar operacion {e}'
                print(message) 

        tasas_mensuales = merged_df.resample('M').last()
        tasas_mensuales.loc[len(tasas_mensuales)] = merged_df.iloc[0]
        tasas_mensuales = tasas_mensuales.sort_values(by='fecha_x')
        tasas_mensuales = tasas_mensuales.reset_index()
        tasas_mensuales["tasa"] = (tasas_mensuales["saldos"] - tasas_mensuales["saldos"].shift(1)) / tasas_mensuales["saldos"].shift(1) * 100
        tasas_mensuales["fecha_inicio"] = tasas_mensuales["fecha_x"].shift(1) 
        tasas_mensuales["fecha_cierre"] = tasas_mensuales["fecha_x"] 
        tasas_mensuales = tasas_mensuales.drop(0)

        tasas_mensuales = tasas_mensuales.values.tolist()
        print(tasas_mensuales)

        for anio in tasas_mensuales:
            fecha_inicio = anio[10]
            fecha_fin = anio[11]
            tasa = anio[9]
            tasas.append({
             "fecha_inicio_tasa":str(fecha_inicio.strftime('%Y-%m-%d')),
             "fecha_fin_tasa":str(fecha_fin.strftime('%Y-%m-%d')),
             "tasa": round(tasa,2),
             "tipo_tasa": "mensual"
        })
        
            try:
                create_tasas=Tasas.objects.create(
                            fecha_inicio_tasa=str(fecha_inicio.strftime('%Y-%m-%d')),
                            fecha_fin_tasa=str(fecha_fin.strftime('%Y-%m-%d')),
                            tasa=round(tasa,2),
                            tipo_tasa="mensual"
                )
            except Exception as e:
                message = f'No pudo guardar operacion {e}'
                print(message) 
        
        balances_porcentajes=Balances_totales.objects.all()
        altcoins_porcentajes=Altcoins_totales.objects.all()
        print(altcoins_porcentajes)
        #tasas_create_=Tasas.objects.all()
        tasas_create_total=Tasas.objects.filter(tipo_tasa__icontains="total")
        tasas_create_ath=Tasas.objects.filter(tipo_tasa__icontains="ath")
        tasas_create_anual=Tasas.objects.filter(tipo_tasa__icontains="anual")
        tasas_create_trimestral=Tasas.objects.filter(tipo_tasa__icontains="trimestral")
        tasas_create_mensual=Tasas.objects.filter(tipo_tasa__icontains="mensual")

        return render(request,'dashboard.html', {'balances_porcentajes':balances_porcentajes, 'symbol':moneda, 'percentage':percentage, 'altcoins_porcentajes':altcoins_porcentajes, 'tasas_create_total':tasas_create_total,'tasas_create_ath':tasas_create_ath, 'tasas_create_anual':tasas_create_anual,'tasas_create_trimestral':tasas_create_trimestral,'tasas_create_mensual':tasas_create_mensual})

#, 'moneda_alt':moneda_alt, 'balance_alt':balance_alt, 'profit_alt':profit_alt, 'percentage_balance':percentage_balance_alt, 'percentage_profit': percentage_profit_alt, 'items_2':items_2





# Auxiliares

def truncate(number: float, max_decimals: int) -> float:
        int_part, dec_part = str(number).split(".")
        return float(".".join((int_part, dec_part[:max_decimals])))

def convert(mes):
     if mes == 1:
        mes = 'ENERO'
     if mes == 2:
        mes = 'FEBRERO'
     if mes == 3:
        mes = 'MARZO'
     if mes == 4:
        mes = 'ABRIL'
     if mes == 5:
        mes = 'MAYO'
     if mes == 6:
        mes = 'JUNIO'
     if mes == 7:
        mes = 'JULIO'
     if mes == 8:
        mes = 'AGOSTO'
     if mes == 9:
        mes = 'SEPTIEMBRE'
     if mes == 10:
        mes = 'OCTUBRE'
     if mes == 11:
        mes = 'NOVIEMBRE'
     if mes == 12:
        mes = 'DICIEMBRE'

     return mes

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
                db='wufto'
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