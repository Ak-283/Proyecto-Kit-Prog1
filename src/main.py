import os
import sys

# Agregar el directorio raíz al path para poder importar módulos
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import analyzer, auditor, organizer, reporter
from src.utils import (
    Spinner,
    clear_screen,
    ensure_directories,
    get_valid_input,
    print_error,
    print_header,
    print_info,
    print_success,
)


def print_menu():
    print_header("KIT MULTIFUNCIONAL DE AUTOMATIZACIÓN")
    print("1. Gestor de Organización de Archivos")
    print("2. Analizador de Contenido")
    print("3. Auditor de Cambios")
    print("4. Generar Reportes")
    print("5. Salir")
    print("=" * 40)


def menu_organizer():
    clear_screen()
    print_header("GESTOR DE ORGANIZACIÓN")
    print("1. Organizar por Extensión")
    print("2. Organizar por Tamaño")
    print("3. Renombrar por Patrón (Regex)")
    print("4. Volver")

    opcion = get_valid_input("Seleccione una opción: ", ["1", "2", "3", "4"])
    if opcion == "4":
        return

    directory = get_valid_input("Ingrese la ruta del directorio a organizar: ")

    if not os.path.isdir(directory):
        print_error("Directorio no válido.")
        return

    dry_run_input = get_valid_input("¿Modo simulación (dry-run)? (s/n): ", ["s", "n"])
    dry_run = dry_run_input == "s"

    if opcion == "3":
        pattern = get_valid_input("Ingrese el patrón Regex a buscar: ")
        replacement = get_valid_input("Ingrese el reemplazo: ")

    with Spinner("Procesando..."):
        if opcion == "1":
            organizer.organize_by_extension(directory, dry_run)
        elif opcion == "2":
            organizer.organize_by_size(directory, dry_run)
        elif opcion == "3":
            organizer.rename_by_pattern(directory, pattern, replacement, dry_run)


def menu_analyzer():
    clear_screen()
    print_header("ANALIZADOR DE CONTENIDO")
    print("1. Buscar patrón en archivos")
    print("2. Contar palabras en archivo")
    print("3. Volver")

    opcion = get_valid_input("Seleccione una opción: ", ["1", "2", "3"])

    if opcion == "1":
        directory = get_valid_input("Ingrese el directorio a analizar: ")
        if not os.path.isdir(directory):
            print_error("Directorio no válido.")
            return
        pattern = get_valid_input("Ingrese el patrón Regex (ej: email, fecha): ")

        with Spinner("Analizando archivos..."):
            results = analyzer.analyze_content(directory, pattern)

        if results:
            print_success(f"Se encontraron coincidencias en {len(results)} archivos.")
            save = get_valid_input("¿Guardar reporte? (s/n): ", ["s", "n"])
            if save == "s":
                reporter.generate_txt_report(
                    f"Búsqueda de '{pattern}'", results, "analisis_contenido.txt"
                )
        else:
            print_info("No se encontraron coincidencias.")

    elif opcion == "2":
        filepath = get_valid_input("Ingrese la ruta del archivo: ")
        if not os.path.isfile(filepath):
            print_error("Archivo no válido.")
            return

        with Spinner("Contando palabras..."):
            count = analyzer.count_words(filepath)
        print_success(f"El archivo tiene {count} palabras.")


def menu_auditor():
    clear_screen()
    print_header("AUDITOR DE CAMBIOS")
    print("1. Tomar Snapshot (Estado actual)")
    print("2. Comparar con último Snapshot")
    print("3. Volver")

    opcion = get_valid_input("Seleccione una opción: ", ["1", "2", "3"])
    if opcion == "3":
        return

    directory = get_valid_input("Ingrese el directorio a auditar: ")

    if not os.path.isdir(directory):
        print_error("Directorio no válido.")
        return

    if opcion == "1":
        with Spinner("Tomando snapshot..."):
            auditor.take_snapshot(directory)
    elif opcion == "2":
        with Spinner("Comparando snapshots..."):
            diff = auditor.compare_snapshot(directory)

        if diff:
            print("\nCambios detectados:")
            print_info(f"Agregados: {len(diff['added'])}")
            print_info(f"Eliminados: {len(diff['removed'])}")
            print_info(f"Modificados: {len(diff['modified'])}")

            save = get_valid_input("¿Guardar reporte de auditoría? (s/n): ", ["s", "n"])
            if save == "s":
                reporter.generate_txt_report(
                    "Auditoría de Cambios", diff, "auditoria.txt"
                )


def main():
    ensure_directories()
    while True:
        clear_screen()
        print_menu()
        opcion = get_valid_input("Seleccione una opción: ", ["1", "2", "3", "4", "5"])

        if opcion == "1":
            menu_organizer()
            input("\nPresione Enter para continuar...")
        elif opcion == "2":
            menu_analyzer()
            input("\nPresione Enter para continuar...")
        elif opcion == "3":
            menu_auditor()
            input("\nPresione Enter para continuar...")
        elif opcion == "4":
            print_info("Los reportes se generan automáticamente en las otras opciones.")
            input("\nPresione Enter para continuar...")
        elif opcion == "5":
            print_success("Saliendo del sistema...")
            break


if __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
