from utilidades import clear_screen
from interfaz_usuario import mensaje, mensaje_2
from utilidades import clear_screen, convertir_segundos_a_horas, crear_listas_valores, crear_listas_valores_dos_claves, ordenar_lista, string_random



clear_screen()
mensaje_2('## Módulo UTILIDADES')
print()
mensaje('# Función clear_screen')
print(clear_screen.__doc__)
print()
mensaje('# Función convertir_segundos_a_horas')
print(convertir_segundos_a_horas.__doc__)
print()
mensaje('# Función crear_listas_valores')
print(crear_listas_valores.__doc__)
print()
mensaje('# Función crear_listas_valores_dos_claves')
print(crear_listas_valores_dos_claves.__doc__)
print()
mensaje('# Función ordenar_lista')
print(ordenar_lista.__doc__)
print()
mensaje('# Función string_random')
print(string_random.__doc__)