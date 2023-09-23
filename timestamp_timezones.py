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

nombre_del_mes = {1:"Enero", 2:"Febrero", 3:"Marzo", 4:"Abril", 5:"Mayo", 6:"Junio",
				  7:"Julio", 8:"Agosto", 9:"Setiembre", 10:"Octubre",
				  11:"Noviembre", 12:"Diciembre"}

nombre_de_la_semana = {1:"Lunes", 2:"Martes", 3:"Miércoles", 4:"Jueves",
					   5:"Viernes", 6:"Sábado", 7:"Domingo"}

def get_year(t_now):
	t_stamp_format = check_timestamp_format(t_now)
	timestamp = datetime.strptime(t_now, t_stamp_format) if isinstance(t_now, str) else t_now
	year = timestamp.year
	return year

def get_month(t_now):
	t_stamp_format = check_timestamp_format(t_now)
	timestamp = datetime.strptime(t_now, t_stamp_format) if isinstance(t_now, str) else t_now
	month = timestamp.month
	return month, nombre_del_mes[month]

def get_day(t_now):
	t_stamp_format = check_timestamp_format(t_now)
	timestamp = datetime.strptime(t_now, t_stamp_format) if isinstance(t_now, str) else t_now
	dia = timestamp.isoweekday()
	return dia, nombre_de_la_semana[dia]

def get_year_dif(t_now, t_stamp_format, t_diff):
	timestamp = datetime.strptime(t_now, t_stamp_format) if isinstance(t_now, str) else t_now
	other_year = timestamp + relativedelta(years=t_diff)
	# Return other_year as datetime.datetime object
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

def convert_timestampSTR_to_timestampDateTime(timestamp, timestamp_format):
	return datetime.strptime(timestamp, timestamp_format)

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

def convert_from_timezone_to_timezone(timestamp, timestamp_format, input_timezone, output_timezone):
	#===========================================================
	# INPUT VARIABLES
	#===========================================================
	# timestamp: the timestamp to convert
	# timestamp_format: the format of the timestamp
	# input_timezone: the timezone of the timestamp
	# output_timezone: the timezone to convert the timestamp

	#===========================================================
	# OUTPUT VARIABLES
	#===========================================================
	# timestamp_converted: the timestamp converted to the output_timezone

	#===========================================================
	# FUNCTION
	#===========================================================
	# Check if timestamp is datetime.datetime object
	if isinstance(timestamp, datetime):
		# Convert from datetime.datetime object to string
		timestamp = timestamp.strftime(timestamp_format)
	else:
		timestamp = timestamp
	# Convert the timestamp to datetime.datetime object
	timestamp = datetime.strptime(timestamp, timestamp_format)
	# Convert the timestamp to the input_timezone
	timestamp = timestamp.replace(tzinfo=pytz.timezone(input_timezone))
	# Convert the timestamp to the output_timezone
	timestamp_converted = timestamp.astimezone(pytz.timezone(output_timezone))
	# Convert the timestamp to string
	timestamp_converted = timestamp_converted.strftime(timestamp_format)

	#===========================================================
	# RETURN
	#===========================================================
	return timestamp_converted