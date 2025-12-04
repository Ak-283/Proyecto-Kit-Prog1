import csv
import datetime
import os

from src.utils import log_execution, print_error, print_success

REPORT_DIR = "reports"


@log_execution
def generate_txt_report(title, data, filename="report.txt"):
    """Genera un reporte en formato TXT."""
    filepath = os.path.join(REPORT_DIR, filename)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"REPORTE: {title}\n")
        f.write(f"FECHA: {timestamp}\n")
        f.write("=" * 40 + "\n\n")

        if isinstance(data, dict):
            for key, value in data.items():
                f.write(f"{key}:\n")
                if isinstance(value, list):
                    for item in value:
                        f.write(f"  - {item}\n")
                else:
                    f.write(f"  {value}\n")
                f.write("\n")
        elif isinstance(data, list):
            for item in data:
                f.write(f"- {item}\n")
        else:
            f.write(str(data))

    print_success(f"Reporte TXT generado en: {filepath}")


@log_execution
def generate_csv_report(data_list, headers, filename="report.csv"):
    """Genera un reporte en formato CSV."""
    filepath = os.path.join(REPORT_DIR, filename)

    try:
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(data_list)
        print_success(f"Reporte CSV generado en: {filepath}")
    except Exception as e:
        print_error(f"Error generando CSV: {e}")