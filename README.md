# Procesador de Documentos de Grado

Esta aplicación automatiza el procesamiento de documentos PDF relacionados con el proceso de grado. Diploma, actas, etc

## Requisitos

- Windows 7 o superior.

## Instalación

1. Copie el ejecutable `ProcesadorDocsGrados.exe` en el directorio deseado.
2. Coloque el archivo de configuración `PARAMETROS_PROCESADOR_ARCHIVOS.xlsx` en el mismo directorio que el ejecutable.
3. Si es necesario, ajuste las rutas dentro del archivo Excel a las carpetas específicas en su sistema.

## Uso

Doble clic en `ProcesadorDocsGrados.exe` para iniciar la aplicación. Siga las instrucciones en pantalla para procesar los documentos o comprimir los directorios.

## Soporte

Este proyecto fue elaborado por Luisa Rincon <lfrincon@javerianacali.edu.co>

## Creacion del ejecutable
# La opción --onefile le indica a PyInstaller que cree un único archivo ejecutable. 
pyinstaller --onefile ProcesamientoDiplomas.py
