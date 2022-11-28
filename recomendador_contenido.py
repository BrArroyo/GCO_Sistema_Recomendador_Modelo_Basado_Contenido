import argparse
import collections
import math
import sys
# ==============================================================================
#                           METODOS
# ==============================================================================

# Calculamos TF
def tf_calculation(terms, vocab):
  count = {}
  for index, doc in enumerate(terms):
    for word in vocab:
      if not (index, word) in count:
        count[(index, word)] = {}
        if doc.count(word) > 0:
          count[(index, word)]['tf'] = 1 + math.log10(doc.count(word))
        else:
          count[(index, word)]['tf'] = 0
  return dict(count)
  
# Calculamos DF
def df_calculation(terms, vocab):
  final_count = {}
  for word in vocab:
    count = 0
    for doc in terms:
      count += doc.count(word)
    if not word in final_count:
      final_count[word] = count
  return dict(final_count)

# Calculamos IDF
def idf_calculation(terms, terms_matrix, vocab):
  corpus = len(terms)
  df_matrix = df_calculation(terms, vocab)
  for word in df_matrix:
    for key in terms_matrix:
      if key[1] == word:
        terms_matrix[key]['idf'] = math.log10(corpus/df_matrix[word])
  return dict(terms_matrix)

# Calculamos TF-IDF
def tf_idf_calculation(terms_matrix):
  for key in terms_matrix:
    terms_matrix[key]['tf-idf'] = terms_matrix[key]['tf'] * terms_matrix[key]['idf']
  return dict(terms_matrix)


def similarity_calculation(terms_matrix):
  print("Calculando similitud...")

def show_results_terms_matrix(terms_matrix, vocab):
  actual_doc = 0
  count = 1
  print('\n{:<3} {:<20} {:<10} {:<10} {:<10}\n'.format("N.", "Termino", "TF", "IDF", "TF-IDF"))
  for key in terms_matrix.keys():
    if terms_matrix[key]['tf'] > 0:
      if actual_doc != key[0]:
        count = 1
        actual_doc = key[0]
        print('\n{:<3} {:<20} {:<10} {:<10} {:<10}\n'.format("N.", "Termino", "TF", "IDF", "TF-IDF"))

      print('{:<3} {:<20} {:<10} {:<10} {:<10}'.format(str(count), key[1], round(terms_matrix[key]['tf'], 3), round(terms_matrix[key]['idf'], 3), round(terms_matrix[key]['tf-idf'], 3)))
      count = count + 1
      


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
  terms_to_replace = ["\n",",",".",":",";","¡","!","¿","?","-"]
  for i in file_lines:
    line = i.split()
    aux_line = []
    for j in line:
      for term in terms_to_replace:
        if term in j:
          j.replace(term, "")
      j = j.lower()
      aux_line.append(j)
    terms.append(aux_line)
  
  # (esto se puede cambiar para pedirlo por linea de comando)
  # Eliminamos stopwords 
  stop_words = []
  f = open("./stop-words/stop-words-en.txt", "r")
  stop_words = f.read()
  f.close()
  
  s = []
  for i in range(len(terms)):
    for j in range(len(terms[i])):
      if terms [i][j] in stop_words:
        s.append(terms[i][j]) 
    terms[i] = [ele for ele in terms[i] if ele not in s]
    s.clear()

  
  # Lematizamos los terminos
  #HACER ESTO


  # Obtenemos el vocabulario
  vocab = []
  for i in terms:
    for j in i:
      if j not in vocab:
        vocab.append(j)
  
  # Creamos la matriz de terminos donde se almacenan lo siguiente: TF, IDF, TF-IDF
  # TF = frecuencia de termino en el documento
  # IDF = logaritmo del numero de documentos entre el numero de documentos que contienen el termino
  # TF-IDF = TF * IDF
  terms_matrix = tf_calculation(terms, vocab)
  terms_matrix = idf_calculation(terms, terms_matrix, vocab)
  terms_matrix = tf_idf_calculation(terms_matrix)

  # Creamos la matriz de similitud entre documentos
  # Similitud = coseno del angulo entre los vectores de terminos
  # Coseno = producto escalar entre los vectores de terminos / (modulo del vector de terminos 1 * modulo del vector de terminos 2) 
  similarity_matrix = [[0 for i in range(len(terms))] for j in range(len(terms))]
  similarity_matrix = similarity_calculation(terms_matrix)
  
  show_results_terms_matrix(terms_matrix, vocab)
  show_results_similarity_matrix(similarity_matrix)

  args.file.close()
  if args.output is not None:
    args.output.close()
    sys.stdout = original_stdout