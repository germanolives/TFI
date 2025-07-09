from utilidades import convertir_segundos_a_horas
from colorama import Fore as Color, init
init(autoreset=True)


def imprimir_lista(lis, msj):
    """función que muestra una lista ordenada de un solo campo del producto

    Args:
        lis (list): lista de productos
        msj (str): mensaje
    """
    print("-" * 80)
    print(f"🛒  {msj} ")
    print("-" * 80)
    lis.sort()
    for i in lis:
        print(f"→   {i.upper()}")
    print("-" * 80)


def imprimir_lista_dos_valores(lis, msj):
    """función que muestra una lista ordenada con dos campos del producto

    Args:
        lis (list): lista de productos
        msj (str): mensaje
    """
    print("-" * 80)
    print(f"🛒  {msj} ")
    print("-" * 80)
    lis.sort()
    for i in lis:
        print(f"→   {i[0].upper():<8}\t ™ {i[1].title():<8}")
    print("-" * 80)

 
def mensaje(x):
    """funcion que muestra mensajes pasados como argumentos según corresponda

    Args:
        x (str): mensaje a mostrar
    """
    print(f"{Color.GREEN}-" * 80)
    print(f"{Color.GREEN}{x}")
    print(f"{Color.GREEN}-" * 80)


def mensaje_2(x):
    """funcion que muestra mensajes pasados como argumentos según corresponda con un logo de carrito de compras

    Args:
        x (str): mensaje a mostrar
    """
    print(f"{Color.GREEN}-" * 80)
    print(f"{Color.GREEN}🛒   {x}")
    print(f"{Color.GREEN}-" * 80)


def mostrar_menu(msj, licla, primer_item_licla, items_licla, orden_licla, items_volver, volver_atras1, volver_atras2, volver_atras3):
    """función que genera menúes en pantalla a partir de parámetros dados

    Args:
        msj (str): nombre del menú
        licla (list): lista con valores de las opciones del menú
        primer_item_licla (int): primer valor de las opciones del menú
        items_licla (int): cantidad de opciones de ese menú a partir del primer item del menú
        orden_licla (bool): ascendente o descendente
        items_volver (int): cantidad (1 a 3) de items de retorno en el menú
        volver_atras1 (str): volver 
        volver_atras2 (str): Volver +
        volver_atras3 (str): Volver ++
    """
    print(f"{Color.BLUE}=" * 80)
    print(f"{Color.BLUE}🛒 {msj} ")
    print(f"{Color.BLUE}=" * 80)
    if orden_licla:
        menu_volver = [volver_atras1, volver_atras2, volver_atras3]
        if items_volver >= 1 and items_volver <= 3:
            fin_ciclo_volver = items_volver
        else:
            fin_ciclo_volver = 0
        if primer_item_licla >= 1 and primer_item_licla <= len(licla):
            inicio_ciclo_items = primer_item_licla
        else:
            primer_item_licla  = 1
            inicio_ciclo_items = primer_item_licla
        if items_licla >=1 and primer_item_licla + items_licla <= len(licla) + 1:
            fin_ciclo_items = primer_item_licla + items_licla
        else:
            items_licla = len(licla) + 1 - primer_item_licla
            fin_ciclo_items = len(licla) + 1
        c = 0
        for i in range(inicio_ciclo_items, fin_ciclo_items):
            c += 1
            print(f"{c:>2}. → {licla[i-1].title()}")
        for i in range(fin_ciclo_volver):
            c += 1
            print(f"{c:>2}. {Color.BLUE}← {menu_volver[i]}")
    else:
        menu_volver = [volver_atras1, volver_atras2, volver_atras3]
        if items_volver >= 1 and items_volver <= 3:
            fin_ciclo_volver = items_volver
        else:
            fin_ciclo_volver = 0
        if primer_item_licla >= 1 and primer_item_licla <= len(licla):
            inicio_ciclo_items = primer_item_licla
        else:
            primer_item_licla  = len(licla)
            inicio_ciclo_items = primer_item_licla
        if items_licla >=1 and items_licla <= len(licla):
            fin_ciclo_items = primer_item_licla -items_licla
            inicio_ciclo_volver = items_licla + 1
        else:
            items_licla = primer_item_licla
            fin_ciclo_items = 0
        c = 0
        for i in range(inicio_ciclo_items, fin_ciclo_items, -1):
            c += 1
            print(f"{c:>2}. → {licla[i-1].title()}")
        c = 0
        for i in range(inicio_ciclo_volver, inicio_ciclo_volver + fin_ciclo_volver):
            c += 1
            print(f"{i:>2}. {Color.BLUE}← {menu_volver[c-1]}")
    print(f"{Color.BLUE}=" * 80)



def mostrar_lista_eliminados(lis):
    """Función que muestra una lista de productos eliminados en consola

    Args:
        lis (list): lista de productos eliminados
    """
    def format_float_str(num):
        form = "%.2f" % num
        form = str(form)
        return form
    print(f"{Color.CYAN}-" * 200)
    print(f"{Color.CYAN}{"Item:"[:6]: <4}\t{"ID:"[:6]: >6}\t{"Código:"[:16]: <16}\t{"Descripción:"[:12]: <12}\t{"Marca:"[:12]: <12}\t{"Modelo:"[:12]: <12}\t{"Categoría:"[:12]: <12}\t{"Origen:"[:12]: <12}\t{"Ubic:"[:10]: <10}\t{"Cant:"[:6]: <6}\t{"Precio en -($)-:"[:16]: <16}\t{"Fecha Alta:"[:11]: <11}\t{"Fecha Baja:"[:11]: <11}")
    print("-" * 200)
    c = 0
    for i in lis:
        c += 1
        print(f"{Color.RED}{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("codigo")[:16].upper(): <16}\t{i.get("descripcion")[:12].title(): <12}\t{i.get("marca")[:12].title(): <12}\t{i.get("modelo")[:12].title(): <12}\t{i.get("categoria")[:12].title(): <12}\t{i.get("origen")[:12].title(): <12}\t{i.get("ubicacion")[:10].upper(): <10}\t{str(i.get("cantidad"))[:6]: >6}\t{format_float_str(i.get("precio"))[:16]: >16}\t{i.get("fecha_alta")[:10]: <10}\t{i.get("fecha_baja")[:10]: <10}")
    print(f"{Color.CYAN}-" * 200)


