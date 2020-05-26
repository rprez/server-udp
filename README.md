# server-udp

## Descripción

Aplicación servidor de mensajes UDP. Almacena paquetes de mensajes envíados por los medidores de Antel-Ute

## Requisitos

### runtime
 Python 3.6 o +
### Dependencias
* sqlalchemy
* psycopg2-binary (Base de Datos ORACLE)
* cx_Oracle (Base de Datos PostGres)

## Configuración

### Variables de ambientes
* IP_ADDRESS - Dirección IP en la que escucha el server
* LISTER_PORT - Puerto en el que escucha el server
* PG_CONNECTION - Conexión a PostGres ej: postgres:postgres@172.17.0.3:5432/utenotificaciones
* ORA_CONNECTION - Conexión a Oracle ej: ute:ute@172.17.0.3:1521/ORCLCDB

### Oracle
Instalar el driver correspondiente a la versión desde:
* https://oracle.github.io/odpi/doc/installation.html#other-platforms


