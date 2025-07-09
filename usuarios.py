import datetime, getpass, json
from database import agregar_logs_usuario_en_db
from interfaz_usuario import imprimir_lista
from validaciones import correo_valido


def agregar_usuario(perfiles_usuario):
    """Función que crea un nuevo usuario al sistema 

    Args:
        perfiles_usuario (list): lista de perfiles de acceso
    """
    usuario = {"id": 0, "nombre": "", "apellido": "",  "mail": "", "password_usuario": "", "perfil_acceso": "", "tracking_json": True, "tracking_db": True, "fecha_modificacion": "", "fecha_alta": "", "fecha_baja": "", "estado": True}
    for i in usuario:
        clave = i
        contenido_clave = usuario.get(i)
        if clave != "id" and clave != "fecha_modificacion" and clave!= "fecha_alta" and clave != "fecha_baja" and clave != "estado" and clave != "tracking_json" and clave != "tracking_json" and clave != "tracking_db":                        
            if isinstance(contenido_clave, str):
                if clave != "mail" and clave != "perfil_acceso" and clave != "password_usuario":
                    valor = input(f"\n• {clave.title()}: ").strip().lower()
                    while valor == "":
                        valor = input(f"\n• {clave.title()}: ").strip().lower()
                    usuario[i] = valor
                elif clave == "mail":
                    valor = input(f"\n• {clave.title()}: ").strip().lower()
                    while not correo_valido(valor)[1]:
                        valor = input(f"\n• {clave.title()}: ").strip().lower()
                    usuario[i] = valor
                elif clave == "perfil_acceso":
                    print()
                    imprimir_lista(perfiles_usuario, "Perfiles de Acceso")
                    valor = input(f"\n• : ").strip().lower()
                    while valor not in perfiles_usuario:
                        valor = input(f"\n• : ").strip().lower()
                    usuario[i] = valor
                else:
                    primera, segunda = "x", "y"
                    while primera != segunda:
                        valor = getpass.getpass(f"\n• {clave.title()}: ").strip()
                        #valor= input(f"\n• {clave.title()}: ").strip()
                        while valor == "":
                            valor = getpass.getpass(f"\n• {clave.title()}: ").strip()
                        primera = valor
                        valor = getpass.getpass(f"\n• {clave.title()} (Repetir): ").strip()
                        #valor = input(f"\n• {clave.title()} (Repetir): ").strip()
                        while valor == "":
                            valor = getpass.getpass(f"\n• {clave.title()} (Repetir): ").strip()
                        segunda = valor
                    usuario[i] = valor
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")           
    usuario["fecha_alta"] = fecha
    return usuario 


