import time  # Importaciones
import unittest
from unittest.mock import MagicMock, patch
import os
import pandas as pd
import xml.etree.ElementTree as ET

from XML_A_CSV import LeerXml  # Importamos la clase que vamos a probar


class TestLeerXml(unittest.TestCase):  # Definición de la clase de prueba

    def setUp(self):  # Método de configuración que se ejecuta antes de cada prueba
        self.leer_xml = LeerXml()  # Creamos una instancia de la clase a probar
# -------------------------------------------------------------------------------------------------------------------------------

    def test_tearDown(self):
        # Eliminar archivos de las carpetas después de cada prueba
        for folder in ['XML_ENTRADA', 'XML_PROCESADOS', 'RESULTADOS']:
            files = os.listdir(folder)
            for file in files:
                if file.startswith('test_') and (file.endswith('.xml') or file.endswith('.csv')):
                    os.remove(os.path.join(folder, file))

# ---------------------------------------------------------------------------------------------------------------------------------
    def test_list_archivos(self):
        test_xml = '''
        <BillDeterminantData xmlns="SAMSettlementDataOutput_v502.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="SAMSettlementDataOutput_v502.xsd">
            <MessageHeader>
                <TimeDate></TimeDate>
                <Source></Source>
                <JobMRID></JobMRID>
            </MessageHeader>
            <MessagePayload>
                <BillDeterminant name="test" mrid="1" dataType="test_type" lastModified="2022-04-04" settlementVer="v1.0" dataSource="source" uom="kg" calcLevel="high" precisionLevel="medium" configVer="v2.0" tradeDateBegin="2022-01-01" tradeDateEnd="2022-01-31" effectiveDate="2022-01-01" terminationDate="2022-12-31" intervalCount="10">
                    <Attribute name="attribute_name" value="attribute_value" seq="1"/>
                    <Data int="6" val="10"/>
                </BillDeterminant>
            </MessagePayload>
        </BillDeterminantData>
        '''

        # Creamos un archivo de prueba en la carpeta XML_ENTRADA
        with open(os.path.join(self.leer_xml.in_path, 'test_list_archivos.xml'), 'w') as f:
            f.write(test_xml)

        # Configuración del objeto mockeado
        self.leer_xml.msg = MagicMock()
        self.leer_xml.procesar_xml = MagicMock()

        # Ejecutamos el método que queremos probar
        self.leer_xml.list_archivos()

        # Verificamos si el archivo creado está en la carpeta de entrada (XML_ENTRADA)
        files = os.listdir(self.leer_xml.in_path)
        self.assertIn('test_list_archivos.xml', files)

# -------------------------------------------------------------------------------------------------------
    def test_procesar_xml(self):

        test_xml = '''
        <BillDeterminantData xmlns="SAMSettlementDataOutput_v502.xsd" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="SAMSettlementDataOutput_v502.xsd">
            <MessageHeader>
                <TimeDate></TimeDate>
                <Source></Source>
                <JobMRID></JobMRID>
            </MessageHeader>
            <MessagePayload>
                <BillDeterminant name="test" mrid="1" dataType="test_type" lastModified="2022-04-04" settlementVer="v1.0" dataSource="source" uom="kg" calcLevel="high" precisionLevel="medium" configVer="v2.0" tradeDateBegin="2022-01-01" tradeDateEnd="2022-01-31" effectiveDate="2022-01-01" terminationDate="2022-12-31" intervalCount="10">
                    <Attribute name="attribute_name" value="attribute_value" seq="1"/>
                    <Data int="6" val="10"/>
                </BillDeterminant>
            </MessagePayload>
        </BillDeterminantData>
        '''
        # Método de prueba para la función que procesa archivos XML

        # Ruta del archivo de prueba en la carpeta XML_ENTRADA
        archivo = 'test_procesar_xml.xml'
        test_file_path = os.path.join(self.leer_xml.in_path, archivo)

        # Creamos un archivo de prueba en la carpeta XML_ENTRADA
        with open(test_file_path, 'w') as f:
            f.write(test_xml)

        # Verificamos que el archivo se ha creado correctamente
        self.assertTrue(os.path.isfile(test_file_path))

        # Ejecutamos el método para procesar XML
        self.leer_xml.procesar_xml(archivo)

        # Verificamos que el archivo de entrada ya no existe
        self.assertFalse(os.path.isfile(test_file_path))

        # Verificamos que el archivo procesado sí existe en la carpeta de salida (XML_PROCESADOS)
        processed_file_path = os.path.join(self.leer_xml.out_path, archivo)
        self.assertTrue(os.path.isfile(processed_file_path))

        # Verificamos que se haya creado un archivo CSV correspondiente en la carpeta de resultados
        files_csv = os.listdir(self.leer_xml.result_path)
        self.assertIn('test_procesar_xml.csv', files_csv)

