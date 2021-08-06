# Paquetes necesarios
```
pip install pytz
```

# Get_timestamp_in_diferent_Timezones
Normalmente es buena práctica almacenar en una base de datos el timestamp en UTC, sin embargo dependiendo de su zona horaria es útil convertir UTC a su Timezone determinado.

Pytz es un paquete sencillo de interpretar que permite entre muchas otras funciones, convertir timezones de una a otra.

Este código coloca la variable **CRC_Format** con el formato que se utiliza en Costa Rica para obtener la hora.
Y adicionalmente la variable **Phoenix_Format**, con el formato que se utiliza en la ciudad de Phoenix Arizona.

Utilizando el tiempo actual en UTC y estas dos variables se convierte el tiempo UTC en estas dos zonas horarias y se imprime en pantalla.

Adicionalmente en el siguiente link se pueden observar las diferentes zonas horarias de la base de datos tz:
[Lista de zonas horarias según base de datos TZ](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

Y también si se requiere, con el siguiente comando se pueden observar todas las zonas horarias soportadas por pytz
```python
for tz in pytz:
  print(tz)
```