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

from timestamp_timezones import *

if __name__ == "__main__":
	# Imprimir título
	os.write(
		sys.stdout.fileno(), 
		"\n######### Obtener timestamp con zonas horarias #########\n\n"
		.encode('utf-8')
		)
	
	#Establecer el formato de timestamp que se desea:
	timestamp_format = "%Y-%m-%d %H:%M:%S.%f"
	
	#Se obtiene timestamp actual en UTC en formato string
	time_now_UTC = get_UTC_Now(timestamp_format)
	
	#Por lo tanto hay que convertirla de str a datetime.datetime
	t_UTC = convert_timestampSTR_to_timestampDateTime(time_now_UTC, timestamp_format)

	#Convertir time_now_UTC a zona horaria de America/Regina por ejemplo:
	time_now_CRC = convert_from_timezone_to_timezone(t_UTC, timestamp_format, 'UTC', 'America/Costa_Rica')

	#Convertir time_now_UTC a zona horaria de Phoenix por ejemplo:
	time_now_Phoenix = convert_from_timezone_to_timezone(t_UTC, timestamp_format, 'UTC', 'America/Phoenix')
	
	# Imprimir el tiempo NOW en UTC obtenido
	os.write(sys.stdout.fileno(), "\n\n-----------\nInformación de hoy\n".encode('utf-8'))
	os.write(sys.stdout.fileno(), ("Tiempo en UTC: \t\t\t\t" + str(time_now_UTC)).encode('utf-8'))
	os.write(sys.stdout.fileno(), " --> Notar la T para diferencias entre fecha y hora".encode('utf-8'))

	# Imprimir el tiempo en zona horaria America/Phoenix
	os.write(sys.stdout.fileno(), ("\nTiempo en Phoenix: \t\t\t" + str(time_now_Phoenix)).encode('utf-8'))

	# Imprimir el tiempo en zona horaria America/Costa_Rica
	os.write(sys.stdout.fileno(), ("\nTiempo en America/Costa_Rica: \t\t" + str(time_now_CRC)).encode('utf-8'))

	# Obtener el año, el mes y el día de la fecha actual
	ano_actual = get_year(time_now_CRC)
	mes_actual_num, mes_actual_nom = get_month(time_now_CRC)
	dia_actual_num, dia_actual_nom = get_day(time_now_CRC)

	os.write(sys.stdout.fileno(), ("\n\nEl año actual es: \t\t" + str(ano_actual)).encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nEl mes actual es: \t\t" + str(mes_actual_num) + " (" + mes_actual_nom + ")").encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nEl día de la semana es: \t" + str(dia_actual_num) + " (" + dia_actual_nom + ")").encode('utf-8'))
	os.write(sys.stdout.fileno(), "\n-----------\n".encode('utf-8'))

	os.write(sys.stdout.fileno(), ("\n\n--> Se envía una hora y se convierte a datetime con la fecha de hoy").encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nSi le ingreso la hora 12:12:20.\nAutomático me sale la fecha de hoy y la hora: " + str(join_hour_to_today("12:12:20", "America/Costa_Rica"))).encode('utf-8'))
	
	# Diferencia de X años al año actual
	diferencia_de_anos = 4
	nuevo_timestamp_con_dif_de_anos = get_year_dif(time_now_CRC, timestamp_format, diferencia_de_anos)
	new_timestamp_con_dif_de_anos_ANO = get_year(nuevo_timestamp_con_dif_de_anos)
	os.write(sys.stdout.fileno(), ("\n\nHoy en " + str(diferencia_de_anos) + " años será: " + nuevo_timestamp_con_dif_de_anos).encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nEl año resultante es: " + str(new_timestamp_con_dif_de_anos_ANO)).encode('utf-8'))
	diferencia_de_meses = -1
	nuevo_timestamp_con_dif_de_meses = get_month_dif(time_now_CRC, timestamp_format, diferencia_de_meses)
	new_timestamp_con_dif_de_meses_MES = get_month(nuevo_timestamp_con_dif_de_meses)
	os.write(sys.stdout.fileno(), ("\n\n" + str(diferencia_de_meses) + " meses representa el timestamp: " + nuevo_timestamp_con_dif_de_meses).encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\nEl mes resultante es: " + str(new_timestamp_con_dif_de_meses_MES)).encode('utf-8'))
	os.write(sys.stdout.fileno(), ("\n\n\n\n").encode('utf-8'))