from os import system
from os.path import isdir, expanduser
import subprocess

# Variables descriptivas para los mensajes de salida
MSG_MAIN_MENU = (
    "\n1.- Iniciar sistema gráfico\n"
    "2.- Agregar proyecto\n"
    "3.- Instalar Xampp\n"
    "4.- Iniciar servidor Xampp\n"
    "5.- Parar servidor Xampp\n"
    "6.- Limpiar consola\n"
    "7.- Desinstalar Xampp\n"
    "8.- Seguridad\n"
    "0.- Cerrar"
)
PROMPT_PATH_START = "Ingresa la ruta de la carpeta que deseas agregar..."
PROMPT_PATH_END = "¿Quieres ingresarlo a Htdocs Xampp? [S/n]:: "
PROMPT_DEST_PATH = "Ingresa la ruta de destino..."
PROMPT_USER = "\nROOT::USER~>| "
MSG_ERROR_TOO_MANY_ATTEMPTS = "Demasiados intentos erróneos, favor de ingresar los datos correctos"
MSG_ERROR_INVALID_INPUT = "Favor de ingresar valores válidos"
MSG_PROGRAM_ENDED = "Programa finalizado"
MSG_COPY_SUCCESS = "Se ha copiado correctamente"
MSG_CONFIRM_UNINSTALL = "¿Está seguro de desinstalar? [S/n]:: "
MSG_CONFIRM_SECURITY = "¿Está seguro de realizar cambios en la seguridad? [S/n]:: "

# Rutas del sistema
XAMPP_MANAGER_PATH = "/opt/lampp/./manager-linux-x64.run"
XAMPP_START_PATH = "/opt/lampp/lampp start"
XAMPP_STOP_PATH = "/opt/lampp/lampp stop"
XAMPP_UNINSTALL_PATH = "/opt/lampp/./uninstall"
XAMPP_SECURITY_PATH = "/opt/lampp/lampp security"
XAMPP_INSTALLER_PATH = "~/Desktop/autXampp/xampp/./xampp-linux-x64-8.2.12-0-installer.run"
XAMPP_HTDOCS_PATH = "/opt/lampp/htdocs"

def func_containsKW(param):
    caracteres_validos = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    )
    validos_set = set(caracteres_validos)
    return any(char in validos_set for char in param)

def func_containsNum(param):
    return any(char.isdigit() for char in param)

def clear():
    system("sudo clear")

def func_cpToPath(pathStart, pathEnd):
    # Nota: `sudo` puede requerir la contraseña del usuario
    # Asegúrate de que `pathStart` y `pathEnd` sean rutas absolutas válidas
    system(f"sudo cp -r {pathStart} {pathEnd}")

def func_get_valid_path(prompt):
    while True:
        path = input(prompt + PROMPT_USER)
        path = expanduser(path)  # Expande ~ a la ruta del usuario
        if isdir(path):  # Verifica si la ruta es un directorio válido
            return path
        else:
            print(f"La ruta '{path}' no existe o no es un directorio válido...")

def func_QuestXampp_Run():
    try:
        result = subprocess.run(['ps', 'aux'], stdout=subprocess.PIPE, text=True)
        output = result.stdout
        apache_running = 'httpd' in output or 'apache2' in output
        mysql_running = 'mysql' in output
        return apache_running and mysql_running
    except Exception as e:
        print(f"Error al verificar el estado de Xampp: {e}")
        return False

def main():
    clear()
    w_op = True
    D_pathEnd = XAMPP_HTDOCS_PATH

    attempt_count = 0
    max_attempts = 3
    while w_op:
        if attempt_count >= max_attempts:
            clear()
            print(MSG_ERROR_TOO_MANY_ATTEMPTS)
            break
        
        __op = input(MSG_MAIN_MENU + PROMPT_USER)
        
        if func_containsKW(__op):
            clear()
            attempt_count += 1
            print(MSG_ERROR_INVALID_INPUT)
        else:
            attempt_count = 0
            if func_containsNum(__op):
                __op = int(__op)
                if __op == 0:
                    clear()
                    if func_QuestXampp_Run():
                        system(f"sudo {XAMPP_STOP_PATH}")
                    print(MSG_PROGRAM_ENDED)
                    break
                elif __op == 1:
                    clear()
                    system(f"sudo {XAMPP_MANAGER_PATH}")
                elif __op == 2:
                    clear()
                    __pathStart = func_get_valid_path(PROMPT_PATH_START)
                    
                    __pathEnd = input(PROMPT_PATH_END)
                    if __pathEnd.lower() == "n":
                        __pathEnd = func_get_valid_path(PROMPT_DEST_PATH)
                        func_cpToPath(__pathStart, __pathEnd)
                    else:
                        func_cpToPath(__pathStart, D_pathEnd)
                        print(MSG_COPY_SUCCESS)
                elif __op == 4:
                    clear()
                    system(f"sudo {XAMPP_START_PATH}")
                elif __op == 5:
                    clear()
                    if func_QuestXampp_Run():
                        system(f"sudo {XAMPP_STOP_PATH}")
                elif __op == 6:
                    clear()
                elif __op == 3:
                    system(f"sudo chmod +x {XAMPP_INSTALLER_PATH}")
                    system(f"sudo {XAMPP_INSTALLER_PATH}")
                elif __op == 7:
                    desinstalar = input(MSG_CONFIRM_UNINSTALL)
                    if desinstalar.lower() in ("s", "y"):
                        system(f"sudo {XAMPP_UNINSTALL_PATH}")
                    else:
                        clear()
                elif __op == 8:
                    seguro = input(MSG_CONFIRM_SECURITY)
                    if seguro.lower() in ("s", "y"):
                        system(f"sudo {XAMPP_SECURITY_PATH}")
                    else:
                        clear()
                else:
                    clear()
                    print(MSG_ERROR_INVALID_INPUT)
            else:
                clear()
                print(MSG_ERROR_INVALID_INPUT)

if __name__ == "__main__":
    main()
    
