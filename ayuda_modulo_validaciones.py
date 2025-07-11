from utilidades import clear_screen
from interfaz_usuario import mensaje, mensaje_2
from validaciones import correo_valido, de_caracter_a_float, validar_fecha



clear_screen()
mensaje_2('## Módulo VALIDACIONES')
print()
mensaje('# Función correo_valido')
print(correo_valido.__doc__)
print()
mensaje('# Función de_caracter_a_float')
print(de_caracter_a_float.__doc__)
print()
mensaje('# Función validar_fecha')
print(validar_fecha.__doc__)