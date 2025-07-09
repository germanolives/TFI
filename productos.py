import datetime
from database import actualizar_item_producto_en_db, actualizar_item_movimiento_producto_en_db, agregar_ajuste_producto_db, agregar_ingreso_egreso_producto_db, eliminar_item_producto_en_db, traer_id_mov_desde_db
from interfaz_usuario import mensaje, mostrar_detalle_cambio_stock, mostrar_detalle_cambio_stock_seleccion, mostrar_lista, mostrar_menu, opcion_menu, opcion_menu_con_0, opcion_menu_2_con_0
from variables import lista_cambio_stock, lista_menu_claves_producto, lista_item_movimiento, lista_item_movimiento_eliminar, lista_si_no
from utilidades import ordenar_lista, clear_screen
from validaciones import de_caracter_a_float, validar_fecha
from usuarios import seguir_usuario



def calcular_cantidad_producto(producto):
    """Función que calcula la cantidad en stock de un producto chequeando todos los movimientos de ese producto

    Args:
        producto (dict): producto a calcular su cantidad en stock

    Returns:
        cantidad_producto (int): cantidad en stock del producto calculada
    """
    cantidad_producto = 0
    if producto["ingreso"]:
        for i in producto["ingreso"]:
            if i ["estado"]:
                cantidad_producto += i["cantidad_ingreso"]
    if producto["egreso"]:
        for i in producto["egreso"]:
            if i ["estado"]:
                cantidad_producto -= i["cantidad_egreso"]
    if producto["ajuste"]:
        for i in producto["ajuste"]:
            if i ["estado"]:
                cantidad_producto += i["cantidad_ajuste"]
    return cantidad_producto


