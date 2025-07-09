from utilidades import clear_screen
from interfaz_usuario import mensaje, mensaje_2
from validaciones import correo_valido, de_caracter_a_float, validar_fecha



clear_screen()
mensaje_2('## Módulo VALIDACIONES')
print()
mensaje('# Función correo_valido')
help(correo_valido)
print()
mensaje('# Función de_caracter_a_float')
help(de_caracter_a_float)
print()
mensaje('# Función validar_fecha')
help(validar_fecha)