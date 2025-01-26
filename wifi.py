import argparse
import subprocess
import sys
import os
import time
from multiprocessing import Process, Manager

start_time = time.perf_counter()

def run_aircrack(bssid, cap_file, dictionary_chunk, found_flag):
    """Ejecuta aircrack-ng en un fragmento del diccionario."""
    try:
        # Construir el comando para un fragmento del diccionario
        command = ["aircrack-ng", "-b", bssid, "-w", dictionary_chunk, cap_file]

        print(f"Ejecutando aircrack-ng con el fragmento: {dictionary_chunk}")

        # Ejecutar el comando y capturar la salida
        process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Mostrar el resultado del comando
        if process.returncode == 0 and "KEY FOUND" in process.stdout:
            print("\nResultado de aircrack-ng:")
            print(process.stdout)
            found_flag[0] = True  # Señalar que la clave fue encontrada
            sys.exit(0)  # Detener el proceso actual
        else:
            print(f"\nError o clave no encontrada en el fragmento: {dictionary_chunk}")

    except FileNotFoundError:
        print("Error: El comando 'aircrack-ng' no está instalado o no está en el PATH.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}", file=sys.stderr)
        sys.exit(1)

def split_dictionary(dictionary_path, num_chunks):
    """Divide el diccionario en archivos temporales según el número de CPUs disponibles."""
    with open(dictionary_path, "r") as file:
        lines = file.readlines()

    chunk_size = len(lines) // num_chunks
    chunks = []

    for i in range(num_chunks):
        chunk_lines = lines[i * chunk_size: (i + 1) * chunk_size]
        chunk_file = f"dictionary_chunk_{i}.txt"
        with open(chunk_file, "w") as chunk:
            chunk.writelines(chunk_lines)
        chunks.append(chunk_file)

    # Agregar cualquier línea restante al último chunk
    if len(lines) % num_chunks != 0:
        with open(chunks[-1], "a") as chunk:
            chunk.writelines(lines[num_chunks * chunk_size:])

    return chunks

def main():
    # Configurar los argumentos
    parser = argparse.ArgumentParser(description="Script para ejecutar aircrack-ng con los datos proporcionados.")
    parser.add_argument("-b", "--bssid", required=True, help="Dirección BSSID (MAC) del punto de acceso.")
    parser.add_argument("-f", "--file", required=True, help="Archivo de captura (.cap) a procesar.")
    parser.add_argument("-d", "--dictionary", required=True, help="Archivo de diccionario para ataques de fuerza bruta.")

    args = parser.parse_args()

    # Asignar argumentos a variables
    bssid = args.bssid
    cap_file = args.file
    dictionary = args.dictionary

    # Número de CPUs disponibles
    cpus = os.cpu_count()
    print(f"Número de CPUs disponibles: {cpus}")

    # Dividir el diccionario
    dictionary_chunks = split_dictionary(dictionary, cpus)

    # Mecanismo para compartir estado entre procesos
    with Manager() as manager:
        found_flag = manager.list([False])  # Lista compartida para señalizar cuando se encuentra la clave

        # Crear procesos para cada fragmento del diccionario
        processes = []
        for chunk in dictionary_chunks:
            p = Process(target=run_aircrack, args=(bssid, cap_file, chunk, found_flag))
            p.start()
            processes.append(p)

        # Monitorear procesos
        while not found_flag[0]:
            for p in processes:
                if not p.is_alive():
                    processes.remove(p)

        # Terminar procesos restantes
        for p in processes:
            p.terminate()

        # Eliminar archivos temporales
        for chunk in dictionary_chunks:
            os.remove(chunk)
        
        end_time = time.perf_counter()
        print(f"Tiempo de ejecución: {end_time - start_time} segundos")

if __name__ == "__main__":
    main()
