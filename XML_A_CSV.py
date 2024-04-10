# -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 08:59:53 2024

@author: 50682
"""

import numpy as np
import pandas as pd
from datetime import datetime
import xml.etree.ElementTree as ET
import shutil
import os


class LeerXml(object):

    def __init__(self):
        self.abs_path = os.getcwd()
        self.in_path = os.path.join(self.abs_path, 'XML_ENTRADA')
        self.out_path = os.path.join(self.abs_path, 'XML_PROCESADOS')
        self.result_path = os.path.join(self.abs_path, 'RESULTADOS')
        self.xml_actual = ''

    def list_archivos(self):
        """
        Revisa los XML disponibles en la Carpeta XML_entrada y los lista, para
        transformarlos a CSV

        :return: None
        :rtype: TYPE
        """
        self.msg('Inicia Lectura de Archivos')
        lista = [file for file in os.listdir(
            self.in_path) if file.endswith('.xml')]
        if len(lista) == 0:
            self.msg('No se encontraron XML a procesar')
        else:
            self.msg('Procesando XML ... ')
            for file in lista:
                self.procesar_xml(file)

    def procesar_xml(self, nombre):
        """
        Dado el nombre de un XML, este método lee el archivo, extrae su raiz
        XML y recorre cada Billdeterminant.

        :param nombre: Nombre de un archivo XML
        :type nombre: STR
        :return: None
        :rtype: TYPE

        """

        file_path = os.path.join(self.in_path, str(nombre))
        self.xml_actual = file_path
        tree = ET.parse(file_path)
        root = tree.getroot()
        lista_datos = []
        for bill_determinant in root.findall(
                './/{SAMSettlementDataOutput_v502.xsd}BillDeterminant'):
            data = self.extraer_fila(bill_determinant)
            lista_datos.append(data)
        df = pd.DataFrame(lista_datos)
        # Eliminar Columnas Vacías
        df = df.replace(" ", np.nan)
        df = df.dropna(axis=1, how='all')

        self.guardar(df, nombre)

    def extraer_fila(self, registro):
        """
        Cada Billdeterminat representa una fila, este método recorre un
        Billdeterminat y extrae sus atributos en un diccionario llamado data.

        :param registro: Registro de XML
        :type registro: Objeto ET
        :return: Data
        :rtype: dict

        """
        data = {'name': " ", 'mrid':  " ", 'dataType':  " ", 'lastModified':  " ",
                'settlementVer':  " ", 'dataSource':  " ", 'uom':  " ",
                'calcLevel':  " ", 'precisionLevel':  " ", 'configVer':  " ",
                'tradeDateBegin':  " ", 'tradeDateEnd': " ",
                'effectiveDate':  " ", 'terminationDate':  " ",
                'intervalCount':  " ", 'PM_ID': " ", 'PM_TIPO': " ",
                'PM_SUBTIPO': " ", 'CP_TIPO': " ", 'FRONTERA': " ",
                'FRONTERA_TIPO': " ", 'FRONTERA_SUBTIPO': " ",
                'FRONTERA_SUBSUBTIPO': " ", 'FRONTERA_EMBEBIDA': " ",
                'FRONTERA_ESTADO': " ", 'RECURSO': " ", 'RECURSO_TIPO': " ",
                'RECURSO_SUBTIPO': " ", 'COMBUSTIBLE_TIPO': " ",
                'RECURSO_EMBEBIDO': " ", 'SUBMERCADO': " ",
                'SUBMERCADO_TIPO': " ", 'SUBMERCADO_SUBTIPO': " ",
                'MERCADO': " ", 'MERCADO_TIPO': " ", 'TIPO_DESPACHO': " ",
                'NIVEL_TENSION': " ", 'TIPO_GENERICO': " ",
                'ESTADO_GENERICO': " ", 'DIRECTION_GENERICO': " ",
                'CONTRATO_ID': " ", 'CONTRATO_TIPO': " ",
                'CONTRATO_SUBTIPO': " ", 'CONTRATO_SUBSUBTIPO': " ",
                'SUBASTA_ID': " ", 'PM_CP_ID': " ", 'RECURSO_ESTADO': " ",
                'CONFIGURACION': " ", 'SISTEMA_TRANSMISION': " ",
                'LOCATION': " ", 'ORDEN_GENERICO': " ", 'PM_CP_SUBTIPO': " ",
                'EVENTO_ID': " ", 'GRUPO_GENERICO': " ", 'Economic_link': " ",
                'IMPORTANCIA_COMB': " ", 'KEY42': " ", 'KEY43': " ",
                'KEY44': " ", 'KEY45': " ", 'DUE_DATE': " ",
                'TRADE_DATE_BEGIN': " ", 'TRADE_DATE_END': " ",
                'TIPO_DIA': " ", 'KEY50': " "
                }

        try:

            data['name'] = registro.get('name')
            data['mrid'] = registro.get('mrid')
            data['dataType'] = registro.get('dataType')
            data['lastModified'] = registro.get('lastModified')
            data['settlementVer'] = registro.get('settlementVer')
            data['dataSource'] = registro.get('dataSource')
            data['uom'] = registro.get('uom')
            data['calcLevel'] = registro.get('calcLevel')
            data['precisionLevel'] = registro.get('precisionLevel')
            data['configVer'] = registro.get('configVer')
            data['tradeDateBegin'] = registro.get('tradeDateBegin')
            data['tradeDateEnd'] = registro.get('tradeDateEnd')
            data['effectiveDate'] = registro.get('effectiveDate')
            data['terminationDate'] = registro.get('terminationDate')
            data['intervalCount'] = registro.get('intervalCount')

            for child in registro:
                if child.tag == '{SAMSettlementDataOutput_v502.xsd}Attribute':
                    data[child.get('name')] = child.get('value')
                elif child.tag == '{SAMSettlementDataOutput_v502.xsd}Data':
                    data[child.get('int')] = child.get('val')
            return data
        except Exception as e:
            self.msg(
                'Error  Extrayendo los registros, posible error en XML: '
                + str(e))

    def guardar(self, df, nombre):
        """
        Este método convierte la lista de datos en un Data Frame, lo guarda
        como un archivo CSV, y por último, mueve el XML a la carpeta de
        XML_PROCESADOS.

        :param df: Datos extraidos de XML
        :type df: DataFrame
        :param nombre: Nombre del XML
        :type nombre: str
        :return: None
        :rtype: TYPE

        """

        nombre_csv = nombre[:-4] + '.csv'
        save_path = os.path.join(self.result_path, nombre_csv)
        df.to_csv(save_path, sep=",", index=False)
        try:
            shutil.move(self.xml_actual, self.out_path)
        except Exception as e:
            self.msg('Fallo al mover Archivo. \n\n Error: \n'+str(e))

    def msg(self, m):
        """
        Escribe un mensaje espaciado en consola.

        :param m: Mensaje a Publciar.
        :type m: STR
        :return: None
        :rtype: TYPE

        """

        print("-----------------------------------------------\n", m, '\n')


if __name__ == "__main__":
    t1 = datetime.now()
    obj = LeerXml()
    obj.list_archivos()
    t2 = datetime.now()
    t = t2 - t1
    print('Tiempo ejecución Total', t)