# ----------------------------------------------------------------------------------------------------
    def test_extraer_fila(self):
        # Obtener una instancia del objeto para leer XML
        obj = self.leer_xml

        # Crear un elemento XML llamado 'BillDeterminant' con una serie de atributos
        registro = ET.Element('BillDeterminant')
        registro.set('name', 'test')
        registro.set('mrid', '1')
        registro.set('dataType', 'test_type')
        registro.set('lastModified', '2022-04-04')
        registro.set('settlementVer', 'v1.0')
        registro.set('dataSource', 'source')
        registro.set('uom', 'kg')
        registro.set('calcLevel', 'high')
        registro.set('precisionLevel', 'medium')
        registro.set('configVer', 'v2.0')
        registro.set('tradeDateBegin', '2022-01-01')
        registro.set('tradeDateEnd', '2022-01-31')
        registro.set('effectiveDate', '2022-01-01')
        registro.set('terminationDate', '2022-12-31')
        registro.set('intervalCount', '10')

        # Añadir subelementos 'Attribute' y 'Data' con sus atributos correspondientes
        attribute_child = ET.SubElement(
            registro, '{SAMSettlementDataOutput_v502.xsd}Attribute')
        attribute_child.set('name', 'attribute_name')
        attribute_child.set('value', 'attribute_value')
        attribute_child.set('seq', '1')

        data_child = ET.SubElement(
            registro, '{SAMSettlementDataOutput_v502.xsd}Data')
        data_child.set('int', '6')
        data_child.set('val', '10')

        # Escribir el elemento XML en un archivo para simular un archivo de entrada
        with open(os.path.join(self.leer_xml.in_path, 'test_extraer_fila.xml'), 'wb') as f:
            f.write(ET.tostring(registro))

        # Llamar al método extraer_fila  para procesar el XML y obtener el resultado
        result = obj.extraer_fila(registro)

        # Verificar que el resultado sea el esperado
        self.assertEqual(result['name'], 'test')
        self.assertEqual(result['mrid'], '1')
        self.assertEqual(result['dataType'], 'test_type')
        self.assertEqual(result['lastModified'], '2022-04-04')
        self.assertEqual(result['settlementVer'], 'v1.0')
        self.assertEqual(result['dataSource'], 'source')
        self.assertEqual(result['uom'], 'kg')
        self.assertEqual(result['calcLevel'], 'high')
        self.assertEqual(result['precisionLevel'], 'medium')
        self.assertEqual(result['configVer'], 'v2.0')
        self.assertEqual(result['tradeDateBegin'], '2022-01-01')
        self.assertEqual(result['tradeDateEnd'], '2022-01-31')
        self.assertEqual(result['effectiveDate'], '2022-01-01')
        self.assertEqual(result['terminationDate'], '2022-12-31')
        self.assertEqual(result['intervalCount'], '10')
        self.assertEqual(result['attribute_name'], 'attribute_value')
        self.assertEqual(result['6'], '10')

    # Método de prueba para la función que guarda un DataFrame en un archivo
    def test_guardar(self):
        # Creamos un DataFrame de prueba
        data = {'name': ['test'], 'mrid': ['1'], 'dataType': ['test_type'], 'lastModified': ['2022-04-04'], 'settlementVer': ['v1.0'],
                'dataSource': ['source'], 'uom': ['kg'], 'calcLevel': ['high'], 'precisionLevel': ['medium'],
                'configVer': ['v2.0'], 'tradeDateBegin': ['2022-01-01'], 'tradeDateEnd': ['2022-01-31'], 'effectiveDate': ['2022-01-01'], 'terminationDate': ['2022-12-31'],
                'intervalCount': ['10']}
        df = pd.DataFrame(data)
        # Ejecutamos la función para guardar el DataFrame
        self.leer_xml.guardar(df, 'test_guardar.xml')


if __name__ == '__main__':
    unittest.main()  # Ejecutamos las pruebas si este script es ejecutado directamente
