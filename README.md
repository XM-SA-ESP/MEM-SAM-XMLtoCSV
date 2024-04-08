# Propósito:
El conversor de XML a CSV es una solución útil para quienes que necesitan transformar datos estructurados en XML en un formato de tabla como el CSV (Comma Separated Values).
En el XML es complejo realizar búsquedas con múltiples filtros, por el contrario, al cargar un CSV en Excel, se pueden realizar análisis y procesamiento de datos de forma más eficiente.

# Funcionalidades
- Listar los archivos XML: Verifica la carpeta XML_ENTRADA y lista los nombres de los archivos que tengan extensión .XML
- Extraer Información del XML: Recorre la estructura de árbol definida para el XML, extrae los nombres y los valores de interés y los convierte en una fila.  Cada registro del XML se transforma de una fila de una tabla que termina en un DataFrame.
- Guardar Resultados: Guarda el DataFrame de datos en formato CSV. Posteriormente, mueve el XML de la carpeta XML_ENTRADA a XML_PROCESADOS.

# Forma de uso:
- El programa esta diseñado para ser ejecutado únicamente pegando los XML a procesar, en la carpeta XML_ENTRADA, posteriormente se ejecuta el Python XML_A_CSV.py y se espera que termine para visualizar los resultados en la carpeta RESULTADOS. 
- El CSV de salida queda con el mismo nombre del XML entrada, excepto por el cambio de formato.
- El programa ha sido validado y funciona correctamente para transformar los XML a los que fue diseñado. Es importante considerar la configuración regional o el separador decimal en el equipo de cómputo para evitar pérdida de datos o lecturas erróneas del archivo CSV y sus decimales.

# Instalación:
Es una carpeta portable, solo se requiere descargar y ejecutar el archivo XML_A_CSV.py en un ambiente de Python.
Librerías necesarias:
- numpy 
-	pandas 
-	datetime
-	xml.etree.ElementTre
-	shutil
-	os
Versiones Recomendadas:
- conda conda 4.14.0
- Python 3.9.18
- ipython kernel –version  8.15.0
- pandas Version: 1.3.4

