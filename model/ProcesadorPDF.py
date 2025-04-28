import logging
import os
import re
import shutil
import zipfile

import unicodedata
from PyPDF2 import PdfReader


class ProcesadorPDF:

    def __init__(self, configuracion, log_path):
        self.configuracion = configuracion
        # Configura el logging para capturar información y errores.
        destino_log = os.path.join(log_path, 'rocesador_documentos.log')
        logging.basicConfig(filename=destino_log, level=logging.INFO,
                            format='%(asctime)s:%(levelname)s:%(message)s')

    def normalizar_nombre(self, nombre):
        """
         Método para normalizar los nombres, quitando espacios y tildes
        :param nombre:
        :return:  nombre normalizado
        """
        # Primero, quitamos espacios al principio y al final de la cadena original
        nombre = nombre.strip()
        nombre = self.limpiar_texto_extraido(nombre)
        # Normalizamos el nombre a su forma NFD. Esto separará los caracteres
        # de sus marcas diacríticas (como las tildes). Por ejemplo, "Á" se descompone en "A" y la tilde como entidades separadas.
        nombre_sin_tildes = ''.join(
            # Iteramos sobre cada carácter de la cadena normalizada
            c for c in unicodedata.normalize('NFD', nombre)
            # Filtramos aquellos caracteres que no son marcas diacríticas (Mn).
            # 'Mn' significa 'Mark, Nonspacing', que son caracteres que se combinan con el anterior sin ocupar espacio adicional.
            # Al omitir estos caracteres, efectivamente quitamos las tildes y otras marcas diacríticas del nombre.
            if unicodedata.category(c) != 'Mn'
        )

        # Ahora que hemos eliminado las tildes, reemplazamos los espacios en blanco por guiones bajos
        # para normalizar aún más el nombre, haciéndolo más adecuado, por ejemplo, para nombres de archivos.
        nombre_normalizado = nombre_sin_tildes.replace(' ', '_')
        return nombre_normalizado

    def extraer_nombre(self, texto, expresion_regular):
        """
        Método para extraer nombres basados en una expresión regular que se recibe por parametros
        :param texto:
        :param expresion_regular:
        :return:
        """
        try:
            patron = re.compile(expresion_regular)
            busqueda = patron.search(texto)
            if busqueda:
                return busqueda.group(1)
            return None
        except Exception as e:
            # Registra el error con la traza completa
            logging.error("Error al extraer el nombre: ", exc_info=True)
            raise e

    def limpiar_texto_extraido(self, texto):
        # 1. Eliminar dobles espacios o más
        texto = re.sub(r'\s{2,}', ' ', texto)

        # 2. Reemplazar patrones de palabras cortadas erróneamente (espacio dentro de una palabra de mayúsculas)
        texto = re.sub(r'(?<=[A-ZÁÉÍÓÚÑ])\s+(?=[A-ZÁÉÍÓÚÑ])', '', texto)

        # 3. Separar campos unidos sin espacio entre letras y puntos o números
        texto = re.sub(r'([a-zA-ZÁÉÍÓÚÑ])(\d)', r'\1 \2', texto)  # Ej: "C.C.1.23..." → "C.C. 1.23..."
        texto = re.sub(r'(\d)([A-ZÁÉÍÓÚÑ])', r'\1 \2', texto)  # Ej: "123CALI" → "123 CALI"

        return texto.strip()

    def descomprimir_mover(self):
        # Descomprimir carpetas comprimidas
        for archivo in os.listdir('.'):
            if archivo.endswith('.zip'):
                with zipfile.ZipFile(archivo, 'r') as zip_ref:
                    zip_ref.extractall('.')
                os.remove(archivo)  # Elimina el archivo ZIP después de descomprimir

        # Mover todos los archivos a la raíz
        for raiz, _, archivos in os.walk('.'):
            for archivo in archivos:
                ruta_actual = os.path.join(raiz, archivo)
                if os.path.abspath(raiz) != os.path.abspath('.'):
                    shutil.move(ruta_actual, '.')  # Mueve el archivo a la raíz

        # Elimina los directorios cuando quedan vacíos
        for raiz, directorios, _ in os.walk('.'):
            for directorio in directorios:
                ruta_directorio = os.path.join(raiz, directorio)
                if os.path.abspath(ruta_directorio) != os.path.abspath('.'):
                    try:
                        os.rmdir(ruta_directorio)  # Elimina el directorio si está vacío
                    except OSError:
                        pass # No es necesario controlar ese caso



    def procesar(self):
        """
        Método para procesar los PDFs: cambiar directorio, buscar nombres y mover archivos
        :return: None
        """
        try:
            os.chdir(self.configuracion.ruta_pdfs)
            encontro_nombre = False
            # Descomprime y mueve archivos a la raíz y elimina los directorios vacíos
            self.descomprimir_mover()

            for archivo in os.listdir('.'):
                # El archivo no es un directorio y termina en .pdf
                path = os.path.abspath(archivo)
                if archivo.endswith('.pdf') and os.path.isfile(path):
                    reader = PdfReader(archivo)
                    texto = ''
                    for pagina in reader.pages:
                        texto += pagina.extract_text()

                    encontro_nombre = False
                    for parametro in self.configuracion.parametros:
                        if parametro is not None and parametro['expresion_regular'] is not None:
                            nombre = self.extraer_nombre(texto, parametro['expresion_regular'])
                            if nombre:
                                nombre = self.normalizar_nombre(nombre)
                                # El texto de verificacion es el que verifica que en el titulo si quede el nombre que esperamos
                                if texto.__contains__(parametro['texto_verificacion']):
                                    self.mover_archivo(archivo, nombre, parametro['prefijo'])
                                    encontro_nombre = True
                                    break
                    if not encontro_nombre:
                        msj = f"ERROR: NO encontró NOMBRE: Archivo {archivo}"
                        logging.error(msj)
                        print(msj)
        except Exception as e:
            logging.error("Error al procesar PDF: ", exc_info=True)
            raise e

    def mover_archivo(self, archivo, nombre, prefijo):
        """
        Método para mover archivos: crea directorios si no existen, gestiona nombres de archivos y maneja colisiones de nombres
        :param archivo:
        :param nombre:
        :param prefijo: para el nombramiento de archivos
        :return:
        """
        carpeta_nombre = os.path.join(self.configuracion.ruta_salida, nombre)
        # Si no existe el directorio de salida lo crea
        if not os.path.exists(self.configuracion.ruta_salida):
            os.mkdir(self.configuracion.ruta_salida)

        if not os.path.exists(carpeta_nombre):
            os.mkdir(carpeta_nombre)

        nombre_archivo = f"{prefijo}-{nombre}.pdf" if prefijo else f"{nombre}.pdf"
        destino_pdf = os.path.join(carpeta_nombre, nombre_archivo)

        if not os.path.exists(destino_pdf):
            # Si ya existe el pdf no se hace el movimiento porque significa que hubo algun problema con algun patron
            shutil.move(archivo, destino_pdf)
            print(f"Archivo {archivo} procesado y movido a {destino_pdf}.")
            # Registra la acción de mover el archivo como información
            logging.info(f"Archivo {archivo} procesado y movido a {destino_pdf}.")
        else:
            msj = f"ERROR - NO se movio el archivo {archivo}, ya existe en el directorio de salida o no hubo un problema identificando automaticamente el nombre"
            logging.error(msj)
            print(msj)

    def comprimir_directorios(self):
        """
        Método para comprimir directorios: navega por los directorios y los comprime en archivos zip
        :return:
        """
        os.chdir(self.configuracion.ruta_salida)
        for directorio in os.listdir('.'):
            if os.path.isdir(directorio):
                nombre_zip = f"{directorio}.zip"
                with zipfile.ZipFile(nombre_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for raiz, _, archivos in os.walk(directorio):
                        for archivo in archivos:
                            zipf.write(os.path.join(raiz, archivo),
                                       os.path.relpath(os.path.join(raiz, archivo), os.path.join(directorio, '..')))
                logging.info(f"Directorio {directorio} comprimido a {nombre_zip}.")
                print(f"Directorio {directorio} comprimido a {nombre_zip}.")