def editar_usuario(usuario_a_editar, perfiles, nro_opcion, usuarios, usuario, logs_usuario, id_autoinc):
    """Funcion que edita datos del usuario a partir de los datos de ese usuario a editar, una lista de perfiles de acceso de los usuarios y una opción que indica la clave a editar

    Args:
        usuario (dict): usuario a editar
        perfiles (list): lista de perfiles de acceso al sistema
        nro_opcion (int): nro opción que indica índice del campo a modificar
    """
    clave = list(usuario_a_editar)
    if nro_opcion == 1 or nro_opcion == 2:
        valor_anterior = usuario_a_editar[clave[nro_opcion]]
        valor = input(f"\n• {clave[nro_opcion].title()} ⟨Nuevo Dato⟩: ").strip().lower()
        while valor == "":
            valor = input(f"\n• {clave[nro_opcion].title()} ⟨Nuevo Dato⟩: ").strip().lower()
        usuario_a_editar[clave[nro_opcion]] = valor
    elif nro_opcion == 3:
        valor_anterior = usuario_a_editar[clave[nro_opcion]]
        valor = input(f"\n• {clave[nro_opcion].title()} ⟨Nuevo Dato⟩: ").strip().lower()
        while not correo_valido(valor)[1]:
            valor = input(f"\n• {clave[nro_opcion].title()} ⟨Nuevo Dato⟩: ").strip().lower()
        usuario_a_editar[clave[nro_opcion]] = valor
    elif nro_opcion == 4:
        valor_anterior = usuario_a_editar[clave[nro_opcion]]
        primera, segunda = "x", "y"
        while primera != segunda:
            valor = getpass.getpass(f"\n• {clave[nro_opcion].title()} ⟨Nuevo Dato⟩: ").strip()
            while valor == "":
                valor = getpass.getpass(f"\n• {clave[nro_opcion].title()} ⟨Nuevo Dato⟩: ").strip()
            primera = valor
            valor = getpass.getpass(f"\n• {clave[nro_opcion].title()} ⟨Nuevo Dato⟩ (Repetir): ").strip()
            while valor == "":
                valor = getpass.getpass(f"\n• {clave[nro_opcion].title()} ⟨Nuevo Dato⟩ (Repetir): ").strip()
            segunda = valor
        usuario_a_editar[clave[nro_opcion]] = valor
    elif nro_opcion == 5:
        print()
        imprimir_lista(perfiles, "Perfiles de Acceso")
        valor_anterior = usuario_a_editar[clave[nro_opcion]]
        valor = input(f"\n• {clave[nro_opcion].title()} ⟨Nuevo Dato⟩: ").strip().lower()
        while valor not in perfiles:
            valor = input(f"\n• {clave[nro_opcion].title()} ⟨Nuevo Dato⟩: ").strip().lower()
        usuario_a_editar[clave[nro_opcion]] = valor
    elif nro_opcion == 6 or nro_opcion == 7:
        valor_anterior = usuario_a_editar[clave[nro_opcion]]
        valor = input(f"\n• {clave[nro_opcion].title()} ⟨Nuevo Dato⟩: ").strip().lower()
        while not(valor == "0" or valor == "1"):
            valor = input(f"\n• {clave[nro_opcion].title()} ⟨Nuevo Dato⟩: ").strip().lower()
        usuario_a_editar[clave[nro_opcion]] = int(valor)
    etapa_usuario, id_autoinc = seguir_usuario(usuario, id_autoinc,f"usuario cambia de: {clave[nro_opcion]}: '{valor_anterior}' a {clave[nro_opcion]}: '{valor}'", id_usuario_a_gestionar=usuario_a_editar.get("id"))
    logs_usuario.append(etapa_usuario)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")                
    usuario_a_editar["fecha_modificacion"] = fecha
    return id_autoinc, usuario_a_editar 


def seguir_usuario(usuario, id_autoinc ,etapa, id_producto=0, id_usuario_a_gestionar=0, id_ingreso_producto=0, id_egreso_producto=0, id_ajuste_producto=0, ope_ingreso=False, ope_egreso=False, ope_ajuste=False):
    """Función de crea un diccionario con la información recibida del momento en que se encuentra el usuario en el flujo del programa. La función retorna ese diccionario y una variable tipo entera incrementada en uno para que lo tome la próxima función que la requiera. Ese id_autoinc funciona en el programa como un id autoincremental único que identifica a cada movimiento del usuario. Comienza con un valor dado por el archivo 'logs_usuario.json'. Si este archivo no fue creado todavía id_autoinc toma un valor 0 (cero). De lo contrario toma el valor almacenado en ese archivo.

    Args:
        usuario (dicc): usuario
        id_autoinc (int): variable id autoincremental
        etapa (str): describe el momento del usuario
        id_producto (int, optional): id del producto
        id_usuario_a_gestionar (int, optional): id del usuario a gestionar
        id_ingreso_producto (int, optional): id de movimiento de compra de un producto
        id_egreso_producto (int, optional): id de movimiento de venta de un producto
        id_ajuste_producto (int, optional): id de movimiento de ajuste de un producto
        ope_ingreso (bool, optional): valor true si hubo una compra
        ope_egreso (bool, optional): valor true si hubo una venta
        ope_ajuste (bool, optional): valor true si hubo un ajuste

    Returns:
        logs_usuario (dicc): dato del movimiento del usuario
        id_autoinc (int): id del dato del movimiento del usuario
    """
    id_autoinc += 1
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_usuario = {}
    log_usuario["id"] = id_autoinc
    log_usuario["id_usuario"] = usuario["id"]
    log_usuario["lugar_usuario"] = etapa
    log_usuario["momento_usuario"] = fecha
    log_usuario["id_producto"] = id_producto
    log_usuario["id_usuario_a_gestionar"] = id_usuario_a_gestionar
    log_usuario["id_ingreso_producto"] = id_ingreso_producto
    log_usuario["id_egreso_producto"] = id_egreso_producto
    log_usuario["id_ajuste_producto"] = id_ajuste_producto
    log_usuario["inicio_logueo"] = ""
    log_usuario["final_logueo"] = ""
    log_usuario["tiempo_log_en_segundos"] = 0
    log_usuario["momento_actual_serie"] = 0
    log_usuario["momento_final_serie"] = 0
    log_usuario["momento_cero"] = 0
    log_usuario["ope_ingreso"] = ope_ingreso
    log_usuario["ope_egreso"] = ope_egreso
    log_usuario["ope_ajuste"] = ope_ajuste
    return log_usuario, id_autoinc 


