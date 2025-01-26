"""
Turbo Hash Breaker 1.0

Turbo Hash Breaker is a complete password recovery tool for multiple hash types. It uses a wordlist full of passwords and then tries to crack a given hash with each of the passwords in the wordlist. In the first version, it supports the following hash types:
    
        MD5
        SHA1
        SHA256
        SHA3
        BLAKE2

The program is written in Python and uses the hashlib library to generate the hashes. The program is divided into two files: main.py and hasher.py. The main.py file contains the main program, while the hasher.py file contains the Hasher class, which is responsible for generating the hashes.

It use threads and the powerfull of parallelism to speed up the process of cracking the hashes.
"""

import argparse
import sys
from hasher import Hasher
import os
import time
from multiprocessing import Process

start_time = time.perf_counter()

def commonHashBreaker(hash_value, hash_type, dictionary_path):
    #valiate if the hash type is supported

    if hash_type not in ["md5", "sha1", "sha256", "sha3", "blake2"]:
        print("Error: Tipo de hash no soportado.")
        sys.exit(1)

    # Leer el diccionario uno por uno y comparar con el hash
    with open(dictionary_path, "r") as archivo:
        for password in archivo:
            #clean console
            sys.stdout.write("\033[H\033[J")  # Mueve el cursor al inicio y limpia la pantalla
            sys.stdout.flush()
            print(f"Hash destino: {hash_value}")
            print(f"Probando contraseña: {password}", end="\r")
            print(f"Tipo de hash: {hash_type}")
            print(f"diccionario: {dictionary_path}")

            password = password.strip()
            hasher = Hasher(password)

            # Calcular el hash
            if hash_type == "md5":
                current_hash = hasher.hash_md5()
            elif hash_type == "sha1":
                current_hash = hasher.hash_sha1()
            elif hash_type == "sha256":
                current_hash = hasher.hash_sha256()
            elif hash_type == "sha3":
                current_hash = hasher.hash_sha3()
            elif hash_type == "blake2":
                current_hash = hasher.hash_blake2()

            # Comparar el hash
            if current_hash == hash_value:
                print(f"Contraseña encontrada: {password}")
                end_time = time.perf_counter()
                print(f"Tiempo de ejecución: {end_time - start_time} segundos")
                sys.exit(0)

def process_chunk(hash_value, hash_type, chunk):
    for password in chunk:
        password = password.strip()
        hasher = Hasher(password)

        # Calcular el hash
        if hash_type == "md5":
            current_hash = hasher.hash_md5()
        elif hash_type == "sha1":
            current_hash = hasher.hash_sha1()
        elif hash_type == "sha256":
            current_hash = hasher.hash_sha256()
        elif hash_type == "sha3":
            current_hash = hasher.hash_sha3()
        elif hash_type == "blake2":
            current_hash = hasher.hash_blake2()

        # Comparar el hash
        if current_hash == hash_value:
            print(f"Contraseña encontrada: {password}")
            end_time = time.perf_counter()
            print(f"Tiempo de ejecución: {end_time - start_time} segundos")
            os._exit(0)

def turboHashBreaker(hash_value, hash_type, dictionary_path):
    cpus = os.cpu_count()
    print(f"Number of CPU's: {cpus}")

    if hash_type not in ["md5", "sha1", "sha256", "sha3", "blake2"]:
        print("Error: Tipo de hash no soportado.")
        sys.exit(1)

    with open(dictionary_path, "r") as archivo:
        passwords = archivo.readlines()

    # Dividir el diccionario en chunks según el número de CPUs
    chunk_size = len(passwords) // cpus
    chunks = [passwords[i:i + chunk_size] for i in range(0, len(passwords), chunk_size)]

    processes = []

    for chunk in chunks:
        p = Process(target=process_chunk, args=(hash_value, hash_type, chunk))
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

def main():
    # Crear un parser
    parser = argparse.ArgumentParser(description="Recoge y valida los argumentos.")

    # Agregar los argumentos
    parser.add_argument('-p', '--hash', type=str, help="Hash a procesar")
    parser.add_argument('-t', '--hash_type', type=str, required=True, help="Tipo de hash")
    parser.add_argument('-d', '--dictionary_path', type=str, required=True, help="Ruta al diccionario")

    # Parsear los argumentos
    args = parser.parse_args()

    # Si no se pasa el hash, se imprime el mensaje de ayuda
    if args.hash is None:
        print("Este programa requiere los siguientes argumentos:")
        print("-p o --hash para especificar el hash.")
        print("-t o --hash_type para especificar el tipo de hash.")
        print("-d o --dictionary_path para especificar la ruta al diccionario.")
        sys.exit(0)

    # Validar que todos los argumentos estén presentes
    if not args.hash or not args.hash_type or not args.dictionary_path:
        print("Error: Todos los argumentos son obligatorios (-p, -t, -d).")
        sys.exit(1)

    # Asignar los valores a las variables
    hash_value = args.hash
    hash_type = args.hash_type
    dictionary_path = args.dictionary_path

    # Imprimir los valores
    print(f"Hash: {hash_value}")
    print(f"Tipo de hash: {hash_type}")
    print(f"Ruta al diccionario: {dictionary_path}")
    turboHashBreaker(hash_value, hash_type, dictionary_path)

if __name__ == "__main__":
    main()
