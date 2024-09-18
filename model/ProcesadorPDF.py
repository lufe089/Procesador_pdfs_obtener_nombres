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
        # Devolvemos el nombre ya normalizado
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

    def procesar(self):
        """
        Método para procesar los PDFs: cambiar directorio, buscar nombres y mover archivos
        :return: None
        """
        try:
            os.chdir(self.configuracion.ruta_pdfs)
            encontro_nombre = False
            for archivo in os.listdir('.'):
                if archivo.endswith('.pdf'):

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
            msj = f"ERROR - NO se movio el archivo {archivo}, hubo algun error identificando automaticamente el nombre"
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
