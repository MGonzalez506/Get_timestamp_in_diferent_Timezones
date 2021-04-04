# Get_timestamp_in_diferent_Timezones
Normalmente es buena práctica almacenar en una base de datos el timestamp en UTC, sin embargo dependiendo de su zona horaria es útil convertir UTC a su Timezone determinado.

Primeramente instala la librería pytz con el comando **pip install pytz**, una librería sencilla de interpretar que permite entre muchas otras funciones, convertir timezones de una a otra.

Este código coloca la variable **UTC_Format**, para luego obtener el tiempo en UTC, luego una variable **CRC_Format** con el formato de la zona horaria donde usted se encuentra, como ejemplo está la zona horaria 'America/Regina' que respecto al UTC, son 6 horas menos. 

Con el siguiente comando puedes encontrar una lista completa de los timezones soportados por pytz:

```python
for tz in pytz:
  print(tz)
```

Y eso te generará toda una lista de timezones soportadas.
Adicionalmente en el siguiente link está un standard de las diferentes zonas horarias para que puedas buscar la zona horaria donde te encuentres.

[Base de datos de diferentes zonas horarias](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones)

Por último el código imprime en pantalla las zonas horarias, así como un formato específico si deseamos que se note la zona horaria en la que se está tomando cada timestamp.