def mostrar_productos_entre_cantidades_stock(lis, min, max, usuario, fecha, opcion=True):
    """Función que genera un reporte de productos que se encuentran entre dos cantidades. Muestra en consola el reporte y genera un archivo .txt con ese mismo informe

    Args:
        lis (list): lista de productos
        min (int): cantidad mínima de producto
        max (int): cantidad máxima de producto
        usuario (dict): _description_
        fecha (str): fecha en la que se genera el reporte
        opcion (bool, optional): setea que todos los productos tengan el mismo color (False), o por defecto (True() cada linea alterna entre dos colores para mejor lectura
    """
    datos_lista = lis
    datos_lista_ord = sorted(datos_lista, key=lambda x: x[5], reverse=False)
    mensaje(f'Reporte de productos con cantidades entre {min} y {max}  |  {fecha}')
    filename = f'{usuario["mail"]}_reporte_stock_entre_cantidades_{min}_{max}.txt'
    if opcion:
        ini_color = Color.CYAN
    else:
        ini_color = Color.RESET
    archivo = open(filename, "w", encoding='utf-8')
    archivo.write(f"Reporte de productos con cantidades entre {min} y {max}  |  {fecha}\n")
    archivo.write("\n")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print(f"{Color.CYAN}-" * 200)
    archivo.write(f"{"Item:"[:6]: <4}\t{"ID:"[:6]: >6}\t{"Código:"[:16]: <16}\t{"Descripción:"[:16]: <16}\t{"Marca:"[:16]: <16}\t{"Modelo:"[:16]: <16}\t{"Cantidad:"[:16]: <16}\n")
    print(f"{Color.BLUE}{"Item:"[:6]: <4}\t{"ID:"[:6]: >6}\t{"Código:"[:16]: <16}\t{"Descripción:"[:16]: <16}\t{"Marca:"[:16]: <16}\t{"Modelo:"[:16]: <16}\t{"Cantidad:"[:16]: <16}")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print(f"{Color.CYAN}-" * 200)
    c = 0
    for i in datos_lista_ord:
        c += 1
        if c%2 == 0:
            archivo.write(f"{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:16].upper(): <16}\t{i[4][:16].title(): <16}\t{i[2][:16].title(): <16}\t{i[3][:16].title(): <16}\t{str(i[5])[:6]: >6}\n")
            print(f"{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:16].upper(): <16}\t{i[4][:16].title(): <16}\t{i[2][:16].title(): <16}\t{i[3][:16].title(): <16}\t{str(i[5])[:6]: >6}")
        elif c%2 == 1:
            archivo.write(f"{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:16].upper(): <16}\t{i[4][:16].title(): <16}\t{i[2][:16].title(): <16}\t{i[3][:16].title(): <16}\t{str(i[5])[:6]: >6}\n")
            print(f"{ini_color}{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:16].upper(): <16}\t{i[4][:16].title(): <16}\t{i[2][:16].title(): <16}\t{i[3][:16].title(): <16}\t{str(i[5])[:6]: >6}")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    archivo.close()
    print(f"{Color.CYAN}-" * 200)
    


def mostrar_lista(lis, opcion = True):
    """Función que muestra una lista de productos en consola

    Args:
        lis (list): lista de productos
        opcion (bool, optional): setea que todos los productos tengan el mismo color (False), o por defecto (True() cada linea alterna entre dos colores para mejor lectura
    """
    def format_float_str(num):
        form = "%.2f" % num
        form = str(form)
        return form
    if opcion:
        ini_color = Color.CYAN
    else:
        ini_color = Color.RESET
    print(f"{Color.CYAN}-" * 200)
    print(f"{Color.BLUE}{"Item:"[:6]: <4}\t{"ID:"[:6]: >6}\t{"Código:"[:16]: <16}\t{"Descripción:"[:12]: <12}\t{"Marca:"[:12]: <12}\t{"Modelo:"[:12]: <12}\t{"Categoría:"[:12]: <12}\t{"Origen:"[:12]: <12}\t{"Ubic:"[:10]: <10}\t{"Cant:"[:6]: <6}\t{"Precio en -($)-:"[:16]: <16}\t{"Fecha Alta:"[:11]: <11}\t{"Modificación:"[:13]: <13}")
    print(f"{Color.CYAN}-" * 200)
    c = 0
    for i in lis:
        c += 1
        if c%2 == 0:
            print(f"{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("codigo")[:16].upper(): <16}\t{i.get("descripcion")[:12].title(): <12}\t{i.get("marca")[:12].title(): <12}\t{i.get("modelo")[:12].title(): <12}\t{i.get("categoria")[:12].title(): <12}\t{i.get("origen")[:12].title(): <12}\t{i.get("ubicacion")[:10].upper(): <10}\t{str(i.get("cantidad"))[:6]: >6}\t{format_float_str(i.get("precio"))[:16]: >16}\t{i.get("fecha_alta")[:10]: <10}\t{i.get("fecha_modificacion")[:10]: <10}")
        elif c%2 == 1:
            print(f"{ini_color}{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("codigo")[:16].upper(): <16}\t{i.get("descripcion")[:12].title(): <12}\t{i.get("marca")[:12].title(): <12}\t{i.get("modelo")[:12].title(): <12}\t{i.get("categoria")[:12].title(): <12}\t{i.get("origen")[:12].title(): <12}\t{i.get("ubicacion")[:10].upper(): <10}\t{str(i.get("cantidad"))[:6]: >6}\t{format_float_str(i.get("precio"))[:16]: >16}\t{i.get("fecha_alta")[:10]: <10}\t{i.get("fecha_modificacion")[:10]: <10}")
    print(f"{Color.CYAN}-" * 200)


