import datetime


def correo_valido(mail):
    """Función que recibe un string y valida si dicha cadena de caracteres puede ser o no una dirección de correo electrónico. Devuelve una tupla: la cadena que recibió y verdadero o falso de acuerdo a si esa cadena es un correo.

    Args:
        mail (str): correo a validar

    Returns:
        tuple: _mail, bool
    """
    caracteres_validos = "abcdefghijklmnopqrstuvwxyz0123456789._-@"
    caracteres_invalidos_primer_ultimo_caracter = "._-@"
    cant_caract_mail = len(mail)
    valido = False
    if cant_caract_mail:
        mail = mail.strip().lower()
        c = 0
        for i in mail:
            if i in caracteres_validos:
                c += 1
        if cant_caract_mail == c:
            if mail.count("@") == 1 and mail[0] not in caracteres_invalidos_primer_ultimo_caracter and mail[-1] not in caracteres_invalidos_primer_ultimo_caracter:
                mail_dividido = mail.split("@", 2)
                usuario = mail_dividido[0]
                dominio = mail_dividido[1]
                if len(usuario) <= 64 and usuario[-1] not in caracteres_invalidos_primer_ultimo_caracter and dominio[0] not in caracteres_invalidos_primer_ultimo_caracter and dominio.count(".") >= 1:
                    valido = True
    return mail, valido


def de_caracter_a_float (x):
    """FUnción que convierte un string válido en un número float

    Args:
        x (str): valor de entrada

    Returns:
        float: número válido
    """
    valores_validos = "0123456789.-"
    contador_caracteres_validos = 0
    cantidad_puntos = 0
    cantidad_guiones = 0
    x = x.strip()
    for i in range(len(x)):
        for j in range (len(valores_validos)):
            if x[i] == valores_validos[j]:
                contador_caracteres_validos += 1
                if x[i] == ".":
                    cantidad_puntos += 1
                elif x[i] == "-":
                    cantidad_guiones += 1
    if x != "" and contador_caracteres_validos == len(x) and x != "-." and x != ".-" and x != "-" and x != "." and x[-1] != "-" and 0 <= cantidad_puntos <= 1 and (cantidad_guiones == 0 or (cantidad_guiones == 1 and x[0] == "-")):
        return float(x)
    else:
        x = bool(0)
        return x


def validar_fecha(fecha_a_validar):
    """Función que devuelve una fecha en un formato válido

    Args:
        fecha_a_validar (str): valor de la fecha a validar

    Returns:
        (str): fecha validada o fecha no valida (false)
    """
    fecha_a_validar = str(fecha_a_validar).strip()
    fecha_a_validar += ' 12:00:00'
    try:
        fecha = datetime.datetime.strptime(fecha_a_validar, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return False
    else:
        return fecha
    
