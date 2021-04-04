from datetime import datetime
import pytz
import os

# Limpia lo que tenga el terminal
os.system('clear')

# Formato para zona horaria estándar UTC
UTC_Format = pytz.utc

# Formato para zona horaria específica ('En este caso America/Regina')
CRC_Format = pytz.timezone('America/Regina')

# Obtiene el primer Timestamp con el formato UTC definido previamente
t1 = datetime.now(UTC_Format)
# Obtiene el segundo Timestamp con el formato America/Regina definido previamente
t2 = datetime.now(CRC_Format)

# Imprime el primer valor del Timestamp en formato UTC
print("Timestamp en formato UTC: \t\t",t1)
# Imprime el segundo valor del Timestamp en formato America/Regina
print("Timestamp en formato America/Regina: \t",t2)

# Imprime los valores con un formato específico, mostrando la zona horaria y 
# adicionalmente la cantidad de horas que representa respecto al estándar UTC
print("\n\nTimestamp con formato:\t\t\t",
	t1.strftime('%Y:%m:%d %H:%M:%S.%f %Z %z'))

print("Timestamp con formato: \t\t\t",
	t2.strftime('%Y:%m:%d %H:%M:%S.%f %Z %z'))
print("\n\n")
