# Django Biblioteca

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

### 3. Hostea en tu equipo el dominio `libmgmtsys.com`

Edita el archivo `/etc/hosts/` y agrega la siguiente linea
```bash
127.0.0.1	libmgmtsys.com
```

### 4. Ingresa desde el navegador a `http://libmgmtsys.com/`
