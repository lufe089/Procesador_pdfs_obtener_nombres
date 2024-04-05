from model.AnalizadorReporte import AnalizadorReporte
from model.Configuracion import Configuracion
from model.ProcesadorPDF import ProcesadorPDF


class Vista:
    def __init__(self, path, log_path):
        # Inicializa la vista con la configuración y el procesador PDF
        self.configuracion = Configuracion(path)
        self.procesador = ProcesadorPDF(self.configuracion, log_path)

    def mostrar_menu(self):
        opcion = None  # Inicializa la variable opción para entrar al ciclo
        while opcion != '0':  # Continúa mientras la opción sea diferente de '0'
            print(
                "\nBienvenido P R O C E S A D O R   D O C S   G R A D O S. \nProyecto elaborado por: Luisa Rincon <lfrincon@javerianacali.edu.co> Facultad de Ingeniería y Ciencias \n Abril 2024")
            opcion = input(
                "Seleccione:\n"
                "1 - Iniciar el procesamiento de documentos.\n"
                "2 - Comprimir los directorios de salida.\n"
                "0 para salir.\n"
                "Opción: ")

            if opcion == '1':
                try:
                    print("Procesando archivos ....")
                    self.procesador.procesar()
                    print("Elaborando reporte de movimiento ....")
                    reporte = AnalizadorReporte(self.configuracion)
                    reporte.crear_reporte()
                    print(
                        f":) Procesamiento completado.... para archivos disponibles en {self.configuracion.ruta_pdfs}. Puede consultar los resultados en {self.configuracion.ruta_salida} y en el archivo de log ")
                    print(
                        "\n\nRecuerde revisar:\n1.La carpeta de entrada para nombrar manualmente los archivos que no se pudieron procesar automaticamente. \n2. Los nombres de las carpetas antes de hacer la compresión, algunas veces un mismo estudiante puede tener más de una carpeta debido a la estructura del nombre en los archivos")
                except Exception:
                    print(
                        "Ha ocurrido un error durante el procesamiento. Por favor, consulte el log para más detalles.")
            elif opcion == '2':
                try:
                    self.procesador.comprimir_directorios()
                    print("Compresión de directorios completada exitosamente.")
                except Exception:
                    print(
                        "Ha ocurrido un error durante la compresión de los directorios. Por favor, consulte el log para más detalles.")
            elif opcion == '0':
                # Opción para salir del programa
                print("Saliendo del programa...")
            else:
                print("Opción no válida. Intente de nuevo.")
