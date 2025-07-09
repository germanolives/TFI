from database import iniciar_carga_productos
from interfaz_usuario import mostrar_menu, opcion_menu, mensaje
from menu import menu_agregar_producto, menu_ver_productos, menu_buscar_producto, menu_actualizar_producto, menu_eliminar_producto, menu_mantenimiento, menu_gestionar_usuarios, menu_restriccion_de_acceso, menu_actualizar_movimientos_producto
from variables import lista_menu_principal
from usuarios import seguir_usuario, iniciar_logs_usuario_json, finalizar_logs_usuario_json, genera_bloque_rastreo_usuario_json, genera_bloque_rastreo_usuario_db
from utilidades import clear_screen


def principal(usuario, usuarios):
    """Función general del programa con los distintos bloques funcionales. El usuario que ingresa al sistema puede o no ser traqueado en todo su recorrido (generando un archivo .json o registros en una tabla en la base de datos. El usuario administrador quien tiene acceso a gestionar a los usuarios puede seleccionar estas posibilidades para cada usuario del sistema). El administrador y el supervisor pueden generar reporte de tiempo de uso en el sistema de los usuarios y también la cantidad de ventas realizadas entre un período de tiempo.

    Args:
        usuario (dict): usuario logueado en el sistema
        usuarios (list): lista de usuarios
    """
    if usuario:
        rastreo_usuario_json = usuario["tracking_json"]
        rastreo_usuario_db = usuario["tracking_db"]
        logs_usuario = []
        id_autoinc = 0
        if rastreo_usuario_json:
            logs_usuario, id_autoinc = iniciar_logs_usuario_json()
        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al sistema")
        logs_usuario.append(etapa_usuario)
        productos = iniciar_carga_productos()
        perfil_usuario = usuario["perfil_acceso"]
        bucle_menu_principal = True
        while bucle_menu_principal:
            clear_screen()
            mostrar_menu("   TIENDA / CRUD • Menú [PRINCIPAL] →", lista_menu_principal, 1, 8, True, 1, "[SALIR]", "", "")
            match opcion_menu(9, "Ingresar DATOS"):
                case 1: #opción para agregar un producto
                    if perfil_usuario == "administrador" or perfil_usuario == "supervisor":
                        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al menú agregar producto")
                        logs_usuario.append(etapa_usuario)
                        id_autoinc = menu_agregar_producto(productos, usuario, logs_usuario, id_autoinc)
                    else:
                        bucle_menu_principal = menu_restriccion_de_acceso("perfil sin acceso a esta funcionalidad")
                case 2: #opción para ver todos los productos en un listado ordenado de diversas maneras
                    if productos:
                        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al menú ver productos")
                        logs_usuario.append(etapa_usuario)
                        id_autoinc = menu_ver_productos(productos, usuario, logs_usuario, id_autoinc)
                    else:
                        bucle_menu_principal = menu_restriccion_de_acceso("stock inexistente")
                case 3: #opción para buscar un producto o productos por algún atributo
                    if productos:
                        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al menú buscar productos")
                        logs_usuario.append(etapa_usuario)
                        id_autoinc = menu_buscar_producto(productos, usuario, logs_usuario, id_autoinc)
                    else:
                        bucle_menu_principal = menu_restriccion_de_acceso("stock inexistente")
                case 4: #opción para actualizar los atributos de un producto en particular o algún atributo particular de un grupo de productos
                    if perfil_usuario == "administrador" or perfil_usuario == "supervisor" or perfil_usuario == "vendedor":
                        if productos:
                            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al menú actualizar producto")
                            logs_usuario.append(etapa_usuario)
                            id_autoinc = menu_actualizar_producto(productos, usuario, logs_usuario, id_autoinc)
                        else:
                            bucle_menu_principal = menu_restriccion_de_acceso("stock inexistente")
                    else:
                        bucle_menu_principal = menu_restriccion_de_acceso("perfil sin acceso a esta funcionalidad")
                case 5: #opción para actualizar los movimientos (compra/venta/ajuste) de un producto en particular
                    if perfil_usuario == "administrador" or perfil_usuario == "supervisor" or perfil_usuario == "vendedor":
                        if productos:
                            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al menú actualizar movimientos de producto")
                            logs_usuario.append(etapa_usuario)
                            id_autoinc = menu_actualizar_movimientos_producto(productos, usuario, logs_usuario, id_autoinc)
                        else:
                            bucle_menu_principal = menu_restriccion_de_acceso("stock inexistente")
                    else:
                        bucle_menu_principal = menu_restriccion_de_acceso("perfil sin acceso a esta funcionalidad")
                case 6: #opción para eliminar un producto en particular o eliminar un grupo de productos de un modelo o una marca solicitada
                    if perfil_usuario == "administrador" or perfil_usuario == "supervisor":
                        if productos:
                            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al menú eliminar producto")
                            logs_usuario.append(etapa_usuario)
                            id_autoinc = menu_eliminar_producto(productos, usuario, logs_usuario, id_autoinc)
                        else:
                            bucle_menu_principal = menu_restriccion_de_acceso("stock inexistente")
                    else:
                        bucle_menu_principal = menu_restriccion_de_acceso("perfil sin acceso a esta funcionalidad")
                case 7: #opción mantenimiento para recuperar eliminados
                    if perfil_usuario == "administrador":
                        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al menú mantenimiento")
                        logs_usuario.append(etapa_usuario)
                        id_autoinc = menu_mantenimiento(productos, usuario, logs_usuario, id_autoinc)
                    else:
                        bucle_menu_principal = menu_restriccion_de_acceso("perfil sin acceso a esta funcionalidad")
                case 8: # Gestionar usuarios
                    if perfil_usuario == "administrador" or perfil_usuario == "supervisor":
                        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"ingreso al menú gestionar usuarios")
                        logs_usuario.append(etapa_usuario)
                        id_autoinc =  menu_gestionar_usuarios(usuarios, usuario, logs_usuario, id_autoinc)
                    else:
                        bucle_menu_principal = menu_restriccion_de_acceso("perfil sin acceso a esta funcionalidad")
                case 9:
                    clear_screen()
                    etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,"salir del sistema")
                    logs_usuario.append(etapa_usuario)
                    if rastreo_usuario_json:
                        finalizar_logs_usuario_json(genera_bloque_rastreo_usuario_json(logs_usuario))
                    if rastreo_usuario_db:
                        genera_bloque_rastreo_usuario_db(logs_usuario)
                    mensaje("🔚")
                    bucle_menu_principal = False
                    return True
    else:
        clear_screen()
        mensaje("🔚")