def mostrar_lista_usuarios(lis, opcion = True):
    """Función que muestra una lista de usuarios en consola

    Args:
        lis (list): lista de usuarios
        opcion (bool, optional): setea que todos los productos tengan el mismo color (False), o por defecto (True() cada linea alterna entre dos colores para mejor lectura
    """
    if opcion:
        ini_color = Color.CYAN
    else:
        ini_color = Color.RESET
    passw = "********"
    print(f"{Color.CYAN}-" * 200)
    print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Nombre:"[:16]: <16}\t{"Apellido:"[:16]: <16}\t{"Mail:"[:32]: <32}\t{"Passw:"[:8]: <8}\t{"Perfil:"[:16]: <16}\t{"Fecha Alta:"[:11]: <11}\t{"Modificación:"[:13]: <13}\t{"Json"[:4]: >4}\t{"Db"[:4]: >4}")
    print(f"{Color.CYAN}-" * 200)
    c = 0
    for i in lis:
        c += 1
        if i.get("tracking_json"):
                js = "✓"
        else:
            js = "✕"
        if i.get("tracking_db"):
            db = "✓"
        else:
            db = "✕"
        if c%2 == 0:
            print(f"{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("nombre")[:16].title(): <16}\t{i.get("apellido")[:16].title(): <16}\t{i.get("mail")[:32].lower(): <32}\t{passw[:8].title(): <8}\t{i.get("perfil_acceso")[:16].title(): <16}\t{i.get("fecha_alta")[:10]: <10}\t{i.get("fecha_modificacion")[:10]: <10}\t{js[:4]: >4}\t{db[:4]: >4}")
        elif c%2 == 1:
            print(f"{ini_color}{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("nombre")[:16].title(): <16}\t{i.get("apellido")[:16].title(): <16}\t{i.get("mail")[:32].lower(): <32}\t{passw[:8].title(): <8}\t{i.get("perfil_acceso")[:16].title(): <16}\t{i.get("fecha_alta")[:10]: <10}\t{i.get("fecha_modificacion")[:10]: <10}\t{js[:4]: >4}\t{db[:4]: >4}")
    print(f"{Color.CYAN}-" * 200)


def mostrar_lista_usuarios_eliminados(lis, opcion = True):
    """Función que muestra una lista de usuarios eliminados en consola

    Args:
        lis (list): lista de usuarios
        opcion (bool, optional): setea que todos los productos tengan el mismo color (False), o por defecto (True() cada linea alterna entre dos colores para mejor lectura
    """
    if opcion:
        ini_color = Color.RED
    else:
        ini_color = Color.RESET
    passw = "********"
    print(f"{Color.CYAN}-" * 200)
    print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Nombre:"[:16]: <16}\t{"Apellido:"[:16]: <16}\t{"Mail:"[:32]: <32}\t{"Passw:"[:8]: <8}\t{"Perfil:"[:16]: <16}\t{"Fecha Alta:"[:11]: <11}\t{"Fecha Baja:"[:13]: <13}\t{"Json"[:4]: >4}\t{"Db"[:4]: >4}")
    print(f"{Color.CYAN}-" * 200)
    c = 0
    for i in lis:
        c += 1
        if i.get("tracking_json"):
                js = "✓"
        else:
            js = "✕"
        if i.get("tracking_db"):
            db = "✓"
        else:
            db = "✕"
        print(f"{ini_color}{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("nombre")[:16].title(): <16}\t{i.get("apellido")[:16].title(): <16}\t{i.get("mail")[:32].lower(): <32}\t{passw[:8].title(): <8}\t{i.get("perfil_acceso")[:16].title(): <16}\t{i.get("fecha_alta")[:10]: <10}\t{i.get("fecha_baja")[:10]: <10}\t{js[:4]: >4}\t{db[:4]: >4}")
    print(f"{Color.CYAN}-" * 200)


def mostrar_lista_usuarios_seleccion(lis, usuario_ini, usuario_fin, opcion = True):
    """# funcion que muestra una lista de usuarios seleccionados

    Args:
        lis (list): lista de usuarios
        usuario_ini (int): primer usuario de la lista seleccionada
        usuario_fin (int): ultimo usuario de la lista seleccionada
        opcion (bool, optional): setea que todos los productos tengan el mismo color (False), o por defecto (True() cada linea alterna entre dos colores para mejor lectura
    """
    if opcion:
        ini_color = Color.CYAN
    else:
        ini_color = Color.RESET
    passw = "********"
    print(f"{Color.CYAN}-" * 200)
    print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Nombre:"[:16]: <16}\t{"Apellido:"[:16]: <16}\t{"Mail:"[:32]: <32}\t{"Password:"[:12]: <12}\t{"Perfil:"[:16]: <16}\t{"Fecha Alta:"[:11]: <11}\t{"Modificación:"[:13]: <13}")
    print(f"{Color.CYAN}-" * 200)
    c = 0
    for i in lis:
        c += 1
        if c >= usuario_ini and c <= usuario_fin:
            print(f"{ini_color}{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("nombre")[:16].title(): <16}\t{i.get("apellido")[:16].title(): <16}\t{i.get("mail")[:32].lower(): <32}\t{passw[:12].title(): <12}\t{i.get("perfil_acceso")[:16].title(): <16}\t{i.get("fecha_alta")[:10]: <10}\t{i.get("fecha_modificacion")[:10]: <10}")
        else:
            print(f"{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("nombre")[:16].title(): <16}\t{i.get("apellido")[:16].title(): <16}\t{i.get("mail")[:32].lower(): <32}\t{passw[:12].title(): <12}\t{i.get("perfil_acceso")[:16].title(): <16}\t{i.get("fecha_alta")[:10]: <10}\t{i.get("fecha_modificacion")[:10]: <10}")
    print(f"{Color.CYAN}-" * 200)


