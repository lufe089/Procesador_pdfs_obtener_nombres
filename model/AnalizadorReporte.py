# Continuación del código en ReporteDirectorio.py

import os

from openpyxl import Workbook


class AnalizadorReporte:
    def __init__(self, configuracion):
        self.configuracion = configuracion
        self.ruta_salida = configuracion.ruta_salida
        self.ruta_pdfs = configuracion.ruta_pdfs

    def crear_reporte(self):
        # Crear un nuevo workbook y hojas
        wb = Workbook()
        ws_salidas = wb.active
        ws_salidas.title = "Salidas"

        # Contar archivos en directorio de salida
        self._contar_archivos_directorio(self.ruta_salida, ws_salidas)

        # Guardar el workbook en la ruta de salida
        archivo_excel = os.path.join(self.ruta_salida, 'informe_renombramiento.xlsx')
        wb.save(archivo_excel)
        print(f"Resumen guardado en {archivo_excel}")

    def _contar_archivos_directorio(self, ruta_directorio, ws):
        # Agregar encabezados a la hoja
        ws.append(['Nombre Carpeta/Subdirectorio', 'Cantidad Archivos'])

        # Recorrer los directorios y contar archivos
        for elemento in os.listdir(ruta_directorio):
            ruta_completa = os.path.join(ruta_directorio, elemento)
            if os.path.isdir(ruta_completa):
                archivos = [archivo for archivo in os.listdir(ruta_completa) if
                            os.path.isfile(os.path.join(ruta_completa, archivo))]
                conteo = len(archivos)
                ws.append([elemento, conteo])  # Agregar a la hoja de Excel
            elif os.path.isfile(ruta_completa):  # Para el caso de archivos en la carpeta de entrada
                ws.append([ruta_directorio, 1])
