import datetime

notas = {}
notas_canceladas = []

def validar_entero(mensaje):
    while True:
        try:
            numero = int(input(mensaje))
            return numero
        except ValueError:
            print("Por favor, ingrese un número válido.")

def registrar_notas():
    print('\n** REGISTRA UNA NUEVA NOTA **')
    while True:
        fecha_actual = datetime.date.today()
        nombre_cliente = input('\nIngrese el nombre del cliente: ')
        print("\n---------------------------------------------")
        print('            SERVICIOS DISPONIBLES')
        print("---------------------------------------------")
        servicios = {
            1: ('Afinación mayor', 2200),
            2: ('Servicio de frenos', 2000),
            3: ('Servicio de balatas traseros', 1387),
            4: ('Transmisiones', 3500),
            5: ('Cambio de llantas', 800)
        }
        for clave, (nombre_servicio, precio) in servicios.items():
            print(f'({clave}) {nombre_servicio} -------${precio}')

        total = 0
        detalle_nota = []

        while True:
            servicio = input('\nIngrese el número del servicio que se solicitó: ')
            try:
                servicio = int(servicio)
                if servicio in servicios:
                    nombre_servicio, precio = servicios[servicio]
                    detalle_nota.append((nombre_servicio, precio))
                    total += precio
                else:
                    print('\n*Opción no válida. Ingrese un número de servicio válido*')
            except ValueError:
                print('\n*Solamente se aceptan números enteros*')

            servicio_n = input('¿Desea agregar otro servicio? (S)i (N)o: ')
            if servicio_n.lower() != 's':
                break

        nueva_nota = (fecha_actual, nombre_cliente, total, detalle_nota)
        notas[len(notas) + 1] = nueva_nota

        print(f'\nNota Agregada: {nueva_nota}')

        agregar_nota = input('¿Desea registrar otra nota? (S)i (N)o: ')
        if agregar_nota.lower() != 's':
            print("\n** NOTA(S) REGISTRADA CORRECTAMENTE **")
            break

def recuperar_nota():
    print('\n** RECUPERAR UNA NOTA CANCELADA **')
    if not notas_canceladas:
        print("No hay notas canceladas para recuperar.")
        return

    print("\nListado de notas canceladas:")
    for folio in notas_canceladas:
        fecha, nombre, total, _ = notas[folio]
        print(f"Folio: {folio}, Fecha: {fecha}, Cliente: {nombre}, Total: ${total:.2f}")

    while True:
        folio_recuperar = input("Ingrese el folio de la nota a recuperar (o 0 para cancelar): ")
        try:
            folio_recuperar = int(folio_recuperar)
            if folio_recuperar in notas_canceladas:
                notas_canceladas.remove(folio_recuperar)
                print(f"Nota {folio_recuperar} recuperada.")
                break
            elif folio_recuperar == 0:
                print("Cancelación de recuperación de nota.")
                break
            else:
                print("El folio ingresado no corresponde a una nota cancelada.")
        except ValueError:
            print("Por favor, ingrese un número válido o 0 para cancelar.")

def consulta_periodo():
    print('\n** CONSULTA POR PERÍODO **')
    fecha_inicial = datetime.date.today()
    fecha_final = datetime.date.today()

    while True:
        try:
            fecha_inicial = datetime.datetime.strptime(input("Ingrese la fecha inicial (AAAA-MM-DD): "), "%Y-%m-%d").date()
            fecha_final = datetime.datetime.strptime(input("Ingrese la fecha final (AAAA-MM-DD): "), "%Y-%m-%d").date()
            if fecha_final < fecha_inicial:
                print("La fecha final debe ser mayor o igual que la fecha inicial.")
            else:
                break
        except ValueError:
            print("Formato de fecha incorrecto. Utilice el formato AAAA-MM-DD.")

    notas_periodo = []
    for folio, (fecha, nombre, total, _) in notas.items():
        if fecha_inicial <= fecha <= fecha_final:
            notas_periodo.append((folio, fecha, nombre, total))

    if not notas_periodo:
        print(f"No hay notas emitidas para el período de {fecha_inicial} a {fecha_final}.")
    else:
        print("\nListado de notas en el período:")
        for folio, fecha, nombre, total in notas_periodo:
            print(f"Folio: {folio}, Fecha: {fecha}, Cliente: {nombre}, Total: ${total:.2f}")

