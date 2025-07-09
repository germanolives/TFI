from utilidades import clear_screen
from interfaz_usuario import mensaje, mensaje_2
from usuarios import agregar_usuario, editar_usuario, seguir_usuario, iniciar_logs_usuario_json, genera_bloque_rastreo_usuario_json, genera_bloque_rastreo_usuario_db, finalizar_logs_usuario_json



clear_screen()
mensaje_2('## Módulo USUARIOS')
print()
mensaje('# Función agregar_usuario')
help(agregar_usuario)
print()
mensaje('# Función editar_usuario')
help(editar_usuario)
print()
mensaje('# Función seguir_usuario')
help(seguir_usuario)
print()
mensaje('# Función iniciar_logs_usuario_json')
help(iniciar_logs_usuario_json)
print()
mensaje('# Función genera_bloque_rastreo_usuario_json')
help(genera_bloque_rastreo_usuario_json)
print()
mensaje('# Función genera_bloque_rastreo_usuario_db')
help(genera_bloque_rastreo_usuario_db)
print()
mensaje('# Función finalizar_logs_usuario_json')
help(finalizar_logs_usuario_json)