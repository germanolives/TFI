import datetime
import sqlite3
from interfaz_usuario import mensaje


def traer_id_producto_desde_db(base_datos, nombre_tabla, item):
    """Función que devuelve el valor del id del registro que se solicita pasando como argumentos el nombre de la base de datos, el nombre de la tabla y el registro que estamos usando en el script (diccionario)

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'productos'
        item (dict): producto
    """
    campo_id = "id"
    campos_item = list(item)[1:10]
    campos_item2 = list(item)[13:]
    valores_item = list(item.values())[1:10]
    valores_item2 = list(item.values())[13:]
    campos_item.extend(campos_item2)
    valores_item.extend(valores_item2)
    nombres_claves = '= ? AND '.join(campos_item) + ' = ? '
    base_datos_db = base_datos + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('''BEGIN TRANSACTION''')
            sql_select = f'''SELECT {campo_id} FROM {nombre_tabla} WHERE {nombres_claves}'''
            cursor.execute(sql_select, valores_item)
            tupla_id = cursor.fetchall()
            id_item = tupla_id[0][0]
            conexion.commit()
        except:
            conexion.rollback()
            id_item = False
    except sqlite3.Error as e:
        id_item = False
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        return id_item


def traer_id_producto_preex_desde_db(base_datos, nombre_tabla, item):
    """Devuelve 'True' si ese nuevo producto que se quiere crear ya se encuentra en la base de datos y así evitar crear productos duplicados

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'productos'
        item (dict): producto
    """
    campo_id = "id"
    campos_item = list(item)[2:4]
    valores_item = list(item.values())[2:4]
    nombres_claves = '= ? AND '.join(campos_item) + ' = ? '
    base_datos_db = base_datos + ".db"
    try:    
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('''BEGIN TRANSACTION''')
            sql_select = f'''SELECT {campo_id} FROM {nombre_tabla} WHERE {nombres_claves}'''
            cursor.execute(sql_select, valores_item)
            tupla_id = cursor.fetchall()
            id_item = tupla_id[0][0]
            conexion.commit()
        except:
            conexion.rollback()
            id_item = False 
    except sqlite3.Error as e:
        id_item = False
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        return id_item


def traer_id_mov_desde_db(base_datos, nombre_tabla, item):
    """Devuelve el 'id' desde la base de datos de un movimiento de un prodcuto

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'ingresos', 'egresos' o 'ajustes'
        item (dict): item
    """
    campo_id = "id"
    campos_item = list(item)
    base_datos_db = base_datos + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            cursor.execute(f'SELECT {campo_id} FROM {nombre_tabla} WHERE {campos_item[1]} = ? AND {campos_item[3]} = ? AND {campos_item[4]} = ?', (item.get(campos_item[1]), item.get(campos_item[3]), item.get(campos_item[4])))
            tupla_id = cursor.fetchall()
            id_item = tupla_id[0][0]
            conexion.commit()         
        except:
            conexion.rollback()
            id_item = False
    except sqlite3.Error as e:
        id_item = False
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        return id_item


def cargar_lista_desde_db(base_datos, nombre_tabla):
    """Retorna una lista con los registros de una tabla ('productos' o 'usuarios') en una base de datos determinada y solicitada sin los 'id'

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'productos' o 'usuarios'
    """
    base_datos_db = base_datos.strip() + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            cursor.execute(f'SELECT * FROM {nombre_tabla}')
            lis = cursor.fetchall()
            campos = cursor.description
            lista = []
            for li in lis:
                dic = {}
                c = 0
                for campo in campos[1:]:
                    dic.setdefault(campo[0], li[1:][c])
                    c += 1
                lista.append(dic)
            conexion.commit()
        except:
            conexion.rollback()
            lista = [] 
    except sqlite3.Error as e:
        lista = []
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        return lista


def cargar_lista_desde_db2(base_datos, nombre_tabla):
    """Retorna una lista con los registros de una tabla ('ingresos' , 'egresos' o 'ajustes') en una base de datos determinada y solicitada sin los 'id'

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'ingresos' , 'egresos' o 'ajustes'
    """
    base_datos_db = base_datos.strip() + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            cursor.execute(f'SELECT * FROM {nombre_tabla}')
            lis = cursor.fetchall()
            campos = cursor.description
            lista = []
            for li in lis:
                dic = {}
                c = 0
                for campo in campos[2:]:
                    dic.setdefault(campo[0], li[2:][c])
                    c += 1
                lista.append(dic)
            conexion.commit()
        except:
            conexion.rollback()
            lista = [] 
    except sqlite3.Error as e:
        lista = []
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        return lista


def cargar_lista_con_id_desde_db(base_datos, nombre_tabla):
    """Retorna una lista con los registros (todas sus claves - valor) de una tabla en una base de datos determinada

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): nombre de la tabla
    """
    base_datos_db = base_datos.strip() + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            cursor.execute(f'SELECT * FROM {nombre_tabla}')
            lis = cursor.fetchall()
            campos = cursor.description
            lista = []
            for li in lis:
                dic = {}
                c = 0
                for campo in campos:
                    dic.setdefault(campo[0], li[c])
                    c += 1
                lista.append(dic)
            conexion.commit()
        except:
            conexion.rollback()
            lista = []
    except sqlite3.Error as e:
        lista = []
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        return lista