def cancelar_nota():
    while True:
        folio_cancelar = input("Ingrese el folio de la nota a cancelar o escriba 'q' si quiere regresar al menú principal: ")

        if folio_cancelar.lower() == 'q':
          return

        try:
            folio_cancelar = int(folio_cancelar)
            if folio_cancelar in notas and folio_cancelar not in notas_canceladas:
                fecha, nombre, total, detalle_nota = notas[folio_cancelar]
                print(f'Folio: {folio_cancelar}')
                print(f'Fecha: {fecha}')
                print(f'Nombre del cliente: {nombre}')
                print(f'Total: ${total:.2f} pesos')
                print('Servicios:')
                for servicio in detalle_nota:
                    nombre_servicio, costo_servicio = servicio
                    print(f'- Nombre: {nombre_servicio}')
                    print(f'  Costo: ${costo_servicio:.2f} pesos')

                confirmacion = input("¿Desea cancelar esta nota? (S/N): ").strip().lower()
                if confirmacion == "s":
                    notas_canceladas.append(folio_cancelar)
                    print("Nota cancelada.")
                else:
                    print("Cancelación de nota abortada.")
                    continue
            else:
                print("La nota no existe o ya está cancelada.")
        except ValueError:
            print("Por favor, ingrese un número válido.")

def consulta_folio():
    folio_consulta = validar_entero("Ingrese el folio de la nota que desea buscar: ")
    if folio_consulta in notas and folio_consulta not in notas_canceladas:
        fecha, nombre, total, detalle_nota = notas[folio_consulta]
        print(f'\n** NOTA CONSULTADA **')
        print("--------------------------------")
        print(f"Folio: {folio_consulta}:")
        print(f"Fecha: {fecha}")
        print(f"Nombre del cliente: {nombre}")
        print(f"Total: ${total:,.2f} pesos")
        print("Detalle de la nota:")

        for servicio in detalle_nota:
            nombre_servicio, costo_servicio = servicio
            print(f"- Servicio: {nombre_servicio}")
            print(f"  Costo: ${costo_servicio:,.2f} pesos")
    else:
        print("La nota no existe o ya está cancelada.")

def menu_principal():
    while True:
        print("\n---------------------------------------------")
        print("       MENÚ PRINCIPAL TALLER MECÁNICO         ")
        print("---------------------------------------------")
        print("1. Registrar una nota")
        print("2. Consultas y reportes")
        print("3. Cancelar una nota")
        print("4. Recuperar una nota")
        print("5. Salir")

        opcion = validar_entero("\nIngrese el número de la operación que desea realizar: ")

        if 1 <= opcion <= 5:
            if opcion == 1:
                registrar_notas()
            elif opcion == 2:
                submenu_consultas()
            elif opcion == 3:
                cancelar_nota()
            elif opcion == 4:
                recuperar_nota()
            elif opcion == 5:
                print("\n*Has salido del sistema*")
                break
        else:
            print('\n*Opción no válida. Ingrese el número de alguna opción mostrada*')

def submenu_consultas():
    while True:
        print("\n---------------------------------------------")
        print("        SUBMENÚ CONSULTAS Y REPORTES")
        print("---------------------------------------------")
        print("1. Consulta por período")
        print("2. Consulta por folio")
        print("3. Regresar al menú principal")

        subopcion = validar_entero("\nIngrese el número de la operación que desea realizar: ")

        if 1 <= subopcion <= 3:
            if subopcion == 1:
                consulta_periodo()
            elif subopcion == 2:
                consulta_folio()
            elif subopcion == 3:
                return
        else:
            print('\n*Opción no válida. Ingrese el número de alguna opción mostrada*')

menu_principal()