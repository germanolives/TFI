from database import cargar_lista_con_id_desde_db_opcion
from login import iniciar_login
from principal import principal

def main():
    """Función main del programa donde se cargan los usuarios desde la base de datos, se loguea el usuario y puede ejecutar el programa y al salir tiene la opción de volver a loguearse antes de salir definitivamente del crud o puede loguearse otro usuario
    """
    usuarios = cargar_lista_con_id_desde_db_opcion("crud", "usuarios")
    usuario = iniciar_login(usuarios)
    while usuario:
        if principal(usuario, usuarios):
            usuario= iniciar_login(usuarios)

main()