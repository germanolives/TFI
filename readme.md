# Título

Tienda / CRUD

## Descripción

Programa de tienda que gestiona repuestos de automotores de distintas marcas. Este permite mantener el stock de productos, agregando uno nuevo, modificando sus valores o eliminándolos. El acceso a las distintas funcionalidades depende del perfil del usuario del sistema.

## Instalación

Para ingresar al sistema debe ejecutarse el archivo 'main.py'.
El usuario administrador, quien tiene todas las funcionalidades, se loguea con:
mail de usuario: '<perro@gmail.com>'
contraseña: 'perro'

## Esquema de módulos del programa

MAIN
    |→ LOGIN
            |→ PRINCIPAL
                        |→ MENU
                               |→ PRODUCTOS
                               |→ USUARIOS
                                           |→ DATABASE
                                           |→ INTERFAZ USUARIO
                                           |→ UTILIDADES
                                           |→ VALIDACIONES
                                           |→ VARIABLES

- MAIN: se cargan los usuarios desde la base de datos, se loguea el usuario y puede ejecutar el programa y al salir tiene la opción de volver a loguearse antes de salir definitivamente del crud o puede loguearse otro usuario
- LOGIN: de manera interactiva se valida un usuario dentro de una lista de usuarios, solamente devuelve usuario válido con mail y contraseña respaldada en base de datos, si el usuario es válido y hay más de 5 intentos de contraseña incorrectos, se bloquea ese usuario cambiándole la contraseña por una cadena aleatoria de caracteres.
- PRINCIPAL: constituyen los distintos bloques funcionales. El usuario que ingresa al sistema puede o no ser traqueado en todo su recorrido (generando un archivo .json o registros en una tabla en la base de datos. El usuario administrador quien tiene acceso a gestionar a los usuarios puede seleccionar estas posibilidades para cada usuario del sistema). El administrador y el supervisor pueden generar reporte de tiempo de uso en el sistema de los usuarios y también la cantidad de ventas realizadas entre un período de tiempo.
- MENU: cada bloque funcional del módulo PRINCIPAL está subdividido en varias funciones y subfunciones dentro de este módulo MENU.
- PRODUCTOS: módulo con las funciones relativas al manejo de productos.
- USUARIOS: módulo con las funciones relativas al manejo de usuarios.
- DATABASE: módulo con funciones que interactúan con la base de datos CRUD.db
- INTERFAZ USUARIO: módulo de funciones de salida en consola y generación de reportes en archivos .txt.
- UTILIDADES / VALIDACIONES / VARIABLES: módulos con funciones y variables utilizadas en los otros módulos.

## Uso

Hay cuatro(4) perfiles de usuario en el sistema:

- Administrador
- Supervisor
- Vendedor
- Consultas

El usuario 'administrador' tiene todo el acceso al sistema:

- Agregar un nuevo producto
- Visualización de productos y reporte de sotck entre valores dados
- Búsqueda de productos
- Actualización de productos
- Actualización de movimientos de productos (compras / ventas / ajustes)
- Eliminación de productos
- Mantenimiento (recuperación de productos eliminados / creación de backup de la base de datos (CRUD_BACKUP.db) / recuperación desde backup)
- Gestión de usuarios (visualización y modificación de datos del usuario / eliminación de usuarios / recuperación de usuarios eliminados / generación de reportes de tiempo de uso del sistema de los usuarios entre fechas especificadas / generación de reportes de ventas entre fechas dadas / eliminación de logs de los usuarios).

El usuario 'supervisor' varía del acceso al sistema del 'administrador' en que no puede:

- Acceder al menú de mantenimiento
- Dentro del menú de gestión de usuarios solamente puede generar los reportes de tiempo de uso y ventas de usuario pero excluyendo en esos informes los movimientos del 'administrador'

El usuario 'vendedor' tiene acceso a:

- Visualización de productos y reporte de sotck entre valores dados
- Búsqueda de productos
- Actualización de productos
- Actualización de movimientos de productos (compras / ventas / ajustes)

El usuario 'consultas' accede a:

- Visualización de productos y reporte de sotck entre valores dados
- Búsqueda de productos

## Ayuda

Los archivos:

- ayuda_modulo_database.py
- ayuda_modulo_interfaz_usuario.py
- ayuda_modulo_login.py
- ayuda_modulo_menu.py
- ayuda_modulo_principal.py
- ayuda_modulo_productos.py
- ayuda_modulo_usuarios.py
- ayuda_modulo_utilidades.py
- ayuda_modulo_validaciones.py

muestran al ejecutarse una breve descripción de lo que hacen las funciones de cada uno de esos módulos.

## Autor

Germán Matías Olives
Mail: <germanolives@gmail.com>
Comisión: 25009 / Talento Tech