def cargar_lista_con_id_desde_db_opcion(base_datos, nombre_tabla, estado=True):
    """Retorna una lista con los registros (todas sus claves - valor) de una tabla en una base de datos determinada pero solamente aquellos cuyo estado se determine como opción. La opción predeterminada estado=True no considera a los registros que fueron eliminados. Si la opción de estado la determinamos con False se devolverán los items eliminados

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): nombre de la tabla
        estado (bool, optional): True: registros en uso, False: registros eliminados
    """
    campo_estado = "estado"
    estado = str(int(estado))
    base_datos_db = base_datos.strip() + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            sql_select = f'SELECT * FROM {nombre_tabla} WHERE {campo_estado} = ?'
            cursor.execute(sql_select, estado)
            lis = cursor.fetchall()
            campos = cursor.description
            lista = []
            for li in lis:
                dic = {}
                c = 0
                for campo in campos:
                    dic.setdefault(campo[0], li[c])
                    c += 1
                lista.append(dic)
            conexion.commit()
        except:
            conexion.rollback()
            lista = []
    except sqlite3.Error as e:
        lista = []
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        return lista


def iniciar_carga_productos():
    """Carga en las variable productos los registros de las tablas productos, ingresos y egresos

    Returns:
        productos(list): productos
    """
    productos = cargar_lista_con_id_desde_db_opcion("crud", "productos")
    productos_copia_para_iterar = productos[:]
    ingresos = cargar_lista_con_id_desde_db_opcion("crud", "ingresos")
    egresos = cargar_lista_con_id_desde_db_opcion("crud", "egresos")
    ajustes = cargar_lista_con_id_desde_db_opcion("crud", "ajustes")
    for i in range(len(productos_copia_para_iterar)):
        productos[i].update({"ingreso": []})
        for j in range(len(ingresos)):
            if productos[i]["id"] == ingresos[j]["producto_id"]:
                productos[i]["ingreso"].append(ingresos[j])
        productos[i].update({"egreso": []})
        for k in range(len(egresos)):
            if productos[i]["id"] == egresos[k]["producto_id"]:
                productos[i]["egreso"].append(egresos[k])
        productos[i].update({"ajuste": []})
        for l in range(len(ajustes)):
            if productos[i]["id"] == ajustes[l]["producto_id"]:
                productos[i]["ajuste"].append(ajustes[l])
    return productos 


def iniciar_carga_productos_eliminados():
    """Carga en las variable productos_eliminados los registros de las tablas productos, ingresos y egresos que fueron eliminados permanecieron en las tablas con registro 'estado' = 0 ó False

    Returns:
        productos(list): productos_eliminados
    """
    productos_eliminados = cargar_lista_con_id_desde_db_opcion("crud", "productos", estado=False)
    for i in productos_eliminados:
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        i.update({"fecha_alta": fecha})
        i.update({"fecha_modificacion": ""})
        i.update({"fecha_baja": ""})
        i.update({"estado": True})
    productos_eliminados_copia_para_iterar = productos_eliminados[:]
    ingresos = cargar_lista_con_id_desde_db("crud", "ingresos")
    egresos = cargar_lista_con_id_desde_db("crud", "egresos")
    ajustes = cargar_lista_con_id_desde_db("crud", "ajustes")
    for i in range(len(productos_eliminados_copia_para_iterar)):
        cantidad_producto = 0
        productos_eliminados[i].update({"ingreso": []})
        for j in range(len(ingresos)):
            if productos_eliminados[i]["id"] == ingresos[j]["producto_id"]:
                ingresos[j].update({"estado": True})
                cantidad_producto += ingresos[j].get("cantidad_ingreso")
                productos_eliminados[i]["ingreso"].append(ingresos[j])
        productos_eliminados[i].update({"egreso": []})
        for k in range(len(egresos)):
            if productos_eliminados[i]["id"] == egresos[k]["producto_id"]:
                egresos[j].update({"estado": True})
                cantidad_producto -= egresos[j].get("cantidad_egreso")
                productos_eliminados[i]["egreso"].append(egresos[k])
        productos_eliminados[i].update({"ajuste": []})
        for l in range(len(ajustes)):
            if productos_eliminados[i]["id"] == ajustes[l]["producto_id"]:
                ajustes[j].update({"estado": True})
                cantidad_producto += ajustes[j].get("cantidad_ajuste")
                productos_eliminados[i]["ajuste"].append(ajustes[l])
        productos_eliminados[i].update({"cantidad": cantidad_producto})
    return productos_eliminados


