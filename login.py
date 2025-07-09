import getpass
from database import bloquear_usuario
from interfaz_usuario import mostrar_menu, opcion_menu, mensaje, mensaje_2
from utilidades import string_random, clear_screen
from variables import lista_alfa_omega, lista_inicio_fin



def iniciar_login(usuarios):
    """Función que de manera interactiva devuelve usuario válido dentro de una lista de usuarios, solamente devuelve usuario válido con mail y contraseña respaldada en base de datos, si el usuario es válido y hay más de 5 intentos de contraseña incorrectos, se bloquea ese usuario cambiándole la contraseña por una cadena aleatoria de caracteres.

    Args:
        usuarios (list): lista de usuarios
    """
    usuario = {}
    bucle_menu_login = True
    while bucle_menu_login:
        clear_screen()
        mostrar_menu("   TIENDA / CRUD • Menú [LOG-IN] →", lista_alfa_omega, 1, 1, True, 1, "[SALIR]", "", "")
        match opcion_menu(2, "Ingresar DATOS"):
            case 1:
                clear_screen()
                intentos_usuario = 0
                usuario_correcto = False
                while not usuario_correcto and intentos_usuario < 6:
                    clear_screen()
                    mensaje_2("Inicio de Sesión")
                    mail_usuario = input("USUARIO: ")
                    intentos_usuario += 1
                    for i in usuarios:
                        if i.get("mail") == mail_usuario:
                            usuario_correcto = True
                            usuario = i
                if intentos_usuario < 6:
                    intentos_contras = 1
                    contras = getpass.getpass("CONTRASEÑA: ")
                    while contras != usuario["password_usuario"] and intentos_contras < 6:
                        clear_screen()
                        mensaje_2("Inicio de Sesión")
                        print("USUARIO:", usuario["mail"])
                        contras = getpass.getpass("CONTRASEÑA: ")
                        if usuario["perfil_acceso"] != "administrador":
                            intentos_contras += 1
                    if intentos_contras > 5:
                        usuario.update({"password_usuario": string_random(48)})
                        usuario_bloqueado = [usuario["id"], usuario["password_usuario"]]
                        bloquear_usuario("crud", "usuarios", usuario_bloqueado)
                        print("\n")
                        clear_screen()
                        mensaje("🛒   USUARIO BLOQUEADO   ✕")
                        mostrar_menu("   Menú [RAIZ] →", lista_inicio_fin, 1, 1, True, 1, "← Salir", "", "")
                        match opcion_menu(2, "Ingresar DATOS"):
                            case 1:
                                clear_screen()
                            case 2:
                                clear_screen()
                                mensaje("🔚")
                                bucle_menu_login = False
                    else:
                        return (usuario)
                else:
                    print("\n")
                    clear_screen()
                    mensaje("🛒   USUARIO INEXISTENTE   ✕")
                    mostrar_menu("   Menú [RAIZ] →", lista_inicio_fin, 1, 1, True, 1, "← Salir", "", "")
                    match opcion_menu(2, "Ingresar DATOS"):
                        case 1:
                            clear_screen()
                        case 2:
                            clear_screen()
                            mensaje("🔚")
            case 2:
                clear_screen()
                mensaje("🔚")
                bucle_menu_login = False
"""
"""