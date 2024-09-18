# Procesador de Documentos de Grado

## Descripción General
Este proyecto proporciona una solución automatizada para procesar documentos académicos, como diplomas y actas de grado, extraer datos clave utilizando expresiones regulares configurables y gestionar los archivos procesados.

## Requisitos
- Windows 7 o superior.

## Requerimientos Funcionales

1. **Procesamiento de PDFs**: La aplicación procesa documentos PDF, extrayendo nombres y datos relevantes mediante expresiones regulares configurables.
2. **Organización de Archivos**: Crea una carpeta individual para cada estudiante cuyos datos son procesados, donde se almacenan todos los documentos procesados por estudiante.
3. **Compresión de Archivos**: Comprime carpetas en formato ZIP para facilitar la distribución de cada carpeta.
4. **Generación de Reportes**: Genera un informe en formato Excel detallando los archivos procesados, su ubicación y cualquier error o problema encontrado.
5. **Configuración Dinámica**: 

## Requerimientos No Funcionales

1. **Usabilidad**: La interfaz es intuitiva, facilitando la operación por usuarios sin conocimientos técnicos avanzados.
3. **Seguridad**: Gestiona de forma segura la información confidencial extraída de los documentos.
4. **Mantenibilidad**: El código está bien organizado y documentado, simplificando futuras actualizaciones y mantenimiento. Utiliza un archivo de configuración externo (`PARAMETROS_PROCESADOR_ARCHIVOS.xlsx`) para especificar rutas y parámetros operativos sin intervenir el código fuente
5. **Compatibilidad**: Compatible con las versiones más comunes de Windows, distribuida como un ejecutable.

## Diseño
![UMLDiagram.png](doc%2FUMLDiagram.png)

## Soporte
Este proyecto fue elaborado por Luisa Rincon <lfrincon@javerianacali.edu.co>

## Creacion del ejecutable 
La opción --onefile le indica a PyInstaller que cree un único archivo ejecutable.
>pyinstaller --onefile ProcesamientoDiplomas.py
 
## Instalación
1. Copie el ejecutable `ProcesadorDocsGrados.exe` en el directorio deseado.
2. Coloque el archivo de configuración `PARAMETROS_PROCESADOR_ARCHIVOS.xlsx` en el mismo directorio que el ejecutable.
3. Si es necesario, ajuste las rutas dentro del archivo Excel a las carpetas específicas en su sistema.

## Uso
Doble clic en `ProcesadorDocsGrados.exe` para iniciar la aplicación. Siga las instrucciones en pantalla para procesar
los documentos o comprimir los directorios.

### Versiones
- 1.0.0: Versión Inicial
- 1.0.1: Agrega validación en el caso de parametros nulos en el archivo de configuración por filas vacías y actualiza expresión regular para detectar el nombre de los diplomas