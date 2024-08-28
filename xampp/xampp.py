from os import system
from os.path import isdir, expanduser
import subprocess

def func_containsKW(param):
    caracteres_validos = (
        "abcdefghijklmnopqrstuvwxyz"
        "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
    )
    validos_set = set(caracteres_validos)
    for char in param:
        if char in validos_set:
            return True
    return False

def func_containsNum(param):
    for char in param:
        if char.isdigit():
            return True
    return False

def clear():
    system("clear")

def func_cpToPath(pathStart, pathEnd):
    # Nota: `sudo` puede requerir la contraseña del usuario
    # Asegúrate de que `pathStart` y `pathEnd` sean rutas absolutas válidas
    system(f"sudo cp -r {pathStart} {pathEnd}")

def func_get_valid_path(prompt):
    while True:
        path = input(prompt)
        path = expanduser(path)  # Expande ~ a la ruta del usuario
        if isdir(path):  # Verifica si la ruta es un directorio válido
            return path
        else:
            print(f"La ruta '{path}' no existe o no es un directorio válido...")

def func_QuestXampp_Run():
    try:
        result = subprocess.run(['ps','aux'],stdout=subprocess.PIPE,text=True)
        output = result.stdout
        apache_running = 'httpd' in output or 'apache2' in output
        mysql_running = 'mysql' in output
        return apache_running and mysql_running
    
    except Exception as e:
        print(f"Error al verificar el estado de Xampp:{e}")
        return False

def main():
    clear()
    w_op = True
    D_pathEnd = "/opt/lampp/htdocs"

    ms_outRes = ("\n1.-Iniciar sistema grafico\n2.-Agregar proyecto\n3.-Instalar xampp\n4.-Iniciar servidor xampp\n5.-Parar servidor xampp\n6.-limpiar consola\n0.-cerrar")
    ms_outPathStart = "Ingresa la ruta de la carpeta que deseas agregar..."
    ms_outPathEnd = "Quieres ingresarlo a Htdocs Xampp?"

    ms_res = "\nROOT::USER~>| "

    consoleRun__xampp = "sudo /opt/lampp/manager-linux-x64.run"

    ms_err = "Demasiados intentos erróneos, favor de ingresar los datos correctos"
    ms_err1 = "Favor de ingresar valores válidos"

    ms_end = "Programa finalizado"
    i = 0
    while w_op:
        if i >= 3:
            clear()
            print(ms_err)
            break
        
        __op = input(ms_outRes + ms_res)
        
        if func_containsKW(__op):
            clear()
            i += 1
            print(ms_err1)
        else:
            i = 0
            if func_containsNum(__op):
                __op = int(__op)
                if __op == 0:
                    clear()
                    if func_QuestXampp_Run():
                        system("sudo /opt/lampp/lampp stop")
                    print(ms_end)
                    break
                elif __op == 1:
                    clear()
                    system(consoleRun__xampp)
                elif __op == 2:
                    clear()
                    __pathStart = func_get_valid_path(ms_outPathStart + ms_res)
                    
                    __pathEnd = input(ms_outPathEnd + ms_res + "[S/n]:: ")
                    if __pathEnd.lower() == "n":
                        __pathEnd = func_get_valid_path("Ingresa la ruta de destino..." + ms_res)
                        func_cpToPath(__pathStart, __pathEnd)
                    else:
                        func_cpToPath(__pathStart, D_pathEnd)
                        print("Se ha copiado correctamente")
                elif __op == 4:
                    clear()
                    system("sudo /opt/lampp/lampp start")
                elif __op == 5:
                    clear()
                    if func_QuestXampp_Run():
                        system("sudo /opt/lampp/lampp stop")
                elif __op == 6:
                    clear()
                else:
                    clear()
                    print(ms_err1)
            else:
                clear()
                print(ms_err1)

if __name__ == "__main__":
    main()
