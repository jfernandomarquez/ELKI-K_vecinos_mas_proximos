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

Según la bibliografía estudiada los mejores valores para el analisis de logs con KNN se encuntran entre 4 y 10, según [Anomaly Detection in Application Log Data](https://dspace.library.uu.nl/bitstream/handle/1874/338664/thesis-patrick-kostjens.pdf?sequence=2&isAllowed=y) y [Detecting Anomalies in System Log Files using Machine Learning Techniques](ftp://ftp.informatik.uni-stuttgart.de/pub/library/medoc.ustuttgart_fi/BCLR-0148/BCLR-0148.pdf)

Gracias a la ayuda de @PatrickKostjens se pudo trabajar con un generador de entradas artificiales para el algoritmo KNNoutlier, con el cual se identificaron las siguientes entradas del algoritmo, para nuestro caso de detección de anomalias en logs de aplicaciones:

* Minute
* Hour
* Day
* Count

Continuará..

### Extraer parametros para el algoritmo de Elasticsearch

**Query**

## Depurar los scripts




