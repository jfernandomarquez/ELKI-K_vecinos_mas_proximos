# Configuración de watchers en sentinl

Sentinl permite enviar correos electronicos en los cuales se pueden incluir datos de los eventos que se consultan con el Query y que además cumplieron cierta condición.

## Entradas de watcher

### Input

Aqui se realiza la consulta a elasticsearch que van a hacer de datos de entrada.

Ejemplo:

```json
{
  "search": {
    "request": {
      "index": [
        "logstash-*"
      ],
      "body": {
        "size": 0,
        "query": {
          "match_all": {}
        }
      }
    }
  }
}
```
### Condition

La condicion es la que determina cuando se debe activar la acción.

Ejemplo:
```json
{
  "script": {
    "script": "payload.hits.total > 0"
  }
}
```
### Action

La acción es lo que se realizara en caso de que se cumpla la condición. Para este caso en particula se utilza como acción un *email html* para poder personalizar el cuerpo de correo que se enviará para alertar.

Ejemplo:

``` html

<h1 style="color:#c00000;font-family:calibri;font-size:28px;text-align:center;">Anomalía Detectada</h1><pre style="color:#21356a;font-family::calibri;font-size:14px">Se tuvo un total de {{payload.hits.total}} eventos, esto prodría indicar que se esta generando un ataque.

<b style="color:#21356a;font-family:calibri;font-size:18px%">Detalles:</b>

 payload.hits.object: {{payload.hits.object}}

<b style="color:#21356a;font-family:calibri;font-size:14px">
Nombre</b>
<div style="color:gray;font-family:calibri;font-size:11px">Área propia
<b>Área de la que depende</b><hr><pre style="color:gray;font-family:calibri;font-size:9px">
Dirección: 
Código Postal: 
Ciudad – País
</pre>
```
Se puede observar como se queda el correo recibido [aquí](https://www.w3schools.com/code/tryit.asp?filename=FS33JZY259P1), se le debe dar al boton verde run.

