import re
import os
import sys
import csv
import sqlite3
from sqlite3 import Error
import openpyxl
from openpyxl import Workbook
from datetime import datetime
from prettytable import PrettyTable

def registrar_nota():
    while True:
        print('\n═══════════════════════════════════')
        print('     REGISTRAR UNA NUEVA NOTA')
        print('═══════════════════════════════════')
        monto_total = 0
        servicios_seleccionados = []
        try:
            with sqlite3.connect('/content/tallermecanico.db') as conn:
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
                        print('\nNota: La fecha debe estar en formato DD/MM/YYYY')
                        fecha_str = input('\nIngrese la fecha o ingrese "0" para volver al menú anterior: ')
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
                            agregar_otro_servicio = input('\n¿Deseas agregar otro servicio? (S)i (N)o: ')
                            if agregar_otro_servicio.lower() == 's':
                                continue
                            elif agregar_otro_servicio.strip() == '':
                                print("ERROR, NO SE PUEDE OMITIR, INGRESE UN DATO VÁLIDO")
                            else:
                                mi_cursor.execute('INSERT INTO notas (fecha, ClaveCliente, monto, estadoN) VALUES (?, ?, ?, ?)',
                                                  (fecha_ingresada, cliente, monto_total, 1))
                                id_nota = mi_cursor.lastrowid
                                for id_servicio in servicios_seleccionados:
                                    valores_detalle = (id_nota, id_servicio)
                                    mi_cursor.execute('INSERT INTO detalle (Folio, ClaveServicio) VALUES (?, ?)', valores_detalle)
                                print('\n** NOTA(S) REGISTRADA(S) CORRECTAMENTE **')
                                break
                        else:
                            print('\n** LA CLAVE DE SERVICIO INGRESADA NO ESTÁ REGISTRADA O CORRESPONDE A UN SERVICIO CANCELADO. **')
                            continue
                    except ValueError:
                        print(f'\n** DATO NO VÁLIDO. POR FAVOR, INGRESE UN DATO VÁLIDO. **')
                while True:
                    agregar_nota = input('\n¿Deseas registrar otra nota? (S)i (N)o: ')
                    if agregar_nota.lower() == 'n':
                        return
                    elif agregar_nota.lower() == 's':
                        break
                    else:
                        print('\n** DATO NO VÁLIDO. POR FAVOR, INGRESE (S) PARA CONFIRMAR LA ACCIÓN O (N) PARA CANCELAR LA OPERACIÓN **')
        except Error as e:
            print(e)
        except Exception:
            print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
        finally:
            conn.close
            
def cancelar_nota():
    while True:
        print('\n════════════════════════════')
        print('     CANCELAR UNA NOTA')
        print('════════════════════════════')
        try:
            with sqlite3.connect('/content/tallermecanico.db') as conn:
                try:
                    folio_cancelar = int(input('\nIngrese el folio de la nota a cancelar o ingrese "0" para volver al menú anterior: '))
                    if folio_cancelar == 0:
                        print('\n** OPERACIÓN CANCELADA. VOLVIENDO AL MENÚ DE NOTAS **')
                        return
                    else:
                        mi_cursor = conn.cursor()
                        mi_cursor.execute('SELECT notas.folio, strftime("%d/%m/%Y", notas.fecha) AS fecha_formateada, clientes.ClaveCliente, clientes.nombre AS nombre_cliente, GROUP_CONCAT(servicios.descripcion, ", ") AS servicios, SUM(servicios.costo) AS costo_total FROM notas INNER JOIN clientes ON notas.ClaveCliente = clientes.ClaveCliente INNER JOIN detalle ON notas.folio = detalle.Folio INNER JOIN servicios ON detalle.ClaveServicio = servicios.ClaveServicio WHERE notas.folio = ? AND notas.estadoN = 1 GROUP BY notas.folio, notas.fecha, clientes.ClaveCliente, clientes.nombre;', (folio_cancelar,))
                        nota_existente = mi_cursor.fetchone()
                        if nota_existente:
                            tabla_detalles = PrettyTable(["Folio", "Fecha", "Clave Cliente", "Nombre Cliente", "Descripción de Servicios", "Costo Total"])
                            tabla_detalles.add_row(nota_existente)
                            print('\n    DETALLES DE LA NOTA')
                            print(tabla_detalles)
                        else:
                            print('\n** ERROR, EL FOLIO INGRESADO NO CORRESPONDE A UNA NOTA ACTIVA **')
                            continue
                except ValueError:
                    print(f'\n** DATO NO VÁLIDO. POR FAVOR, INGRESE UN DATO VÁLIDO. **')
                    continue
                while True:
                    confirmacion = input('\n¿Desea cancelar esta nota? (S)i (N)o: ')
                    if confirmacion.lower() == 's':
                        mi_cursor = conn.cursor()
                        mi_cursor.execute('UPDATE notas SET estadoN = 0 WHERE folio = ?', (folio_cancelar,))
                        print('\n** NOTA CANCELADA CORRECTAMENTE **')
                        break
                    elif confirmacion.lower() == 'n':
                        print('\n** OPERACIÓN CANCELADA **')
                        break
                    else:
                        print('\n** DATO NO VÁLIDO. POR FAVOR, INGRESE (S) PARA CONFIRMAR LA ACCIÓN O (N) PARA CANCELAR LA OPERACIÓN **')
        except Error as e:
            print(e)
        except Exception:
            print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
        finally:
            conn.close()
            