def mostrar_detalle_cambio_stock(lis, tipo_oper, opcion = True):
    """Funcion que muestra una lista de movimientos (ingresos, egresos o ajustes) de productos en consola

    Args:
        lis (list): lista de movimientos de producto
        tipo_oper (str): selecciona si los movimientos a mostrar son compras, ventas o ajustes
        opcion (bool, optional): setea que todos los productos tengan el mismo color (False), o por defecto (True() cada linea alterna entre dos colores para mejor lectura
    """
    def format_float_str(num):
        form = "%.2f" % num
        form = str(form)
        return form 
    if opcion:
        ini_color = Color.CYAN
    else:
        ini_color = Color.RESET
    print(f"{Color.CYAN}-" * 200)
    match tipo_oper.lower():
        case "compra":
            print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Fecha Compra:"[:12]: <12}\t{"Proveedor:"[:16]: <16}\t{"N°Factura:"[:16]: <16}\t{"Cant:"[:6]: <6}\t{"Costo Unidad ($):"[:16]: <16}\t{"Total Compra ($):"[:16]: <16}")
            print(f"{Color.CYAN}-" * 200)
            c = 0
            for i in lis:
                c += 1
                if c%2 == 0:
                    print(f"{ini_color}{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("fecha_compra")[:10]: >10}\t{i.get("proveedor_id")[:16].title(): <16}\t{i.get("nro_factura_proveedor")[:16].title(): <16}\t{str(i.get("cantidad_ingreso"))[:6]: >6}\t{format_float_str(i.get("costo_unitario"))[:16]: >16}\t{format_float_str(i.get("valor_compra"))[:16]: >16}")
                elif c%2 == 1:
                    print(f"{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("fecha_compra")[:10]: >10}\t{i.get("proveedor_id")[:16].title(): <16}\t{i.get("nro_factura_proveedor")[:16].title(): <16}\t{str(i.get("cantidad_ingreso"))[:6]: >6}\t{format_float_str(i.get("costo_unitario"))[:16]: >16}\t{format_float_str(i.get("valor_compra"))[:16]: >16}")
                print(f"{Color.CYAN}-" * 200)
        case "venta":
            print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Fecha Venta:"[:12]: <12}\t{"Cliente:"[:16]: <16}\t{"N°Factura:"[:16]: <16}\t{"Cant:"[:6]: <6}\t{"Precio Unidad ($):"[:17]: <16}\t{"Total Venta ($):"[:16]: <16}")
            print(f"{Color.CYAN}-" * 200)
            c = 0
            for i in lis:
                c += 1
                if c%2 == 0:
                    print(f"{ini_color}{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("fecha_venta")[:10]: >10}\t{i.get("cliente_id")[:16].title(): <16}\t{i.get("nro_factura_cliente")[:16].title(): <16}\t{str(i.get("cantidad_egreso"))[:6]: >6}\t{format_float_str(i.get("precio_unitario"))[:16]: >16}\t{format_float_str(i.get("valor_venta"))[:16]: >16}")
                elif c%2 == 1:
                    print(f"{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("fecha_venta")[:10]: >10}\t{i.get("cliente_id")[:16].title(): <16}\t{i.get("nro_factura_cliente")[:16].title(): <16}\t{str(i.get("cantidad_egreso"))[:6]: >6}\t{format_float_str(i.get("precio_unitario"))[:16]: >16}\t{format_float_str(i.get("valor_venta"))[:16]: >16}")
                print(f"{Color.CYAN}-" * 200)
        case "ajuste":
            print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Fecha Ajuste:"[:12]: <12}\t{"Detalle:"[:64]: <64}\t{"Cant:"[:6]: <6}")
            print(f"{Color.CYAN}-" * 200)
            c = 0
            for i in lis:
                c += 1
                if c%2 == 0:
                    print(f"{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("fecha_ajuste")[:10]: >10}\t{i.get("detalle_ajuste")[:64].title(): <64}\t{str(i.get("cantidad_ajuste"))[:6]: >6}")
                elif c%2 == 1:
                    print(f"{ini_color}{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("fecha_ajuste")[:10]: >10}\t{i.get("detalle_ajuste")[:64].title(): <64}\t{str(i.get("cantidad_ajuste"))[:6]: >6}")
                print(f"{Color.CYAN}-" * 200)


