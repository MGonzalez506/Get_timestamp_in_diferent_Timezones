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

if __name__ == "__main__":
	# Solamente para imprimir un título
	os.write(sys.stdout.fileno(), "\n######### Obtener timestamp con zonas horarias #########\n\n".encode('utf-8'))
	#Establecer el formato de timestamp que se desea:
	timestamp_format = "%Y-%m-%d %H:%M:%S.%f"
	#Se obtiene time_now en UTC en formato string
	time_now_UTC = datetime.utcnow().isoformat(timespec='microseconds')
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