def recuperar_nota():
    while True:
        print('\n════════════════════════════')
        print('    RECUPERAR UNA NOTA')
        print('════════════════════════════')
        try:
            with sqlite3.connect('/content/tallermecanico.db') as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute('SELECT folio FROM notas WHERE estadoN = 0')
                notas_canceladas = [folio[0] for folio in mi_cursor.fetchall()]  
                if not notas_canceladas:
                    print('*  No hay notas canceladas para recuperar *')
                    return
                print('\n** NOTAS PREVIAMENTE CANCELADAS: **')
                print('---------------------------------------')
                prettytable1 = PrettyTable()
                prettytable1.field_names = ["Folio"]
                for folio in notas_canceladas:
                    prettytable1.add_row([folio])
                print(prettytable1)
                while True:
                    try:
                        folio_recuperar = int(input('\nIngrese el folio de la nota a recuperar o ingrese "0" para regresar al menú anterior: '))
                        if folio_recuperar == 0:
                            print('\n** OPERACIÓN CANCELADA. VOLVIENDO AL MENÚ DE NOTAS **')
                            return
                        elif folio_recuperar in notas_canceladas:
                            mi_cursor.execute('SELECT notas.folio, strftime("%d/%m/%Y", notas.fecha) AS fecha_formateada, clientes.ClaveCliente, clientes.nombre AS nombre_cliente, GROUP_CONCAT(servicios.descripcion, ", ") AS servicios, SUM(servicios.costo) AS costo_total FROM notas INNER JOIN clientes ON notas.ClaveCliente = clientes.ClaveCliente INNER JOIN detalle ON notas.folio = detalle.Folio INNER JOIN servicios ON detalle.ClaveServicio = servicios.ClaveServicio WHERE notas.folio = ? AND notas.estadoN = 0 GROUP BY notas.folio, notas.fecha, clientes.ClaveCliente, clientes.nombre;', (folio_recuperar,))
                            detalle_nota = mi_cursor.fetchone()
                            tabla_detalles = PrettyTable(["Folio", "Fecha", "Clave Cliente", "Nombre Cliente", "Descripción de Servicios", "Costo Total"])
                            tabla_detalles.add_row(detalle_nota)
                            print('\n    DETALLES DE LA NOTA A RECUPERAR')
                            print(tabla_detalles)
                            while True:
                                confirmacion = input('\n¿Desea recuperar esta nota? (S)i (N)o: ')
                                if confirmacion.lower() == 's':
                                    mi_cursor.execute('UPDATE notas SET estadoN = 1 WHERE folio = ?', (folio_recuperar,))
                                    print(f'\n** Nota {folio_recuperar} recuperada **')
                                    break
                                elif confirmacion.lower() == 'n':
                                    print('\n** OPERACION CANCELADA **')
                                    break
                                else:
                                    print('\n** DATO NO VÁLIDO. POR FAVOR, INGRESE (S) PARA CONFIRMAR LA ACCIÓN O (N) PARA CANCELAR LA OPERACIÓN **')
                                    continue
                        else:
                            print('\n** El FOLIO INGRESADO NO CORRESPONDE A UNA NOTA CANCELADA **')
                    except ValueError:
                        print(f'\n** DATO NO VÁLIDO. POR FAVOR, INGRESE UN DATO VÁLIDO. **')
        except Error as e:
            print(e)
        except Exception:
            print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
        finally:
            conn.close()

