# Implementación del Algoritmo KNN del Framework ELKI en un Ecosistema ELK.

Con en fin de identificar y alertar comportamientos fuera de lo normal en los sistemas de información, se busca aplicar algoritmos de *machine learning* a los registros del sistema que se encuentran centralizados en *elasticsearch*.

## Ejecutar los algoritmos de ELKI

El algoritmo KNN de ELKI esta desarrollado en java y se puede usar como herramiento de la interfaz de linea de comandos. Para ejecutar los algoritmos en la terminal de un linux se usa el siguiente comando:

```javascript
java -jar elki-bundle-0.7.1.jar KDDCLIApplication -dbc.in mydata/mouse.csv -algorithm clustering.kmeans.KMedoidsEM -kmeans.k 1 -resulthandler ResultWriter -out.gzi -out output/k-1
```
> Aquí se puede descargar el .jar: [elki-bundle-0.7.1.jar](https://elki-project.github.io/releases/release0.7.1/elki-bundle-0.7.1.jar).

El algoritmo que nos interesa usar, de todos los que hay en el framework ELKI, es el KNNOutlier. Ya que Patrick KOSTJENS en su tesis [1] hizo una comparación de los algoritmos y concluyó que este algoritmo tenia el mejor comportamiento. Un ejemplo de como puede ser ejecutado es el siguiente:

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

> Este es el script [KNN.sh](https://github.com/jfernandomarquez/Log-Based-Outlier-Detection-KNN-ELKI-en-Elasticsearch/blob/master/KNN.sh), que sirve, además de ejecutar el algoritmo en el dataset, para mostrar los resultados.

## Establecer los parametros de entrada para el algoritmo KNN

Las entradas para el algoritmo KNN son un numero positivo K y un dataset. Según la bibliografía estudiada los mejores valores para k en el análisis de logs con KNN se encuentran entre 5 y 20, según [1], [4] y [5]  que se pueden encontrar en la [Bibliografía](https://github.com/jfernandomarquez/Log-Based-Outlier-Detection-KNN-ELKI-en-Elasticsearch/blob/master/Bibliografia.md).

Ahora para el dataset se debe indicar que información se necesita. Las anomalias que se quieren detectar en los logs de las aplicaciones son:

* Los acceso exitosos aparece más veces que lo usual
* Acceso exitosos en horarios no laborales
* Los intentos de inicio de sesión fallidos aparece más veces que lo usual.

Para ello se necesita todos los eventos de autenticación (logging in, logging out, failed logins, etc.) que permita detectar ataque por fuerza bruta o intentos de adivinar contraseñas.

> Algunos ejemplos de archivos de logs son: transaction log file, event log file, audit log file, server logs, etc. Syslog messages provide the information by where, when and why, i.e., IP-Address, Timestamp and the log message.

Por lo tanto, se identificaron las siguientes variables que servirán como entrada al algoritmo, junto con el parametro k.

* Año
* Mes
* Dia
* Hora
* Minuto
* Cuenta

Gracias a la ayuda de @PatrickKostjens autor de [1], se pudo trabajar con un generador de datasets artificiales que sirven como entrada para el algoritmos de detección de anomalías, el cual fue utilizado en su tesis para comparar varios algoritmos y concluir que el mejor comportamiento lo daba el algoritmo KNNoutlier.

> **Para tener en cuenta:** también es objeto de monitoreo la modificación de cualquier caracterista de los datos, incluyendo permisos de accesos o etiquetas, localización en bases de datos o sistema de archivos, o propiedad de los datos.

## Generar dataset con información de Elasticsearch para el algoritmo KNNoutlier 

**Procedimiento:**
Consultar cuantas veces un evento en especifico se registró en elasticsearch durante un tiempo determinado, ejemplos: Accesos exitosos, fallo en la autenticación, etc. Luego se almacena la cuenta de eventos(hits) en un archivo de texto plano que sera el dataset, acompañado de información de fecha y hora. Este archivo sera una de las entradas del algoritmo de deteción de anomalias KNNoutlier.

A continuación se muestra un ejemplo de la consulta que se le hace a elasticsearch. Esta consultalos devuelve la cantidad de eventos de acceso exitos en los ultimos 5 minutos:

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

Con el fin de tener los datos de entrada del algoritmo en una forma apropiada para KNNoutlier y hacer la consulta periodicamente, se desarrollo el script [creando_dataset_real_v6.py](https://github.com/jfernandomarquez/Log-Based-Outlier-Detection-KNN-ELKI-en-Elasticsearch/blob/master/creando_dataset_real_v6.py)

> **nota:** Corriendo script colector de datos durante 24 horas, con una tasa de consulta de 5min, se genero un archivo de 10KB.

## Experimento

Arbitrariamente se dice que si la puntuación que da el algoritmo a los datos es mayor a ___ con un k=5,10,20 se le etiquetará como anomalía.

## Resultados Esperados

![Graficas](https://raw.githubusercontent.com/jfernandomarquez/Log-Based-Outlier-Detection-KNN-ELKI-en-Elasticsearch/master/Figuras/grafica_anomalias.jpg)

## Procedimiento para alertar anomalías 

Con el fin de enviar correo con el detalle de la anomalía detectada al personal correspondiente, se debe: identificar la anomalía, almacenar la información sobre la anomalía en *elasticsearch* con un PUT, programar un regla en [sentinl](https://docs.search-guard.com/latest/search-guard-sentinl) (plugin de ELK) para enviar correos cuando al buscar lo que se subió a elasticsearch concida con ciertas condiciones, como se observa [aquí](https://github.com/jfernandomarquez/Log-Based-Outlier-Detection-KNN-ELKI-en-Elasticsearch/blob/master/Configuracion_watchers_sentinl.md) que pueda ser activada cada vez que una posible amenaza sea registrada y gracias esto permita enviar por correo la información del detalle de la amenaza.

*Inspiración:*

[*Anomaly detection rules - IBM*](https://www.ibm.com/support/knowledgecenter/en/SS42VS_7.3.0/com.ibm.qradar.doc/c_qradar_rul_anomaly_detection.html)

## Alertas

### Cantidad anormal de intentos fallidos de inicios de sesión

### Inicios de sesión en horarios fuera de oficina

1. Programar un busqueda en horarios fuera de oficina cada 10 min.
2. Cuando se tenga un usuario diferente a los autorizados enviar una alerta por correo.

### Alertar cuando existan conexiones por VPN en un pais diferente a CO

Utilizar la utilidad de detección de anomalías de sentinl 


> "Is the data the same as yesterday at the same time?"
> "How much does the data change when it compares this minute to the minute before?"


