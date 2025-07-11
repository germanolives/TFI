from utilidades import clear_screen
from interfaz_usuario import mensaje, mensaje_2
from principal import principal



clear_screen()
mensaje_2('## Módulo PRINCIPAL')
print()
mensaje('# Función principal')
print(principal.__doc__)