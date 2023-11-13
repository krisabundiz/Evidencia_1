import openpyxl
import csv
from openpyxl import Workbook
from openpyxl.styles import Font
from datetime import datetime
import re
import os
from prettytable import PrettyTable
import sys
import sqlite3
from sqlite3 import Error
import pandas as pd

def registrar_nota():
    while True:
        print('\n═══════════════════════════════════')
        print('     REGISTRAR UNA NUEVA NOTA')
        print('═══════════════════════════════════')
        monto_total = 0
        servicios_seleccionados = []
        try:
            with sqlite3.connect('/home/kristellabundiz/tallermecanico.db') as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute('SELECT ClaveCliente, nombre FROM clientes WHERE estadoC = 1')
                datos = mi_cursor.fetchall()
                tabla = PrettyTable()
                tabla.field_names = ["CLAVE", "NOMBRE"]
                print('\n    Clientes Registrados')
                for dato in datos:
                    tabla.add_row(dato)
                print(tabla)               
                if not datos:
                    print("NO HAY CLIENTES REGISTRADOS")                
                while True:
                    try:
                        cliente = int(input('\nIngrese la clave del cliente o ingrese "0" para regresar al menú anterior: '))
                        if cliente == 0:
                            print('\n** OPERACIÓN CANCELADA. VOLVIENDO AL MENÚ DE NOTAS **')
                            return
                        else:
                            mi_cursor.execute('SELECT ClaveCliente FROM clientes WHERE estadoC = 1 AND ClaveCliente = ?', (cliente,))
                            cliente_existente = mi_cursor.fetchall()
                            if cliente_existente:
                                break
                            else:
                                print('\n** EL CLIENTE NO ESTÁ REGISTRADO O CORRESPONDE A UN CLIENTE SUSPENDIDO. **')
                        continue
                    except ValueError:
                        print(f'\n** DATO NO VÁLIDO. POR FAVOR, INGRESE UN DATO VÁLIDO. **')
                while True:
                    try:
                        fecha_str = input('\nIngrese la fecha en formato DD/MM/YYYY: ')
                        fecha_actual = datetime.now().date()
                        fecha_ingresada = datetime.strptime(fecha_str, "%d/%m/%Y").date()
                        if fecha_ingresada > fecha_actual:
                            print('\n** LA FECHA INGRESADA NO DEBE SER POSTERIOR A LA FECHA ACTUAL. INGRESE UNA FECHA VÁLIDA **')
                        else:
                            break
                    except Exception:
                        print(f'\n** DATO NO VÁLIDO. POR FAVOR, INGRESE LA FECHA EN EL FORMATO CORRECTO. **')                
                mi_cursor.execute('SELECT ClaveServicio, descripcion, costo FROM servicios WHERE estadoS = 1')
                datos_s = mi_cursor.fetchall()
                tabla = PrettyTable()
                tabla.field_names = ['CLAVE', 'DESCRIPCIÓN', 'COSTO']
                print('\n      Servicios Registrados')
                for dato in datos_s:
                    tabla.add_row(dato)
                print(tabla)
                while True:
                    try:
                        servicio = int(input('\nIngrese la clave del servicio o ingrese "0" para volver al menú anterior: '))
                        if servicio == 0:
                            return
                        mi_cursor.execute('SELECT ClaveServicio, costo FROM servicios WHERE ClaveServicio = ? AND estadoS = 1', (servicio,))
                        servicio_existente = mi_cursor.fetchone()
                        if servicio_existente:
                            monto_total += servicio_existente[1]
                            servicios_seleccionados.append(int(servicio))
                            while True:
                                agregar_otro_servicio = input('\n¿Deseas agregar otro servicio? (S)i (N)o: ')
                                if agregar_otro_servicio.lower() == 's':
                                    break
                                elif agregar_otro_servicio.lower() == 'n':
                                    mi_cursor.execute('INSERT INTO notas (fecha, ClaveCliente, monto, estadoN) VALUES (?, ?, ?, ?)',
                                                      (fecha_ingresada, cliente, monto_total, 1))
                                    id_nota = mi_cursor.lastrowid
                                    for id_servicio in servicios_seleccionados:
                                        valores_detalle = (id_nota, id_servicio)
                                        mi_cursor.execute('INSERT INTO detalle (Folio, ClaveServicio) VALUES (?, ?)', valores_detalle)
                                        print('\n** NOTA(S) REGISTRADA(S) CORRECTAMENTE **')
                                    break
                                else:
                                    print('\n** OPCIÓN NO VÁLIDA. INGRESE (S) PARA SÍ O (N) PARA NO. **')
                            break 
                        else:
                            print('\n** LA CLAVE DE SERVICIO INGRESADA NO ESTÁ REGISTRADA O CORRESPONDE A UN SERVICIO CANCELADO. **')
                            continue
                    except ValueError:
                        print(f'\n** DATO NO VÁLIDO. POR FAVOR, INGRESE UN DATO VÁLIDO. **')
                while True:
                    agregar_otra_nota = input('\n¿Deseas registrar otra nota? (S)i (N)o: ')
                    if agregar_otra_nota.lower() == 'n':
                        return
                    elif agregar_otra_nota.lower() == 's':
                        break
                    else:
                        print('\n** DATO NO VÁLIDO. POR FAVOR, INGRESE (S) PARA CONFIRMAR LA ACCIÓN O (N) PARA CANCELAR LA OPERACIÓN **')
        except Error as e:
            print(e)
        except Exception:
            print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
        finally:
            conn.close()
