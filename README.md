# Implementación del algoritmo KNN del framework ELKI

**Idea principal del algoritmo:** “A point in a data set is an outlier with respect to parameters k and d if no more than k
points in the data set are at a distance of d or less from p.” [Ramaswamy et al., 2000](https://webdocs.cs.ualberta.ca/~zaiane/pub/check/ramaswamy.pdf)

El algoritmo KNN de ELKI esta desarrollado en java y se usara como Herramiento de la interfaz de linea de comandos.

## Ejecutar los algoritmos de ELKI

Se pudo ejecutar los algoritmos en un centOS sin interfaz gráfica usando el comando que se encuentra en *CLI-ELKI_0.2.sh*, en este script se usando ELKI como una herramienda de linea de comandos en la terminal de linux. Se hace un script con el fin de programar la ejecución del algoritmo más adelante.

> Aquí se puede descargar el jar: [elki-bundle-0.7.1.jar](https://elki-project.github.io/releases/release0.7.1/elki-bundle-0.7.1.jar).

El algoritmo que para este caso nos interesa es el KNNOutlier. Un ejemplo de como puede ser ejecutado es el siguiente:

```javascript
_java -jar elki-bundle-0.7.1.jar KDDCLIApplication -verbose -dbc.in dataset.txt -algorithm outlier.distance.KNNOutlier -knno.k 5
```

donde dataset.txt puede ser cualquier dataset y 5 corresponde al parametro k. [Mas ejemplos](https://elki-project.github.io/releases/release0.7.0/doc/examplecalls.html)

Se realiza un script que como entrada toma un dataset y un valor de k, llamado *KNN.sh*, con el objetivo de estudiar el algoritmo con diferentes datasets y parametros k de entrada.

Donde: k es el numero de vecinos de un punto del que estamos interesados y dataset es el conjunto de datos al que le aplicamos el algoritmo.

Para ejecutarlo se escribe en la terminal, por ejemplo:

```bash
$./KNN.sh mydata/exampledata.txt 5
```
## Establecer los parametros de entrada para el algoritmo KNN

Las entradas para el algoritmo KNN son un numero positivo K y un dataset

Según la bibliografía estudiada los mejores valores para k en el análisis de logs con KNN se encuentran entre 4 y 10, según [Anomaly Detection in Application Log Data](https://dspace.library.uu.nl/bitstream/handle/1874/338664/thesis-patrick-kostjens.pdf?sequence=2&isAllowed=y) y [Detecting Anomalies in System Log Files using Machine Learning Techniques](ftp://ftp.informatik.uni-stuttgart.de/pub/library/medoc.ustuttgart_fi/BCLR-0148/BCLR-0148.pdf)

Ahora para el dataset se debe indicar que información se necesita. Las anomalias que se quieren detectar en los logs de las aplicaciones son:

* Los acceso exitosos aparece más veces que lo usual
* Los acceso exitosos aparece menos veces que lo usual
* Los acceso exitosos deja de aparecer
* Un usuario nuevo aparece
* Modification of any data characteristics, including access control permissions or labels, location in database or file system, or data ownership. Administrators can detect if their configurations were changed.

> All authentication events (logging in, logging out, failed logins, etc.) that allow to detect brute force and guessing attacks.

> Algunos ejemplos de archivos de logs son: transaction log file, event log file, audit log file, server logs, etc. Syslog messages provide the information by where, when and why, i.e., IP-Address, Timestamp and the log message.

Por lo tanto, se identificaron las siguientes variables que servirán como entrada al algoritmo, junto con el parametro k.

* Minute
* Hour
* Day
* Count

Gracias a la ayuda de @PatrickKostjens se pudo trabajar con un generador de entradas artificiales para el algoritmos de detección de anomalías, el cual fue utilizado para comparar varios algoritmos y concluir que el mejor comportamiento lo daba el algoritmo KNNoutlier. Esto ayudo a identificar las variables antes mencionadas.


### Extraer parametros para el algoritmo de Elasticsearch

**¿Cómo se va a hacer?**

* Consultar (query) una evento en especifico en elasticsearch cada 5 min usando python, ejemplo: Accesos exitosos, fallo en la autenticación, etc.
* Almacenar la cuenta(hits) en un dataset, junto con el timestamp.
* Usar el algoritmo de deteción de anomalias KNNoutlier.

**Query:**
```javascript
GET /logstash-*/_search?filter_path=hits.total
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

```
>Nota: Este query consulta la cantidad de acceso exitosos en los ultimos 5 minutos.

Con el fin de tener los datos de entrada del algoritmo en la forma que lo necesita KNNoutlier, se desarrollo el script *QueryingES_v5.py*

Corriendo el colector de datos durante 24 horas, con una tasa de consulta de 5min, se genero un archivo de 10KB.

## Aplicar KNNoutlier con dataset real

Lo primero que se debemos hacer es dejar recolectar información, dejando correr el script *QueryingES_v5.py*...

Se aplica el algoritmo de KNNoutlier, identificando comportamiento fuera de lo normal debido a la puntuación que le da el algoritmo a cada grupo de logs. 

## Procedimiento para alertar sobre anomalías 

Con el fin de enviar correo con el detalle de la anomalía detectada al personal correspondiente, debemos seguir los siguientes pasos:

1. crear y guardar un busqueda por el evento indeseable, y guardar la cuenta mas algún id que permita saber a que grupo se refiere.

2. Aplicar el algoritmo de detección de anomalías a la busqueda guardada, y cuando la puntuación que da el algoritmo supere un umbral enviar la información que permita identificar esos eventos al grupo a elasticsearch.

3. Programar un regla en [sentinl](https://docs.search-guard.com/latest/search-guard-sentinl) (plugin de ELK) para enviar correos cuando al buscar lo que se subió a elasticsearch concida con ciertas condiciones, como se observa [aquí](https://github.com/jfernandomarquez/Consultas-Elasticsearch/blob/master/Configuracion_watchers_sentinl.md). 

**Inspiración:**

[Anomaly detection rules - IBM](https://www.ibm.com/support/knowledgecenter/en/SS42VS_7.3.0/com.ibm.qradar.doc/c_qradar_rul_anomaly_detection.html)

[Anomaly Detection in Application Log Data, Patrick KOSTJENS](https://github.com/repat/README-template/blob/master/README-websites-gh-pages.md)

### Alertar cuando un usuarios se conecte en horarios fuera de oficina

1. Programar un busqueda en horarios fuera de oficina cada 10 min.
2. Cuando se tenga un usuario diferente a los autorizados enviar una alerta por correo.

### Alertar cuando usuario se conecte por VPN en un pais diferente a CO

1. Utilizar la utilidad de detección de anomalías de sentinl 


> "Is the data the same as yesterday at the same time?"
> "How much does the data change when it compares this minute to the minute before?"


