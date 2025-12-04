import datetime
import functools
import logging
import logging.handlers
import os
import sys
import threading
import time

from colorama import Fore, Style, init

# Inicializar colorama
init(autoreset=True)

# Configuración de Logging
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "audit.log")

if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Configurar logger
logger = logging.getLogger("ProyectoKIT")
logger.setLevel(logging.INFO)

# Handler para archivo con rotación (max 1MB, guarda 5 archivos previos)
file_handler = logging.handlers.RotatingFileHandler(
    LOG_FILE, maxBytes=1024 * 1024, backupCount=5, encoding="utf-8"
)
file_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def print_success(message):
    print(f"{Fore.GREEN}[✔] {message}")
    logger.info(f"Éxito: {message}")


def print_error(message):
    print(f"{Fore.RED}[✘] {message}")
    logger.error(f"Error: {message}")


def print_warning(message):
    print(f"{Fore.YELLOW}[!] {message}")
    logger.warning(f"Advertencia: {message}")


def print_info(message):
    print(f"{Fore.CYAN}[i] {message}")
    logger.info(f"Info: {message}")


def print_header(message):
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}{'='*40}")
    print(f" {message.center(38)}")
    print(f"{'='*40}")
    logger.info(f"--- Sección: {message} ---")


class Spinner:
    """
    Clase para mostrar una animación de carga en la consola.
    Uso:
    with Spinner("Procesando..."):
        # tarea larga
    """

    def __init__(self, message="Cargando...", delay=0.1):
        self.spinner = ["|", "/", "-", "\\"]
        self.delay = delay
        self.message = message
        self.running = False
        self.thread = None

    def spin(self):
        while self.running:
            for char in self.spinner:
                sys.stdout.write(f"\r{Fore.CYAN}{char} {self.message}")
                sys.stdout.flush()
                time.sleep(self.delay)
                if not self.running:
                    break

    def __enter__(self):
        self.running = True
        self.thread = threading.Thread(target=self.spin)
        self.thread.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.running = False
        self.thread.join()
        sys.stdout.write(f'\r{" " * (len(self.message) + 2)}\r')  # Limpiar línea
        sys.stdout.flush()


def log_execution(func):
    """
    Decorador para registrar la ejecución de funciones, sus argumentos y si hubo errores.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            logger.info(
                f"Ejecutando '{func.__name__}' con args: {args}, kwargs: {kwargs}"
            )
            result = func(*args, **kwargs)
            logger.info(f"Finalizado '{func.__name__}' exitosamente.")
            return result
        except Exception as e:
            logger.error(f"Fallo en '{func.__name__}': {str(e)}", exc_info=True)
            raise e

    return wrapper


def ensure_directories():
    """Asegura que existan los directorios necesarios."""
    for folder in ["logs", "reports", "snapshots", "tests_sample"]:
        if not os.path.exists(folder):
            os.makedirs(folder)


def clear_screen():
    """Limpia la pantalla de la consola."""
    os.system("cls" if os.name == "nt" else "clear")


def get_valid_input(prompt, options=None):
    """
    Solicita entrada al usuario y valida contra una lista de opciones si se provee.
    """
    while True:
        user_input = input(f"{Fore.BLUE}{prompt}").strip()
        if options:
            if user_input in options:
                return user_input
            print_error(
                f"Opción inválida. Por favor elija una de: {', '.join(options)}"
            )
        else:
            if user_input:
                return user_input
            print_error("La entrada no puede estar vacía.")