# funcion que muestra una lista de movimientos de productos seleccionandos con color diferente
def mostrar_detalle_cambio_stock_seleccion(lis, tipo_oper, item_ini, item_fin):
    """Función que muestra en consola una lista de movimientos de productos (compra, venta o ajuste) que fueron seleccionados en color rojo

    Args:
        lis (list): lista de movimientos de producto
        tipo_oper (str): operacion: 'compra', 'venta' o 'ajuste'
        item_ini (int): primer item de la lista seleccionada
        item_fin (int): último item de la lista seleccionada
    """
    def format_float_str(num):
        form = "%.2f" % num
        form = str(form)
        return form
    print(f"{Color.CYAN}-" * 200)
    match tipo_oper.lower():
        case "compra":
            print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Fecha Compra:"[:12]: <12}\t{"Proveedor:"[:16]: <16}\t{"N°Factura:"[:16]: <16}\t{"Cant:"[:6]: <6}\t{"Costo Unidad($):"[:16]: <16}\t{"Total Compra($):"[:16]: <16}")
            print(f"{Color.CYAN}-" * 200)
            c = 0
            for i in lis:
                c += 1
                if c >= item_ini and c <= item_fin:
                    print(f"{Color.RED}{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("fecha_compra")[:10]: >10}\t{i.get("proveedor_id")[:16].title(): <16}\t{i.get("nro_factura_proveedor")[:16].title(): <16}\t{str(i.get("cantidad_ingreso"))[:6]: >6}\t{format_float_str(i.get("costo_unitario"))[:16]: >16}\t{format_float_str(i.get("valor_compra"))[:16]: >16}")
                else:
                    print(f"{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("fecha_compra")[:10]: >10}\t{i.get("proveedor_id")[:16].title(): <16}\t{i.get("nro_factura_proveedor")[:16].title(): <16}\t{str(i.get("cantidad_ingreso"))[:6]: >6}\t{format_float_str(i.get("costo_unitario"))[:16]: >16}\t{format_float_str(i.get("valor_compra"))[:16]: >16}")
                print(f"{Color.CYAN}-" * 200)
        case "venta":
            print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Fecha Venta:"[:12]: <12}\t{"Cliente:"[:16]: <16}\t{"N°Factura:"[:16]: <16}\t{"Cant:"[:6]: <6}\t{"Precio Unidad($):"[:16]: <16}\t{"Total Venta($):"[:16]: <16}")
            print(f"{Color.CYAN}-" * 200)
            c = 0
            for i in lis:
                c += 1
                if c >= item_ini and c <= item_fin:
                    print(f"{Color.RED}{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("fecha_venta")[:10]: >10}\t{i.get("cliente_id")[:16].title(): <16}\t{i.get("nro_factura_cliente")[:16].title(): <16}\t{str(i.get("cantidad_egreso"))[:6]: >6}\t{format_float_str(i.get("precio_unitario"))[:16]: >16}\t{format_float_str(i.get("valor_venta"))[:16]: >16}")
                else:
                    print(f"{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("fecha_venta")[:10]: >10}\t{i.get("cliente_id")[:16].title(): <16}\t{i.get("nro_factura_cliente")[:16].title(): <16}\t{str(i.get("cantidad_egreso"))[:6]: >6}\t{format_float_str(i.get("precio_unitario"))[:16]: >16}\t{format_float_str(i.get("valor_venta"))[:16]: >16}")
                print(f"{Color.CYAN}-" * 200)
        case "ajuste":
            print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Fecha Ajuste:"[:12]: <12}\t{"Detalle:"[:64]: <64}\t{"Cant:"[:6]: <6}")
            print(f"{Color.CYAN}-" * 200)
            c = 0
            for i in lis:
                c += 1
                if c >= item_ini and c <= item_fin:
                    print(f"{Color.RED}{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("fecha_ajuste")[:10]: >10}\t{i.get("detalle_ajuste")[:64].title(): <64}\t{str(i.get("cantidad_ajuste"))[:6]: >6}")
                else:
                    print(f"{str(c)[:6]: >4}\t{str(i.get("id"))[:6]: >6}\t{i.get("fecha_ajuste")[:10]: >10}\t{i.get("detalle_ajuste")[:64].title(): <64}\t{str(i.get("cantidad_ajuste"))[:6]: >6}")
                print(f"{Color.CYAN}-" * 200)


def reportar_tiempo_usuarios_por_dia_entrefechas(lista, usuario , opcion=True):
    """Función que muestra en consola un reporte del tiempo que estuvieron los usuarios en el sistema entre dos fechas determinadas con el detalle de cada día en ese período de tiempo. También genera un reporte en formato .txt

    Args:
        lista (lista): lista reporte: lista de listas, una sublista con las tuplas de la info de cada usuario en cada logueo y la otra sublista con las fechas de ese período de tiempo.
        usuario (dict): usuario del sistema
        opcion (bool, optional): setea que todos los productos tengan el mismo color (False), o por defecto (True() cada linea alterna entre dos colores para mejor lectura

    Returns:
        nuevalis(list): 
    """
    datos_lista = lista[0]
    fecha_lista = lista[1]
    nuevalis= []
    if datos_lista:
        datos_lista.append((datos_lista[0][0], datos_lista[-1][1], datos_lista[-1][2], datos_lista[-1][3][:10], datos_lista[-1][4]))
        usu_id = datos_lista[0][0]
        usu_fecha = datos_lista[3][:10]
        acum = 0
        for i in range(len(datos_lista)):
            if i != len(datos_lista):
                if datos_lista[i][0] == usu_id and datos_lista[i][3][:10] == usu_fecha:
                    acum += datos_lista[i][4]
                else:
                    nuevalis.append((usu_id, datos_lista[i-1][1], datos_lista[i-1][2], datos_lista[i-1][3][:10], acum))
                    usu_id = datos_lista[i][0]
                    usu_fecha = datos_lista[i][3][:10]
                    acum = 0
                    if datos_lista[i][0] == usu_id:
                        acum += datos_lista[i][4]
        nuevalis.pop(0)
    mensaje(f'Reporte de tiempo de usuarios por día entre el {fecha_lista[0]} y el {fecha_lista[1]}')
    filename = f'{usuario["mail"]}_uso_diario_{fecha_lista[0]}_{fecha_lista[1]}.txt'
    if opcion:
        ini_color = Color.CYAN
    else:
        ini_color = Color.RESET
    archivo = open(filename, "w", encoding='utf-8')
    archivo.write(f'Reporte de tiempo de usuarios por día entre el {fecha_lista[0]} y el {fecha_lista[1]}\n')
    archivo.write("\n")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print(f"{Color.CYAN}-" * 200)
    archivo.write(f"{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Mail:"[:32]: <32}\t{"Perfil:"[:16]: <16}\t{"Fecha de uso:"[:13]: <11}\t{"Tiempo de Uso:"[:24]: >24}\n")
    print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Mail:"[:32]: <32}\t{"Perfil:"[:16]: <16}\t{"Fecha de uso:"[:13]: <11}\t{"Tiempo de Uso:"[:24]: >24}")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print(f"{Color.CYAN}-" * 200)
    if datos_lista:
        c = 0
        for i in nuevalis:
            c += 1
            if c%2 == 0:
                archivo.write(f"{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:32].lower(): <32}\t{i[2][:16].title(): <16}\t{i[3][:10]: <10}\t{convertir_segundos_a_horas(i[4])[:24]: >24}\n")
                print(f"{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:32].lower(): <32}\t{i[2][:16].title(): <16}\t{i[3][:10]: <10}\t{convertir_segundos_a_horas(i[4])[:24]: >24}")
            elif c%2 == 1:
                archivo.write(f"{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:32].lower(): <32}\t{i[2][:16].title(): <16}\t{i[3][:10]: <10}\t{convertir_segundos_a_horas(i[4])[:24]: >24}\n")
                print(f"{ini_color}{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:32].lower(): <32}\t{i[2][:16].title(): <16}\t{i[3][:10]: <10}\t{convertir_segundos_a_horas(i[4])[:24]: >24}")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    archivo.close()
    print(f"{Color.CYAN}-" * 200)
    return nuevalis


