import datetime
import sqlite3
from interfaz_usuario import mostrar_menu, opcion_menu, mensaje, mostrar_lista, mostrar_detalle_cambio_stock, mostrar_lista_eliminados, mostrar_lista_usuarios, mostrar_lista_usuarios_eliminados, mostrar_lista_usuarios_seleccion, imprimir_lista, opcion_menu_con_0, opcion_menu_2_con_0, imprimir_lista_dos_valores, reportar_tiempo_por_usuario_total_entrefechas, reportar_tiempo_usuarios_por_dia_entrefechas, reportar_ventas_por_usuario_por_dia_entrefechas, reportar_ventas_por_usuario_total_entrefechas, mostrar_productos_entre_cantidades_stock
from variables import lista_inicio_fin, lista_menu_principal, lista_menu_claves_producto, lista_menu_orden, perfiles_usuario, lista_menu_buscar, lista_si_no, lista_menu_claves_usuarios, lista_menu_usuarios, lista_menu_mantenimiento, lista_menu_eliminar, lista_menu_ver
from utilidades import ordenar_lista, crear_listas_valores, crear_listas_valores_dos_claves, clear_screen
from database import traer_id_producto_preex_desde_db, agregar_producto_db, recuperar_usuarios_eliminados_en_db, actualizar_usuario_en_db, eliminar_usuario_en_db, cargar_lista_con_id_desde_db_opcion, agregar_usuario_en_db, recuperar_movimientos_producto_en_db, recuperar_producto_eliminados_en_db, cargar_lista_con_id_desde_db, actualizar_item_producto_en_db, eliminar_producto_en_db, eliminar_movimientos_producto_en_db, iniciar_carga_productos_eliminados, traer_id_producto_desde_db, generar_reportes_ventas_en_db, generar_reportes_tiempo_usuario_en_db, generar_reporte_de_bajo_stock, eliminar_logs_usuario_en_db
from usuarios import agregar_usuario, editar_usuario, seguir_usuario
from productos import agregar_producto, encontrar_producto, buscar_codigo, actualizar_movimientos_producto, actualizar_atributos_producto ,buscar_producto_2, encontrar_producto_por_id, encontrar_producto_por_descripcion
from validaciones import validar_fecha



def menu_restriccion_de_acceso(msj):
    """Función que devuelve un valor booleano según sea la elección del usuario. Recibe una cadena de caracteres como argumento para mostrar un mensaje para que el usuario decida la ruta a seguir

    Args:
        msj (str): mensaje para tomar la decisión 

    Returns:
        (bool): valor booleano según decidió el usuario
    """
    clear_screen()
    mensaje(f"🛒   {msj.upper()}   ✕")
    mostrar_menu("   Menú [RAIZ] →", lista_inicio_fin, 1, 1, True, 1, "← Salir", "", "")
    match opcion_menu(2, "Ingresar DATOS"):
        case 1:
            clear_screen()
            bucle_menu_principal = True
        case 2:
            clear_screen()
            mensaje("🔚")
            bucle_menu_principal = False
    return bucle_menu_principal 


def menu_agregar_producto(productos, usuario, logs_usuario, id_autoinc):
    """Agrega un nuevo producto, si ese producto no existe previamente en la base de datos. Primero pasa ese nuevo registro a la base de datos y chequea que esos campos no existan en la misma. Trae de la BD el valor del id del producto, si ese valor es nulo entonces agrega ese nuevo producto y actualiza el id del producto con el valor del indice de la BD en la lista de diccionarios 'productos'. Se va registrando en la lista logs_usuario lo que va ocurriendo y esa lista de sucesos devuelva esta función junto con la variable entera id_autoinc.

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    bucle_menu_agregar = True
    while bucle_menu_agregar:
        mostrar_menu("   Menú [AGREGAR PRODUCTO] →", lista_menu_principal, 1, 1, True, 1, "Menú [PRINCIPAL]", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                clear_screen()
                mensaje("🛒   INGRESE PRODUCTO AL STOCK   →")
                nuevo_producto = agregar_producto()
                id_preex = traer_id_producto_preex_desde_db("crud", "productos", nuevo_producto)
                if id_preex:
                    etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"intento de agregar producto '{nuevo_producto["codigo"]} - {nuevo_producto["marca"]}': ya existe en stock ✕", id_producto=id_preex)
                    logs_usuario.append(etapa_usuario) 
                    clear_screen()
                    mensaje(f"🛒   PRODUCTO EXISTENTE EN STOCK   ✕")
                else:
                    agregar_producto_db("crud", "productos", nuevo_producto)                                                   
                    nuevo_producto.update({"id": traer_id_producto_desde_db("crud", "productos", nuevo_producto)})
                    productos.append(nuevo_producto)
                    etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"producto '{nuevo_producto["codigo"]} - {nuevo_producto["marca"]}' agregado ✓", id_producto=nuevo_producto["id"])
                    logs_usuario.append(etapa_usuario)                                             
                    clear_screen()
                    mensaje(f"🛒   PRODUCTO AGREGADO: '{nuevo_producto.get("codigo").upper()}' '{nuevo_producto.get("descripcion").upper()}'   ✓")
                    nuevo_producto_lista = []
                    nuevo_producto_lista.append(nuevo_producto)
                    mostrar_lista(nuevo_producto_lista)
                print("\n")
            case 2:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del menú agregar producto")
                logs_usuario.append(etapa_usuario)  
                bucle_menu_agregar = False
    return id_autoinc 


def submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, atributo_1, atributo_2="marca", atributo_3="codigo"):
    """Función que de acuerdo a su menú interactivo de opciones muestra en consola todos los productos por el atributo seleccionado (que recibe como parámetro). Ordena esa selección o puede regresar al menú anterior para seleccionar otro atributo, o bien al menú principal del programa saliendo del menú para ver el listado de productos

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
        atributo_1 (str): atributo seleccionado para mostrar por orden
        atributo_2 (str, optional): _description_. Defaults to "marca".
        atributo_3 (str, optional): _description_. Defaults to "codigo".

    Returns:
        bucle_menu_mostrar (bool): variable para retorno al menú ver
        bucle_menu_ver (bool): variable para retorno al menú principal
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    bucle_menu_ordenar = bucle_menu_mostrar = bucle_menu_ver = True                                   
    while bucle_menu_ordenar and bucle_menu_mostrar and bucle_menu_ver:
        mostrar_menu(f"  Menú [ORDENAR POR '{atributo_1.upper()}'] →", lista_menu_orden, 1, 2, True, 3, "Menú [MOSTRAR PRODUCTOS ORDENADOS POR →]", "Menú [VER PRODUCTOS]", "Menú [PRINCIPAL]")
        match opcion_menu(5, "Ingresar DATOS"):
            case 1:
                clear_screen()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"ingreso a muestra productos ordenados por {atributo_1} en forma ascendente")
                logs_usuario.append(etapa_usuario)
                mensaje(f"🛒   PRODUCTOS ORDENADOS POR {atributo_1.upper()} ↑   →")
                mostrar_lista(ordenar_lista(productos, atributo_1, atributo_2, atributo_3, True))
            case 2:
                clear_screen()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"ingreso a muestra productos ordenados por {atributo_1} en forma descendente")
                logs_usuario.append(etapa_usuario)
                mensaje(f"🛒   PRODUCTOS ORDENADOS POR {atributo_1.upper()} ↓   →")
                mostrar_lista(ordenar_lista(productos, atributo_1, atributo_2, atributo_3, False))
            case 3:
                clear_screen()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del submenú mostrar productos y vuelve al menú mostrar productos ordenados por el atributo de orden que se seleccione")
                logs_usuario.append(etapa_usuario) 
                bucle_menu_ordenar = False
            case 4:
                clear_screen()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"sale del submenú mostrar productos por {atributo_1}")
                logs_usuario.append(etapa_usuario) 
                bucle_menu_mostrar = False
            case 5:
                clear_screen()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"sale del submenú mostrar productos por {atributo_1} y vuelve al menú principal")
                logs_usuario.append(etapa_usuario)  
                bucle_menu_ver = False
    return bucle_menu_mostrar, bucle_menu_ver, id_autoinc 


