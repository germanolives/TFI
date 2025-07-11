from utilidades import clear_screen
from interfaz_usuario import mensaje, mensaje_2
from usuarios import agregar_usuario, editar_usuario, seguir_usuario, iniciar_logs_usuario_json, genera_bloque_rastreo_usuario_json, genera_bloque_rastreo_usuario_db, finalizar_logs_usuario_json



clear_screen()
mensaje_2('## Módulo USUARIOS')
print()
mensaje('# Función agregar_usuario')
print(agregar_usuario.__doc__)
print()
mensaje('# Función editar_usuario')
print(editar_usuario.__doc__)
print()
mensaje('# Función seguir_usuario')
print(seguir_usuario.__doc__)
print()
mensaje('# Función iniciar_logs_usuario_json')
print(iniciar_logs_usuario_json.__doc__)
print()
mensaje('# Función genera_bloque_rastreo_usuario_json')
print(genera_bloque_rastreo_usuario_json.__doc__)
print()
mensaje('# Función genera_bloque_rastreo_usuario_db')
print(genera_bloque_rastreo_usuario_db.__doc__)
print()
mensaje('# Función finalizar_logs_usuario_json')
print(finalizar_logs_usuario_json.__doc__)