def reportar_tiempo_por_usuario_total_entrefechas(lista, usuario , opcion=True):
    """Función que muestra en consola un reporte del tiempo total por usuario en ese período de tiempo ordenado por usuario con más tiempo de uso del sistema. También genera un reporte en formato .txt

    Args:
        lista (lista): lista reporte: lista de listas, una sublista con las tuplas de la info de cada usuario en cada logueo y la otra sublista con las fechas de ese período de tiempo.
        usuario (dict): usuario del sistema
        opcion (bool, optional): setea que todos los productos tengan el mismo color (False), o por defecto (True() cada linea alterna entre dos colores para mejor lectura

    Returns:
        nuevalis_ord(list): 
    """
    datos_lista = lista[0]
    fecha_lista = lista[1]
    nuevalis_ord= []
    if datos_lista:
        datos_lista.append((datos_lista[0][0], datos_lista[-1][1], datos_lista[-1][2], datos_lista[-1][3][:10], datos_lista[-1][4]))
        nuevalis = []
        usu_id = datos_lista[0][0]
        acum = 0
        for i in range(len(datos_lista)):
            if i != len(datos_lista):
                if datos_lista[i][0] == usu_id:
                    acum += datos_lista[i][4]
                else:
                    nuevalis.append((usu_id, datos_lista[i-1][1], datos_lista[i-1][2], datos_lista[i-1][3][:10], acum))
                    usu_id = datos_lista[i][0]
                    acum = 0
                    if datos_lista[i][0] == usu_id:
                        acum += datos_lista[i][4]
        nuevalis_ord = sorted(nuevalis, key=lambda x: x[4], reverse=True)
    mensaje(f'Reporte de tiempo de usuarios total entre el {fecha_lista[0]} y el {fecha_lista[1]}')
    filename = f'{usuario["mail"]}_total_uso_{fecha_lista[0]}_{fecha_lista[1]}.txt'
    if opcion:
        ini_color = Color.CYAN
    else:
        ini_color = Color.RESET
    archivo = open(filename, "w", encoding='utf-8')
    archivo.write(f'Reporte de tiempo de usuarios total entre el {fecha_lista[0]} y el {fecha_lista[1]}\n')
    archivo.write("\n")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print(f"{Color.CYAN}-" * 200)
    archivo.write(f"{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Mail:"[:32]: <32}\t{"Perfil:"[:16]: <16}\t{"Fecha desde:"[:13]: <11}\t{"Fecha hasta:"[:13]: <11}\t{"Tiempo de Uso:"[:24]: >24}\n")
    print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"ID:"[:6]: >6}\t{"Mail:"[:32]: <32}\t{"Perfil:"[:16]: <16}\t{"Fecha desde:"[:13]: <11}\t{"Fecha hasta:"[:13]: <11}\t{"Tiempo de Uso:"[:24]: >24}")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print(f"{Color.CYAN}-" * 200)
    if datos_lista:
        c = 0
        for i in nuevalis_ord:
            c += 1
            if c%2 == 0:
                archivo.write(f"{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:32].lower(): <32}\t{i[2][:16].title(): <16}\t{fecha_lista[0][:10]: <10}\t{fecha_lista[1][:10]: <10}\t{convertir_segundos_a_horas(i[4])[:24]: >24}\n")
                print(f"{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:32].lower(): <32}\t{i[2][:16].title(): <16}\t{fecha_lista[0][:10]: <10}\t{fecha_lista[1][:10]: <10}\t{convertir_segundos_a_horas(i[4])[:24]: >24}")
            elif c%2 == 1:
                archivo.write(f"{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:32].lower(): <32}\t{i[2][:16].title(): <16}\t{fecha_lista[0][:10]: <10}\t{fecha_lista[1][:10]: <10}\t{convertir_segundos_a_horas(i[4])[:24]: >24}\n")
                print(f"{ini_color}{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:32].lower(): <32}\t{i[2][:16].title(): <16}\t{fecha_lista[0][:10]: <10}\t{fecha_lista[1][:10]: <10}\t{convertir_segundos_a_horas(i[4])[:24]: >24}")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    archivo.close()
    print(f"{Color.CYAN}-" * 200)
    return nuevalis_ord