def recuperar_producto_eliminados_en_db(base_datos, nombre_tabla, lista_productos):
    """Vuelve a traer al stock de productos los eliminados previamente actualizando su clave 'estado' a valor verdadero

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'productos' en este caso
        lista_productos (list): "id" de productos eliminados
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sublista_productos = []
    sublista_cantidad = []
    for i in lista_productos:
        sublista_productos.append(i[0])
        sublista_cantidad.append(i[1])
    campo_estado = "estado"
    campo_fecha_a = "fecha_alta"
    campo_fecha_m = "fecha_modificacion"
    campo_fecha_b = "fecha_baja"
    campo_id = "id"
    campo_cant = "cantidad"
    base_datos_db = base_datos.strip() + ".db"
    marcador_posicion = ', '.join('?' * len(sublista_productos))
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            sql_1 = f'UPDATE {nombre_tabla} SET {campo_estado} = ?, {campo_fecha_a} = ?, {campo_fecha_m} = ?, {campo_fecha_b} = ? WHERE {campo_id} IN ({marcador_posicion})'
            cursor.execute(sql_1, (True, fecha, "", "", *sublista_productos))
            for id_prod, cant_prod in lista_productos:
                sql_2 = f'UPDATE {nombre_tabla} SET {campo_cant} = ? WHERE {campo_id} = ?'
                cursor.execute(sql_2, (cant_prod, id_prod))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def recuperar_movimientos_producto_en_db(base_datos, nombre_tabla, productos_eliminados_a_recuperar):
    """Vuelve a traer al stock de los movimientos de productos eliminados previamente actualizando su clave 'estado' a valor ''True''

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (list): 'ingresos', 'egresos' o 'ajustes'
        productos_eliminados_a_recuperar (list): "id" de productos eliminados
    """
    id_productos_eliminados_a_recuperar = []
    for i in productos_eliminados_a_recuperar:
        id_productos_eliminados_a_recuperar.append(i[0])
    campo_estado = "estado"
    campo_id = "id"
    base_datos_db = base_datos.strip() + ".db"
    marcador_posicion = ', '.join('?' * len(id_productos_eliminados_a_recuperar))
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            sql = f'UPDATE {nombre_tabla} SET {campo_estado} = ? WHERE {campo_id} IN ({marcador_posicion})'
            cursor.execute(sql, (True, *id_productos_eliminados_a_recuperar))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def eliminar_producto_en_db(base_datos, nombre_tabla, lista_productos):
    """Elimina productos del stock actualizando su clave 'estado' a valor 'False'

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'productos' en este caso
        lista_productos (list): "id" de productos a eliminar
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    campo_fecha = "fecha_baja"
    campo_estado = "estado"
    campo_id = "id"
    base_datos_db = base_datos.strip() + ".db"
    marcador_posicion = ', '.join('?' * len(lista_productos))
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            sql_productos = f'UPDATE {nombre_tabla} SET {campo_estado} = ?, {campo_fecha} = ? WHERE {campo_id} IN ({marcador_posicion})'
            cursor.execute(sql_productos, (False, fecha, *lista_productos))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def eliminar_movimientos_producto_en_db(base_datos, nombre_tabla, productos_a_eliminar):
    """Elimina movimientos de productos del stock actualizando su clave 'estado' a valor 'False'

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (list): 'ingresos', 'egresos' o 'ajustes'
        productos_eliminados_a_recuperar (list): "id" de productos a eliminar
    
    """
    campo_estado = "estado"
    campo_id = "id"
    base_datos_db = base_datos.strip() + ".db"
    marcador_posicion = ', '.join('?' * len(productos_a_eliminar))
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            sql = f'UPDATE {nombre_tabla} SET {campo_estado} = ? WHERE {campo_id} IN ({marcador_posicion})'
            cursor.execute(sql, (False, *productos_a_eliminar))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def actualizar_item_movimiento_producto_en_db(base_datos, nombre_tabla, campo_item, nuevo_valor, nombre_tabla_2, item_mov):
    """Función que actualiza los valores de un movimiento del producto en la base de datos, pasando como argumentos el nombre de la base de datos, el nombre de la tabla de productos, el campo a actualizar, el nuevo valor, el nombre de la tabla del movimiento (ingresos, egresos, ajustes) y el registro con los nuevos valores (dicc)

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'productos'
        campo_item (str): 'cantidad'
        nuevo_valor (int): nuevo valor de cantidad del producto
        nombre_tabla_2 (str): 'imgresos', 'egresos' o 'ajustes'
        item_mov (dict): item movimiento
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    campo_fecha = "fecha_modificacion"
    campo_id = "id"
    item_id = item_mov["id"]
    producto_id = item_mov["producto_id"]
    campos_item_mov = list(item_mov)[2:]
    valores_item_mov = list(item_mov.values())[2:]
    nombres_claves = '= ? , '.join(campos_item_mov) + ' = ? '
    base_datos_db = base_datos.strip() + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            sql_nombre_tabla = f'UPDATE {nombre_tabla} SET {campo_item} = ?, {campo_fecha} = ? WHERE {campo_id} = ?'
            sql_nombre_tabla_2 = f'UPDATE {nombre_tabla_2} SET {nombres_claves} WHERE {campo_id} = ?'
            cursor.execute(sql_nombre_tabla, (nuevo_valor, fecha, producto_id))
            cursor.execute(sql_nombre_tabla_2, (*valores_item_mov, item_id))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def agregar_producto_db(base_datos, nombre_tabla, prod):
    """Crea un nuevo registro en la base de datos de un nuevo producto y devuelve el 'id' de ese nuevo registro para actualizar ese valor en lista de productos del sistema

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'productos'
        prod (dict): nuevo producto
    """
    campos_prod = list(prod)[1:]
    nombres_claves = ', '.join(campos_prod)
    valores_item= list(prod.values())[1:]
    valores_item[9] = valores_item[10] = valores_item[11] = prod.get(campos_prod[1])+"<=>"+prod.get(campos_prod[2])
    marcador_posicion = ', '.join('?' * len(campos_prod))
    base_datos_db = base_datos + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('''BEGIN TRANSACTION''')
            sql_crea_tabla = f'''CREATE TABLE IF NOT EXISTS {nombre_tabla} (id INTEGER PRIMARY KEY AUTOINCREMENT, {campos_prod[0]} TEXT NOT NULL, {campos_prod[1]} TEXT NOT NULL, {campos_prod[2]} TEXT NOT NULL, {campos_prod[3]} TEXT NOT NULL, {campos_prod[4]} TEXT NOT NULL, {campos_prod[5]} TEXT NOT NULL, {campos_prod[6]} TEXT NOT NULL, {campos_prod[7]} INTEGER NOT NULL, {campos_prod[8]} REAL NOT NULL, {campos_prod[9]} TEXT NOT NULL, {campos_prod[10]} TEXT NOT NULL, {campos_prod[11]} TEXT NOT NULL, {campos_prod[12]} DATE NOT NULL, {campos_prod[13]} DATE NOT NULL, {campos_prod[14]} DATE NOT NULL, {campos_prod[15]} BOOL NOT NULL)'''
            sql_inserta_registro = f'''INSERT INTO {nombre_tabla} ({nombres_claves}) VALUES ({marcador_posicion})'''
            cursor.execute(sql_crea_tabla)
            cursor.execute(sql_inserta_registro, valores_item)
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def actualizar_item_producto_en_db(base_datos, nombre_tabla, lista_productos, campo_item, nuevo_valor):
    """Actualiza un campo ('marca', 'modelo' o 'categoría') con un nuevo valor de una lista de productos que pertenecen a ese conjunto de ese campo seleccionado
    o actualiza ('descripción', 'codigo', 'marca', 'modelo', 'categoría', 'origen', 'ubicación' o 'precio') de un producto determinado

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'productos' en este caso
        lista_productos (list): "id" de los productos a actualizar
        campo_item (str): 'descripción', 'codigo', 'marca', 'modelo', 'categoría', 'origen', 'ubicación' o 'precio'
        nuevo_valor (str): nuevo valor del campo a actualizar
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    campo_fecha = "fecha_modificacion"
    campo_id = "id"
    base_datos_db = base_datos.strip() + ".db"
    marcador_posicion = ', '.join('?' * len(lista_productos))
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            sql = f'UPDATE {nombre_tabla} SET {campo_item} = ?, {campo_fecha} = ? WHERE {campo_id} IN ({marcador_posicion})'
            cursor.execute(sql, (nuevo_valor, fecha, *lista_productos))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def eliminar_item_producto_en_db(base_datos, nombre_tabla, producto_id, campo_item, nuevo_valor, nombre_tabla_2, items_id):
    """Elimina los movimientos seleccionados ('ingresos', 'egresos' o 'ajustes') de un producto actualizando el valor de la clave 'estado' en 'False' en el movimiento y cambiando el valor de la clave 'cantidad' del producto a partir de la eliminación de esos movimientos

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'productos'
        producto_id (int): 'id' del producto a eliminar movimientos
        campo_item (str): 'cantidad' del producto
        nuevo_valor (int): valor nuevo de la cantidad del producto
        nombre_tabla_2 (str): 'ingresos', 'egresos' o 'ajustes'
        items_id (list): lista de 'id' de los movimientos a eliminar
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    campo_fecha = "fecha_modificacion"
    campo_id = "id"
    campo_estado = "estado"
    base_datos_db = base_datos.strip() + ".db"
    marcador_posicion = ', '.join('?' * len(items_id))
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            cursor.execute(f'UPDATE {nombre_tabla} SET {campo_item} = ?, {campo_fecha} = ? WHERE {campo_id} = ?', (nuevo_valor, fecha, producto_id))
            sql = f'UPDATE {nombre_tabla_2} SET {campo_estado} = ? WHERE id IN ({marcador_posicion})'
            cursor.execute(sql, (False, *items_id))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def bloquear_usuario(base_datos, nombre_tabla, datos_usuario):
    """Bloquea el acceso de un usuario generando un valor de contraseña random y cambiando el valor original en la tabla por ese nuevo valor

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'usuarios'
        datos_usuario (list): dos valores: 'id' de usuario y valor nuevo de contraseña generada de manera random
    """
    campo_id = "id"
    campo_passw = "password_usuario"
    usuario_id = datos_usuario[0]
    usuario_passw = datos_usuario[1]
    base_datos_db = base_datos.strip() + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor() 
        try:
            conexion.execute('BEGIN TRANSACTION')
            sql = f'UPDATE {nombre_tabla} SET {campo_passw} = ? WHERE {campo_id} = ?'
            cursor.execute(sql , (usuario_passw, usuario_id))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def agregar_ajuste_producto_db(base_datos, nombre_tabla, campo_item, nuevo_valor, nuevo_item_id, nombre_tabla_2, mov):
    """Genera un nuevo registro de movimiento 'ingreso' en la tabla 'ingresos' o 'egreso' en la tabla 'egresos' y actualiza en la tabla 'productos' el nuevo valor en el campo 'cantidad'y devuelve el 'id' de ese nuevo movimiento

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'productos'
        campo_item (str): 'cantidad'
        nuevo_valor (int): nuevo valor de 'cantidad'
        nuevo_item_id (int): 'id' del producto
        nombre_tabla_2 (str): 'ingresos', 'egresos' o 'ajustes'
        mov (dict): nuevo movimiento
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    campo_fecha = "fecha_modificacion"
    campo_id = "id"
    campos = list(mov)
    base_datos_db = base_datos + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            cursor.execute(f'UPDATE {nombre_tabla} SET {campo_item} = ?, {campo_fecha} = ? WHERE {campo_id} = ?', (nuevo_valor, fecha, nuevo_item_id))
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {nombre_tabla_2} (id INTEGER PRIMARY KEY AUTOINCREMENT, {campos[1]} INTEGER NOT NULL REFERENCES productos(id), {campos[2]} DATE NOT NULL, {campos[3]} TEXT NOT NULL, {campos[4]} INTEGER NOT NULL, {campos[5]} BOOL NOT NULL)''')
            cursor.execute(f'''INSERT INTO {nombre_tabla_2} ({campos[1]}, {campos[2]}, {campos[3]}, {campos[4]}, {campos[5]}) VALUES (?, ?, ?, ?, ?)''', (mov.get(campos[1]), mov.get(campos[2]), mov.get(campos[3]), mov.get(campos[4]), True))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def agregar_ingreso_egreso_producto_db(base_datos, nombre_tabla, campo_item, nuevo_valor, nuevo_item_id, nombre_tabla_2, mov):
    """Genera un nuevo registro de movimiento 'ingreso' en la tabla 'ingresos' o 'egreso' en la tabla 'egresos' y actualiza en la tabla 'productos' el nuevo valor en el campo 'cantidad'y devuelve el 'id' de ese nuevo movimiento

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'productos'
        campo_item (str): 'cantidad'
        nuevo_valor (int): nuevo valor de 'cantidad'
        nuevo_item_id (int): 'id' del producto
        nombre_tabla_2 (str): 'ingresos', 'egresos' o 'ajustes'
        mov (dict): nuevo movimiento
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    campo_fecha = "fecha_modificacion"
    campo_id = "id"
    campos = list(mov)
    base_datos_db = base_datos + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            cursor.execute(f'UPDATE {nombre_tabla} SET {campo_item} = ?, {campo_fecha} = ? WHERE {campo_id} = ?', (nuevo_valor, fecha, nuevo_item_id))
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {nombre_tabla_2} (id INTEGER PRIMARY KEY AUTOINCREMENT, {campos[1]} INTEGER NOT NULL REFERENCES productos(id), {campos[2]} DATE NOT NULL, {campos[3]} TEXT NOT NULL, {campos[4]} TEXT NOT NULL, {campos[5]} INTEGER NOT NULL, {campos[6]} REAL NOT NULL, {campos[7]} REAL NOT NULL, {campos[8]} BOOL NOT NULL)''')
            cursor.execute(f'''INSERT INTO {nombre_tabla_2} ({campos[1]}, {campos[2]}, {campos[3]}, {campos[4]}, {campos[5]}, {campos[6]}, {campos[7]}, {campos[8]}) VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', (mov.get(campos[1]), mov.get(campos[2]), mov.get(campos[3]), mov.get(campos[4]), mov.get(campos[5]), mov.get(campos[6]), mov.get(campos[7]), True))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def agregar_usuario_en_db(base_datos, nombre_tabla, user):
    """Crea un nuevo registro de usuario en la base de datos y devuele el 'id' de ese nuevo usuario para actualizarla en ese mismo usuarios en la variable de lista de usuarios en el sistema

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'usuarios'
        user (dict): nuevo registro de usuario
    """
    campos_user = list(user)[1:]
    nombres_claves = ', '.join(campos_user)
    valores_user= list(user.values())[1:]
    marcador_posicion = ', '.join('?' * len(campos_user))
    base_datos_db = base_datos + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('''BEGIN TRANSACTION''')
            sql_crea_tabla = f'''CREATE TABLE IF NOT EXISTS {nombre_tabla} (id INTEGER PRIMARY KEY AUTOINCREMENT, {campos_user[0]} TEXT NOT NULL, {campos_user[1]} TEXT NOT NULL, {campos_user[2]} TEXT NOT NULL, {campos_user[3]} TEXT NOT NULL, {campos_user[4]} TEXT NOT NULL, {campos_user[5]} BOOL NOT NULL, {campos_user[6]} BOOL NOT NULL, {campos_user[7]} DATE NOT NULL, {campos_user[8]} DATE NOT NULL, {campos_user[9]} DATE NOT NULL, {campos_user[10]} BOOL NOT NULL)'''
            sql_inserta_registro = f'''INSERT INTO {nombre_tabla} ({nombres_claves}) VALUES ({marcador_posicion})'''
            cursor.execute(sql_crea_tabla)
            cursor.execute(sql_inserta_registro, valores_user)
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def recuperar_usuarios_eliminados_en_db(base_datos, nombre_tabla, lista_usuarios):
    """ Vuelve a traer al CRUD usuarios eliminados actualizando su campo 'estado' a True

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'usuarios'
        lista_usuarios (list): lista de 'id' de usuarios a recuperar
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    campo_fecha_a = "fecha_alta"
    campo_fecha_m = "fecha_modificacion"
    campo_fecha_b = "fecha_baja"
    campo_estado = "estado"
    campo_id = "id"
    base_datos_db = base_datos.strip() + ".db"
    marcador_posicion = ', '.join('?' * len(lista_usuarios))
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            sql = f'UPDATE {nombre_tabla} SET {campo_estado} = ?, {campo_fecha_a} = ?, {campo_fecha_m} = ?, {campo_fecha_b} = ? WHERE {campo_id} IN ({marcador_posicion})'
            cursor.execute(sql, (True, fecha, "", "", *lista_usuarios))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def eliminar_usuario_en_db(base_datos, nombre_tabla, lista_usuarios):
    """Elimina usuarios en la tabla 'usuarios' en la base de datos actualizando su campo 'estado' a False y generando un valor en la clave 'fecha de baja'

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'usuarios'
        lista_usuarios (list): lista de 'id' de usuarios a eliminar
    """
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    campo_fecha_b = "fecha_baja"
    campo_estado = "estado"
    campo_id = "id"
    base_datos_db = base_datos.strip() + ".db"
    marcador_posicion = ', '.join('?' * len(lista_usuarios))
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            sql_productos = f'UPDATE {nombre_tabla} SET {campo_estado} = ?, {campo_fecha_b} = ? WHERE {campo_id} IN ({marcador_posicion})'
            cursor.execute(sql_productos, (False, fecha, *lista_usuarios))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def actualizar_usuario_en_db(base_datos, nombre_tabla, usuario_editado):
    """Actualiza en la base de datos, en la tabla 'usuarios' los todos los campos del registro con los nuevos valores del usuario
    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'usuarios'
        usuario_editado (dict): nuevo registro de usuario
    """
    campo_id = "id"
    usuario_id = usuario_editado["id"]
    campos_usuario = list(usuario_editado)[1:]
    valores_usuario = list(usuario_editado.values())[1:]
    nombres_claves = '= ? , '.join(campos_usuario) + ' = ? '
    base_datos_db = base_datos.strip() + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('BEGIN TRANSACTION')
            sql_nombre_tabla_2 = f'UPDATE {nombre_tabla} SET {nombres_claves} WHERE {campo_id} = ?'
            cursor.execute(sql_nombre_tabla_2, (*valores_usuario, usuario_id))
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()


def agregar_logs_usuario_en_db(base_datos, nombre_tabla, log_usuario):
    """Crea en la base de datos, dentro de la tabla 'logs_usuarios' un seguimiento de actividad de cada usuario

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'logs_usuarios'
        log_usuario (dict): nuevo registro de usuario
    """
    campos_user = list(log_usuario)[1:]
    nombres_claves = ', '.join(campos_user)
    valores_user= list(log_usuario.values())[1:]
    marcador_posicion = ', '.join('?' * len(campos_user))
    base_datos_db = base_datos + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('''BEGIN TRANSACTION''')
            sql_crea_tabla = f'''CREATE TABLE IF NOT EXISTS {nombre_tabla} (id INTEGER PRIMARY KEY AUTOINCREMENT, {campos_user[0]} INTEGER NOT NULL REFERENCES usuarios(id) , {campos_user[1]} TEXT NOT NULL, {campos_user[2]} DATE NOT NULL, {campos_user[3]} INTEGER NOT NULL REFERENCES productos(id), {campos_user[4]} INTEGER NOT NULL, {campos_user[5]} INTEGER NOT NULL REFERENCES ingresos(id), {campos_user[6]} INTEGER NOT NULL REFERENCES egresos(id), {campos_user[7]} INTEGER NOT NULL REFERENCES ajustes(id), {campos_user[8]} DATE NOT NULL, {campos_user[9]} DATE NOT NULL, {campos_user[10]} INTEGER NOT NULL, {campos_user[11]} INTEGER NOT NULL, {campos_user[12]} INTEGER NOT NULL, {campos_user[13]} INTEGER NOT NULL, {campos_user[14]} BOOL NOT NULL, {campos_user[15]} BOOL NOT NULL, {campos_user[16]} BOOL NOT NULL)'''
            sql_inserta_registro = f'''INSERT INTO {nombre_tabla} ({nombres_claves}) VALUES ({marcador_posicion})'''
            cursor.execute(sql_crea_tabla)
            cursor.execute(sql_inserta_registro, valores_user)
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()



def eliminar_logs_usuario_en_db(base_datos, nombre_tabla):
    """Elimina en la base de datos, los registros de la tabla 'logs_usuarios'

    Args:
        base_datos (str): nombre de la base de datos (sin la extensión .db)
        nombre_tabla (str): 'logs_usuarios'
        log_usuario (dict): nuevo registro de usuario
    """
    base_datos_db = base_datos + ".db"
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('''BEGIN TRANSACTION''')
            sql_elimina_registros = f'''DELETE FROM {nombre_tabla}'''
            cursor.execute(sql_elimina_registros)
            conexion.commit()
        except:
            conexion.rollback()
    except sqlite3.Error as e:
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()



def generar_reportes_tiempo_usuario_en_db(base_datos, nombre_tabla, fecha_desde, fecha_hasta, usuario):
    """Trae de la DB los registros entre fechas dadas para generar reporte de tiempo de uso de cada usuario del sistema
    """
    fecha_desde += ' 00:00:00'
    fecha_hasta += ' 23:59:59'
    lis_consulta = []
    base_datos_db = base_datos + ".db"
    campos = ['id', 'id_usuario', 'lugar_usuario', 'momento_usuario', 'id_producto', 'id_usuario_a_gestionar' ,'id_ingreso_producto', 'id_egreso_producto', 'id_ajuste_producto', 'inicio_logueo', 'final_logueo', 'tiempo_log_en_segundos', 'momento_actual_serie', 'momento_final_serie', 'momento_cero', 'ope_ingreso', 'ope_egreso', 'ope_ajuste']
    nombre_tabla_padre = 'usuarios'
    campos_padre = ["id", "mail", "perfil_acceso", "estado"]
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        if usuario["perfil_acceso"] == "administrador":
            try:
                conexion.execute('''BEGIN TRANSACTION''')
                sql_consulta = f"""SELECT {campos[1]}, {campos_padre[1]}, {campos_padre[2]}, {campos[10]}, {campos[11]} FROM {nombre_tabla} JOIN {nombre_tabla_padre} ON {nombre_tabla}.{campos[1]} = {nombre_tabla_padre}.{campos_padre[0]} WHERE {campos[10]} BETWEEN ? AND ? AND {campos[14]} = ? ORDER BY {campos[1]} ASC"""
                cursor.execute(sql_consulta, (fecha_desde, fecha_hasta, 0))
                consulta = cursor.fetchall()
                lis_consulta.append(consulta)
                lis_consulta.append([fecha_desde[:10], fecha_hasta[:10]])
                conexion.commit()
            except:
                conexion.rollback()
                lis_consulta = []
        elif usuario["perfil_acceso"] == "supervisor":
            try:
                conexion.execute('''BEGIN TRANSACTION''')
                sql_consulta = f"""SELECT {campos[1]}, {campos_padre[1]}, {campos_padre[2]}, {campos[10]}, {campos[11]} FROM {nombre_tabla} JOIN {nombre_tabla_padre} ON {nombre_tabla}.{campos[1]} = {nombre_tabla_padre}.{campos_padre[0]} WHERE {campos[10]} BETWEEN ? AND ? AND {campos[14]} = ? AND {campos_padre[2]} IN (?, ?, ?) ORDER BY {campos[1]} ASC"""
                cursor.execute(sql_consulta, (fecha_desde, fecha_hasta, 0, "supervisor", "vendedor", "consultas"))
                consulta = cursor.fetchall()
                lis_consulta.append(consulta)
                lis_consulta.append([fecha_desde[:10], fecha_hasta[:10]])
                conexion.commit()
            except:
                conexion.rollback()
                lis_consulta = []
    except sqlite3.Error as e:
        lis_consulta = []
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        return lis_consulta



def generar_reportes_ventas_en_db(base_datos, nombre_tabla, fecha_desde, fecha_hasta, usuario):
    """trae de la db los resgistros de los usuarios que realizaron ventas de productos entre fechas dadas 
    """
    fecha_desde += ' 00:00:00'
    fecha_hasta += ' 23:59:59'
    lis_consulta = []
    base_datos_db = base_datos + ".db"
    campos = ['id', 'id_usuario', 'lugar_usuario', 'momento_usuario', 'id_producto', 'id_usuario_a_gestionar' ,'id_ingreso_producto', 'id_egreso_producto', 'id_ajuste_producto', 'inicio_logueo', 'final_logueo', 'tiempo_log_en_segundos', 'momento_actual_serie', 'momento_final_serie', 'momento_cero', 'ope_ingreso', 'ope_egreso', 'ope_ajuste']
    nombre_tabla_padre = 'usuarios'
    nombre_tabla_padre_2 = 'productos'
    nombre_tabla_padre_3 = 'egresos'
    campos_padre = ["id", "mail", "perfil_acceso", "estado"]
    campos_padre_2 = ["id", "codigo", "marca"]
    campos_padre_3 = ["id", "cantidad_egreso", "valor_venta"]
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        if usuario["perfil_acceso"] == "administrador":
            try:
                conexion.execute('''BEGIN TRANSACTION''')
                sql_consulta = f"""SELECT {campos[1]}, {campos_padre[1]}, {campos_padre[2]}, {campos[3]}, {campos[4]}, {campos_padre_2[1]}, {campos_padre_2[2]}, {campos_padre_3[1]}, {campos_padre_3[2]} FROM {nombre_tabla} JOIN {nombre_tabla_padre} ON {nombre_tabla}.{campos[1]} = {nombre_tabla_padre}.{campos_padre[0]} JOIN {nombre_tabla_padre_2} ON {nombre_tabla}.{campos[4]} = {nombre_tabla_padre_2}.{campos_padre_2[0]} JOIN {nombre_tabla_padre_3} ON {nombre_tabla}.{campos[7]} = {nombre_tabla_padre_3}.{campos_padre_3[0]} WHERE {campos[3]} BETWEEN ? AND ? AND {campos[16]} = ? ORDER BY {campos[1]} ASC"""
                cursor.execute(sql_consulta, (fecha_desde, fecha_hasta, True))
                consulta = cursor.fetchall()
                lis_consulta.append(consulta)
                lis_consulta.append([fecha_desde[:10], fecha_hasta[:10]])
                conexion.commit()
            except:
                conexion.rollback()
                lis_consulta = []
        elif usuario["perfil_acceso"] == "supervisor":
            try:
                conexion.execute('''BEGIN TRANSACTION''')
                sql_consulta = f"""SELECT {campos[1]}, {campos_padre[1]}, {campos_padre[2]}, {campos[3]}, {campos[4]}, {campos_padre_2[1]}, {campos_padre_2[2]}, {campos_padre_3[1]}, {campos_padre_3[2]} FROM {nombre_tabla} JOIN {nombre_tabla_padre} ON {nombre_tabla}.{campos[1]} = {nombre_tabla_padre}.{campos_padre[0]} JOIN {nombre_tabla_padre_2} ON {nombre_tabla}.{campos[4]} = {nombre_tabla_padre_2}.{campos_padre_2[0]} JOIN {nombre_tabla_padre_3} ON {nombre_tabla}.{campos[7]} = {nombre_tabla_padre_3}.{campos_padre_3[0]} WHERE {campos[3]} BETWEEN ? AND ? AND {campos[16]} = ? AND {campos_padre[2]} = ? ORDER BY {campos[1]} ASC"""
                cursor.execute(sql_consulta, (fecha_desde, fecha_hasta, True, "vendedor"))
                consulta = cursor.fetchall()
                lis_consulta.append(consulta)
                lis_consulta.append([fecha_desde[:10], fecha_hasta[:10]])
                conexion.commit()
            except:
                conexion.rollback()
                lis_consulta = []
    except sqlite3.Error as e:
        lis_consulta = []
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        return lis_consulta


def generar_reporte_de_bajo_stock(base_datos, nombre_tabla, cantidad_piso, cantidad_techo):
    """Trae de la DB los registros entre fechas dadas para generar reporte de tiempo de uso de cada usuario del sistema
    """
    base_datos_db = base_datos + ".db"
    campos = ["id", "descripcion", "codigo", "marca", "modelo", "categoria", "origen", "ubicacion", "cantidad", "precio", "ingreso", "egreso", "ajuste", "fecha_modificacion", "fecha_alta", "fecha_baja", "estado"]
    try:
        conexion = sqlite3.connect(base_datos_db)
        cursor = conexion.cursor()
        try:
            conexion.execute('''BEGIN TRANSACTION''')
            sql_consulta = f"""SELECT {campos[0]}, {campos[2]}, {campos[3]}, {campos[4]}, {campos[1]}, {campos[8]} FROM {nombre_tabla} WHERE {campos[8]} BETWEEN ? AND ? ORDER BY {campos[3]} ASC, {campos[4]} ASC, {campos[1]} ASC, {campos[2]} ASC"""
            cursor.execute(sql_consulta, (cantidad_piso, cantidad_techo))
            consulta = cursor.fetchall()
            conexion.commit()
        except:
            conexion.rollback()
            consulta = []
    except sqlite3.Error as e:
        consulta = []
        mensaje ('✕ NO SE PUDO ESTABLECER LA CONEXIÓN: {e} ✕')
    finally:
        if cursor:
            cursor.close()
        if conexion:
            conexion.close()
        return consulta
