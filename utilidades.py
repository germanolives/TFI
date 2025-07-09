import datetime
import os
import random
import string



def clear_screen():
    """Función que borra la pantalla de la consola con un argumento que varía de acuerdo a la plataforma
    """
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux - macOS
        os.system('clear')


def convertir_segundos_a_horas(segundos):
  """Convierte segundos a formato HH:MM:SS usando datetime."""
  return str(datetime.timedelta(seconds=segundos))


def crear_listas_valores(lis, cla):
    """Función que crea una lista de valores a partir de una lista y una clave dada

    Args:
        lis (list): lista
        cla (str): clave
    """
    sublis = []
    for i in lis:
        sublis.append(i.get(cla))
    sublista = []
    for i in sublis:
        if i not in sublista:
            sublista.append(i)
    return sublista 


def crear_listas_valores_dos_claves(lis, cla, cla2):
    """Función crea una lista de valores a partir de una lista y de dos claves dadas

    Args:
        lis (list): lista
        cla (str): clave 1
        cla2 (str): clave 2
    """
    sublis = []
    for i in lis:
        sublis.append([i.get(cla), i.get(cla2)])
    sublista = []
    for i in sublis:
        if i not in sublista:
            sublista.append(i)
    return sublista 


def ordenar_lista(lis, cla, cla_ID, cla_ID2, asc):
    """Funcion que ordena una lista de diccionarios por todas sus claves en forma ascendente y descendente

    Args:
        lis (_type_): _description_
        cla (_type_): _description_
        cla_ID (_type_): _description_
        cla_ID2 (_type_): _description_
        asc (bool): orden

    Returns:
        _type_: _description_
    """
    for i in range(len(lis)-1):
        for j in range(len(lis)-1):
            valor_cla = lis[j].get(cla)
            valor_cla_prox = lis[j+1].get(cla)
            valor_cla_ID = lis[j].get(cla_ID)
            valor_cla_ID_prox = lis[j+1].get(cla_ID)
            valor_cla_ID2 = lis[j].get(cla_ID2)
            valor_cla_ID2_prox = lis[j+1].get(cla_ID2)
            match asc:
                case True:           
                    if (valor_cla > valor_cla_prox) or (valor_cla == valor_cla_prox and valor_cla_ID > valor_cla_ID_prox) or (valor_cla == valor_cla_prox and valor_cla_ID == valor_cla_ID_prox and valor_cla_ID2 > valor_cla_ID2_prox):
                        aux = lis[j]
                        lis[j] = lis[j+1]
                        lis[j+1] = aux                        
                case False:           
                    if (valor_cla < valor_cla_prox) or (valor_cla == valor_cla_prox and valor_cla_ID < valor_cla_ID_prox) or (valor_cla == valor_cla_prox and valor_cla_ID == valor_cla_ID_prox and valor_cla_ID2 > valor_cla_ID2_prox):
                        aux = lis[j]
                        lis[j] = lis[j+1]
                        lis[j+1] = aux
    return lis


def string_random(val):
    """Función que genera un cadena de caracteres de forma aleatoria y de una longitud determinada por el argumento pasado

    Args:
        val (int): longitud del string
    """
    caracteres_a_usar = string.ascii_letters + string.ascii_lowercase + string.ascii_uppercase + string.digits + "[}]{?¿!'·@$&%/()-_.,;:"
    resul = ""
    for i in range(val):
        resul += random.choice(caracteres_a_usar)
    return resul 