def reportar_ventas_por_usuario_por_dia_entrefechas(lista, usuario , opcion=True):
    """Función que muestra en consola un reporte del ventas de los usuarios en el sistema entre dos fechas determinadas con el detalle de cada día en ese período de tiempo. También genera un reporte en formato .txt

    Args:
        lista (lista): lista reporte: lista de listas, una sublista con las tuplas de la info de cada usuario en cada logueo y la otra sublista con las fechas de ese período de tiempo.
        usuario (dict): usuario del sistema
        opcion (bool, optional): setea que todos los productos tengan el mismo color (False), o por defecto (True() cada linea alterna entre dos colores para mejor lectura

    Returns:
        nuevalis(list): 
    """
    def format_float_str(num):
        form = "%.2f" % num
        form = str(form)
        return form
    datos_lista = lista[0]
    fecha_lista = lista[1]
    mensaje(f'Reporte de ventas de usuarios por día entre el {fecha_lista[0]} y el {fecha_lista[1]}')
    filename = f'{usuario["mail"]}_ventas_diarias_{fecha_lista[0]}_{fecha_lista[1]}.txt'
    if opcion:
        ini_color = Color.CYAN
    else:
        ini_color = Color.RESET
    archivo = open(filename, "w", encoding='utf-8')
    archivo.write(f'Reporte de ventas de usuarios por día entre el {fecha_lista[0]} y el {fecha_lista[1]}\n')
    archivo.write("\n")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print(f"{Color.CYAN}-" * 200)
    archivo.write(f"{"Item:"[:6]: >4}\t{"IdUsu:"[:6]: >6}\t{"Mail:"[:32]: <32}\t{"Perfil:"[:16]: <16}\t{"Fecha Venta:"[:13]: <11}\t{"IdPro:"[:6]: >6}\t{"Código:"[:16]: >16}\t{"Marca:"[:12]: <12}\t{"Cant:"[:6]: <6}\t{"Venta ($):"[:16]: >16}\n")
    print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"IdUsu:"[:6]: >6}\t{"Mail:"[:32]: <32}\t{"Perfil:"[:16]: <16}\t{"Fecha Venta:"[:13]: <11}\t{"IdPro:"[:6]: >6}\t{"Código:"[:16]: >16}\t{"Marca:"[:12]: <12}\t{"Cant:"[:6]: <6}\t{"Venta ($):"[:16]: >16}")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print(f"{Color.CYAN}-" * 200)
    if datos_lista:
        c = 0
        for i in datos_lista:
            c += 1
            if c%2 == 0:
                archivo.write(f"{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:32].lower(): <32}\t{i[2][:16].title(): <16}\t{i[3][:10]: <10}\t{str(i[4])[:6]: >6}\t{i[5][:16].upper(): >16}\t{i[6][:12].title(): <12}\t{str(i[7])[:6]: >6}\t{format_float_str(i[8])[:16]: >16}\n")
                print(f"{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:32].lower(): <32}\t{i[2][:16].title(): <16}\t{i[3][:10]: <10}\t{str(i[4])[:6]: >6}\t{i[5][:16].upper(): >16}\t{i[6][:12].title(): <12}\t{str(i[7])[:6]: >6}\t{format_float_str(i[8])[:16]: >16}")
            elif c%2 == 1:
                archivo.write(f"{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:32].lower(): <32}\t{i[2][:16].title(): <16}\t{i[3][:10]: <10}\t{str(i[4])[:6]: >6}\t{i[5][:16].upper(): >16}\t{i[6][:12].title(): <12}\t{str(i[7])[:6]: >6}\t{format_float_str(i[8])[:16]: >16}\n")
                print(f"{ini_color}{str(c)[:6]: >4}\t{str(i[0])[:6]: >6}\t{i[1][:32].lower(): <32}\t{i[2][:16].title(): <16}\t{i[3][:10]: <10}\t{str(i[4])[:6]: >6}\t{i[5][:16].upper(): >16}\t{i[6][:12].title(): <12}\t{str(i[7])[:6]: >6}\t{format_float_str(i[8])[:16]: >16}")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    archivo.close()
    print(f"{Color.CYAN}-" * 200)
    return datos_lista


