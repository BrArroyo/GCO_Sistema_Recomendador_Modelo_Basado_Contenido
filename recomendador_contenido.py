import argparse
import collections
import math
import sys

# ==============================================================================
#                           METODOS
# ==============================================================================

def tf_calculation(terms, terms_matrix, vocab):
  print("Calculando TF...")

def idf_calculation(terms, terms_matrix, vocab):
  print("Calculando IDF...")

def tf_idf_calculation(terms_matrix):
  print("Calculando TF-IDF...")

def similarity_calculation(terms_matrix, similarity_matrix):
  print("Calculando similitud...")

def show_results_terms_matrix(terms_matrix, vocab):
  print("Matriz de términos:")

def show_results_similarity_matrix(similarity_matrix):
  print("Matriz de similitud:")


# ==============================================================================
#                           MAIN
# ==============================================================================


if __name__ == '__main__':
  # Obtención de los parámetros pasados al programa
  parser = argparse.ArgumentParser(description='Practica Sistema Recomendador Basado en Contenido')
  parser.add_argument('-f', '--file', type=argparse.FileType('r'), required=True, help='Fichero con los datos de entrada')
  parser.add_argument('-o', '--output', type=argparse.FileType('w'), required=True, help='Fichero de salida')
  args = parser.parse_args()

  original_stdout = sys.stdout # Save a reference to the original standard output
  sys.stdout = args.output
  
  # # Si elegimo que sea por pantalla o fichero usar esto
  # if args.output is not None:
  #    sys.stdout = args.output
  
  # Lectura del fichero especificado por el usuario
  file_lines = args.file.readlines()

  # Obtenemos los terminos de cada documento (eliminar caracteres especiales, pasar a minusculas, etc)
  # Eliminamos los caracteres especiales y convertimos a minusculas
  terms = []
  for i in file_lines:
    line = i.split()
    aux_line = []
    for j in line:
      j = j.replace(",", "")
      j = j.replace(".", "")
      j = j.replace(":", "")
      j = j.replace(";", "")
      j = j.replace("¡", "")
      j = j.replace("!", "")
      j = j.replace("¿", "")
      j = j.replace("?", "")
      j = j.replace("-", "")
      j = j.lower()
      aux_line.append(j)
    terms.append(aux_line)
  
  # (esto se puede cambiar para pedirlo por linea de comando)
  # Eliminamos stopwords 
  stop_words = []
  f = open("./stop-words/stop-words-en.txt", "r")
  stop_words = f.read()
  f.close()

  for i in range(len(terms)):
    for j in range(len(terms[i])):
      if terms [i][j] in stop_words:
        terms[i][j] = "*"
  
  for i in range(len(terms)):
    terms[i] = [i for i in terms[i] if i != "*"]
  
  # Lematizamos los terminos
  #HACER ESTO


  # Obtenemos el vocabulario
  vocab = []
  for i in terms:
    for j in i:
      if j not in vocab:
        vocab.append(j)
  
  # Creamos la maatriz de terminos donde se almacenan lo siguiente: TF, IDF, TF-IDF
  # TF = frecuencia de termino en el documento
  # IDF = logaritmo del numero de documentos entre el numero de documentos que contienen el termino
  # TF-IDF = TF * IDF
  terms_matrix = [[[0,0,0] for i in range(len(vocab))] for j in range(len(terms))]

  # Creamos la matriz de similitud entre documentos
  # Similitud = coseno del angulo entre los vectores de terminos
  # Coseno = producto escalar entre los vectores de terminos / (modulo del vector de terminos 1 * modulo del vector de terminos 2) 
  similarity_matrix = [[0 for i in range(len(terms))] for j in range(len(terms))]

  # Realizamos las operaciones necesarias para obtener la matriz de terminos y la matriz de similitud
  tf_calculation(terms, terms_matrix, vocab)
  idf_calculation(terms, terms_matrix, vocab)
  tf_idf_calculation(terms_matrix)
  similarity_calculation(terms_matrix, similarity_matrix)
  show_results_terms_matrix(terms_matrix, vocab)
  show_results_similarity_matrix(similarity_matrix)

  args.file.close()
  if args.output is not None:
    args.output.close()
    sys.stdout = original_stdout