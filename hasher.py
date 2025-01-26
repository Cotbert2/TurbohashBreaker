import hashlib

"""
La siguiente clase posee las 5 funcinoes hash mas usadas en la actualidad
"""

class Hasher:
    def __init__(self, cadena):
        self.cadena = cadena

    def hash_md5(self):
        return hashlib.md5(self.cadena.encode()).hexdigest()

    def hash_sha1(self):
        return hashlib.sha1(self.cadena.encode()).hexdigest()

    def hash_sha256(self):
        return hashlib.sha256(self.cadena.encode()).hexdigest()


    def hash_blake2(self):
        return hashlib.blake2b(self.cadena.encode()).hexdigest()


# Ejemplo de uso
if __name__ == "__main__":
    cadena = "Hola, mundo!"
    hasher = Hasher(cadena)
    print("MD5:", hasher.hash_md5())
    print("SHA1:", hasher.hash_sha1())
    print("SHA256:", hasher.hash_sha256())
    print("BLAKE2:", hasher.hash_blake2())
    
