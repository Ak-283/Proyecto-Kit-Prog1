import os
import re

from src.utils import log_execution, print_error


def read_large_file(file_path):
    """Generador para leer archivos grandes línea por línea."""
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            yield line


@log_execution
def search_pattern_in_file(file_path, pattern):
    """Busca un patrón regex en un archivo y devuelve las líneas coincidentes."""
    matches = []
    try:
        regex = re.compile(pattern)
        line_num = 0
        for line in read_large_file(file_path):
            line_num += 1
            if regex.search(line):
                matches.append((line_num, line.strip()))
    except re.error as e:
        print_error(f"Error en regex: {e}")
    return matches


@log_execution
def analyze_content(directory, pattern):
    """Analiza todos los archivos de texto en un directorio buscando un patrón."""
    results = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt") or file.endswith(".log") or file.endswith(".csv"):
                filepath = os.path.join(root, file)
                matches = search_pattern_in_file(filepath, pattern)
                if matches:
                    results[filepath] = matches
    return results


@log_execution
def count_words(file_path):
    """Cuenta palabras en un archivo usando un generador."""
    count = 0
    for line in read_large_file(file_path):
        count += len(line.split())
    return count
