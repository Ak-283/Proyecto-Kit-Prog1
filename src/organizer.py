import datetime
import os
import re
import shutil

from src.utils import (
    log_execution,
    print_error,
    print_info,
    print_success,
    print_warning,
)


@log_execution
def organize_by_extension(directory, dry_run=False):
    """Organiza archivos en carpetas según su extensión."""
    actions = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            ext = filename.split(".")[-1] if "." in filename else "no_ext"
            target_folder = os.path.join(directory, ext)

            if os.path.exists(target_folder) and not os.path.isdir(target_folder):
                print_error(
                    f"No se puede usar la carpeta '{ext}' porque existe un archivo con ese nombre. Saltando {filename}."
                )
                continue

            target_path = os.path.join(target_folder, filename)

            actions.append((filepath, target_path, target_folder))

    if dry_run:
        print_warning("\n[MODO SIMULACIÓN] Se realizarían los siguientes cambios:")
        for src, dst, folder in actions:
            print_info(f"Mover: {src} -> {dst}")
    else:
        print_info("\nRealizando cambios:")
        for src, dst, folder in actions:
            if not os.path.exists(folder):
                os.makedirs(folder)

            if os.path.exists(dst):
                base, ext = os.path.splitext(dst)
                counter = 1
                while os.path.exists(dst):
                    dst = f"{base}_{counter}{ext}"
                    counter += 1
                print_warning(
                    f"El archivo destino ya existe. Se moverá a: {os.path.basename(dst)}"
                )

            shutil.move(src, dst)
            print_info(f"Movido: {src} -> {dst}")
        print_success(f"Se organizaron {len(actions)} archivos por extensión.")
    return actions


@log_execution
def organize_by_size(directory, dry_run=False):
    """Organiza archivos en carpetas: Pequeño (<1MB), Mediano (1-10MB), Grande (>10MB)."""
    actions = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            if size_mb < 1:
                folder_name = "Pequeno"
            elif size_mb < 10:
                folder_name = "Mediano"
            else:
                folder_name = "Grande"

            target_folder = os.path.join(directory, folder_name)

            if os.path.exists(target_folder) and not os.path.isdir(target_folder):
                print_error(
                    f"No se puede usar la carpeta '{folder_name}' porque existe un archivo con ese nombre. Saltando {filename}."
                )
                continue

            target_path = os.path.join(target_folder, filename)
            actions.append((filepath, target_path, target_folder))

    if dry_run:
        print_warning("\n[MODO SIMULACIÓN] Se realizarían los siguientes cambios:")
        for src, dst, folder in actions:
            print_info(f"Mover: {src} -> {dst}")
    else:
        print_info("\nRealizando cambios:")
        for src, dst, folder in actions:
            if not os.path.exists(folder):
                os.makedirs(folder)

            if os.path.exists(dst):
                base, ext = os.path.splitext(dst)
                counter = 1
                while os.path.exists(dst):
                    dst = f"{base}_{counter}{ext}"
                    counter += 1
                print_warning(
                    f"El archivo destino ya existe. Se moverá a: {os.path.basename(dst)}"
                )

            shutil.move(src, dst)
            print_info(f"Movido: {src} -> {dst}")
        print_success(f"Se organizaron {len(actions)} archivos por tamaño.")
    return actions


@log_execution
def rename_by_pattern(directory, pattern, replacement, dry_run=False):
    """Renombra archivos que coincidan con un patrón regex."""
    actions = []
    try:
        regex = re.compile(pattern)
    except re.error as e:
        print_error(f"Error en la expresión regular: {e}")
        return []

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            if regex.search(filename):
                new_filename = regex.sub(replacement, filename)
                new_filepath = os.path.join(directory, new_filename)
                if filename != new_filename:
                    actions.append((filepath, new_filepath))

    if dry_run:
        print_warning("\n[MODO SIMULACIÓN] Se realizarían los siguientes cambios:")
        for src, dst in actions:
            print_info(f"Renombrar: {src} -> {dst}")
    else:
        print_info("\nRealizando cambios:")
        for src, dst in actions:
            if os.path.exists(dst):
                base, ext = os.path.splitext(dst)
                counter = 1
                while os.path.exists(dst):
                    dst = f"{base}_{counter}{ext}"
                    counter += 1
                print_warning(
                    f"El archivo destino ya existe. Se renombrará a: {os.path.basename(dst)}"
                )

            try:
                os.rename(src, dst)
                print_info(f"Renombrado: {src} -> {dst}")
            except OSError as e:
                print_error(f"No se pudo renombrar {src} a {dst}: {e}")
        print_success(f"Se procesaron {len(actions)} archivos.")
    return actions
