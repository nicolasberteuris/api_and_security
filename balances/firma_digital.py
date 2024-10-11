from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from django.http import JsonResponse
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import boto3
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
import json
import boto3
from botocore.exceptions import ClientError
from datetime import datetime
import requests
from cryptography.fernet import Fernet
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import redirect, render
import base64
from django.http import HttpResponseForbidden


def error_403(request):
    mensaje = "Lo siento, no tienes permiso para acceder a esta página."
    return render(request, 'error_403.html', {'mensaje': mensaje}, status=403)

def firmaaaa():
    crear_claves_y_encriptar_dato()
    #buscar_y_verificar_firma()



def crear_claves_y_encriptar_dato():
    try:
        # Generar clave
        clave_bytes = Fernet.generate_key()  # Genera una clave como bytes
        clave = clave_bytes.decode()  # Convierte la clave de bytes a una cadena de texto
        os.environ['MY_SECRET_KEY'] = clave

        # Utilizar la clave para Fernet
        fernet = Fernet(clave_bytes)  # Utiliza la clave en formato de bytes con Fernet

        # Generar clave privada RSA
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()

        # Serializar claves
        private_key_serialized = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_key_serialized = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Encriptar clave privada serializada
        dato_encriptado = fernet.encrypt(private_key_serialized)
        os.environ['dato_encriptado'] = dato_encriptado.decode()

        # Encriptar clave pública serializada
        dato_encriptado_2 = fernet.encrypt(public_key_serialized)
        os.environ['dato_encriptado_2'] = dato_encriptado_2.decode()

        try:

            # Ejemplo de transacción (sustituye con tus datos reales)
            fecha_hora_actual = datetime.now()
            fecha_hora_actual_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:00")

            transaccion = {
                'fecha': fecha_hora_actual_formateada,
            }

            firma = firmar_transaccion(private_key, transaccion)
            # Convertir los bytes de la firma a una cadena de texto utilizando codificación base64
            firma = base64.b64encode(firma).decode()

            # Asignar la firma a la variable de entorno
            os.environ['firma'] = firma

        except Exception as e:
            print("Error al crear la firma:", e)

    except Exception as e:
        print("Error al crear claves y encriptar dato:", e)


def buscar_y_verificar_firma(request):
    try:
        # Recuperar dato encriptado de la variable de entorno
        dato_encriptado_recuperado = os.environ.get('dato_encriptado')
        dato_encriptado_recuperado_2 = os.environ.get('dato_encriptado_2')

        # Recuperar claves y configurar Fernet
        clave = os.environ.get('MY_SECRET_KEY')
        fernet = Fernet(clave)

        # Desencriptar clave privada y pública serializada
        private_key_serialized_bytes = fernet.decrypt(dato_encriptado_recuperado.encode())
        public_key_serialized_bytes = fernet.decrypt(dato_encriptado_recuperado_2.encode())

        # Cargar claves RSA
        private_key_api = serialization.load_pem_private_key(
            private_key_serialized_bytes,
            password=None,
            backend=default_backend()
        )
        public_key_api = serialization.load_pem_public_key(
            public_key_serialized_bytes,
            backend=default_backend()
        )

        # Ejemplo de transacción (sustituye con tus datos reales)
        fecha_hora_actual = datetime.now()
        fecha_hora_actual_formateada = fecha_hora_actual.strftime("%Y-%m-%d %H:00")

        transaccion = {
            'fecha': fecha_hora_actual_formateada,
        }

        # Firmar la transacción
        #firma = firmar_transaccion(private_key_api, transaccion)
        firma = os.environ.get('firma')
        # Convertir firma de Unicode a bytes utilizando UTF-8
        firma = base64.b64decode(firma.encode()) 

        # Verificar la firma
        a =  verificar_transaccion(public_key_api, transaccion, firma)
        if a == True:
            print("La firma de la transaccion es valida.") 
            return True 
        else:
            print("La firma de la transaccion es invalida.")
            #error_403(request)
            return False
            #return HttpResponseForbidden("No tienes permiso para acceder a esta página.")
            #return redirect('logout')

    except Exception as e:
        print("Error al buscar y verificar firma:", e)
        return False
        return redirect('logout')



def generar_claves():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key

def firmar_transaccion(private_key, transaccion):
    transaccion_json = json.dumps(transaccion)
    transaccion_bytes = transaccion_json.encode('utf-8')

    firma = private_key.sign(
        transaccion_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return firma

def verificar_transaccion(public_key, transaccion, firma):
    transaccion_json = json.dumps(transaccion)
    transaccion_bytes = transaccion_json.encode('utf-8')

    try:
        public_key.verify(
            firma,
            transaccion_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f'Error al verificar la transacción: {e}')
        return False


def generate_and_serialized():
    # Generar las claves una sola vez
    private_key, public_key = generar_claves()
    # Serializar claves

    private_key_serialized = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    public_key_serialized = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    #os.environ['private_key_serialized'] = private_key_serialized
    #os.environ['public_key_serialized'] = public_key_serialized

    return private_key_serialized, public_key_serialized

