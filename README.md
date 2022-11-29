# Sistema-Recomendador-Basado-en-el-Contenido
# Integrantes
  - Bruno Lorenzo Arroyo Pedraza - alu0101123677
  - Jonay Estévez Díaz - alu0101100586
  - Carla Cristina Olivares Rodriguez - alu0101120218
  - Jose Miguel Hernandez Santana - alu0101101507

# Ejecución y dependencias
El programa se ha realizado con Python, concretamente con Python3 y en un entorno Ubuntu, si no se dispone de python3 se puede instalar con el siguiente comando en Ubuntu con:

```bash
sudo apt update
sudo apt install python3
```

Si no se ha podido descargar python con los pasos anteriores puede revisar el siguiente enlace: [python3](https://www.makeuseof.com/install-python-ubuntu/)
              
Para el desarrollo del programa se ha utilizado la dependencia de python Pandas, para poder instalar pandas se necesita pip, ambos se pueden instalar con:

```bash
sudo apt-get install python3-pip
sudo pip install pandas
```

Una forma de instalar pandas sin usar pip es con el siguiente comando:

```bash
sudo apt-get install python3-pandas
```

Para el uso de la aplicación se deberá tener en cuenta que los parámetros se han de pasar por línea de comando. El programa recibe como entrada un fichero de texto plano .txt donde cada documento viene representado por una línea del fichero, un fichero que contiene las stop words a utilizar, y un fichero de lematización de términos. Opcionalmente se le puede especificar al programa que la salida por terminal la realice por un fichero de texto plano.

El uso del programa sería el siguiente:

```bash
$ python3 recomendador_contenido.py [-h] -f FILE -l LEMATAZIONE -s STOPWORDS [-o OUTPUT]
```

Un ejemplo de uso sería el siguiente:

```bash
$ python3 recomendador_contenido.py -f ./examples-documents/documents-01.txt -l ./corpus/corpus-en.txt -s ./stop-words/stop-word-en.txt -o ./results/results-01.txt
```
En el repositorio del proyecto se encuentra:
- carpeta corpus con ficheros para realizar la lematización de términos
- carpeta examples-documents con ficheros para realizar prueba
- carpeta results con ficheros con los resultados
- carpeta stop-word con ficheros para realizar la eliminación de stop words

# Descripción del Código

## Main
Se obtienen los argumentos pasados por línea de comando pasado a l programa. para ello, utilizamos *parser*, donde iremos añadiendo los argumentos de los que dispone el programa, los cuales son:

 - *-f || --file* para los ficheros de entrada de datos.
 - *-l || --lematazione* para especificar el fichero que usaremos para la lematización.
 - *-s || --stopwords* para la especificación de las palabras de parada.  
 - *-o || --output* para el fichero donde se almacenarán los resultados (Opcional). En caso de no especificar salida, se mostrarán los resultados por pantalla.

```python
  parser = argparse.ArgumentParser(description='Practica Sistema Recomendador Basado en Contenido')
  parser.add_argument('-f', '--file', type=argparse.FileType('r'), required=True, help='Fichero con los datos de entrada')
  parser.add_argument('-l', '--lematazione', type=argparse.FileType('r'), required=True, help='Lemmatization')
  parser.add_argument('-s', '--stopwords', type=argparse.FileType('r'), required=True, help='Stopwords')
  parser.add_argument('-o', '--output', type=argparse.FileType('w'), help='Fichero de salida')
  args = parser.parse_args()
``` 
Luego, se realiza la lectura del fichero con los datos de entrada y se obtienen los términos para cada documento, mientras se obtienen, se eliminan todos los caracteres especiales y se convierten todas las letras a minúsculas. Para ello, exploramos documento a documento a traves de un bucle y se van eliminando lo especificado anteriormente.

```python
file_lines = args.file.readlines()

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
```

Acto seguido, se debe filtar todos los terminos obtenidos y quitar todas aquellas palabras que concuenden con las *stopwords*. En caso de que coincida, se ingresa dicha parabra en el vector *s* y luego se sustituye del vector de terminos, por el resultado de la diferencia de dicho vector con el *s*, quedando por tanto todos los términos que están en *terms[i]* y no están en *s*.

```python
stop_words = args.stopwords.read()
  
s = []
for i in range(len(terms)):
  for j in range(len(terms[i])):
    if terms [i][j] in stop_words:
      s.append(terms[i][j]) 
  terms[i] = [ele for ele in terms[i] if ele not in s]
  s.clear()
```
Finalmente, antes de dar paso a los calculos, se realiza la lematización de los terminos y se obtiene el vocabulario. Para la lematización, primero, preparamos el contenido del argumento que corresponde con la lematización, para ello, eliminamos todos las caracteres especiales y separamos por espacios todas las cadenas del fichero, obteniendo de esta manera un vector. Tras ésto, se recorre para cada documentos sus terminos y comparamos con el vector de la lematazación, y si concuerdan las cadenas, se sustituye la original por la palabra ya lematizada.

```python
lemmatization = args.lematazione.read()
lemmatization = lemmatization.replace(",", " ")
lemmatization = lemmatization.replace(".", " ")
lemmatization = lemmatization.replace(":", " ")
lemmatization = lemmatization.replace("{", "")
lemmatization = lemmatization.replace("}", "")
lemmatization = lemmatization.replace("\"", "")
lemmatization = lemmatization.split(" ")
  
for i in range(len(terms)):
  for j in range(len(terms[i])):
    for k in range(0, len(lemmatization), 2):
      if terms[i][j] == lemmatization[k]:
        terms[i][j] = lemmatization[k+1]
        break
```

Para el vocabulario, simplemente, se recorre de nuevo todos los terminos, y si el termino explorado no se encuentra en el vocabulario se agrega.

```python
vocab = []
for i in terms:
  for j in i:
    if j not in vocab:
      vocab.append(j)
```

Es entonces cuando se procede a calcular la matriz de terminos, donde se almacena el *TF*, *IDF*, y el *TF-IDF*, a través de las siguientes funcionalidades del programa.

```python
terms_matrix = tf_calculation(terms, vocab)
terms_matrix = idf_calculation(terms, terms_matrix, vocab)
terms_matrix = tf_idf_calculation(terms_matrix)
```
Además, tambien creamos la matriz de similitud entre documentos, donde se utiliza la siguiente función del programa.

```python
similarity_matrix = similarity_calculation(terms, terms_matrix, vocab)
```

Para finalizar, se muestran los resultados de las dos matrices que se obtienen tras la ejecución, la matriz de terminos y la matriz de similitud, y se cierran todos aquellos ficheros que se han abierto.

```python
print("--RECOMENDADOR BASADO EN CONOCIMIENTO--")
show_results_terms_matrix(terms_matrix)
print("\n")
show_results_similarity_matrix(similarity_matrix)

args.file.close()
args.stopwords.close()
args.lematazione.close()
if args.output is not None:
  args.output.close()
  sys.stdout = original_stdout
```

## Calculo del TF

Para calcular el valor TF de cada termino en cada documento se recorre los terminos de cada documento y se cuenta el número de veces que aparece cada termino en dicho documento, para ello, se utiliza un contador que se reinicia cada vez que se cambia de documento. Si el termino aparece al menos una vez  se guarda en la recien creada matriz de terminos como realizando la operación de tf = 1 + log10(numero de veces que aparece en el documento).
Si no ha aparece se guarda en la matriz de términos como tf = 0.

Este aparatado es importando ya que retornamos la matriz de terminos con el valor de tf calculado para
cada termino, matriz que se usará posteriormente para el resto de operaciones. Para emular el comportamiento
de la matriz de terminos de manera cómoda se usan los diccionarios de Python.

```python
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
```

## Calculo del DF

El calculo del DF de cada documento, se analiza la cantidad de veces que aparece dicho termino, para ello, se almacena dicha cantidad en una variable de nombre *final_count*. Se recorren las palabras del vocabulario y tambien los documentos, y se alamacena en la valiable *count* las cuncurrencias de la palabra en el documento, y luego se almacena, si no lo está, se almacena el *count* calculado.

```python
def df_calculation(terms, vocab):
  final_count = {}
  for word in vocab:
    count = 0
    for doc in terms:
      count += doc.count(word)
    if not word in final_count:
      final_count[word] = count
  return dict(final_count)
```

## Calculo del IDF

Con el DF calculado se procede a calcular el IDF de cada termino, para ello, se recorre
el recorre el diccionario obtenido del calculo del DF y se calcula el valor de cada IDF
con la operación idf = log10(numero de documentos / numero de documentos que contiene el termino)

```python
def idf_calculation(terms, terms_matrix, vocab):
  corpus = len(terms)
  df_matrix = df_calculation(terms, vocab)
  for word in df_matrix:
    for key in terms_matrix:
      if key[1] == word:
        terms_matrix[key]['idf'] = math.log10(corpus/df_matrix[word])
  return dict(terms_matrix)
```

## Calculo del TF-IDF

El calculo del TF-IDF se realiza multiplicando el valor de TF por el valor de IDF de cada termino,
para ello se recorre la matriz de terminos y se realiza la multiplicación para guardarlo en la matriz de terminos.

```python
def tf_idf_calculation(terms_matrix):
  for key in terms_matrix:
    terms_matrix[key]['tf-idf'] = terms_matrix[key]['tf'] * terms_matrix[key]['idf']
  return dict(terms_matrix)
```

## Similitud entre Documentos
En esta función, se realiza el calculo de la similitud entre documentos mediante uso del coseno, para ello, lo que se realiza para cada palabra, se realiza la siguiente divición, en el numerador, tendremos el sumatorio de la multiplicación, para la misma palabra en los dos documentos, del valor *tf-idf*. Luego tendremos dos denominadores, que luego se multiplicaran para realizar la divición. El primer denominador, es la raiz del sumarotio de la multiplicación al cuadrado de dicha palabra en el priomer documento, y el otro denominador es lo mismo, salvo que para el segundo documento, devolviendo así la medida de la similitud.

```python
def similarity_calculation_cos(terms_matrix, vocab, doc1, doc2):
  numerator = 0
  denominator_izq = 0
  denominator_der = 0
  for word in vocab:
    numerator += terms_matrix[(doc1, word)]['tf-idf'] * terms_matrix[(doc2, word)]['tf-idf']
    denominator_izq += terms_matrix[(doc1, word)]['tf-idf']**2
    denominator_der += terms_matrix[(doc2, word)]['tf-idf']**2
  denominator = math.sqrt(denominator_izq) * math.sqrt(denominator_der)    
  if denominator == 0:
    return 0
  return round(numerator / denominator, 3) 
```

## Calculo de la matriz de similitud
Se procede con la creación de una matriz, de nom,bre *similarity_matrix*, la cual rellenamos con 0 para las mismas dimencones de la variable de *terms* y por último para cada una de las posiciones, se calcula la similitud entre documentos explicada con anterioridad.

```python
def similarity_calculation(terms, terms_matrix, vocab):
  similarity_matrix = [[0 for i in range(len(terms))] for j in range(len(terms))]
  for i in range(len(similarity_matrix)):
    for j in range(len(similarity_matrix)):
      similarity_matrix[i][j] = similarity_calculation_cos(terms_matrix, vocab, i, j)
  return similarity_matrix
```

## Muestra de los resultados

Para mostrar los resultados tanto de la matriz de términos como de la matriz de similitud
se realizan los siguientes métodos.

Para el diccionario utilizado para la matriz de terminos, se formatea la salida
y se va recorriendo el diccionario para mostrar los valores de cada termino, siempre
que este termino esté en el documento.

```python
def show_results_terms_matrix(terms_matrix):
  actual_doc = 0
  count = 1
  print("ANALISIS DE CADA DOCUMENTO")
  print("Documento 0")
  print('\n{:<3} {:<20} {:<10} {:<10} {:<10}\n'.format("N.", "Termino", "TF", "IDF", "TF-IDF"))
  for key in terms_matrix.keys():
    if terms_matrix[key]['tf'] > 0:
      if actual_doc != key[0]:
        count = 1
        actual_doc = key[0]
        print('--------------------------------------------------------')
        print("\nDocumento {}".format(actual_doc))
        print('\n{:<3} {:<20} {:<10} {:<10} {:<10}\n'.format("N.", "Termino", "TF", "IDF", "TF-IDF"))
      print('{:<3} {:<20} {:<10} {:<10} {:<10}'.format(str(count), key[1], round(terms_matrix[key]['tf'], 3), round(terms_matrix[key]['idf'], 3), round(terms_matrix[key]['tf-idf'], 3)))
      count = count + 1
```

Para mostrar la matriz de similitud formateada se utiliza pandas, para ello se transforma
la matriz de similitud en un dataframe de pandas y se muestra.

```python
def show_results_similarity_matrix(similarity_matrix):
  print("MATRIZ DE SIMILITUD")
  print(pandas.DataFrame(similarity_matrix))
```

# Ejemplo de Ejecución
```bash
$ python3 recomendador_contenido.py -f ./examples-documents/documents-01.txt -s ./stop-words/stop-words-en.txt -l ./corpus/corpus-en.txt 
--RECOMENDADOR BASADO EN CONOCIMIENTO--
ANALISIS DE CADA DOCUMENTO
Documento 0

N.  Termino              TF         IDF        TF-IDF    

1   aromas               1.0        0.398      0.398     
2   include              1.0        1.0        1.0       
3   tropical             1.0        1.0        1.0       
4   fruit                1.0        0.699      0.699     
5   broom                1.0        1.0        1.0       
6   brimstone            1.0        1.0        1.0       
7   dried                1.301      0.523      0.68      
8   herb                 1.0        0.699      0.699     
9   palate               1.0        0.523      0.523     
10  overly               1.0        1.0        1.0       
11  expressive           1.0        1.0        1.0       
12  offer                1.0        0.699      0.699     
13  unripened            1.0        1.0        1.0       
14  apple                1.0        0.699      0.699     
15  citrus               1.0        1.0        1.0       
16  sage                 1.0        1.0        1.0       
17  brisk                1.0        0.699      0.699     
18  acidity              1.0        0.155      0.155     
--------------------------------------------------------

Documento 1

N.  Termino              TF         IDF        TF-IDF    

1   acidity              1.0        0.155      0.155     
2   ripe                 1.0        1.0        1.0       
3   fruity               1.0        0.699      0.699     
4   wine                 1.0        0.301      0.301     
5   smooth               1.0        1.0        1.0       
6   structured           1.0        1.0        1.0       
7   firm                 1.0        0.699      0.699     
8   tannins              1.0        0.699      0.699     
9   fill                 1.0        1.0        1.0       
10  juicy                1.0        1.0        1.0       
11  berry                1.0        0.699      0.699     
12  fruits               1.0        0.699      0.699     
13  freshened            1.0        1.0        1.0       
14  drinkable            1.0        1.0        1.0       
15  2016                 1.0        1.0        1.0       
--------------------------------------------------------

Documento 2

N.  Termino              TF         IDF        TF-IDF    

1   acidity              1.0        0.155      0.155     
2   wine                 1.0        0.301      0.301     
3   tart                 1.0        1.0        1.0       
4   snappy               1.0        1.0        1.0       
5   flavors              1.301      0.398      0.518     
6   lime                 1.0        1.0        1.0       
7   flesh                1.0        1.0        1.0       
8   rind                 1.0        0.699      0.699     
9   dominate             1.0        1.0        1.0       
10  green                1.0        0.699      0.699     
11  pineapple            1.0        0.699      0.699     
12  pokes                1.0        1.0        1.0       
13  crisp                1.0        0.699      0.699     
14  underscoring         1.0        1.0        1.0       
15  stainlesssteel       1.0        1.0        1.0       
16  fermented            1.0        1.0        1.0       
--------------------------------------------------------

Documento 3

N.  Termino              TF         IDF        TF-IDF    

1   aromas               1.0        0.398      0.398     
2   palate               1.0        0.523      0.523     
3   rind                 1.0        0.699      0.699     
4   pineapple            1.0        0.699      0.699     
5   lemon                1.0        1.0        1.0       
6   pith                 1.0        1.0        1.0       
7   orange               1.0        1.0        1.0       
8   blossom              1.0        1.0        1.0       
9   start                1.0        1.0        1.0       
10  bite                 1.0        1.0        1.0       
11  opulent              1.0        1.0        1.0       
12  note                 1.0        0.699      0.699     
13  honeydrizzled        1.0        1.0        1.0       
14  guava                1.0        1.0        1.0       
15  mango                1.0        1.0        1.0       
16  give                 1.0        1.0        1.0       
17  slightly             1.0        1.0        1.0       
18  astringent           1.0        1.0        1.0       
19  semidry              1.0        1.0        1.0       
20  finish               1.0        0.699      0.699     
--------------------------------------------------------

Documento 4

N.  Termino              TF         IDF        TF-IDF    

1   wine                 1.0        0.301      0.301     
2   regular              1.0        1.0        1.0       
3   bottling             1.0        1.0        1.0       
4   2012                 1.0        1.0        1.0       
5   tannic               1.0        1.0        1.0       
6   rustic               1.0        1.0        1.0       
7   earthy               1.0        1.0        1.0       
8   herbal               1.0        0.699      0.699     
9   characteristics      1.0        1.0        1.0       
10  pleasantly           1.0        1.0        1.0       
11  unfussy              1.0        1.0        1.0       
12  country              1.0        1.0        1.0       
13  good                 1.0        1.0        1.0       
14  companion            1.0        1.0        1.0       
15  hearty               1.0        1.0        1.0       
16  winter               1.0        1.0        1.0       
17  stew                 1.0        1.0        1.0       
--------------------------------------------------------

Documento 5

N.  Termino              TF         IDF        TF-IDF    

1   aromas               1.0        0.398      0.398     
2   fruit                1.0        0.699      0.699     
3   acidity              1.0        0.155      0.155     
4   flavors              1.0        0.398      0.398     
5   green                1.0        0.699      0.699     
6   finish               1.0        0.699      0.699     
7   herbal               1.0        0.699      0.699     
8   blackberry           1.0        1.0        1.0       
9   raspberry            1.0        1.0        1.0       
10  show                 1.0        1.0        1.0       
11  typical              1.0        1.0        1.0       
12  navarran             1.0        1.0        1.0       
13  whiff                1.0        1.0        1.0       
14  herbs                1.0        1.0        1.0       
15  case                 1.0        1.0        1.0       
16  horseradish          1.0        1.0        1.0       
17  mouth                1.0        1.0        1.0       
18  bodied               1.0        1.0        1.0       
19  tomatoey             1.0        1.0        1.0       
20  spicy                1.0        1.0        1.0       
21  complement           1.0        1.0        1.0       
22  dark                 1.0        1.0        1.0       
23  plum                 1.0        1.0        1.0       
24  fresh                1.0        0.398      0.398     
25  grabby               1.0        1.0        1.0       
--------------------------------------------------------

Documento 6

N.  Termino              TF         IDF        TF-IDF    

1   aromas               1.0        0.398      0.398     
2   herb                 1.0        0.699      0.699     
3   palate               1.0        0.523      0.523     
4   acidity              1.0        0.155      0.155     
5   tannins              1.0        0.699      0.699     
6   berry                1.0        0.699      0.699     
7   fresh                1.0        0.398      0.398     
8   bright               1.0        1.0        1.0       
9   informal             1.0        1.0        1.0       
10  open                 1.0        1.0        1.0       
11  candied              1.0        1.0        1.0       
12  white                1.0        1.0        1.0       
13  pepper               1.0        1.0        1.0       
14  savory               1.0        0.699      0.699     
15  carry                1.0        1.0        1.0       
16  balance              1.0        0.523      0.523     
17  soft                 1.0        1.0        1.0       
--------------------------------------------------------

Documento 7

N.  Termino              TF         IDF        TF-IDF    

1   offer                1.0        0.699      0.699     
2   acidity              1.0        0.155      0.155     
3   wine                 1.0        0.301      0.301     
4   firm                 1.0        0.699      0.699     
5   balance              1.0        0.523      0.523     
6   dry                  1.0        0.699      0.699     
7   restrain             1.0        1.0        1.0       
8   spice                1.0        0.699      0.699     
9   profusion            1.0        1.0        1.0       
10  texture              1.0        0.699      0.699     
11  food                 1.0        1.0        1.0       
--------------------------------------------------------

Documento 8

N.  Termino              TF         IDF        TF-IDF    

1   dried                1.0        0.523      0.523     
2   brisk                1.0        0.699      0.699     
3   fruity               1.0        0.699      0.699     
4   wine                 1.0        0.301      0.301     
5   flavors              1.0        0.398      0.398     
6   note                 1.0        0.699      0.699     
7   fresh                1.0        0.398      0.398     
8   savory               1.0        0.699      0.699     
9   thyme                1.0        1.0        1.0       
10  accent               1.0        1.0        1.0       
11  sunnier              1.0        1.0        1.0       
12  preserve             1.0        1.0        1.0       
13  peach                1.0        1.0        1.0       
14  offdry               1.0        1.0        1.0       
15  elegant              1.0        1.0        1.0       
16  sprightly            1.0        1.0        1.0       
17  footprint            1.0        1.0        1.0       
--------------------------------------------------------

Documento 9

N.  Termino              TF         IDF        TF-IDF    

1   apple                1.0        0.699      0.699     
2   acidity              1.0        0.155      0.155     
3   fruits               1.0        0.699      0.699     
4   crisp                1.0        0.699      0.699     
5   fresh                1.0        0.398      0.398     
6   balance              1.0        0.523      0.523     
7   dry                  1.0        0.699      0.699     
8   spice                1.0        0.699      0.699     
9   texture              1.0        0.699      0.699     
10  great                1.0        1.0        1.0       
11  depth                1.0        1.0        1.0       
12  flavor               1.0        1.0        1.0       
13  touch                1.0        1.0        1.0       
14  drink                1.0        1.0        1.0       


MATRIZ DE SIMILITUD
       0      1      2      3      4      5      6      7      8      9
0  1.000  0.002  0.002  0.030  0.000  0.043  0.082  0.060  0.070  0.050
1  0.002  1.000  0.010  0.000  0.007  0.002  0.094  0.077  0.052  0.054
2  0.002  0.010  1.000  0.072  0.007  0.048  0.002  0.014  0.026  0.053
3  0.030  0.000  0.072  1.000  0.000  0.036  0.032  0.000  0.035  0.000
4  0.000  0.007  0.007  0.000  1.000  0.028  0.000  0.010  0.007  0.000
5  0.043  0.002  0.048  0.036  0.028  1.000  0.023  0.002  0.021  0.014
6  0.082  0.094  0.002  0.032  0.000  0.023  1.000  0.037  0.058  0.048
7  0.060  0.077  0.014  0.000  0.010  0.002  0.037  1.000  0.011  0.252
8  0.070  0.052  0.026  0.035  0.007  0.021  0.058  0.011  1.000  0.016
9  0.050  0.054  0.053  0.000  0.000  0.014  0.048  0.252  0.016  1.000
```