def agregar_item_movimiento_de_compra(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que agrega un movimiento de ingreso (compra) de un producto determinado

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_compra = dicc["ingreso"]
    movimiento_compra = {"id": 0, "producto_id": 0, "fecha_compra": "", "proveedor_id": "", "nro_factura_proveedor": "", "cantidad_ingreso": 0, "costo_unitario": 0.0, "valor_compra": 0.0, "estado": True}
    agregar_item_movimientos = True                                   
    while agregar_item_movimientos:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   INGRESOS   →")
        mostrar_detalle_cambio_stock(movimientos_compra, "compra")
        print("\n")
        mensaje("🛒   INGRESAR LOS DATOS   →")
        nuevo_item = {}
        for i in movimiento_compra:
            if i != "fecha_compra" and i!= "valor_compra" and i!= "estado":
                if isinstance(movimiento_compra.get(i), int):
                    if i == "id":
                        nuevo_item[i] = 0
                    elif i == "producto_id":
                        nuevo_item[i] = dicc["id"]
                    else:                    
                        valor_in= input(f"\n# {i.title()}: ").strip().lower()
                        while not valor_in.isdigit() or int(valor_in) == 0:
                            valor_in= input(f"\n# {i.title()}: ").strip().lower()
                        valor_in = int(valor_in)
                        nuevo_item[i] = valor_in
                elif isinstance(movimiento_compra.get(i), str):
                    valor_in= input(f"\n• {i.title()}: ").strip().lower()
                    while valor_in == "":
                        valor_in= input(f"\n• {i.title()}: ").strip().lower()
                    nuevo_item[i] = valor_in
                elif isinstance(movimiento_compra.get(i), float):
                    valor_in= input(f"\n$ {i.title()}: ").strip().lower()
                    while not de_caracter_a_float(valor_in):
                        valor_in= input(f"\n$ {i.title()}: ").strip().lower()
                    valor_in = float(valor_in)
                    nuevo_item[i] = valor_in
            elif i == "fecha_compra":
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                nuevo_item[i] = fecha
        cantidad_compra = nuevo_item.get("cantidad_ingreso")
        precio_compra = nuevo_item.get("costo_unitario")
        valor_compra =  cantidad_compra * precio_compra
        nuevo_item["valor_compra"] = valor_compra
        nuevo_item["estado"] = True
        dicc["ingreso"].append(nuevo_item)
        cantidad_nueva = calcular_cantidad_producto(dicc)
        dicc.update({"cantidad": cantidad_nueva})
        agregar_ingreso_egreso_producto_db("crud", "productos", "cantidad", cantidad_nueva, nuevo_item["producto_id"], "ingresos", nuevo_item)
        nuevo_item.update({"id": traer_id_mov_desde_db("crud", "ingresos", nuevo_item)})
        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"agrega movimiento compra: '({nuevo_item["fecha_compra"]}) - ({nuevo_item["proveedor_id"]}) - ({nuevo_item["nro_factura_proveedor"]}) - ({nuevo_item["cantidad_ingreso"]}) - ({nuevo_item["costo_unitario"]}) - ({nuevo_item["valor_compra"]})'", id_producto=dicc.get("id"), id_ingreso_producto=nuevo_item["id"], ope_ingreso=True)
        logs_usuario.append(etapa_usuario)
        mensaje("🛒   ITEM AGREGADO   ✓")
        print("\n")
        actualizado = True
        mostrar_menu("   Menú [AGREGAR MÁS ITEMS] →", lista_si_no, 1, 2, True, 0, "", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                clear_screen()
                mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
                mensaje("🛒   INGRESOS   →")
                print("\n")
                mostrar_detalle_cambio_stock(movimientos_compra, "compra")
            case 2:
                agregar_item_movimientos = False
    return id_autoinc, actualizado


def eliminar_un_item_seleccionado_movimiento_de_compra(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que elimina un movimiento de ingreso (compra) de un producto determinado

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_compra = dicc["ingreso"]
    clear_screen()
    mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
    mensaje("🛒   INGRESOS   →")
    mostrar_detalle_cambio_stock(movimientos_compra, "compra")
    print("\n")
    mensaje(f"🛒   INGRESAR NÚMERO DE ITEM A ELIMINAR '1' - '{len(movimientos_compra)}'  →")
    indice_item = opcion_menu_con_0(len(movimientos_compra), "Ingresar DATOS / (0) Salir") - 1
    if indice_item != -1:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   INGRESOS   →")
        mostrar_detalle_cambio_stock_seleccion(movimientos_compra, "compra", indice_item+1, indice_item+1)
        print("\n")
        mostrar_menu("   Menú [CONFIRMA ELIMINAR] →", lista_si_no, 1, 2, True, 0, "", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                actualizado = True
                movimientos_compra[indice_item]["estado"] = False                                                        
                if dicc["id"] == movimientos_compra[indice_item]["producto_id"]:
                    producto_id = dicc["id"]
                    id_item_a_eliminar = movimientos_compra[indice_item]["id"]
                    lista_items_a_eliminar = []
                    lista_items_a_eliminar.append(id_item_a_eliminar)
                    etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"elimina movimiento compra: '({movimientos_compra[indice_item]["fecha_compra"]}) - ({movimientos_compra[indice_item]["proveedor_id"]}) - ({movimientos_compra[indice_item]["nro_factura_proveedor"]}) - ({movimientos_compra[indice_item]["cantidad_ingreso"]}) - ({movimientos_compra[indice_item]["costo_unitario"]}) - ({movimientos_compra[indice_item]["valor_compra"]})'", id_producto=producto_id, id_ingreso_producto=movimientos_compra[indice_item]["id"])
                    logs_usuario.append(etapa_usuario)
                    movimientos_compra.pop(indice_item)
                    cantidad_nueva = calcular_cantidad_producto(dicc)
                    dicc.update({"cantidad": cantidad_nueva})
                    eliminar_item_producto_en_db("crud", "productos", producto_id, "cantidad", cantidad_nueva, "ingresos", lista_items_a_eliminar)
                clear_screen()
                mensaje("🛒   ITEM ELIMINADO   ✓")
                mostrar_detalle_cambio_stock(movimientos_compra, "compra")
                print("\n")
            case 2:
                actualizado = False
    else:
        clear_screen()
    return id_autoinc, actualizado


def eliminar_varios_items_seleccionados_movimiento_de_compra(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que elimina varios movimientos de ingreso (compra) seleccionados de un producto determinado

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_compra = dicc["ingreso"]
    clear_screen()
    mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
    mensaje("🛒   INGRESOS   →")
    mostrar_detalle_cambio_stock(movimientos_compra, "compra")
    print("\n")
    mensaje(f"🛒   INGRESAR RANGO DE ITEMS A ELIMINAR   →")
    primer_item = opcion_menu_2_con_0(1, len(movimientos_compra), "'Primer ITEM'/ (0) Salir")
    if primer_item != 0:
        ultimo_item = opcion_menu_2_con_0(primer_item, len(movimientos_compra)-primer_item+1, "'Último ITEM'/ (0) Salir")
        if ultimo_item != 0:
            clear_screen()
            mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
            mensaje("🛒   SELECCIÓN DE ITEMS A ELIMINAR   →")
            mostrar_detalle_cambio_stock_seleccion(movimientos_compra, "compra", primer_item, ultimo_item)
            print("\n")
            mostrar_menu("   Menú [CONFIRMA ELIMINAR] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    actualizado = True
                    totcant = 0
                    c = 0
                    movimientos_compra_copia = movimientos_compra[:]
                    lista_items_a_eliminar = []
                    for mov in movimientos_compra_copia:
                        c += 1
                        if c >= primer_item and c <= ultimo_item:
                            totcant += mov["cantidad_ingreso"]
                            mov["estado"] = False
                            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"elimina movimiento compra: '({mov["fecha_compra"]}) - ({mov["proveedor_id"]}) - ({mov["nro_factura_proveedor"]}) - ({mov["cantidad_ingreso"]}) - ({mov["costo_unitario"]}) - ({mov["valor_compra"]})'", id_producto=dicc.get("id"), id_ingreso_producto=mov["id"])
                            logs_usuario.append(etapa_usuario)
                            lista_items_a_eliminar.append(mov["id"])
                            movimientos_compra.remove(mov)
                    cantidad_nueva = calcular_cantidad_producto(dicc)
                    dicc.update({"cantidad": cantidad_nueva})
                    producto_id = dicc["id"]
                    eliminar_item_producto_en_db("crud", "productos", producto_id, "cantidad", cantidad_nueva, "ingresos", lista_items_a_eliminar)
                    mensaje("🛒   ITEMs ELIMINADOs   ✓")
                case 2:
                    actualizado = False
        else:
            clear_screen() 
    else:
        clear_screen()
    return id_autoinc, actualizado


def eliminar_todos_los_items_movimiento_de_compra(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que elimina todos los movimientos de ingreso (compra) de un producto determinado

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_compra = dicc["ingreso"]
    clear_screen()
    mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
    mensaje("🛒   INGRESOS   →")
    mostrar_detalle_cambio_stock_seleccion(movimientos_compra, "compra", 1, len(movimientos_compra))
    print("\n")
    mensaje(f"🛒   ELIMINAR LOS '{len(movimientos_compra)}' ITEMS   →")
    print("\n")
    mostrar_menu("   Menú [CONFIRMA ELIMINAR] →", lista_si_no, 1, 2, True, 0, "", "", "")
    match opcion_menu(2, "Ingresar DATOS"):
        case 1:
            actualizado = True
            totcant = 0
            movimientos_compra_copia = movimientos_compra[:]
            lista_items_a_eliminar = []
            for mov in movimientos_compra_copia:
                totcant += mov["cantidad_ingreso"]
                mov["estado"] = False
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"elimina movimiento compra: '({mov["fecha_compra"]}) - ({mov["proveedor_id"]}) - ({mov["nro_factura_proveedor"]}) - ({mov["cantidad_ingreso"]}) - ({mov["costo_unitario"]}) - ({mov["valor_compra"]})'", id_producto=dicc.get("id"), id_ingreso_producto=mov["id"])
                logs_usuario.append(etapa_usuario)
                lista_items_a_eliminar.append(mov["id"])
            movimientos_compra.clear()
            cantidad_nueva = calcular_cantidad_producto(dicc)
            dicc.update({"cantidad": cantidad_nueva})
            producto_id = dicc["id"]
            eliminar_item_producto_en_db("crud", "productos", producto_id, "cantidad", cantidad_nueva, "ingresos", lista_items_a_eliminar)
            mensaje("🛒   ITEMs ELIMINADOs   ✓")
        case 2:
            actualizado = False
    return id_autoinc, actualizado


def eliminar_item_movimiento_de_compra(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que permite al usuario elegir como eliminar movimientos de compra de los productos

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_compra = dicc["ingreso"]
    eliminar_item_movimientos = True                                   
    while movimientos_compra and eliminar_item_movimientos:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   INGRESOS   →")
        mostrar_detalle_cambio_stock(movimientos_compra, "compra")
        print("\n")
        mostrar_menu("   Menú [ELIMINAR MOVIMIENTOS] →", lista_item_movimiento_eliminar, 1, 3, True, 1, "Menú [VOLVER]", "", "")
        match opcion_menu(4, "Ingresar DATOS"):
            case 1:
                id_autoinc, actualizado  = eliminar_un_item_seleccionado_movimiento_de_compra(dicc, usuario, logs_usuario, id_autoinc)
            case 2:
                id_autoinc, actualizado  = eliminar_varios_items_seleccionados_movimiento_de_compra(dicc, usuario, logs_usuario, id_autoinc)
            case 3:
                id_autoinc, actualizado  = eliminar_todos_los_items_movimiento_de_compra(dicc, usuario, logs_usuario, id_autoinc)
            case 4:
                actualizado = False
                eliminar_item_movimientos = False
    return id_autoinc, actualizado


def editar_item_movimiento_de_compra(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que permite al usuario 'administrador' modificar los valores de un movimiento de compra de un producto

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_compra = dicc["ingreso"]
    editar_item_movimientos = True                                   
    while movimientos_compra and editar_item_movimientos:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   INGRESOS   →")
        mostrar_detalle_cambio_stock(movimientos_compra, "compra")
        print("\n")
        mensaje(f"🛒   INGRESAR NÚMERO DE ITEM A EDITAR '1' - '{len(movimientos_compra)}'  →")
        indice_item = opcion_menu_con_0(len(movimientos_compra), "Ingresar DATOS / (0) Salir") - 1
        if indice_item != -1:
            item_a_editar = movimientos_compra[indice_item]
            cantidad_mov_previa = item_a_editar.get("cantidad_ingreso")
            lista_menu_claves_ingresos = list (item_a_editar)[2:]
            lista_item_a_editar = []
            lista_item_a_editar.append(item_a_editar)
            clear_screen()
            mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
            print("\n")
            mostrar_detalle_cambio_stock_seleccion(lista_item_a_editar, "compra", 1, 1)
            print("\n")
            mostrar_menu("   Menú [EDITAR ITEM] →", lista_menu_claves_ingresos, 1, 5, True, 1, "[SALIR]", "", "")
            ie = opcion_menu(6, "Ingresar DATOS") - 1
            if ie != 5:
                actualizado = True
                if ie == 0:
                    clave_in2 = lista_menu_claves_ingresos[ie]
                    valor_in2_previo = item_a_editar.get(clave_in2)
                    valor_in2 = input(f"\n• {clave_in2.title()} ⟨Nuevo Valor 'YYYY-MM-DD'⟩: ").strip().lower()
                    while not validar_fecha(valor_in2):
                        valor_in2= input(f"\n• {clave_in2.title()} ⟨Nuevo Valor 'YYYY-MM-DD'⟩: ").strip().lower()
                    item_a_editar.update({clave_in2: valor_in2})
                elif ie == 1 or ie == 2:
                    clave_in2 = lista_menu_claves_ingresos[ie]
                    valor_in2_previo = item_a_editar.get(clave_in2)
                    valor_in2 = input(f"\n• {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    while valor_in2 == "":
                        valor_in2= input(f"\n• {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    item_a_editar.update({clave_in2: valor_in2})
                elif ie == 3:
                    clave_in2 = lista_menu_claves_ingresos[ie]
                    valor_in2_previo = item_a_editar.get(clave_in2)
                    valor_in2 = input(f"\n# {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    while not valor_in2.isdigit() or int(valor_in2) == 0:
                        valor_in2= input(f"\n# {clave_in2.title()} (Nuevo Valor⟩: ").strip().lower()
                    item_a_editar.update({clave_in2: int(valor_in2)})
                elif ie == 4:
                    clave_in2 = lista_menu_claves_ingresos[ie]
                    valor_in2_previo = item_a_editar.get(clave_in2)
                    valor_in2 = input(f"\n$ {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    while not de_caracter_a_float(valor_in2):
                        valor_in2= input(f"\n$ {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    item_a_editar.update({clave_in2: float(valor_in2)})
                item_a_editar.update({"valor_compra": (item_a_editar.get("cantidad_ingreso")*item_a_editar.get("costo_unitario"))})
                cantidad_nueva = calcular_cantidad_producto(dicc)
                dicc.update({"cantidad": cantidad_nueva})
            clear_screen()
            mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
            print("\n")
            mostrar_detalle_cambio_stock_seleccion(lista_item_a_editar, "compra", 1, 1)
            print("\n")
            if ie != 5:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"movimiento compra cambia de: {clave_in2}: '{valor_in2_previo}' a {clave_in2}: '{item_a_editar.get(clave_in2)}'", id_producto=dicc.get("id"), id_ingreso_producto=movimientos_compra[indice_item]["id"])
                logs_usuario.append(etapa_usuario)
                actualizar_item_movimiento_producto_en_db("crud", "productos", "cantidad", cantidad_nueva, "ingresos", item_a_editar)
                mensaje("🛒   ITEM EDITADO   ✓")
            print("\n")
            mostrar_menu("   Menú [SEGUIR EDITANDO] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    editar_item_movimientos = True
                case 2:
                    editar_item_movimientos = False
        else:
            editar_item_movimientos = False
            clear_screen()
    return id_autoinc, actualizado


def agregar_item_movimiento_de_venta(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que agrega un movimiento de egreso (venta) de un producto determinado

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_venta = dicc["egreso"]
    movimiento_venta = {"id": 0, "producto_id": 0, "fecha_venta": "", "cliente_id": "", "nro_factura_cliente": "", "cantidad_egreso": 0, "precio_unitario": 0.0, "valor_venta": 0.0, "estado": True}
    agregar_item_movimientos = True                                   
    while agregar_item_movimientos:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   EGRESOS   →")
        mostrar_detalle_cambio_stock(movimientos_venta, "venta")
        print("\n")
        mensaje("🛒   INGRESAR LOS DATOS   →")
        nuevo_item = {}
        for i in movimiento_venta:
            if i != "fecha_venta" and i!= "valor_venta" and i!= "estado":
                if isinstance(movimiento_venta.get(i), int):
                    if i == "id":
                        nuevo_item[i] = 0
                    elif i == "producto_id":
                        nuevo_item[i] = dicc["id"]
                    else:                    
                        valor_in= input(f"\n# {i.title()}: ").strip().lower()
                        while not valor_in.isdigit() or dicc["cantidad"] < int(valor_in) or int(valor_in) == 0:
                            valor_in= input(f"\n# {i.title()}: ").strip().lower()
                        valor_in = int(valor_in)
                        nuevo_item[i] = valor_in
                elif isinstance(movimiento_venta.get(i), str):
                    valor_in= input(f"\n• {i.title()}: ").strip().lower()
                    while valor_in == "":
                        valor_in= input(f"\n• {i.title()}: ").strip().lower()
                    nuevo_item[i] = valor_in
                elif isinstance(movimiento_venta.get(i), float):
                    valor_in= input(f"\n$ {i.title()}: ").strip().lower()
                    while not de_caracter_a_float(valor_in):
                        valor_in= input(f"\n$ {i.title()}: ").strip().lower()
                    valor_in = float(valor_in)
                    nuevo_item[i] = valor_in
            elif i == "fecha_venta":
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                nuevo_item[i] = fecha
        cantidad_venta = nuevo_item.get("cantidad_egreso")
        precio_venta = nuevo_item.get("precio_unitario")
        valor_venta =  cantidad_venta * precio_venta
        nuevo_item["valor_venta"] = valor_venta
        nuevo_item["estado"] = True
        dicc["egreso"].append(nuevo_item)
        cantidad_nueva = calcular_cantidad_producto(dicc)
        dicc.update({"cantidad": cantidad_nueva})
        agregar_ingreso_egreso_producto_db("crud", "productos", "cantidad", cantidad_nueva, nuevo_item["producto_id"], "egresos", nuevo_item)
        nuevo_item.update({"id": traer_id_mov_desde_db("crud", "egresos", nuevo_item)})
        dicc.update({"cantidad": cantidad_nueva})
        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"agrega movimiento venta: '({nuevo_item["fecha_venta"]}) - ({nuevo_item["cliente_id"]}) - ({nuevo_item["nro_factura_cliente"]}) - ({nuevo_item["cantidad_egreso"]}) - ({nuevo_item["precio_unitario"]}) - ({nuevo_item["valor_venta"]})'", id_producto=dicc.get("id"), id_egreso_producto=nuevo_item["id"], ope_egreso=True)
        logs_usuario.append(etapa_usuario)
        mensaje("🛒   ITEM AGREGADO   ✓")
        print("\n")
        actualizado = True
        mostrar_menu("   Menú [AGREGAR MÁS ITEMS] →", lista_si_no, 1, 2, True, 0, "", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                clear_screen()
                mensaje(f"🛒   VENTAS DE '{dicc.get("codigo").upper()} {dicc.get("descripcion").upper()} {dicc.get("marca").upper()} {dicc.get("modelo").upper()}' ✓")
                print("\n")
                mostrar_detalle_cambio_stock(movimientos_venta, "venta")
            case 2:
                agregar_item_movimientos = False
    return id_autoinc, actualizado


def eliminar_un_item_seleccionado_movimiento_de_venta(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que elimina un movimiento de egreso (venta) de un producto determinado

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_venta = dicc["egreso"]
    clear_screen()
    mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
    mensaje("🛒   EGRESOS   →")
    mostrar_detalle_cambio_stock(movimientos_venta, "venta")
    print("\n")
    mensaje(f"🛒   INGRESAR NÚMERO DE ITEM A ELIMINAR '1' - '{len(movimientos_venta)}'  →")
    indice_item = opcion_menu_con_0(len(movimientos_venta), "Ingresar DATOS / (0) Salir") - 1
    if indice_item != -1:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   EGRESOS   →")
        mostrar_detalle_cambio_stock_seleccion(movimientos_venta, "venta", indice_item+1, indice_item+1)
        print("\n")
        mostrar_menu("   Menú [CONFIRMA ELIMINAR] →", lista_si_no, 1, 2, True, 0, "", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                actualizado = True
                movimientos_venta[indice_item]["estado"] = False
                if dicc["id"] == movimientos_venta[indice_item]["producto_id"]:
                    producto_id = dicc["id"]
                    id_item_a_eliminar = movimientos_venta[indice_item]["id"]
                    lista_items_a_eliminar = []
                    lista_items_a_eliminar.append(id_item_a_eliminar)
                    etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"elimina movimiento venta: '({movimientos_venta[indice_item]["fecha_venta"]}) - ({movimientos_venta[indice_item]["cliente_id"]}) - ({movimientos_venta[indice_item]["nro_factura_cliente"]}) - ({movimientos_venta[indice_item]["cantidad_egreso"]}) - ({movimientos_venta[indice_item]["precio_unitario"]}) - ({movimientos_venta[indice_item]["valor_venta"]})'", id_producto=producto_id, id_egreso_producto=movimientos_venta[indice_item]["id"])
                    logs_usuario.append(etapa_usuario)
                    movimientos_venta.pop(indice_item)
                    cantidad_nueva = calcular_cantidad_producto(dicc)
                    dicc.update({"cantidad": cantidad_nueva})
                    eliminar_item_producto_en_db("crud", "productos", producto_id, "cantidad", cantidad_nueva, "egresos", lista_items_a_eliminar)
                clear_screen()
                mensaje("🛒   ITEM ELIMINADO   ✓")
                mostrar_detalle_cambio_stock(movimientos_venta, "venta")
                print("\n")
            case 2:
                actualizado = False
    else:
        clear_screen()
    return id_autoinc, actualizado


def eliminar_varios_items_seleccionados_movimiento_de_venta(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que elimina varios movimientos de egreso (venta) seleccionados de un producto determinado

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_venta = dicc["egreso"]
    clear_screen()
    mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
    mensaje("🛒   EGRESOS   →")
    mostrar_detalle_cambio_stock(movimientos_venta, "venta")
    print("\n")
    mensaje(f"🛒   INGRESAR RANGO DE ITEMS A ELIMINAR   →")
    primer_item = opcion_menu_2_con_0(1, len(movimientos_venta), "'Primer ITEM'/ (0) Salir")
    if primer_item != 0:
        ultimo_item = opcion_menu_2_con_0(primer_item, len(movimientos_venta)-primer_item+1, "'Último ITEM'/ (0) Salir")
        if ultimo_item != 0:
            clear_screen()
            mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
            mensaje("🛒   SELECCIÓN DE ITEMS A ELIMINAR   →")
            mostrar_detalle_cambio_stock_seleccion(movimientos_venta, "venta", primer_item, ultimo_item)
            print("\n")
            mostrar_menu("   Menú [CONFIRMA ELIMINAR] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    actualizado = True
                    totcant = 0
                    c = 0
                    movimientos_venta_copia = movimientos_venta[:]
                    lista_items_a_eliminar = []
                    for mov in movimientos_venta_copia:
                        c += 1
                        if c >= primer_item and c <= ultimo_item:
                            totcant += mov["cantidad_egreso"]
                            mov["estado"] = False
                            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"elimina movimiento venta: '({mov["fecha_venta"]}) - ({mov["cliente_id"]}) - ({mov["nro_factura_cliente"]}) - ({mov["cantidad_egreso"]}) - ({mov["precio_unitario"]}) - ({mov["valor_venta"]})'", id_producto=dicc.get("id"), id_egreso_producto=mov["id"])
                            logs_usuario.append(etapa_usuario)
                            lista_items_a_eliminar.append(mov["id"])
                            movimientos_venta.remove(mov)
                    cantidad_nueva = calcular_cantidad_producto(dicc)
                    dicc.update({"cantidad": cantidad_nueva})
                    producto_id = dicc["id"]
                    eliminar_item_producto_en_db("crud", "productos", producto_id, "cantidad", cantidad_nueva, "egresos", lista_items_a_eliminar)
                    mensaje("🛒   ITEMs ELIMINADOs   ✓")
                case 2:
                    actualizado = False
        else:
            clear_screen()
    else:
        clear_screen()
    return id_autoinc, actualizado


def eliminar_todos_los_items_movimiento_de_venta(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que elimina todos los movimientos de egreso (venta) de un producto determinado

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_venta = dicc["egreso"]
    clear_screen()
    mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
    mensaje("🛒   EGRESOS   →")
    mostrar_detalle_cambio_stock_seleccion(movimientos_venta, "venta", 1, len(movimientos_venta))
    print("\n")
    mensaje(f"🛒   ELIMINAR LOS '{len(movimientos_venta)}' ITEMS   →")
    print("\n")
    mostrar_menu("   Menú [CONFIRMA ELIMINAR] →", lista_si_no, 1, 2, True, 0, "", "", "")
    match opcion_menu(2, "Ingresar DATOS"):
        case 1:
            actualizado = True
            totcant = 0
            movimientos_venta_copia = movimientos_venta[:]
            lista_items_a_eliminar = []
            for mov in movimientos_venta_copia:
                totcant += mov["cantidad_egreso"]
                mov["estado"] = False
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"elimina movimiento venta: '({mov["fecha_venta"]}) - ({mov["cliente_id"]}) - ({mov["nro_factura_cliente"]}) - ({mov["cantidad_egreso"]}) - ({mov["precio_unitario"]}) - ({mov["valor_venta"]})'", id_producto=dicc.get("id"), id_egreso_producto=mov["id"])
                logs_usuario.append(etapa_usuario)
                lista_items_a_eliminar.append(mov["id"])
            movimientos_venta.clear()
            cantidad_nueva = calcular_cantidad_producto(dicc)
            dicc.update({"cantidad": cantidad_nueva})
            producto_id = dicc["id"]
            eliminar_item_producto_en_db("crud", "productos", producto_id, "cantidad", cantidad_nueva, "egresos", lista_items_a_eliminar)
            mensaje("🛒   ITEMs ELIMINADOs   ✓")
        case 2:
            actualizado = False
    return id_autoinc, actualizado


def eliminar_item_movimiento_de_venta(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que permite al usuario elegir como eliminar movimientos de venta de los productos

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_venta = dicc["egreso"]
    eliminar_item_movimientos = True                                   
    while movimientos_venta and eliminar_item_movimientos:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   EGRESOS   →")
        mostrar_detalle_cambio_stock(movimientos_venta, "venta")
        print("\n")
        mostrar_menu("   Menú [ELIMINAR MOVIMIENTOS] →", lista_item_movimiento_eliminar, 1, 3, True, 1, "Menú [VOLVER]", "", "")
        match opcion_menu(4, "Ingresar DATOS"):
            case 1:
                id_autoinc, actualizado  = eliminar_un_item_seleccionado_movimiento_de_venta(dicc, usuario, logs_usuario, id_autoinc)
            case 2:
                id_autoinc, actualizado  = eliminar_varios_items_seleccionados_movimiento_de_venta(dicc, usuario, logs_usuario, id_autoinc)
            case 3:
                id_autoinc, actualizado  = eliminar_todos_los_items_movimiento_de_venta(dicc, usuario, logs_usuario, id_autoinc)
            case 4:
                actualizado = False
                eliminar_item_movimientos = False
    return id_autoinc, actualizado


def editar_item_movimiento_de_venta(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que permite al usuario 'administrador' modificar los valores de un movimiento de venta de un producto

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_venta = dicc["egreso"]
    editar_item_movimientos = True                                   
    while movimientos_venta and editar_item_movimientos:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   EGRESOS   →")
        mostrar_detalle_cambio_stock(movimientos_venta, "venta")
        print("\n")
        mensaje(f"🛒   INGRESAR NÚMERO DE ITEM A EDITAR '1' - '{len(movimientos_venta)}'  →")
        indice_item = opcion_menu_con_0(len(movimientos_venta), "Ingresar DATOS / (0) Salir") - 1
        if indice_item != -1:
            item_a_editar = movimientos_venta[indice_item]
            cantidad_mov_previa = item_a_editar.get("cantidad_egreso")
            lista_menu_claves_egresos = list (item_a_editar)[2:]
            lista_item_a_editar = []
            lista_item_a_editar.append(item_a_editar)
            clear_screen()
            mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
            print("\n")
            mostrar_detalle_cambio_stock_seleccion(lista_item_a_editar, "venta", 1, 1)
            print("\n")
            mostrar_menu("   Menú [EDITAR ITEM] →", lista_menu_claves_egresos, 1, 5, True, 1, "[SALIR]", "", "")
            ie = opcion_menu(6, "Ingresar DATOS") - 1
            if ie != 5:
                actualizado = True
                if ie == 0:
                    clave_in2 = lista_menu_claves_egresos[ie]
                    valor_in2_previo = item_a_editar.get(clave_in2)
                    valor_in2 = input(f"\n• {clave_in2.title()} ⟨Nuevo Valor 'YYYY-MM-DD'⟩: ").strip().lower()
                    while not validar_fecha(valor_in2):
                        valor_in2= input(f"\n• {clave_in2.title()} ⟨Nuevo Valor 'YYYY-MM-DD'⟩: ").strip().lower()
                    item_a_editar.update({clave_in2: valor_in2})
                elif ie == 1 or ie == 2:
                    clave_in2 = lista_menu_claves_egresos[ie]
                    valor_in2_previo = item_a_editar.get(clave_in2)
                    valor_in2 = input(f"\n• {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    while valor_in2 == "":
                        valor_in2= input(f"\n• {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    item_a_editar.update({clave_in2: valor_in2})
                elif ie == 3:
                    clave_in2 = lista_menu_claves_egresos[ie]
                    valor_in2_previo = item_a_editar.get(clave_in2)
                    valor_in2 = input(f"\n# {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    while not valor_in2.isdigit() or int(valor_in2) == 0:
                        valor_in2= input(f"\n# {clave_in2.title()} (Nuevo Valor⟩: ").strip().lower()
                    item_a_editar.update({clave_in2: int(valor_in2)})
                elif ie == 4:
                    clave_in2 = lista_menu_claves_egresos[ie]
                    valor_in2_previo = item_a_editar.get(clave_in2)
                    valor_in2 = input(f"\n$ {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    while not de_caracter_a_float(valor_in2):
                        valor_in2= input(f"\n$ {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    item_a_editar.update({clave_in2: float(valor_in2)})
                item_a_editar.update({"valor_venta": (item_a_editar.get("cantidad_egreso")*item_a_editar.get("precio_unitario"))})
                cantidad_nueva = calcular_cantidad_producto(dicc)
                dicc.update({"cantidad": cantidad_nueva})
            clear_screen()
            mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
            print("\n")
            mostrar_detalle_cambio_stock_seleccion(lista_item_a_editar, "venta", 1, 1)
            print("\n")
            if ie != 5:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"movimiento venta cambia de: {clave_in2}: '{valor_in2_previo}' a {clave_in2}: '{item_a_editar.get(clave_in2)}'", id_producto=dicc.get("id"), id_egreso_producto=movimientos_venta[indice_item]["id"])
                logs_usuario.append(etapa_usuario)
                actualizar_item_movimiento_producto_en_db("crud", "productos", "cantidad", cantidad_nueva, "egresos", item_a_editar)
                mensaje("🛒   ITEM EDITADO   ✓")
            print("\n")
            mostrar_menu("   Menú [SEGUIR EDITANDO] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    editar_item_movimientos = True
                case 2:
                    editar_item_movimientos = False
        else:
            editar_item_movimientos = False
            clear_screen()
    return id_autoinc, actualizado


def agregar_item_movimiento_de_ajuste(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que agrega un movimiento de ajuste de un producto determinado

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_ajuste = dicc["ajuste"]
    movimiento_ajuste = {"id": 0, "producto_id": 0, "fecha_ajuste": "", "detalle_ajuste": "", "cantidad_ajuste": 0, "estado": True}
    agregar_item_movimientos = True                                   
    while agregar_item_movimientos:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   AJUSTE DE STOCK   →")
        mostrar_detalle_cambio_stock(movimientos_ajuste, "ajuste")
        print("\n")
        mensaje("🛒   INGRESAR LOS DATOS: ALTAS (>0), BAJAS (<0)")
        nuevo_item = {}
        for i in movimiento_ajuste:
            if i != "fecha_ajuste" and i!= "estado":
                if isinstance(movimiento_ajuste.get(i), int):
                    if i == "id":
                        nuevo_item[i] = 0
                    elif i == "producto_id":
                        nuevo_item[i] = dicc["id"]
                    else:                    
                        valor_in= input(f"\n# {i.title()}: ").strip().lower()
                        while not valor_in.isdigit() and dicc["cantidad"] + int(valor_in) < 0:
                            valor_in= input(f"\n# {i.title()}: ").strip().lower()
                        valor_in = int(valor_in)
                        nuevo_item[i] = valor_in
                elif isinstance(movimiento_ajuste.get(i), str):
                    valor_in= input(f"\n• {i.title()}: ").strip().lower()
                    while valor_in == "":
                        valor_in= input(f"\n• {i.title()}: ").strip().lower()
                    nuevo_item[i] = valor_in
            elif i == "fecha_ajuste":
                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                nuevo_item[i] = fecha
        nuevo_item["estado"] = True
        dicc["ajuste"].append(nuevo_item)       
        cantidad_nueva = calcular_cantidad_producto(dicc)
        dicc.update({"cantidad": cantidad_nueva})
        agregar_ajuste_producto_db("crud", "productos", "cantidad", cantidad_nueva, nuevo_item["producto_id"], "ajustes", nuevo_item)
        nuevo_item.update({"id": traer_id_mov_desde_db("crud", "ajustes", nuevo_item)})
        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"agrega movimiento ajuste: '({nuevo_item["fecha_ajuste"]}) - ({nuevo_item["detalle_ajuste"]}) - ({nuevo_item["cantidad_ajuste"]})'", id_producto=dicc.get("id"), id_ajuste_producto=nuevo_item["id"], ope_ajuste=True)
        logs_usuario.append(etapa_usuario)
        mensaje("🛒   ITEM AGREGADO   ✓")
        print("\n")
        actualizado = True
        mostrar_menu("   Menú [AGREGAR MÁS ITEMS] →", lista_si_no, 1, 2, True, 0, "", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                clear_screen()
                mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
                mensaje("🛒   INGRESOS   →")
                print("\n")
                mostrar_detalle_cambio_stock(movimientos_ajuste, "ajuste")
            case 2:
                agregar_item_movimientos = False
    return id_autoinc, actualizado


def eliminar_un_item_seleccionado_movimiento_de_ajuste(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que elimina un movimiento de ajuste de un producto determinado

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_ajuste = dicc["ajuste"]
    clear_screen()
    mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
    mensaje("🛒   AJUSTES   →")
    mostrar_detalle_cambio_stock(movimientos_ajuste, "ajuste")
    print("\n")
    mensaje(f"🛒   INGRESAR NÚMERO DE ITEM A ELIMINAR '1' - '{len(movimientos_ajuste)}'  →")
    indice_item = opcion_menu_con_0(len(movimientos_ajuste), "Ingresar DATOS / (0) Salir") - 1
    if indice_item != -1:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   AJUSTES   →")
        mostrar_detalle_cambio_stock_seleccion(movimientos_ajuste, "ajuste", indice_item+1, indice_item+1)
        print("\n")
        mostrar_menu("   Menú [CONFIRMA ELIMINAR] →", lista_si_no, 1, 2, True, 0, "", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                actualizado = True
                movimientos_ajuste[indice_item]["estado"] = False
                if dicc["id"] == movimientos_ajuste[indice_item]["producto_id"]:
                    producto_id = dicc["id"]
                    id_item_a_eliminar = movimientos_ajuste[indice_item]["id"]
                    lista_items_a_eliminar = []
                    lista_items_a_eliminar.append(id_item_a_eliminar)
                    etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"elimina movimiento ajuste: '({movimientos_ajuste[indice_item]["fecha_ajuste"]}) - ({movimientos_ajuste[indice_item]["detalle_ajuste"]}) - ({movimientos_ajuste[indice_item]["cantidad_ajuste"]})'", id_producto=producto_id, id_ajuste_producto=movimientos_ajuste[indice_item]["id"])
                    logs_usuario.append(etapa_usuario)
                    movimientos_ajuste.pop(indice_item)
                    cantidad_nueva = calcular_cantidad_producto(dicc)
                    dicc.update({"cantidad": cantidad_nueva})
                    eliminar_item_producto_en_db("crud", "productos", producto_id, "cantidad", cantidad_nueva, "ajustes", lista_items_a_eliminar)
                clear_screen()
                mensaje("🛒   ITEM ELIMINADO   ✓")
                mostrar_detalle_cambio_stock(movimientos_ajuste, "ajuste")
                print("\n")
            case 2:
                actualizado = False
    else:
        clear_screen()
    return id_autoinc, actualizado


def eliminar_varios_items_seleccionados_movimiento_de_ajuste(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que elimina varios movimientos de ajuste seleccionados de un producto determinado

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_ajuste = dicc["ajuste"]
    clear_screen()
    mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
    mensaje("🛒   AJUSTES   →")
    mostrar_detalle_cambio_stock(movimientos_ajuste, "ajuste")
    print("\n")
    mensaje(f"🛒   INGRESAR RANGO DE ITEMS A ELIMINAR   →")
    primer_item = opcion_menu_2_con_0(1, len(movimientos_ajuste), "'Primer ITEM'/ (0) Salir")
    if primer_item != 0:
        ultimo_item = opcion_menu_2_con_0(primer_item, len(movimientos_ajuste)-primer_item+1, "'Último ITEM'/ (0) Salir")
        if ultimo_item != 0:
            clear_screen()
            mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
            mensaje("🛒   SELECCIÓN DE ITEMS A ELIMINAR   →")
            mostrar_detalle_cambio_stock_seleccion(movimientos_ajuste, "ajuste", primer_item, ultimo_item)
            print("\n")
            mostrar_menu("   Menú [CONFIRMA ELIMINAR] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    actualizado = True
                    totcant = 0
                    c = 0
                    movimientos_ajuste_copia = movimientos_ajuste[:]
                    lista_items_a_eliminar = []
                    for mov in movimientos_ajuste_copia:
                        c += 1
                        if c >= primer_item and c <= ultimo_item:
                            totcant += mov["cantidad_ajuste"]
                            mov["estado"] = False
                            etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"elimina movimiento ajuste: '({mov["fecha_ajuste"]}) - ({mov["detalle_ajuste"]}) - ({mov["cantidad_ajuste"]})'", id_producto=dicc.get("id"), id_ajuste_producto=mov["id"])
                            logs_usuario.append(etapa_usuario)
                            lista_items_a_eliminar.append(mov["id"])
                            movimientos_ajuste.remove(mov)
                    cantidad_nueva = calcular_cantidad_producto(dicc)
                    dicc.update({"cantidad": cantidad_nueva})
                    producto_id = dicc["id"]
                    eliminar_item_producto_en_db("crud", "productos", producto_id, "cantidad", cantidad_nueva, "ajustes", lista_items_a_eliminar)
                    mensaje("🛒   ITEMs ELIMINADOs   ✓")
                    eliminar_item_movimientos = False
                case 2:
                    actualizado = False
        else:
            clear_screen()
    else:
        clear_screen()
    return id_autoinc, actualizado


def eliminar_todos_los_items_movimiento_de_ajuste(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que elimina todos los movimientos ajuste de un producto determinado

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_ajuste = dicc["ajuste"]
    clear_screen()
    mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
    mensaje("🛒   AJUSTES   →")
    mostrar_detalle_cambio_stock_seleccion(movimientos_ajuste, "ajuste", 1, len(movimientos_ajuste))
    print("\n")
    mensaje(f"🛒   ELIMINAR LOS '{len(movimientos_ajuste)}' ITEMS   →")
    print("\n")
    mostrar_menu("   Menú [CONFIRMA ELIMINAR] →", lista_si_no, 1, 2, True, 0, "", "", "")
    match opcion_menu(2, "Ingresar DATOS"):
        case 1:
            actualizado = True
            totcant = 0
            movimientos_ajuste_copia = movimientos_ajuste[:]
            lista_items_a_eliminar = []
            for mov in movimientos_ajuste_copia:
                totcant += mov["cantidad_ajuste"]
                mov["estado"] = False
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"elimina movimiento ajuste: '({mov["fecha_ajuste"]}) - ({mov["detalle_ajuste"]}) - ({mov["cantidad_ajuste"]})'", id_producto=dicc.get("id"), id_ajuste_producto=mov["id"])
                logs_usuario.append(etapa_usuario)
                lista_items_a_eliminar.append(mov["id"])
            movimientos_ajuste.clear()
            cantidad_nueva = calcular_cantidad_producto(dicc)
            dicc.update({"cantidad": cantidad_nueva})
            producto_id = dicc["id"]
            eliminar_item_producto_en_db("crud", "productos", producto_id, "cantidad", cantidad_nueva, "ajustes", lista_items_a_eliminar)
            mensaje("🛒   ITEMs ELIMINADOs   ✓")
        case 2:
            actualizado = False
    return id_autoinc, actualizado


def eliminar_item_movimiento_de_ajuste(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que permite al usuario elegir como eliminar movimientos de ajuste de los productos

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_ajuste = dicc["ajuste"]
    eliminar_item_movimientos = True                                   
    while movimientos_ajuste and eliminar_item_movimientos:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   AJUSTES   →")
        mostrar_detalle_cambio_stock(movimientos_ajuste, "ajuste")
        print("\n")
        mostrar_menu("   Menú [ELIMINAR MOVIMIENTOS] →", lista_item_movimiento_eliminar, 1, 3, True, 1, "Menú [VOLVER]", "", "")
        match opcion_menu(4, "Ingresar DATOS"):
            case 1:
                id_autoinc, actualizado  = eliminar_un_item_seleccionado_movimiento_de_ajuste(dicc, usuario, logs_usuario, id_autoinc)
            case 2:
                id_autoinc, actualizado  = eliminar_varios_items_seleccionados_movimiento_de_ajuste(dicc, usuario, logs_usuario, id_autoinc)
            case 3:
                id_autoinc, actualizado  = eliminar_todos_los_items_movimiento_de_ajuste(dicc, usuario, logs_usuario, id_autoinc)
            case 4:
                actualizado = False
                eliminar_item_movimientos = False
    return id_autoinc, actualizado


def editar_item_movimiento_de_ajuste(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que permite al usuario 'administrador' modificar los valores de un movimiento de ajuste de un producto

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizar = False
    movimientos_ajuste = dicc["ajuste"]
    editar_item_movimientos = True                                   
    while movimientos_ajuste and editar_item_movimientos:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   AJUSTES   →")
        mostrar_detalle_cambio_stock(movimientos_ajuste, "ajuste")
        print("\n")
        mensaje(f"🛒   INGRESAR NÚMERO DE ITEM A EDITAR '1' - '{len(movimientos_ajuste)}'  →")
        indice_item = opcion_menu_con_0(len(movimientos_ajuste), "Ingresar DATOS / (0) Salir") - 1
        if indice_item != -1:
            item_a_editar = movimientos_ajuste[indice_item]
            cantidad_mov_previa = item_a_editar.get("cantidad_ajuste")
            lista_menu_claves_ajustes = list (item_a_editar)[2:]
            lista_item_a_editar = []
            lista_item_a_editar.append(item_a_editar)
            clear_screen()
            mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
            print("\n")
            mostrar_detalle_cambio_stock_seleccion(lista_item_a_editar, "ajuste", 1, 1)
            print("\n")
            mostrar_menu("   Menú [EDITAR ITEM] →", lista_menu_claves_ajustes, 1, 3, True, 1, "[SALIR]", "", "")
            ie = opcion_menu(4, "Ingresar DATOS") - 1
            if ie != 3:
                actualizar = True
                if ie == 0:
                    clave_in2 = lista_menu_claves_ajustes[ie]
                    valor_in2_previo = item_a_editar.get(clave_in2)
                    valor_in2 = input(f"\n• {clave_in2.title()} ⟨Nuevo Valor 'YYYY-MM-DD'⟩: ").strip().lower()
                    while not validar_fecha(valor_in2):
                        valor_in2= input(f"\n• {clave_in2.title()} ⟨Nuevo Valor 'YYYY-MM-DD'⟩: ").strip().lower()
                    item_a_editar.update({clave_in2: valor_in2})
                elif ie == 1:
                    clave_in2 = lista_menu_claves_ajustes[ie]
                    valor_in2_previo = item_a_editar.get(clave_in2)
                    valor_in2 = input(f"\n• {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    while valor_in2 == "":
                        valor_in2= input(f"\n• {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    item_a_editar.update({clave_in2: valor_in2})
                elif ie == 2:
                    clave_in2 = lista_menu_claves_ajustes[ie]
                    valor_in2_previo = item_a_editar.get(clave_in2)
                    valor_in2 = input(f"\n# {clave_in2.title()} ⟨Nuevo Valor⟩: ").strip().lower()
                    while not valor_in2.isdigit() and (len(valor_in2) <= 1 or valor_in2[0:1] !="-" or not valor_in2[1:].isdigit()):
                        valor_in2= input(f"\n# {clave_in2.title()} (Nuevo Valor⟩: ").strip().lower()
                    item_a_editar.update({clave_in2: int(valor_in2)})
                cantidad_nueva = calcular_cantidad_producto(dicc)
                dicc.update({"cantidad": cantidad_nueva})
            clear_screen()
            mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
            print("\n")
            mostrar_detalle_cambio_stock_seleccion(lista_item_a_editar, "ajuste", 1, 1)
            print("\n")
            if ie != 5:
                etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"movimiento ajuste cambia de: {clave_in2}: '{valor_in2_previo}' a {clave_in2}: '{item_a_editar.get(clave_in2)}'", id_producto=dicc.get("id"), id_ajuste_producto=movimientos_ajuste[indice_item]["id"])
                logs_usuario.append(etapa_usuario)
                actualizar_item_movimiento_producto_en_db("crud", "productos", "cantidad", cantidad_nueva, "ajustes", item_a_editar)
                mensaje("🛒   ITEM EDITADO   ✓")
            print("\n")
            mostrar_menu("   Menú [SEGUIR EDITANDO] →", lista_si_no, 1, 2, True, 0, "", "", "")
            match opcion_menu(2, "Ingresar DATOS"):
                case 1:
                    editar_item_movimientos = True
                case 2:
                    editar_item_movimientos = False
        else:
            editar_item_movimientos = False
            clear_screen()
    return id_autoinc, actualizar


def actualizar_movimientos_de_compra_de_productos(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que permite al usuario elegir que tipo de operación realizar sobre los movimientos de compra de un producto

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_compra = dicc["ingreso"]
    mostrar_detalle_cambio_stock(movimientos_compra, "compra")                                              
    items_movimientos_compra = True
    while items_movimientos_compra:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   INGRESOS   →")
        mostrar_detalle_cambio_stock(movimientos_compra, "compra")
        print("\n")
        mostrar_menu("   Menú [DETALLE DE MOVIMIENTOS] →", lista_item_movimiento, 1, 3, True, 1, "Menú [VOLVER]", "", "")
        match opcion_menu(4, "Ingresar DATOS"):
            case 1:
                id_autoinc, actualizado  = agregar_item_movimiento_de_compra(dicc, usuario, logs_usuario, id_autoinc)
            case 2:
                id_autoinc, actualizado  = eliminar_item_movimiento_de_compra(dicc, usuario, logs_usuario, id_autoinc)
            case 3:
                id_autoinc, actualizado  = editar_item_movimiento_de_compra(dicc, usuario, logs_usuario, id_autoinc)
            case 4: # volver a menú de movimientos de compra
                actualizado = False
                items_movimientos_compra = False
    return id_autoinc, actualizado


def actualizar_movimientos_de_venta_de_productos(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que permite al usuario elegir que tipo de operación realizar sobre los movimientos de venta de un producto

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_venta = dicc["egreso"]
    mostrar_detalle_cambio_stock(movimientos_venta, "venta")                                              
    items_movimientos_venta = True
    while items_movimientos_venta:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   EGRESOS   →")
        mostrar_detalle_cambio_stock(movimientos_venta, "venta")
        print("\n")
        mostrar_menu("   Menú [DETALLE DE MOVIMIENTOS] →", lista_item_movimiento, 1, 3, True, 1, "Menú [VOLVER]", "", "")
        match opcion_menu(4, "Ingresar DATOS"):
            case 1:
                id_autoinc, actualizado  = agregar_item_movimiento_de_venta(dicc, usuario, logs_usuario, id_autoinc)
            case 2:
                id_autoinc, actualizado  = eliminar_item_movimiento_de_venta(dicc, usuario, logs_usuario, id_autoinc)
            case 3:
                id_autoinc, actualizado  = editar_item_movimiento_de_venta(dicc, usuario, logs_usuario, id_autoinc)
            case 4: # volver a menú de movimientos de venta
                actualizado = False
                items_movimientos_venta = False
    return id_autoinc, actualizado


def actualizar_movimientos_de_ajuste_de_productos(dicc, usuario, logs_usuario, id_autoinc):
    """_Función que permite al usuario elegir que tipo de operación realizar sobre los movimientos de ajuste de un producto

    Args:
        dicc (dict): producto a agregar un movimiento
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json
    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    movimientos_ajuste = dicc["ajuste"]
    mostrar_detalle_cambio_stock(movimientos_ajuste, "ajuste")                                              
    items_movimientos_ajuste = True
    while items_movimientos_ajuste:
        clear_screen()
        mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
        mensaje("🛒   AJUSTE DE STOCK   →")
        mostrar_detalle_cambio_stock(movimientos_ajuste, "ajuste")
        print("\n")
        mostrar_menu("   Menú [DETALLE DE MOVIMIENTOS] →", lista_item_movimiento, 1, 3, True, 1, "Menú [VOLVER]", "", "")
        match opcion_menu(4, "Ingresar DATOS"):
            case 1:
                id_autoinc, actualizado  = agregar_item_movimiento_de_ajuste(dicc, usuario, logs_usuario, id_autoinc)
            case 2:
                id_autoinc, actualizado  = eliminar_item_movimiento_de_ajuste(dicc, usuario, logs_usuario, id_autoinc)
            case 3:
                id_autoinc, actualizado  = editar_item_movimiento_de_ajuste(dicc, usuario, logs_usuario, id_autoinc)
            case 4: # volver a menú de movimientos de compra
                items_movimientos_ajuste = False
    return id_autoinc, actualizado


def actualizar_atributos_producto_no_cantidad_no_precio(dicc, i, usuario, logs_usuario, id_autoinc):
    """Función que permite modificar los valores de los atributos de un producto, menos la cantidad y el precio

    Args:
        dicc (dict): producto a agregar un movimiento
        i (int): valor entre 1 y 7 (opciones de atributo = 1: 'codigo', 2: 'descripcion', 3: 'marca', 4: 'modelo', 5: 'categoria', 6: 'origen', 7: 'ubicacion')
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    if i>=1 and i<=7:
        actualizado = True
        clave = list(dicc)[i]
        valor_anterior = dicc.get(clave)
        valor = input(f"\n• {clave.title()} ⟨Nuevo Nombre⟩: ").strip().lower()
        while valor == "":
            valor= input(f"\n• {clave.title()} ⟨Nuevo Nombre⟩: ").strip().lower()
        dicc.update({clave: valor})
        lista_items_a_actualizar = []
        lista_items_a_actualizar.append(dicc["id"])
        etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"producto: '{dicc.get("codigo")} - {dicc.get("marca")}' actualizado cambia {clave.title()} de valor {valor_anterior} a {valor}", id_producto=dicc.get("id"))
        logs_usuario.append(etapa_usuario)
        actualizar_item_producto_en_db("crud", "productos", lista_items_a_actualizar, clave, valor)
    return id_autoinc, actualizado


def actualizar_precio_producto(dicc, usuario, logs_usuario, id_autoinc ,i=8):
    """Función que permite modificar el valor del precio de un producto

    Args:
        dicc (dict): producto a agregar un movimiento
        i (int): valor entero (opciones de atributo = 8: 'precio')
        usuario (dict): usuario que hace la operación
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no 
    """
    actualizado = False
    clave = list(dicc)[i]
    valor_anterior = dicc.get(clave)
    valor = input(f"\n$ {clave.title()} ⟨Nuevo Valor⟩: ").strip().lower()
    while not de_caracter_a_float(valor):
        valor = input(f"\n$ {clave.title()} ⟨Nuevo Valor⟩: ").strip().lower()
    valor = float(valor)
    dicc.update({clave: valor})
    actualizado = True
    lista_items_a_actualizar = []
    lista_items_a_actualizar.append(dicc["id"])
    etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"producto: '{dicc.get("codigo")} - {dicc.get("marca")}' actualizado cambia {clave.title()} de valor {valor_anterior} a {valor}", id_producto=dicc.get("id"))
    logs_usuario.append(etapa_usuario)
    actualizar_item_producto_en_db("crud", "productos", lista_items_a_actualizar, clave, valor)
    return id_autoinc, actualizado


def actualizar_atributos_producto(productos, producto_a_actualizar, usuario, logs_usuario, id_autoinc):
    """Función que permite seleccionar qué atributo del producto seleccionado será modificado en su valor, excepto la cantidad

    Args:
        productos (list): lista de productos
        producto_a_actualizar (list): producto a actualizar
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no
    """
    actualizado = False
    dicc = producto_a_actualizar[0]
    print("\n")
    mostrar_menu("   Menú [EDITAR PRODUCTOS] →", lista_menu_claves_producto, 2, 8, True, 1, "[SALIR]", "", "")
    i = opcion_menu(9, "Ingresar DATOS")
    if i != 9:
        if i <= 7: 
            id_autoinc, actualizado = actualizar_atributos_producto_no_cantidad_no_precio(dicc, i, usuario, logs_usuario, id_autoinc)
        elif i == 8:
            id_autoinc, actualizado = actualizar_precio_producto(dicc, usuario, logs_usuario, id_autoinc ,i=9)
        productos_copia = productos[:]
        for producto in productos_copia:
            if producto["id"] == dicc["id"]:
                productos.remove(producto)
                productos.append(dicc)
        actualizado = True
    return productos, id_autoinc, actualizado


def actualizar_movimientos_producto(productos, producto_a_actualizar, usuario, logs_usuario, id_autoinc):
    """Función que permite seleccionar qué tipo de movimiento (compra/venta/ajuste) se va a modificar de un producto determinado

    Args:
        productos (list): lista de productos
        producto_a_actualizar (list): producto a actualizar
        usuario (dict): usuario del sistema
        logs_usuario (list): registro de acciones del usuario en el sistema
        id_autoinc (int): variable autoincremental que cursa a través de todo el programa y que da un id único a cada evento para que pueda registrarse en un archivo json

    Returns:
        id_autoinc (int): variable id autoincremental
        actualizado (bool): variable con valor true/false de acuerdo a si se agregó un movimiento a no
    """
    actualizado = False
    dicc = producto_a_actualizar[0]
    print("\n")
    clear_screen()
    mensaje(f"🛒   ™ {dicc.get("codigo").upper()} → {dicc.get("marca").upper()} {dicc.get("modelo").upper()}, '{dicc.get("descripcion").upper()}', # {dicc.get("cantidad")}, $ {dicc.get("precio")} ")
    mostrar_lista(producto_a_actualizar)
    print("\n")
    mostrar_menu("   Menú [CAMBIAR STOCK POR] →", lista_cambio_stock, 1, 3, True, 1, "Menú [VOLVER]", "", "")
    match opcion_menu(4, "Ingresar DATOS"):
        case 1:
            id_autoinc, actualizado = actualizar_movimientos_de_compra_de_productos(dicc, usuario, logs_usuario, id_autoinc)
        case 2:
            id_autoinc, actualizado = actualizar_movimientos_de_venta_de_productos(dicc, usuario, logs_usuario, id_autoinc)
        case 3:
            id_autoinc, actualizado  = actualizar_movimientos_de_ajuste_de_productos(dicc, usuario, logs_usuario, id_autoinc)
        case 4:
            actualizado = False
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    dicc.update({"fecha_modificacion": fecha})
    productos_copia = productos[:]
    for producto in productos_copia:
        if producto["id"] == dicc["id"]:
            productos.remove(producto)
            productos.append(dicc)
    return productos, id_autoinc, actualizado


def buscar_producto(lis, cla):
    """funcion que devuelve una lista de diccionario de un producto que fue encontrado en una lista a partir de una clave

    Args:
        lis (list): lista
        cla (str): clave

    Returns:
        list: lista de iguales
    """
    lista_iguales = []
    producto_a_buscar= input(f"\n• {cla.title()}: ").strip().lower()
    while producto_a_buscar == "":
        producto_a_buscar = input(f"\n• {cla.title()}: ").strip().lower()
    for i in lis:
        if producto_a_buscar == i.get(cla):
            lista_iguales.append(dict(i.items()))
    return lista_iguales


def buscar_producto_2(lis, cla, val):
    """funcion que devuelve una lista de diccionario de un producto que fue encontrado en una lista a partir de una clave/valor pasadas como argumentos

    Args:
        lis (list): lista
        cla (str): clave
        val (_type_): valor

    Returns:
        _type_: _description_
    """
    lista_iguales = []
    for i in lis:
        if val == i.get(cla):
            lista_iguales.append(dict(i.items()))
    return lista_iguales


def agregar_producto():
    """Función que crea un nuevo producto

    Returns:
        producto (dict): nuevo producto
    """
    producto = {"id": 0, "descripcion": "", "codigo": "", "marca": "", "modelo": "", "categoria": "", "origen": "", "ubicacion": "", "cantidad": 0, "precio": 0.0, "ingreso": [], "egreso": [], "ajuste": [], "fecha_modificacion": "", "fecha_alta": "", "fecha_baja": "", "estado": True}
    for i in producto:
        clave = i
        contenido_clave = producto.get(i)
        if clave != "id" and clave != "cantidad" and clave != "fecha_modificacion" and clave != "fecha_alta" and clave != "fecha_baja" and clave != "estado":                             
            if isinstance(contenido_clave, str):
                valor= input(f"\n• {clave.title()}: ").strip().lower()
                while valor == "":
                    valor= input(f"\n• {clave.title()}: ").strip().lower()
                producto[i] = valor
            elif isinstance(contenido_clave, float):
                valor= input(f"\n$ {clave.title()}: ").strip().lower()
                while not de_caracter_a_float(valor):
                    valor= input(f"\n$ {clave.title()}: ").strip().lower()
                valor = float(valor)
                producto[i] = valor
            elif isinstance(contenido_clave, list):
                producto[i] = []
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")                
    producto["fecha_alta"] = fecha
    return producto 


def buscar_codigo(lis):
    """Función para buscar un producto comenzado con el código del mismo y devolviendo una lista como resultado

    Args:
        lis (list): lista de productos
    """
    producto_a_actualizar = []
    bucle_codigo = True
    productos_codigo = []
    while bucle_codigo:
        clear_screen()
        mensaje(f"🛒   INGRESAR CÓDIGO DEL PRODUCTO   →")
        productos_codigo = buscar_producto(lis, "codigo")
        if len(productos_codigo) == 1:
            clear_screen()
            producto_a_actualizar = productos_codigo
            mensaje("🛒   PRODUCTO ENCONTRADO   ✓")
            mostrar_lista(productos_codigo)
            bucle_codigo = False
        elif len(productos_codigo) > 1:
            bucle_marca = True
            productos_marca = []
            while bucle_marca:
                #clear_screen()
                mostrar_lista(ordenar_lista(productos_codigo, "codigo", "descripcion", "marca", True))
                mensaje(f"🛒   INGRESAR MARCA PRODUCTO CON CÓDIGO '{productos_codigo[0].get("codigo").title()}'  →")
                productos_marca = buscar_producto(productos_codigo, "marca")
                if len(productos_marca) == 1:
                    clear_screen()
                    producto_a_actualizar = productos_marca
                    mensaje("🛒   PRODUCTO ENCONTRADO   ✓")
                    mostrar_lista(productos_marca)
                    bucle_marca = False
                    bucle_codigo = False
                elif len(productos_marca) > 1:
                    clear_screen()
                    mensaje("🛒   PRODUCTO DUPLICADO / IR A MENÚ MANTENIMIENTO   ✕")
                    mostrar_lista(ordenar_lista(productos_marca, "codigo", "descripcion", "marca", True))
                    producto_a_actualizar = productos_marca
                    bucle_marca = False
                    bucle_codigo = False
                else:
                    clear_screen()
                    mensaje(f"🛒   MARCA INEXISTENTE PARA CÓDIGO '{productos_codigo[0].get("codigo").title()}'  ✕")
                    mostrar_menu("   Menú [BUSCAR POR ⟨MARCA⟩•⟨CÓDIGO⟩] →", lista_menu_claves_producto, 4, 2, False, 1, "Menú [ACTUALIZAR PRODUCTOS]", "", "")
                    match opcion_menu(3, "Ingresar DATOS"):
                        case 1:
                            clear_screen()
                            bucle_marca = True
                        case 2:
                            clear_screen()
                            bucle_marca = False
                            bucle_codigo = True
                        case 3:
                            clear_screen()
                            bucle_marca = False
                            bucle_codigo = False
        else:
            clear_screen()
            mensaje("🛒   CÓDIGO INEXISTENTE   ✕")
            bucle_codigo = False
    return producto_a_actualizar 


def encontrar_producto(lis):
    """funcion que devuelve una lista de productos encontrados a través de una búsqueda por claves pedidas en forma intervactiva comenzando por la descripción cuando se llama a esta función

    Args:
        lis (list): lista de productos
    """
    producto_encontrado = []
    item_descripcion = []
    while len(item_descripcion) == 0:
        clear_screen()
        mensaje("🛒   INGRESE LA DESCRIPCIÓN DEL PRODUCTO   →")
        item_descripcion = buscar_producto(lis, "descripcion")
        if len(item_descripcion) > 1:
            clear_screen()
            mensaje(f"🛒   PRODUCTOS CON DESCRIPCIÓN '{item_descripcion[0].get("descripcion").upper()}'   →")
            mostrar_lista(ordenar_lista(item_descripcion, "codigo", "descripcion", "marca", True))
            item_codigo = []
            while len(item_codigo) == 0:
                #clear_screen()
                mensaje(F"🛒   INGRESE EL CÓDIGO DEL PRODUCTO '{item_descripcion[0].get("descripcion").upper()}'  →")
                item_codigo = buscar_producto(item_descripcion, "codigo")
                if len(item_codigo) > 1:
                        clear_screen()
                        mensaje(f"🛒   PRODUCTO '{item_descripcion[0].get("descripcion").upper()}' CON CÓDIGO '{item_codigo[0].get("codigo").upper()}'   →")
                        mostrar_lista(ordenar_lista(item_codigo, "codigo", "descripcion", "marca", True))
                        item_marca = []
                        while len(item_marca) == 0:
                            #clear_screen()
                            mensaje(f"🛒   PRODUCTO '{item_descripcion[0].get("descripcion").upper()}' CON CÓDIGO '{item_codigo[0].get("codigo").upper()}'   →")
                            item_marca = buscar_producto(item_codigo, "marca")                       
                            if len(item_marca) == 1:
                                clear_screen()
                                mensaje("🛒   PRODUCTO ENCONTRADO   ✓")
                                mostrar_lista(item_marca)
                                producto_encontrado = item_marca
                            elif len(item_marca) > 1:
                                clear_screen()
                                mensaje("🛒   PRODUCTO DUPLICADO / IR A MENÚ MANTENIMIENTO   ✕")
                                mostrar_lista(item_marca)
                                producto_encontrado = item_marca
                            else:
                                clear_screen()
                                mensaje("🛒   MARCA INEXISTENTE   ✕")
                                mensaje(f"🛒   PRODUCTO '{item_descripcion[0].get("descripcion").upper()}' CON CÓDIGO '{item_codigo[0].get("codigo").upper()}'   →")
                                mostrar_menu("   Menú [MARCA • CÓDIGO • DESCRIPCIÓN] →", lista_menu_claves_producto, 4, 3, False, 1, "Menú [BUSCAR PRODUCTO]", "", "")
                                match opcion_menu(4, "Ingresar DATOS"):
                                    case 1:
                                        item_marca = []
                                    case 2:
                                        item_marca = [1]
                                        item_codigo = []
                                    case 3:
                                        item_marca = [1]
                                        item_codigo = [1]
                                        item_descripcion = []
                                    case 4:
                                        clear_screen()
                                        item_marca = [1]
                                        item_codigo = [1]
                                        item_descripcion = [1]                                
                elif len(item_codigo) == 1:
                    clear_screen()
                    mensaje("🛒   PRODUCTO ENCONTRADO   ✓")
                    mostrar_lista(item_codigo)
                    producto_encontrado = item_codigo
                else:
                    clear_screen()
                    mensaje("🛒   CÓDIGO INEXISTENTE   ✕")
                    mensaje(f"🛒   PRODUCTO '{item_descripcion[0].get("descripcion").upper()}'   →")
                    mostrar_menu("   Menú [CÓDIGO • DESCRIPCIÓN] →", lista_menu_claves_producto, 3, 2, False, 1, "Menú [BUSCAR PRODUCTO]", "", "")
                    match opcion_menu(3, "Reingresar DATOS"):
                        case 1:
                            item_codigo = []
                        case 2:
                            item_codigo = [1]
                            item_descripcion = []
                        case 3:
                            clear_screen()
                            item_codigo = [1]
                            item_descripcion = [1]
        elif len(item_descripcion) == 1:
            clear_screen()
            mensaje("🛒   PRODUCTO ENCONTRADO   ✓")
            mostrar_lista(item_descripcion)
            producto_encontrado = item_descripcion
        else:
            clear_screen()
            mensaje("🛒   DESCRIPCIÓN INEXISTENTE   ✕")
            mostrar_menu("   Menú [DESCRIPCIÓN] →", lista_menu_claves_producto, 2, 1, True, 1, "Menú [BUSCAR PRODUCTO]", "", "")
            match opcion_menu(2, "Reingresar DATOS"):
                case 1:
                    item_descripcion = []
                case 2:
                    clear_screen()
                    item_descripcion = [1]
    return producto_encontrado



def encontrar_producto_por_descripcion(lis):
    """funcion que devuelve una lista de productos encontrados a través de una búsqueda por claves pedidas en forma intervactiva comenzando por la descripción cuando se llama a esta función

    Args:
        lis (list): lista de productos
    """
    producto_encontrado = []
    item_descripcion = []
    while len(item_descripcion) == 0:
        clear_screen()
        mensaje("🛒   INGRESE LA DESCRIPCIÓN DEL PRODUCTO   →")
        item_descripcion = buscar_producto(lis, "descripcion")
        if len(item_descripcion) > 1:
            clear_screen()
            mensaje(f"🛒   PRODUCTOS CON DESCRIPCIÓN '{item_descripcion[0].get("descripcion").upper()}'   →")
            mostrar_lista(ordenar_lista(item_descripcion, "codigo", "descripcion", "marca", True))
            print()
            mensaje(F"🛒   INGRESE EL ID DEL PRODUCTO '{item_descripcion[0].get("descripcion").upper()}'  →")
            producto_encontrado = []
            valor_id = input("\n# Producto Id: ").strip().lower()
            while not valor_id.isdigit():
                valor_id = input("\n# Producto Id: ").strip().lower()
            valor_id = int(valor_id)
            for producto in item_descripcion:
                if producto["id"] == valor_id:
                    producto_encontrado.append(producto)
        elif len(item_descripcion) == 1:
            clear_screen()
            mensaje("🛒   PRODUCTO ENCONTRADO   ✓")
            mostrar_lista(item_descripcion)
            producto_encontrado = item_descripcion
        else:
            clear_screen()
            mensaje("🛒   DESCRIPCIÓN INEXISTENTE   ✕")
            mostrar_menu("   Menú [DESCRIPCIÓN] →", lista_menu_claves_producto, 2, 1, True, 1, "Menú [BUSCAR PRODUCTO]", "", "")
            match opcion_menu(2, "Reingresar DATOS"):
                case 1:
                    item_descripcion = []
                case 2:
                    clear_screen()
                    item_descripcion = [1]
    return producto_encontrado


def encontrar_producto_por_id(productos):
    """Función que busca un producto por su id y lo devuelve si lo encuentra

    Args:
        productos (list): lista de productos

    Returns:
        producto_encontrado (dict) / false(bool): devuelve el producto si fue encontrado o fase si no
    """
    clear_screen()
    mensaje("🛒   INGRESE EL ID DEL PRODUCTO   →")
    producto_encontrado = []
    valor_id = input("\n# Producto Id: ").strip().lower()
    while not valor_id.isdigit():
        valor_id = input("\n# Producto Id: ").strip().lower()
    valor_id = int(valor_id)
    for producto in productos:
        if producto["id"] == valor_id:
            producto_encontrado.append(producto)
            return producto_encontrado
    clear_screen()
    mensaje("🛒   ID INEXISTENTE   ✕")
    return False

