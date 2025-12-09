import json
import os

from src.utils import log_execution, print_success, print_warning

SNAPSHOT_FILE = os.path.join("snapshots", "snapshot.json")


@log_execution
def take_snapshot(directory):
    """
    Crea un snapshot del estado actual del directorio (archivos y fecha de modificación).
    """
    snapshot = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(filepath)
                snapshot[filepath] = mtime
            except OSError:
                continue

    with open(SNAPSHOT_FILE, "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=4)

    print_success(f"Snapshot guardado en {SNAPSHOT_FILE}")
    return snapshot


@log_execution
def compare_snapshot(directory):
    """
    Compara el estado actual con el último snapshot guardado.
    """
    if not os.path.exists(SNAPSHOT_FILE):
        print_warning("No existe un snapshot previo. Ejecute 'Tomar Snapshot' primero.")
        return None

    with open(SNAPSHOT_FILE, "r", encoding="utf-8") as f:
        old_snapshot = json.load(f)

    current_snapshot = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            try:
                mtime = os.path.getmtime(filepath)
                current_snapshot[filepath] = mtime
            except OSError:
                continue

    added = [f for f in current_snapshot if f not in old_snapshot]
    removed = [f for f in old_snapshot if f not in current_snapshot]
    modified = []

    for f in current_snapshot:
        if f in old_snapshot:
            if current_snapshot[f] != old_snapshot[f]:
                modified.append(f)

    return {"added": added, "removed": removed, "modified": modified}
