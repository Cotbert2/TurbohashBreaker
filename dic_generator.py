#Dependencies
from itertools import product

class DictionaryGenerator:
    def __init__(self, caracteres, longitud):
        self.caracteres = caracteres
        self.longitud = longitud

    def generar_diccionario(self):
        with open("dic.txt", "w") as archivo:
            for combinacion in product(self.caracteres, repeat=self.longitud):
                archivo.write("".join(combinacion) + "\n")

# Ejemplo de uso
if __name__ == "__main__":
    caracteres = "abcdefghijklmnopqrstuvwxyz"
    longitud = 3
    diccionario = DictionaryGenerator(caracteres, longitud)
    diccionario.generar_diccionario()
    print("Diccionario generado en dic.txt")