def reportar_ventas_por_usuario_total_entrefechas(lista, usuario , opcion=True):
    """Función que muestra en consola un reporte de ventas totales por usuario en ese período de tiempo ordenado por usuario con más ventas. También genera un reporte en formato .txt

    Args:
        lista (lista): lista reporte: lista de listas, una sublista con las tuplas de la info de cada usuario en cada logueo y la otra sublista con las fechas de ese período de tiempo.
        usuario (dict): usuario del sistema
        opcion (bool, optional): setea que todos los productos tengan el mismo color (False), o por defecto (True() cada linea alterna entre dos colores para mejor lectura

    Returns:
        nuevalis_ord(list): 
    """
    def format_float_str(num):
        form = "%.2f" % num
        form = str(form)
        return form
    datos_lista = lista[0]
    fecha_lista = lista[1]
    nuevalis_final_ord = []
    if datos_lista:
        nuevalis = []
        otra_nuevalis = []
        nuevalis_final = []
        for i in datos_lista:
                nuevalis.append((i[0], i[1], i[2]))
        for i in range(len(nuevalis)):
                otra_nuevalis.append((nuevalis[i], nuevalis.count(nuevalis[i])))
        for i in otra_nuevalis:
                if i not in nuevalis_final:
                        nuevalis_final.append(i)
        nuevalis_final_ord = sorted(nuevalis_final, key=lambda x: x[1], reverse=True)
    mensaje(f'Reporte de ventas de usuarios total entre el {fecha_lista[0]} y el {fecha_lista[1]}')
    filename = f'{usuario["mail"]}_total_ventas_{fecha_lista[0]}_{fecha_lista[1]}.txt'
    if opcion:
        ini_color = Color.CYAN
    else:
        ini_color = Color.RESET
    archivo = open(filename, "w", encoding='utf-8')
    archivo.write(f'Reporte de ventas de usuarios total entre el {fecha_lista[0]} y el {fecha_lista[1]}\n')
    archivo.write("\n")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print(f"{Color.CYAN}-" * 200)
    archivo.write(f"{"Item:"[:6]: >4}\t{"IdUsu:"[:6]: >6}\t{"Mail:"[:32]: <32}\t{"Perfil:"[:16]: <16}\t{"Fecha desde:"[:13]: <11}\t{"Fecha hasta:"[:13]: <11}\t{"Cantidad de Ventas:"[:24]: >24}\n")
    print(f"{Color.BLUE}{"Item:"[:6]: >4}\t{"IdUsu:"[:6]: >6}\t{"Mail:"[:32]: <32}\t{"Perfil:"[:16]: <16}\t{"Fecha desde:"[:13]: <11}\t{"Fecha hasta:"[:13]: <11}\t{"Cantidad de Ventas:"[:24]: >24}")
    archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    print(f"{Color.CYAN}-" * 200)
    if datos_lista:
        c = 0
        for i in nuevalis_final_ord:
            c += 1
            if c%2 == 0:
                archivo.write(f"{str(c)[:6]: >4}\t{str(i[0][0])[:6]: >6}\t{i[0][1][:32].lower(): <32}\t{i[0][2][:16].title(): <16}\t{fecha_lista[0][:10]: <10}\t{fecha_lista[1][:10]: <10}\t{str(i[1])[:24]: >24}\n")
                print(f"{str(c)[:6]: >4}\t{str(i[0][0])[:6]: >6}\t{i[0][1][:32].lower(): <32}\t{i[0][2][:16].title(): <16}\t{fecha_lista[0][:10]: <10}\t{fecha_lista[1][:10]: <10}\t{str(i[1])[:24]: >24}")
            elif c%2 == 1:
                archivo.write(f"{str(c)[:6]: >4}\t{str(i[0][0])[:6]: >6}\t{i[0][1][:32].lower(): <32}\t{i[0][2][:16].title(): <16}\t{fecha_lista[0][:10]: <10}\t{fecha_lista[1][:10]: <10}\t{str(i[1])[:24]: >24}\n")
                print(f"{ini_color}{str(c)[:6]: >4}\t{str(i[0][0])[:6]: >6}\t{i[0][1][:32].lower(): <32}\t{i[0][2][:16].title(): <16}\t{fecha_lista[0][:10]: <10}\t{fecha_lista[1][:10]: <10}\t{str(i[1])[:24]: >24}")
        archivo.write("--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\n")
    archivo.close()
    print(f"{Color.CYAN}-" * 200)
    return nuevalis_final_ord



def opcion_menu(x, nombre_menu):
    """funcion que genera la cantidad de opciones en el menú que se ingresa

    Args:
        x (int): cantidad de opciones pedidas (números positivos mayores a 0)
        nombre_menu (str): nombre del menú

    Returns:
        opcion_usuario(int): opciones devueltas
    """
    opciones_menu = []
    for i in range(x):
        opciones_menu.append(str(i+1))
    opcion_usuario = input(f"* {nombre_menu} * Seleccionar Opción (1-{x}): ").strip()
    while len(opcion_usuario) > len(opciones_menu[-1]) or not opcion_usuario.isdigit() or int(opcion_usuario) > int(opciones_menu[-1]) or int(opcion_usuario) < int(opciones_menu[0]):
        opcion_usuario = input(f"Seleccionar Opción (1-{x}): ").strip()
    return int(opcion_usuario)


def opcion_menu_con_0(x, nombre_menu):
    """funcion que genera la cantidad de opciones en el menú que se ingresa y el cero

    Args:
        x (int): cantidad de opciones pedidas
        nombre_menu (str): nombre del menú

    Returns:
        opcion_usuario(int): opciones devueltas
    """
    opciones_menu = []
    for i in range(x):
        opciones_menu.append(str(i+1))
    opcion_usuario = input(f"* {nombre_menu} * Seleccionar Opción (1-{x}): ").strip()
    while len(opcion_usuario) > len(opciones_menu[-1]) or not opcion_usuario.isdigit() or int(opcion_usuario) > int(opciones_menu[-1]):
        opcion_usuario = input(f"Seleccionar Opción (1-{x}): ").strip()
    return int(opcion_usuario)


def opcion_menu_2(inicio, cantidad, nombre_menu):
    """funcion que genera la cantidad de opciones en el menú que se ingresa a partir de un número de inicio

    Args:
        inicio (int): primer número de las opciones
        cantidad (int): cantidad de opciones
        nombre_menu (str): nombre del menú

    Returns:
         opcion_usuario(int): opciones devueltas
    """
    opciones_menu = []
    for i in range(inicio, inicio + cantidad):
        opciones_menu.append(str(i))
    opcion_usuario = input(f"* {nombre_menu} * Seleccionar Opción ({inicio}-{inicio + cantidad - 1}): ").strip()
    while not opcion_usuario.isdigit() or int(opcion_usuario) > int(opciones_menu[-1]) or int(opcion_usuario) < int(opciones_menu[0]):
        opcion_usuario = input(f"* {nombre_menu} * Seleccionar Opción ({inicio}-{inicio + cantidad - 1}): ").strip()
    return int(opcion_usuario)



def opcion_menu_2_con_0(inicio, cantidad, nombre_menu):
    """funcion que genera la cantidad de opciones en el menú que se ingresa a partir de un número de inicio y el cero

    Args:
        inicio (int): primer número de las opciones
        cantidad (int): cantidad de opciones
        nombre_menu (str): nombre del menú

    Returns:
         opcion_usuario(int): opciones devueltas
    """
    opciones_menu = []
    for i in range(inicio, inicio + cantidad):
        opciones_menu.append(str(i))
    opcion_usuario = input(f"* {nombre_menu} * Seleccionar Opción ({inicio}-{inicio + cantidad - 1}): ").strip()
    while not opcion_usuario.isdigit() or int(opcion_usuario) > int(opciones_menu[-1]):
        opcion_usuario = input(f"* {nombre_menu} * Seleccionar Opción ({inicio}-{inicio + cantidad - 1}): ").strip()
    return int(opcion_usuario)