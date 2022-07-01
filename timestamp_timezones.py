#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import threading
import traceback
import time
import signal
import fcntl
import string
import re

import pytz

from datetime import datetime
from pytz import timezone

CRC_Format = 'America/Costa_Rica'
Phoenix_Format = 'America/Phoenix'

def join_hour_to_today(hour):
	global CRC_Format
	#Ingresa la hora a la que quieres añadir a la fecha
	#Sale el datetime correspondiente que se ha creado

	time_now_UTC = datetime.utcnow().isoformat(timespec='microseconds')
	t_UTC = datetime.strptime(time_now_UTC, "%Y-%m-%dT%H:%M:%S.%f")
	t_CRC = t_UTC.replace(tzinfo=pytz.UTC).astimezone(timezone(CRC_Format)).strftime("%Y-%m-%dT%H:%M:%S.%f")
	t_dia = t_CRC.split("T")[0] + "T" + hour
	datetime_creado = datetime.strptime(t_dia, "%Y-%m-%dT%H:%M:%S")
	return datetime_creado


def get_timestamp_and_weekday(utc_or_other):
	#No ingresa nada
	#Retorna un array con el timestamp y el weekday
	datos_de_retorno = []
	time_now_UTC = datetime.utcnow().isoformat(timespec='microseconds')
	t_UTC = datetime.strptime(time_now_UTC, "%Y-%m-%dT%H:%M:%S.%f")
	timestamp_now = t_UTC
	iso_week_day = t_UTC.isoweekday()

	if utc_or_other != "UTC":
		t_CRC = t_UTC.replace(tzinfo=pytz.UTC).astimezone(timezone(utc_or_other)).strftime("%Y-%m-%dT%H:%M:%S.%f")
		timestamp_now = datetime.strptime(t_CRC, "%Y-%m-%dT%H:%M:%S.%f")
		iso_week_day = timestamp_now.isoweekday()

	datos_de_retorno.append(timestamp_now)
	datos_de_retorno.append(iso_week_day)
	return datos_de_retorno




if __name__ == "__main__":
	# Solamente para imprimir un título
	os.write(sys.stdout.fileno(), "\n######### Obtener timestamp con zonas horarias #########\n\n".encode('utf-8'))
	#Establecer el formato de timestamp que se desea:
	timestamp_format = "%Y-%m-%d %H:%M:%S.%f"
	#Se obtiene time_now en UTC en formato string
	time_now_UTC = datetime.utcnow().isoformat(timespec='microseconds')
	print(timestamp_hour_and_weekday("America/New_York"))
	print("\n\n")
	#Por lo tanto hay que convertirla de str a datetime.datetime
	t_UTC = datetime.strptime(time_now_UTC, "%Y-%m-%dT%H:%M:%S.%f")
	#Convertir time_now_UTC a zona horaria de America/Regina por ejemplo:
	time_now_CRC = t_UTC.replace(tzinfo=pytz.UTC).astimezone(timezone(CRC_Format)).strftime(timestamp_format)
	time_now_Phoenix = t_UTC.replace(tzinfo=pytz.UTC).astimezone(timezone(Phoenix_Format)).strftime(timestamp_format)
	os.write(sys.stdout.fileno(), ("El número de día UTC hoy es: \t\t" + str(t_UTC.isoweekday()) + "\n").encode('utf-8'))
	os.write(sys.stdout.fileno(), ("Tiempo en UTC: \t\t\t\t" + str(time_now_UTC)).encode('utf-8'))
	os.write(sys.stdout.fileno(), " --> Notar la T para diferencias entre fecha y hora\n".encode('utf-8'))
	os.write(sys.stdout.fileno(), ("Tiempo en America/Regina: \t\t" + str(time_now_CRC)).encode('utf-8'))
	os.write(sys.stdout.fileno(), " --> Esta conversión ya no tiene T entre fecha y hora\n".encode('utf-8'))
	os.write(sys.stdout.fileno(), ("Tiempo en Phoenix: \t\t\t" + str(time_now_Phoenix)).encode('utf-8'))
	os.write(sys.stdout.fileno(), " --> Esta conversión ya no tiene T entre fecha y hora\n".encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nSi le ingreso la hora 12:12:20,\nautomatico me sale la fecha de hoy\ny la hora: \t\t\t\t" + str(join_hour_to_today("12:12:20"))).encode('utf-8'))
	os.write(sys.stdout.fileno(), (" --> Se le envía una hora y él la convierte a datetime con la fecha de hoy"  + "\n\n\n\n\n").encode('utf-8'))