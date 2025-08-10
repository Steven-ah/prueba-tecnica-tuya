# Prueba técnica tuya

Repositorio que almacena toda la información y explicación de la solución brindada a la prueba ténica. Realizado por Steven Alvarez Holguín.

## Punto 1

Para este caso, lo que se plantea es que se tienen multiples fuentes de datos, como se puede ver en el diagrama.

![Diagrama del proceso](<Ejercicio-1 y 2/diagrama_proceso.svg>)

Mediante herramientas de procesado de datos, Databricks como se propone en este caso, permitiría la creación de notebooks de tipo jupiter en los que, mediante Python, SQL o R, pueden realizarse la consulta y consolidación de la información. Para posteriomente dejarla disponible en un repositorio, en este caso un data lake; para que los usuarios puedan consultarla los datos desde allí. Ya sea, mediante la creación de un informe, creado con herramientas como power bi, o que tomen los datos directamente desde el datalake.

Para la implementación de esto, se plantea la creación de una carpeta de de GIT en Databricks, esta carpeta permitiría que toda la información tenga el control de versiones y hacer uso de CI/CD mediante la herramienta pertinente, ya sea Azure DevOps, GitHub Actions, etc. El esquema de la implemantación sería el propuesto por el diagrama

![proceso detallado](<Ejercicio-1 y 2/explicacion_proceso.svg>)

En el que tenemos las 3 fases. En una primera fase (bronze), se cargaría la información tal cuál como llega de la fuente. Ya que el objetivo allí es tener los datos base del proceso. Posteriomente en silver, se realizaría todo el proceso de limpieza por cada fuente, es decir, se estándarizan datos para que tengan las mismas columnas, mismo tipo de datos y por ultimo se haría la unificación de los telefonos, para posteriormente retirar los datos duplicados de manera global.

Por ultimo, en la fase de gold, se realizan todos los calculos que se consideren necesarios en base a las reglas que brinde el negocio para todo el manejo de estos datos. Reglas como el qué hacer cuando un mismo cliente tenga multiples números, un caso en que un número pertenezca a varios clientes, etc.

## Punto 2

Para poder realizar todo el proceso de veeduría de la información de los telefonos del cliente, lo que se puede hacer es la creación de un informe en el que se consulten dos componentes del dataset. Allí, lo que se haría es tomar dos elementos del dataset previamente creado. Un primer elemento es la tabla de silver que contiene el detalle de todos los telefonos para todos los clientes y el segundo sería la tabla de gold que tiene el detalle ajustado según las reglas del negocio. De esta manera se construiría un informe que permitiría tener la visual de cuantos clientes tienen inconsistencias, qué clientes son y cuales son los números inconsistentes para que el area encargada se dedique a la revisión y ajuste de estos elementos. Además, de ser necesario, pueden generarse alertas en base a KPIs indicados para asegurar que cuando se supere un umbral específico se alerte a las personas para que tengan el seguimiento de esto.

## Punto 3

Este ejercicio se encuentra solucionado sobre la carpeta [Ejercicio 3](https://github.com/Steven-ah/prueba-tecnica-tuya/tree/main/Ejercicio-3) en la que encontrarán varios archivos.

- load_data_postgresql.py: Es un archivo en python que usé para cargar la información sobre la base de datos. Realicé la carga de esta manera para así asegurar que se está cargando toda la información sobre la base de datos, además de evitar errores con los tipos de datos.

- prueba-tecnica-tuya-bkp.sql: Contiene todos los scripts para la creación de la base de datos e inserción de la información allí cargada.

- ejercicio-3-tuya.sql: Contiene el script SQL con el que se le da solución al tercer punto de la prueba técnica.

> Para asegurar tener todos los datos es ideal cargar el script de creación con la información, o en caso tal, mediante el archivo xlsx de rachas alojado en la carpeta de data y el script load_data_postgresql.py se puede realizar la carga de la información. Es importante que si se usa el script de python para cargar los datos, se instalen las librerías del archivo "requirements.txt"

Respecto a la construcción de la base de datos y la solución del problema:

1. Se crea una tabla extra con fechas para que, mediante esta puedan obtenerse los intervalos de tiempo que no se tienen en la tabla de historia brindada.

    Además, se mantienen los tipos de datos en base a lo que fue brindado en el archivo HTML para mantener consistencia. Ya que, en un escenario real, la columna de saldo debería de ser de tipo numeric o decimal para mantener precisión decimal en los valores.

2. La consulta SQL se basa en multiples fases con una pequeña descripción en el código. Cada fase se encarga de brindar los elementos necesarios para dar solución. 

    2.1 Una primera fase obtiene los intervalos en los que un cliente estuvo activo en base a las fechas brindadas.

    2.2 Llena los espacios vacios en ese intervalo, es decir, agrega todos los meses en base al intervalo brindado valiendose de la tabla de fechas.

    2.3 la generación de la columna de nivel para la categorizacion de los saldos.

    2.4 El analisis de rachas mediante la función lag para verificar qué nivel tenía el cliente en un periodo anterior, marcando con 0 aquellos que tienen racha y 1 aquellos que no.

    2.5 La suma de los valores de la racha, para generar grupos por cada racha (cada racha nueva aumenta en uno, por lo que aquellos que tienen racha se mantienen estáticos, por eso se les asigna 0 a las rachas).

    2.6 Se resumen las rachas, contando y agrupando por los grupos (se suma 1 en la cantidad de la racha debido a que el primer mes de la racha es descartado con el filtro racha = 0).

    2.7 Obtenemos racha máxima por cliente y nivel.

    2.8 Se muestra solo la información de las rachas máximas.

Para el filtrado basta con aplicar los filtros como se muestra al final de la consulta luego de haber creado el filtro.

## Punto 4

Este ejercicio se encuentra solucionado sobre la carpeta [Ejercicio 4](https://github.com/Steven-ah/prueba-tecnica-tuya/tree/main/Ejercicio-4) en la que encontrarán varios archivos.

- HTMLImageEncoder.py: Contiene toda la lógica para la lectura y creación de los nuevos archivos en .html

- EncondeImageToBase64.py: Contiene toda la lógica para la codificación de las imagenes en base 64.

- ejercicio-3-tuya.py: Este archivo funciona como desencadenador del proceso, básicamente un main.py

Se debe de tener en cuenta de que el ejercicio se realizó con multiples archivos HTML y se identifica que, para muchos casos depende mucho de cómo esté definida la estructura para la carga de la imgen. Ya que para páginas como Wikipedia, las imagenes se cargan mediante una etiqueta img, pero en su componente src no contiene la URL completa de la imagen sino que está en otro apartado.

Además de que aquellas url que no provengan de una ruta HTTPS de internet se descartan ya que al no poder tomar la imagen, se generará un error de carga de datos e inflaría el total de imagenes fallidas cuando ni se realizó el intento de codificación.

@SAH