def menu_ver_productos(productos, usuario, logs_usuario, id_autoinc):
    """Función que de acuerdo a su menú interactivo de opciones permite seleccionar el atributo que va a determinar el orden del listado de productos

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json. También genera un reporte de productos que tiene una cantidad en stock entre los valores que pasa el usuario.

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    bucle_menu_ver = True
    while bucle_menu_ver:
        mostrar_menu("   Menú [VER PRODUCTOS] →", lista_menu_ver, 1, 2, True, 1, "Menú [PRINCIPAL]", "", "")
        match opcion_menu(3, "Ingresar DATOS"):
            case 1:
                clear_screen()
                bucle_menu_mostrar = True
                while bucle_menu_mostrar and bucle_menu_ver:
                    mostrar_menu("   Menú [MOSTRAR PRODUCTOS ORDENADOS POR] →", lista_menu_claves_producto, 1, 12, True, 2, "Menú [VER PRODUCTOS]", "Menú [PRINCIPAL]", "")
                    match opcion_menu(14, "Ingresar DATOS"):
                        case 1:
                            bucle_menu_mostrar, bucle_menu_ver, id_autoinc  = submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, "id")
                        case 2:
                            bucle_menu_mostrar, bucle_menu_ver, id_autoinc  = submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, "descripcion")
                        case 3:
                            bucle_menu_mostrar, bucle_menu_ver, id_autoinc  = submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, "codigo", "marca", "descripcion")
                        case 4:
                            bucle_menu_mostrar, bucle_menu_ver, id_autoinc  = submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, "marca", "codigo", "descripcion")
                        case 5:
                            bucle_menu_mostrar, bucle_menu_ver, id_autoinc  = submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, "modelo")
                        case 6:
                            bucle_menu_mostrar, bucle_menu_ver, id_autoinc  = submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, "categoria")
                        case 7:
                            bucle_menu_mostrar, bucle_menu_ver, id_autoinc  = submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, "origen")
                        case 8:
                            bucle_menu_mostrar, bucle_menu_ver, id_autoinc  = submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, "ubicacion")
                        case 9:
                            bucle_menu_mostrar, bucle_menu_ver, id_autoinc  = submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, "precio")
                        case 10:
                            bucle_menu_mostrar, bucle_menu_ver, id_autoinc  = submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, "cantidad")
                        case 11:
                            bucle_menu_mostrar, bucle_menu_ver, id_autoinc  = submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, "fecha_modificacion")
                        case 12:
                            bucle_menu_mostrar, bucle_menu_ver, id_autoinc  = submenu_mostrar_productos(productos, usuario, logs_usuario, id_autoinc, "fecha_alta")
                        case 13:
                            clear_screen()
                            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del menú mostrar productos y vuelve al menú ver productos")
                            logs_usuario.append(etapa_usuario) 
                            bucle_menu_mostrar = False
                        case 14:
                            clear_screen()
                            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del menú ver productos y vuelve al menú principal")
                            logs_usuario.append(etapa_usuario) 
                            bucle_menu_ver = False
            case 2:
                clear_screen()
                mensaje("🛒   INGRESE LAS CANTIDADES (DESDE→HASTA) PARA GENERAR EL REPORTE  →")
                cantidad_desde = input(f"\n# Cantidad Mínima: ").strip().lower()
                while not cantidad_desde.isdigit() or int(cantidad_desde) < 0:
                    cantidad_desde = input(f"\n# Cantidad Mínima: ").strip().lower()
                cantidad_hasta = input(f"\n# Cantidad Máxima: ").strip().lower()
                while not cantidad_hasta.isdigit() or int(cantidad_hasta) < 0 or cantidad_hasta <= cantidad_desde:
                    cantidad_hasta = input(f"\n# Cantidad Máxima: ").strip().lower()
                consulta_stock = generar_reporte_de_bajo_stock("crud", "productos", cantidad_desde, cantidad_hasta)
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"genero reportes de productos con stock entre cantidades dadas")
                logs_usuario.append(etapa_usuario) 
                clear_screen()
                mostrar_productos_entre_cantidades_stock(consulta_stock, cantidad_desde, cantidad_hasta, usuario, fecha)
                print()
            case 3:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del menú ver productos y vuelve al menú principal")
                logs_usuario.append(etapa_usuario) 
                bucle_menu_ver = False
    return id_autoinc 


def submenu_buscar_producto_por_id(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que busca un producto por su id y muestra en consola con los movimientos que tenga

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    resultado_busqueda = encontrar_producto_por_id(productos)
    if resultado_busqueda:
        clear_screen()
        mensaje("🛒   PRODUCTO ENCONTRADO   ✓")
        mostrar_lista(resultado_busqueda)
        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"ingreso a mostrar el producto: '{resultado_busqueda[0]["id"]}'")
        logs_usuario.append(etapa_usuario)
        if resultado_busqueda[0]["ingreso"]:
            mensaje("🛒   MOVIMIENTOS DE COMPRA   ✓")
            mostrar_detalle_cambio_stock(resultado_busqueda[0]["ingreso"],"compra")
        if resultado_busqueda[0]["egreso"]:
            mensaje("🛒   MOVIMIENTOS DE VENTA   ✓")
            mostrar_detalle_cambio_stock(resultado_busqueda[0]["egreso"],"venta")
        if resultado_busqueda[0]["ajuste"]:
            mensaje("🛒   MOVIMIENTOS DE AJUSTE   ✓")
            mostrar_detalle_cambio_stock(resultado_busqueda[0]["ajuste"],"ajuste")
    return id_autoinc 


def submenu_buscar_producto_por_descripcion(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que busca un producto por su descripción y muestra en consola con los movimientos que tenga

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    resultado_busqueda = encontrar_producto(productos)
    if resultado_busqueda:
        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"ingreso a mostrar el producto: '{resultado_busqueda[0]["descripcion"]}'")
        logs_usuario.append(etapa_usuario)
        if resultado_busqueda[0]["ingreso"]:
            mensaje("🛒   MOVIMIENTOS DE COMPRA   ✓")
            mostrar_detalle_cambio_stock(resultado_busqueda[0]["ingreso"],"compra")
        if resultado_busqueda[0]["egreso"]:
            mensaje("🛒   MOVIMIENTOS DE VENTA   ✓")
            mostrar_detalle_cambio_stock(resultado_busqueda[0]["egreso"],"venta")
        if resultado_busqueda[0]["ajuste"]:
            mensaje("🛒   MOVIMIENTOS DE AJUSTE   ✓")
            mostrar_detalle_cambio_stock(resultado_busqueda[0]["ajuste"],"ajuste")
    return id_autoinc 


def submenu_buscar_producto_por_codigo_marca(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que busca un producto por su código-marca y muestra en consola con los movimientos que tenga

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    mensaje("🛒   BÚSQUEDA POR CÓDIGO DEL PRODUCTO   →")
    resultado_busqueda = buscar_codigo(productos)
    if resultado_busqueda:
        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"ingreso a mostrar el producto de '{resultado_busqueda[0].get("codigo").upper()} - {resultado_busqueda[0].get("marca").upper()}'")
        logs_usuario.append(etapa_usuario)
        if resultado_busqueda[0]["ingreso"]:
            mensaje("🛒   MOVIMIENTOS DE COMPRA   ✓")
            mostrar_detalle_cambio_stock(resultado_busqueda[0]["ingreso"],"compra")
        if resultado_busqueda[0]["egreso"]:
            mensaje("🛒   MOVIMIENTOS DE VENTA   ✓")
            mostrar_detalle_cambio_stock(resultado_busqueda[0]["egreso"],"venta")
        if resultado_busqueda[0]["ajuste"]:
            mensaje("🛒   MOVIMIENTOS DE AJUSTE   ✓")
            mostrar_detalle_cambio_stock(resultado_busqueda[0]["ajuste"],"ajuste")
    return id_autoinc


def submenu_buscar_producto_por_modelo_marca(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que busca un producto por su modelo-marca y muestra en consola con los movimientos que tenga

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    modelo_a_buscar = ""
    lista_modelos = crear_listas_valores_dos_claves(productos, "modelo", "marca")
    no_hay_modelo = True
    while len(modelo_a_buscar) == 0 or no_hay_modelo:
        clear_screen()
        mensaje("🛒   BÚSQUEDA DE PRODUCTOS POR MODELO / MARCA   →")
        imprimir_lista_dos_valores(lista_modelos, "Modelos en el Stock")
        modelo_a_buscar = input("\n• Modelo: ").strip().lower()
        for i in range(len(lista_modelos)):
            if modelo_a_buscar in lista_modelos[i]:
                no_hay_modelo = False
    marca_a_buscar = ""
    no_hay_marca = True
    while len(marca_a_buscar) == 0 or no_hay_marca:
        marca_a_buscar = input("\n• Marca: ").strip().lower()
        for i in range(len(lista_modelos)):
            if marca_a_buscar in lista_modelos[i] and modelo_a_buscar in lista_modelos[i]:
                no_hay_marca = False
    por_modelo = buscar_producto_2(productos, "modelo", modelo_a_buscar)
    if len(por_modelo) >= 1:
        por_marca = buscar_producto_2(por_modelo, "marca", marca_a_buscar)
        if len(por_marca) >= 1:
            clear_screen()
            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"ingreso a mostrar productos de: '{por_marca[0].get("marca").upper()} - {por_modelo[0].get("modelo").upper()}'")
            logs_usuario.append(etapa_usuario)
            mensaje(f"🛒   PRODUCTOS DEL MODELO '{por_marca[0].get("marca").upper()} {por_modelo[0].get("modelo").upper()}' ✓")
            mostrar_lista(ordenar_lista(por_marca, "modelo", "marca", "codigo", True))
            resultado_busqueda = por_marca
            if len(resultado_busqueda) == 1:
                if resultado_busqueda[0]["ingreso"]:
                    mensaje("🛒   MOVIMIENTOS DE COMPRA   ✓")
                    mostrar_detalle_cambio_stock(resultado_busqueda[0]["ingreso"],"compra")
                if resultado_busqueda[0]["egreso"]:
                    mensaje("🛒   MOVIMIENTOS DE VENTA   ✓")
                    mostrar_detalle_cambio_stock(resultado_busqueda[0]["egreso"],"venta")
                if resultado_busqueda[0]["ajuste"]:
                    mensaje("🛒   MOVIMIENTOS DE AJUSTE   ✓")
                    mostrar_detalle_cambio_stock(resultado_busqueda[0]["ajuste"],"ajuste")
        else:
            clear_screen()
            mensaje(f"🛒   MODELO INEXISTENTE PARA ESA MARCA  ✕")
    else:
        clear_screen()
        mensaje("🛒   MODELO INEXISTENTE   ✕")
    return id_autoinc


def submenu_buscar_producto_por_marca(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que busca un producto por su marca y muestra en consola con los movimientos que tenga

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    mensaje("🛒   BÚSQUEDA DE PRODUCTOS POR MARCA   →")
    marca_a_buscar = ""
    lista_marcas = crear_listas_valores(productos, "marca")
    while len(marca_a_buscar) == 0 or marca_a_buscar not in lista_marcas:
        clear_screen()
        mensaje("🛒   BÚSQUEDA DE PRODUCTOS POR MARCA   →")
        imprimir_lista(lista_marcas, "Marcas en el Stock")
        marca_a_buscar = input("\n• Marca: ").strip().lower()
        por_marca = buscar_producto_2(productos, "marca", marca_a_buscar)
        if len(por_marca) >= 1:
            clear_screen()
            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"ingreso a mostrar productos de: '{por_marca[0].get("marca").upper()}'")
            logs_usuario.append(etapa_usuario)
            mensaje(F"🛒   PRODUCTOS DE LA MARCA '{por_marca[0].get("marca").upper()}' ✓")
            mostrar_lista(ordenar_lista(por_marca, "marca", "codigo", "modelo", True))
            resultado_busqueda = por_marca
            if len(resultado_busqueda) == 1:
                if resultado_busqueda[0]["ingreso"]:
                    mensaje("🛒   MOVIMIENTOS DE COMPRA   ✓")
                    mostrar_detalle_cambio_stock(resultado_busqueda[0]["ingreso"],"compra")
                if resultado_busqueda[0]["egreso"]:
                    mensaje("🛒   MOVIMIENTOS DE VENTA   ✓")
                    mostrar_detalle_cambio_stock(resultado_busqueda[0]["egreso"],"venta")
                if resultado_busqueda[0]["ajuste"]:
                    mensaje("🛒   MOVIMIENTOS DE AJUSTE   ✓")
                    mostrar_detalle_cambio_stock(resultado_busqueda[0]["ajuste"],"ajuste")
        else:
            clear_screen()
            mensaje("🛒   MARCA INEXISTENTE   ✕")
    return id_autoinc


def submenu_buscar_producto_por_categoria(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que busca un producto por su categoría y muestra en consola con los movimientos que tenga

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    categoria_a_buscar = ""
    lista_categorias = crear_listas_valores(productos, "categoria")
    while len(categoria_a_buscar) == 0 or categoria_a_buscar not in lista_categorias:
        clear_screen()
        mensaje("🛒   BÚSQUEDA DE PRODUCTOS POR CATEGORÍA   →") 
        imprimir_lista(lista_categorias, "Categorías en el Stock")
        categoria_a_buscar = input("\n• Categoría: ").strip().lower()
        por_categoria = buscar_producto_2(productos, "categoria", categoria_a_buscar)
        if len(por_categoria) >= 1:
            clear_screen()
            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"ingreso a mostrar productos de la categoría '{por_categoria[0].get("categoria").upper()}'")
            logs_usuario.append(etapa_usuario)
            mensaje(f"🛒   PRODUCTOS DE LA CATEGORÍA '{por_categoria[0].get("categoria").upper()}' ✓")
            mostrar_lista(ordenar_lista(por_categoria, "categoria", "marca", "modelo", True))
            resultado_busqueda = por_categoria
            if len(resultado_busqueda) == 1:
                if resultado_busqueda[0]["ingreso"]:
                    mensaje("🛒   MOVIMIENTOS DE COMPRA   ✓")
                    mostrar_detalle_cambio_stock(resultado_busqueda[0]["ingreso"],"compra")
                if resultado_busqueda[0]["egreso"]:
                    mensaje("🛒   MOVIMIENTOS DE VENTA   ✓")
                    mostrar_detalle_cambio_stock(resultado_busqueda[0]["egreso"],"venta")
                if resultado_busqueda[0]["ajuste"]:
                    mensaje("🛒   MOVIMIENTOS DE AJUSTE   ✓")
                    mostrar_detalle_cambio_stock(resultado_busqueda[0]["ajuste"],"ajuste")
        else:
            clear_screen()
            mensaje("🛒   CATEGORÍA INEXISTENTE   ✕")
    return id_autoinc


def menu_buscar_producto(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que muestra al usuario las opciones de búsqueda de producto

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    bucle_menu_buscar = True
    while bucle_menu_buscar:
        mostrar_menu("   Menú [BUSCAR PRODUCTOS] →", lista_menu_buscar, 1, 6, True, 1, "Menú [PRINCIPAL]", "", "")
        match opcion_menu(7, "Ingresar DATOS"):
            case 1:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al submenú buscar productos por id")
                logs_usuario.append(etapa_usuario)
                id_autoinc = submenu_buscar_producto_por_id(productos, usuario, logs_usuario, id_autoinc)
            case 2:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al submenú buscar productos por descripción")
                logs_usuario.append(etapa_usuario)
                id_autoinc = submenu_buscar_producto_por_descripcion(productos, usuario, logs_usuario, id_autoinc)
            case 3:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al submenú buscar productos por código-marca")
                logs_usuario.append(etapa_usuario)
                id_autoinc = submenu_buscar_producto_por_codigo_marca(productos, usuario, logs_usuario, id_autoinc)              
            case 4:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al submenú buscar productos por modelo-marca")
                logs_usuario.append(etapa_usuario)
                id_autoinc = submenu_buscar_producto_por_modelo_marca(productos, usuario, logs_usuario, id_autoinc)
            case 5:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al submenú buscar productos por marca")
                logs_usuario.append(etapa_usuario)
                id_autoinc = submenu_buscar_producto_por_marca(productos, usuario, logs_usuario, id_autoinc)
            case 6:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al submenú buscar productos por categoría")
                logs_usuario.append(etapa_usuario)
                id_autoinc = submenu_buscar_producto_por_categoria(productos, usuario, logs_usuario, id_autoinc)
            case 7:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del menú buscar productos y vuelve al menú principal")
                logs_usuario.append(etapa_usuario)
                bucle_menu_buscar = False
    return id_autoinc 


def submenu_actualizar_producto_por_id(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que actualiza un producto por su id

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    mensaje("🛒   INGRESE PRODUCTO A ACTUALIZAR   →")                        
    producto_a_actualizar = encontrar_producto_por_id(productos)
    if producto_a_actualizar:
        clear_screen()
        mensaje("🛒   PRODUCTO ENCONTRADO   ✓")
        mostrar_lista(producto_a_actualizar)
        editar = True
        while editar:
            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"ingresar a actualizar producto: '{producto_a_actualizar[0].get("codigo")} - {producto_a_actualizar[0].get("marca")}'", id_producto=producto_a_actualizar[0].get("id"))
            logs_usuario.append(etapa_usuario)                              
            productos, id_autoinc, actualizado = actualizar_atributos_producto(productos, producto_a_actualizar, usuario, logs_usuario, id_autoinc)
            clear_screen()
            if actualizado:
                mensaje("🛒   PRODUCTO ACTUALIZADO   ✓")
            else:
                mensaje("🛒   PRODUCTO NO ACTUALIZADO   ✓")
            mostrar_lista(producto_a_actualizar)
            print("\n")
            mostrar_menu("   Menú [SEGUIR EDITANDO] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    clear_screen()
                    mensaje(f"🛒   EDICIÓN DEL PRODUCTO: '{producto_a_actualizar[0].get("codigo").upper()}' '{producto_a_actualizar[0].get("descripcion").upper()}'   →")
                    mostrar_lista(producto_a_actualizar)
                    editar = True
                case 2:
                    clear_screen()
                    editar = False
    return id_autoinc


def submenu_actualizar_producto_por_descripcion(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que actualiza un producto por su descripción

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    mensaje("🛒   INGRESE PRODUCTO A ACTUALIZAR   →")                        
    producto_a_actualizar = encontrar_producto_por_descripcion(productos)
    clear_screen()
    mensaje(f"🛒   EDICIÓN DEL PRODUCTO: '{producto_a_actualizar[0].get("codigo").upper()}' '{producto_a_actualizar[0].get("descripcion").upper()}'   →")
    mostrar_lista(producto_a_actualizar)
    if producto_a_actualizar:
        editar = True
        while editar:
            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"ingresar a actualizar producto: '{producto_a_actualizar[0].get("codigo")} - {producto_a_actualizar[0].get("marca")}'", id_producto=producto_a_actualizar[0].get("id"))
            logs_usuario.append(etapa_usuario)                              
            productos, id_autoinc, actualizado = actualizar_atributos_producto(productos, producto_a_actualizar, usuario, logs_usuario, id_autoinc)
            clear_screen()
            if actualizado:
                mensaje("🛒   PRODUCTO ACTUALIZADO   ✓")
            else:
                mensaje("🛒   PRODUCTO NO ACTUALIZADO   ✓")
            mostrar_lista(producto_a_actualizar)
            mostrar_menu("   Menú [SEGUIR EDITANDO] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    clear_screen()
                    mensaje(f"🛒   EDICIÓN DEL PRODUCTO: '{producto_a_actualizar[0].get("codigo").upper()}' '{producto_a_actualizar[0].get("descripcion").upper()}'   →")
                    mostrar_lista(producto_a_actualizar)
                    editar = True
                case 2:
                    clear_screen()
                    editar = False
    return id_autoinc


def submenu_actualizar_producto_por_codigo(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que actualiza un producto por su código-marca

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    clear_screen()
    mensaje("🛒   INGRESE PRODUCTO A ACTUALIZAR   →")                        
    producto_a_actualizar = buscar_codigo(productos)
    if producto_a_actualizar:
        editar = True
        while editar:
            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"ingresar a actualizar producto: '{producto_a_actualizar[0].get("codigo")} - {producto_a_actualizar[0].get("marca")}'", id_producto=producto_a_actualizar[0].get("id"))
            logs_usuario.append(etapa_usuario)                              
            productos, id_autoinc, actualizado = actualizar_atributos_producto(productos, producto_a_actualizar, usuario, logs_usuario, id_autoinc)
            clear_screen()
            if actualizado:
                mensaje("🛒   PRODUCTO ACTUALIZADO   ✓")
            else:
                mensaje("🛒   PRODUCTO NO ACTUALIZADO   ✓")
            mostrar_lista(producto_a_actualizar)
            mostrar_menu("   Menú [SEGUIR EDITANDO] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    clear_screen()
                    mensaje(f"🛒   EDICIÓN DEL PRODUCTO: '{producto_a_actualizar[0].get("codigo").upper()}' '{producto_a_actualizar[0].get("descripcion").upper()}'   →")
                    mostrar_lista(producto_a_actualizar)
                    editar = True
                case 2:
                    clear_screen()
                    editar = False
    return id_autoinc


def submenu_actualizar_producto_por_marca(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que actualiza un producto por su marca

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    marca_a_actualizar = ""
    lista_productos_nueva_marca = []
    lista_marcas = crear_listas_valores(productos, "marca")
    while len(marca_a_actualizar) == 0 or marca_a_actualizar not in lista_marcas:
        clear_screen()
        mensaje("🛒   INGRESE LA MARCA DE PRODUCTOS A ACTUALIZAR   →")
        imprimir_lista(lista_marcas, "Marcas en el Stock")
        marca_a_actualizar = input("\n• Marca: ").strip().lower()
    marca_actualizada = ""
    while len(marca_actualizada) == 0:
        marca_actualizada = input("\n• Nueva Marca: ").strip().lower()
    c = 0
    for i in productos:
        if i.get("marca") == marca_a_actualizar:
            i.update({"marca": marca_actualizada})
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            i.update({"fecha_modificacion": fecha})
            lista_productos_nueva_marca.append(i.get("id"))
            c += 1
    if c > 0:
        for i in range(len(lista_productos_nueva_marca)):
            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"producto cambia de marca '{marca_a_actualizar.upper()}' a '{marca_a_actualizar.upper()}'", id_producto=lista_productos_nueva_marca[i])
            logs_usuario.append(etapa_usuario)
        actualizar_item_producto_en_db("crud", "productos", lista_productos_nueva_marca, "marca", marca_actualizada)
        clear_screen()
        mensaje(f"MARCA ACTUALIZADA ✓ \n{marca_a_actualizar.upper()} cambia a {marca_actualizada.upper()}")
    else:
        clear_screen()
        mensaje("🛒   MARCA INEXISTENTE   ✕")
    return id_autoinc


def submenu_actualizar_producto_por_modelo(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que actualiza un producto por su modelo-marca

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    modelo_a_actualizar = ""
    lista_productos_nuevo_modelo_marca = []
    lista_modelos = crear_listas_valores_dos_claves(productos, "modelo", "marca")
    no_hay_modelo = True
    while len(modelo_a_actualizar) == 0 or no_hay_modelo:
        clear_screen()
        mensaje("🛒   INGRESE MODELO DE UNA MARCA A ACTUALIZAR   →")
        imprimir_lista_dos_valores(lista_modelos, "Modelos en el Stock")
        modelo_a_actualizar = input("\n• Modelo: ").strip().lower()
        for i in range(len(lista_modelos)):
            if modelo_a_actualizar in lista_modelos[i]:
                no_hay_modelo = False
    marca_a_actualizar = ""
    no_hay_marca = True
    while len(marca_a_actualizar) == 0 or no_hay_marca:
        marca_a_actualizar = input("\n• Marca: ").strip().lower()
        for i in range(len(lista_modelos)):
            if marca_a_actualizar in lista_modelos[i] and modelo_a_actualizar in lista_modelos[i]:
                no_hay_marca = False
    modelo_actualizado = ""
    while len(modelo_actualizado) == 0:
        modelo_actualizado = input("\n\n• Nuevo Modelo: ").strip().lower()
    c = 0
    for i in productos:
        if i.get("modelo") == modelo_a_actualizar and i.get("marca") == marca_a_actualizar:
            i.update({"modelo": modelo_actualizado})
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            i.update({"fecha_modificacion": fecha})
            lista_productos_nuevo_modelo_marca.append(i.get("id"))
            c += 1
    if c > 0:
        for i in range(len(lista_productos_nuevo_modelo_marca)):
            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"producto cambia de marca-modelo '{marca_a_actualizar.upper()} {modelo_a_actualizar.upper()}' a '{marca_a_actualizar.upper()} {modelo_actualizado.upper()}'", id_producto=lista_productos_nuevo_modelo_marca[i])
            logs_usuario.append(etapa_usuario)
        actualizar_item_producto_en_db("crud", "productos", lista_productos_nuevo_modelo_marca, "modelo", modelo_actualizado)
        clear_screen()
        mensaje(f"🛒   MODELO ACTUALIZADO   ✓ \n{marca_a_actualizar.upper()} {modelo_a_actualizar.upper()} cambia a {marca_a_actualizar.upper()} {modelo_actualizado.upper()}")
    else:
        clear_screen()
        mensaje(f"🛒   MODELO '{modelo_a_actualizar.upper()}' INEXISTENTE PARA LA MARCA '{marca_a_actualizar.upper()}'  ✕")
    return id_autoinc


def submenu_actualizar_producto_por_categoria(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que actualiza un producto por su categoría

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    categoria_a_actualizar = ""
    lista_productos_nueva_categoria = []
    lista_categorias = crear_listas_valores(productos, "categoria")
    while len(categoria_a_actualizar) == 0 or categoria_a_actualizar not in lista_categorias:
        clear_screen()
        mensaje("🛒   INGRESE CATEGORÍA A ACTUALIZAR   →") 
        imprimir_lista(lista_categorias, "Categorías en el Stock")
        categoria_a_actualizar = input("\n• Categoría: ").strip().lower()
    categoria_actualizada = ""
    while len(categoria_actualizada) == 0:
        categoria_actualizada = input("\n• Nueva Categoría: ").strip().lower()
    c = 0
    for i in productos:
        if i.get("categoria") == categoria_a_actualizar:
            i.update({"categoria": categoria_actualizada})
            fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            i.update({"fecha_modificacion": fecha})
            lista_productos_nueva_categoria.append(i.get("id"))
            c += 1
    if c > 0:
        for i in range(len(lista_productos_nueva_categoria)):
            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"producto cambia de categoría '{categoria_a_actualizar.upper()}' a '{categoria_actualizada.upper()}'", id_producto=lista_productos_nueva_categoria[i])
            logs_usuario.append(etapa_usuario)
        actualizar_item_producto_en_db("crud", "productos", lista_productos_nueva_categoria, "categoria", categoria_actualizada)
        clear_screen()
        mensaje(f"🛒   CATEGORÍA ACTUALIZADA   ✓ \n{categoria_a_actualizar.upper()} cambia a {categoria_actualizada.upper()}")
    else:
        clear_screen()
        mensaje("🛒   CATEGORÍA INEXISTENTE   ✕")
    return id_autoinc


def menu_actualizar_producto(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que muestra al usuario las opciones de actualización de un producto

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """   
    clear_screen()
    bucle_menu_actualizar = True
    while bucle_menu_actualizar:
        mostrar_menu("   Menú [ACTUALIZAR PRODUCTOS] →", lista_menu_claves_producto, 1, 6, True, 1, "Menú [PRINCIPAL]", "", "")
        match opcion_menu(7, "Ingresar DATOS"):
            case 1:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al submenú actualizar producto por id")
                logs_usuario.append(etapa_usuario)
                id_autoinc = submenu_actualizar_producto_por_id(productos, usuario, logs_usuario, id_autoinc)
            case 2:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al submenú actualizar producto por descripción")
                logs_usuario.append(etapa_usuario)
                id_autoinc = submenu_actualizar_producto_por_descripcion(productos, usuario, logs_usuario, id_autoinc)
            case 3:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al submenú actualizar producto por código")
                logs_usuario.append(etapa_usuario)
                id_autoinc = submenu_actualizar_producto_por_codigo(productos, usuario, logs_usuario, id_autoinc)
            case 4:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al submenú actualizar producto por marca")
                logs_usuario.append(etapa_usuario)
                id_autoinc = submenu_actualizar_producto_por_marca(productos, usuario, logs_usuario, id_autoinc)
            case 5:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al submenú actualizar producto por modelo")
                logs_usuario.append(etapa_usuario)
                id_autoinc = submenu_actualizar_producto_por_modelo(productos, usuario, logs_usuario, id_autoinc)
            case 6:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al submenú actualizar producto por categoría")
                logs_usuario.append(etapa_usuario)
                id_autoinc = submenu_actualizar_producto_por_categoria(productos, usuario, logs_usuario, id_autoinc)
            case 7:
                clear_screen()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del menú actualizar producto")
                logs_usuario.append(etapa_usuario)
                bucle_menu_actualizar = False
    return id_autoinc


