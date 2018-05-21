# ELKI-K_vecinos_mas_proximos
Implementación del algoritmo KNN (K_vecinos_más_próximos) del framework ELKI.

**Idea principal del algoritmo:** “A point in a data set is an outlier with respect to parameters k and d if no more than k
points in the data set are at a distance of d or less from p.” [Ramaswamy et al., 2000](https://webdocs.cs.ualberta.ca/~zaiane/pub/check/ramaswamy.pdf)

El algoritmo KNN de ELKI esta desarrollado en java y se usara como Herramiento de la interfaz de linea de comandos.

## Ejecutar los algoritmos de ELKI

Se pudo ejecutar los algoritmos en un centOS sin interfaz gráfica usando el comando que se encuentra en *CLI-ELKI_0.2.sh*, en este script se usando ELKI como una herramienda de linea de comandos en la terminal de linux. Se hace un script con el fin de programar la ejecución del algoritmo más adelante.

> Aquí se puede descargar el jar: [elki-bundle-0.7.1.jar](https://elki-project.github.io/releases/release0.7.1/elki-bundle-0.7.1.jar).

El algoritmo que para este caso nos interesa es el KNNOutlier. Un ejemplo de como puede ser ejecutado es el siguiente:

_java -jar elki-bundle-0.7.1.jar KDDCLIApplication -verbose -dbc.in dataset.txt -algorithm outlier.distance.KNNOutlier -knno.k 5

donde dataset.txt puede ser cualquier dataset y 5 corresponde al parametro k.

Se realiza un script que como entrada toma un dataset y un valor de k, llamado *KNN.sh*, con el objetivo de estudiar el algoritmo con diferentes datasets y parametros k de entrada.

Donde: k es el numero de vecinos de un punto del que estamos interesados y dataset es el conjunto de datos al que le aplicamos el algoritmo.

Para ejecutarlo se escribe en la terminal, por ejemplo:

$./KNN.sh mydata/exampledata.txt 5

## Establecer los parametros de entrada para el algoritmo KNN

Las entradas para el algoritmo KNN son un numero positivo K y un dataset

Según la bibliografía estudiada los mejores valores para k en el análisis de logs con KNN se encuentran entre 4 y 10, según [Anomaly Detection in Application Log Data](https://dspace.library.uu.nl/bitstream/handle/1874/338664/thesis-patrick-kostjens.pdf?sequence=2&isAllowed=y) y [Detecting Anomalies in System Log Files using Machine Learning Techniques](ftp://ftp.informatik.uni-stuttgart.de/pub/library/medoc.ustuttgart_fi/BCLR-0148/BCLR-0148.pdf)

Ahora para el dataset se debe indicar que información se necesita. Las anomalias que se quieren detectar en los logs de las aplicaciones son:

* Los acceso exitosos aparece más veces que lo usual
* Los acceso exitosos aparece menos veces que lo usual
* Los acceso exitosos deja de aparecer
* Un usuario nuevo aparece

Por lo tanto, se identificaron las siguientes variables que servirán como entrada al algoritmo, junto con el parametro k.

* Minute
* Hour
* Day
* Count

Gracias a la ayuda de @PatrickKostjens se pudo trabajar con un generador de entradas artificiales para el algoritmos de detección de anomalías, el cual fue utilizado para comparar varios algoritmos y concluir que el mejor comportamiento lo daba el algoritmo KNNoutlier. Esto ayudo a identificar las variables antes mencionadas.


### Extraer parametros para el algoritmo de Elasticsearch

**¿Cómo se va a hacer?**

* Consultar (query) una evento en especifico en elasticsearch usando python cada 5 min, ejemplo: host, application,etc(aggregations)
* Almacenar la cuenta(hits) en un dataset, junto con el timestamp.
* Usar el algoritmo de deteción de anomalias KNNoutlier



> **Query:** GET /logstash-*/_search?filter_path=hits.total
{
  "query": {
    "bool": {
      "must": [
        {
          "match": {
            "task": "Logon"
          }
        },
        {
          "range": {
            "@timestamp": {
              "gte": "now-5m/m",
              "lt": "now"
            }
          }
        }
      ]
    }
  }
}
*Nota:* Este query consulta la cantidad de acceso exitosos en los ultimos 5 minutos.

## Implementar KNNoutlier con dataset real




