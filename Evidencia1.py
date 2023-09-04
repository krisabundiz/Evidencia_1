import datetime

class Nota:
    def _init_(self, folio, fecha, cliente):
        self.folio = folio
        self.fecha = fecha
        self.cliente = cliente
        self.servicios = []
        
notas = []
folio_actual = 1
notas_canceladas = [] 


##Cancelar notas
def cancelar_nota():
    folio_cancelar=int(input("Ingrese el folio de la nota a cancelar:"))
    
    for  nota in notas:
        if nota.folio==folio_cancelar and nota not in notas_canceladas:
            print("Folio:", nota.folio)
            print("Fecha", nota.fecha)
            print("Cliente:", nota.cliente)
            print("Monto a pagar:", nota.calcular_monto_total())
            print("Servicios:")
            for servicio in nota.servicios:
                print("- Nombre:", servicio.nombre)
                print("  Costo:", servicio.costo)
            
            confirmacion = input("¿Desea cancelar esta nota? (S/N): ")
            if confirmacion.lower() == "s":
                notas_canceladas.append(nota)
                print("Nota cancelada.")
            else:
                print("Cancelación de nota abortada.")
            return
    print("La nota no existe o ya está cancelada.")
        

##Consulta por folio
def consulta_folio():
    folio_consulta=int(input("Ingrese el folio de la nota que desea buscar: "))

    for nota in notas:
        if nota.folio == folio.consulta and nota not in notas_canceladas:
          print ("Folio: ", nota.folio)
          print ("Fecha: ", nota.fecha)
          print ("Cliente: ", nota.cliente)
          print ("Detalle de la nota: ")
          for servicio in nota.servicios:
            print ("- Nombre del servicio: ", servicio.nombre)
            print ("- Costo del servicio: ", servicio.costo)
          return
    print ("La nota consultada no existe o corresponde a una nota cancelada.")

def menu_principal():
    while True:
        print("\n---------------------------------------------")
        print("       MENÚ PRINCIPAL TALLER MECANICO         ")
        print("---------------------------------------------")
        print("1. Registrar una nota")
        print("2. Consultas y reportes")
        print("3. Cancelar una nota")
        print("4. Recuperar una nota")
        print("5. Salir")
        try:
            opcion = int(input("\nIngrese el número de la operación que desea realizar: "))
        except Exception:
            print('\n**Solamente se aceptan dígitos**')
        else:
            if 1 <= opcion <= 5:
                if opcion == 1:
                    registro_notas()
                elif opcion == 2:
                    submenu_consultas()
                elif opcion == 3:
                    cancelar_nota()
                elif opcion == 4:
                    recuperar_nota()
                elif opcion == 5:
                    print("\n**Has salido del sistema*")
                    break
            else:
                print('\n**Opción no valida. Ingrese el número de alguna opción mostrada**')

def submenu_consultas():
    while True:
        print("\n---------------------------------------------")
        print("        SUBMENÚ CONSULTAS Y REPORTES")
        print("---------------------------------------------")
        print("1. Consulta por período")
        print("2. Consulta por folio")
        print("3. Regresar al menú principal")
        try:
            subopcion = int(input("\nIngrese el número de la operación que desea realizar: "))
        except Exception:
            print('\n**Solamente se aceptan dígitos**')
        else:
            if 1 <= subopcion <= 3:
                if subopcion == 1:
                    consulta_periodo()
                elif subopcion == 2:
                    consulta_folio()
                elif subopcion == 3:
                    return  
            else:
                print('\n**Opción no válida. Ingrese el número de alguna opción mostrada**')
