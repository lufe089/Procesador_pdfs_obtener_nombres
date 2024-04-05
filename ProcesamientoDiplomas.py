# This is a sample Python script.
import os
import sys

from Vista import Vista

if __name__ == '__main__':
    # Obtiene el directorio donde se encuentra el ejecutable generado
    # Determina si se está ejecutando como un script o como un ejecutable generado por PyInstaller
    if getattr(sys, 'frozen', False):
        # Si se ejecuta como un ejecutable de PyInstaller
        directorio_ejecutable = os.path.dirname(sys.executable)
    else:
        # Si se ejecuta como un script normal (durante el desarrollo)
        directorio_ejecutable = os.path.dirname(os.path.abspath(__file__))

    # Construye la ruta al archivo de parámetros
    ruta_archivo_parametros = os.path.join(directorio_ejecutable, 'PARAMETROS_PROCESADOR_ARCHIVOS.xlsx')

    # ruta_archivo_parametros = 'C:/ProcesarDiplomas/PARAMETROS_PROCESADOR_ARCHIVOS.xlsx'

    log_path = '.'
    vista = Vista(ruta_archivo_parametros, log_path)
    vista.mostrar_menu()
