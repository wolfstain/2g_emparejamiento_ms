# 2g_emparejamiento_ms dop

Microservicio encargado del emparejamiento para la aplicacion. Su funcion es generar la lista de posibles emparejamientos y hacer los emparejamientos correspondientes.

Se usa como lenguaje base **Python 3**, con el framework Django REST.

Como base de datos se usa PostgreSQL.

### Ejecución

En la carpeta del archivo ejecutar las siguientes instucciones:

1. Añadir ip del nodo al archivo dop_app/setting.py , en el arreglo ALLOWED_HOSTS.
2. Ejecutar `docker-compose build`
3. Ejecutar `docker-compose run web python3 manage.py makemigrations`.
4. Ejecutar `docker-compose run web python3 manage.py migrate`.
5. Ejecutar `docker-compose up`.
