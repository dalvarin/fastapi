# fastapi

## Uso de dockerfile

Para que funcione la parte del compose.yaml que recarga el contenedor ante cambios en los ficheros.

En dos sesiones de terminal hay que lanzar dos comandos de docker compose

### Primera sesión

En esta tendremos la salida estándard para ver errores y demás. Y veremos la recarga del contenedor ante cambios.

```bash

$ docker compose watch up

```

### Segunda sesión

Esta es la que se encarga de la recarga del contenedor.

```bash

$ docker compose watch

```