def submenu_actualizar_movimientos_producto(productos, producto_a_actualizar, usuario, logs_usuario, id_autoinc):
    """Función que permite actualizar los movimientos de un producto determinado

    Args:
        productos (list): lista de productos
        producto_a_actualizar (list): producto a actualizar
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """
    if producto_a_actualizar:
        editar = True
        while editar:
            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"ingresar a actualizar movimiento de producto: '{producto_a_actualizar[0].get("codigo")} - {producto_a_actualizar[0].get("marca")}'", id_producto=producto_a_actualizar[0].get("id"))
            logs_usuario.append(etapa_usuario)                              
            productos, id_autoinc, actualizado = actualizar_movimientos_producto(productos, producto_a_actualizar, usuario, logs_usuario, id_autoinc)
            clear_screen()
            if actualizado:
                mensaje("🛒   PRODUCTO ACTUALIZADO   ✓")
            else:
                mensaje("🛒   PRODUCTO NO ACTUALIZADO   ✓")
            mostrar_lista(producto_a_actualizar)
            print("\n")
            mostrar_menu("   Menú [SEGUIR EDITANDO] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    clear_screen()
                    mensaje(f"🛒   EDICIÓN DEL PRODUCTO: '{producto_a_actualizar[0].get("codigo").upper()}' '{producto_a_actualizar[0].get("descripcion").upper()}'   →")
                    mostrar_lista(producto_a_actualizar)
                    editar = True
                case 2:
                    clear_screen()
                    editar = False
    return id_autoinc


def menu_actualizar_movimientos_producto(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que muestra al usuario las opciones de búsqueda de un producto para su actualización

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """   
    clear_screen()
    bucle_menu_actualizar = True
    while bucle_menu_actualizar:
        mostrar_menu("   Menú [ACTUALIZAR MOVIMIENTOS DE PRODUCTO] →", lista_menu_claves_producto, 1, 3, True, 1, "Menú [PRINCIPAL]", "", "")
        match opcion_menu(4, "Ingresar DATOS"):
            case 1:
                clear_screen()
                mensaje("🛒   INGRESE PRODUCTO A ACTUALIZAR   →")                        
                producto_a_actualizar = encontrar_producto_por_id(productos)
                id_autoinc = submenu_actualizar_movimientos_producto(productos, producto_a_actualizar, usuario, logs_usuario, id_autoinc)
            case 2:
                clear_screen()
                mensaje("🛒   INGRESE PRODUCTO A ACTUALIZAR   →")                        
                producto_a_actualizar = encontrar_producto_por_descripcion(productos)
                id_autoinc = submenu_actualizar_movimientos_producto(productos, producto_a_actualizar, usuario, logs_usuario, id_autoinc)
            case 3:
                clear_screen()
                mensaje("🛒   INGRESE PRODUCTO A ACTUALIZAR   →")                        
                producto_a_actualizar = buscar_codigo(productos)
                id_autoinc = submenu_actualizar_movimientos_producto(productos, producto_a_actualizar, usuario, logs_usuario, id_autoinc)
            case 4:
                clear_screen()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del menú actualizar movimientos producto")
                logs_usuario.append(etapa_usuario)
                bucle_menu_actualizar = False
    return id_autoinc


def submenu_eliminar_producto_por_id(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que permite al usuario eliminar un producto por su id, actualizando la base de datos de dicho producto y sus movimientos

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """  
    bucle_producto_codigo = True
    clear_screen()
    mensaje("🛒   INGRESE PRODUCTO A ELIMINAR DEL STOCK   →")
    while bucle_producto_codigo:
        producto_encontrado = encontrar_producto_por_id(productos)
        if producto_encontrado:
            clear_screen()
            mensaje(f"🛒   ELIMINACIÓN DEL PRODUCTO: '{producto_encontrado[0].get("codigo").upper()}' '{producto_encontrado[0].get("id")}'   →")
            mostrar_lista(producto_encontrado)
            print()                         
            mostrar_menu(f"   Menú [CONFIRMAR ELIMINACIÓN PRODUCTO '{producto_encontrado[0].get("codigo").upper()}'] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    for i in productos:
                        for j in producto_encontrado:
                            if i == j:
                                i.update({"estado": False})
                                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"producto eliminado: '({i.get("codigo")} - {i.get("marca")})'", id_producto=i.get("id"))
                                logs_usuario.append(etapa_usuario)
                    lista_productos_a_eliminar = []
                    productos_copia = productos[:]
                    for i in productos_copia:
                        if i.get("estado") == False:
                            lista_productos_a_eliminar.append(i["id"])
                            productos.remove(i)
                    eliminar_producto_en_db("crud", "productos", lista_productos_a_eliminar)
                    eliminar_movimientos_producto_en_db("crud", "ingresos", lista_productos_a_eliminar)
                    eliminar_movimientos_producto_en_db("crud", "egresos", lista_productos_a_eliminar)
                    eliminar_movimientos_producto_en_db("crud", "ajustes", lista_productos_a_eliminar)
                    clear_screen()
                    mensaje("🛒   PRODUCTO ELIMINADO   ✓")
                    bucle_producto_codigo = False                                
                case 2:
                    clear_screen()
                    bucle_producto_codigo = False
        else:
            mostrar_menu("   Menú [VOLVER A BUSCAR] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    clear_screen()
                case 2:
                    clear_screen()
                    bucle_producto_codigo = False
    return id_autoinc


def submenu_eliminar_producto_por_descripcion(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que permite al usuario eliminar un producto por su descripción, actualizando la base de datos de dicho producto y sus movimientos

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """  
    bucle_producto_codigo = True
    clear_screen()
    mensaje("🛒   INGRESE PRODUCTO A ELIMINAR DEL STOCK   →")
    while bucle_producto_codigo:
        producto_encontrado = encontrar_producto_por_descripcion(productos)
        if producto_encontrado:
            clear_screen()
            mensaje(f"🛒   ELIMINACIÓN DEL PRODUCTO: '{producto_encontrado[0].get("codigo").upper()}' '{producto_encontrado[0].get("descripcion").upper()}'   →")
            mostrar_lista(producto_encontrado)
            print()                         
            mostrar_menu(f"   Menú [CONFIRMAR ELIMINACIÓN PRODUCTO '{producto_encontrado[0].get("codigo").upper()}'] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    for i in productos:
                        for j in producto_encontrado:
                            if i == j:
                                i.update({"estado": False})
                                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"producto eliminado: '({i.get("codigo")} - {i.get("marca")})'", id_producto=i.get("id"))
                                logs_usuario.append(etapa_usuario)
                    lista_productos_a_eliminar = []
                    productos_copia = productos[:]
                    for i in productos_copia:
                        if i.get("estado") == False:
                            lista_productos_a_eliminar.append(i["id"])
                            productos.remove(i)
                    eliminar_producto_en_db("crud", "productos", lista_productos_a_eliminar)
                    eliminar_movimientos_producto_en_db("crud", "ingresos", lista_productos_a_eliminar)
                    eliminar_movimientos_producto_en_db("crud", "egresos", lista_productos_a_eliminar)
                    eliminar_movimientos_producto_en_db("crud", "ajustes", lista_productos_a_eliminar)
                    clear_screen()
                    mensaje("🛒   PRODUCTO ELIMINADO   ✓")
                    bucle_producto_codigo = False                                
                case 2:
                    clear_screen()
                    bucle_producto_codigo = False
        else:
            mostrar_menu("   Menú [VOLVER A BUSCAR] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    clear_screen()
                case 2:
                    clear_screen()
                    bucle_producto_codigo = False
    return id_autoinc


def submenu_eliminar_producto_por_codigo(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que permite al usuario eliminar un producto por su código-marca, actualizando la base de datos de dicho producto y sus movimientos

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """  
    bucle_producto_codigo = True
    clear_screen()
    mensaje("🛒   INGRESE PRODUCTO A ELIMINAR DEL STOCK   →")
    while bucle_producto_codigo:
        producto_encontrado = buscar_codigo(productos)
        if producto_encontrado:
            clear_screen()
            mensaje(f"🛒   ELIMINACIÓN DEL PRODUCTO: '{producto_encontrado[0].get("codigo").upper()}' '{producto_encontrado[0].get("descripcion").upper()}'   →")
            mostrar_lista(producto_encontrado)
            print()                         
            mostrar_menu(f"   Menú [CONFIRMAR ELIMINACIÓN PRODUCTO '{producto_encontrado[0].get("codigo").upper()}'] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    for i in productos:
                        for j in producto_encontrado:
                            if i == j:
                                i.update({"estado": False})
                                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"producto eliminado: '({i.get("codigo")} - {i.get("marca")})'", id_producto=i.get("id"))
                                logs_usuario.append(etapa_usuario)
                    lista_productos_a_eliminar = []
                    productos_copia = productos[:]
                    for i in productos_copia:
                        if i.get("estado") == False:
                            lista_productos_a_eliminar.append(i["id"])
                            productos.remove(i)
                    eliminar_producto_en_db("crud", "productos", lista_productos_a_eliminar)
                    eliminar_movimientos_producto_en_db("crud", "ingresos", lista_productos_a_eliminar)
                    eliminar_movimientos_producto_en_db("crud", "egresos", lista_productos_a_eliminar)
                    eliminar_movimientos_producto_en_db("crud", "ajustes", lista_productos_a_eliminar)
                    clear_screen()
                    mensaje("🛒   PRODUCTO ELIMINADO   ✓")
                    bucle_producto_codigo = False                                
                case 2:
                    clear_screen()
                    bucle_producto_codigo = False
        else:
            mostrar_menu("   Menú [VOLVER A BUSCAR] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    clear_screen()
                case 2:
                    clear_screen()
                    bucle_producto_codigo = False
    return id_autoinc


def submenu_eliminar_productos_de_una_marca(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que permite al usuario eliminar todos los productos de una marca seleccionada, actualizando la base de datos de dichos productos y sus movimientos

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """  
    marca_valida = ""
    lista_marcas = crear_listas_valores(productos, "marca")
    while len(marca_valida) == 0 or marca_valida not in lista_marcas:
        clear_screen()
        mensaje("🛒   INGRESE LA MARCA DE PRODUCTOS A ELIMINAR   →")
        imprimir_lista(lista_marcas, "Marcas en el Stock")
        marca_valida = input("\n• Marca: ").strip().lower()
    print("\n")
    marca = buscar_producto_2(productos, "marca", marca_valida)
    if len(marca) > 0:
        clear_screen()
        mostrar_menu(f"   Menú [CONFIRMAR ELIMINACIÓN DE LA MARCA '{marca_valida.upper()}'] →", lista_si_no, 1, 2, True, 0, "", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                for i in productos:
                    for j in marca:
                        if i == j:
                            i.update({"estado": False})
                            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"producto eliminado: '({i.get("codigo")} - {i.get("marca")})'", id_producto=i.get("id"))
                            logs_usuario.append(etapa_usuario)
                lista_productos_a_eliminar = []
                productos_copia = productos[:]
                for i in productos_copia:
                    if i.get("estado") == False:
                        lista_productos_a_eliminar.append(i["id"])
                        productos.remove(i)
                eliminar_producto_en_db("crud", "productos", lista_productos_a_eliminar)
                eliminar_movimientos_producto_en_db("crud", "ingresos", lista_productos_a_eliminar)
                eliminar_movimientos_producto_en_db("crud", "egresos", lista_productos_a_eliminar)
                eliminar_movimientos_producto_en_db("crud", "ajustes", lista_productos_a_eliminar)
                mensaje("🛒   MARCA ELIMINADA   ✓")
            case 2:
                clear_screen()
    return id_autoinc


def submenu_eliminar_productos_de_un_modelo_marca(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que permite al usuario eliminar todos los productos de un modelo de una marca seleccionada, actualizando la base de datos de dichos productos y sus movimientos

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """  
    modelo_valido = ""
    lista_modelos = crear_listas_valores_dos_claves(productos, "modelo", "marca")
    no_hay_modelo = True
    while len(modelo_valido) == 0 or no_hay_modelo:
        clear_screen()
        mensaje("🛒   INGRESE MODELO DE UNA MARCA A ELIMINAR   →")
        imprimir_lista_dos_valores(lista_modelos, "Modelos en el Stock")
        modelo_valido = input("\n• Modelo: ").strip().lower()
        for i in range(len(lista_modelos)):
            if modelo_valido in lista_modelos[i]:
                no_hay_modelo = False
    marca_valida = ""
    no_hay_marca = True
    while len(marca_valida) == 0 or no_hay_marca:
        marca_valida = input("\n• Marca: ").strip().lower()
        for i in range(len(lista_modelos)):
            if marca_valida in lista_modelos[i] and modelo_valido in lista_modelos[i]:
                no_hay_marca = False
    marca = buscar_producto_2(productos, "marca", marca_valida)
    if len(marca) > 0:
        modelo = buscar_producto_2(marca, "modelo", modelo_valido)
        if len(modelo) > 0:
            clear_screen()
            mostrar_menu(f"   Menú [CONFIRMAR ELIMINACIÓN DEL MODELO '{marca_valida.upper()} {modelo_valido.upper()}'] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    for i in productos:
                        for j in modelo:
                            if i == j:
                                i.update({"estado": False})
                                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"producto eliminado: '({i.get("codigo")} - {i.get("marca")})'", id_producto=i.get("id"))
                                logs_usuario.append(etapa_usuario)
                    lista_productos_a_eliminar = []
                    productos_copia = productos[:]
                    for i in productos_copia:
                        if i.get("estado") == False:
                            lista_productos_a_eliminar.append(i["id"])
                            productos.remove(i)
                    eliminar_producto_en_db("crud", "productos", lista_productos_a_eliminar)
                    eliminar_movimientos_producto_en_db("crud", "ingresos", lista_productos_a_eliminar)
                    eliminar_movimientos_producto_en_db("crud", "egresos", lista_productos_a_eliminar)
                    eliminar_movimientos_producto_en_db("crud", "ajustes", lista_productos_a_eliminar)
                    mensaje("🛒   MODELO ELIMINADO   ✓")
                case 2:
                    clear_screen()
    return id_autoinc


def menu_eliminar_producto(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que muestra al usuario las opciones de eliminación de un producto/productos

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """    
    clear_screen()
    bucle_menu_eliminar = True
    while bucle_menu_eliminar:
        mostrar_menu("  Menú [ELIMINAR PRODUCTOS] →", lista_menu_eliminar, 1, 5, True, 1, "Menú [PRINCIPAL]", "", "")
        match opcion_menu(6, "Ingresar DATOS"):
            case 1:
                id_autoinc = submenu_eliminar_producto_por_id(productos, usuario, logs_usuario, id_autoinc)
            case 2:
                id_autoinc = submenu_eliminar_producto_por_descripcion(productos, usuario, logs_usuario, id_autoinc)
            case 3:
                id_autoinc = submenu_eliminar_producto_por_codigo(productos, usuario, logs_usuario, id_autoinc)
            case 4:
                id_autoinc = submenu_eliminar_productos_de_una_marca(productos, usuario, logs_usuario, id_autoinc)
            case 5:
                id_autoinc = submenu_eliminar_productos_de_un_modelo_marca(productos, usuario, logs_usuario, id_autoinc)
            case 6: #opción para salir del menú eliminar
                clear_screen()
                bucle_menu_eliminar = False
    return id_autoinc


def submenu_gestionar_productos_eliminados(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que permite mostrar al usuario los productos eliminados y poder recuperarlos con sus movimientos

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """   
    clear_screen()
    productos_eliminados = iniciar_carga_productos_eliminados()
    if productos_eliminados:
        mensaje("🛒   LISTA DE PRODUCTOS ELIMINADOS   ↓")
        mostrar_lista_eliminados(ordenar_lista(productos_eliminados, "fecha_baja", "marca", "modelo", False))
        print("\n")
        mostrar_menu("   Menú [RECUPERAR PRODUCTOS] →", lista_si_no, 1, 2, True, 0, "", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                clear_screen()
                lista_productos_eliminados_a_recuperar = []
                for i in productos_eliminados:
                    etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"producto recuperado: '({i.get("codigo")} - {i.get("marca")})'", id_producto=i.get("id"))
                    logs_usuario.append(etapa_usuario)
                    lista_productos_eliminados_a_recuperar.append((i["id"], i["cantidad"]))
                productos.extend(productos_eliminados)
                productos_eliminados.clear()
                recuperar_producto_eliminados_en_db("crud", "productos", lista_productos_eliminados_a_recuperar)
                recuperar_movimientos_producto_en_db("crud", "ingresos", lista_productos_eliminados_a_recuperar)
                recuperar_movimientos_producto_en_db("crud", "egresos", lista_productos_eliminados_a_recuperar)
                recuperar_movimientos_producto_en_db("crud", "ajustes", lista_productos_eliminados_a_recuperar)
                clear_screen()
                mensaje("🛒   PRODUCTOS RECUPERADOS   ✓")
            case 2:
                clear_screen()
    else:
        clear_screen()
        mensaje("🛒   NO HAY PRODUCTOS ELIMINADOS   →")
        print("\n")
    return id_autoinc


def submenu_crear_un_backup(usuario, logs_usuario, id_autoinc):
    """Función que crea un backup de la base de datos

    Args:
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """   
    clear_screen()
    mostrar_menu("   Menú [CREA UN BACKUP DE LA BASE DE DATOS] →", lista_si_no, 1, 2, True, 0, "", "", "")
    match opcion_menu(2, "Ingresar DATOS"):
        case 1:
            try:
                conexion_original = sqlite3.connect('crud.db')
                conexion_backup = sqlite3.connect('crud_backup.db')
                try:
                    conexion_original.execute('''BEGIN TRANSACTION''')
                    conexion_original.backup(conexion_backup)
                    conexion_original.commit()
                except:
                    conexion_original.rollback()
            except sqlite3.Error as error:
                mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN ✕')
            finally:
                if conexion_backup:
                    conexion_backup.close()
                if conexion_original:
                    conexion_original.close()
            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"backup realizado")
            logs_usuario.append(etapa_usuario)
            clear_screen()
            mensaje(f"🛒   BACKUP REALIZADO   ✓")
            print("\n")
        case 2:
            clear_screen()
    return id_autoinc


def submenu_volver_desde_backup(usuario, logs_usuario, id_autoinc):
    """Función que recupera la base de datos desde un backup previamente creado

    Args:
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """   
    if cargar_lista_con_id_desde_db("crud_backup", "productos"):
        clear_screen()
        mensaje(f"🛒   VOLVER A BACKUP   →")
        mostrar_menu("   Menú [CONFIRMAR OPERACIÓN] →", lista_si_no, 1, 2, True, 0, "", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                try:
                    conexion_backup = sqlite3.connect('crud_backup.db')
                    conexion_original = sqlite3.connect('crud.db')
                    try:
                        conexion_backup.execute('''BEGIN TRANSACTION''')
                        conexion_backup.backup(conexion_original)
                        conexion_backup.commit()
                    except:
                        conexion_backup.rollback()
                except sqlite3.Error as error:
                    mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN ✕')
                finally:
                    if conexion_original:
                        conexion_original.close()
                    if conexion_backup:
                        conexion_backup.close()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"base de datos recuperada desde backup")
                logs_usuario.append(etapa_usuario)
                clear_screen()
                mensaje(f"🛒   BASE DE DATOS RECUPERADA  ✓")
                print("\n")
            case 2:
                clear_screen()
    else:
        clear_screen()
        mensaje(f"🛒   NO HAY BACKUP REALIZADO  ✕")
    return id_autoinc


def menu_mantenimiento(productos, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que muestra al usuario las opciones de mantenimiento de productos (recuperar productos eliminados, crear backup y volver desde backup)

    Args:
        productos (list): lista de productos
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """    
    clear_screen()
    bucle_menu_mantenimiento = True
    while bucle_menu_mantenimiento:
        mostrar_menu("   Menú [MANTENIMIENTO DEL STOCK] →", lista_menu_mantenimiento, 1, 3, True, 1, "Menú [PRINCIPAL]", "", "")
        match opcion_menu(4, "Ingresar DATOS"):
            case 1:
                id_autoinc = submenu_gestionar_productos_eliminados(productos, usuario, logs_usuario, id_autoinc)
            case 2:
                id_autoinc = submenu_crear_un_backup(usuario, logs_usuario, id_autoinc)
            case 3:
                id_autoinc = submenu_volver_desde_backup(usuario, logs_usuario, id_autoinc)
            case 4: # Volver al Menú [PRINCIPAL]
                clear_screen()
                bucle_menu_mantenimiento = False
    return id_autoinc


def submenu_ver_usuarios_del_sistema(usuarios, usuario, logs_usuario, id_autoinc):
    """Función que muestra al usuario 'administrador' un listado de usuarios del sistema

    Args:
        usuarios (list): lista de usuarios
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        _type_: _description_
    """
    clear_screen()
    mensaje("🛒   LISTADO DE USUARIOS   →")
    etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso a ver usuarios del sistema")
    logs_usuario.append(etapa_usuario)
    mostrar_lista_usuarios(ordenar_lista(usuarios, "perfil_acceso", "mail", "id", True))
    print("\n")
    return id_autoinc


def submenu_agregar_usuario_al_sistema(usuarios, usuario, logs_usuario, id_autoinc):
    """Agrega un nuevo usuario, si ese usuario no existe previamente en la base de datos. Primero pasa ese nuevo registro a la base de datos y chequea que esos campos no existan en la misma. Trae de la BD el valor del id del usuario, si ese valor es nulo entonces agrega ese nuevo usuario y actualiza el id del usuario con el valor del indice de la BD en la lista de diccionarios 'usuarios'. Se va registrando en la lista logs_usuario lo que va ocurriendo y esa lista de sucesos devuelva esta función junto con la variable entera id_autoinc.

    Args:
        usuarios (list): lista de usuarios
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        _type_: _description_
    """
    clear_screen()
    bucle_menu_agregar = True
    while bucle_menu_agregar:
        mostrar_menu("   Menú [AGREGAR USUARIO] →", lista_menu_usuarios, 2, 1, True, 1, "Menú [GESTIONAR USUARIOS]", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                bucle_menu_agregar_usuario = True
                while bucle_menu_agregar_usuario:
                    clear_screen()
                    mensaje("🛒   INGRESE USUARIO AL SISTEMA   →")
                    nuevo_usuario = agregar_usuario(perfiles_usuario)
                    id_preex = traer_id_producto_preex_desde_db("crud", "usuarios", nuevo_usuario)
                    if id_preex:
                        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"intento de agregar usuario '{nuevo_usuario["mail"]} - {nuevo_usuario["perfil_acceso"]}': ya existe en stock ✕", id_usuario_a_gestionar=id_preex)
                        logs_usuario.append(etapa_usuario) 
                        clear_screen()
                        mensaje(f"🛒   USUARIO EXISTENTE   ✕")
                        print("\n")
                        mostrar_menu("   Menú [AGREGAR USUARIO AL SISTEMA] →", lista_si_no, 1, 2, True, 0, "", "", "")
                        match opcion_menu(2, "Ingresar DATOS"):
                            case 1:
                                clear_screen()
                                bucle_menu_agregar_usuario = True
                            case 2:
                                clear_screen()
                                bucle_menu_agregar_usuario = False
                    else:
                        agregar_usuario_en_db("crud", "usuarios", nuevo_usuario)
                        nuevo_usuario.update({"id": traer_id_producto_desde_db("crud", "usuarios", nuevo_usuario)})
                        usuarios.append(nuevo_usuario)
                        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"usuario: '({nuevo_usuario["mail"]} - {nuevo_usuario["perfil_acceso"]})' agregado ✓", id_usuario_a_gestionar=nuevo_usuario["id"])
                        logs_usuario.append(etapa_usuario)                                                  
                        clear_screen()
                        mensaje(f"🛒   USUARIO AGREGADO    ✓")
                        print("\n")
                        mostrar_menu("   Menú [AGREGAR USUARIO AL SISTEMA] →", lista_si_no, 1, 2, True, 0, "", "", "")
                        match opcion_menu(2, "Ingresar DATOS"):
                            case 1:
                                bucle_menu_agregar_usuario = True
                            case 2:
                                clear_screen()
                                bucle_menu_agregar_usuario = False
            case 2:
                clear_screen()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del menú agregar usuario")
                logs_usuario.append(etapa_usuario)
                bucle_menu_agregar = False
    return id_autoinc


def submenu_editar_datos_de_usuario_del_sistema(usuarios, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que permite al usuario 'administrador' editar los atributos de un usuario del sistema

    Args:
        usuarios (list): lista de usuarios
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        _type_: _description_
    """
    clear_screen()
    bucle_menu_editar = True
    while bucle_menu_editar:
        mostrar_menu("   Menú [EDITAR DATOS DEL USUARIO] →", lista_menu_usuarios, 3, 1, True, 1, "Menú [GESTIONAR USUARIOS]", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                clear_screen()
                mensaje("🛒   LISTADO DE USUARIOS   →")
                mostrar_lista_usuarios(ordenar_lista(usuarios, "perfil_acceso", "mail", "id", True))
                print("\n")
                mensaje(f"🛒   INGRESAR USUARIO A EDITAR: ITEM '1' - '{len(usuarios)}'  →")
                i = opcion_menu_con_0(len(usuarios), "Ingresar DATOS / (0) Salir")
                if i != 0:
                    indice_item = i - 1
                    usuario_a_editar = usuarios[indice_item]
                    lista_usuario_a_editar = []
                    lista_usuario_a_editar.append(usuario_a_editar)
                    clear_screen()
                    mensaje(f"🛒   '{usuario_a_editar.get("nombre").upper()} {usuario_a_editar.get("apellido").upper()}' →→→ {usuario_a_editar.get("mail").upper()}")
                    mostrar_lista_usuarios(lista_usuario_a_editar, False)
                    print("\n")
                    mostrar_menu("   Menú [EDITAR USUARIOS] →", lista_menu_claves_usuarios, 1, 7, True, 1, "[SALIR]", "", "")
                    i = opcion_menu(8, "Ingresar DATOS")
                    while i != 8:
                        id_autoinc = editar_usuario(usuario_a_editar, perfiles_usuario, i, usuarios, usuario, logs_usuario, id_autoinc)[0]
                        clear_screen()
                        mensaje(f"🛒   '{usuario_a_editar.get("nombre").upper()} {usuario_a_editar.get("apellido").upper()}' →→→ {usuario_a_editar.get("mail").upper()}")
                        mostrar_lista_usuarios(lista_usuario_a_editar, False)
                        mensaje(f"🛒   USUARIO EDITADO    ✓")
                        mostrar_menu("   Menú [EDITAR USUARIOS] →", lista_menu_claves_usuarios, 1, 7, True, 1, "[SALIR]", "", "")
                        i = opcion_menu(8, "Ingresar DATOS")
                    actualizar_usuario_en_db("crud", "usuarios", usuario_a_editar)
                clear_screen()
            case 2:
                clear_screen()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del menú editar datos del usuario")
                logs_usuario.append(etapa_usuario)
                bucle_menu_editar = False
    return id_autoinc


def submenu_eliminar_usuario_del_sistema(usuarios, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que permite al usuario 'administrador' eliminar un usuario/usuarios seleccionado/s

    Args:
        usuarios (list): lista de usuarios
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        _type_: _description_
    """
    clear_screen()
    bucle_menu_eliminar = True
    while bucle_menu_eliminar:
        mostrar_menu("   Menú [ELIMINAR USUARIO] →", lista_menu_usuarios, 4, 1, True, 1, "Menú [GESTIONAR USUARIOS]", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                clear_screen()
                mensaje("🛒   LISTADO DE USUARIOS   →")
                mostrar_lista_usuarios(usuarios)
                print("\n")
                mensaje(f"🛒   INGRESAR RANGO DE USUARIOS A ELIMINAR '1' - '{len(usuarios)}'  →")
                primer_usuario = opcion_menu_2_con_0(1, len(usuarios), "'Primer USUARIO'/ (0) Salir")
                if primer_usuario != 0:
                    ultimo_usuario = opcion_menu_2_con_0(primer_usuario, len(usuarios)-primer_usuario+1, "'Último USUARIO'/ (0) Salir")
                    if ultimo_usuario != 0:
                            clear_screen()
                            usuarios_copia = usuarios[:]
                            lista_usuarios_a_eliminar = []
                            for i in usuarios[primer_usuario-1:ultimo_usuario]:
                                lista_usuarios_a_eliminar.append(i.get("id"))
                            clear_screen()
                            mensaje("🛒   LISTADO DE USUARIOS A ELIMINAR  →")
                            mostrar_lista_usuarios_seleccion(usuarios, primer_usuario, ultimo_usuario)
                            print("\n")
                            mostrar_menu("   Menú [ELIMINAR USUARIOS] →", lista_si_no, 1, 2, True, 0, "", "", "")
                            match opcion_menu(2, "Ingresar DATOS"):
                                case 1:
                                    for i in usuarios_copia:
                                        if i["id"] in lista_usuarios_a_eliminar:
                                            usuarios.remove(i)
                                            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"usuario: '({i["mail"]} - {i["perfil_acceso"]})' eliminado ✕", id_usuario_a_gestionar=i["id"])
                                            logs_usuario.append(etapa_usuario) 
                                    clear_screen()
                                    mensaje("🛒   USUARIOS ELIMINADOS   ✓")
                                    eliminar_usuario_en_db("crud", "usuarios", lista_usuarios_a_eliminar)
                                case 2:
                                    clear_screen()
                    else:
                        clear_screen()
                else:
                    clear_screen()
            case 2:
                clear_screen()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del menú eliminar usuario")
                logs_usuario.append(etapa_usuario)
                bucle_menu_eliminar = False
    return id_autoinc


def submenu_gestionar_usuarios_eliminados(usuarios, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que permite mostrar al usuario 'administrador' los usuarios eliminados y poder recuperarlos

    Args:
        usuarios (list): lista de usuarios
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        _type_: _description_
    """
    clear_screen()
    usuarios_eliminados = cargar_lista_con_id_desde_db_opcion("crud", "usuarios", False)
    if usuarios_eliminados:
        mensaje("🛒   LISTA DE USUARIOS ELIMINADOS   ↓")
        mostrar_lista_usuarios_eliminados(usuarios_eliminados)
        print("\n")
        mostrar_menu("   Menú [RECUPERAR USUARIOS] →", lista_si_no, 1, 2, True, 0, "", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                clear_screen()
                lista_usuarios_eliminados_a_recuperar = []
                if usuarios_eliminados != []:
                    for i in usuarios_eliminados:
                        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        i.update({"fecha_alta": fecha})
                        i.update({"fecha_modificacion": ""})
                        i.update({"fecha_baja": ""})
                        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"usuario: '({i["mail"]} - {i["perfil_acceso"]})' recuperado ✓", id_usuario_a_gestionar=i["id"])
                        logs_usuario.append(etapa_usuario) 
                        lista_usuarios_eliminados_a_recuperar.append(i["id"])
                    usuarios.extend(usuarios_eliminados)
                    usuarios_eliminados.clear()
                    recuperar_usuarios_eliminados_en_db("crud", "usuarios", lista_usuarios_eliminados_a_recuperar)
                    clear_screen()
                    mensaje("🛒   USUARIOS RECUPERADOS   ✓")
                    clear_screen()
            case 2:
                clear_screen()
    else:
        clear_screen()
        mensaje("🛒   NO HAY USUARIOS ELIMINADOS   →")
        print("\n")
    return id_autoinc


def submenu_generar_reporte_de_tiempo_de_uso(usuario, logs_usuario, id_autoinc):
    """Función que genera reporte de tiempo de uso del sistema de los usuarios en un período de tiempo estipulado. El usuario 'administrador' puede generar un reporte de todos los usuarios pero el 'supervisor' no puede ver los movimientos del 'administrador'

    Args:
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        _type_: _description_
    """
    clear_screen()
    bucle_menu_generar = True
    while bucle_menu_generar:
        mostrar_menu("   Menú [GENERAR REPORTE DE USO] →", lista_menu_usuarios, 6, 1, True, 1, "Menú [GESTIONAR USUARIOS]", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                clear_screen()
                mensaje("🛒   INGRESE LAS FECHAS (DESDE→HASTA) PARA GENERAR EL REPORTE  →")
                fecha_desde = input(f"\n• Fecha Desde ('YYYY-MM-DD'⟩: ").strip().lower()
                while not validar_fecha(fecha_desde):
                    fecha_desde= input(f"\n• Fecha Desde ('YYYY-MM-DD'⟩: ").strip().lower()
                fecha_hasta = input(f"\n• Fecha Hasta ('YYYY-MM-DD'⟩: ").strip().lower()
                while not validar_fecha(fecha_hasta) or fecha_hasta < fecha_desde:
                    fecha_hasta= input(f"\n• Fecha hasta('YYYY-MM-DD'⟩: ").strip().lower()
                if usuario["perfil_acceso"] == "administrador":
                    lista_reporte = generar_reportes_tiempo_usuario_en_db("crud", "logs_usuarios", fecha_desde, fecha_hasta, usuario)
                else:
                    lista_reporte = generar_reportes_tiempo_usuario_en_db("crud", "logs_usuarios", fecha_desde, fecha_hasta, usuario)
                clear_screen()
                reportar_tiempo_usuarios_por_dia_entrefechas(lista_reporte, usuario)
                print()
                reportar_tiempo_por_usuario_total_entrefechas(lista_reporte, usuario)
                print()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"genero reporte de tiempo de uso desde '{fecha_desde} hasta {fecha_hasta}'")
                logs_usuario.append(etapa_usuario)
            case 2:
                clear_screen()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del submenú generar reportes de tiempo de uso")
                logs_usuario.append(etapa_usuario)  
                bucle_menu_generar = False
    return id_autoinc 


def submenu_generar_reporte_de_ventas(usuario, logs_usuario, id_autoinc):
    """Función que genera reporte de ventas de los usuarios en un período de tiempo estipulado. El usuario 'administrador' puede generar un reporte de todos los usuarios pero el 'supervisor' no puede ver los movimientos del 'administrador'

    Args:
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        _type_: _description_
    """
    clear_screen()
    bucle_menu_generar = True
    while bucle_menu_generar:
        mostrar_menu("   Menú [GENERAR REPORTE DE VENTAS] →", lista_menu_usuarios, 7, 1, True, 1, "Menú [GESTIONAR USUARIOS]", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                clear_screen()
                mensaje("🛒   INGRESE LAS FECHAS (DESDE→HASTA) PARA GENERAR EL REPORTE  →")
                fecha_desde = input(f"\n• Fecha Desde ('YYYY-MM-DD'⟩: ").strip().lower()
                while not validar_fecha(fecha_desde):
                    fecha_desde= input(f"\n• Fecha Desde ('YYYY-MM-DD'⟩: ").strip().lower()
                fecha_hasta = input(f"\n• Fecha Hasta ('YYYY-MM-DD'⟩: ").strip().lower()
                while not validar_fecha(fecha_hasta) or fecha_hasta < fecha_desde:
                    fecha_hasta= input(f"\n• Fecha hasta('YYYY-MM-DD'⟩: ").strip().lower()
                if usuario["perfil_acceso"] == "administrador":
                    lista_reporte = generar_reportes_ventas_en_db("crud", "logs_usuarios", fecha_desde, fecha_hasta, usuario)
                else:
                    lista_reporte = generar_reportes_ventas_en_db("crud", "logs_usuarios", fecha_desde, fecha_hasta, usuario)
                clear_screen()
                reportar_ventas_por_usuario_por_dia_entrefechas(lista_reporte, usuario)
                print()
                reportar_ventas_por_usuario_total_entrefechas(lista_reporte, usuario)
                print()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"genero reporte de cantidad de ventas desde '{fecha_desde} hasta {fecha_hasta}'")
                logs_usuario.append(etapa_usuario)
            case 2:
                clear_screen()
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"sale del submenú generar reportes cantidad de ventas")
                logs_usuario.append(etapa_usuario)  
                bucle_menu_generar = False
    return id_autoinc 


def submenu_eliminar_logs_usuarios(usuario, logs_usuario, id_autoinc):
    """Función que muestra al usuario 'administrador' la opción de eliminar los logs de los usuarios

    Args:
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
    """   
    if cargar_lista_con_id_desde_db("crud", "logs_usuarios"):
        clear_screen()
        mensaje(f"🛒   ELIMINAR LOGS DE USUARIOS   →")
        mostrar_menu("   Menú [CONFIRMAR OPERACIÓN] →", lista_si_no, 1, 2, True, 0, "", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                eliminar_logs_usuario_en_db("crud", "logs_usuarios")
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"base de datos recuperada desde backup")
                logs_usuario.append(etapa_usuario)
                clear_screen()
                mensaje(f"🛒   LOGS USUARIOS ELIMINADOS  ✓")
                print("\n")
            case 2:
                clear_screen()
    else:
        clear_screen()
        mensaje(f"🛒   NO HAY LOGS USUARIOS  ✕")
    return id_autoinc



def menu_gestionar_usuarios(usuarios, usuario, logs_usuario, id_autoinc):
    """Función con menú interactivo que muestra al usuario administrador las opciones de gestionar a los usuarios y generar reportes de tiempo de uso del sistema y de ventas. También el usuario 'supervisor' tiene acceso a ciertas opciones de este menú pero con algunas diferencias
    Args:
        usuarios (list): lista de usuarios
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        _type_: _description_
    """
    clear_screen()
    bucle_menu_gestionar_usuarios = True
    while bucle_menu_gestionar_usuarios:
        mostrar_menu("   Menú [GESTIONAR USUARIOS] →", lista_menu_usuarios, 1, 8, True, 1, "Menú [PRINCIPAL]", "", "")
        match opcion_menu(9, "Ingresar DATOS"):
            case 1:
                if usuario["perfil_acceso"] == "administrador":
                    id_autoinc = submenu_ver_usuarios_del_sistema(usuarios, usuario, logs_usuario, id_autoinc)
                else:
                    bucle_menu_gestionar_usuarios = menu_restriccion_de_acceso("perfil sin acceso a esta funcionalidad")
            case 2:
                if usuario["perfil_acceso"] == "administrador":
                    id_autoinc = submenu_agregar_usuario_al_sistema(usuarios, usuario, logs_usuario, id_autoinc)
                else:
                    bucle_menu_gestionar_usuarios = menu_restriccion_de_acceso("perfil sin acceso a esta funcionalidad")
            case 3:
                if usuario["perfil_acceso"] == "administrador":
                    id_autoinc = submenu_editar_datos_de_usuario_del_sistema(usuarios, usuario, logs_usuario, id_autoinc)
                else:
                    bucle_menu_gestionar_usuarios = menu_restriccion_de_acceso("perfil sin acceso a esta funcionalidad")
            case 4:
                if usuario["perfil_acceso"] == "administrador":
                    id_autoinc = submenu_eliminar_usuario_del_sistema(usuarios, usuario, logs_usuario, id_autoinc)
                else:
                    bucle_menu_gestionar_usuarios = menu_restriccion_de_acceso("perfil sin acceso a esta funcionalidad")
            case 5:
                if usuario["perfil_acceso"] == "administrador":
                    id_autoinc = submenu_gestionar_usuarios_eliminados(usuarios, usuario, logs_usuario, id_autoinc)
                else:
                    bucle_menu_gestionar_usuarios = menu_restriccion_de_acceso("perfil sin acceso a esta funcionalidad")
            case 6:
                id_autoinc = submenu_generar_reporte_de_tiempo_de_uso(usuario, logs_usuario, id_autoinc)
            case 7:
                id_autoinc = submenu_generar_reporte_de_ventas(usuario, logs_usuario, id_autoinc)
            case 8:
                if usuario["perfil_acceso"] == "administrador":
                    id_autoinc = submenu_eliminar_logs_usuarios(usuario, logs_usuario, id_autoinc)
                else:
                    bucle_menu_gestionar_usuarios = menu_restriccion_de_acceso("perfil sin acceso a esta funcionalidad")
            case 9:
                clear_screen()
                bucle_menu_gestionar_usuarios = False
    return id_autoinc