def consultas_reportes_notas():
    while True:
        print('\n═══════════════════════════════════')
        print('    CONSULTAS Y REPORTES NOTAS')
        print('═══════════════════════════════════')
        print('1. Consulta por período')
        print('2. Consulta por folio')
        print('3. Volver al menú notas')
        try:
            consulta = int(input('\nIngresa el número de la operación que desea realizar: '))
            if 1 <= consulta <= 3:
                if consulta == 1:
                    try:
                        with sqlite3.connect('/content/tallermecanico.db') as conn:
                            mi_cursor = conn.cursor()
                            fecha_inicial_str = input('\nIngrese la fecha inicial (DD/MM/YYYY) o presione Enter para usar fecha dada por el sistema (01/01/2000): ')
                            if fecha_inicial_str == '':
                                fecha_inicial = datetime(2000, 1, 1).date()
                            else:
                                try:
                                    fecha_inicial = datetime.strptime(fecha_inicial_str, "%d/%m/%Y").date()
                                except ValueError:
                                    print('\n** FORMATO DE FECHA INVÁLIDO. Intente de nuevo. **')
                                    continue
                            while True:
                                fecha_final_str = input('\nIngrese la fecha final (DD/MM/YYYY) o presione Enter para usar la fecha actual: ')
                                if fecha_final_str == '':
                                    fecha_final = datetime.today().date()
                                else:
                                    try:
                                        fecha_final = datetime.strptime(fecha_final_str, "%d/%m/%Y").date()
                                    except ValueError:
                                        print('\n** FORMATO DE FECHA INVÁLIDO. Intente de nuevo. **')
                                        continue
                                if fecha_final < fecha_inicial:
                                    print('\n** LA FECHA FINAL DEBE SER MAYOR O IGUAL QUE LA FECHA ACTUAL. **')
                                    continue
                                else:
                                    break
                            mi_cursor.execute('SELECT folio, fecha, ClaveCliente FROM notas WHERE fecha BETWEEN ? AND ?;', (fecha_inicial, fecha_final))
                            registros = mi_cursor.fetchall()
                            if registros:
                                mi_cursor.execute('SELECT folio, fecha, ClaveCliente, monto FROM notas WHERE estadoN = True')
                                datos = mi_cursor.fetchall()
                                tabla = PrettyTable()
                                tabla.field_names = ['FOLIO', 'FECHA', 'CLAVE CLIENTE', 'MONTO']
                                print('')
                                for dato in datos:
                                    fecha_datetime = datetime.strptime(dato[1], "%Y-%m-%d")
                                    fecha_formateada = fecha_datetime.strftime("%d/%m/%Y")
                                    tabla.add_row([dato[0], fecha_formateada, dato[2], dato[3]])
                                print(tabla)
                                print('\n---------------------------------------')
                                print('           EXPORTAR REPORTE')
                                print('---------------------------------------')
                                print('1. Exportar reporte como archivo EXCEL')
                                print('2. Exportar reporte como archivo CSV')
                                print('3. Volver al menú consultas y reportes')
                                exportar = int(input('\nIngresa el número de la operación que deseas realizar: '))
                                encabezados = ['FOLIO', 'FECHA', 'CLAVE CLIENTE', 'MONTO']
                                if exportar == 1:
                                    nombre_excel = f'ReportePorPeriodo_{fecha_inicial}_{fecha_final}.xlsx'
                                    wb = Workbook()
                                    hoja = wb.active
                                    hoja.append(encabezados)
                                    for dato in datos:
                                        hoja.append(dato)
                                    wb.save(nombre_excel)
                                    print(f'\nInforme {nombre_excel} exportado correctamente')
                                elif exportar == 2:
                                    nombre_csv = f'ReportePorPeriodo_{fecha_inicial}_{fecha_final}.csv'
                                    with open(nombre_csv, 'w', newline='') as reporte_csv:
                                        grabador = csv.writer(reporte_csv)
                                        grabador.writerow(encabezados)
                                        grabador.writerows(datos)
                                    print(f'\nInforme {nombre_csv} exportado correctamente')
                                elif exportar == 3:
                                    continue
                            else:
                                print(f'\n** NO HAY NOTAS EMITIDAS EN EL PERIODO {fecha_inicial} A {fecha_final} **')
                    except sqlite3.Error as e:
                        print(e)
                    except Exception:
                        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
                    finally:
                        conn.close()
                elif consulta == 2:
                    try:
                        with sqlite3.connect('/content/tallermecanico.db') as conn:
                            conn.row_factory = sqlite3.Row
                            mi_cursor = conn.cursor()
                            mi_cursor.execute('SELECT n.folio, n.fecha, c.nombre FROM notas n, clientes c WHERE n.ClaveCliente = c.ClaveCliente ORDER BY n.folio')
                            datos = mi_cursor.fetchall()
                            tabla = PrettyTable()
                            tabla.field_names = ['FOLIO', 'FECHA', 'NOMBRE CLIENTE']
                            print('')
                            for dato in datos:
                                tabla.add_row(dato)
                            print(tabla)
                            while True:
                                clave_consultar = input('\nIngrese el folio de la nota que desea consultar o ingrese "0" para volver): ')
                                if clave_consultar == '0':
                                    break
                                datos = {'folio': int(clave_consultar)}
                                mi_cursor.execute('''SELECT notas.folio,
                                               notas.fecha,
                                               clientes.ClaveCliente,
                                               clientes.nombre,
                                               clientes.correo,
                                               clientes.rfc,
                                               GROUP_CONCAT(servicios.descripcion || ' - $' || CAST(servicios.costo AS TEXT), '\n') as descripcion_costo,
                                               SUM(servicios.costo)
                                            FROM notas
                                            INNER JOIN clientes ON notas.ClaveCliente = clientes.ClaveCliente
                                            INNER JOIN detalle ON notas.folio = detalle.Folio
                                            INNER JOIN servicios ON detalle.ClaveServicio = servicios.ClaveServicio
                                            WHERE notas.folio = :folio AND notas.estadoN = True
                                            GROUP BY notas.folio, notas.fecha, clientes.ClaveCliente, clientes.nombre;''', datos)
                                registro = mi_cursor.fetchall()
                                if registro:
                                    nueva_tabla = PrettyTable()
                                    nueva_tabla.field_names = ["Folio", "Fecha", "Clave Cliente", "Nombre Cliente", "Correo Cliente", "RFC cliente", "Descripción de Servicios", "Costo Total"]
                                    print('')
                                    for fila in registro:
                                        nueva_tabla.add_row(fila)
                                    print(nueva_tabla)
                                else:
                                    print(f'\n** LA NOTA ASOCIADA AL FOLIO {clave_consultar} NO HA SIDO ENCONTRADA O SE ENCUENTRA CANCELADA. POR FAVOR, VERIFICA LA INFORMACIÓN E INTENTA NUEVAMENTE. **')
                    except Error as e:
                        print(e)
                    except Exception:
                        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
                    finally:
                        conn.close()
                elif consulta == 3:
                    print('\n** OPERACIÓN CANCELADA. VOLVIENDO AL MENÚ DE NOTAS **')
                    return
            else:
                raise ValueError
        except ValueError:
            print('\n** DATO NO VÁLIDO. INGRESE EL NÚMERO DE ALGUNA OPCIÓN MOSTRADA **')

def menu_notas():
    while True:
        print('\n---------------------------------------')
        print('      BIENVENIDO AL MENU DE NOTAS   ')
        print('---------------------------------------')
        print('1. Registrar una nota')
        print('2. Cancelar una nota')
        print('3. Recuperar una nota')
        print('4. Consultas y reportes')
        print('5. Salir')
        opcion = input('\nIngrese el número de la opción a la que desea ingresar: ')
        if opcion.isdigit():
            opcion = int(opcion)
            if opcion == 1:
                registrar_nota()
            elif opcion == 2:
                cancelar_nota()
            elif opcion == 3:
                recuperar_nota()
            elif opcion == 4:
                consultas_reportes_notas()
            elif opcion == 5:
              menu_principal()
            else:
                print('\nERROR, POR FAVOR INGRESE UNA OPCIÓN VÁLIDA.')
        else:
            print('\nERROR, POR FAVOR INGRESE UNA OPCIÓN VÁLIDA.')