def iniciar_logs_usuario_json():
    """Función que lee el archivo 'logs_usuarios.json', si este existe retorna el último id del ultimo registro almacenado en ese archivo json. Si no devuelve cero ese ese id_autoinc. También devuelve una lista vacía en donde se irán agregando los momentos del usuario.

    Returns:
        _type_: _description_
    """
    logs_usuario = []
    filename = f'logs_usuarios.json'
    try:
        with open(filename, encoding='utf-8') as archivo:
            logs_usuario_previos = json.load(archivo)
            id_autoinc = logs_usuario_previos[-1][-1]["id"]
    except FileNotFoundError:
        id_autoinc = 0
    finally:
        return logs_usuario, id_autoinc 



def genera_bloque_rastreo_usuario_json(logs_usuario):
    """Función que actualiza algunos campos de los diccionarios que conforman la lista de los eventos del usuario durante una sesión en la que estuvo logueado, retornando esa lista actualizada

    Args:
        logs_usuario (list): lista de diccionarios de eventos de un usuario durante una sesión

    Returns:
        logs_usuario (list): lista de diccionarios de eventos de un usuario durante una sesión, actualizada
    """
    inicio_logueo = logs_usuario[0]["momento_usuario"].strip()
    final_logueo = logs_usuario[-1]["momento_usuario"].strip()
    ini_logueo = datetime.datetime.strptime(inicio_logueo, "%Y-%m-%d %H:%M:%S")
    fin_logueo = datetime.datetime.strptime(final_logueo, "%Y-%m-%d %H:%M:%S")
    dif_tiempo = fin_logueo - ini_logueo
    tiempo_en_log = int(dif_tiempo.total_seconds())
    cant_logs = len(logs_usuario)
    c = 0
    for log_usuario in logs_usuario:
        c += 1
        log_usuario["inicio_logueo"] = inicio_logueo
        log_usuario["final_logueo"] = final_logueo
        log_usuario["tiempo_log_en_segundos"] = tiempo_en_log
        log_usuario["momento_actual_serie"] = c
        log_usuario["momento_final_serie"] = cant_logs
        log_usuario["momento_cero"] = cant_logs-c
    return logs_usuario


def genera_bloque_rastreo_usuario_db(logs_usuario):
    """Función que actualiza algunos campos de los diccionarios que conforman la lista de los eventos del usuario durante una sesión en la que estuvo logueado y guarda en la base de datos esos registros

    Args:
        logs_usuario (list): lista de diccionarios de eventos de un usuario durante una sesión
    """
    inicio_logueo = logs_usuario[0]["momento_usuario"].strip()
    final_logueo = logs_usuario[-1]["momento_usuario"].strip()
    ini_logueo = datetime.datetime.strptime(inicio_logueo, "%Y-%m-%d %H:%M:%S")
    fin_logueo = datetime.datetime.strptime(final_logueo, "%Y-%m-%d %H:%M:%S")
    dif_tiempo = fin_logueo - ini_logueo
    tiempo_en_log = int(dif_tiempo.total_seconds())
    cant_logs = len(logs_usuario)
    c = 0
    for log_usuario in logs_usuario:
        c += 1
        log_usuario["inicio_logueo"] = inicio_logueo
        log_usuario["final_logueo"] = final_logueo
        log_usuario["tiempo_log_en_segundos"] = tiempo_en_log
        log_usuario["momento_actual_serie"] = c
        log_usuario["momento_final_serie"] = cant_logs
        log_usuario["momento_cero"] = cant_logs-c
        agregar_logs_usuario_en_db("crud", "logs_usuarios", log_usuario)


def finalizar_logs_usuario_json(logs_usuario):
    """Función que agrega la lista de los eventos de un usuario durante su sesión en un archivo json existente

    Args:
        logs_usuario (_type_): _description_
    """
    filename = f'logs_usuarios.json'
    try:
        with open(filename, encoding='utf-8') as archivo:
            archivo = open(filename, encoding='utf-8')
            logs_usuario_previos = json.load(archivo)
    except FileNotFoundError:
        logs_usuario_previos = []
    finally:
        logs_usuario_previos.append(logs_usuario)
        with open(filename, 'w', encoding='utf-8') as archivo:
            json.dump(logs_usuario_previos, archivo, ensure_ascii=False, indent=4)


