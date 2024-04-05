import os
import re
import shutil

from PyPDF2 import PdfReader

# Configurar el directorio de trabajo donde están los PDFs
"""
Version inicial que luego mutó a la versión con clases
"""

CONECTOR_DIPLOMA = 'DECANO DE FACUL TAD'
DIPLOMA_PRE = 'Diploma'


def extraer_nombre(texto, expresion_regular):
    # Modificar la expresión regular según el formato de los nombres en tus PDFs

    # Usando fr antes de las comillas, le indicamos a Python que interprete la cadena como una f-string (permitiendo la inserción de la variable nombre_a_buscar) y al mismo tiempo como una cadena cruda (ignorando cualquier secuencia de escape dentro de la expresión regular)."
    # patron_nombre = re.compile(fr'{patron_separador}: (\w+ \w+)')
    # Buscamos después de 'DECANO DE FACUL TAD' y capturamos hasta el salto de línea
    patron = re.compile(expresion_regular)
    busqueda = patron.search(texto)
    if busqueda:
        return busqueda.group(1)
    return None


def encontrar_nombre_en_texto(texto):
    expresion_regular_diploma = fr"DECANO DE FACUL TAD([^\n]+)"

    # Expresión regular para buscar después de 'A' y capturar hasta el salto de línea
    expresion_regular_a_saber_pro = r"A:\s*\n\s*(.+?)\n"
    expresion_regular_mencion_honor = r"\bA\b\s*\n\s*([^\n]+)"
    expresion_regular_a_acta = r"A\n(.+?)\n"
    # Expresión regular para buscar después de 'CONSIDERANDO QUE:' y capturar hasta el salto de línea
    expresion_regular_considerando_que = r"CONSIDERANDO QUE:\s*\n(.+?)\n"

    nombre = extraer_nombre(texto, expresion_regular_diploma)
    if nombre:
        return nombre
    else:
        nombre_merito_academico = extraer_nombre(texto, expresion_regular_considerando_que)
        if nombre_merito_academico is not None:
            return nombre_merito_academico
        else:
            nombre_saber_pro = extraer_nombre(texto, expresion_regular_a_saber_pro)
            if nombre_saber_pro:
                return nombre_saber_pro
            else:
                nombre_acta_grado = extraer_nombre(texto, expresion_regular_a_acta)
                if nombre_acta_grado:
                    return nombre_acta_grado
                else:
                    nombre_mencion_honor = extraer_nombre(texto, expresion_regular_mencion_honor)
                    if nombre_mencion_honor:
                        return nombre_mencion_honor
    return None  # Si no retorna por alguno de los otros caminos es que no se encontró


def procesar_pdfs(ruta_pdfs):
    os.chdir(ruta_pdfs)
    contador = 0
    for archivo in os.listdir('.'):
        if archivo.endswith('.pdf'):
            try:
                reader = PdfReader(archivo)
                texto = ''
                for pagina in reader.pages:
                    texto += pagina.extract_text()

                nombre = encontrar_nombre_en_texto(texto)
                if nombre:
                    # Crear una carpeta para el nombre si no existe
                    carpeta_nombre = os.path.join(ruta_salida, nombre)
                    if not os.path.exists(carpeta_nombre):
                        os.mkdir(carpeta_nombre)
                    # Mover y renombrar el PDF
                    expresion_regular_numero_diploma = r"No\.\s+(C-\d+)"
                    numero_diploma = extraer_nombre(texto, expresion_regular_numero_diploma)
                    # Construir el nombre del archivo de destino condicionalmente, dependiendo de si numero_diploma es None
                    if numero_diploma:
                        nombre_archivo = f"{nombre} {numero_diploma}.pdf"
                    else:
                        nombre_archivo = f"{nombre}.pdf"
                    destino_pdf = os.path.join(carpeta_nombre, nombre_archivo)

                    # Si por algun error en los patrones el archivo ya existe entonces se guarda el siguiente archivo solo con el nombre el estudiante y algun contador
                    if os.path.exists(destino_pdf):
                        nombre_archivo = f"{nombre}_{contador}.pdf"
                        destino_pdf = os.path.join(carpeta_nombre, nombre_archivo)
                    shutil.move(archivo, destino_pdf)
                    print(f"Archivo {archivo} procesado y movido a {destino_pdf}.")
                    contador += 1  #
            except Exception as e:
                print(f"Error procesando archivo {archivo}: {e}")


# Reemplaza 'ruta/a/tus/pdfs' con la ruta real a tus archivos PDF
ruta_pdfs = 'W:/automation/DocsFacultad/Entradas'
ruta_salida = 'W:/automation/DocsFacultad/Procesados_dos'
procesar_pdfs(ruta_pdfs, DIPLOMA_PRE)
