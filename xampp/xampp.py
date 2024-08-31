from os import system
from os.path import isdir, expanduser
import subprocess
from time import sleep
import json

# Variables descriptivas para los mensajes de salida
MSG_MAIN_MENU = ("\n"
    "1.- Iniciar servidor Xampp\n"
    "2.- Parar servidor Xampp\n"
    "3.- Agregar proyecto\n"
    "4.- Iniciar sistema gráfico\n"
    "5.- Instalar Xampp\n"
    "6.- Desinstalar Xampp\n"
    "7.- Limpiar consola\n"
    "8.- Seguridad\n"
    "9.- Rutas de proyectos\n"
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
MSG_CONFIRM_UNINSTALL = "¿Está seguro de desinstalar? [s/N]:: "
MSG_CONFIRM_SECURITY = "¿Está seguro de realizar cambios en la seguridad? [s/N]:: "
MSG_RUTASDES = ("Que quieres hacer?\n"
                "\n1.-Agregar una nueva ruta"
                "\n2.-Eliminar una ruta"
                "\n3.-Modificar una ruta"
                "\n4.-Borrar todas las rutas"
                "\n5.-Agregar una cantidad de rutas"
                "\n6.-Ver las rutas"
                "\n0.-Cerrar opciones"
                )
MSG_INRUN = "El programa ya fue iniciado"
MSG_NORUN = "El programa no ha sido iniciado"
MSG_ERROR_OPTION_PATH = "Ingresa una opcion valida en la opcion '9'"
MSG_CLOSE_OPTION_PATH = "Cerrando operaciones de rutas..."
# Rutas del sistema
XAMPP_MANAGER_PATH = "/opt/lampp/./manager-linux-x64.run"
XAMPP_START_PATH = "/opt/lampp/lampp start"
XAMPP_STOP_PATH = "/opt/lampp/lampp stop"
XAMPP_UNINSTALL_PATH = "/opt/lampp/./uninstall"
XAMPP_SECURITY_PATH = "/opt/lampp/lampp security"
XAMPP_INSTALLER_PATH = "~/Desktop/autXampp/xampp/./xampp-linux-x64-8.2.12-0-installer.run"
XAMPP_HTDOCS_PATH = "/opt/lampp/htdocs"
DATA_JSONFILES = "~/Desktop/autXampp/xampp/data/paths.json"

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
    system("clear")

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

def func_ReadPath__FILE(param):
    """
    Debe de poder leer un archivo json y que devuelva su contenido en un diccionario
    :param param: Ruta del archivo json
    :return: contenido del json como un diccionario
    """
    try:
        param = expanduser(param)  # Expande ~ a la ruta del usuario
        with open(param, 'r') as archivo:
            contenido = json.load(archivo)
        return contenido
        
    except FileNotFoundError:
        print(f"El archivo {param} no se encuentra")
        return None
    
    except json.JSONDecodeError:
        print("Error al decodificar el archivo json")
        return None
    
    except Exception as error:
        print(f"Ocurrio un error: {error}")
        return None

def func_addPath(name,path,param):
    param = expanduser(param)
    try:
        with open(param,'r') as file:
            data = json.load(file)        
        data[name]=path
        
        with open(param, 'w') as file:
            json.dump(data,file,indent=4)
        print(f"Directorio '{name}' agregado exitosamente")
    
    except FileNotFoundError:
        print(f"El archivo '{param}' no se encontró.")
    
    except json.JSONDecodeError:
        print(f"Error al leer el archivo '{param}'. Asegúrate de que esté en formato JSON válido.")
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def func_delPath(name,pathParam):
    pathParam = expanduser(pathParam)
    try:
        with open(pathParam,'r') as file:
            data = json.load(file)
        if name in data:#? Busca si el valor existe en el diccionario
            del data[name]#? Elimina el directorio del diccionario
            #* Escribir los cambios devuelta al archivo
            with open(pathParam,'w') as file:
                json.dump(data,file,indent=4)
            print(f"Directorio '{name}' borrado exitosamente")
        else:
            print(f"El directorio '{name}' no se encontro en el archivo")
    except FileNotFoundError:
        print(f"El archivo '{pathParam}' no se encontró")
    
    except json.JSONDecodeError:
        print(f"Error al leer el archivo '{pathParam}'. Asegúrate de que esté en formato JSON válido")
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")
def func_modPath(name, newPath, pathParam):
    pathParam = expanduser(pathParam)
    try:
        with open(pathParam, 'r') as file:
            data = json.load(file)
        if name in data:
            data[name] = newPath
            with open(pathParam, 'w') as file:
                json.dump(data, file, indent=4)
            print(f"Directorio '{name}' modificado exitosamente")
        else:
            print(f"El directorio '{name}' no se encontró en el archivo")
    except FileNotFoundError:
        print(f"El archivo '{pathParam}' no se encontró")
    
    except json.JSONDecodeError:
        print(f"Error al leer el archivo '{pathParam}'. Asegúrate de que esté en formato JSON válido")
    
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def __main_opt__0():
    clear()
    if func_QuestXampp_Run():
        system(f"sudo {XAMPP_STOP_PATH}")
    print(MSG_PROGRAM_ENDED)
def __main_opt__1():#? Iniciar servidor
    clear()
    if func_QuestXampp_Run():
        clear()
        print(MSG_INRUN)
        sleep(0.5)
    else:
        system(f"sudo {XAMPP_START_PATH}")

def __main_opt__2():#? Finalizar servidor
    clear()
    if func_QuestXampp_Run():
        system(f"sudo {XAMPP_STOP_PATH}")
    else:
        clear()
        print(MSG_NORUN)
        sleep(0.5)
def __main_opt__3(D_pathEnd):#? Agregar proyecto
    clear()
    __optAP = input()
    if func_containsKW(__optAP):
        print()
    elif func_containsNum(__optAP):
        print()
    __pathStart = func_get_valid_path(PROMPT_PATH_START)
    
    __pathEnd = input(PROMPT_PATH_END)
    if __pathEnd.lower() == "n":
        __pathEnd = func_get_valid_path(PROMPT_DEST_PATH)
        func_cpToPath(__pathStart, __pathEnd)
    else:
        func_cpToPath(__pathStart, D_pathEnd)
        print(MSG_COPY_SUCCESS)

def __main_opt__4():#? Iniciar sistema grafico
    clear()
    system(f"sudo {XAMPP_MANAGER_PATH}")

def __main_opt__5():#? Instalar xampp
    system(f"sudo chmod +x {XAMPP_INSTALLER_PATH}")
    system(f"sudo {XAMPP_INSTALLER_PATH}")


def __main_opt__6():
    desinstalar = input(MSG_CONFIRM_UNINSTALL)
    if desinstalar.lower() in ("s", "y"):
        system(f"sudo {XAMPP_UNINSTALL_PATH}")
    else:
        clear()

def __main_opt__8():
    seguro = input(MSG_CONFIRM_SECURITY)
    if seguro.lower() in ("s", "y"):
        system(f"sudo {XAMPP_SECURITY_PATH}")
    else:
        clear()

def __main_opt__9_0():
    clear()
    print(MSG_CLOSE_OPTION_PATH)
    sleep(0.5)

def __main_opt__9_1():
    clear()
    modName = input("Ingresa el nombre de la ruta:"+PROMPT_USER)
    modPath = input("Ingresa la ruta"+PROMPT_USER)
    func_addPath(modName,modPath,param=DATA_JSONFILES)

def __main_opt__9_2(__PATHINTOJSON):
    if __PATHINTOJSON is not None:
        for clave, valor in __PATHINTOJSON.items():
            clear()
            print(f"\nNombre:{clave} = {valor}")
    else:
        print("No se pudo leer el valor del archivo json")
    delName = input(f"Ingresa el nombre de la ruta que desea eliminar\n{PROMPT_USER}")
    func_delPath(delName,pathParam=DATA_JSONFILES)

def __main_opt__9_3(__PATHINTOJSON):
    clear()
    if __PATHINTOJSON is not None:
        for clave, valor in __PATHINTOJSON.items():
            print(f"\nNombre: {clave} = {valor}")
    else:
        print("No se pudo leer el valor del archivo JSON")
    
    modName = input("Ingresa el nombre de la ruta que deseas modificar" + PROMPT_USER)
    modPath = input("Ingresa la nueva ruta" + PROMPT_USER)
    func_modPath(modName, modPath, pathParam=DATA_JSONFILES)

def __main_opt__9_6(__PATHINTOJSON):
    if __PATHINTOJSON is not None:
        for clave, valor in __PATHINTOJSON.items():
            clear()
            print(f"{clave}: {valor}")
    else:
        print("No se pudo leer el valor del archivo json")

def __main_opt__9(__PATHINTOJSON):
    clear()
    rutasDes = input(MSG_RUTASDES + PROMPT_USER)
    if func_containsKW(rutasDes):
        print(MSG_ERROR_OPTION_PATH)
    elif func_containsNum(rutasDes):
        clear()
        rutasDes = int(rutasDes)
        if rutasDes == 0:
            
            __main_opt__9_0()
        elif rutasDes == 1:
            __main_opt__9_1()
        elif rutasDes == 2:
            __main_opt__9_2(__PATHINTOJSON)
        elif rutasDes == 3:
            __main_opt__9_3(__PATHINTOJSON)
        elif rutasDes == 6:
            __main_opt__9_6(__PATHINTOJSON)

def main():
    clear()
    __PATHINTOJSON = func_ReadPath__FILE(DATA_JSONFILES)
    sleep(0.5)
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
                    __main_opt__0()
                    break
                elif __op == 1:#? Iniciar servidor
                    __main_opt__1()
                elif __op == 2:#? Finalizar servidor
                    __main_opt__2()
                elif __op == 3:#? Agregar proyecto
                    __main_opt__3(D_pathEnd=D_pathEnd)
                elif __op == 4:#? Iniciar sistema grafico
                    __main_opt__4()
                elif __op == 5:#? Instalar xampp
                    __main_opt__5()
                elif __op == 6:#? Desinstalar xampp
                    __main_opt__6()
                elif __op == 7:
                    clear()
                elif __op == 8:#? Seguridad
                    __main_opt__8()
                elif __op == 9:#? Rutas de proyectos
                    __main_opt__9(__PATHINTOJSON=__PATHINTOJSON)
                else:
                    clear()
                    print(MSG_ERROR_INVALID_INPUT)
            else:
                clear()
                print(MSG_ERROR_INVALID_INPUT)

if __name__ == "__main__":
    main()
