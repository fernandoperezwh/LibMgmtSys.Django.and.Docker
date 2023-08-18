# Django Biblioteca
Practica de libro "La guia definitiva de django" de Adrian Holovaty y Jacob Kaplan Mosss

## Instalacion 
### 1. Construir los servicios del proyecto con el comando
```bash
docker-compose up
```

### 2. Entrar al contenedor del servicio de nuestra aplicación llamada `backend` para hacer las migraciones de django
```bash
docker exec -it libmgmtsysdjangoanddocker_backend_1 sh 
```

#### 2.1 Dentro de nuestro contenedor ejecutar las migraciones de django con
```bash
python manage.py migrate
```

Podemos comprobar que la migracion fue generada entrando al contenedor de la base de datos
```bash
docker exec -it libmgmtsysdjangoanddocker_db_1 sh
```

Una vez dentro del contenedor, accedemos a mysql para poder ver las tablas que django genera.
```bash
mysql -u libmgmtsys_user -D libmgmtsys_db -p"libmgmtsys_password"
```

## Uso
- Realizar las migraciones con>: ```python manage.py migrate```
- Ejecutar la aplicación con: ```python manage.py runserver```