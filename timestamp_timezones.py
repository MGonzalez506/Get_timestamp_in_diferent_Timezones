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

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone

CRC_Format = 'America/Costa_Rica'
Phoenix_Format = 'America/Phoenix'

def get_year(t_now, t_stamp_format):
	timestamp = datetime.strptime(t_now, t_stamp_format) if isinstance(t_now, str) else t_now
	year = timestamp.year
	return str(year)

def get_month(t_now, t_stamp_format):
	timestamp = datetime.strptime(t_now, t_stamp_format) if isinstance(t_now, str) else t_now
	month = timestamp.month
	return str(month)

def get_year_dif(t_now, t_stamp_format, t_diff):
	timestamp = datetime.strptime(t_now, t_stamp_format) if isinstance(t_now, str) else t_now
	other_year = timestamp + relativedelta(years=t_diff)
	return str(other_year)

def get_month_dif(t_now, t_stamp_format, t_diff):
	timestamp = datetime.strptime(t_now, t_stamp_format) if isinstance(t_now, str) else t_now
	other_year = timestamp + relativedelta(months=t_diff)
	return str(other_year)

def get_month_dif_beginning(t_now, t_stamp_format, t_diff):
	timestamp = datetime.strptime(t_now, t_stamp_format) if isinstance(t_now, str) else t_now
	other_year = timestamp + relativedelta(months=t_diff)
	return str(other_year.replace(day=1, hour=0, minute=0, second=0, microsecond=0))

def get_TStamp_with_TZone_from_UTC(t_now, t_stamp_format, zona_horaria):
	timestamp = datetime.strptime(t_now, t_stamp_format) if isinstance(t_now, str) else t_now
	return str(timestamp.replace(tzinfo=pytz.UTC).astimezone(timezone(zona_horaria)).strftime(t_stamp_format))

def get_UTC_Now(t_stamp_format):
	return datetime.strptime(datetime.utcnow().isoformat(timespec='microseconds'), "%Y-%m-%dT%H:%M:%S.%f").strftime(t_stamp_format)

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




# Create a function that gets the timezone and the format of a timestamp
def get_timestamp_format_timezone_and_numberOfDecimalPoints(timestamp,default_tz):
	# t_stamp string
	t_stamp = ""

	#===========================================================
	# OUTPUT VARIABLES
	#===========================================================
	# default_tz: the timezone where the program is running.
	# In case that the timestamp doesn't have a timezone, the default_tz will be used
	timezone = default_tz
	# timestamp_format: the format of the timestamp
	timestamp_format = ""
	# number_of_decimal_points: the number of decimal points in the timestamp
	number_of_decimal_points = 0

	#===========================================================
	# FUNCTION
	#===========================================================
	# Check if t_stamp is datetime.datetime object
	if isinstance(t_stamp, datetime):
		# Convert from datetime.datetime object to string
		t_stamp = timestamp.isoformat(timespec='microseconds')
	else:
		t_stamp = timestamp

	# Check if the timestamp contains the letter "Z" at the end
	if t_stamp[-1] == "Z":
		timezone = "UTC+00:00"
	elif t_stamp[-6] == "+":
		timezone = "UTC" + t_stamp[-6:]
	elif t_stamp[-6] == "-":
		timezone = "UTC" + t_stamp[-6:]
	
	# Check if the timestamp contains the "." character
	if "." in t_stamp:
		number_of_decimal_points = len(t_stamp.split(".")[1])
		# Check if the timestamp contains the letter "T" character
		if "T" in t_stamp:
			timestamp_format = "%Y-%m-%dT%H:%M:%S.%f"
		else:
			timestamp_format = "%Y-%m-%d %H:%M:%S.%f"
	else:
		# Check if the timestamp contains the letter "T" character
		if "T" in t_stamp:
			timestamp_format = "%Y-%m-%dT%H:%M:%S"
		else:
			timestamp_format = "%Y-%m-%d %H:%M:%S"

	#===========================================================
	# RETURN
	#===========================================================
	return timestamp_format, timezone, number_of_decimal_points
if __name__ == "__main__":
	# Solamente para imprimir un título
	os.write(sys.stdout.fileno(), "\n######### Obtener timestamp con zonas horarias #########\n\n".encode('utf-8'))
	#Establecer el formato de timestamp que se desea:
	timestamp_format = "%Y-%m-%d %H:%M:%S.%f"
	#Se obtiene time_now en UTC en formato string
	time_now_UTC = get_UTC_Now(timestamp_format)
	print(get_timestamp_and_weekday("America/New_York"))
	print("\n\n")
	#Por lo tanto hay que convertirla de str a datetime.datetime
	t_UTC = datetime.strptime(time_now_UTC, "%Y-%m-%d %H:%M:%S.%f")
	#Convertir time_now_UTC a zona horaria de America/Regina por ejemplo:
	time_now_CRC = t_UTC.replace(tzinfo=pytz.UTC).astimezone(timezone(CRC_Format)).strftime(timestamp_format)
	time_now_Phoenix = t_UTC.replace(tzinfo=pytz.UTC).astimezone(timezone(Phoenix_Format)).strftime(timestamp_format)
	os.write(sys.stdout.fileno(), ("El número de día UTC hoy es: \t" + str(t_UTC.isoweekday()) + "\n").encode('utf-8'))
	os.write(sys.stdout.fileno(), ("Tiempo en UTC: \t\t\t\t\t" + str(time_now_UTC)).encode('utf-8'))
	os.write(sys.stdout.fileno(), " --> Notar la T para diferencias entre fecha y hora".encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nTiempo en America/Regina: \t\t" + str(time_now_CRC)).encode('utf-8'))
	os.write(sys.stdout.fileno(), " --> Esta conversión ya no tiene T entre fecha y hora\n".encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nTiempo en America/Costa_Rica: \t" + get_TStamp_with_TZone_from_UTC(t_UTC, timestamp_format, 'America/Costa_Rica')).encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nTiempo en Phoenix: \t\t\t\t" + str(time_now_Phoenix)).encode('utf-8'))
	os.write(sys.stdout.fileno(), " --> Esta conversión ya no tiene T entre fecha y hora\n".encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\n\n--> Se le envía una hora y él la convierte a datetime con la fecha de hoy").encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nSi le ingreso la hora 12:12:20.\nAutomático me sale la fecha de hoy y la hora: " + str(join_hour_to_today("12:12:20"))).encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\n\nEl año actual es: " + get_year(time_now_CRC, timestamp_format)).encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nEl mes actual es: " + get_month(time_now_CRC, timestamp_format)).encode('utf-8'))
	# Diferencia de X años al año actual
	diferencia_de_anos = 4
	os.write(sys.stdout.fileno(), ("\n\n" + str(diferencia_de_anos) + " años representa el timestamp: " + get_year_dif(time_now_CRC, timestamp_format, diferencia_de_anos)).encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nEl año resultante es: " + get_year(get_year_dif(time_now_CRC, timestamp_format, diferencia_de_anos), timestamp_format)).encode('utf-8'))
	diferencia_de_meses = -1
	os.write(sys.stdout.fileno(), ("\n\n" + str(diferencia_de_meses) + " meses representa el timestamp: " + get_month_dif(t_UTC, timestamp_format, diferencia_de_meses)).encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nEl mes resultante es: " + get_month(get_month_dif(time_now_CRC, timestamp_format, diferencia_de_meses), timestamp_format)).encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nEl inicio de este cambio de mes es: " + get_month_dif_beginning(time_now_CRC, timestamp_format, diferencia_de_meses)).encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\n\n\n\n").encode('utf-8'))